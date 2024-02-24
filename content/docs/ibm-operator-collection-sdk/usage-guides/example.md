---
weight: 1320
title: "Example"
description: "An example definition for an Operator Config yaml file. "
icon: "category"
date: "2024-01-18T16:50:21-08:00"
lastmod: "2024-01-18T16:50:21-08:00"
draft: false
toc: true
---

The example below shows a minimal configuration needed to be provided in an `operator-config.yml` file in order for dynamic generation of Kubernetes Operators. 

This example will create a `RACF` operator which extends the Kubernetes API with a new Custom Resource Definition (CRD) called `ZosUserId`. The CRD will be an additional tile in the OCP Developer Catalog and showcases the [lifecycle stages](/docs/ibm-operator-collection-sdk/operator-collection-specification/) supported by z/OS Cloud Broker.

```yaml
domain: zosutils
name: racf
version: 0.0.2
displayName: RACF Operator
description: >-
  # z/OS RACF Operator
  
  This operator allows users to create and delete user IDs on z/OS.
resources:
  - kind: ZosUserId
    displayName: z/OS User Id
    description: A User ID managed by the RACF security facility on z/OS.
    playbook: playbooks/add-user.yml
    finalizer: playbooks/remove-user.yml
    vars:
      - name: name
        displayName: Real Name
        description: Specifies the user name to be associated with the new user ID.
        type: string
      - name: userid
        displayName: User ID
        description: Specifies the user to be defined to RACF.
        type: string
      - name: email_to
        displayName: Email
        description: Email address to send the new user credentials
        type: string
icon:
  - base64data: >-
      PHN2ZyBpZD0iaWNvbiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB2aWV3Qm94PSIwIDAgMzIgMzIiPjxkZWZzPjxzdHlsZT4uY2xzLTF7ZmlsbDpub25lO308L3N0eWxlPjwvZGVmcz48dGl0bGU+dXNlcjwvdGl0bGU+PHBhdGggZD0iTTE2LDRhNSw1LDAsMSwxLTUsNSw1LDUsMCwwLDEsNS01bTAtMmE3LDcsMCwxLDAsNyw3QTcsNywwLDAsMCwxNiwyWiIvPjxwYXRoIGQ9Ik0yNiwzMEgyNFYyNWE1LDUsMCwwLDAtNS01SDEzYTUsNSwwLDAsMC01LDV2NUg2VjI1YTcsNywwLDAsMSw3LTdoNmE3LDcsMCwwLDEsNyw3WiIvPjxyZWN0IGlkPSJfVHJhbnNwYXJlbnRfUmVjdGFuZ2xlXyIgZGF0YS1uYW1lPSImbHQ7VHJhbnNwYXJlbnQgUmVjdGFuZ2xlJmd0OyIgY2xhc3M9ImNscy0xIiB3aWR0aD0iMzIiIGhlaWdodD0iMzIiLz48L3N2Zz4=
    mediatype: image/svg+xml
```

![RACF Operator](images/racf-operator.png)

## Details
The [root-level fields](/docs/ibm-operator-collection-sdk/operator-collection-specification/#operatorhub-integration) (`domain`, `name`, etc) provide the interfaces for how the Operator tile is displayed in the OCP OperatorHub and Installed Operators UIs.

The [`resources`](/docs/ibm-operator-collection-sdk/operator-collection-specification/#operator-resources) array provides the interface for the Kubernetes Custom Resource Definitions (CRDs) and Custom Controllers. The generated CRD will also have an auto-generated OCP UI for users to create "instances" of these CRDs, also called Custom Resources (CR).

- For every new Kubernetes Custom Resource (`kind`) you want to be controlled by a `playbook`, add a new object to the `resources` array
- Specify the `playbook` that will be called when someone creates an instance of the `kind`
- Specify the `finalizer` (playbook) that will be called when someone deletes an instance of the `kind` (this can be the same playbook, see [provided variables](/docs/ibm-operator-collection-sdk/operator-collection-specification/#provided-variables))
- Provide a list of [`vars`](/docs/ibm-operator-collection-sdk/operator-collection-specification/#resource-variables) that may optionally be provided when a user attempts to create an instance of the `kind` via the OCP UI