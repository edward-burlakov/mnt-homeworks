---
## Домашнее задание к занятию "3. Использование Yandex Cloud"
--
Подготовка к выполнению
Подготовьте в Yandex Cloud три хоста: для clickhouse, для vector и для lighthouse.
Ссылка на репозиторий LightHouse: https://github.com/VKCOM/lighthouse

---
## Основная часть
1) Создаем  в YC  три хоста  clickhouse-01, vector-01  , lighthouse-01 .

       Указываем в атрибута хостов пользователя bes  .  
       В атрибутах хостов в поле  ssh ключа копируеb вставляем public ключ с локального хоста, на котором запускаем ansible.
       подключаемся к удаленным хостам по ssh  , либо копируем  ключ на удалённый хост с помощью команды ssh-copy-id username@IP 
       # ssh -l bes <IP>

2) Устанавливаем пакет c ролью clickhouse  из  https://github.com/AlexeySetevoi/ansible-clickhouse

       - В корне каталоге проекта создаем файл requirements.yml
          # cat requirements.yml
            - name ansible-clickhouse
              src: git@github.com:AlexeySetevoi/ansible-clickhouse.git
              scm: git
              version: 1.11.1
       - Запускаем установку роли : 
         # ansible-galaxy install -p roles -r requirements.yml
       - Файл настроек по умолчанию находится в каталоге  /roles  ->  /roles/ansible-clickhouse/defaults/main.yml 

3) Запускаем тестовый PLAY для проверки развертывания clickhouse-server

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

       PLAY [Install lighthouse on hosts] **************************************************************************
       skipping: no hosts matched

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




           
 
Допишите playbook: нужно сделать ещё один play, который устанавливает и настраивает lighthouse.
При создании tasks рекомендую использовать модули: get_url, template, yum, apt.
Tasks должны: скачать статику lighthouse, установить nginx или любой другой webserver, настроить его конфиг для открытия lighthouse, запустить webserver.
Приготовьте свой собственный inventory файл prod.yml.
Запустите ansible-lint site.yml и исправьте ошибки, если они есть.
Попробуйте запустить playbook на этом окружении с флагом --check.

root@docker:/home/bes/LESSONS/08-ansible-03-yandex/playbook# ansible-playbook  --check  -i inventory/prod.yml site.yml

PLAY [Install NGINX on hosts] ***************************************************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************************************
ok: [nginx-01]

TASK [Export environment variables for NGINX] ***********************************************************************************************************************
ok: [nginx-01]

TASK [NGINX / Add epel-release repository] **************************************************************************************************************************
ok: [nginx-01]

TASK [NGINX / Install NGINX] ****************************************************************************************************************************************
ok: [nginx-01]

TASK [Insert Default Index Page] ************************************************************************************************************************************
ok: [nginx-01]

PLAY [Install LIGHTHOUSE on hosts] **********************************************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************************************
ok: [lighthouse-01]

TASK [Set facts for NGINX vars] *************************************************************************************************************************************
ok: [lighthouse-01]

TASK [Upload .tar.gz file containing binaries from local storage] ***************************************************************************************************
ok: [lighthouse-01]

TASK [Add virtual domain in NGINX] **********************************************************************************************************************************
changed: [lighthouse-01]

TASK [Ensure installation dir exists] *******************************************************************************************************************************
ok: [lighthouse-01]

TASK [Extract lighthouse in the installation directory] *************************************************************************************************************
skipping: [lighthouse-01]

TASK [Export environment variables] *********************************************************************************************************************************
ok: [lighthouse-01]

RUNNING HANDLER [Reload-nginx] **************************************************************************************************************************************
changed: [lighthouse-01]

PLAY [Install ClICKHOUSE on hosts] **********************************************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Get clickhouse distrib] ***************************************************************************************************************************************
ok: [clickhouse-01] => (item=clickhouse-client)
ok: [clickhouse-01] => (item=clickhouse-server)
ok: [clickhouse-01] => (item=clickhouse-common-static)

TASK [Install clickhouse packages] **********************************************************************************************************************************
ok: [clickhouse-01]

TASK [Export environment variables for clickhouse] ******************************************************************************************************************
ok: [clickhouse-01]

TASK [Run clickhouse server] ****************************************************************************************************************************************
changed: [clickhouse-01]

TASK [Create database] **********************************************************************************************************************************************
skipping: [clickhouse-01]

PLAY [Install VECTOR on hosts] **************************************************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************************************
ok: [vector-01]

TASK [Export environment variables for Vector] **********************************************************************************************************************
ok: [vector-01]

TASK [Get Vector installed version] *********************************************************************************************************************************
skipping: [vector-01]

