---
weight: 200
title: "Tutorial"
description: ""
icon: "article"
date: "2024-01-18T16:50:12-08:00"
lastmod: "2024-01-18T16:50:12-08:00"
draft: true
toc: true
---

# Operator Collection Tutorial <!-- omit from toc -->

- [Prerequisites](#prerequisites)
- [Overview](#overview)
- [(Optional) Configure the IBM Operator Collection SDK Alias Commands](#optional-configure-the-ibm-operator-collection-sdk-alias-commands)
- [Install the IBM Operator Collection SDK](#install-the-ibm-operator-collection-sdk)
- [Initialize a new Operator Collection](#initialize-a-new-operator-collection)
- [Apply collection modifications](#apply-collection-modifications)
  - [Update collection requirements](#update-collection-requirements)
  - [Apply playbooks and roles](#apply-playbooks-and-roles)
  - [Update the operator-config](#update-the-operator-config)
- [Create the operator](#create-the-operator)
- [Create an instance of the operator](#create-an-instance-of-the-operator)
- [Debugging the operator](#debugging-the-operator)
- [Cleanup](#cleanup)
- [Watch the video](#watch-the-video)


# Prerequisites
- [Red Hat OpenShift Cluster (version 4.10 or later)][openshift]
- [Red Hat OpenShift Command Line Interface (CLI)][openshift-cli]
- [Ansible CLI Tools (version 2.7 or later)][ansible]
- [Kubernetes Python Client][kubernetes]
- [z/OS Cloud Broker v2.2.0+][broker]
- [z/OS Cloud Broker Encryption CLI][cli] (optional)


# Overview
This tutorial is a walkthrough of building a new operator collection that performs RACF user management against a z/OS environment. This operator will allow you to create a new user ID by creating instances in Openshift, and removing this ID once this instance is deleted.


# (Optional) Configure the IBM Operator Collection SDK Alias Commands
Alternatively, you can configure alias commands to simplify the IBM Operator Collection SDK `ansible-playbook` commands:

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
alias ocsdk-install="ansible-galaxy collection install git+https://github.com/IBM/operator-collection-sdk.git#ibm/operator_collection_sdk -f"
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

# Install the IBM Operator Collection SDK
To install the latest version of IBM Operator Collection SDK, run the following command:

```bash
ansible-galaxy collection install git+https://github.com/IBM/operator-collection-sdk.git#ibm/operator_collection_sdk -f
```

Alternatively, you can run the following alias:

```bash
ocsdk-install
```


# Initialize a new Operator Collection
To initialize a new Operator Collection, run the following command:

```bash
ansible-playbook ibm.operator_collection_sdk.init_collection.yml 
```

Alternatively, you can run the following alias:

```bash
ocsdk-init
```

Enter the collection name and Ansible Galaxy namespace when prompted. For the collection name, enter `racf_operator`. For the Ansible Galaxy namespace, enter the name of your existing namespace in Ansible Galaxy. Note that a valid Ansible Galaxy namespace is required only if you plan to publish this collection to Ansible Galaxy after completion.

After completing the previous step, an Operator Collection scaffold should appear in the `./<galaxy-namespace>/<collection-name>` directory. Navigate to this directory to proceed with the rest of this tutorial.

# Apply collection modifications
## Update collection requirements
Update the `collections/requirements.yml` file as follows to add the `ibm.ibm_zos_core` collection:

```bash
collections:
  - name: operator_sdk.util
    version: "0.4.0"
  - name: kubernetes.core
    version: "2.4.0"
  - name: ibm.ibm_zos_core
```

## Apply playbooks and roles
Clone the repo, and copy the files in the `playbooks/` directory from the [racf-operator example][racf-operator] and replace the files in your current `playbooks/` directory with the ones you copied.

The playbooks and roles in the `playbooks/` directory serve as your operator controller logic and execute every time a user creates an operator instance in Openshift.
- `add-user.yml` - This playbook creates a new user ID on the z/OS environment.
- `remove-user.yml` - This playbook removes a user ID from the z/OS environment.

**Note:** Playbooks must use the `hosts: all` parameter. Target hosts for operator collection are driven by using z/OS endpoints that are provided by the IBM® z/OS Cloud Broker. When the Ansible playbook is executed by the IBM® z/OS Cloud Broker, the `hosts: all` value is limited to the selected z/OS endpoint by setting the `--limit` flag. The IBM® z/OS Cloud Broker handles host limiting internally and no additional playbook modifications are required.

## Update the operator-config
The `operator-config.yml` file contains the necessary metadata for the IBM® z/OS Cloud Broker to configure your operator in Openshift. This file is used to configure things such as the name, description, and icon to be displayed in your operator. This is also where you will configure the name of the [custom resource][custom-resource] to be generated in Openshift. More details on configuring custom resources will be discussed in the following sections.

**Let's start by configuring the `domain`, `name`, `version`, `displayName`, and `description` of our operator:**

```bash
domain: <galaxy-namespace> # Convert underscores to dashes
name: racf-operator
version: 1.0.0
displayName: RACF Operator
description: >-
  # z/OS RACF Operator
  
  This operator allows users to create and delete user IDs on z/OS.
```

**Now let's configure our new [custom resource][custom-resource]:**

A custom resource is an object that expands the functions of the Kubernetes API or allows you to introduce your own API into a project or a cluster. In this example, we will introduce a new custom resource called `ZosUserId`. This custom resource will enable Openshift users to call our new `ZosUserId` API and create user IDs on a z/OS endpoint.

When creating our new custom resource, we also need to configure our operator with the playbook to execute when a new custom resource instance is created by the user, and the playbook to execute when the custom resource instance is deleted. This is done by supplying these playbook locations in the `playbook` and [finalizer][finalizers] fields respectively. 

```bash
resources:
  - kind: ZosUserId
    displayName: z/OS User Id
    description: A User ID managed by the RACF security facility on z/OS.
    playbook: playbooks/add-user.yml
    finalizer: playbooks/remove-user.yml
```

**Now we need to configure the variables that are needed to execute our playbooks.**

The `add-user` playbook requires two variables, `name`, and `userid`, which must be supplied by the user. The `remove-user` playbook also accepts the `userid` variable. To prompt the user for these values in Openshift, we must configure these variables in the `vars` section of our new custom resource. By doing this, the IBM® z/OS Cloud Broker can configure our operator to request these values from the user. After configuration, these values will be supplied to the playbook as "extra vars" (-e) input parameters during execution.

```bash
vars:
    - name: name
    displayName: Real Name
    description: Specifies the user name to be associated with the new user ID.
    type: string
    required: true
    - name: userid
    displayName: User ID
    description: Specifies the user to be defined to RACF.
    type: string
    required: true
```

**Last, we will supply a based64-encoded icon for our operator.**

```bash
icon:
  - base64data: >-
      PHN2ZyBpZD0iaWNvbiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB2aWV3Qm94PSIwIDAgMzIgMzIiPjxkZWZzPjxzdHlsZT4uY2xzLTF7ZmlsbDpub25lO308L3N0eWxlPjwvZGVmcz48dGl0bGU+dXNlcjwvdGl0bGU+PHBhdGggZD0iTTE2LDRhNSw1LDAsMSwxLTUsNSw1LDUsMCwwLDEsNS01bTAtMmE3LDcsMCwxLDAsNyw3QTcsNywwLDAsMCwxNiwyWiIvPjxwYXRoIGQ9Ik0yNiwzMEgyNFYyNWE1LDUsMCwwLDAtNS01SDEzYTUsNSwwLDAsMC01LDV2NUg2VjI1YTcsNywwLDAsMSw3LTdoNmE3LDcsMCwwLDEsNyw3WiIvPjxyZWN0IGlkPSJfVHJhbnNwYXJlbnRfUmVjdGFuZ2xlXyIgZGF0YS1uYW1lPSImbHQ7VHJhbnNwYXJlbnQgUmVjdGFuZ2xlJmd0OyIgY2xhc3M9ImNscy0xIiB3aWR0aD0iMzIiIGhlaWdodD0iMzIiLz48L3N2Zz4=
    mediatype: image/svg+xml
```

In the end, your `operator-config.yml` field should look similar to this [example][operator-config-example].

# Create the operator
Now that we've applied our playbooks and updated our `operator-config`, we can build our collection and create an operator in Openshift to validate our changes.

To do this, you should first install the latest release in the `v2.2` channel of the IBM® z/OS Cloud Broker in your namespace and create an instance of the `ZosCloudBroker` resource. Once the installation is successful, log in to the cluster from your command line by using the `oc login` command and validate that you are in the correct project by using the `oc project` command.

Now, you should be able to run the following command by using the IBM Operator Collection SDK to build your collection and create an operator:

```bash
ANSIBLE_JINJA2_NATIVE=true ansible-playbook ibm.operator_collection_sdk.create_operator
```

Alternatively, you can run the following alias:

```bash
ocsdk-create-operator
```

This command should now prompt you for the z/OS endpoint you would like to execute this operator against, and the SSH credentials that are needed to access this endpoint.

```bash
Enter your ZosEndpoint name: wazi-sandbox
Enter your ZosEndpoint host: ***HOST_REMOVED***
Enter your ZosEndpoint port [22]: 32281
Enter your SSH Username for this endpoint (Press Enter to skip if the zoscb-encrypt CLI isn't installed): ibmuser
Enter the path to your private SSH Key for this endpoint (Press Enter to skip if the zoscb-encrypt CLI isn't installed): ~/.ssh/id_rsa
Enter the passphrase for the SSH Key for this endpoint (Press Enter to skip if the zoscb-encrypt CLI isn't installed):
```

**Note:** SSH credentials are optional when creating the operator. If SSH credentials are not supplied, the operator is configured by using the `personal` credential type, which requires a credential to be generated by using the `zoscb-encrypt` CLI before creating an instance of the operator.

After the installation completes, you should see the RACF Operator in Openshift under Operators > Installed Operators.

![InstalledOperator](../docs/images/installed-racf-operator.png)

# Create an instance of the operator
In the installed operator in Openshift, you can now attempt to create an instance of the operator by supplying the required values and clicking `Create`.

**Note:** The initial creation will fail due to an injected failure. However, this failure will be corrected in the following debugging stage.

# Debugging the operator
There are multiple ways to debug failures in the operator. The first way would be to open the newly created instance and scroll down to the `Conditions` section to see whether a task message is displaying with a `Failed` Reason.

![Conditions](../docs/images/Conditions.png)

Another way would be to scan the `Pod` logs under Workloads > Pods > `<racf-operator-podname>`. Once you click the Logs tab in the pod, you should see the task failure displayed at the bottom of the log.

![Logs](../docs/images/pod-logs.png)

If both the `Conditions` and the `Pod` logs aren't displaying the failure, you can access the verbose logs within the container itself. To access these logs, do the following steps:
1. Click the `Terminal` within the `Pod`.
2. `cd` into the `/tmp/ansible-operator/runner/suboperator.zoscb.ibm.com/<api-version>/ZosUserId/<ocp-namespace>/<instance-name>/artifacts/latest/` directory and `cat` the `stdout` file.

To resolve this failure, you should remove the task that is named "Injecting Failure here for tutorial" in the `playbooks/roles/add-zos-user/tasks/main.yml` file.

After removing this task, run the following command to publish this playbook modification to the installed operator Pod:

```bash
ansible-playbook ibm.operator_collection_sdk.redeploy_collection
```

Alternatively, you can run the following alias:

```bash
ocsdk-redeploy-collection 
```

After the operator Pod restarts, the instance that is previously created in the namespace should reconcile automatically and create the requested user ID on the z/OS endpoint.

Next, we will add a new task to send an email containing the generated password to the user. This task will require a new variable called `email_to`, which will allow us to go through the end-to-end flow of the steps that are required to append a new variable to an existing operator. 

First, we should uncomment the task that is named "Send email containing login credentials to {{ email_to }}" in `playbooks/roles/add-zos-user/tasks/main.yml`. Then, we need to update the `operator-config.yml` file to add a new variable called `email_to`:

```bash
- name: email_to
  displayName: Email
  description: Email address to send the new user credentials
  type: string
  required: true
```

**Note:** Adding new required variables can cause an error in Openshift if there are existing instances in the namespace. This is because those instances would not have the new required variable in their `spec`. To avoid this error, you should remove all existing instances for this custom resource before applying this new configuration.

As we are updating the `operator-config` to display a new variable to the user, it is necessary to redeploy the entire operator. This should not be confused with redeploying the collection, as we have done previously. Therefore, run the following command to redeploy the entire operator:

```bash
ansible-playbook ibm.operator_collection_sdk.redeploy_operator
```

Alternatively, you can run the following alias:

```bash
ocsdk-redeploy-operator
```

After the redeploy is successful, you should be able to create a new instance and supply an email address for the credentials to be sent after completion.

![Email](../docs/images/racf-new-variable.png)

**Note:** An email will not be sent to the requested email ID because this is a fake task that simply prints a debug statement.

# Cleanup

After validating that your operator runs successfully, you can delete the operator from your namespace by running the following command:

```bash
ansible-playbook ibm.operator_collection_sdk.delete_operator
```

Alternatively, you can run the following alias:

```bash
ocsdk-delete-operator
```

# Watch The Video

Click [here][tutorial-video] to watch the video of the scenarios covered above.

[openshift]:https://www.redhat.com/en/technologies/cloud-computing/openshift
[openshift-cli]:https://docs.openshift.com/container-platform/4.12/cli_reference/openshift_cli/getting-started-cli.html
[ansible]:https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#pip-install
[cli]:https://www.ibm.com/docs/en/cloud-paks/z-modernization-stack/2023.1?topic=credentials-installing-zoscb-encrypt-cli-tool
[kubernetes]:https://github.com/kubernetes-client/python#installation
[broker]:https://ibm.biz/ibm-zoscb-install
[racf-operator]:../examples/racf-operator/playbooks/
[custom-resource]: https://docs.openshift.com/container-platform/3.11/admin_guide/custom_resource_definitions.html
[finalizers]: https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/
[operator-config-example]: ../examples/racf-operator/operator-config.yml
[tutorial-video]:https://mediacenter.ibm.com/playlist/dedicated/1_6hssue17/1_lcap76s4