#!/usr/bin/env bash

set -eux

echo $(pwd)
echo "$HOME"
echo $(ls)

ansible-playbook playbook.yml "$@"