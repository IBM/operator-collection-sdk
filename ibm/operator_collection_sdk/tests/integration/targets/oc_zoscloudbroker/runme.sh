#!/usr/bin/env bash

set -eux

echo $(pwd)
echo "$HOME"
echo $(ls)
echo $(ls ..)
echo $(ls ../..)

echo "$GITHUB_WORKSPACE"

ansible-playbook playbook.yml "$@"