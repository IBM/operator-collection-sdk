#!/usr/bin/env bash

set -eux
mkdir vars
touch vars/main.yml
cp ../../integration_config.yml vars/main.yml
ansible-playbook playbook.yml "$@"