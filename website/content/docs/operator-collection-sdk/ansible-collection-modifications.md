---
weight: 1600
title: "Ansible Collection Modifications" # <!-- omit from toc -->
description: ""
icon: "box_edit"
date: "2024-01-18T16:49:28-08:00"
lastmod: "2024-01-18T16:49:28-08:00"
draft: true
toc: true
---

Additional Ansible collection modifications may be desirable for a complete native OpenShift experience. 

## Installing Dependencies
---
Ansible and Python dependencies can be installed using additional configuration files.

### Ansible Collection Dependencies
Additional Ansible collections may be necessary for your Operator Collection's dependent modules. This is also necessary for allowing your Ansible playbook to communicate with Kubernetes using the `operator_sdk.util` and `kubernetes.core` modules.

To specify additional Ansible collections as dependencies, create a `collections/requirements.yml` file at the root of your Operator Collection following the [Ansible documentation guidelines](https://docs.ansible.com/ansible/5/user_guide/collections_using.html#install-multiple-collections-with-a-requirements-file).

For example:
`collections/requirements.yml`
```yaml
collections:
  - name: operator_sdk.util
    version: "0.4.0"
  - name: kubernetes.core
  - name: ansible.utils
```

### Python Dependencies
Additional python dependencies may be necessary due to various extensions to the Ansible ecosystem. These additional python dependencies can be installed via `pip` following the `requirements.txt` file format as seen in the [`pip` documentation](https://pip.pypa.io/en/stable/reference/requirements-file-format/#). 

This file may be placed anywhere in the Operator Collection's structure. 

For example:
`python/requirements.txt`

```yaml
# Required for the ansible collection 'ansible.utils.ipaddr' depedency resolution
netaddr
```

<!-- ### Offline depedencies -->

## Playbook Modifications
---
For best compatibility with Red Hat OpenShift, some playbook modifications may be necessary.

### Target Hosts
When an [Ansible playbook](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html) is written, a set of target `hosts` must be provided at the top of an Ansible 'play'. This `hosts` selection tells the playbook which hosts to target during execution and is typically driven by an Ansible inventory file that specifies more information for these target `hosts`. 

An Operator Collection's target hosts are driven using z/OS Endpoints provided by IBM z/OS Cloud Broker. 

For this reason, the playbook MUST use the `hosts: all` value as seen below.

```yaml
- name: An example play from an ansible playbook
  hosts: all
  gather_facts: false
  ...
```

When the Ansible Playbook is executed by z/OS Cloud Broker, the `hosts: all` value is limited to the selected z/OS Endpoint by setting the [`--limit` flag](https://docs.ansible.com/ansible/latest/inventory_guide/intro_patterns.html#patterns-and-ad-hoc-commands). This is done internally by z/OS Cloud Broker and no additional playbook modifications must be made to handle host limiting.

### Dual Execution
If a playbook is intended to co-exist as both a SubOperator and a native Ansible playbook able to executed outside of Kubernetes, use the `k8s_managed` [provided variable](spec.md#provided-variables) to ensure tasks that require Kubernetes environments will not cause failures.

```yaml
- name: Retrieve all information about a Kubernetes custom resource (CR)
  kubernetes.core.k8s_info:
    api_version: "{{ k8s_cr_version }}"
    kind: DvipaReserve
    name: "{{ ansible_operator_meta.name }}"
    namespace: "{{ ansible_operator_meta.namespace }}"
  register: cr_info
  when: k8s_managed
```

### Retrieving CR data
When creating playbooks that are driven from Kubernetes Custom Resources (CRs), it is frequently necessary to retrieve the state of the CR from Kubernetes. 

To pull the full information of a Custom Resource as is currently visible in Kubernetes, use the `kubernetes.core.k8s_info` [module](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/k8s_info_module.html). 

Typically, this is only needed for scenarios when you want to retrieve the `status` of the CR or additional metadata. Additional information about the CR is also provided in the Operator Collection spec's [provided variables](spec.md#provided-variables).

You may want to understand the current values of the `status` fields to identify if this resource has been previously provisioned or if it's in some improper functional state. In these cases, use an Ansible task similar to the following example.

```yaml
- name: Retrieve all information about a Kubernetes custom resource (CR)
  kubernetes.core.k8s_info:
    api_version: "{{ k8s_cr_version }}"
    kind: DvipaReserve
    name: "{{ ansible_operator_meta.name }}"
    namespace: "{{ ansible_operator_meta.namespace }}"
  register: cr_info

  - name: Display full CR data
    ansible.builtin.debug:
      var: cr_info

  - name: Set variables for CIDR block and reserved IPs
    ansible.builtin.set_fact:
      reserved_ips: "{{ cr_info.resources[0].status.some_field }}"
```

**Note**: The example above contains Jinja variable references (`k8s_cr_version`, `ansible_operator_meta.name`, `ansible_operator_meta.namespace`) that are part of the [provided variables](spec.md#provided-variables) made avaiable to the ansible playbook when being executed as a z/OS Cloud Broker suboperator.

### Setting CR status
To make the Ansible playbooks truly part of the Kubernetes ecosystem and report updates back to the Kubernetes custom resource, usage of the `operator_sdk.utils.k8s_status` [module](https://galaxy.ansible.com/operator_sdk/util) is necessary.

This is especially important if you want the Custom Resource that is being managed by this playbook to support [Kubernetes reconciliation](https://developers.redhat.com/articles/2021/06/22/kubernetes-operators-101-part-2-how-operators-work#how_operators_reconcile_kubernetes_cluster_states).

```yaml
- name: Update a Kubernetes CR status
  operator_sdk.util.k8s_status:
    api_version: "{{ k8s_cr_version }}"
    kind: MyKind
    name: "{{ ansible_operator_meta.name }}"
    namespace: "{{ ansible_operator_meta.namespace }}"
    replace_lists: true
    status:
      foo_output_var: something informative
      bar_output_var: true
```

**Note**: The example above contains Jinja variable references (`k8s_cr_version`, `ansible_operator_meta.name`, `ansible_operator_meta.namespace`) that are part of the [provided variables](spec.md#provided-variables) made avaiable to the ansible playbook when being executed as a z/OS Cloud Broker suboperator.

Any data can be added to the CR `status` with the following limitations:
* The `status.conditions` fields are not modified
* The serialized CR content cannot exceed 2MB
* Be cautious about placing sensitive information into the `status` as other users may be able to see this information based on their levels of access control in Kubernetes. Additionally, all updates are logged in Kubernetes audit logs.