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

from re import match, MULTILINE


def remove_mount(content, omvs_zfs_data_set_name, omvs_home_directory):
    """Remove a mount command from BPXPRMxx member.

    Returns:
         str: The updated BPXPRMxx member's contents.
    """
    content_lines = content.split('\n')
    remove_starting_at_index = None
    for index, line in enumerate(content_lines):
        if match(r"^\s*MOUNT\s+FILESYSTEM\(." + omvs_zfs_data_set_name.upper() + r".\)", line, MULTILINE):
            remove_starting_at_index = index
            break
    if remove_starting_at_index is not None:
        del content_lines[remove_starting_at_index: remove_starting_at_index+3]
    return "\n".join(content_lines)


class FilterModule(object):
    """ Jinja2 filter for removing a mount from BPXPRMxx member. """

    def filters(self):
        filters = {
            "remove_mount": remove_mount,
        }
        return filters
