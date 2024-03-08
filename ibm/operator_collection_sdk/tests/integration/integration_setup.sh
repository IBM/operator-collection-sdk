#!/usr/bin/env bash

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

# get collection root path
function parseCommandLine {
    for arg in "$@"; do
        case $arg in
            --collection-root=*)
                collection_root=${arg#*=}
                break
        ;;
            *)
                echo "Unrecognized option: $arg"
                echo "Usage: [--collection-root=<path/to/collection/root>], default: ''"
                exit 1;
        ;;
        esac
    done

    if [[ "$collection_root" == "" ]]; then
        echo -e "\n\033[1;31m Error: Must supply path to --collection-root, i.e. '--collection-root=~/**/ibm/operator_collection_sdk' \033[00m"
        exit 1
    fi
}

parseCommandLine "$@"

# Populate integration_config.yml file with environment variables
ocpnamespace=""
truncate -s 0 "$collection_root"/tests/integration/integration_config.yml
while read -r line;
do
    if [[ "$line" =~ "#" ]]; then
        continue
    fi
    eval 'echo "'"$line"'" >> "'"$collection_root"'"/tests/integration/integration_config.yml'

    # determine ocpnamespace
    if [[ "$line" =~ "ocp_namespace" ]]; then
        l=$(eval 'echo "'"$line"'"')

        # isolate namespace | trim spaces | make lowercase | replace non-alphanumeric with "-"
        ocpnamespace=$(echo "$l" | sed -e 's/^.*:[[:space:]]*//' | sed 's/[[:space:]]*$//g' | tr '[:upper:]' '[:lower:]' | sed -e 's/[^-a-zA-Z0-9]/-/g')
        echo 'ocpnamespace: "'"$ocpnamespace"'"' >> "$collection_root"/tests/integration/integration_config.yml
    fi
done < "$collection_root/tests/integration/integration_config.yml.template"


printf "Setting Up Cluster for Integration Tests...\n"
ANSIBLE_JINJA2_NATIVE=true ansible-playbook "$collection_root"/playbooks/molecule/cluster_setup.yml \
    --extra-vars @"$collection_root"/tests/integration/integration_config.yml \
    -i "$collection_root"/tests/integration/inventory

exit "$?"