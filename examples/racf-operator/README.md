# Manage RACF Users
This operator collection provides playbooks and roles which can be used to create and remove users from a z/OS system.

## Playbook Summary

- [**add-user.yml**](playbooks/add-user.yml) - Handles adding a user to z/OS. Playbook includes group configuration, granting permissions, generating passwords, creating and mounting ZFS filesystem for OMVS, transferring files and templates, creating generic profile, and creating catalog alias. Playbook is designed to be used standalone or in an Ansible Tower workflow template.
- [**remove-user.yml**](playbooks/remove-user.yml) - Handles removal of a user from z/OS. Playbook includes removal of all configuration performed in **add-user.yml**. Playbook is designed to be used standalone or in an Ansible Tower workflow template.

## Role Summary

- [**add-zos-user**](playbooks/roles/add-zos-user/README.md) - Holds tasks related to adding a z/OS user.
- [**remove-zos-user**](playbooks/roles/remove-zos-user/README.md) - Holds tasks related to removing a z/OS user.

# License
Licensed under [Apache License,
Version 2.0](https://opensource.org/licenses/Apache-2.0)