---
weight: 300
title: "Troubleshooting"
description: ""
icon: "troubleshoot"
date: "2024-01-19T16:15:21-08:00"
lastmod: "2024-01-19T16:15:21-08:00"
draft: false
toc: true
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