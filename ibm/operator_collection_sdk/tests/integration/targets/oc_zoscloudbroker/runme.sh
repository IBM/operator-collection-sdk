#!/usr/bin/env bash

set -eux
ansible-playbook playbook.yml "$@"