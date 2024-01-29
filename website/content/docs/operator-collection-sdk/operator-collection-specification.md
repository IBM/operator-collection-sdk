---
weight: 1400
title: "Operator Collection Specification" # <!-- omit from toc -->
description: ""
icon: "list_alt"
date: "2024-01-18T15:16:11-08:00"
lastmod: "2024-01-18T15:16:11-08:00"
draft: true
toc: true
---

<!-- ## Table of Contents
- [Table of Contents](#table-of-contents)
- [Notations \& Terminology](#notations--terminology)
- [OperatorHub Integration](#operatorhub-integration)
- [Operator Resources](#operator-resources)
- [Resource Variables](#resource-variables)
- [Provided Variables](#provided-variables) -->

The `OperatorCollection` specification defines a YAML interface for
standard [Ansible Collections](https://www.ansible.com/blog/getting-started-with-ansible-collections) to be converted
into a [Kubernetes Operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) managing multiple
Kubernetes [Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources).

Ansible collections built conforming to this spec can be directly imported into z/OS Cloud Broker v2.x.

## Notations & Terminology
---
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to
be interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

## OperatorHub Integration
---
{{< table "table-striped table-hover"  >}} <!-- OperatorHub Integration Table Begin -->
The goal of the `OperatorCollection` spec is to easily integrate Ansible-backed automated tasks into OpenShift by
creating new tiles in
the [OpenShift OperatorHub](https://docs.openshift.com/container-platform/4.12/operators/understanding/olm-understanding-operatorhub.html).

These root-level fields defined in the `operator-config` YAML specify the items needed to properly construct the tile
for the Openshift OperatorHub catalog.

| Key            | Required | Type            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|----------------|----------|-----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `domain`       | Required | `string`        | A unique value that will be used to construct the Kubernetes API group for the [`resources`](#operator-resources) defined in this `OperatorCollection`. <br><br>This value MUST conform to the [Kubernetes DNS Subdomain naming](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-subdomain-names) scheme as defined in [RFC 1123](https://datatracker.ietf.org/doc/html/rfc1123).<br><br> This value SHOULD be the same as the `namespace` value specified in an Ansible Collection's `galaxy.yml` file. In scenarios where forks/clones of an official Ansible Collection are desired, the `domain` value MAY be set to another unique, conforming, value.                         |
| `name`         | Required | `string`        | A unique value that will be prepended to the `domain` value to construct a full Kubernetes API Group for the [`resources`](#operator-resources) defined in this `OperatorCollection`. <br><br> This value MUST conform to the [Kubernetes DNS Subdomain naming](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-subdomain-names) scheme as defined in [RFC 1123](https://datatracker.ietf.org/doc/html/rfc1123).<br><br> This value SHOULD be the same as the `name` value specified in an Ansible Collection's `galaxy.yml` file. In scenarios where forks/clones of an official Ansible Collection are desired, the `name` value MAY be set to another unique, conforming, value. |
| `version`      | Required | `semver-string` | A [semantic versioning](https://semver.org/) compliant version number. <br><br> This value SHOULD be the same as the `version` value specified in an Ansible Collection's `galaxy.yml` file.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `displayName`  | Required | `string`        | A short name that will be displayed in OperatorHub for the generated `OperatorCollection` tile.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `description`  | Optional | `string`        | A markdown formatted string that provides information regarding the `OperatorCollection` and it's functionality within the OCP cluster. The markdown content MUST provide a new line after headers (`#`, `##`, etc) for proper compatibility within OCP.                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `resources`    | Required | `array(object)` | A list of Kubernetes resources managed by this `OperatorCollection`. See [Operator Resources](#operator-resources).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `clusterRoles` | Optional | `array(object)` | A list of Kubernetes ClusterRole permission resources managed by this `OperatorCollection`. See [Operator ClusterRoles Permission](#operator-clusterroles-permission)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `roles`        | Optional | `array(object)` | A list of Kubernetes Role permission resources managed by this `OperatorCollection`. See [Operator Roles Permission](#operator-roles-permission)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `icon`         | Optional | `array(object)` | A base64-encoded icon unique to the Operator. See [Icon Object](#icon-object)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
{{< /table >}} <!-- OperatorHub Integration Table End -->


## Icon Object <!-- omit from toc -->
---
{{< table "table-striped table-hover"  >}} <!-- Icon Object Table Begin -->
| Key          | Required | Type     | Description                                |
|--------------|----------|----------|--------------------------------------------|
| `base64data` | Required | `string` | The based64-encoded image string           |
| `mediatype`  | Required | `string` | The media type of the base64-encoded image |
{{< /table >}} <!-- Icon Object Table End -->


## Operator Resources
---
Operator Resources are
the [Custom Resource Definitions](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)
that the `OperatorCollection` will make available within the Kubernetes cluster. An `OperatorCollection` MUST define at
least one resource that will be dynamically created and owned.

The combination of the `version` and `resources.kind` value MUST be unique within the Kubernetes cluster. These values
compose a Kubernetes `Group` `Version`
and `Kind` ([GVK](https://ddymko.medium.com/understanding-kubernetes-gvr-e7fb94093e88)) and therefore MUST be unique.

{{< table "table-striped table-hover"  >}} <!-- Operator Resources Table Begin -->
| Key            | Required | Type            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|----------------|----------|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `kind`         | Required | `string`        | A functional name for the automation that will be managed by this Operator `resource`. This value MUST be Pascal Case (e.g. `SomeMiddleware`).                                                                                                                                                                                                                                                                                                                              |
| `displayName`  | Optional | `string`        | A short name that will be displayed in OperatorHub for the generated `OperatorCollection` tile. <br><br> If a value is not provided, the tile in OCP will use the value given to the `kind`.                                                                                                                                                                                                                                                                                |
| `description`  | Optional | `string`        | A short description of what this `resource` enables or performs.                                                                                                                                                                                                                                                                                                                                                                                                            |
| `playbook`     | Required | `string`        | The path to the Ansible Playbook that will be triggered for managing this `resource`. This path MUST be relative to the root of the Ansible Collection archive. An Ansible Collection with a playbook called `run.yml` in a `playbooks` directory would specify `playbooks/run.yml` for this value. <br><br> The playbook MUST use a `hosts: all` value. When z/OS Cloud Broker executes this playbook, the list of target hosts will be set to the z/OS Endpoint selected. |
| `finalizer`    | Optional | `string`        | An Ansible Playbook MAY be provided that will be triggered when a `resource` is deleted from Kubernetes. This playbook MAY reference the same value specified in `playbook` or provide a secondary playbook to run for deletion actions. <br><br> If a `finalizer` is not provided, Kubernetes will perform clean-up of the references managed within Kubernetes, but resources in z/OS MAY become orphaned.                                                                |
| `vars`         | Optional | `array(object)` | A list of variables that SHOULD be provided during playbook invocation. See [Resource Variables](#resource-variables).                                                                                                                                                                                                                                                                                                                                                      |
| `hideResource` | Optional | `boolean`       | Specifies whether the current resource should be hidden in the OCP "Installed Operators" view.                                                                                                                                                                                                                                                                                                                                                                              |
{{< /table >}} <!-- Operator Resources Table End -->

## Resource Variables
---
Resource variables are input variables that will be provided to the `playbook` defined in a given `resource`. The
variables specified here SHALL override any other variable defaults set within the Ansible Collection that adhere to
Ansible's [variable precedence](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#ansible-variable-precedence)
specification. Any variable defined in the `vars` array SHALL be passed to the playbook at the level of "extra vars" as
described
in [variable precedence](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#ansible-variable-precedence).

Ansible Collections MAY provide default variables throughout their collection, but SHOULD only declare the variables
that MAY be overridden at playbook execution in this `vars` array. In other words, an Ansible variable MAY be declared
in an playbook or role, but not set in `vars` if there is no need for user input during execution from OCP.


{{< table "table-striped table-hover"  >}} <!-- Resource Variables Table Begin -->
| Key               | Required | Type            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|-------------------|----------|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `name`            | Required | `string`        | The variable name that SHALL be provided to the defined `playbook` as an "extra vars" (`-e`) input parameter during execution. The provided value MUST conform to an existing variable referenced in the `playbook` or underlying Ansible role.                                                                                                                                                                                                                                                                                                                             |
| `displayName`     | Required | `string`        | A short label that SHALL be visible in the OCP Kubernete's Custom Resource creation UIs.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `type`            | Required | `string`        | The variable type as is needed to be passed down to the Ansible `playbook`. Valid values for this include `string`, `number`, `boolean`, `password`, `object`. <br><br> The `password` type will generate a dropdown list of the `Secrets` in the current namespace. This variable should be a reference to the `Secret` name selected by the user, in which the playbook/role should retrieve this `Secret` to read the private data. <br><br> Enums (or "dropdowns") are also supported by setting `type: string` and providing an additional `options` field. |
| `options`         | Optional | `[]string`      | A list of valid `strings` to specify the available options for an enum ("dropdown") `type`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `required`        | Optional | `boolean`       | Set this field to `true` if this variable MUST be input by the user before resource creation is allowed.                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `default`         | Optional | `string`        | A default value that should be set in the OCP UIs for this variable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `description`     | Optional | `string`        | A short description that SHALL be visible in the OCP Kubernetes Custom Resource creation UIs under the provided `displayName`. This value MUST provide any relevant information for users to understand the purpose for the provided `var`.                                                                                                                                                                                                                                                                                                                                 |
| `kindReference`   | Optional | `string`        | Specify this field if the `playbook` requires information from other Kubernetes resources managed by the z/OS Cloud Broker. <br><br> This will enable a dynamically populated dropdown in the OCP UIs containing all previously created instances of the specified `kind`. Use this for running actions against previously created instances. <br><br>                                                                                                                                                                                                                      |
| `objectVariables` | Optional | `array(object)` | A list of variables that SHOULD be provided in the object. See [Object Variables](#object-variables). <br><br> This value is required when the `type` is set to `object`                                                                                                                                                                                                                                                                                                                                                                                                |
| `array`           | Optional | `boolean`       | Set this field to `true` if the variable should be stored as an array.  <br><br> Arrays are only supported for the `string`, `number`, and `object` variable types                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
{{< /table >}} <!-- Resource Variables Table End -->

## Object Variables
---
Object variables are a specialized form of resource variables. They are used when a variable needs to hold a complex or
structured value, and these object
variables are intended to be nested within the parent resource variables. Unlike parent resource variables, object
variables do not support object and array types definition from the parent resource variable.


{{< table "table-striped table-hover"  >}} <!-- Object Variables Table Begin -->
| Key               | Required | Type            | Description                                                                                                                                                                                                                                                                                                                                             |
|-------------------|----------|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `name`            | Required | `string`        | The variable name that SHALL be provided to the defined `playbook` as an "extra vars" (`-e`) input parameter during execution. The provided value MUST conform to an existing variable referenced in the `playbook` or underlying Ansible role.                                                                                                         | 
| `displayName`     | Required | `string`        | A short label that SHALL be visible in the OCP Kubernetes Custom Resource creation UIs.                                                                                                                                                                                                                                                                 |
| `type`            | Required | `string`        | The variable type as is needed to be passed down to the Ansible `playbook`. Valid values for this include `string`, `number`, `boolean`, `password`. <br><br> Enums (or "dropdowns") are also supported by setting `type: string` and providing an additional `options` field.                                                               |
| `options`         | Optional | `[]string`      | A list of valid `strings` to specify the available options for an enum ("dropdown") `type`.                                                                                                                                                                                                                                                             |
| `required`        | Optional | `boolean`       | Set this field to `true` if this variable MUST be input by the user before resource creation is allowed.                                                                                                                                                                                                                                                | 
| `default`         | Optional | `string`        | A default value that should be set in the OCP UIs for this variable.                                                                                                                                                                                                                                                                                    |
| `description`     | Optional | `string`        | A short description that SHALL be visible in the OCP Kubernetes Custom Resource creation UIs under the provided `displayName`. This value MUST provide any relevant information for users to understand the purpose for the provided `var`.                                                                                                             | 
| `kindReference`   | Optional | `string`        | Specify this field if the `playbook` requires information from other Kubernetes resources  managed by the z/OS Cloud Broker. <br><br> This will enable a dynamically populated dropdown in the OCP UIs containing all previously created instances of the specified `kind`. Use this for running actions against previously created instances. <br><br> |
{{< /table >}} <!-- Object Variables Table End -->

## Provided Variables
---
The Ansible Playbooks available within collections MAY be executed in multiple runtime environments. For example,
locally on a workstation during development, or via a Kubernetes Operator for larger self-service consumption. In these
scenarios, there MAY be tasks that require different logical paths through the Ansible Playbook in a local environment
that MAY NOT be necessary in a Kubernetes environment.

For this reason the Operator created for each `resource` will also provide the following variables that may be used
within an Ansible Playbook's conditions (`when`) to progress through different logical paths.

{{< table "table-striped table-hover"  >}} <!-- Provided Variables Table Begin -->
| Key                               | Value                       | Description                                                                                                                                                                                                    |
|-----------------------------------|-----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `k8s_managed`                     | `true`                      | A Boolean variable indicating that the Ansible Playbook is being managed (and run) from a Kubernetes environment.                                                                                              |
| `k8s_cr_event`                    | `create` or `delete`        | When a Custom resource is created via Kubernetes, the `create` value will be provided. When a Custom Resource is deleted via Kubernetes, the `delete` value will be provided.                                  |
| `k8s_cr_group`                    | `suboperator.zoscb.ibm.com` | A reference to the Kubernetes API Group. Useful for `k8s_status` or `k8s_info` module calls.                                                                                                                   |
| `k8s_cr_version`                  | `{{ version }}`             | A reference to the value specified in the root-level `version` field. Useful for `k8s_status` or `k8s_info` module calls.                                                                                      |
| `k8s_cr_kind`                     | `{{ resource.kind }}`       | A reference to the `kind` value provided for a resource. Useful for `k8s_status` or `k8s_info` module calls.                                                                                                   |
| `ansible_operator_meta.namespace` | `{{ namespace }}`           | A built-in reference supplied by the Operator-SDK for retrieving the Kubernetes namespace that the Custom Resource (and playbook) are being executed from. Useful for `k8s_status` or `k8s_info` module calls. |
| `ansible_operator_meta.name`      | `{{ CR name }}`             | A built-in reference supplied by the Operator-SDK for retrieving the Kubernetes Custom Resource name that triggered the playbook execution. Useful for `k8s_status` or `k8s_info` module calls.                |
{{< /table >}} <!-- Provided Variables Table End -->

## Operator ClusterRoles Permission
---
Operator ClusterRoles Permission defines cluster-wide Operator permissions that the `OperatorCollection` will make
available within the Kubernetes cluster. An `OperatorCollection` can optionally create clusterrole permissions.
The following field can be used to create cluster scoped permission.

{{< table "table-striped table-hover"  >}} <!-- Operator ClusterRoles Permission Table Begin -->
| Key     | Required | Type            | Description                                                                                                                                                         |
|---------|----------|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `rules` | Optional | `array(object)` | A list of cluster-scoped policy rules for the operator. See Rules example [here](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#clusterrole-example) |
{{< /table  >}} <!-- Operator ClusterRoles Permission Table End -->

## Operator Roles Permission
---
Operator Roles Permission defines Operator roles permissions within a namespace that the `OperatorCollection` will make
available within the Kubernetes cluster. An `OperatorCollection` can optionally create these namespace permissions using
Roles field.
The following field can be used to create namespace scoped permission.

{{< table "table-striped table-hover"  >}} <!-- Operator Roles Permission Table Begin -->
| Key     | Required | Type            | Description                                                                                                                                                    |
|---------|----------|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `rules` | Optional | `array(object)` | A list of namespace-scoped policy rules for the operator. See Rules example [here](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#role-example) |
{{< /table >}} <!-- Operator Roles Permission Table Begin -->