---
weight: 1240
title: "Collection Verification"
description: "How to sign and verify your collections."
icon: "fingerprint"
date: "2024-02-08T14:31:16-08:00"
lastmod: "2024-02-08T14:31:16-08:00"
draft: true
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

## Using Github Workflow Actions
---

Optionally, you can use Github Workflows to automate the Operator Collection signing process. Workflow files are written in yaml and should be placed in the `.github/workflows` directory of your repository. 

Below is an example of a Github Workflow yaml file that builds and signs a collection at release. Steps can be added as needed to upload and distrubte the Operator Collection as well.

```yaml
name: Release

on:
  push:
    tags:
      - "**"

permissions:
  contents: write

jobs:
    # necessary jobs...

publish:
    name: Publish
    needs: release
    runs-on: ubuntu-latest

    steps:

        # additional steps...

        - name: Build Collection
            run: |
            ansible-galaxy collection build ${GITHUB_WORKSPACE}/freemanlatrell/file_manager -f --output-path ${GITHUB_WORKSPACE}/freemanlatrell/file_manager/local/builds
            echo "COLLECTION_BUILD=$(ls ${GITHUB_WORKSPACE}/freemanlatrell/file_manager/local/builds)" >> $GITHUB_ENV
            echo "COLLECTION_BUILD_LOCATION=${GITHUB_WORKSPACE}/freemanlatrell/file_manager/local/builds/$(ls ${GITHUB_WORKSPACE}/freemanlatrell/file_manager/local/builds)" >> $GITHUB_ENV

        - name: Sign Collection
            run: |
            openssl genrsa -out privatekey.pem 2048
            openssl rsa -in privatekey.pem -out file-manager.pub -outform PEM -pubout
            openssl dgst -sha256 -sign privatekey.pem -out file-manager-${RELEASE}.sig ${COLLECTION_BUILD_LOCATION}
            openssl dgst -sha256 -verify file-manager.pub -signature file-manager-${RELEASE}.sig ${COLLECTION_BUILD_LOCATION}
            echo "PUBLIC_KEY=$(readlink -f file-manager.pub)" >> $GITHUB_ENV
            echo "SIGNATURE=$(readlink -f file-manager-${RELEASE}.sig)" >> $GITHUB_ENV
            env:
            RELEASE:  ${{ env.RELEASE_TAG }}
        
        # additional steps...
```