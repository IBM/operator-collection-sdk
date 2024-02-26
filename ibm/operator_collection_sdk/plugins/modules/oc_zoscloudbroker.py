#!/usr/bin/python

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: oc_zoscloudbroker

short_description: This module creates or delete an IBM® z/OS® Cloud Broker (zoscloudbroker) instance.

version_added: "2.0.0"

author:
  - Yemi Kelani (@yemi-kelani)

description: This module creates or delete an IBM® z/OS® Cloud Broker (zoscloudbroker) instance.
options:
  state:
    description: >
      Dictates whether an instance of the zoscloudbroker is created or deleted.
      When set to C(present), an instance will be created, if it does not already exist.
      If set to C(absent), an existing instance will be deleted.
    required: false
    type: str
    default: "present"
    choices: ["absent", "present"]
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
    description: >
      Boolean indicating if the IBM® z/OS® Cloud Broker license agreement (https://ibm.biz/ibm-zoscb-license)
      is accepted (a value of true indicates acceptance).
    required: false
    type: bool
    default: false
  labels:
    description: Labels i.e. type=ibm-zos-cloud-broker. Key-value pairs where key and value are separated by "=".
    required: false
    default: []
    type: list
    elements: str
  multi_namespace_suboperators:
    description: Boolean indicating whether to expose suboperators across multiple namespaces.
    required: false
    type: bool
    default: true
    aliases: ["multi_namespace"]
  log_level:
    description: Deployment log level.
    required: false
    type: str
    default: "debug"
    choices: ["info", "debug", "trace"]
  ansible_galaxy_configuration:
    description: Configure Ansible Galaxy Server settings.
    type: dict
    default: {'enabled': 'true', 'url': 'https://galaxy.ansible.com'}
    aliases: ["galaxyConfig", "galaxy_config", "galaxy_configuration"]
    suboptions:
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
    description: >
      Persistent Storage is recommended to enable the persistence of imported Ansible Collections. This may be
      required in clusters with network firewall configurations. For more information, please refer to
      https://ibm.biz/ibm-zoscb-storage.
    required: false
    type: dict
    suboptions:
      configure:
        description: >
          If set to true, create a new Persistent Volume Claim otherwise use existing PVC i.e.
          (PVC enabled is True).
        required: false
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
      volume_mode:
        description: VolumeMode defines what type of volume is required by the claim (ignored if using an existing PVC).
        required: false
        type: str
        default: "Filesystem"
        choices: ["Filesystem", "filesystem", "FILESYSTEM"]
      persistent_volume_claim:
        description: Utilize An Existing Persistent Volume Claim (ignored if configuring a new PVC).
        required: false
        type: str
        aliases: ["pvc", "volume_claim"]

# extends_documentation_fragment:
#   - ibm.operator_collection_sdk.documentaion
"""

EXAMPLES = r"""
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
"""

RETURN = r"""
changed:
  description: Boolean indicating whether target was modified.
  returned: always
  type: bool
error:
  description: Boolean indicating whether the module errored.
  returned: always
  type: bool
result:
  description: The Custom Resource Definition returned by the performed operation.
  returned: success
  type: complex
  contains:
    api_version:
      description: Version schema.
      returned: success
      type: str
      sample: v1
    kind:
      description: The resource type this object is.
      returned: success
      type: str
      sample: Status
    status:
      description: The status of the request.
      returned: success
      type: str
      sample: Success
    metadata:
      description: Target resource metadata.
      returned: success
      type: complex
    details:
      description: Information about the target resource.
      returned: success
      type: complex
      contains:
        group:
          description: API group.
          returned: success
          type: str
          sample: zoscb.ibm.com
        kind:
          description: Custom resource kind.
          returned: success
          type: str
          sample: zoscloudbrokers
        name:
          description: Custom resource name.
          returned: success
          type: str
          sample: zoscloudbroker
        uid:
          description: Resource UID.
          returned: success
          type: str
          sample: 1f922d43-ce6f-42fd-9290-75f2a274a6d2
"""

from ansible.module_utils.basic import AnsibleModule

DEPENDENCY_IMPORT_ERROR = None

try:
    import re
    from jinja2 import Environment, FileSystemLoader
    from ansible_collections.kubernetes.core.plugins.module_utils.k8s.core import AnsibleK8SModule
    from ansible_collections.kubernetes.core.plugins.module_utils.k8s.runner import run_module
    from ansible_collections.kubernetes.core.plugins.module_utils.k8s.exceptions import CoreException
except ImportError as e:
    DEPENDENCY_IMPORT_ERROR = f"Failed to import dependency: {e}"


def run_zoscloudbroker_module():
    module_args = dict(
        state=dict(type="str", required=False, default="present", choices=["absent", "present"]),
        name=dict(type="str", required=False, default="zoscloudbroker"),
        namespace=dict(type="str", required=True),
        accept_license=dict(type="bool", required=False, default=False),
        labels=dict(type="list", elements="str", required=False, default=[]),
        multi_namespace_suboperators=dict(type="bool", required=False, default=True, aliases=["multi_namespace"]),
        log_level=dict(type="str", required=False, default="debug", choices=["info", "debug", "trace"]),
        ansible_galaxy_configuration=dict(
            type="dict",
            required=False,
            default=dict(enabled="true", url="https://galaxy.ansible.com"),
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

    if DEPENDENCY_IMPORT_ERROR is not None:
        module = AnsibleModule(argument_spec=module_args)
        module.fail_json(msg=DEPENDENCY_IMPORT_ERROR)

    module = AnsibleK8SModule(
        module_class=AnsibleModule,
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ["state", "present", ["accept_license", "storage"], True],
            ["state", "absent", ["name"], True]
        ]
    )

    result = dict(
        changed=False,  # if this module effectively modified the target
        error=False
    )

    # if in only check mode, return the state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    validated_params = validate_module_parameters(module=module, result=result)

    # load template and render CRD
    environment = Environment(loader=FileSystemLoader("./templates/"))
    template = environment.get_template("zoscloudbroker.yml")
    custom_resource_definition = template.render(validated_params)
    module.params["resource_definition"] = custom_resource_definition

    # attempt to modify target
    try:
        run_module(module)
        result["changed"] = True
    except CoreException as e:
        result["error"] = True
        module.fail_from_exception(e)

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
            msg="Invalid parameters; Storage parameters 'configure' and 'enabled' cannot both be true.",
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
                    or params_copy["storage"][param] == "" \
                    or params_copy["storage"][param] is None:
                module.fail_json(
                    msg=f"Missing required argument '{param}'. The following arguments must be suppled when \
                        argument storage.configure is True: {', '.join(required_params)}.",
                    **result)
    elif params_copy["storage"]["enabled"]:
        if "persistent_volume_claim" not in params_copy["storage"] \
                or params_copy["storage"]["persistent_volume_claim"] == "" \
                or params_copy["storage"]["persistent_volume_claim"] is None:
            module.fail_json(
                msg="Missing required argument 'persistent_volume_claim'. persistent_volume_claim must be \
                    suppled when argument storage.enabled is True.",
                **result)

    # validate label format if they exist
    if "labels" in params_copy:
        labels = {}
        for label in params_copy["labels"]:
            if re.match("^[^=]*=[^=]*$", label) is None:
                module.fail_json(
                    msg=f"Recieved label with misshapen form: '{label}'. Each label in the list should take the \
                        form 'key=value'.",
                    **result)
            else:
                [key, value] = label.split("=")
                labels[key] = value

        params_copy["labels"] = labels

    return params_copy


def main():
    run_zoscloudbroker_module()


if __name__ == '__main__':
    main()
