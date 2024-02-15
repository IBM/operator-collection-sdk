#!/usr/bin/python

# Copyright: (c) 2024, Zarin Ohiba <zarin.ohiba@ibm.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
import kubernetes
import csv, os, json, yaml
from jinja2 import Environment, FileSystemLoader

from kubernetes import client, config, watch

__metaclass__ = type

DOCUMENTATION = r'''
---
module: oc_zosendpoint

short_description: This module creates a zosendpoint

version_added: "1.0.0"

description: This module creates a zosendpoint.

options:
    state:
        description: Determines if an object should be created, patched, or deleted. When set to C(present), an object will be created, if it does not already exist. If set to C(absent), an existing object will be deleted. If set to C(present), an existing object will be patched, if its attributes differ from those specified using I(resource_definition) or I(src). C(patched) state is an existing resource that has a given patch applied. If the resource doesn't exist, silently skip it (do not raise an error).
        type: str
        required: true
        default: present
        choices: [ absent, present, patched ]
    name:
        description: The name of the zosendpoint.
        required: true
        type: str
    namespace:
        description: The endpoint is created in this provided namespace.
        required: true
        type: str
    endpointType:
        description: Sets endpoint type to remote or local.
        required: true
        type: str
    host:
        description: If provided, it sets host of the zosendpoint.
        required: false
        type: str
    port:
        description: If provided, it sets port of the zosendpoint.
        required: false
        type: int
    variables:
        description: If provided, it sets vars of the zosendpoint.
        required: false
        type: list

    
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
# extends_documentation_fragment:
#     - ocsdk.collection.my_doc_fragment_name

author:
    - Your Name (@zohiba)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with remote endpointType
  ocsdk.collection.oc_zosendpoint:
    name: endpoint-1
    namespace: test-world
    host: test-host-1
    port: 123
    endpointType: remote
    state: present

# pass in a message and have changed true
- name: Test with local endpointType
  ocsdk.collection.oc_zosendpoint:
    name: endpoint-2
    namespace: test-world
    state: present
    endpointType: local
# fail the module
- name: Test failure of the module
  ocsdk.collection.oc_zosendpoint:
    name: endpoint-3
    namespace: test-world
    state: blah
    endpointType: blah
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


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        namespace=dict(type='str', required=True),
        host=dict(type='str', required=False),
        port=dict(type='int', required=False),
        endpointType=dict(type='str', required=True, choices=["remote", "local" ]),
        variables=dict(type="list", required=False, default=[]),
        state=dict(type='str', required=True, choices=[ "absent", "present", "patched" ]),
    )

    # make sure host and port is provided when endpointType is set to "remote"
    required_if_args = [
    ["endpointType", "remote", ["host", "port"]]
    ]

    # seed the result dict in the object
    # we primarily care about changed and resource
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        resource='',
        error=False,
       
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if = required_if_args,
    )

    errorMsg = verify_arguments_passed(module)

    if errorMsg != None:
        result['error'] = True
        module.fail_json(msg=errorMsg, **result)

    #config.load_incluster_config() #used during testing inside cluster, also needs to give permission to SA to list endpoints
    # config.load_incluster_config()
    # v1 = client.CoreV1Api()
    config.load_kube_config()

    v1 = client.CoreV1Api()
    
    environment = Environment(loader=FileSystemLoader("./templates"))
    template = environment.get_template("endpoint.yml")
    content = template.render(
        module.params
    )
    # print(content)
    yaml_object = yaml.safe_load(content)
    # print(yaml_object)

    # this is going to be the part where your module will do what it needs to do
    crd_resource, changed, err, errorMsg = endpoint_action(module, yaml_object)
   
    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    result['resource'] = crd_resource
    result['error'] = err
    result['changed'] = changed

    if err:
        module.fail_json(msg=errorMsg, **result)
    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result

    
    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def verify_arguments_passed(module):

    
    if module.params["endpointType"] == "local" and (module.params["host"] or module.params["port"]):
        return "EndpointType local shouldn't have host or port defined"

    if module.params["endpointType"] == "remote" and module.params["host"] == "":
        return "Valid Host required when endpointType is remote"

    if module.params["endpointType"] == "remote" and module.params["port"] <=0 :
        return "Valid Port required when endpointType is remote"

    return None

def endpoint_action(module, yaml_object):
    # Given the module(params,kubeconfig etc) check the desired state of the resource and apply the kubernetes API accordingly.
    crd_resource=""
    err= False
    changed = False
    try:
        if module.params["state"] == "present":
            crd_resource = kubernetes.client.CustomObjectsApi().create_namespaced_custom_object(group="zoscb.ibm.com", version="v2beta2", plural="zosendpoints", body=yaml_object, namespace=module.params["namespace"])
            changed = True
        elif module.params["state"] == "absent":
            crd_resource = kubernetes.client.CustomObjectsApi().delete_namespaced_custom_object(group="zoscb.ibm.com", version="v2beta2", plural="zosendpoints", name=module.params["name"] , namespace=module.params["namespace"])
            changed = True
        elif module.params["state"] == "patched":
            crd_resource = kubernetes.client.CustomObjectsApi().patch_namespaced_custom_object(group="zoscb.ibm.com", version="v2beta2", plural="zosendpoints", name=module.params["name"] ,body=yaml_object, namespace=module.params["namespace"])
            changed = True
    
        return crd_resource,changed, err, None
    except Exception as e:
        err = True
        return crd_resource, changed, err, str(e)

def main():
    run_module()


if __name__ == '__main__':
    main()