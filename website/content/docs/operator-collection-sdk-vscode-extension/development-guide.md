---
weight: 200
title: "Development Guide"
description: ""
icon: "article"
date: "2024-01-15T13:21:07-08:00"
lastmod: "2024-01-15T13:21:07-08:00"
draft: true
toc: true
---

# IBM Operator Collection SDK for VS Code Development Guide

---

## Local debugging
* Press `F5` to open a new window with your extension loaded.
* Run your command from the command palette by pressing (`Ctrl+Shift+P` or `Cmd+Shift+P` on Mac) and typing `Hello World`.
* Set breakpoints in your code inside `src/extension.ts` to debug your extension.
* Find output from your extension in the debug console.

## Making changes
* You can relaunch the extension from the debug toolbar after changing code in `src/extension.ts`.
* You can also reload (`Ctrl+R` or `Cmd+R` on Mac) the VS Code window with your extension to load your changes.

## Explore the API
* You can open the full set of our API when you open the file `node_modules/@types/vscode/index.d.ts`.

## Run tests

### Running tests in terminal
* Run the `oc login` command to log in to an OpenShift cluster, and validate you're in the correct project.
* Run the following command to execute tests.
```
npm run test
```

### Running tests in VS Code
* Open the debug viewlet (`Ctrl+Shift+D` or `Cmd+Shift+D` on Mac) and from the launch configuration dropdown pick `Extension Tests`.
* Press `F5` to run the tests in a new window with your extension loaded.
* See the output of the test result in the debug console.

### Executing Tests using GitHub Workflows
Since the current tests require access to an Openshift cluster, you are required to configure the following variables in your workspace before successfully executing an end to end test of your changes.
* Navigate to `Setting > Secrets and variables > Actions` and click the "New repository secret" button
![GitHub Settings](/images/vs-code-extension/github-settings.png)
* Configure the `OCP_SERVER_URL` secret. This value can be retrieved  and set using the following command:
    ```bash
    oc config view --minify -o jsonpath='{.clusters[*].cluster.server}'
    ```
* Generate a new Service Account token in Openshift and configure the `OCP_TOKEN` secret in GitHub. Follow the steps below to generate a token with the proper access in the cluster
    ```bash
    saName=github
    oc create sa ${saName} -n default
    oc adm policy add-cluster-role-to-user cluster-admin -z ${saName} -n default
    oc sa new-token ${saName} -n default
    ```

## Local builds
* Run the following command to install the `vsce` package globally
    ```
    npm install -g @vscode/vsce
    ```
* Run the following command to build the `.vsix` file
    ```
    npm run build
    ```
* Run the following command to install the extenion to your VS Code editor
    ```
    npm run deploy
    ```