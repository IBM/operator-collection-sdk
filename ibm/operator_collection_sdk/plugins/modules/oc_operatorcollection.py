#!/usr/bin/python

# Copyright: (c) 2024, Zarin Ohiba <zarin.ohiba@ibm.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: oc_operatorcollection

short_description: This module creates a operatorcollection

version_added: "1.0.0"

description: This module creates a operatorcollection.

options:
    state:
        description: >
          Determines if an object should be created, patched, or deleted. When set to C(present), an object will be created,
          if it does not already exist. If set to C(absent), an existing object will be deleted.
          If set to C(present), an existing object will be patched, if its attributes differ from those specified using I(resource_definition) or I(src).
          C(patched) state is an existing resource that has a given patch applied. If the resource doesn't exist, silently skip it (do not raise an error).
        type: str
        required: true
        choices: [ absent, present, patched ]
    name:
        description: The name of the operatorcollection.
        required: true
        type: str
    namespace:
        description: The operatorcollection is created in this provided namespace.
        required: true
        type: str
    api_version:
        description: The apiversion.
        required: false
        type: str
        default: zoscb.ibm.com/v2beta2
    kind:
        description: The kind of resource.
        required: false
        type: str
        default: OperatorCollection
    collectionURLToken:
        description: Provided in certain cases when collection is imported via url.
        required: false
        type: str
    collectionURL:
        description: If provided, it sets url from where to import the collection.
        required: false
        type: str
    collection_src:
        description: If provided, it sets location in local machine from where to upload collection.
        required: false
        type: str
    skipSignatureVerification:
        description: If set to true will verify signature of the collection.
        required: true
        type: bool
    signatureSecret:
        description: Must be provided when we do signature verification.
        required: false
        type: str

# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
# extends_documentation_fragment:
#     - ibm.operator_collection_sdk.my_doc_fragment_name

author:
    - Your Name (@zohiba)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with operatorcollection URL
  ibm.operator_collection_sdk.oc_operatorcollection:
    name: operatorcollection-1
    namespace: test-world
    collectionURL: testurl
    skipSignatureVerification: true
    state: present

# pass in a message and have changed true
- name: Test with signature verification
  ibm.operator_collection_sdk.oc_operatorcollection:
    name: operatorcollection-2
    namespace: test-world
    collectionURL: testurl
    signatureSecret: some-secret
    skipSignatureVerification: false
    state: present

# fail the module
- name: Test failure of the module
  ibm.operator_collection_sdk.oc_operatorcollection:
    name: operatorcollection-3
    namespace: test-world
    state: blah

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
    from jinja2 import Environment, FileSystemLoader
    from ansible_collections.kubernetes.core.plugins.module_utils.k8s.core import AnsibleK8SModule
    from ansible_collections.kubernetes.core.plugins.module_utils.k8s.runner import run_module
    from ansible_collections.kubernetes.core.plugins.module_utils.k8s.exceptions import CoreException
    import subprocess
    import yaml
    from kubernetes import config, client
except ImportError as e:
    DEPENDENCY_IMPORT_ERROR = f"Failed to import dependency: {e}"


