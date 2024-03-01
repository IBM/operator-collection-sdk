import json

from ansible.module_utils import basic
from ansible.module_utils.common.text.converters import to_bytes


def error_equal(error1: str, error2: str) -> bool:
    return str(error1).replace(" ", "") == str(error2).replace(" ", "")


def set_module_args(args, check_mode=False):
    """prepare arguments so that they will be picked up during module creation"""
    anisble_module_args = {"ANSIBLE_MODULE_ARGS": args}
    if check_mode:
        anisble_module_args["ANSIBLE_MODULE_ARGS"]["_ansible_check_mode"] = True
    args = json.dumps(anisble_module_args)
    basic._ANSIBLE_ARGS = to_bytes(args)


class AnsibleExitJson(Exception):
    """Exception class to be raised by module.exit_json and caught by the test case"""
    pass


class AnsibleFailJson(Exception):
    """Exception class to be raised by module.fail_json and caught by the test case"""
    pass


def exit_json(*args, **kwargs):
    """function to patch over exit_json; package return data into an exception"""
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    """function to patch over fail_json; package return data into an exception"""
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)


def get_bin_path(self, arg, required=False):
    """Mock AnsibleModule.get_bin_path"""
    if arg.endswith('my_command'):
        return '/usr/bin/my_command'
    else:
        if required:
            fail_json(msg='%r not found !' % arg)
