#!/usr/bin/env bash


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



# ansible-test integration should detect the integration_config.yml file
# but it fails to. Temporarily, we'll copy the contents into the targets
for target in $(ls "$collection_root/tests/integration/targets"); do
    target_path="$collection_root/tests/integration/targets/$target"
    if [[ -f "$target_path/vars/main.yml" ]]; then
        while read -r line;
        do
            if [[ "$line" =~ "---" ]]; then
                continue
            fi
            var_name=${line%%:*}
            if grep -q "$var_name" "$target_path/vars/main.yml"; then
                # var exists
                echo "Var '$var_name' already exists for target '$target'. Skipping Copy."
                continue
            else
                echo "Coppying '$var_name'"
                echo "$line" >> "$target_path/vars/main.yml"
            fi
        done < "$collection_root/tests/integration/integration_config.yml"
    else
        mkdir "$target_path/vars"
        cat "$collection_root/tests/integration/integration_config.yml" >> "$target_path/vars/main.yml"
    fi
done
