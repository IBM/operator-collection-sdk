---
weight: 3100
title: "Integrated Operator Collection Linter"
description: "The IBM Operator Collection SDK for VS Code integrated Operator Collection Linter"
icon: "quick_reference_all"
date: "2024-01-15T13:24:15-08:00"
lastmod: "2024-01-15T13:24:15-08:00"
draft: false
toc: true
---

## Linter Configuration
---
The IBM Operator Collection SDK extension for VS Code has a built-in linter meant to validate your `operator-config` yaml file. 


The linter can be configured with a yaml file called **`.oc-lint`**, which should be placed in the same directory as your `operator-config` file. It contains the following format:

```yaml
---
# .oc-lint

# List of files for the linter to ignore.
exclude_paths:
    - '**'

# Use all the default linter rules
use_default_rules: true

# List of rules to skip linting.
skip_list:
    - match-domain

# List of additional rules to enable.
enable_list:
    - hosts-all
```

Where:
- `exlude_paths` defines a glob pattern to ignore when matching against the files the linter will process.
- `use_default_rules` Enables all the linting rules to be applied.
- `skip_list` Lists all the rules you want disabled.
- `enable_list` Lists all the rules you want to explicitly enable.

You can ignore or enable rules, and ignore files from linting. 


## Linter Rules
---
You can customize the linter rules and files to suit your needs. By default, the following rules are applied:

{{< table "table-striped table-hover"  >}}
|        Rule            |                Description              |
|------------------------|-----------------------------------------|
|**`missing-galaxy`**    |Missing `galaxy.yaml` file errors.       |
|**`match-domain`**      |`galaxy.yml` file `domain` mismatch      |
|**`match-name`**        |`galaxy.yml` file `name` mismatch        |
|**`match-version`**     |`galaxy.yml` file `version` mismatch     |
|**`ansible-config`**    |Build includes `ansible.cfg` error       |
|**`playbook-path`**     |Playbook relative path validation error  |
|**`hosts-all`**         |Playbook hosts validation                |
|**`missing-playbook`**  |Validate Playbook existence              |
|**`finalizer-path`**    |Finalizer relative path validation error |
|**`missing-finalizer`** |Validate Finalizer existence             |
{{< /table >}}


## Quick Fix Options
---
The built-in linter will attempt to remedy playbooks specified in the `operator-config` yaml file with playbooks that it finds in the collection workspace. When errors are found, for instance in the case that the specifed playbook cannot be located, the linter may provide options to quickly resolve them:

![Linter Quick Fix Options](/images/vs-code-extension/linter-quick-fix-options.png) 