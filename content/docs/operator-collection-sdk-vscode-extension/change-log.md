---
weight: 500
title: "Change Log"
description: "A record of feature enhancements, bug fixes, and other changes to the IBM Operator Collection SDK for VS Code extension."
icon: "change_history"
date: "2024-01-23T14:52:14-08:00"
lastmod: "2024-01-23T14:52:14-08:00"
draft: false
toc: true
---

### v1.1.0
- Prevent error messages and response delays when connectivity to OpenShift and Ansible Galaxy connectivity is disrupted
- Added documentation note about lack of Windows OS support.
- Added ability to copy error message from toast notification
- Restrict redeploy collection command when signature validation is required
- Added support for scaffolding files, an operator-sdk submenu, and quick-fix actions for the linter.
- Local ZosEndpoint fixes
- Added '-' and '_' as valid characters in sha256 token regex.
- Added support for operator collection workspace initialization

### v1.0.1
- Bypass 401 failures when extension activates but user isn't logged into OpenShift

### v1.0.0
- Updated linter json schema with latest spec changes
- Open link failure message change
- Fixed namespace failures during OCP logout
- Restrict viewing resources while operations are pending

### v0.4.0

- Display z/OS Cloud Broker install status in About view
- Fixed Critical Vulnerability CVSS Score 9.8: tough-cookie-2.5.0.tgz
- Added ability to refresh pod logs
- New icons
- Refresh context if user is logged out during command execution
- Changed login command to request a single input and validate with regex
- Fixed create operator command stacking
- Relocate verbose log download button to custom resource item
- Added fix to prevent failures when custom resource is created but Ansible Runner tasks have yet to be executed
- Add dependency on `iliazeus.vscode-ansi` extension to add styling to Ansible logs
- Update context when current OpenShift project is invalid

### v0.3.0

- Display logs as virtual documents
- Display Custom Resource yaml files as virtual documents in editor
- Added operator-config yaml schema linter
- Refresh OpenShift Cluster Info when updated outside of editor
- Detect if local collection sdk is outdated
- Added validation check to cluster commands
- Adding prettier and slint in pre-commit hook
- Bug [#25](https://github.com/IBM/operator-collection-sdk-vscode-extension/issues/25) fix
- Bug fix [#37](https://github.com/IBM/operator-collection-sdk-vscode-extension/issues/37)\
- Linter enhancements
- Added single clicks to Help and Openshift Panels. Functions as expected. Enhancements [#55](https://github.com/IBM/operator-collection-sdk-vscode-extension/issues/5) and [#13](https://github.com/IBM/operator-collection-sdk-vscode-extension/issues/13)
- Prohibit project update during certain operations, bug fix [#43](https://github.com/IBM/operator-collection-sdk-vscode-extension/issues/43)
- Added logout button for enhancement [#14](https://github.com/IBM/operator-collection-sdk-vscode-extension/issues/14)
- Enhanced Linter name matching fix
- fixed some minor issues with logout function
- Added extension Galaxy and Linter settings
- Added picture to `readme.md` showing where to find access token from OpenShift homepage
- Added support for latest Ansible Galaxy APIs
- Prohibit operation overlapping
- Ocsdk version - incorporating About view
- Addded install dependency step for OcSDK
- Prompt user to login when OCP token expires

### v0.2.0

- Removed additional prompt asking if user would like to use extra vars file
- Prompt for SSH Key passphrase when using extra vars file
- Fix to detect extra vars file in specific Operator Collection, when multiple Operator Collections are listed in the workspace
- Fixed undefined error messages

### v0.1.0

- Initial prototype