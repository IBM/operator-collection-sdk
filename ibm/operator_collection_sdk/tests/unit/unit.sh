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

if [[ "${install_collection}" == "true" ]]; then
    cwd=$(pwd)
    if [[ ${cwd} =~ "ibm/operator_collection_sdk" ]]; then 
        printf "\n\033[1;32m Installing collection locally... \033[00m"
        collection_path=$(echo "${cwd}" | sed -e "s/ibm\/operator_collection_sdk.*$/ibm\/operator_collection_sdk/g")
        ansible-galaxy collection install  "${collection_path}" -f
    else 
        echo -e "\n\033[1;31m Expected script to be run from somewhere within '~/**/ibm/operator_collection_sdk/*' instead got '${cwd}'\033[00m" 
        exit 1
    fi
fi

# Run Unit Tests
cd ~/.ansible/collections/ansible_collections/ibm/operator_collection_sdk
ansible-test units -v --venv
exit_status="$?"

if [[ ${exit_status} != 0 ]] \
&& [[ $(echo "$VIRTUAL_ENV" | awk '{print length}') != 0 ]] \
|| [[ -n "$VIRTUAL_ENV" ]]; then 
    echo -e "\n\033[1;31m Hint: Is your virtual environment still on?  If so, try turning it off (deactivate). \033[00m"
    echo -e '\033[1;31m "'"$VIRTUAL_ENV"'" \033[00m\n'
    exit "$exit_status"
fi

exit "$exit_status"