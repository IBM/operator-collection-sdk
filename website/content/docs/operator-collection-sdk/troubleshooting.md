---
weight: 1900
title: "Troubleshooting"
description: "Common errors and known issues."
icon: "troubleshoot"
date: "2024-01-18T16:51:53-08:00"
lastmod: "2024-01-18T16:51:53-08:00"
draft: false
toc: true
---

## Ansible® Python Interpreter
---
When implementing playbooks for your operators and using the `delegate_to` key, you may encounter the following error (or something similar) stating that the path to your python executable is invalid:

```
FAILED! => {
    "changed": false, 
    "module_stderr": "/bin/sh: PATH_TO_PYTHON: No such file or directory\n", 
    "module_stdout": "", 
    "msg": "The module failed to execute correctly, you probably need to set the interpreter...", 
    "rc": 127
}
```

If you are experiencing this issue, supply the `ansible_python_interpreter` variable in the `vars` section of your playbook, or at the task level if necessary:

```yaml
vars:
    ansible_python_interpreter: PATH_TO_PYTHON
```

where `PATH_TO_PYTHON` is the path to your python executable, i.e. `/usr/bin/python3`.


## SSL Certificates
---
If you experience issues with `urlopen error [SSL: CERTIFICATE_VERIFY_FAILED]`, or similar issues, you may need to install and use SSL Certificates before running this extension.

To install SSL Certificates in Python, you can install the [`certifi`](https://pypi.org/project/certifi/) package via `pip`:

```cmd
pip install certifi
```

Alternatively, you can navigate to your python folder and run the `Certificates` command from your terminal:

```cmd
cd <PATH_TO_PYTHON>
./Install\ Certificates.command
```

---

##### Can't find what you're looking for?
[Submit an issue](https://github.com/IBM/operator-collection-sdk/issues)