# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import unittest
from unittest.mock import patch
from ansible.module_utils.basic import AnsibleModule

from plugins.modules import oc_zoscloudbroker
from tests.unit.utils.mock import (
    error_equal,
    fail_json,
    exit_json,
    AnsibleFailJson,
    AnsibleExitJson,
    set_module_args,
    get_bin_path
)


class TestValidateParams(unittest.TestCase):
    mock_module_params = dict(
        state="present",  # present, absent
        name="zoscloudbroker",
        namespace="fake-namespace",
        accept_license=True,
        labels=[],
        multi_namespace_suboperators=True,
        log_level="debug",  # info, debug, trace
        ansible_galaxy_configuration=dict(
            enabled="true",
            url="https://galaxy.ansible.com"
        ),
        storage=dict(
            configure=False,
            enabled=False,
            volume_access_mode="ReadWriteMany",
            storage_size="5Gi",
            storage_class="fake-storage-class",
            volume_mode="Filesystem",
            persistent_volume_claim="zoscloudbroker"
        )
    )

    def setUp(self):
        self.mock_module_helper = patch.multiple(
            AnsibleModule,
            exit_json=exit_json,
            fail_json=fail_json,
            get_bin_path=get_bin_path
        )

        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def test_module_fails_when_no_args_passed(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            oc_zoscloudbroker.create_and_validate_module()

    def test_module_fails_when_storage_enabled_and_configure_true(self):
        with self.assertRaises(AnsibleFailJson) as result:
            args = {**self.mock_module_params}
            args["storage"]["enabled"] = True
            args["storage"]["configure"] = True
            set_module_args(args)
            oc_zoscloudbroker.create_and_validate_module()

        assert (
            result.exception.args[0]["msg"]
            == "Invalid parameters; Storage parameters 'configure' and 'enabled' cannot both be true."
        )

    def test_module_fails_when_storage_enabled_and_pcv_missing(self):
        with self.assertRaises(AnsibleFailJson) as result:
            args = {**self.mock_module_params}
            args["storage"] = {"enabled": True}
            set_module_args(args)
            oc_zoscloudbroker.create_and_validate_module()

        assert (
            error_equal(
                result.exception.args[0]["msg"],
                "Missing required argument 'persistent_volume_claim'. persistent_volume_claim must be \
                suppled when argument storage.enabled is True."))

    def test_module_created_when_storage_enabled_pcv_present(self):
        with self.assertRaises(AnsibleExitJson):
            args = {**self.mock_module_params}
            args["storage"]["enabled"] = True
            set_module_args(args, check_mode=True)
            oc_zoscloudbroker.main()

    def test_module_fails_when_storage_configured_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson) as result:
            args = {**self.mock_module_params}
            args["storage"] = {"configure": True}
            set_module_args(args)
            oc_zoscloudbroker.create_and_validate_module()

        assert (
            error_equal(
                result.exception.args[0]["msg"],
                "Missing required argument 'storage_class'. The following arguments must be suppled when \
                argument storage.configure is True: storage_class."))

    def test_module_created_when_storage_configured_required_args_present(self):
        with self.assertRaises(AnsibleExitJson):
            args = {**self.mock_module_params}
            args["storage"]["configure"] = True
            set_module_args(args, check_mode=True)
            oc_zoscloudbroker.main()

    def test_module_validates_and_constructs_valid_labels_arg(self):
        args = {**self.mock_module_params}
        args["labels"] = ["TestLabel1=LabelValue1", "TestLabel2=LabelValue2"]
        set_module_args(args)
        ignore1, ignore2, params = oc_zoscloudbroker.create_and_validate_module()

        labels = params["labels"]
        assert ("TestLabel1" in labels and labels["TestLabel1"] == "LabelValue1")
        assert ("TestLabel2" in labels and labels["TestLabel2"] == "LabelValue2")

    def test_module_fails_when_labels_arg_invalid(self):
        with self.assertRaises(AnsibleFailJson) as result:
            misshapenLabel = "This=Is=A=Misshapen=Label"

            args = {**self.mock_module_params}
            args["labels"] = [misshapenLabel]
            set_module_args(args)
            oc_zoscloudbroker.create_and_validate_module()

        assert (
            error_equal(
                result.exception.args[0]["msg"],
                "Recieved label with misshapen form: '{}'. Each label in the list should take the \
                form 'key=value'.".format(misshapenLabel)))

        with self.assertRaises(AnsibleFailJson) as result:
            misshapenLabel = "AMisshapenLabel"

            args["labels"] = [misshapenLabel]
            set_module_args(args)
            oc_zoscloudbroker.create_and_validate_module()

        assert (
            error_equal(
                result.exception.args[0]["msg"],
                "Recieved label with misshapen form: '{}'. Each label in the list should take the \
                form 'key=value'.".format(misshapenLabel)))
