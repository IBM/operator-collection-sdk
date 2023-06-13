# Operator Collection Development Guide <!-- omit from toc -->

## Table of Contents
- [Testing changes in a forked repo](#testing-changes-in-a-forked-repo)
  - [Installing local collection](#installing-local-collection)
  - [Installing from forked GitHub repo](#installing-from-forked-github-repo)
- [Executing GitHub Workflows in a forked GitHub repo](#executing-github-workflows-in-a-forked-github-repo)
- [Ansible Molecule Setup](#ansible-molecule-setup)
- [Writing Molecule Tests](#writing-molecule-tests)

# Testing changes in a forked repo
When working in a forked repository, there may be times where performing the `ansible-playbook` command from within the OC SDK collection is restricted, since most playbooks are required to be executed from the root of another Operator Collection. This requires that the OC SDK collection be installed globally, and below are the steps to do so.

## Installing local collection
From the `operator-collection-sdk/ibm` directory issue the following command:
```bash
ansible-galaxy collection install ./operator_collection_sdk -f
```

## Installing from forked GitHub repo
```bash
BRANCH_NAME=$(git branch | grep -F '*' | cut -d ' ' -f2)
REPO_URL=$(git config --get remote.origin.url)
ansible-galaxy collection install git+${REPO_URL}#ibm/operator_collection_sdk,${BRANCH_NAME} -f
```

# Executing GitHub Workflows in a forked GitHub repo
GitHub doesn't allow GitHub workflow Secrets to be passed to forked repositories. Since the current Ansible Molecule tests require access to an Openshift cluster, you are required to configure the following two variables in your workspace before successfully executing an end to end test of your changes.

- Navigate to `Setting > Secrets and variables > Actions` and click the "New repository secret" button
![GitHub Settings](images/GitHub%20Settings.png)
- Configure the `OPENSHIFT_SERVER` secret. This value can be retrieved using the following command:
    ```bash
    oc config view --minify -o jsonpath='{.clusters[*].cluster.server}'
    ```
- Generate a new Service Account token in Openshift and configure the `OPENSHIFT_TOKEN` secret in GitHub. Follow the steps below to generate a token with the proper access in the cluster
    ```bash
    oc create sa github -n default
    oc adm policy add-cluster-role-to-user cluster-admin -z github -n default
    TOKEN=$(oc sa new-token github -n default)
    echo ${TOKEN}
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
Below are a few links I'd recommend to review to get started with Ansible Molecule: 

Ansible Molecule Overview: https://www.toptechskills.com/ansible-tutorials-courses/rapidly-build-test-ansible-roles-molecule-docker/

Video Tutorial on Molecule playbook testing: https://www.youtube.com/watch?v=CYghlf-6Opc
