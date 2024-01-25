---
weight: 100
title: "Overview"
description: ""
icon: "overview_key"
date: "2024-01-15T13:24:15-08:00"
lastmod: "2024-01-15T13:24:15-08:00"
draft: false
toc: true
---
<div class="alert alert-block alert-info">
<b>Tip:</b> Use blue boxes (alert-info) for tips and notes. 
If it’s a note, you don’t have to include the word “Note”.
</div>

## Getting Started
---
{{< alert context="warning" text="This extension is not supported on Windows OS." />}}

The IBM Operator Collection SDK VS Code extension simplifies the Operator Collection development experience by allowing you to manage the deployment of your operator in OpenShift and debug direcly from your VS Code editor.

**Requirements:** This VS Code extension requires the following dependencies to function:
* Install [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) version 2.9.10 or higher
* Install the [IBM Operator Collection SDK](https://galaxy.ansible.com/ui/repo/published/ibm/operator_collection_sdk/) Ansible Collection
    * To install the latest version of this collection:
    ```
    ansible-galaxy collection install ibm.operator_collection_sdk
    ```
    * Alternatively, you can install this collection via the VS Code extension upon activation.

**Installing the VS Code Extension for the IBM Operator Collection:**\
{{< tabs tabTotal="3">}}
{{% tab tabName="Visual Studio® Marketplace (Recommended)" %}}
[Install the VS Code Extension](https://marketplace.visualstudio.com/items?itemName=IBM.operator-collection-sdk) from the Visual Studio® Marketplace.
{{% /tab %}}

{{% tab tabName="From .vsix" %}}

1. Download the `.vsix` file from the latest [release](https://github.com/IBM/operator-collection-sdk-vscode-extension/releases) in the IBM Operator Collection SDK VS Code Extension repository on github.

2. Install the `.vsix` file from the Extensions tab in your VS Code editor:

![Install the .vsix file](images/vs-code-extension/install-from-vsix.png)

{{% /tab %}}

{{% tab tabName="Manual Installation" %}}
For local builds, you will first need to install [node js](https://nodejs.org/en) in order to build and deploy the extension.
1. First clone the IBM Operator Collection SDK VS Code Extension repository on github:
    ```
    git clone https://github.com/IBM/operator-collection-sdk-vscode-extension.git \
    && cd operator-collection-sdk-vscode-extension
    ```
2. Install the extension dependencies:
    ```
    npm install
    ```
3. Build the `.vsix` file:
    ```
    npm run build
    ```
4. Deploy the extension to your VS Code editor:
    ```
    npm run deploy
    ```
{{% /tab %}}
{{< /tabs >}}

## Features
---

### Deploy your operator to OpenShift with single-click actions

- Single-click actions to Create, Re-deploy, and Delete your operator in OpenShift.

![Deploy and manage operator](images/vs-code-extension/oc-sdk-actions.png)

### Monitor your operator status & resources directly from your VS Code editor

- Display the status of the operator pod, and each container within the pod.
- Download and view container logs directly from your VS Code editor.

![Download logs](images/vs-code-extension/oc-sdk-download-logs.gif)

- Display the status of the OpenShift resources created to generate your operator (`OperatorCollections`, `SubOperatorConfigs`, `ZosEndpoints`).
- Create and monitor the Custom Resources for your operator.

![Monitor operator status](images/vs-code-extension/oc-sdk-view-create-resources.gif)

### Manage your OpenShift cluster connection and project

Configure your OpenShift server URL, and select your OpenShift Project directly from your VS Code editor

![OpenShift configuration](images/vs-code-extension/oc-cluster-login-url-and-token.gif)

### Quickly generate operator collections and files from scratch using the sub-menu

- Initialize new operator collections in seconds
- Scaffold `operator-config`, `galaxy`, and `playbook` boilerplate files.
- Convert a collection to air-gapped collection using single-click actions

![Scaffold collection](images/vs-code-extension/oc-sdk-scaffold-collection.gif)

### Dynamic linting and code completion

- Instant `operator-config` validation and code completion
- Display `operator-config` property descriptions

![Operator Collection Linter](images/vs-code-extension/oc-sdk-vs-code-linter.gif)
