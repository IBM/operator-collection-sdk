---
weight: 1800
title: "Release Notes"
description: "A record of feature enhancements, bug fixes, and other changes to the IBM Operator Collection SDK."
icon: "notes"
date: "2024-01-15T13:20:41-08:00"
lastmod: "2024-01-15T13:20:41-08:00"
draft: false
toc: true
---

[v1.1.1](https://github.com/IBM/operator-collection-sdk/releases/tag/1.1.1)
---
##### What's Changed
* Disable signature validation when redeploying operator by @freemanlatrell in https://github.com/IBM/operator-collection-sdk/pull/67
* Added support to redeploy operator with new version by @freemanlatrell in https://github.com/IBM/operator-collection-sdk/pull/68
* ansible.utils.unsafe_proxy.AnsibleUnsafeText fix by @freemanlatrell in https://github.com/IBM/operator-collection-sdk/pull/70


**Full Changelog**: https://github.com/IBM/operator-collection-sdk/compare/1.1.0...1.1.1

---

[v1.1.0](https://github.com/IBM/operator-collection-sdk/releases/tag/1.1.0)
---
##### What's Changed
* Offline python package download suing requirements file by @zohiba in https://github.com/IBM/operator-collection-sdk/pull/49
* Moved all python and galaxy requirements file and packages inside collections directory by @zohiba in https://github.com/IBM/operator-collection-sdk/pull/50
* Remove galaxy.yml validation for create_offline_requirements playbook by @freemanlatrell in https://github.com/IBM/operator-collection-sdk/pull/51
* update operatorcollection spec and update python version by @zohiba in https://github.com/IBM/operator-collection-sdk/pull/52
* Added ability to use variables from an ocsdk-extra-vars.yml file by @yemi-kelani in https://github.com/IBM/operator-collection-sdk/pull/56
* Added OC SDK and Ansible VS Code extensions as recommendation in operator collection scaffold by @freemanlatrell in https://github.com/IBM/operator-collection-sdk/pull/57
* Update spec.md by @freemanlatrell in https://github.com/IBM/operator-collection-sdk/pull/58
* Create SubOperatorConfigs using "shared" credential type for local endpoints by @freemanlatrell in https://github.com/IBM/operator-collection-sdk/pull/59
* Remove integer references in spec by @freemanlatrell in https://github.com/IBM/operator-collection-sdk/pull/62
* Added link to video tutorial by @freemanlatrell in https://github.com/IBM/operator-collection-sdk/pull/64

##### New Contributors
* @yemi-kelani made their first contribution in https://github.com/IBM/operator-collection-sdk/pull/56

---

[v1.0.0](https://github.com/IBM/operator-collection-sdk/releases/tag/1.0.0)
---
##### What's Changed
* Fixed OperatorCollection and SubOperatorConfig labels  by @freemanlatrell in https://github.com/IBM/operator-collection-sdk/pull/14
* Racf tutorial updates by @freemanlatrell in https://github.com/IBM/operator-collection-sdk/pull/21
* Passphrase fix by @freemanlatrell in https://github.com/IBM/operator-collection-sdk/pull/32
* remove credentials fix by @freemanlatrell in https://github.com/IBM/operator-collection-sdk/pull/36
* Create playbook for zoscb-encrypt tool by @kberkos-public in https://github.com/IBM/operator-collection-sdk/pull/6
* Add zosendpoint type local or remote by @zohiba in https://github.com/IBM/operator-collection-sdk/pull/39
* Added ability to convert collections for offline support by @freemanlatrell in https://github.com/IBM/operator-collection-sdk/pull/40

##### New Contributors
* @kberkos-public made their first contribution in https://github.com/IBM/operator-collection-sdk/pull/6
* @zohiba made their first contribution in https://github.com/IBM/operator-collection-sdk/pull/39

**Full Changelog**: https://github.com/IBM/operator-collection-sdk/compare/0.2.0...1.0.0

---

[v1.0.0-alpha.1](https://github.com/IBM/operator-collection-sdk/releases/tag/1.0.0-alpha.1)
---
##### What's Changed
* Added authorization to Test workflow by @freemanlatrell in https://github.com/IBM/operator-collection-sdk/pull/16
* Fixed OperatorCollection and SubOperatorConfig labels  by @freemanlatrell in https://github.com/IBM/operator-collection-sdk/pull/14
* Test workflow fix by @freemanlatrell in https://github.com/IBM/operator-collection-sdk/pull/19
* Racf tutorial updates by @freemanlatrell in https://github.com/IBM/operator-collection-sdk/pull/21
* Passphrase fix by @freemanlatrell in https://github.com/IBM/operator-collection-sdk/pull/32


**Full Changelog**: https://github.com/IBM/operator-collection-sdk/compare/0.2.0...1.0.0-alpha.1

---

[v0.2.0](https://github.com/IBM/operator-collection-sdk/releases/tag/0.2.0)
---
##### What's Changed
* Tutorial doc updates by @freemanlatrell in https://github.com/IBM/operator-collection-sdk/pull/1
* Update license IBM copyright statement by @some-ibmer in https://github.com/IBM/operator-collection-sdk/pull/2
* Create CI and Release workflows by @freemanlatrell in https://github.com/IBM/operator-collection-sdk/pull/4

##### New Contributors
* @freemanlatrell made their first contribution in https://github.com/IBM/operator-collection-sdk/pull/1
* @some-ibmer made their first contribution in https://github.com/IBM/operator-collection-sdk/pull/2

**Full Changelog**: https://github.com/IBM/operator-collection-sdk/commits/0.2.0