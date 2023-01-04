Role Name
=========

Ansible my_own_role role deployment.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, 
if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------
A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, 
vars/main.yml, and any variables that can/should be set via parameters to the role. 
Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

    ansible_python_interpreter:
        description:   Required version of interpreter.
        default value: /usr/bin/python3
    path:
        description:
            - This is the path to newly creating file.
        required: true
        type: str
        default value: "/root/"
    content:
        description:
            - This is the content of newly creating file.
        required: true
        type: str
        default value: "Some text"
    name:
        description:
            - This is a name of newly creating file.
        required: true
        type: str
        default value: "first.md"

 
Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: my_own_role }

License
-------

BSD

Author Information
------------------

Edward Burlakov,  edwardb@mail.ru
