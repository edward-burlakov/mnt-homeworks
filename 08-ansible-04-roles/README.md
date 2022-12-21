--
## Домашнее задание к занятию "8.4. Работа с roles"

----
### Создайте два пустых публичных репозитория в любом своём проекте: vector-role и lighthouse-role.
-Добавьте публичную часть своего ключа к своему профилю в github.
-Основная часть
-Наша основная цель - разбить наш playbook на отдельные roles. 
-Задачи: 
  - сделать roles для clickhouse, vector и lighthouse 
  - написать playbook для использования этих ролей. 
  - Ожидаемый результат: существуют три ваших репозитория: два с roles и один с playbook.

---
### 1) Копируем  старый проект "LESSON_8.3" в проект "LESSON_8.4" 
###    Создаем в новой версии в каталоге playbook файл requirements.yml и заполняем его следующим содержимым:

       root@docker:/#   cd playbook
       root@docker:/#   touch  requirements.yml 
       root@docker:/#   cat playbook /requirements.yml
         ---
           - name: ansible-clickhouse 
             src: git@github.com:AlexeySetevoi/ansible-clickhouse.git
             scm: git
             version: "1.11.0"

---
### 2) На management хосте  с установленным Ansible cоздаем  публичный репозиторий vector-role локально и
###   публикуем его на Github с именем vector-role
<https://github.com/edward-burlakov/vector-role.git>
         
         root@docker:/#  git init
         root@docker:/#  git branch -M main
         root@docker:/#  git remote add origin https://github.com/edward-burlakov/vector-role .git
         root@docker:/#  git push -u origin main
--- 
### 3) При помощи ansible-galaxy внутри репозитория создаём новую структуру каталогов с ролью vector-role  из шаблона  по умолчанию

         root@docker:/# ansible-galaxy role init vector-role
---
### 4) На основе tasks из старого playbook заполняем  новую role. Из основного  проекта "LESSON_8.4" переносим все таски касающиеся роли vector .
###        Также разносим переменные  из старых каталогов group_vars в  каталогами vars и default. 
###         В каталог  vars помещаем те переменные, которые НЕ сможет менять пользователь опубликованного нами плейбука.

---
### 5) Переносим нужные шаблоны конфигов  из каталога templates основного проекта "LESSON_8.4"  в  папку templates.

---
###  6) Публикуем изменения проекта vector-role на GITHUB . 

---
### 7)  На management хосте  с установленным Ansible  создаём публичный репозиторий для роли  lighthouse-role . 
###     И публикуем его  в личном кабинете GITHUB с именем vector-role <https://github.com/edward-burlakov/lighthouse-role.git>  

          root@docker:/#  git init
          root@docker:/#  git branch -M main
          root@docker:/#  git remote add origin https://github.com/edward-burlakov/lighthouse-role .git
          root@docker:/#  git push -u origin main
          
--- 
### 8)   Развертываем пустой каталог  lighthouse  при помощи ansible-galaxy из шаблона  по умолчанию
       
         root@docker:/#  ansible-galaxy role init lighthouse-role
---
### 9)  Повторяем шаги 4)-5)-6) для  проекта lighthouse , учитывая, что одна роль должна настраивать один продукт. 

---
### 10) Описываем в README.md  основного проекта обе роли и их параметры.

---
### 11) Добавляем в playbook основного проекта в файл requirements.yml  обе roles, опубликованные  в сторонних репозиториях  .

         root@docker:/# cat playbook /requirements.yml
         ---
           - name: ansible-clickhouse 
             src: git@github.com:AlexeySetevoi/ansible-clickhouse.git
             scm: git
             version: "1.13"
           - name: ansible-vector-role
             src: git@github.com/edward-burlakov/vector-role.git
             scm: git
             version: "1.0.2"
           - name ansible-lighthouse-role           
             src: git@github.com/edward-burlakov/lighthouse-role.git
             scm: git
             version: "1.0.2"

---
### 12) Проставляем тэги , в обоих проектах , используя семантическую нумерацию. 

           Добавляем  tag "1.0.X"  на итоговые  коммиты  обоих репозиториев 
           для версионирования  опубликованных  ролей и  публикации их релизов в виде архива .

