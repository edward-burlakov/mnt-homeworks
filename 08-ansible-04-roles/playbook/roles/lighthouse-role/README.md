Role Name
=========

Ansible lighthouse role deployment.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, 
vars/main.yml, and any variables that can/should be set via parameters to the role. 
Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

    nginx_user: "nginx"                          # NGINX user 
    lighthouse_version: "7.10.1"                 # Lighthouse version
    nginx_home: "/etc/nginx"                     # Path to configuration files of NGINX
    default_web_root: "/usr/share/nginx/html"    # Path to default webpage of NGINX
    virtual_domain: "lighthouse-master"          # Path to virtual domain of light

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: lighthouse-role }

License
-------


Author Information
------------------

Edward Burlakov,  edwardb@mail.ru
