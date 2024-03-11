#!/usr/bin/env bash

set -eux

echo "$GITHUB_WORKSPACE"

ansible-playbook playbook.yml "$@"