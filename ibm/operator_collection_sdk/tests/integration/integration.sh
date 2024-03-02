#!/bin/bash

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

install_collection=false

# Parse command line options
function parseCommandLine {
  for i in "$@"; do
      case $i in
          --install-collection)
              install_collection=true
      ;;
          -i)
              install_collection=true
      ;;
          *)
            echo "Unrecognized option: $i"
            printUsage;
            exit 1;
      ;;
      esac
  done
}

parseCommandLine "$@"

if [[ install_collection ]]; then
    cwd=$(pwd)
    if [[ ${cwd} =~ "ibm/operator_collection_sdk" ]]; then 
        echo "Installing collection locally..."
        echo "\n"

        collection_path=$(echo ${cwd} | sed -e 's/ibm\/operator_collection_sdk.*$/ibm\/operator_collection_sdk/g')
        ansible-galaxy collection install  ${collection_path} -f

        cd ${cwd}
    else 
        echo -e "\n\033[1;31m Expected script to be run from somewhere within '~/.../ibm/operator_collection_sdk/.../' instead got '${cwd}'\033[00m" 
        exit 1
    fi
fi

echo "Setting Up Cluster for Integration Tests...\n"
ANSIBLE_JINJA2_NATIVE=true ansible-playbook ./../playbooks/molecule/cluster_setup.yml

# Run Integration Tests
cd ~/.ansible/collections/ansible_collections/ibm/operator_collection_sdk
ansible-test integration -v --venv
exit_status=$(echo $?)

if [[ ${exit_status} != 0 ]] \
&& [[ $(echo "$VIRTUAL_ENV" | awk '{print length}') != 0 ]] \
|| [[ -n "$VIRTUAL_ENV" ]]; then 
    echo -e "\n\033[1;31m Hint: Is your virtual environment still on?  If so, try turning it off (deactivate). \033[00m"
    echo -e "\033[1;31m $(echo $VIRTUAL_ENV) \033[00m\n"
    exit ${exit_status}
fi

echo "Tearing Down Cluster after Integration Tests..."
ANSIBLE_JINJA2_NATIVE=true ansible-playbook ./../playbooks/molecule/cluster_clean.yml
if [[ $(echo $?) != 0 ]]; then
    echo -e "\n\033[1;31m Failed to tear down cluster environment after Integration Tests! Please investigate. \033[00m"
fi

exit ${exit_status}