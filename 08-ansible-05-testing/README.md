### Molecule
----

1) Убедимся предварительно что необходимый драйвер  docker пакета-фрейморка molecule установлен.
            root@docker:/#   pip install 'molecule[docker]'
            ...
            ERROR: docker 6.0.1 has requirement urllib3>=1.26.0, but you'll have urllib3 1.25.8 which is incompatible.
            ERROR: molecule-docker 2.1.0 has requirement molecule>=4.0.0, but you'll have molecule 3.5.2 which is incompatible.
            Installing collected packages: websocket-client, docker, molecule-docker
            Successfully installed docker-6.0.1 molecule-docker-2.1.0 websocket-client-1.4.2


3) Запустите molecule test -s centos_7 внутри корневой директории clickhouse-role ( Ошибка) , посмотрите на вывод команды.

            Проверяем версию молекулы
            root@docker:/# molecule --version
            molecule 3.5.2 using python 3.8
            ansible:2.13.6
            delegated:3.5.2 from molecule


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


3) Инициализируем новую  пустую роль со сценарием тестирования default с выбранным драйвером
    c помощью команды  "molecule init role vector-role --driver-name docker"

           root@docker:/#  molecule init role --driver-name docker vector-role
  
    Или переходим  в каталог с уже существующей ролью vector-role, чтобы создать сценарий тестирования по умолчанию

            root@docker:/#  cd /vector-role
            root@docker:/#  molecule init scenario --driver-name docker
            INFO     Initializing new scenario default...
            INFO     Initialized scenario in /home/bes/LESSONS/vector-role/molecule/default successfully.

4) Добавляем несколько разных дистрибутивов (centos:8, ubuntu:latest) для инстансов и протестируйте роль, исправьте найденные ошибки, если они есть.
          
            root@docker:/#  cat  /vector-role/molecule/default/molecule.yml
            ---
            dependency:
              name: galaxy
            driver:
              name: docker
            platforms:
              - name: Centos8
                image: docker.io/pycontribs/centos:8
                pre_build_image: true
              - name: Centos7
                image: docker.io/pycontribs/centos:7
                pre_build_image: true

            provisioner:
              name: ansible
            verifier:
              name: ansible

5) Добавяем несколько assert'ов в verify.yml файл для проверки работоспособности vector-role
   (проверка, что конфиг валидный, проверка успешности запуска, etc).
6) Запустите тестирование роли повторно и проверьте, что оно прошло успешно.
7) Добавьте новый тег на коммит с рабочим сценарием в соответствии с семантическим версионированием.
