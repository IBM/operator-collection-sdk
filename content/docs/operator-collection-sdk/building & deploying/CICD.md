---
weight: 1420
title: "CI/CD"
description: "Enable Continuous Integration and Continuous Delivery for your Operator Collections."
icon: "valve"
date: "2024-02-09T16:04:34-08:00"
lastmod: "2024-02-09T16:04:34-08:00"
draft: false
toc: true
---

## Using GitHub Workflow Actions for Deployment
---

You can use GitHub Workflows to automate the Operator Collection signing process. Workflow files are written in YAML and should be placed in the `.github/workflows` directory of your repository. 

1. Create a local git repository at the root of your Operator Collection workspace, if you haven't already.

2. Create a file called `release.yml` inside your `.github/workflows` directory. If the directory does not exist, create it.

3. Copy the following YAML code into your `.github/workflows/release.yml` file then push your committed changes to GitHub. Its function is to build, sign, and upload your Operator Collection signature files at release.

    ```YAML
    name: Release

    on:
      push: # this workflow is triggered when tags are pushed to GitHub
        tags:
          - "**"

    permissions:
      contents: write

    jobs:
      release:
        name: Release
        runs-on: ubuntu-latest

        steps:
          - name: Determine tag
            run: "echo \"RELEASE_TAG=${GITHUB_REF#refs/tags/}\" >> $GITHUB_ENV"

          - name: Create release
            uses: actions/github-script@v7
            with:
              github-token: "${{ secrets.GITHUB_TOKEN }}"
              script: |
                try {
                  const response = await github.rest.repos.createRelease({
                    draft: false,
                    generate_release_notes: true,
                    name: process.env.RELEASE_TAG,
                    owner: context.repo.owner,
                    prerelease: false,
                    repo: context.repo.repo,
                    tag_name: process.env.RELEASE_TAG,
                  });
                  core.exportVariable('RELEASE_ID', response.data.id);
                  core.exportVariable('RELEASE_UPLOAD_URL', response.data.upload_url);
                } catch (error) {
                  core.setFailed(error.message);
                }

      publish:
        name: Publish
        needs: release
        runs-on: ubuntu-latest
        environment: release

        env:
          FULL_COLLECTION_PATH: "${GITHUB_WORKSPACE}/${{ vars.COLLECTION_PATH }}"

        steps:
          - name: Determine tag
            run: "echo \"RELEASE_TAG=${GITHUB_REF#refs/tags/}\" >> $GITHUB_ENV"

          - name: Check-out repository
            uses: actions/checkout@v4
            with:
              fetch-depth: 0
              ref: ${{ env.RELEASE_TAG }}

          # install, remove, and modify dependencies as needed

          - name: Install Ansible
            run: pip install ansible==8.0.0

          - name: Install Operator Collection SDK
            run: ansible-galaxy collection install git+https://github.com/IBM/operator-collection-sdk.git#ibm/operator_collection_sdk -f

          - name: Create local/builds folder it it doesn't exist...
            run: mkdir -p "${{ env.FULL_COLLECTION_PATH }}/local/builds"

          - name: Build Collection
            run: |
              ansible-galaxy collection build ${{ env.FULL_COLLECTION_PATH }} -f --output-path ${{ env.FULL_COLLECTION_PATH }}/local/builds
              echo "COLLECTION_BUILD=$(ls ${{ env.FULL_COLLECTION_PATH }}/local/builds)" >> $GITHUB_ENV
              echo "COLLECTION_BUILD_LOCATION=${{ env.FULL_COLLECTION_PATH }}/local/builds/$(ls ${{ env.FULL_COLLECTION_PATH }}/local/builds)" >> $GITHUB_ENV

          - name: Sign Collection
            run: |
              openssl genrsa -out privatekey.pem 2048
              openssl rsa -in privatekey.pem -out ${{ vars.COLLECTION_NAME }}.pub -outform PEM -pubout
              openssl dgst -sha256 -sign privatekey.pem -out ${{ vars.COLLECTION_NAME }}-${RELEASE}.sig ${COLLECTION_BUILD_LOCATION}
              openssl dgst -sha256 -verify ${{ vars.COLLECTION_NAME }}.pub -signature ${{ vars.COLLECTION_NAME }}-${RELEASE}.sig ${COLLECTION_BUILD_LOCATION}
              echo "PUBLIC_KEY=$(readlink -f ${{ vars.COLLECTION_NAME }}.pub)" >> $GITHUB_ENV
              echo "SIGNATURE=$(readlink -f ${{ vars.COLLECTION_NAME }}-${RELEASE}.sig)" >> $GITHUB_ENV
            env:
              RELEASE:  ${{ env.RELEASE_TAG }}

          - name: Upload Collection and Signature Files to GitHub
            run: |
              gh release upload ${RELEASE_TAG} ${COLLECTION_BUILD_LOCATION}
              gh release upload ${RELEASE_TAG} ${PUBLIC_KEY}
              gh release upload ${RELEASE_TAG} ${SIGNATURE}
            env:
              GITHUB_TOKEN: ${{ github.TOKEN }}

          - name: Build Offline Collection
            run: |
              rm -rf ${{ env.FULL_COLLECTION_PATH }}/local/
              cd ${{ env.FULL_COLLECTION_PATH }}
              ansible-playbook ibm.operator_collection_sdk.create_offline_requirements
              ansible-galaxy collection build ${{ env.FULL_COLLECTION_PATH }} -f --output-path ${{ env.FULL_COLLECTION_PATH }}/local/builds
              COLLECTION_BUILD=$(ls ${{ env.FULL_COLLECTION_PATH }}/local/builds)
              mv ${{ env.FULL_COLLECTION_PATH }}/local/builds/${COLLECTION_BUILD} ${{ env.FULL_COLLECTION_PATH }}/local/builds/${{ vars.COLLECTION_NAME }}-offline-${RELEASE}.tar.gz
              echo "COLLECTION_BUILD_OFFLINE_LOCATION=${{ env.FULL_COLLECTION_PATH }}/local/builds/$(ls ${{ env.FULL_COLLECTION_PATH }}/local/builds)" >> $GITHUB_ENV
            env:
              RELEASE:  ${{ env.RELEASE_TAG }}

          - name: Sign Offline Collection
            run: |
              openssl genrsa -out privatekey-offline.pem 2048
              openssl rsa -in privatekey-offline.pem -out ${{ vars.COLLECTION_NAME }}-offline.pub -outform PEM -pubout
              openssl dgst -sha256 -sign privatekey-offline.pem -out ${{ vars.COLLECTION_NAME }}-${RELEASE}-offline.sig ${COLLECTION_BUILD_OFFLINE_LOCATION}
              openssl dgst -sha256 -verify ${{ vars.COLLECTION_NAME }}-offline.pub -signature ${{ vars.COLLECTION_NAME }}-${RELEASE}-offline.sig ${COLLECTION_BUILD_OFFLINE_LOCATION}
              echo "PUBLIC_KEY_OFFLINE=$(readlink -f ${{ vars.COLLECTION_NAME }}-offline.pub)" >> $GITHUB_ENV
              echo "SIGNATURE_OFFLINE=$(readlink -f ${{ vars.COLLECTION_NAME }}-${RELEASE}-offline.sig)" >> $GITHUB_ENV
            env:
              RELEASE:  ${{ env.RELEASE_TAG }}

          - name: Upload Offline Collection and Signature Files to GitHub
            run: |
              gh release upload ${RELEASE_TAG} ${COLLECTION_BUILD_OFFLINE_LOCATION}
              gh release upload ${RELEASE_TAG} ${PUBLIC_KEY_OFFLINE}
              gh release upload ${RELEASE_TAG} ${SIGNATURE_OFFLINE}
            env:
              GITHUB_TOKEN: ${{ github.TOKEN }}

          - name: Publish Collection to Ansible Galaxy
            run: ansible-galaxy collection publish -vvvv --api-key ${GALAXY_API_KEY} ${COLLECTION_BUILD_LOCATION}
            env:
              GALAXY_API_KEY: ${{ secrets.GALAXY_API_KEY }}
    ```

