---
## Домашнее задание к занятию "3. Использование Yandex Cloud"
--
Подготовка к выполнению
Подготовьте в Yandex Cloud три хоста: для clickhouse, для vector и для lighthouse.
Ссылка на репозиторий LightHouse: https://github.com/VKCOM/lighthouse

---
### Основная часть

1) Создаем  в Yandex Cloud   три хоста  clickhouse-01, vector-01  , lighthouse-01 .

       Указываем в атрибута хостов пользователя bes  .  
       В атрибутах хостов в поле  ssh ключа копируеb вставляем public ключ с локального хоста, на котором запускаем ansible.
       подключаемся  по очереди к кажому из удалеённыхм хостов по ssh  
       # ssh -l bes <IP>
       либо копируем  ключ на удалённый хост с помощью команды ssh-copy-id username@IP 
       
2) Создаем  тестовую среду  - файл test.yml.

       # cat test.yml
       ---
         clickhouse:
           hosts:
             clickhouse-01:
               ansible_host: 158.160.14.100
               ansible_connection: ssh
               ansible_user: bes
         vector:
           hosts:
             vector-01:
               ansible_host: 62.84.123.36
               ansible_connection: ssh
               ansible_user: bes 

3) Пишем плей для развёртывания  clickhouse-server и запускаем его на тестовой среде 

       # ansible-playbook -i inventory/test.yml site.yml

       PLAY [Install Clickhouse on hosts] **************************************************************************

       TASK [Gathering Facts] **************************************************************************************
       ok: [clickhouse-01]

       TASK [Get clickhouse distrib] *******************************************************************************
       ok: [clickhouse-01] => (item=clickhouse-client)
       ok: [clickhouse-01] => (item=clickhouse-server)
       ok: [clickhouse-01] => (item=clickhouse-common-static)

       TASK [Install clickhouse packages] **************************************************************************
       ok: [clickhouse-01]

       TASK [Export environment variables for clickhouse] **********************************************************
       ok: [clickhouse-01]

       TASK [Run clickhouse server] ********************************************************************************
       changed: [clickhouse-01]

       TASK [Create database] **************************************************************************************
       changed: [clickhouse-01]
       [WARNING]: Could not match supplied host pattern, ignoring: lighthouse

       PLAY RECAP **************************************************************************************************
       clickhouse-01              : ok=6    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


4) Если всё  прошло успешно входим на сервер и проверяем статус сервера clickhouse
 
       # ssh -l bes <IP адрес clickhouse севера>
       [bes@clickhouse-01 ~]$ sudo systemctl status clickhouse-server
       ● clickhouse-server.service - ClickHouse Server (analytic DBMS for big data)
       Loaded: loaded (/usr/lib/systemd/system/clickhouse-server.service; enabled; vendor preset: disabled)
       Active: active (running) since Sun 2022-12-11 10:11:14 UTC; 2min 22s ago
       ...
       #

5) Проверяем подключение с помощью клиента данной БД

       [bes@clickhouse-01 ~]$ sudo clickhouse-client
       ClickHouse client version 22.9.6.20 (official build).
       Connecting to localhost:9000 as user default.
       Connected to ClickHouse server version 22.9.6 revision 54460.

        Warnings:
       * Linux transparent hugepages are set to "always". Check /sys/kernel/mm/transparent_hugepage/enabled
       * Linux threads max count is too low. Check /proc/sys/kernel/threads-max
       * Maximum number of threads is lower than 30000. There could be problems with handling a lot of simultaneous queries.
        clickhouse-01.ru-central1.internal :

6) Проверяем что БД logs создана: Вставляем  строку записей

        clickhouse-01.ru-central1.internal :)  insert into logs  values ( 0, 'Edward');
        clickhouse-01.ru-central1.internal :)  insert into logs  values ( 1, 'Dima');
        clickhouse-01.ru-central1.internal :)  select * from logs;
        select * from logs;

        SELECT *
        FROM logs

        Query id: 35e1e7dd-da3d-4f70-886d-b3379ba1ffda
        ┌─id─┬─name───┐
        │  0 │ Edward │
        └────┴────────┘
        ┌─id─┬─name─┐
        │  1 │ Dima │
        └────┴──────┘
        2 rows in set. Elapsed: 0.003 sec.