def run_operatorcollection_module():

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        kind=dict(type='str', default="OperatorCollection"),
        api_version=dict(type='str', default="zoscb.ibm.com/v2beta2"),
        name=dict(type='str', required=True),
        namespace=dict(type='str', required=True),
        collectionURL=dict(type='str', required=False),
        collectionURLToken=dict(type='str', required=False, no_log=False),
        signatureSecret=dict(type='str', required=False, no_log=False),
        collection_src=dict(type='str', required=False),
        skipSignatureVerification=dict(type="bool", required=True),
        state=dict(type='str', required=True, choices=["absent", "present", "patched"]),
    )

    # make sure host and port is provided when endpointType is set to "remote"
    required_if_args = [
        ["skipSignatureVerification", False, ["signatureSecret"]]
    ]
    mutually_exclusive = [
        ('collection_src', 'collectionURL'),
    ]
    required_one_of = [
        ('collection_src', 'collectionURL'),
    ]

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
        required_if=required_if_args,
        mutually_exclusive=mutually_exclusive,
        required_one_of=required_one_of
    )

    errorMsg = verify_arguments_passed(module)

    if errorMsg is not None:
        result['error'] = True
        module.fail_json(msg=errorMsg, **result)

    if module.params["collection_src"] is not None:

        # extract the operator-config file and copy tar.gz to manager pod
        filename, errorMsg = extract_and_grep(module.params["collection_src"])
        if errorMsg is not None:
            result['error'] = True
            module.fail_json(msg=errorMsg, **result)
        # assign labels
        with open(filename, 'r') as file:
            data = yaml.safe_load(file)
        module.params["labels"] = {"operator-domain": data["domain"],
                                   "operator-name": data["name"], "operator-version": data["version"], "managed-by": "ibm-zos-cloud-broker"}

        manager_pod_err = fetch_manager_pod_name_and_copy_collection_to_manager(module.params["namespace"],
                                                                                module.params["collection_src"], data["name"], data["version"])
        if manager_pod_err is not None:
            result['error'] = True
            module.fail_json(msg=manager_pod_err, **result)
        os.remove(filename)

    environment = Environment(loader=FileSystemLoader("./templates"))
    template = environment.get_template("operatorcollection.yml")
    content = template.render(
        module.params
    )

    module.params["resource_definition"] = content

    try:
        run_module(module)
        result["changed"] = True
    except CoreException as e:
        result["error"] = True
        module.fail_from_exception(e)

    # # during the execution of the module, if there is an exception or a
    # # conditional state that effectively causes a failure, run
    # # AnsibleModule.fail_json() to pass in the message and the result

    # # in the event of a successful module execution, you will want to
    # # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def verify_arguments_passed(module):

    if module.params["collectionURL"] is None and module.params["collection_src"] is None:
        return "Both collectionURL and collection_src can't be None."

    if module.params["collectionURL"] is None and module.params["collection_src"] == "":
        return "collection_src can't be empty string."

    if module.params["collectionURL"] == "" and module.params["collection_src"] is None:
        return "collectionURL can't be empty string."

    if module.params["skipSignatureVerification"] is False and (module.params["signatureSecret"] == "" or module.params["signatureSecret"] is None):
        return "Valid signatureSecret must be entered."

    if module.params["collectionURLToken"] is not None and module.params["collectionURLToken"] == "":
        return "collectionURLToken field can't be empty string. Enter a valid token or remove the field."

    return None


def extract_and_grep(localpath):

    try:
        stdout = subprocess.PIPE
        # Execute 'tar ztf path/name' command
        find_config_file_name = subprocess.Popen(['tar', 'ztf', localpath], stdout=subprocess.PIPE)

        # Execute 'grep "some-value"' command
        match_file = subprocess.Popen(['grep', 'operator-config'], stdin=find_config_file_name.stdout, stdout=subprocess.PIPE)
        # Wait for the 'grep' command to finish
        match_file.wait()
        # Read the output of 'grep' command
        filename = match_file.communicate()[0].decode().strip()
        # Execute 'tar -zxvf path/name filename' command
        process = subprocess.Popen(['tar', '-zxvf', localpath, filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            return filename, None
        return filename, "HII"

    except Exception as e:
        return "", f"Error extracting operator-config yaml: {e}"


def fetch_manager_pod_name_and_copy_collection_to_manager(namespace, localpath, name, version):

    try:
        # Load kubeconfig file or in-cluster config
        config.load_kube_config()
        # Create a Kubernetes API client
        core_api = client.CoreV1Api()
        # Define label selector for the pod
        label_selector = "component=manager"
        # List pods in the specified namespace matching the label selector
        pod_list = core_api.list_namespaced_pod(namespace=namespace, label_selector=label_selector)
        # Get pod name
        pod_name = pod_list.items[0].metadata.name

        remote_dir_path = "/opt/collections/suboperator/" + name + "/" + version
        # mkdir in the pod to store the collection tar file
        mkdir_command = "oc exec -i -n " + namespace + " " + pod_name + " -- mkdir -p " + remote_dir_path
        result = subprocess.run(mkdir_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')

        remote_dir = namespace + "/" + pod_name + ":" + remote_dir_path

        try:
            # Compose the oc cp command to copy the local tar.gz file to the OpenShift pod
            oc_command = "oc cp " + localpath + " " + remote_dir
            result = subprocess.run(oc_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        except subprocess.CalledProcessError as e:
            return f"Error copying tar file to pod: {e}"

        # print(f"Successfully copied {localpath} to {pod_name} at {remote_dir}")
        return None

    except Exception as e:
        return f"Error fetching manager pod info: {e}"
    return None


def main():
    run_operatorcollection_module()


if __name__ == '__main__':
    main()
