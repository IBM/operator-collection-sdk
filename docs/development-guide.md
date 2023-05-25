# Operator Collection Development Guide <!-- omit from toc -->

## Table of Contents
- [Testing changes in a forked repo](#testing-changes-in-a-forked-repo)
  - [Installing local collection](#installing-local-collection)
  - [Installing from forked Github repo](#installing-from-forked-github-repo)
- [Ansible Molecule Setup](#ansible-molecule-setup)
- [Writing Molecule Tests](#writing-molecule-tests)

# Testing changes in a forked repo
When working in a forked repository, there may be times where performing the `ansible-playbook` command from within the OC SDK collection is restricted, since most playbooks are required to be executed from the root of another Operator Collection. This requires that the OC SDK collection be installed globally, and below are the steps to do so.

## Installing local collection
From the `operator-collection-sdk/ibm` directory issue the following command:
```bash
ansible-galaxy collection install ./operator_collection_sdk -f
```

## Installing from forked Github repo
```bash
BRANCH_NAME=$(git branch | grep -F '*' | cut -d ' ' -f2)
REPO_URL=$(git config --get remote.origin.url)
ansible-galaxy collection install git+${REPO_URL}#ibm/operator_collection_sdk,${BRANCH_NAME} -f
```

# Ansible Molecule Setup
The steps below describe how to setup Ansible Molecule in a vitrual environment on your machine.
- Install virtualenv.
    ```bash
    pip install virtualenv
    ```  
- Create a vitualenv directory in your project.
    ```bash
    virtualenv ansible_venv
    ```
- Navigate to the new virtual environment directory.
    ```bash
    cd ansible_venv
    ```
- Activate the virtual environment.
    ```bash
    source bin/activate
    ```
- Install the following packages after activating the virtual environment.
    ```bash
    pip install molecule ansible docker kubernetes
    ```
- Navigate to the `playbooks` directory to execute the available Molecule scenarios. Example:
    ```bash
    cd ../playbooks
    molecule test -s init_collection
- When you are ready to exit the virtual environment, simply execute the `deactivate` command to exit.

# Writing Molecule Tests