#!/usr/bin/python

# Copyright: (c) 2024, Zarin Ohiba <zarin.ohiba@ibm.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: oc_suboperatorconfig

short_description: This module creates a suboperatorconfig

version_added: "1.0.0"

description: This module creates a suboperatorconfig.

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
        description: The name of the zosendpoint.
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
        default: zoscb.ibm.com/v2beta2
    kind:
        description: The kind of resource.
        required: false
        type: str
        default: SubOperatorConfig
    credentialType:
        description: Sets credential type to shared or personal.
        required: true
        type: str
        choices: [ personal, shared ]
    collection_name:
        description: Sets location of the collection source.
        required: true
        type: str
    endpointMapping:
        description: Sets location of the collection source.
        required: true
        type: list
        elements: dict



# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
# extends_documentation_fragment:
#     - ocsdk.collection.my_doc_fragment_name

author:
    - Your Name (@zohiba)
"""

EXAMPLES = r'''
# Pass in a message
- name: Test with shared suboperatorconfig
  ibm.operator_collection_sdk.oc_suboperatorconfig:
    name: suboperatorconfig-1
    namespace: test-world
    credentialType: shared
    endpointMapping:
      - namespace: "test-world"
        zosendpoints:
          - name: "new-ep1"
    collection_name: "zos-package-manager.zpm.2.1.0"
    state: present

# pass in a message and have changed true
- name: Test with personal suboperatorconfig
  ibm.operator_collection_sdk.oc_suboperatorconfig:
    name: suboperatorconfig-2
    state: present
    namespace: "zarin-dev"
    credentialType: personal
    endpointMapping:
      - namespace: "zarin-dev"
        zosendpoints:
          - name: "new-ep1"
    collection_name: "zos-package-manager.zpm.2.1.0"
# fail the module
- name: Test failure of the module
  ibm.operator_collection_sdk.oc_suboperatorconfig:
    name: suboperatorconfig-3
    namespace: test-world
    state: present
    credentialType: blah
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
    # from ansible.module_utils.basic import AnsibleModule
    from ansible_collections.kubernetes.core.plugins.module_utils.k8s.core import AnsibleK8SModule
    from ansible_collections.kubernetes.core.plugins.module_utils.k8s.runner import run_module
    from ansible_collections.kubernetes.core.plugins.module_utils.k8s.exceptions import CoreException
except ImportError as e:
    DEPENDENCY_IMPORT_ERROR = f"Failed to import dependency: {e}"


def run_suboperatorconfig_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        kind=dict(type='str', default="SubOperatorConfig"),
        api_version=dict(type='str', default="zoscb.ibm.com/v2beta2"),
        name=dict(type='str', required=True),
        namespace=dict(type='str', required=True),
        collection_name=dict(type='str', required=True),
        credentialType=dict(type='str', required=True, choices=["personal", "shared"]),
        endpointMapping=dict(type="list", elements="dict", required=True),
        state=dict(type='str', required=True, choices=["absent", "present", "patched"]),
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

    environment = Environment(loader=FileSystemLoader("./templates"))
    template = environment.get_template("suboperatorconfig.yml")
    content = template.render(
        module.params
    )
    module.params["resource_definition"] = content

    # # if the user is working with this module in only check mode we do not
    # # want to make any changes to the environment, just return the current
    # # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    try:
        run_module(module)
        result["changed"] = True
    except CoreException as e:
        result["error"] = True
        module.fail_from_exception(e)
    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_suboperatorconfig_module()


if __name__ == '__main__':
    main()
