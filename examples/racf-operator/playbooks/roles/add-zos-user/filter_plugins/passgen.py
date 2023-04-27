##############################################################################
# Copyright 2023 IBM Corp. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
##############################################################################

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from string import ascii_lowercase, ascii_uppercase, digits
from random import choice
from re import match, MULTILINE

def generate_password(input, pass_len=8):
    """Generate a password.

    Returns:
        str: The generated password.
    """
    choices = [
        ascii_uppercase,
        digits,
    ]
    password = "".join([choice(choice(choices)) for x in range(pass_len)])
    return password


def generate_passphrase(input, pass_len=16, userid=None):
    """Generate a passphrase.

    Returns:
        str: The generated passphrase.
    """
    choices = [
        ascii_uppercase,
        digits,
        ascii_lowercase
    ]
    passphrase = ""
    good_passphrase_found = False
    while not good_passphrase_found:
        passphrase = "".join([choice(choice(choices)) for x in range(pass_len)])
        if match(r"^(([a-z0-9])\2?(?!\2))+$", passphrase, MULTILINE):
            good_passphrase_found = True
            if userid and userid in passphrase:
                 good_passphrase_found = False
    return passphrase

class FilterModule(object):
    """ Jinja2 filters for generating passwords """

    def filters(self):
        filters = {
            "generate_password": generate_password,
            "generate_passphrase": generate_passphrase,
        }
        return filters