---
### 13) Выкладываем все roles в репозитории. 

           # cat /playbook/site.yml
           ---
           - name: Install lighthouse role
             hosts: lighthouse
             roles:
               - ansible-lighthouse-role 
           - name Install vector role
             hosts: vector
             roles:
               - ansible-vector-role
           - name Install clickhouse role
             hosts: clickhouse
             roles:
               - ansible-clickhouse

---
### 14) Устанавливаем необходимые  роли перечисленные в файле requirements.yml  на management host из репозиториев: 
### По умолчанию роли будут скачаны в каталог /etc/ansible/roles, поскольку этот путь мы указали в файле /etc/ansible/ansible.cfg
### Для принудительной переустановки добавляем ключ --force

          root@docker:/#  ansible-galaxy install -r requirements.yml --force
          Starting galaxy role install process
          - extracting ansible-clickhouse to /etc/ansible/roles/ansible-clickhouse
          - ansible-clickhouse (1.13) was installed successfully
          - extracting vector-role to /etc/ansible/roles/vector-role
          - vector-role (1.0.2) was installed successfully
          - extracting lighthouse-role to /etc/ansible/roles/lighthouse-role
          - lighthouse-role (1.0.2) was installed successfully


---
### 15) Запускаем плейбук и добиваемся работоспособности проекта.  
###     Перерабатываем playbook на использование roles. 
###     Не забываем про зависимости lighthouse и возможности совмещения roles с tasks.

    root@docker:/home/bes/LESSONS/08-ansible-04-roles/playbook# ansible-playbook -v -i inventory/prod.yml site.yml
    Using /etc/ansible/ansible.cfg as config file

    PLAY [Install lighthouse role] **************************************************************************************************************************************

    TASK [Gathering Facts] **********************************************************************************************************************************************
    ok: [lighthouse-01]

    TASK [lighthouse-role : NGINX /  Export environment variables for NGINX] ********************************************************************************************
    ok: [lighthouse-01] => {"changed": false, "checksum": "37eaf67d82aad980a32a699084d81aa9f6f2c2bc", "dest": "/etc/profile.d/nginx.sh", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/etc/profile.d/nginx.sh", "secontext": "system_u:object_r:bin_t:s0", "size": 177, "state": "file", "uid": 0}

    TASK [lighthouse-role : NGINX /  Add epel-release repository] *******************************************************************************************************
    ok: [lighthouse-01] => {"changed": false, "msg": "", "rc": 0, "results": ["epel-release-7-11.noarch providing epel-release is already installed"]}

    TASK [lighthouse-role : NGINX /  Install NGINX] *********************************************************************************************************************
    ok: [lighthouse-01] => {"changed": false, "msg": "", "rc": 0, "results": ["1:nginx-1.20.1-10.el7.x86_64 providing nginx is already installed"]}

    TASK [lighthouse-role : NGINX /  Insert Default Config] *************************************************************************************************************
    ok: [lighthouse-01] => {"changed": false, "checksum": "57bfc7a00ab23215437f5d3b9d08791cc430faf0", "dest": "/etc/nginx/nginx.conf", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/etc/nginx/nginx.conf", "secontext": "unconfined_u:object_r:httpd_config_t:s0", "size": 1785, "state": "file", "uid": 0}

    TASK [lighthouse-role : Set facts for NGINX vars] *******************************************************************************************************************
    ok: [lighthouse-01] => {"ansible_facts": {"lighthouse_home": "/usr/share/nginx/html/lighthouse-master"}, "changed": false}

    TASK [lighthouse-role : Upload .tar.gz file containing binaries from local storage] *********************************************************************************
    ok: [lighthouse-01] => {"attempts": 1, "changed": false, "checksum": "e3ae04b746cdbaed579779d53dca68e3e7167b2d", "dest": "/tmp/lighthouse-master.tar.gz", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/tmp/lighthouse-master.tar.gz", "secontext": "unconfined_u:object_r:user_home_t:s0", "size": 1962985, "state": "file", "uid": 0}

    TASK [lighthouse-role : Extract lighthouse in the installation directory] *******************************************************************************************
    changed: [lighthouse-01] => {"changed": true, "dest": "/usr/share/nginx/html", "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "secontext": "system_u:object_r:httpd_sys_content_t:s0", "size": 161, "src": "/tmp/lighthouse-master.tar.gz", "state": "directory", "uid": 0}

    TASK [lighthouse-role : Add virtual domain in NGINX] ****************************************************************************************************************
    ok: [lighthouse-01] => {"changed": false, "checksum": "f24ab32f7d760da198fb03ab71987e52bd6d2ff0", "dest": "/etc/nginx/conf.d/lighthouse-master.conf", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/etc/nginx/conf.d/lighthouse-master.conf", "secontext": "system_u:object_r:httpd_config_t:s0", "size": 424, "state": "file", "uid": 0}

    TASK [lighthouse-role : Change file ownership, group and permissions for NGINX Directory] ***************************************************************************
    ok: [lighthouse-01] => {"changed": false, "gid": 994, "group": "nginx", "mode": "0755", "owner": "nginx", "path": "/usr/share/nginx", "secontext": "system_u:object_r:usr_t:s0", "size": 33, "state": "directory", "uid": 997}

    TASK [lighthouse-role : Ensure installation dir exists] *************************************************************************************************************
    changed: [lighthouse-01] => {"changed": true, "gid": 0, "group": "root", "mode": "0755", "owner": "root", "path": "/usr/share/nginx/html/lighthouse-master", "secontext": "unconfined_u:object_r:httpd_sys_content_t:s0", "size": 119, "state": "directory", "uid": 0}

    TASK [lighthouse-role : Export environment variables] ***************************************************************************************************************
    ok: [lighthouse-01] => {"changed": false, "checksum": "5b120c15aaa8d411aac579d32b01fc8f2614e41d", "dest": "/etc/profile.d/lighthouse.sh", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/etc/profile.d/lighthouse.sh", "secontext": "system_u:object_r:bin_t:s0", "size": 216, "state": "file", "uid": 0}

    PLAY [Install vector role] ******************************************************************************************************************************************

    TASK [Gathering Facts] **********************************************************************************************************************************************
    ok: [vector-01]

    TASK [vector-role : Export environment variables for Vector] ********************************************************************************************************
    ok: [vector-01] => {"changed": false, "checksum": "7b93e6ae2026bc5a99355c81f6a113a6ff7d9573", "dest": "/etc/profile.d/vector.sh", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/etc/profile.d/vector.sh", "secontext": "system_u:object_r:bin_t:s0", "size": 199, "state": "file", "uid": 0}
 
    TASK [vector-role : Get Vector installed version] *******************************************************************************************************************
    changed: [vector-01] => {"changed": true, "cmd": "$HOME/.vector/bin/vector --version", "delta": "0:00:00.009698", "end": "2022-12-20 23:00:42.902298", "msg": "", "rc": 0, "start": "2022-12-20 23:00:42.892600", "stderr": "", "stderr_lines": [], "stdout": "vector 0.27.0 (x86_64-unknown-linux-musl 1c0716f 2022-12-20)", "stdout_lines": ["vector 0.27.0 (x86_64-unknown-linux-musl 1c0716f 2022-12-20)"]}

    TASK [vector-role : Ensure installation dir exists and create if its not] *******************************************************************************************
    ok: [vector-01] => {"changed": false, "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/root/.vector/config", "secontext": "unconfined_u:object_r:admin_home_t:s0", "size": 89, "state": "directory", "uid": 0}

    TASK [vector-role : Get archive of Vector from remote URL] **********************************************************************************************************
    ok: [vector-01] => {"changed": false, "checksum_dest": "e449c2690290e83afffb078938252f5c5b0602e9", "checksum_src": "e449c2690290e83afffb078938252f5c5b0602e9", "dest": "/tmp/vector.tar.gz", "elapsed": 2, "gid": 0, "group": "root", "md5sum": "a7b57bf6dc5cb0012858ec94208bc53b", "mode": "0755", "msg": "OK (40583423 bytes)", "owner": "root", "secontext": "unconfined_u:object_r:user_home_t:s0", "size": 40583423, "src": "/home/bes/.ansible/tmp/ansible-tmp-1671577244.631355-505963-224961761013274/tmpQw5WzD", "state": "file", "status_code": 200, "uid": 0, "url": "https://packages.timber.io/vector/nightly/latest/vector-nightly-x86_64-unknown-linux-musl.tar.gz"}

    TASK [vector-role : Extract Vector in the installation directory] ***************************************************************************************************
    ok: [vector-01] => {"changed": false, "dest": "/tmp", "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "01777", "owner": "root", "secontext": "system_u:object_r:tmp_t:s0", "size": 4096, "src": "/tmp/vector.tar.gz", "state": "directory", "uid": 0}

    TASK [vector-role : Copy distrib to working catalog] ****************************************************************************************************************
    ok: [vector-01] => {"changed": false, "checksum": null, "dest": "/home/bes/.vector/", "gid": 1000, "group": "bes", "md5sum": null, "mode": "0750", "owner": "bes", "secontext": "unconfined_u:object_r:user_home_t:s0", "size": 74, "src": "/tmp/vector-x86_64-unknown-linux-musl/", "state": "directory", "uid": 1000}

    TASK [vector-role : Copy configuration file  for Vector] ************************************************************************************************************
    ok: [vector-01] => {"changed": false, "checksum": "c001afe55e9765116ee662d218d762cd8e3d2f05", "dest": "/root/.vector/config/vector.toml", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/root/.vector/config/vector.toml", "secontext": "unconfined_u:object_r:admin_home_t:s0", "size": 1295, "state": "file", "uid": 0}

    TASK [vector-role : Copy scriptfile  for Vector] ********************************************************************************************************************
    ok: [vector-01] => {"changed": false, "checksum": "a29caa306fb71816a6cb8ce4fa65e3c99c36305e", "dest": "/root/.vector/bin/vector.sh", "gid": 0, "group": "root", "mode": "0750", "owner": "root", "path": "/root/.vector/bin/vector.sh", "secontext": "system_u:object_r:admin_home_t:s0", "size": 104, "state": "file", "uid": 0}

    TASK [vector-role : Execute Vector in the installation directory] ***************************************************************************************************
    changed: [vector-01] => {"changed": true, "cmd": "$HOME/.vector/bin/vector.sh > /dev/null &", "delta": "0:00:00.004224", "end": "2022-12-20 23:01:01.229718", "msg": "", "rc": 0, "start": "2022-12-20 23:01:01.225494", "stderr": "/bin/bash: /home/bes/.vector/bin/vector.sh: No such file or directory", "stderr_lines": ["/bin/bash: /home/bes/.vector/bin/vector.sh: No such file or directory"], "stdout": "", "stdout_lines": []}

    PLAY [Install clickhouse role] **************************************************************************************************************************************

    TASK [Gathering Facts] **********************************************************************************************************************************************
    ok: [clickhouse-01]

    TASK [ansible-clickhouse : Include OS Family Specific Variables] ****************************************************************************************************
    ok: [clickhouse-01] => {"ansible_facts": {"clickhouse_repo": "https://packages.clickhouse.com/rpm/stable/", "clickhouse_supported": true}, "ansible_included_var_files": ["/etc/ansible/roles/ansible-clickhouse/vars/redhat.yml"], "changed": false}

    TASK [ansible-clickhouse : include_tasks] ***************************************************************************************************************************
    included: /etc/ansible/roles/ansible-clickhouse/tasks/precheck.yml for clickhouse-01

    TASK [ansible-clickhouse : Requirements check | Checking sse4_2 support] ********************************************************************************************
    ok: [clickhouse-01] => {"changed": false, "cmd": ["grep", "-q", "sse4_2", "/proc/cpuinfo"], "delta": "0:00:00.003413", "end": "2022-12-20 23:01:06.322131", "msg": "", "rc": 0, "start": "2022-12-20 23:01:06.318718", "stderr": "", "stderr_lines": [], "stdout": "", "stdout_lines": []}

    TASK [ansible-clickhouse : Requirements check | Not supported distribution && release] ******************************************************************************
    skipping: [clickhouse-01] => {"changed": false, "skip_reason": "Conditional result was False"}

    TASK [ansible-clickhouse : include_tasks] ***************************************************************************************************************************
    included: /etc/ansible/roles/ansible-clickhouse/tasks/params.yml for clickhouse-01

    TASK [ansible-clickhouse : Set clickhouse_service_enable] ***********************************************************************************************************
    ok: [clickhouse-01] => {"ansible_facts": {"clickhouse_service_enable": true}, "changed": false}

    TASK [ansible-clickhouse : Set clickhouse_service_ensure] ***********************************************************************************************************
    ok: [clickhouse-01] => {"ansible_facts": {"clickhouse_service_ensure": "started"}, "changed": false}

    TASK [ansible-clickhouse : include_tasks] ***************************************************************************************************************************
    included: /etc/ansible/roles/ansible-clickhouse/tasks/install/yum.yml for clickhouse-01

    TASK [ansible-clickhouse : Install by YUM | Ensure clickhouse repo installed] ***************************************************************************************
    ok: [clickhouse-01] => {"changed": false, "repo": "clickhouse", "state": "present"}

    TASK [ansible-clickhouse : Install by YUM | Ensure clickhouse package installed (latest)] ***************************************************************************
    skipping: [clickhouse-01] => {"changed": false, "skip_reason": "Conditional result was False"}
 
    TASK [ansible-clickhouse : Install by YUM | Ensure clickhouse package installed (version 22.9.6.20)] ****************************************************************
    ok: [clickhouse-01] => {"changed": false, "msg": "", "rc": 0, "results": ["clickhouse-client-22.9.6.20-1.x86_64 providing clickhouse-client-22.9.6.20 is already installed", "clickhouse-server-22.9.6.20-1.x86_64 providing clickhouse-server-22.9.6.20 is already installed", "clickhouse-common-static-22.9.6.20-1.x86_64 providing clickhouse-common-static-22.9.6.20 is already installed"]}

    TASK [ansible-clickhouse : include_tasks] ***************************************************************************************************************************
    included: /etc/ansible/roles/ansible-clickhouse/tasks/configure/sys.yml for clickhouse-01

    TASK [ansible-clickhouse : Check clickhouse config, data and logs] **************************************************************************************************
    ok: [clickhouse-01] => (item=/var/log/clickhouse-server) => {"ansible_loop_var": "item", "changed": false, "gid": 994, "group": "clickhouse", "item": "/var/log/clickhouse-server", "mode": "0770", "owner": "clickhouse", "path": "/var/log/clickhouse-server", "secontext": "unconfined_u:object_r:var_log_t:s0", "size": 68, "state": "directory", "uid": 997}
    ok: [clickhouse-01] => (item=/etc/clickhouse-server) => {"ansible_loop_var": "item", "changed": false, "gid": 994, "group": "clickhouse", "item": "/etc/clickhouse-server", "mode": "0770", "owner": "clickhouse", "path": "/etc/clickhouse-server", "secontext": "system_u:object_r:etc_t:s0", "size": 72, "state": "directory", "uid": 997}
    ok: [clickhouse-01] => (item=/var/lib/clickhouse/tmp/) => {"ansible_loop_var": "item", "changed": false, "gid": 994, "group": "clickhouse", "item": "/var/lib/clickhouse/tmp/", "mode": "0770", "owner": "clickhouse", "path": "/var/lib/clickhouse/tmp/", "secontext": "system_u:object_r:var_lib_t:s0", "size": 6, "state": "directory", "uid": 997}
    ok: [clickhouse-01] => (item=/var/lib/clickhouse/) => {"ansible_loop_var": "item", "changed": false, "gid": 994, "group": "clickhouse", "item": "/var/lib/clickhouse/", "mode": "0770", "owner": "clickhouse", "path": "/var/lib/clickhouse/", "secontext": "unconfined_u:object_r:var_lib_t:s0", "size": 267, "state": "directory", "uid": 997}

    TASK [ansible-clickhouse : Config | Create config.d folder] *********************************************************************************************************
    ok: [clickhouse-01] => {"changed": false, "gid": 994, "group": "clickhouse", "mode": "0770", "owner": "clickhouse", "path": "/etc/clickhouse-server/config.d", "secontext": "unconfined_u:object_r:etc_t:s0", "size": 24, "state": "directory", "uid": 997}

    TASK [ansible-clickhouse : Config | Create users.d folder] **********************************************************************************************************
    ok: [clickhouse-01] => {"changed": false, "gid": 994, "group": "clickhouse", "mode": "0770", "owner": "clickhouse", "path": "/etc/clickhouse-server/users.d", "secontext": "unconfined_u:object_r:etc_t:s0", "size": 23, "state": "directory", "uid": 997}

    TASK [ansible-clickhouse : Config | Generate system config] *********************************************************************************************************
    ok: [clickhouse-01] => {"changed": false, "checksum": "2fce011fc61d95ef135da61c8bfc9aa6764c203c", "dest": "/etc/clickhouse-server/config.d/config.xml", "gid": 994, "group": "clickhouse", "mode": "0660", "owner": "clickhouse", "path": "/etc/clickhouse-server/config.d/config.xml", "secontext": "system_u:object_r:etc_t:s0", "size": 16515, "state": "file", "uid": 997}

    TASK [ansible-clickhouse : Config | Generate users config] **********************************************************************************************************
    ok: [clickhouse-01] => {"changed": false, "checksum": "d63ce9d45d51fd619a0286747f7fa0cdc227d8a5", "dest": "/etc/clickhouse-server/users.d/users.xml", "gid": 994, "group": "clickhouse", "mode": "0660", "owner": "clickhouse", "path": "/etc/clickhouse-server/users.d/users.xml", "secontext": "system_u:object_r:etc_t:s0", "size": 1860, "state": "file", "uid": 997}

    TASK [ansible-clickhouse : Config | Generate remote_servers config] *************************************************************************************************
    skipping: [clickhouse-01] => {"changed": false, "skip_reason": "Conditional result was False"}

    TASK [ansible-clickhouse : Config | Generate macros config] *********************************************************************************************************
    skipping: [clickhouse-01] => {"changed": false, "skip_reason": "Conditional result was False"}

    TASK [ansible-clickhouse : Config | Generate zookeeper servers config] **********************************************************************************************
    skipping: [clickhouse-01] => {"changed": false, "skip_reason": "Conditional result was False"}

    TASK [ansible-clickhouse : Config | Fix interserver_http_port and intersever_https_port collision] ******************************************************************
    skipping: [clickhouse-01] => {"changed": false, "skip_reason": "Conditional result was False"}

    TASK [ansible-clickhouse : Notify Handlers Now] *********************************************************************************************************************

    TASK [ansible-clickhouse : include_tasks] ***************************************************************************************************************************
    included: /etc/ansible/roles/ansible-clickhouse/tasks/service.yml for clickhouse-01

    TASK [ansible-clickhouse : Ensure clickhouse-server.service is enabled: True and state: started] ********************************************************************
    ok: [clickhouse-01] => {"changed": false, "enabled": true, "name": "clickhouse-server.service", "state": "started", "status": {"ActiveEnterTimestamp": "Tue 2022-12-20 22:57:57 UTC", "ActiveEnterTimestampMonotonic": "8379583569", "ActiveExitTimestamp": "Tue 2022-12-20 22:57:53 UTC", "ActiveExitTimestampMonotonic": "8376300772", "ActiveState": "active", "After": "system.slice network-online.target time-sync.target systemd-journald.socket basic.target", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Tue 2022-12-20 22:57:57 UTC", "AssertTimestampMonotonic": "8379583031", "Before": "multi-user.target shutdown.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "8410112", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Tue 2022-12-20 22:57:57 UTC", "ConditionTimestampMonotonic": "8379583031", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/clickhouse-server.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "ClickHouse Server (analytic DBMS for big data)", "DevicePolicy": "auto", "EnvironmentFile": "/etc/default/clickhouse (ignore_errors=yes)", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "3188", "ExecMainStartTimestamp": "Tue 2022-12-20 22:57:57 UTC", "ExecMainStartTimestampMonotonic": "8379583522", "ExecMainStatus": "0", "ExecStart": "{ path=/usr/bin/clickhouse-server ; argv[]=/usr/bin/clickhouse-server --config=/etc/clickhouse-server/config.xml --pid-file=/run/clickhouse-server/clickhouse-server.pid ; ignore_errors=no ; start_time=[Tue 2022-12-20 22:57:57 UTC] ; stop_time=[n/a] ; pid=3188 ; code=(null) ; status=0/0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/clickhouse-server.service", "Group": "clickhouse", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "clickhouse-server.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Tue 2022-12-20 22:57:57 UTC", "InactiveEnterTimestampMonotonic": "8379581275", "InactiveExitTimestamp": "Tue 2022-12-20 22:57:57 UTC", "InactiveExitTimestampMonotonic": "8379583569", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "500000", "LimitNPROC": "14955", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "14955", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "3188", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "clickhouse-server.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "system.slice basic.target network-online.target", "Restart": "always", "RestartUSec": "30s", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectory": "clickhouse-server", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "simple", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "User": "clickhouse", "WantedBy": "multi-user.target", "Wants": "time-sync.target", "WatchdogTimestamp": "Tue 2022-12-20 22:57:57 UTC", "WatchdogTimestampMonotonic": "8379583554", "WatchdogUSec": "0"}}

    TASK [ansible-clickhouse : Wait for Clickhouse Server to Become Ready] **********************************************************************************************
    ok: [clickhouse-01] => {"changed": false, "elapsed": 5, "match_groupdict": {}, "match_groups": [], "path": null, "port": 9000, "search_regex": null, "state": "started"}

    TASK [ansible-clickhouse : include_tasks] ***************************************************************************************************************************
    included: /etc/ansible/roles/ansible-clickhouse/tasks/configure/db.yml for clickhouse-01

    TASK [ansible-clickhouse : Set ClickHose Connection String] *********************************************************************************************************
    ok: [clickhouse-01] => {"ansible_facts": {"clickhouse_connection_string": "clickhouse-client -h 127.0.0.1 --port 9000"}, "changed": false}

    TASK [ansible-clickhouse : Gather list of existing databases] *******************************************************************************************************
    ok: [clickhouse-01] => {"changed": false, "cmd": ["clickhouse-client", "-h", "127.0.0.1", "--port", "9000", "-q", "show databases"], "delta": "0:00:00.040864", "end": "2022-12-20 23:01:33.469143", "msg": "", "rc": 0, "start": "2022-12-20 23:01:33.428279", "stderr": "", "stderr_lines": [], "stdout": "INFORMATION_SCHEMA\ndefault\ninformation_schema\nlogs\nsystem", "stdout_lines": ["INFORMATION_SCHEMA", "default", "information_schema", "logs", "system"]}

    TASK [ansible-clickhouse : Config | Delete database config] *********************************************************************************************************

    TASK [ansible-clickhouse : Config | Create database config] *********************************************************************************************************

    TASK [ansible-clickhouse : include_tasks] ***************************************************************************************************************************
    included: /etc/ansible/roles/ansible-clickhouse/tasks/configure/dict.yml for clickhouse-01

    TASK [ansible-clickhouse : Config | Generate dictionary config] *****************************************************************************************************
    skipping: [clickhouse-01] => {"changed": false, "skip_reason": "Conditional result was False"}

    TASK [ansible-clickhouse : include_tasks] ***************************************************************************************************************************
    skipping: [clickhouse-01] => {"changed": false, "skip_reason": "Conditional result was False"}

    PLAY RECAP **********************************************************************************************************************************************************
    clickhouse-01              : ok=23   changed=0    unreachable=0    failed=0    skipped=10   rescued=0    ignored=0
    lighthouse-01              : ok=12   changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    vector-01                  : ok=10   changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


### 16) Выкладываем итоговый playbook в репозиторий.

Ниже- ссылки на оба репозитория с roles и одна ссылку на репозиторий с playbook.

<https://github.com/edward-burlakov/lighthouse-role.git>
<https://github.com/edward-burlakov/vector-role.git>
<https://github.com/edward-burlakov/mnt-homeworks/tree/master/08-ansible-04-roles>





