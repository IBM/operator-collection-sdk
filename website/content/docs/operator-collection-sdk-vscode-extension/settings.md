---
weight: 2500
title: "Extension Settings"
description: "Configuration settings for the IBM Operator Collection SDK extension for VS Code."
icon: "settings"
date: "2024-02-02T12:34:10-08:00"
lastmod: "2024-02-02T12:34:10-08:00"
draft: true
toc: true
---

## Where to Find the Extension Settings
---
From the "Extensions" tab of your VS Code editor, search for the installed extension and select the associated cog-wheel icon. From there you can navigate to "Extension Settings" page.

![Extension Settings Location](images/vs-code-extension/extension-settings-location.png)

Your settings page should look similar to the following:

![Extension Settings](images/vs-code-extension/extension-settings.png)


## Configuration Options
---

### Ansible® Galaxy
{{< table "table-striped table-hover"  >}}
| Setting Name                    | Default Value              | Description                                                     |
|---------------------------------|----------------------------|-----------------------------------------------------------------|
| **Ansible Galaxy Connectivity** | True                       | Specifies if you have connectivity to Ansible Galaxy.           |
| **Ansible Galaxy Namespace**    | ibm                        | Specifies the Ansible Galaxy namespace to download the OC-SDK.  |
| **Ansible Galaxy URL**          | https://galaxy.ansible.com | Specifies the Ansible Galaxy URL to download the OC-SDK.        |
{{< /table >}}

### Linter
{{< table "table-striped table-hover"  >}}
| Setting Name        | Default Value | Description                                  |
|---------------------|---------------|----------------------------------------------|
| **Linting Enabled** | True          | Specifies whether or not linting is enabled. |
{{< /table >}}