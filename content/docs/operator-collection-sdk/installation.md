---
weight: 1100
title: "Installation"
description: "Installation guide for the IBM Operator Collection SDK."
icon: "download"
date: "2024-01-26T13:44:59-08:00"
lastmod: "2024-01-26T13:44:59-08:00"
draft: true
toc: true
---

## Prerequisites
---
- [Openshift Cluster (version 4.10 or later)][openshift]
- [OpenShift Command Line Interface (CLI)][openshift-cli]
- [Ansible CLI Tools (version 2.7 or later)][ansible]
- [Kubernetes Python Client][kubernetes]
- [z/OS Cloud Broker v2.2.0+][broker]
- [z/OS Cloud Broker Encryption CLI][cli] (optional)

[openshift]:https://www.redhat.com/en/technologies/cloud-computing/openshift
[openshift-cli]:https://docs.openshift.com/container-platform/4.13/cli_reference/openshift_cli/getting-started-cli.html#cli-installing-cli-web-console_cli-developer-commands
[ansible]:https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#pip-install
[cli]:https://www.ibm.com/docs/en/cloud-paks/z-modernization-stack/2023.1?topic=credentials-installing-zoscb-encrypt-cli-tool
[kubernetes]:https://github.com/kubernetes-client/python#installation
[broker]:https://ibm.biz/ibm-zoscb-install


## Installation
---
The IBM Operator Collection SDK can be installed from Ansible Galaxy, directly from GitHub, or via docker image stored in the IBM Cloud Container Registry

{{< tabs tabTotal="3">}}
{{% tab tabName="Ansible Galaxy" %}}
Install the collection from Ansible Galaxy:
```
ansible-galaxy collection install ibm.operator_collection_sdk
```
{{% /tab %}}

{{% tab tabName="GitHub" %}}
Install the collection from GitHub.
```
ansible-galaxy collection install git+https://github.com/IBM/operator-collection-sdk.git#ibm/operator_collection_sdk -f
```
{{% /tab %}}

{{% tab tabName="IBM Cloud Container Registry" %}}
Download and extract the collection to your local filesystem into the `./operator-collection-sdk` directory, and install the IBM Operator Collection SDK collection into your default collection path:

```
mkdir -vp operator-collection-sdk/
oc image extract icr.io/zmodstack/operator-collection-sdk:latest --path /:operator-collection-sdk/ --confirm
ansible-galaxy collection install ./operator-collection-sdk/ibm/operator_collection_sdk -f
```
{{% /tab %}}
{{< /tabs >}}

<!-- ### Ansible Galaxy Installation
Run the following command to install the collection from Ansible Galaxy
```bash
ansible-galaxy collection install ibm.operator_collection_sdk
```

### GitHub Installation
Run the following command to install the collection from GitHub.
```bash
ansible-galaxy collection install git+https://github.com/IBM/operator-collection-sdk.git#ibm/operator_collection_sdk -f
```

### IBM Cloud Container Registry Installation
Run the following commands to download and extract the collection to your local filesystem into the `./operator-collection-sdk` directory, and install the IBM Operator Collection SDK collection into your default collection path:
```bash
mkdir -vp operator-collection-sdk/
oc image extract icr.io/zmodstack/operator-collection-sdk:latest --path /:operator-collection-sdk/ --confirm
ansible-galaxy collection install ./operator-collection-sdk/ibm/operator_collection_sdk -f
``` -->

#### Upgrading
Supply the `--upgrade` flag to upgrade the collection, e.g.
```
ansible-galaxy collection install ibm.operator_collection_sdk --upgrade
```

## Setup
---
The following steps are required prior to deploying your operator in OpenShift using the IBM Operator Collection SDK playbooks:

1. Install the z/OS Cloud Broker Operator in your namespace and create an instance of `ZosCloudBroker`.
2. Log into the OpenShift cluster from the command line and run the `oc project` command to navigate to the project where the z/OS Cloud Broker Operator is installed.