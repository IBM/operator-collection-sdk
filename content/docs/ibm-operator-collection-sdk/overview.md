---
weight: 1000
title: "Overview"
description: "This collection provides the automation to deploy an operator in your namespace that contains your latest Ansible® collection modifications, quickly redeploy your local modifications in seconds, and delete the operator once development is complete."
icon: "overview_key"
date: "2024-01-15T13:19:10-08:00"
lastmod: "2024-01-15T13:19:10-08:00"
draft: false
toc: false
---

---
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
[![Test](https://github.com/IBM/operator-collection-sdk/actions/workflows/test.yml/badge.svg?event=push)](https://github.com/IBM/operator-collection-sdk/actions/workflows/test.yml)
[![Release](https://github.com/IBM/operator-collection-sdk/actions/workflows/release.yml/badge.svg)](https://github.com/IBM/operator-collection-sdk/actions/workflows/release.yml)

The IBM Operator Collection SDK provides the resources and tools that are needed to develop Operator Collections against the [IBM® z/OS® Cloud Broker](https://ibm.biz/ibm-zoscb-install) which is part of the [IBM Z® and Cloud Modernization Stack](https://www.ibm.com/products/z-and-cloud-modernization-stack).

Operator Collections are simply [Ansible Collections](https://www.ansible.com/blog/getting-started-with-ansible-collections) that are dynamically converted to [Ansible Operators](https://www.ansible.com/blog/ansible-operator) in OpenShift® when imported in the IBM® z/OS® Cloud Broker. This allows you to write any [Ansible Playbook](https://docs.ansible.com/ansible/2.9/user_guide/playbooks_intro.html), develop and iterate on it locally, publish to OpenShift, and expose a catalog of statefully managed new services.

The IBM Operator Collection SDK simplifies the development of these Operator Collections by providing:
- The ability to scaffold a new Operator Collection with a preconfigured set of requirements.
- The ability to quickly debug your Ansible automation in an operator in OpenShift, using a local build of your latest Ansible modifications.

This documentation also contains the [Operator Collection specification](/docs/ibm-operator-collection-sdk/operator-collection-specification/), along with a [tutorial](/docs/ibm-operator-collection-sdk/usage-guides/tutorial/) to guide you along the development process.