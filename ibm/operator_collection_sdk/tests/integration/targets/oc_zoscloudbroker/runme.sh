#!/usr/bin/env bash

set -eux

echo $(pwd)
echo "$HOME"
echo $(ls)
echo $(ls ..)
echo $(ls ../..)

echo $(cat ../../integration.cfg)

ansible-playbook playbook.yml "$@"