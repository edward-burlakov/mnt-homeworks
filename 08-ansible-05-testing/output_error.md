** root@docker:~/vector-role# ** docker run --privileged=True -v /root/vector-role:/opt/vector-role -w /opt/vector-role -it aragast/netology:latest /bin/bash

** [root@593f62096d3a vector-role]# **  tox
py39-ansible210 installed: ansible==2.10.7,ansible-base==2.10.17,ansible-compat==2.2.7,ansible-lint==5.1.3,arrow==1.2.3,attrs==22.2.0,bcrypt==4.0.1,binaryornot==0.4.4,bracex==2.3.post1,Cerberus==1.3.2,certifi==2022.12.7,cffi==1.15.1,chardet==5.1.0,charset-normalizer==2.1.1,click==8.1.3,click-help-colors==0.9.1,commonmark==0.9.1,cookiecutter==2.1.1,cryptography==38.0.4,distro==1.8.0,enrich==1.2.7,idna==3.4,Jinja2==3.1.2,jinja2-time==0.2.0,jmespath==1.0.1,jsonschema==4.17.3,lxml==4.9.2,MarkupSafe==2.1.1,molecule==3.4.0,molecule-podman==1.0.1,packaging==22.0,paramiko==2.12.0,pathspec==0.10.3,pluggy==0.13.1,pycparser==2.21,Pygments==2.13.0,PyNaCl==1.5.0,pyrsistent==0.19.2,python-dateutil==2.8.2,python-slugify==7.0.0,PyYAML==5.4.1,requests==2.28.1,rich==12.6.0,ruamel.yaml==0.17.21,ruamel.yaml.clib==0.2.7,selinux==0.3.0,six==1.16.0,subprocess-tee==0.4.1,tenacity==8.1.0,text-unidecode==1.3,urllib3==1.26.13,wcmatch==8.4.1,yamllint==1.26.3
py39-ansible210 run-test-pre: PYTHONHASHSEED='4048709327'
py39-ansible210 run-test: commands[0] | molecule test -s compatibility --destroy always
INFO     compatibility scenario test matrix: dependency, lint, cleanup, destroy, syntax, create, prepare, converge, side_effect, verify, cleanup, destroy
INFO     Performing prerun...
WARNING  Failed to locate command: [Errno 2] No such file or directory: 'git'
INFO     Guessed /opt/vector-role as project root directory
INFO     Using /root/.cache/ansible-lint/b984a4/roles/edwardburlakov.vector symlink to current repository in order to enable Ansible to find the role using its expected full name.
INFO     Added ANSIBLE_ROLES_PATH=~/.ansible/roles:/usr/share/ansible/roles:/etc/ansible/roles:/root/.cache/ansible-lint/b984a4/roles
INFO     Running compatibility > dependency
INFO     Running ansible-galaxy collection install --force -v containers.podman:>=1.7.0
INFO     Running ansible-galaxy collection install --force -v ansible.posix:>=1.3.0
WARNING  Skipping, dependency is disabled.
WARNING  Skipping, dependency is disabled.
INFO     Running compatibility > lint
COMMAND: ansible-lint .
yamllint .

Failed to locate command: [Errno 2] No such file or directory: 'git'
Traceback (most recent call last):
  File "/opt/vector-role/.tox/py39-ansible210/bin/ansible-lint", line 8, in <module>
    sys.exit(_run_cli_entrypoint())
  File "/opt/vector-role/.tox/py39-ansible210/lib/python3.9/site-packages/ansiblelint/__main__.py", line 299, in _run_cli_entrypoint
    sys.exit(main(sys.argv))
  File "/opt/vector-role/.tox/py39-ansible210/lib/python3.9/site-packages/ansiblelint/__main__.py", line 211, in main
    from ansiblelint.generate_docs import rules_as_rich, rules_as_rst, rules_as_str
  File "/opt/vector-role/.tox/py39-ansible210/lib/python3.9/site-packages/ansiblelint/generate_docs.py", line 6, in <module>
    from rich.console import render_group
ImportError: cannot import name 'render_group' from 'rich.console' (/opt/vector-role/.tox/py39-ansible210/lib/python3.9/site-packages/rich/console.py)
^CERROR: got KeyboardInterrupt signal

Aborted!