7) Создаем новую роль vector . Для запуска приложения  vector в фоновом создаем исполняемый скрипт vector.sh


8) Создаем  свой собственный inventory файл prod.yml.
       
       # cat prod.yml
         ---
           nginx:
             hosts:
               nginx-01:
                 ansible_host: 51.250.110.236
                 ansible_connection: ssh
                 ansible_user: bes
           lighthouse:
             hosts:
               lighthouse-01:
                 ansible_host: 51.250.110.236
                 ansible_connection: ssh
                 ansible_user: bes
           clickhouse:
             hosts:
               clickhouse-01:
                 ansible_host: 51.250.25.244
                 ansible_connection: ssh
                 ansible_user: bes
           vector:
             hosts:
               vector-01:
                 ansible_host: 51.250.101.212
                 ansible_connection: ssh
                 ansible_user: bes


9) После 216 коммитов добиваемся чтобы плейбук работал без сбоев при запуске  

       root@docker:/# ansible-playbook  -i inventory/prod.yml site.yml

10) Запускаем ansible-lint site.yml ,исправляем ошибки и после этого запускаем  playbook на этом окружении с флагом --check.

       root@docker:/# ansible-playbook  --check  -i inventory/prod.yml site.yml

       root@docker:/# ansible-playbook  -v -i inventory/prod.yml site.yml
       Using /etc/ansible/ansible.cfg as config file

       PLAY [Install NGINX on hosts] **************************************************************************************************************************************************

       TASK [Gathering Facts] *********************************************************************************************************************************************************
       ok: [nginx-01]

       TASK [Export environment variables for NGINX] **********************************************************************************************************************************
       ok: [nginx-01] => {"changed": false, "checksum": "37eaf67d82aad980a32a699084d81aa9f6f2c2bc", "dest": "/etc/profile.d/nginx.sh", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/etc/profile.d/nginx.sh", "secontext": "system_u:object_r:bin_t:s0", "size": 177, "state": "file", "uid": 0}

       TASK [NGINX / Add epel-release repository] *************************************************************************************************************************************
       ok: [nginx-01] => {"changed": false, "msg": "", "rc": 0, "results": ["epel-release-7-11.noarch providing epel-release is already installed"]}

       TASK [NGINX / Install NGINX] ***************************************************************************************************************************************************
       ok: [nginx-01] => {"changed": false, "msg": "", "rc": 0, "results": ["1:nginx-1.20.1-10.el7.x86_64 providing nginx is already installed"]}

       TASK [Insert Default Config] ***************************************************************************************************************************************************
       ok: [nginx-01] => {"changed": false, "checksum": "1968d0139babc939565c6b3a68a6b6248f2740f4", "dest": "/etc/nginx/nginx.conf", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/etc/nginx/nginx.conf", "secontext": "unconfined_u:object_r:httpd_config_t:s0", "size": 1368, "state": "file", "uid": 0}

       PLAY [Install LIGHTHOUSE on hosts] *********************************************************************************************************************************************

       TASK [Gathering Facts] *********************************************************************************************************************************************************
       ok: [lighthouse-01]

       TASK [Set facts for NGINX vars] ************************************************************************************************************************************************
       ok: [lighthouse-01] => {"ansible_facts": {"lighthouse_home": "/usr/share/nginx/html/lighthouse-master"}, "changed": false}

       TASK [Upload .tar.gz file containing binaries from local storage] **************************************************************************************************************
       ok: [lighthouse-01] => {"attempts": 1, "changed": false, "checksum": "e3ae04b746cdbaed579779d53dca68e3e7167b2d", "dest": "/tmp/lighthouse-master.tar.gz", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/tmp/lighthouse-master.tar.gz", "secontext": "unconfined_u:object_r:user_home_t:s0", "size": 1962985, "state": "file", "uid": 0}

       TASK [Extract lighthouse in the installation directory] ************************************************************************************************************************
       changed: [lighthouse-01] => {"changed": true, "dest": "/usr/share/nginx/html", "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "secontext": "system_u:object_r:httpd_sys_content_t:s0", "size": 161, "src": "/tmp/lighthouse-master.tar.gz", "state": "directory", "uid": 0}

       TASK [Add virtual domain in NGINX] *********************************************************************************************************************************************
       ok: [lighthouse-01] => {"changed": false, "checksum": "f24ab32f7d760da198fb03ab71987e52bd6d2ff0", "dest": "/etc/nginx/conf.d/lighthouse-master.conf", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/etc/nginx/conf.d/lighthouse-master.conf", "secontext": "system_u:object_r:httpd_config_t:s0", "size": 424, "state": "file", "uid": 0}

       TASK [Change file ownership, group and permissions for NGINX Directory] ********************************************************************************************************
       ok: [lighthouse-01] => {"changed": false, "gid": 994, "group": "nginx", "mode": "0755", "owner": "nginx", "path": "/usr/share/nginx", "secontext": "system_u:object_r:usr_t:s0", "size": 33, "state": "directory", "uid": 997}

       TASK [Ensure installation dir exists] ******************************************************************************************************************************************
       changed: [lighthouse-01] => {"changed": true, "gid": 0, "group": "root", "mode": "0755", "owner": "root", "path": "/usr/share/nginx/html/lighthouse-master", "secontext": "unconfined_u:object_r:httpd_sys_content_t:s0", "size": 119, "state": "directory", "uid": 0}

       TASK [Export environment variables] ********************************************************************************************************************************************
       ok: [lighthouse-01] => {"changed": false, "checksum": "5b120c15aaa8d411aac579d32b01fc8f2614e41d", "dest": "/etc/profile.d/lighthouse.sh", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/etc/profile.d/lighthouse.sh", "secontext": "system_u:object_r:bin_t:s0", "size": 216, "state": "file", "uid": 0}

       PLAY [Install ClICKHOUSE on hosts] *********************************************************************************************************************************************

       TASK [Gathering Facts] *********************************************************************************************************************************************************
       The authenticity of host '51.250.25.244 (51.250.25.244)' can't be established.
       ECDSA key fingerprint is SHA256:Tdgv5966JMkLctKskMG76da1/W0ZEIFfjWM6AVbB2MA.
       Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
       ok: [clickhouse-01]

       TASK [Get clickhouse distrib] **************************************************************************************************************************************************
       ok: [clickhouse-01] => (item=clickhouse-client) => {"ansible_loop_var": "item", "changed": false, "dest": "./clickhouse-client-22.9.6.20.rpm", "elapsed": 0, "gid": 1000, "group": "bes", "item": "clickhouse-client", "mode": "0644", "msg": "HTTP Error 304: Not Modified", "owner": "bes", "secontext": "unconfined_u:object_r:user_home_t:s0", "size": 88339, "state": "file", "status_code": 304, "uid": 1000, "url": "https://packages.clickhouse.com/rpm/stable/clickhouse-client-22.9.6.20.x86_64.rpm"}
       ok: [clickhouse-01] => (item=clickhouse-server) => {"ansible_loop_var": "item", "changed": false, "dest": "./clickhouse-server-22.9.6.20.rpm", "elapsed": 0, "gid": 1000, "group": "bes", "item": "clickhouse-server", "mode": "0644", "msg": "HTTP Error 304: Not Modified", "owner": "bes", "secontext": "unconfined_u:object_r:user_home_t:s0", "size": 114400, "state": "file", "status_code": 304, "uid": 1000, "url": "https://packages.clickhouse.com/rpm/stable/clickhouse-server-22.9.6.20.x86_64.rpm"}
       ok: [clickhouse-01] => (item=clickhouse-common-static) => {"ansible_loop_var": "item", "changed": false, "dest": "./clickhouse-common-static-22.9.6.20.rpm", "elapsed": 0, "gid": 1000, "group": "bes", "item": "clickhouse-common-static", "mode": "0644", "msg": "HTTP Error 304: Not Modified", "owner": "bes", "secontext": "unconfined_u:object_r:user_home_t:s0", "size": 248746603, "state": "file", "status_code": 304, "uid": 1000, "url": "https://packages.clickhouse.com/rpm/stable/clickhouse-common-static-22.9.6.20.x86_64.rpm"}

       TASK [Install clickhouse packages] *********************************************************************************************************************************************
       ok: [clickhouse-01] => {"attempts": 1, "changed": false, "msg": "", "rc": 0, "results": ["clickhouse-common-static-22.9.6.20-1.x86_64 providing clickhouse-common-static-22.9.6.20.rpm is already installed", "clickhouse-client-22.9.6.20-1.x86_64 providing clickhouse-client-22.9.6.20.rpm is already installed", "clickhouse-server-22.9.6.20-1.x86_64 providing clickhouse-server-22.9.6.20.rpm is already installed"]}

       TASK [Export environment variables for clickhouse] *****************************************************************************************************************************
       ok: [clickhouse-01] => {"changed": false, "checksum": "b7d9359a7864ee5d2a33bfa285d1478a0d651ef8", "dest": "/etc/profile.d/clickhouse.sh", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/etc/profile.d/clickhouse.sh", "secontext": "system_u:object_r:bin_t:s0", "size": 199, "state": "file", "uid": 0}

       TASK [Run clickhouse server] **************************************************************************************************************************************************
       ...
       ...
       ....
       TASK [Create database] *********************************************************************************************************************************************************
       changed: [clickhouse-01] => {"changed": true, "cmd": ["clickhouse-client", "-q", "create table if not exists logs (id int, name String) engine=Log;"], "delta": "0:00:00.125825", "end": "2022-12-16 21:48:01.413206", "failed_when_result": false, "msg": "", "rc": 0, "start": "2022-12-16 21:48:01.287381", "stderr": "", "stderr_lines": [], "stdout": "", "stdout_lines": []}

       PLAY [Install VECTOR on hosts] *************************************************************************************************************************************************

       TASK [Gathering Facts] *********************************************************************************************************************************************************
       The authenticity of host '51.250.101.212 (51.250.101.212)' can't be established.
       ECDSA key fingerprint is SHA256:1IVPX8+gk6wLeu42v5YbQeBMXnR5hilQxWd1qBtJUmU.
       Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
       ok: [vector-01]

       TASK [Export environment variables for Vector] *********************************************************************************************************************************
       ok: [vector-01] => {"changed": false, "checksum": "7b93e6ae2026bc5a99355c81f6a113a6ff7d9573", "dest": "/etc/profile.d/vector.sh", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/etc/profile.d/vector.sh", "secontext": "system_u:object_r:bin_t:s0", "size": 199, "state": "file", "uid": 0}

       TASK [Get Vector installed version] ********************************************************************************************************************************************
       changed: [vector-01] => {"changed": true, "cmd": "$HOME/.vector/bin/vector --version", "delta": "0:00:00.901738", "end": "2022-12-16 21:48:32.031664", "msg": "", "rc": 0, "start": "2022-12-16 21:48:31.129926", "stderr": "", "stderr_lines": [], "stdout": "vector 0.27.0 (x86_64-unknown-linux-musl 2cc0bd4 2022-12-12)", "stdout_lines": ["vector 0.27.0 (x86_64-unknown-linux-musl 2cc0bd4 2022-12-12)"]}

       TASK [Ensure installation dir exists and create if it's not] *******************************************************************************************************************
       ok: [vector-01] => {"changed": false, "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/root/.vector/config", "secontext": "unconfined_u:object_r:admin_home_t:s0", "size": 89, "state": "directory", "uid": 0}

       TASK [Get archive of Vector from remote URL] ***********************************************************************************************************************************
       skipping: [vector-01] => {"changed": false, "skip_reason": "Conditional result was False"}

       TASK [Extract Vector in the installation directory] ****************************************************************************************************************************
       ok: [vector-01] => {"changed": false, "dest": "/tmp", "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "01777", "owner": "root", "secontext": "system_u:object_r:tmp_t:s0", "size": 4096, "src": "/tmp/vector.tar.gz", "state": "directory", "uid": 0}

       TASK [Copy distrib to working catalog] *****************************************************************************************************************************************
       changed: [vector-01] => {"changed": true, "checksum": null, "dest": "/root/.vector/", "gid": 0, "group": "root", "md5sum": null, "mode": "0644", "owner": "root", "secontext": "unconfined_u:object_r:admin_home_t:s0", "size": 74, "src": "/tmp/vector-x86_64-unknown-linux-musl/", "state": "directory", "uid": 0}

       TASK [Copy configuration file  for Vector] *************************************************************************************************************************************
       changed: [vector-01] => {"changed": true, "checksum": "c001afe55e9765116ee662d218d762cd8e3d2f05", "dest": "/root/.vector/config/vector.toml", "gid": 0, "group": "root", "md5sum": "303b44aff106b4fdb650e161e7101cb8", "mode": "0644", "owner": "root", "secontext": "unconfined_u:object_r:admin_home_t:s0", "size": 1295, "src": "/home/bes/.ansible/tmp/ansible-tmp-1671227321.4551013-349525-140800510690403/source", "state": "file", "uid": 0}

       TASK [Copy scriptfile  for Vector] *********************************************************************************************************************************************
       ok: [vector-01] => {"changed": false, "checksum": "a29caa306fb71816a6cb8ce4fa65e3c99c36305e", "dest": "/root/.vector/bin/vector.sh", "gid": 0, "group": "root", "mode": "0750", "owner": "root", "path": "/root/.vector/bin/vector.sh", "secontext": "system_u:object_r:admin_home_t:s0", "size": 104, "state": "file", "uid": 0}

       TASK [Execute Vector in the installation directory] ****************************************************************************************************************************
       changed: [vector-01] => {"changed": true, "cmd": "$HOME/.vector/bin/vector.sh > /dev/null &", "delta": "0:00:00.025314", "end": "2022-12-16 21:48:48.199769", "msg": "", "rc": 0, "start": "2022-12-16 21:48:48.174455", "stderr": "error: The subcommand 'true' wasn't recognized\n\nUsage: vector [OPTIONS] [COMMAND]\n\nFor more information try '--help'", "stderr_lines": ["error: The subcommand 'true' wasn't recognized", "", "Usage: vector [OPTIONS] [COMMAND]", "", "For more information try '--help'"], "stdout": "", "stdout_lines": []}
 
       PLAY RECAP *********************************************************************************************************************************************************************
       clickhouse-01              : ok=6    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
       lighthouse-01              : ok=8    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
       nginx-01                   : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
       vector-01                  : ok=9    changed=4    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0


11) Запускаем  playbook на prod.yml окружении  с флагом --diff. Убеждаемся, что изменения на системе произведены.

        root@docker:/# ansible-playbook --diff -i inventory/prod.yml site.yml

        root@docker:/home/bes/LESSONS/08-ansible-03-yandex/playbook# ansible-playbook --diff -i inventory/prod.yml site.yml

        PLAY [Install NGINX on hosts] **************************************************************************************************************************************************

        TASK [Gathering Facts] *********************************************************************************************************************************************************
        ok: [nginx-01]

        TASK [Export environment variables for NGINX] **********************************************************************************************************************************
        ok: [nginx-01]

        TASK [NGINX / Add epel-release repository] *************************************************************************************************************************************
        ok: [nginx-01]

        TASK [NGINX / Install NGINX] ***************************************************************************************************************************************************
        ok: [nginx-01]

        TASK [Insert Default Config] ***************************************************************************************************************************************************
        ok: [nginx-01]

        PLAY [Install LIGHTHOUSE on hosts] *********************************************************************************************************************************************

        TASK [Gathering Facts] *********************************************************************************************************************************************************
        ok: [lighthouse-01]

        TASK [Set facts for NGINX vars] ************************************************************************************************************************************************
        ok: [lighthouse-01]

        TASK [Upload .tar.gz file containing binaries from local storage] **************************************************************************************************************
        ok: [lighthouse-01]

        TASK [Extract lighthouse in the installation directory] ************************************************************************************************************************
        changed: [lighthouse-01]

        TASK [Add virtual domain in NGINX] *********************************************************************************************************************************************
        ok: [lighthouse-01]

        TASK [Change file ownership, group and permissions for NGINX Directory] ********************************************************************************************************
        ok: [lighthouse-01]

        TASK [Ensure installation dir exists] ******************************************************************************************************************************************
        --- before
        +++ after
        @@ -1,4 +1,4 @@
          {
        -    "mode": "0644",
        +    "mode": "0755",
        "path": "/usr/share/nginx/html/lighthouse-master"
          }

        changed: [lighthouse-01]
 
        TASK [Export environment variables] ********************************************************************************************************************************************
        ok: [lighthouse-01]

        PLAY [Install ClICKHOUSE on hosts] *********************************************************************************************************************************************
 
        TASK [Gathering Facts] *********************************************************************************************************************************************************
        ok: [clickhouse-01]
 
        TASK [Get clickhouse distrib] **************************************************************************************************************************************************
        ok: [clickhouse-01] => (item=clickhouse-client)
        ok: [clickhouse-01] => (item=clickhouse-server)
        ok: [clickhouse-01] => (item=clickhouse-common-static)
 
        TASK [Install clickhouse packages] *********************************************************************************************************************************************
        ok: [clickhouse-01]
 
        TASK [Export environment variables for clickhouse] *****************************************************************************************************************************
        ok: [clickhouse-01]
 
        TASK [Run clickhouse server] ***************************************************************************************************************************************************
        changed: [clickhouse-01]
 
        TASK [Create database] *********************************************************************************************************************************************************
        changed: [clickhouse-01]
 
        PLAY [Install VECTOR on hosts] *************************************************************************************************************************************************
 
        TASK [Gathering Facts] *********************************************************************************************************************************************************
        ok: [vector-01]
 
        TASK [Export environment variables for Vector] *********************************************************************************************************************************
        ok: [vector-01]
 
        TASK [Get Vector installed version] ********************************************************************************************************************************************
        changed: [vector-01]
 
        TASK [Ensure installation dir exists and create if it's not] *******************************************************************************************************************
        ok: [vector-01]
 
        TASK [Get archive of Vector from remote URL] ***********************************************************************************************************************************
        skipping: [vector-01]
 
        TASK [Extract Vector in the installation directory] ****************************************************************************************************************************
        ok: [vector-01]
 
        TASK [Copy distrib to working catalog] *****************************************************************************************************************************************
        changed: [vector-01]
 
        TASK [Copy configuration file  for Vector] *************************************************************************************************************************************
        --- before: $HOME/.vector/config/vector.toml
        +++ after: /home/bes/LESSONS/08-ansible-03-yandex/playbook/templates/vector.toml
        @@ -1,3 +1,4 @@
        +#   Edited By  EDWARD
        #                                    __   __  __
        #                                    \ \ / / / /
        #                                     \ V / / /
        @@ -39,6 +40,6 @@
        # Vector's GraphQL API (disabled by default)
        # Uncomment to try it out with the `vector top` command or
        # in your browser at http://localhost:8686
        -#[api]
        -#enabled = true
        -#address = "127.0.0.1:8686"
        +[api]
        +enabled = true
        +address = "127.0.0.1:8686"
        \ No newline at end of file
 
        changed: [vector-01]
 
        TASK [Copy scriptfile  for Vector] *********************************************************************************************************************************************
        ok: [vector-01]
 
        TASK [Execute Vector in the installation directory] ****************************************************************************************************************************
        changed: [vector-01]
        
        PLAY RECAP *********************************************************************************************************************************************************************
        clickhouse-01              : ok=6    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
        lighthouse-01              : ok=8    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
        nginx-01                   : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
        vector-01                  : ok=9    changed=4    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0



12) Повторно запускаем playbook с флагом --diff и убеждаемся, что playbook идемпотентен:

        root@docker:/# ansible-playbook --diff -i inventory/prod.yml site.yml
        ...
        PLAY RECAP *********************************************************************************************************************************************************************
        clickhouse-01              : ok=6    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
        lighthouse-01              : ok=8    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
        nginx-01                   : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
        vector-01                  : ok=9    changed=4    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0


---     
#### Итоги :  

---- 
Цели плейбука:      

        Плэйбук развертывает три хоста :
        - На первом хосте на платформе YC устанавливает   сервер Clickhouse
        - На втром  хосте на платформе YC устанвоаливает  сервер Vector
        - На третьем хосте на платформе YC устанавливает  сервера  Nginx и Lighthouse

----
Параметры плейбука:

        nginx_user: "nginx"
        nginx_home: "/etc/nginx"
        nginx_home: "/etc/nginx"
        web_root: "/usr/share/nginx/html"
        ------
        lighthouse_version: "7.10.1"
        virtual_domain: "lighthouse-master"
        lighthouse_home: "{{ web-root }}/{{ virtual_domain }}"
        ------
        clickhouse_home: "/etc/clickhouse-server"
        clickhouse_version: "22.9.6.20"
        clickhouse_packages:
          - clickhouse-client
          - clickhouse-server
          - clickhouse-common-static
        ------
        vector_version: "0.26.0"
        vector_home: "$HOME/.vector"
        vector_source: "https://packages.timber.io/vector/nightly/latest/vector-nightly-x86_64-unknown-linux-musl.tar.gz"

----
Теги плейбука:

        nginx 
        lighthouse
        clickhouse
        vector 


