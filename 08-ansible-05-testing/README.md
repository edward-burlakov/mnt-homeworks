### Molecule
----

1) Запустите molecule test -s centos_7 внутри корневой директории clickhouse-role ( Ошибка) , посмотрите на вывод команды.

            root@docker:/#  cd /etc/ansible/roles/ansible-clickhouse
            root@docker:/#  ls -la
            total 72
            drwxr-xr-x 10 root root  4096 Dec 21 05:56 .
            drwxr-xr-x  5 root root  4096 Dec 21 05:56 ..
            drwxr-xr-x  2 root root  4096 Dec 21 05:56 defaults
            drwxr-xr-x  3 root root  4096 Dec 21 05:56 .github
            -rw-rw-r--  1 root root    62 Jul 26 15:10 .gitignore
            drwxr-xr-x  2 root root  4096 Dec 21 05:56 handlers
            drwxr-xr-x  2 root root  4096 Dec 21 05:56 meta
            drwxr-xr-x 12 root root  4096 Dec 21 05:56 molecule
            -rw-rw-r--  1 root root 13124 Jul 26 15:10 README.md
            -rw-rw-r--  1 root root  1153 Jul 26 15:10 requirements-test.txt
            drwxr-xr-x  5 root root  4096 Dec 21 05:56 tasks
            drwxr-xr-x  2 root root  4096 Dec 21 05:56 templates
            -rw-rw-r--  1 root root   743 Jul 26 15:10 .travis.yml
            drwxr-xr-x  2 root root  4096 Dec 21 05:56 vars
            -rw-rw-r--  1 root root   598 Jul 26 15:10 .yamllint

            root@docker:/#  molecule test -s centos_7
            ---
            dependency:
              name: galaxy
            driver:
              name: docker
              options:
                D: true
                vv: true
           lint: 'yamllint .
           ...
           ...
           ...
           verifier:
             name: ansible
             playbooks:
           verify: ../resources/tests/verify.yml
   
          CRITICAL Failed to pre-validate.
   
          {'driver': [{'name': ['unallowed value docker']}]}


2) Переходим  в каталог с ролью vector-role и создаем сценарий тестирования по умолчанию при помощи

            root@docker:/#  cd /vector-role
            root@docker:/#  molecule init scenario --driver-name delegated -r vector-role
            INFO     Initializing new scenario default...
            INFO     Initialized scenario in /home/bes/LESSONS/vector-role/molecule/default successfully.

4) Добавьте несколько разных дистрибутивов (centos:8, ubuntu:latest) для инстансов и протестируйте роль, исправьте найденные ошибки, если они есть.
5) Добавьте несколько assert'ов в verify.yml файл для проверки работоспособности vector-role
   (проверка, что конфиг валидный, проверка успешности запуска, etc).
6) Запустите тестирование роли повторно и проверьте, что оно прошло успешно.
7) Добавьте новый тег на коммит с рабочим сценарием в соответствии с семантическим версионированием.
