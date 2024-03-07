#!/usr/bin/env bash

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

function parseCommandLine {
    for arg in "$@"; do
        case $arg in
            -i=*|--install-collection=*)
                install_collection=${arg#*=}
                break
        ;;
            -i|--install-collection)
                install_collection=true
                break
        ;;
            *)
                echo "Unrecognized option: $arg"
                echo "Usage: [--install-collection=<true|false>] (alias: [-i=<true|false>]), default: true"
                exit 1;
        ;;
        esac
    done

    if [[ $(echo "${install_collection}" | tr '[:upper:]' '[:lower:]') == "true" ]]; then
        install_collection=true
    else
        install_collection=false
    fi
}


install_collection=true
parseCommandLine "$@"


# get collection root path
cwd=$(pwd)
collection_path=""
if [[ ${cwd} =~ "ibm/operator_collection_sdk" ]]; then
    collection_path=$(echo ${cwd} | sed -e 's/ibm\/operator_collection_sdk.*$/ibm\/operator_collection_sdk/')
else
    echo -e "\n\033[1;31m Expected script to be run from somewhere within '~/**/ibm/operator_collection_sdk/*' instead got '${cwd}'\033[00m"
    exit 1
fi

# Install collection locally if flag is set
if [[ "${install_collection}" == "true" ]]; then
    echo "\n\033[1;32m Installing collection locally... \033[00m"
    ansible-galaxy collection install  ${collection_path} -f
    cd ${cwd}
fi


# Populate integration_config.yml file with environment variables
ocpnamespace=""
truncate -s 0 $collection_path/tests/integration/integration_config.yml
while read -r line;
do
    if [[ "$line" =~ "#" ]]; then
        continue
    fi
    eval 'echo "'"$line"'" >> "'"$collection_path"'"/tests/integration/integration_config.yml'

    # determine ocpnamespace
    if [[ "$line" =~ "ocp_namespace" ]]; then
        l=$(eval 'echo "'"$line"'"')

        # isolate namespace | trim spaces | make lowercase | replace non-alphanumeric with "-"
        ocpnamespace=$(echo "$l" | sed -e 's/^.*:[[:space:]]*//' | sed 's/[[:space:]]*$//g' | tr '[:upper:]' '[:lower:]' | sed -e 's/[^-a-zA-Z0-9]/-/g')
        echo "ocpnamespace: $ocpnamespace" >> $collection_path/tests/integration/integration_config.yml
    fi
done < "$collection_path/tests/integration/integration_config.yml.template"


echo "Setting Up Cluster for Integration Tests...\n"
ANSIBLE_JINJA2_NATIVE=true ansible-playbook ${collection_path}/playbooks/molecule/cluster_setup.yml \
    --extra-vars "@$collection_path/tests/integration/integration_config.yml"

# Run Integration Tests
cwd=$(pwd)
exit_status=0
cd ~/.ansible/collections/ansible_collections/ibm/operator_collection_sdk
ansible-test integration -v --venv
exit_status=$(echo $?)
cd ${cwd}

if [[ ${exit_status} != 0 ]] \
&& [[ $(echo "$VIRTUAL_ENV" | awk '{print length}') != 0 ]] \
|| [[ -n "$VIRTUAL_ENV" ]]; then 
    echo -e "\n\033[1;31m Hint: Is your virtual environment still on?  If so, try turning it off (deactivate). \033[00m"
    echo -e "\033[1;31m $(echo $VIRTUAL_ENV) \033[00m\n"
    exit ${exit_status}
fi


echo "Tearing Down Cluster Environment after Integration Tests..."
ANSIBLE_JINJA2_NATIVE=true ansible-playbook ${collection_path}/playbooks/molecule/cluster_clean.yml \
    --extra-vars "@$collection_path/tests/integration/integration_config.yml"

if [[ $(echo $?) != 0 ]]; then
    echo -e "\n\033[1;31m Failed to tear down cluster environment after Integration Tests! Review logs. \033[00m"
fi

exit ${exit_status}