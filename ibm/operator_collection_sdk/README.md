# Overview
The Operator Collection SDK is used to assist in the end to end deployment of your Ansible collection during the development lifecycle using IBM® z/OS® Cloud Broker Kubernetes API's. This collection provides the automation to deploy an operator in your namespace that contains your latest Ansible collection modifications, quickly redeploy your local modifications in seconds, and delete the operator once development is complete.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setup](#setup)
- [Initializing your Operator Collection](#initializing-your-operator-collection)
- [Usage Examples](#usage-examples)
- [Tips](#tips)

# Prerequisites
- [Openshift Cluster (version 4.10 or later)][openshift]
- [OpenShift Command Line Interface (CLI)][openshift-cli]
- [Ansible CLI Tools (version 2.7 or later)][ansible]
- [Kubernetes Python Client][kubernetes]
- [z/OS Cloud Broker v2.2.0+][broker]
- [z/OC Cloud Broker Encryption CLI][cli] (optional)
  
# Installation
The Operator Collection SDK can be installed directly from Github, or via docker image stored in the IBM Cloud Container Registry

## Github Installation
Run the following command to install the collection.

```bash
ansible-galaxy collection install git@github.com:IBM/operator-collection-sdk.git#ibm/operator_collection_sdk -f
```

## IBM Cloud Container Registry
Run the following commands to download and extract the collection to your local filesystem into the `./operator-collection-sdk` directory, and install the Opeator Collection SDK collection into your default collection path:

```bash
mkdir -vp operator-collection-sdk/
oc image extract icr.io/zmodstk-open/operator-collection-sdk:latest --path /:operator-collection-sdk/ --confirm
ansible-galaxy collection install ./operator-collection-sdk/ibm/operator_collection_sdk -f
```

# Setup
The following steps are required prior to deploying your operator in OpenShift using the Operator Collection SDK playbooks:

1. Install the z/OS Cloud Broker Operator in your namespace and create an instance of `ZosCloudBroker`.
2. Log into the OpenShift cluster from the command line and run the `oc project` command to navigate to the project where the z/OS Cloud Broker Operator is installed.

# Initializing your Operator Collection
Below are the steps to initialize a new operator collection, or to configure an operator collection from an existing Ansible collection.

## Initializing a new Operator Collection
Run the following command to initialize your operator collection for development.

```bash
ansible-playbook ibm.operator_collection_sdk.init_collection.yml 
```

To bypass input prompts:
```bash
ansible-playbook -e "collectionName=<collection-name> collectionNamespace=<collection-namespace>" ibm.operator_collection_sdk.init_collection.yml
```

## Generating an operator-config.yml in an existing Ansible Collection
Run the following command in the root directory of the Ansible collection to generate the `operator-config.yaml` template

```bash
ansible-playbook ibm.operator_collection_sdk.create_operator_config.yml
```

# Usage Examples
**Note:** To execute this playbook, it is required that your are in the root directory of the collection that you are developing, with a valid `galaxy.yml` and `operator-config.yml` file in the same directory

## Creating the initial operator on the OpenShift cluster
1. Run the following command to create the operator on the cluster

```bash
ANSIBLE_JINJA2_NATIVE=true ansible-playbook ibm.operator_collection_sdk.create_operator.yml
```
2. Once prompted, enter the name, host, and port of the `ZosEndpoint` to execute your collection against

**Note:** You can also pass the required variable as extra vars to bypass input prompts:
```bash
ANSIBLE_JINJA2_NATIVE=true ansible-playbook -e "zosendpoint_name=<endpoint-name> zosendpoint_host=<host> zosendpoint_port=<port> username=<user> ssh_key=<ssh-key-path> passphrase=''" ibm.operator_collection_sdk.create_operator.yml
```

## Re-deploying your Ansible Collection after making local playbook/role modifications

In the event where modifications are needed to your collection, you can run the following command to quickly apply those modifications to your operator

```bash
ansible-playbook ibm.operator_collection_sdk.redeploy_collection.yml
```

## Re-deploying your Ansible Collection after making local playbook/role modifications, and modifications to your operator-config file

In the event where modifications are needed to your collection AND your `operator-config.yml` file (i.e. adding new input variables), the operator would then need to be reconfigured and reinstalled to account for these new operator-config changes. To pick up these changes, you should run the following command to redeploy your operator

```bash
ansible-playbook ibm.operator_collection_sdk.redeploy_operator.yml
```

## Deleting the Operator
Run the following command to uninstall the operator

```bash
ansible-playbook ibm.operator_collection_sdk.delete_operator.yml 
```


# Tips
To simplify the commands needed to be executed, linux/mac users should consider creating an alias for each command in your bash profile.

1. Open your bash profile using the following command:

```bash
vi ~/.bash_profile
```

or 

```bash
vi ~/.zshrc
```

2. Copy the following commands to your bash profile and save:
   
```bash
alias ocsdk-init="ansible-playbook ibm.operator_collection_sdk.init_collection.yml"
alias ocsdk-create-operator-config="ansible-playbook ibm.operator_collection_sdk.create_operator_config.yml"
alias ocsdk-install="ansible-galaxy collection install git@github.com:IBM/operator-collection-sdk.git#ibm/operator_collection_sdk -f"
alias ocsdk-create-operator="ANSIBLE_JINJA2_NATIVE=true ansible-playbook ibm.operator_collection_sdk.create_operator.yml"
alias ocsdk-redeploy-collection="ansible-playbook ibm.operator_collection_sdk.redeploy_collection.yml"
alias ocsdk-redeploy-operator="ansible-playbook ibm.operator_collection_sdk.redeploy_operator.yml"
alias ocsdk-delete-operator="ansible-playbook ibm.operator_collection_sdk.delete_operator.yml"
```

3. Source your bash profile to pick up the latest changes:

```bash
source ~/.bash_profile
```
or

```bash
source ~/.zshrc
```

4. The aliases that were created can now be called instead of the full `ansible-playbook` commands

```bash
~> ocsdk-create-operator
Enter your ZosEndpoint name: 
```

[openshift]:https://www.redhat.com/en/technologies/cloud-computing/openshift
[openshift-cli]:https://docs.openshift.com/container-platform/4.12/cli_reference/openshift_cli/getting-started-cli.html
[ansible]:https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#pip-install
[cli]:https://www.ibm.com/docs/en/cloud-paks/z-modernization-stack/2023.1?topic=credentials-installing-zoscb-encrypt-cli-tool
[kubernetes]:https://github.com/kubernetes-client/python#installation
[broker]:https://ibm.biz/ibm-zoscb-install
