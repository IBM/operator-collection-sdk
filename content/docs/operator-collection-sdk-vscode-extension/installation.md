---
weight: 2200
title: "Installation"
description: "Installation guide for the IBM Operator Collection SDK extension for VS Code."
icon: "download"
date: "2024-01-26T13:45:15-08:00"
lastmod: "2024-01-26T13:45:15-08:00"
draft: false
toc: false
---

---
{{< alert context="warning" text="This extension is not supported on Windows OS." />}}

**Requirements:** This VS Code extension requires the following dependencies to function:
* [Install Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) (version 2.9.10 or higher)
* [Install the IBM Operator Collection SDK](/docs/operator-collection-sdk/installation/) Ansible Collection
    * Alternatively, you can install this collection via the VS Code extension upon activation.
* [Install the OpenShift Command Line Interface (CLI)](https://docs.openshift.com/container-platform/4.8/cli_reference/openshift_cli/getting-started-cli.html)

Depending on your environment configuration, you may also need to [install SSL Certificates](docs/operator-collection-sdk-vscode-extension/troubleshooting/#ssl-certificates), before using this extension.

**Installing the VS Code extension for the IBM Operator Collection:**\
{{< tabs tabTotal="3">}}
{{% tab tabName="Visual Studio® Marketplace (Recommended)" %}}
[Install the VS Code Extension](https://marketplace.visualstudio.com/items?itemName=IBM.operator-collection-sdk) from the Visual Studio® Marketplace.
{{% /tab %}}

{{% tab tabName="From .vsix" %}}

1. Download the `.vsix` file from the "Assests" section of the latest [release](https://github.com/IBM/operator-collection-sdk-vscode-extension/releases) in the IBM Operator Collection SDK VS Code extension repository on github.

2. Install the `.vsix` file from the "Extensions" tab in your VS Code editor:

![Install the .vsix file](images/vs-code-extension/install-from-vsix.png)

{{% /tab %}}

{{% tab tabName="From Source Code" %}}
**Additional Requirements:** For local builds, you will first need to install [node js](https://nodejs.org/en) in order to build and deploy the extension.
1. First clone the IBM Operator Collection SDK VS Code extension repository on github:
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

---
##### Experiencing Issues?
[Visit the troubleshooting page](/docs/operator-collection-sdk-vscode-extension/troubleshooting/)