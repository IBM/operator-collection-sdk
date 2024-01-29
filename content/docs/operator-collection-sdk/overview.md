---
weight: 1000
title: "Overview" # <!-- omit from toc -->
description: "This collection provides the automation to deploy an operator in your namespace that contains your latest Ansible collection modifications, quickly redeploy your local modifications in seconds, and delete the operator once development is complete."
icon: "overview_key"
date: "2024-01-15T13:19:10-08:00"
lastmod: "2024-01-15T13:19:10-08:00"
draft: false
toc: true
---

<!-- ## IBM Operator Collection SDK -->

<!-- ### Table of Contents
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
  - [Suppress playbook warning messages](#suppress-playbook-warning-messages) -->

---
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
[![Test](https://github.com/IBM/operator-collection-sdk/actions/workflows/test.yml/badge.svg?event=push)](https://github.com/IBM/operator-collection-sdk/actions/workflows/test.yml)
[![Release](https://github.com/IBM/operator-collection-sdk/actions/workflows/release.yml/badge.svg)](https://github.com/IBM/operator-collection-sdk/actions/workflows/release.yml)

The IBM Operator Collection SDK provides the resources and tools that are needed to develop Operator Collections against the IBM® z/OS® Cloud Broker which is part of the IBM Z® and Cloud Modernization Stack.

Operator Collections are simply [Ansible Collections](https://www.ansible.com/blog/getting-started-with-ansible-collections) that are dynamically converted to [Ansible Operators](https://www.ansible.com/blog/ansible-operator) in Openshift when imported in the [IBM® z/OS® Cloud Broker](https://ibm.biz/ibm-zoscb-install). This allows you to write any [Ansible Playbook](https://docs.ansible.com/ansible/2.9/user_guide/playbooks_intro.html), develop and iterate on it locally, publish to Openshift, and expose a catalog of statefully managed new services.

The IBM Operator Collection SDK simplifies the development of these Operator Collections by providing:
- The ability to scaffold a new Operator Collection with a preconfigured set of requirements
- The ability to quickly debug your Ansible automation in an operator in Openshift, using a local build of your latest Ansible modifications

This project also provides the documented Operator Collection specification, along with a tutorial to guide you along the development process.

<!-- ## Prerequisites
---
- [Openshift Cluster (version 4.10 or later)][openshift]
- [OpenShift Command Line Interface (CLI)][openshift-cli]
- [Ansible CLI Tools (version 2.7 or later)][ansible]
- [Kubernetes Python Client][kubernetes]
- [z/OS Cloud Broker v2.2.0+][broker]
- [z/OS Cloud Broker Encryption CLI][cli] (optional)
   -->

[openshift]:https://www.redhat.com/en/technologies/cloud-computing/openshift
[openshift-cli]:https://docs.openshift.com/container-platform/4.13/cli_reference/openshift_cli/getting-started-cli.html#cli-installing-cli-web-console_cli-developer-commands
[ansible]:https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#pip-install
[cli]:https://www.ibm.com/docs/en/cloud-paks/z-modernization-stack/2023.1?topic=credentials-installing-zoscb-encrypt-cli-tool
[kubernetes]:https://github.com/kubernetes-client/python#installation
[broker]:https://ibm.biz/ibm-zoscb-install