---
weight: 1410
title: "Collection Verification"
description: "How to sign and verify your Operator Collections."
icon: "fingerprint"
date: "2024-02-08T14:31:16-08:00"
lastmod: "2024-02-08T14:31:16-08:00"
draft: false
toc: true
---

## Manual Signature Creation & Verification
---

You can use pair of public and private (asymmetric) keys to sign and verify your Operator Collections. Remember to replace `<filename>` and `<key_pair_name>` with the appropriate terms in the following commands.

1. Generate a signing key-pair:
    ```bash
        openssl genrsa -out <key_pair_name>.key 4096
        openssl rsa -in <key_pair_name>.key -out <key_pair_name>.pub -outform PEM -pubout
    ```

    The previous commands produce a private key, `<key_pair_name>.key`, which is then used to create a public key `<key_pair_name>.pub`. Note their extensions. The private key, ending in `.key` is used to sign the Operator Collection tarball and should remain private at all times. The public key, ending in `.pub` will be used to verify the Operator Collection.

2. To sign an existing tarball:
    ```bash
    openssl dgst -sha256 -sign <key_pair_name> -out <filename>.sig <filename>.tar.gz
    ```

3. To verify:
    ```bash
    openssl dgst -sha256 -verify <key_pair_name>.pub -signature <filename>.sig <filename>.tar.gz
    ```

You can use this process to sign any file, just replace the `<filename>.tar.gz` in the commands above.
These signatures should work with both the manual and galaxy import paths.

## Automate using GitHub Workflow Actions
---

Alternatively, you can easily automate the process of building, signing, and deploying you Operator Collections with GitHub Workflow Actions. Follow the [CI/CD tutorial](/docs/operator-collection-sdk/building-deploying/cicd/#using-github-workflow-actions) to get started.