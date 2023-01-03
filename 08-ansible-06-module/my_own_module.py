#!/usr/bin/python3

# Copyright: (c) 2022, Edward Burlakovs <edwardb@mail.ru>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
# Импортируем библиотеки Python
from ansible.module_utils.basic import AnsibleModule
import os

DOCUMENTATION = r'''
---
module: my_own_module

short_description: This is my first module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.1"

description: This is my longer description explaining my first module.

options:
    path:
        description:
            - This is the path to newly creating file.
        required: true
        type: str
    content:
        description:
            - This is the content of  newly creating file.
        required: true
        type: str
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    -  edward-burlakov.my_ansible_collection.my_doc_own_module:

author:
    - Edward Burlakov (@edward-burlakov)
'''

EXAMPLES = r'''
# Create file and fill it with content
- name: Touch a file with predefined content
  edward-burlakov.my_ansible_collection.my_own_module:
    path: /root/
    content: "Hello, Edward!"
'''
RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
'''


def run_module():

# define available arguments/parameters a user can pass to the module
    module_args = dict(
         path=dict(type='path', required=True),
         content=dict(type='str', required=True)
    )

# seed the result dict in the object
# we primarily care about changed and state
# changed is if this module effectively modified the target
# state will include any data that you want your module to pass back
# for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='File created  successfully.',
        message=''
    )

# the AnsibleModule object will be our abstraction working with Ansible
# this includes instantiation, a couple of common attr would be the
# args/params passed to the execution, as well as if the module
# supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )


# use whatever logic you need to determine whether or not this module
# made any modifications to your target
    if module.params['content']:
        result['changed'] = True


# Инициализируем переменные
    fpath1 = module.params['path']
    fcontent1 = module.params['content']
    full_tmp_path = os.path.join("/tmp/", "text.txt")
    full_dest_path = os.path.join(fpath1, "text.txt")
#  Создаем файл и записываем содержимое в файл
    f = open(full_tmp_path, "w")
    f.write(fcontent1)
    f.close()
#   Копируем готовый файл из  временного каталога
    module.atomic_move(full_tmp_path, full_dest_path, unsafe_writes=False)

# in the event of a successful module execution, you will want to
# simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
# Запускаем модуль run_module, передавая внутрь внешние аргументы модуля.
    run_module()

if __name__ == '__main__':
    main()
