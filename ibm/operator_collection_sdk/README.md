# Overview <!-- omit from toc -->
The IBM Operator Collection SDK is used to assist in the end to end deployment of your Ansible collection during the development lifecycle using IBM® z/OS® Cloud Broker Kubernetes API's. This collection provides the automation to deploy an operator in your namespace that contains your latest Ansible collection modifications, quickly redeploy your local modifications in seconds, and delete the operator once development is complete.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Ansible Galaxy Installation](#ansible-galaxy-installation)
  - [GitHub Installation](#github-installation)
  - [IBM Cloud Container Registry Installation](#ibm-cloud-container-registry-installation)
- [Setup](#setup)
- [Initializing your Operator Collection](#initializing-your-operator-collection)
  - [Initializing a new Operator Collection](#initializing-a-new-operator-collection)
  - [Generating an operator-config.yml in an existing Ansible Collection](#generating-an-operator-configyml-in-an-existing-ansible-collection)
  - [Converting an existing Operator Collection to execute in an offline OpenShift environment](#converting-an-existing-operator-collection-to-execute-in-an-offline-openshift-environment)
- [Usage Examples](#usage-examples)
  - [Creating the initial operator on the OpenShift cluster](#creating-the-initial-operator-on-the-openshift-cluster)
  - [Re-deploying your Ansible Collection after making local playbook/role modifications](#re-deploying-your-ansible-collection-after-making-local-playbookrole-modifications)
  - [Re-deploying your Ansible Collection after making local playbook/role modifications, and modifications to your operator-config file](#re-deploying-your-ansible-collection-after-making-local-playbookrole-modifications-and-modifications-to-your-operator-config-file)
  - [Creating a credential Secret from within the Operator container](#creating-a-credential-secret-from-within-the-operator-container)
  - [Deleting the Operator](#deleting-the-operator)
- [Tips](#tips)
  - [Configure alias commands to simplify playbook execution](#configure-alias-commands-to-simplify-playbook-execution)
  - [Configure extra-vars file to bypass prompts](#configure-extra-vars-file-to-bypass-prompts)
  - [Suppress playbook warning messages](#suppress-playbook-warning-messages)

# Prerequisites
- [OpenShift Cluster (version 4.10 or later)][openshift]
- [OpenShift Command Line Interface (CLI)][openshift-cli]
- [Ansible CLI Tools (version 2.7 or later)][ansible]
- [Kubernetes Python Client][kubernetes]
- [z/OS Cloud Broker v2.2.0+][broker]
- [z/OS Cloud Broker Encryption CLI][cli] (optional)
  
# Installation
The IBM Operator Collection SDK can be installed directly from GitHub, or via docker image stored in the IBM Cloud Container Registry

## Ansible Galaxy Installation
Run the following command to install the collection from Ansible Galaxy

```bash
ansible-galaxy collection install ibm.operator_collection_sdk
```

## GitHub Installation
Run the following command to install the collection from GitHub.

```bash
ansible-galaxy collection install git+https://github.com/IBM/operator-collection-sdk.git#ibm/operator_collection_sdk -f
```

## IBM Cloud Container Registry Installation
Run the following commands to download and extract the collection to your local filesystem into the `./operator-collection-sdk` directory, and install the IBM Operator Collection SDK collection into your default collection path:

```bash
mkdir -vp operator-collection-sdk/
oc image extract icr.io/zmodstack/operator-collection-sdk:latest --path /:operator-collection-sdk/ --confirm
ansible-galaxy collection install ./operator-collection-sdk/ibm/operator_collection_sdk -f
```

# Setup
The following steps are required prior to deploying your operator in OpenShift using the IBM Operator Collection SDK playbooks:

1. Install the z/OS Cloud Broker Operator in your namespace and create an instance of `ZosCloudBroker`.
2. Log into the OpenShift cluster from the command line and run the `oc project` command to navigate to the project where the z/OS Cloud Broker Operator is installed.

# Initializing your Operator Collection
Below are the steps to initialize a new operator collection, or to configure an operator collection from an existing Ansible collection.

## Initializing a new Operator Collection
Run the following command to initialize your operator collection for development.

```bash
ansible-playbook ibm.operator_collection_sdk.init_collection
```

To bypass input prompts:
```bash
ansible-playbook -e "collectionName=<collection-name> collectionNamespace=<collection-namespace> offline_install=<y/n>" ibm.operator_collection_sdk.init_collection
```

## Generating an operator-config.yml in an existing Ansible Collection
If you are planning to convert an existing Ansible Collection to an Operator Collection, then you should run the following command in the root directory of the Ansible Collection to generate the `operator-config.yml` template.

```bash
ansible-playbook ibm.operator_collection_sdk.create_operator_config
```

## Converting an existing Operator Collection to execute in an offline OpenShift environment
If this Operator Collection will be executed in an offline OpenShift environment, then you should run the command below to download the Ansible dependencies before deploying this operator to OpenShift. 

If your local environment is also offline, then you must download the required Ansible dependencies from an internet-enabled computer. Once those collections are downloaded, you should then transfer those files to the offline computer, and store them in the `./collections` directory before executing the following command.

```bash
ansible-playbook ibm.operator_collection_sdk.create_offline_requirements
```


# Usage Examples
**Note:** To execute this playbook, it is required that your are in the root directory of the collection that you are developing, with a valid `galaxy.yml` and `operator-config.yml` file in the same directory

## Creating the initial operator on the OpenShift cluster
1. Run the following command to create the operator on the cluster

```bash
ANSIBLE_JINJA2_NATIVE=true ansible-playbook ibm.operator_collection_sdk.create_operator
```
2. Once prompted, enter the name, host, and port of the `ZosEndpoint` to execute your collection against

**Note:** You can also pass the required variable as extra vars to bypass input prompts:
```bash
ANSIBLE_JINJA2_NATIVE=true ansible-playbook -e "zosendpoint_name=<endpoint-name> zosendpoint_host=<host> zosendpoint_port=<port> username=<user> ssh_key=<ssh-key-path> passphrase=''" ibm.operator_collection_sdk.create_operator
```

## Re-deploying your Ansible Collection after making local playbook/role modifications

In the event where modifications are needed to your collection, you can run the following command to quickly apply those modifications to your operator

```bash
ansible-playbook ibm.operator_collection_sdk.redeploy_collection
```

## Re-deploying your Ansible Collection after making local playbook/role modifications, and modifications to your operator-config file

In the event where modifications are needed to your collection AND your `operator-config.yml` file (i.e. adding new input variables), the operator would then need to be reconfigured and reinstalled to account for these new operator-config changes. To pick up these changes, you should run the following command to redeploy your operator

```bash
ansible-playbook ibm.operator_collection_sdk.redeploy_operator
```

## Creating a credential Secret from within the Operator container

If you're currently unable to install the [z/OS Cloud Broker Encryption CLI][cli], you also have the option to generate these encrypted credentials using the `zoscb-encrypt` CLI within the operator container. 

Run the following command to generate encrypted credentials in the current Namespace.

```bash
ansible-playbook ibm.operator_collection_sdk.create_credential_secret
```

**Note:** Creating encrypted credentials with passphrases are currently not supported via the IBM Operator Collection SDK.

## Deleting the Operator
Run the following command to uninstall the operator.

```bash
ansible-playbook ibm.operator_collection_sdk.delete_operator
```


# Tips
## Configure alias commands to simplify playbook execution 
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
alias ocsdk-init="ansible-playbook ibm.operator_collection_sdk.init_collection"
alias ocsdk-create-offline-requirements="ansible-playbook ibm.operator_collection_sdk.create_offline_requirements"
alias ocsdk-create-operator-config="ansible-playbook ibm.operator_collection_sdk.create_operator_config"
alias ocsdk-install="ansible-galaxy collection install git+https://github.com/IBM/operator-collection-sdk.git#ibm/operator_collection_sdk -f"
alias ocsdk-create-operator="ANSIBLE_JINJA2_NATIVE=true ansible-playbook ibm.operator_collection_sdk.create_operator"
alias ocsdk-redeploy-collection="ansible-playbook ibm.operator_collection_sdk.redeploy_collection"
alias ocsdk-redeploy-operator="ansible-playbook ibm.operator_collection_sdk.redeploy_operator"
alias ocsdk-delete-operator="ansible-playbook ibm.operator_collection_sdk.delete_operator"
alias ocsdk-create-credential-secret="ansible-playbook ibm.operator_collection_sdk.create_credential_secret"
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
[openshift-cli]:https://docs.openshift.com/container-platform/4.13/cli_reference/openshift_cli/getting-started-cli.html#cli-installing-cli-web-console_cli-developer-commands
[ansible]:https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#pip-install
[cli]:https://www.ibm.com/docs/en/cloud-paks/z-modernization-stack/2023.1?topic=credentials-installing-zoscb-encrypt-cli-tool
[kubernetes]:https://github.com/kubernetes-client/python#installation
[broker]:https://ibm.biz/ibm-zoscb-install

## Configure ocsdk-extra-vars file to bypass prompts
If you find yourself inputting vars_prompts frequently, create an `ocsdk-extra-vars.yaml` file. If `create_operator.yml` detects this file, it will automatically use it.

Example `ocsdk-extra-vars.yaml` file:

```yaml
zosendpoint_type: remote
zosendpoint_name: my-endpoint
zosendpoint_host: 1.2.3.4
zosendpoint_port: '22'
username: user
ssh_key: ~/.ssh/id_rsa
passphrase: my_ssh_passphrase
```

Note: We do not recommend explicitly specifying passphrases in this file as they should be passed through the vars prompt. If the passphrase is specified however, we recommend that the `ocsdk-extra-vars.yaml` file be added to your `.gitignore` file to prevent the exposure of your passphrase on Github.

## Suppress playbook warning messages
Set the following environment variables to suppress the WARNING messages listed below when executing playbooks within the IBM Operator Collection SDK collection.

```console
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'
```

```bash
export ANSIBLE_LOCALHOST_WARNING=false
export ANSIBLE_INVENTORY_UNPARSED_WARNING=false
```
