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

echo "Tearing Down Cluster Environment after Integration Tests..."
ANSIBLE_JINJA2_NATIVE=true ansible-playbook "$collection_root"/playbooks/molecule/cluster_clean.yml \
    --extra-vars @"$collection_root"/tests/integration/integration_config.yml

exit_status="$?"
if [[ ${exit_status} != 0 ]]; then
    echo -e "\n\033[1;31m Failed to tear down cluster environment after Integration Tests! Review logs. \033[00m"
fi

exit "$exit_status"