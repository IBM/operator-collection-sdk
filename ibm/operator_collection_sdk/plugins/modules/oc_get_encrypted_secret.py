#!/usr/bin/python

# Copyright: (c) 2024, Zarin Ohiba <zarin.ohiba@ibm.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: oc_get_encrypted_secret

short_description: This module creates a get_encrypted_secret

version_added: "1.0.0"

description: This module gets an secret and decrypts it.

options:
    name:
        description: The name of the get_encrypted_secret.
        required: true
        type: str
    namespace:
        description: The endpoint is created in this provided namespace.
        required: true
        type: str
    api_version:
        description: The apiversion.
        required: false
        type: str
        default: v1

# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
# extends_documentation_fragment:
#     - ibm.operator_collection_sdk.my_doc_fragment_name

author:
    - Your Name (@zohiba)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with remote endpointType
  ibm.operator_collection_sdk.oc_get_encrypted_secret:
    name: secret1
    namespace: test-world

# pass in a message and have changed true
- name: Test with local endpointType
  ibm.operator_collection_sdk.oc_get_encrypted_secret:
    name: secret12
    namespace: test-world

# fail the module
- name: Test failure of the module
  ibm.operator_collection_sdk.oc_get_encrypted_secret:
    namespace: test-world

'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
resource:
    description: The resource that was modified.
    type: str
    returned: always

errMsg:
    description: The error message that the test module generates.
    type: str
    returned: always

'''

from ansible.module_utils.basic import AnsibleModule
DEPENDENCY_IMPORT_ERROR = None

try:
    from kubernetes import client, config
    import subprocess
    import yaml
    from ansible_collections.kubernetes.core.plugins.module_utils.k8s.core import AnsibleK8SModule
    from ansible_collections.kubernetes.core.plugins.module_utils.k8s.exceptions import CoreException
except ImportError as e:
    DEPENDENCY_IMPORT_ERROR = f"Failed to import dependency: {e}"


def run_get_encrypted_secret_module():

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        api_version=dict(type='str', default="v1"),
        name=dict(type='str', required=True),
        namespace=dict(type='str', required=True),
    )

    # seed the result dict in the object
    # we primarily care about changed and resource
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        error=False,
    )

    if DEPENDENCY_IMPORT_ERROR is not None:
        module = AnsibleModule(argument_spec=module_args)
        module.fail_json(msg=DEPENDENCY_IMPORT_ERROR)
    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleK8SModule(
        module_class=AnsibleModule,
        argument_spec=module_args,
        supports_check_mode=True,
    )
    try:
        # Load kubeconfig file or in-cluster config
        config.load_kube_config()
        # Create a Kubernetes API client
        core_api = client.CoreV1Api()
        install_zoscb_encrypt_cli = """
            mkdir -vp temp/ &&
            OS=$(uname -s | tr '[:upper:]' '[:lower:]') &&
            ARCH=$(uname -m | sed -E "s/i686|x86_64/amd64/g") &&
            echo $OS &&
            echo $ARCH &&
            oc image extract icr.io/cpopen/ibm-zoscb-encryption-cli:latest --path /bin/${OS}-${ARCH}-zoscb-encrypt:temp/
            """
        result_command = subprocess.run(install_zoscb_encrypt_cli, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        try:
            command = ["zoscb-encrypt get-credential-secret --namespace",
                       module.params["namespace"],
                       "--secret-name",
                       module.params["name"],
                       "&& rm -rf temp"]
            command = (" ").join(command)
            result_command = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
            # print(result_command.stdout)
            result["changed"] = True
            data = yaml.safe_load(result_command.stdout)
            result["ssh_key"] = data["data"]["ssh_key"]
            result["username"] = data["data"]["username"]
        except subprocess.CalledProcessError as e:
            result["error"] = True
            # print("Command '{}' failed with exit code {}".format(e.cmd, e.returncode))
            # print("Output:", e.output)
            module.fail_from_exception(e)

    except CoreException as e:
        result["error"] = True
        module.fail_from_exception(e)
    # # during the execution of the module, if there is an exception or a
    # # conditional state that effectively causes a failure, run
    # # AnsibleModule.fail_json() to pass in the message and the result

    # # in the event of a successful module execution, you will want to
    # # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_get_encrypted_secret_module()


if __name__ == '__main__':
    main()
