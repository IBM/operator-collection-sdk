#!/usr/bin/python

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: oc_zoscloudbroker
short_description: This module creates or delete an IBM® z/OS® Cloud Broker (zoscloudbroker) instance.
version_added: "2.0.0"
description: This module creates or delete an IBM® z/OS® Cloud Broker (zoscloudbroker) instance.
options:
    state:
        description: Dictates whether an instance of the zoscloudbroker is created or deleted. When set to C(present), an instance will be created, if it does not already exist. If set to C(absent), an existing instance will be deleted.
        required: false
        type: str
        default: "present"
        choices: [ "absent", "present" ]
    name:
        description: The name of the zoscloudbroker.
        required: false
        type: str
        default: "zoscloudbroker"
    namespace:
        description: The namespace in which to create the instance.
        required: true
        type: str
    accept_license:
        description: Boolean indicating if the IBM® z/OS® Cloud Broker license agreement (https://ibm.biz/ibm-zoscb-license) is accepted (a value of true indicates acceptance).
        required: true
        type: bool
    labels:
        description: Labels i.e. type=ibm-zos-cloud-broker. Key-value pairs where key and value are separated by "=".
        required: false
        default: []
        type: list
    multi_namespace_suboperators:
        description: Boolean indicating whether to expose suboperators across multiple namespaces.
        required: false
        type: bool
        default: true
    log_level:
        description: Deployment log level.
        required: false
        type: str
        default: "debug"
        choices: [ "info", "debug", "trace" ]
    ansible_galaxy_configuration:
        description: Configure Ansible Galaxy Server settings.
        enabled: 
            description: Enables Ansible Galaxy integration. Please disable when running in an air-gapped environment.
            required: false
            type: bool
            default: true
        url:
            description: Specify the URL for Ansible Galaxy.
            required: false
            type: str
            default: "https://galaxy.ansible.com"
    storage:
        description: Persistent Storage is recommended to enable the persistence of imported Ansible Collections. This may be required in clusters with network firewall configurations. For more information, please refer to https://ibm.biz/ibm-zoscb-storage.
        required: true
        configure:
            description: If set to true, create a new Persistent Volume Claim otherwise use existing PVC i.e. (PVC enabled is True).
            required: true
            type: bool
        volume_access_mode:
            description: AccessModes contains the desired access modes the volume should have (ignored if using an existing PVC).
            required: false
            type: str
            default: "ReadWriteMany"
            choices: ["ReadWriteMany"]
        storage_size:
            description: Size represents the storage size (ignored if using an existing PVC).
            required: false
            type: str
            default: "5Gi"
        storage_class:
            description: Name of the StorageClass required by the claim (ignored if using an existing PVC).
            required: false
            type: str
            default: ""
        volume_mode:
            description: VolumeMode defines what type of volume is required by the claim (ignored if using an existing PVC).
            required: false
            type: str
            default: "Filesystem"
            choices: ["Filesystem", "filesystem", "FILESYSTEM"]
        persistent_volume_claim:
            description: Utilize An Existing Persistent Volume Claim (ignored if configuring a new PVC).
            required: false
            default: "zoscloudbroker"
            
# extends_documentation_fragment:
#     - ibm.operator_collection_sdk.doc_fragment

author:
    - Yemi Kelani (@yemi-kelani)
'''

# Usage examples
EXAMPLES = r'''
  - name: Create ZosCloudBroker
    ibm.operator_collection_sdk.oc_zoscloudbroker:
        state: present
        namespace: yemi-test
        accept_license: true
        multi_namespace: true
        log_level: trace
        storage:
            configure: true
            storage_class: rook-cephfs
    register: zcb_results

  - name: Create ZosCloudBroker
    ibm.operator_collection_sdk.oc_zoscloudbroker:
        state: present
        name: zoscloudbroker
        namespace: yemi-test
        accept_license: true
        multi_namespace: true
        log_level: debug
        labels:
            - test=true
            - namespace=yemi-test
        storage:
            enabled: true
            pvc: zoscloudbroker

  - name: Create ZosCloudBroker
    ibm.operator_collection_sdk.oc_zoscloudbroker:
        state: present
        namespace: yemi-test-2
        accept_license: true
        storage:
        enabled: true
        pvc: zoscloudbroker
    register: zcb_results

  - name: Delete ZosCloudBroker
    ibm.operator_collection_sdk.oc_zoscloudbroker:
        state: absent
        name: zoscloudbroker
        namespace: yemi-test-2
    register: zcb_results
'''
# Examples of returns
RETURN = r'''
{
    "changed": true,
    "error": false,
    "failed": false,
    "state": {
        "apiVersion": "v1",
        "details": {
            "group": "zoscb.ibm.com",
            "kind": "zoscloudbrokers",
            "name": "zoscloudbroker",
            "uid": "13fd4922-6fce-4d2f-9920-a7d227a65f24"
        },
        "kind": "Status",
        "metadata": {},
        "status": "Success"
    }
}

{
    "changed": true,
    "error": false,
    "failed": false,
    "state": {
        "apiVersion": "zoscb.ibm.com/v2beta1",
        "kind": "ZosCloudBroker",
        "metadata": {
            "creationTimestamp": "2024-02-22T01:01:02Z",
            "generation": 1,
            "managedFields": [
                {
                    "apiVersion": "zoscb.ibm.com/v2beta1",
                    "fieldsType": "FieldsV1",
                    "fieldsV1": {
                        "f:spec": {
                            ".": {},
                            "f:catalogResources": {},
                            "f:galaxyConfig": {
                                ".": {},
                                "f:enabled": {},
                                "f:galaxyURL": {}
                            },
                            "f:license": {
                                ".": {},
                                "f:accept": {}
                            },
                            "f:logLevel": {},
                            "f:managerResources": {},
                            "f:multiNamespace": {},
                            "f:storage": {
                                ".": {},
                                "f:configure": {},
                                "f:enabled": {},
                                "f:pvc": {}
                            },
                            "f:uiResources": {}
                        }
                    },
                    "manager": "OpenAPI-Generator",
                    "operation": "Update",
                    "time": "2024-02-22T01:01:02Z"
                }
            ],
            "name": "zoscloudbroker",
            "namespace": "yemi-test-2",
            "resourceVersion": "148579203",
            "uid": "0db17b06-fed4-4d63-b82d-3bb021849933"
        },
        "spec": {
            "catalogResources": {},
            "galaxyConfig": {
                "enabled": true,
                "galaxyURL": "https://galaxy.ansible.com"
            },
            "license": {
                "accept": true
            },
            "logLevel": "debug",
            "managerResources": {},
            "multiNamespace": true,
            "storage": {
                "configure": false,
                "enabled": true,
                "pvc": "zoscloudbroker"
            },
            "uiResources": {}
        }
    }
}
'''

# import kubernetes
import re
import yaml
from kubernetes import client, config
from jinja2 import Environment, FileSystemLoader
from ansible.module_utils.basic import AnsibleModule

def run_module():
    module_args = dict(
        state=dict(type="str", required=False, default="present", choices=[ "absent", "present" ]),
        name=dict(type="str", required=False, default="zoscloudbroker"),
        namespace=dict(type="str", required=True),
        accept_license=dict(type="bool", required=False),
        labels=dict(type="list", required=False, default=[]),
        multi_namespace_suboperators=dict(type="bool", required=False, default=True, aliases=["multi_namespace"]),
        log_level=dict(type="str", required=False, default="debug", choices=[ "info", "debug", "trace" ]),
        ansible_galaxy_configuration=dict(
            type="dict",
            required=False,
            default={"enabled": True, "url": "https://galaxy.ansible.com"},
            aliases=["galaxy_configuration", "galaxyConfig", "galaxy_config"],
            options=dict(
                enabled=dict(type="bool", required=False, default=True),
                url=dict(type="str", required=False, default="https://galaxy.ansible.com"),
            )
        ),
        storage=dict(
            type="dict",
            required=False,
            options=dict(
                configure=dict(type="bool", required=False),
                enabled=dict(type="bool", required=False),
                volume_access_mode=dict(type="str", default="ReadWriteMany", choices=["ReadWriteMany"]),
                storage_size=dict(type="str", required=False, default="5Gi"),
                storage_class=dict(type="str", required=False),
                volume_mode=dict(type="str", required=False, default="Filesystem", choices=["Filesystem", "filesystem", "FILESYSTEM"]),
                persistent_volume_claim=dict(type="str", required=False, aliases=["pvc", "volume_claim"])
            )
        )
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ["state", "present", ["accept_license", "storage"], True],
            ["state", "absent", ["name"], True]
        ]
    )

    result = dict(
        changed=False, # if this module effectively modified the target
        state={},      # any data that you want your module to pass back for consumption in a subsequent task
        error=False
    )

    validated_params = validate_module_parameters(module=module, result=result)

    # if in only check mode, return the state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # load template and render yaml object
    environment = Environment(loader=FileSystemLoader("./templates/"))
    template = environment.get_template("zoscloudbroker.yml")
    content = template.render(validated_params)
    yaml_object = yaml.safe_load(content)

    config.load_kube_config()
    v1 = client.CoreV1Api()

    # create or delete zoscloudbroker instance
    crd_resource, error = change_zoscloudbroker_state(validated_params, yaml_object=yaml_object)
    
    result["state"] = crd_resource

    # determine if modifications were made on target
    if error is None:
        result["changed"] = True
    else:
        result["error"] = True
        module.fail_json(msg=str(error), **result)

    # successful module execution, exit and pass results
    module.exit_json(**result)

def validate_module_parameters(module, result):
    # make a copy of module params  
    params_copy = {**module.params}

    if params_copy["state"] == "absent":
        return params_copy

    # set default values if necessary
    if "configure" not in params_copy["storage"]:
        params_copy["storage"]["configure"] = False
    if "enabled" not in params_copy["storage"]:
        params_copy["storage"]["enabled"] = False

    # validate storage has either configured or enabled or both are false
    if params_copy["storage"]["configure"] and params_copy["storage"]["enabled"]:
        module.fail_json(
            msg=f"Invalid parameters; Storage parameters 'configure' and 'enabled' cannot both be true.",
            **result)

    # validate required params are present
    if params_copy["storage"]["configure"]:
        required_params = [
            # "volume_access_mode"
            # "volume_mode",
            # "storage_size",
            "storage_class"
        ]
        for param in required_params:
            if param not in params_copy["storage"] \
            or params_copy["storage"][param] is None:
                module.fail_json(
                    msg=f"Missing required argument '{param}'. The following arguments must be suppled when argument storage.configure is True: {", ".join(required_params)}.",
                    **result)
    elif params_copy["storage"]["enabled"]:
            # if configure is false, but enabled is true
            # ensure persistent_volume_claim param is valid
            pvc_alias = get_present_alias(
                "persistent_volume_claim", module, 
                aliases=module.argument_spec["storage"]["options"], 
                params=params_copy["storage"])
            
            if pvc_alias == "" \
            or params_copy["storage"][pvc_alias] is None \
            or params_copy["storage"][pvc_alias] == "":
                module.fail_json(
                    msg=f"Missing required argument '{pvc_alias}'. {pvc_alias} must be suppled when argument storage.enabled is True.",
                    **result)

    # validate label format if they exist
    if "labels" in params_copy:
        labels = {}
        for label in params_copy["labels"]:
            if re.match("^[^=]*=[^=]*$", label) is None:
                module.fail_json(
                    msg=f"Recieved label with misshapen form: '{label}'. Each label in the list should take the form 'key=value'.",
                    **result)
            else:
                [key, value] = label.split("=")
                labels[key] = value
        
        params_copy["labels"] = labels

    return params_copy
    
# Gets the alias being used for a certain argument
def get_present_alias(real_arg_name, module, aliases=None, params=None):
    params = module.params if params is None else params
    aliases = module.argument_spec[real_arg_name]["aliases"] if aliases is None else aliases

    if real_arg_name in params:
        return real_arg_name
    
    for alias in aliases:
        if alias in module.params:
            return alias
    
    return ""

def change_zoscloudbroker_state(params, yaml_object):
    state = params["state"]
    namespace = params["namespace"]
    name = params["name"]
    try:
        if state == "absent":
            crd_resource = client.CustomObjectsApi().delete_namespaced_custom_object(
                group="zoscb.ibm.com", 
                version="v2beta1", 
                plural="zoscloudbrokers",
                namespace=namespace,
                name=name)
        elif state == "present":
            crd_resource = client.CustomObjectsApi().create_namespaced_custom_object(
                group="zoscb.ibm.com", 
                version="v2beta1", 
                plural="zoscloudbrokers", 
                body=yaml_object, 
                namespace=namespace)

        return crd_resource, None
    except Exception as e:
        return None, e

def main():
    run_module()

if __name__ == '__main__':
    main()