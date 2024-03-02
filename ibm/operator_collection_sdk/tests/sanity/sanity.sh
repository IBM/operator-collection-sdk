#!/bin/bash

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

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

Run Sanity Tests
cd ~/.ansible/collections/ansible_collections/ibm/operator_collection_sdk
ansible-test sanity -v --venv
exit_status=$(echo $?)

if [[ ${exit_status} != 0 ]] \
&& [[ $(echo "$VIRTUAL_ENV" | awk '{print length}') != 0 ]] \
|| [[ -n "$VIRTUAL_ENV" ]]; then 
    echo -e "\n\033[1;31m Hint: Is your virtual environment still on?  If so, try turning it off (deactivate). \033[00m"
    echo -e "\033[1;31m $(echo $VIRTUAL_ENV) \033[00m\n"
    exit ${exit_status}
fi

exit ${exit_status}