TASK [Ensure installation dir exists and create if it's not] ********************************************************************************************************
ok: [vector-01]

TASK [Get archive of Vector from remote URL] ************************************************************************************************************************
skipping: [vector-01]

TASK [Extract Vector in the installation directory] *****************************************************************************************************************
skipping: [vector-01]

TASK [Copy distrib to working catalog] ******************************************************************************************************************************
changed: [vector-01]

TASK [Copy configuration file  for Vector] **************************************************************************************************************************
ok: [vector-01]

TASK [Copy scriptfile  for Vector] **********************************************************************************************************************************
ok: [vector-01]

TASK [Execute Vector in the installation directory] *****************************************************************************************************************
skipping: [vector-01]

PLAY RECAP **********************************************************************************************************************************************************
clickhouse-01              : ok=5    changed=1    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
lighthouse-01              : ok=7    changed=2    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
nginx-01                   : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
vector-01                  : ok=6    changed=1    unreachable=0    failed=0    skipped=4    rescued=0    ignored=0

root@docker:/home/bes/LESSONS/08-ansible-03-yandex/playbook#


Запустите playbook на prod.yml окружении с флагом --diff. Убедитесь, что изменения на системе произведены.
root@docker:/home/bes/LESSONS/08-ansible-03-yandex/playbook# ansible-playbook --diff -i inventory/prod.yml site.yml

PLAY [Install NGINX on hosts] ***************************************************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************************************
ok: [nginx-01]

TASK [Export environment variables for NGINX] ***********************************************************************************************************************
ok: [nginx-01]

TASK [NGINX / Add epel-release repository] **************************************************************************************************************************
ok: [nginx-01]

TASK [NGINX / Install NGINX] ****************************************************************************************************************************************
ok: [nginx-01]

TASK [Insert Default Index Page] ************************************************************************************************************************************
ok: [nginx-01]

PLAY [Install LIGHTHOUSE on hosts] **********************************************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************************************
ok: [lighthouse-01]

TASK [Set facts for NGINX vars] *************************************************************************************************************************************
ok: [lighthouse-01]

TASK [Upload .tar.gz file containing binaries from local storage] ***************************************************************************************************
ok: [lighthouse-01]

TASK [Extract lighthouse in the installation directory] *************************************************************************************************************
ok: [lighthouse-01]

TASK [Add virtual domain in NGINX] **********************************************************************************************************************************
ok: [lighthouse-01]

TASK [Ensure installation dir exists] *******************************************************************************************************************************
ok: [lighthouse-01]

TASK [Export environment variables] *********************************************************************************************************************************
ok: [lighthouse-01]

PLAY [Install ClICKHOUSE on hosts] **********************************************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Get clickhouse distrib] ***************************************************************************************************************************************
ok: [clickhouse-01] => (item=clickhouse-client)
ok: [clickhouse-01] => (item=clickhouse-server)
ok: [clickhouse-01] => (item=clickhouse-common-static)

TASK [Install clickhouse packages] **********************************************************************************************************************************
ok: [clickhouse-01]

TASK [Export environment variables for clickhouse] ******************************************************************************************************************
ok: [clickhouse-01]

TASK [Run clickhouse server] ****************************************************************************************************************************************
changed: [clickhouse-01]

TASK [Create database] **********************************************************************************************************************************************
changed: [clickhouse-01]

PLAY [Install VECTOR on hosts] **************************************************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************************************
ok: [vector-01]

TASK [Export environment variables for Vector] **********************************************************************************************************************
ok: [vector-01]

TASK [Get Vector installed version] *********************************************************************************************************************************
changed: [vector-01]

TASK [Ensure installation dir exists and create if it's not] ********************************************************************************************************
ok: [vector-01]

TASK [Get archive of Vector from remote URL] ************************************************************************************************************************
skipping: [vector-01]

TASK [Extract Vector in the installation directory] *****************************************************************************************************************
ok: [vector-01]

TASK [Copy distrib to working catalog] ******************************************************************************************************************************
changed: [vector-01]

TASK [Copy configuration file  for Vector] **************************************************************************************************************************
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

TASK [Copy scriptfile  for Vector] **********************************************************************************************************************************
ok: [vector-01]

TASK [Execute Vector in the installation directory] *****************************************************************************************************************
changed: [vector-01]

PLAY RECAP **********************************************************************************************************************************************************
clickhouse-01              : ok=6    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
lighthouse-01              : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
nginx-01                   : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
vector-01                  : ok=9    changed=4    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0


Повторно запустите playbook с флагом --diff и убедитесь, что playbook идемпотентен.
Подготовьте README.md файл по своему playbook. В нём должно быть описано: что делает playbook, какие у него есть параметры и теги.
Готовый playbook выложите в свой репозиторий, поставьте тег 08-ansible-03-yandex на фиксирующий коммит, в ответ предоставьте ссылку на него.