4. In order for this workflow to work properly, you'll need to add a couple environment secrets and variables to GitHub:
    * Start by navigating to **Settings > Environments** in your Operator Collection's GitHub repository and creating a **New environment** named `release`.
    
        **Note:** The environment name can be modified. Just be sure to match whatever is written in the `environment` field of the `publish` job with the name you've created.

        ![Release - New Environment](/images/operator-collection-sdk/release-new-environment.png)

    * In your newly created environment, **add the following environment secrets and variables** for use in your release workflow. For details on how to add environment secrets and variables, consult GitHub's [documentation](https://docs.github.com/en/actions/learn-github-actions/variables#defining-configuration-variables-for-multiple-workflows).

        {{< table "table-striped table-hover"  >}}
|    Variable       |                                     description                                          |
|-------------------|------------------------------------------------------------------------------------------|
| `COLLECTION_PATH` | (Enviornment Variable) The path from repository root to the folder that holds both your `galaxy` and `operator-config` files, i.e. "ibm/operator-collection-sdk". |
| `COLLECTION_NAME` | (Enviornment Variable) The name of your Operator Collection. One term where words are demarcated with hyphens or underscore, i.e. "file-manager". |
| `GALAXY_API_KEY`  | (Secret) Your Ansible Galaxy API access token. Remove this secret and the [publishing](/docs/operator-collection-sdk/building-deploying/cicd/#publishing-to-ansible-galaxy) step if you would not like to upload your signed collections to Ansible Galaxy.|
        {{< /table >}}

        ![Release Variables](/images/operator-collection-sdk/release-variables.png)

        **Note:** Secrets and variables prefixed with `GITHUB_` such as `GITHUB_TOKEN` and `GITHUB_WORKSPACE` will be [created automatically](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#about-the-github_token-secret) for each workflow job, no further action is needed.

5. Trigger the workflow. Because we configured this work flow to run when tags are pushed to GitHub, we need only create and push a tag, to test our changes:

    ```bash
    git tag <tag>
    git push origin <tag>
    ```

    where `<tag>` adheres to the [semantic versioning format](https://semver.org/), i.e. `1.0.0`.


### Offline Collections

The workflow YAML block posted above includes steps to build, sign/verify, and upload offline versions of your collections to GitHub. These steps have the following names:
```YAML
- name: Build Offline Collection
    ...

- name: Sign Offline Collection
    ...

- name: Upload Offline Collection and Signature Files to GitHub
    ...
```

### Publishing to Ansible Galaxy

To automate the process of publishing a collection to Ansible® Galaxy, the `release.yml` workflow file includes the following step in under **jobs > publish > steps**. This step requires that you add the `GALAXY_API_KEY` to your enviornment secrets in GitHub as shown above.

```YAML
- name: Publish Collection to Ansible Galaxy
    run: ansible-galaxy collection publish -vvvv --api-key ${GALAXY_API_KEY} ${COLLECTION_BUILD_LOCATION}
    env:
      GALAXY_API_KEY: ${{ secrets.GALAXY_API_KEY }}
```

