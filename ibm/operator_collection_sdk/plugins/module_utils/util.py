# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import subprocess
from re import findall
from json import loads


def get_collection_root_path():
    error = None
    collections_root_path = None

    # check defaults
    default_paths = [
        "/usr/share/ansible/collections/ansible_collections",
        os.path.expanduser("~/.ansible/collections/ansible_collections")
    ]
    for path in default_paths:
        candidate = os.path.join(path, "ibm", "operator_collection_sdk")
        if os.path.exists(candidate):
            collections_root_path = candidate
            break

    # attempt to derive path from shell
    if collections_root_path is None:
        try:
            command = ["ansible-config dump"]
            stdout = subprocess.run(command, shell=True, text=True, capture_output=True, check=True).stdout

            # filter output for COLLECTIONS_PATHS = [*]
            match = findall(r"COLLECTIONS_PATHS[^=]*= [^\]]*\]", stdout)
            del stdout

            if len(match) > 0:
                string_paths = match[0].split("=")[1].strip()

                # valid json must be double quoted for json.loads
                possible_paths = loads(string_paths.replace('\'', "\""))

                for path in possible_paths:
                    candidate = os.path.join(path, "ansible_collections", "ibm", "operator_collection_sdk")
                    if os.path.exists(candidate):
                        collections_root_path = candidate
                        break
        except Exception as e:
            error = str(e)

    return collections_root_path, error
