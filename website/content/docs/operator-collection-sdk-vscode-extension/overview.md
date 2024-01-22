---
weight: 100
title: "Overview"
description: ""
icon: "article"
date: "2024-01-15T13:21:07-08:00"
lastmod: "2024-01-15T13:21:07-08:00"
draft: true
toc: true
---
# IBM Operator Collection SDK for VS Code
---

## Getting Started
---

{{< alert context="warning" text="This extension is not supported on Windows OS." />}}

The IBM Operator Collection SDK extension simplifies the Operator Collection development experience by allowing you to manage the deployment of your operator in OpenShift and debug direcly from your VS Code editor.

[Install the VS Code Extension for the IBM Operator Collection SDK](https://marketplace.visualstudio.com/items?itemName=IBM.operator-collection-sdk)

## Features
---

### Deploy your operator to OpenShift with single-click actions

Single-click actions to Create, Re-deploy, and Delete your operator in OpenShift.

![Deploy and manage operator](images/vs-code-extension/oc-sdk-actions.png)

### Monitor your operator status & resources directly from your VS Code editor

- Display the status of the operator pod, and each container within the pod.
- Download and view container logs directly from your VS Code editor.

![Download logs](images/vs-code-extension/oc-sdk-download-logs.gif)

- Display the status of the OpenShift resources created to generate your operator (`OperatorCollections`, `SubOperatorConfigs`, `ZosEndpoints`).
- Create and monitor the Custom Resources for your operator.

![Monitor operator status](images/vs-code-extension/oc-sdk-view-create-resources.gif)

#### Manage your OpenShift cluster connection and project

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

![Operator Collection Linter](images/vs-code-extension//oc-sdk-vs-code-linter.gif)

### How to contribute

Check out the [contributor documentation](CONTRIBUTING.md).
