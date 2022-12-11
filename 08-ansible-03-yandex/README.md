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

3) Запускаем ansible-playbook -vv -i inventory/test.yml site.yml .

       # ansible-playbook -vv -i inventory/test.yml site.yml

4) Если всё  прошло успешно входим на сервер и проверяесм статус сервера clickhouse
 
       # ssh -l bes <IP адрес clickhouse севера>
       [bes@clickhouse-01 ~]$ sudo systemctl status clickhouse-server
       ● clickhouse-server.service - ClickHouse Server (analytic DBMS for big data)
       Loaded: loaded (/usr/lib/systemd/system/clickhouse-server.service; enabled; vendor preset: disabled)
       Active: active (running) since Sun 2022-12-11 10:11:14 UTC; 2min 22s ago
       ...
       #

5)     Проеряем подключение с помощью клиента данной БД

       [bes@clickhouse-01 ~]$ sudo systemctl status clickhouse-server
       ClickHouse client version 22.9.6.20 (official build).
       Connecting to localhost:9000 as user default.
       Connected to ClickHouse server version 22.9.6 revision 54460.

       Warnings:
       * Linux transparent hugepages are set to "always". Check /sys/kernel/mm/transparent_hugepage/enabled
       * Linux threads max count is too low. Check /proc/sys/kernel/threads-max
       * Maximum number of threads is lower than 30000. There could be problems with handling a lot of simultaneous queries.
       clickhouse-01.ru-central1.internal :

6) 
7) 
Допишите playbook: нужно сделать ещё один play, который устанавливает и настраивает lighthouse.
При создании tasks рекомендую использовать модули: get_url, template, yum, apt.
Tasks должны: скачать статику lighthouse, установить nginx или любой другой webserver, настроить его конфиг для открытия lighthouse, запустить webserver.
Приготовьте свой собственный inventory файл prod.yml.
Запустите ansible-lint site.yml и исправьте ошибки, если они есть.
Попробуйте запустить playbook на этом окружении с флагом --check.
Запустите playbook на prod.yml окружении с флагом --diff. Убедитесь, что изменения на системе произведены.
Повторно запустите playbook с флагом --diff и убедитесь, что playbook идемпотентен.
Подготовьте README.md файл по своему playbook. В нём должно быть описано: что делает playbook, какие у него есть параметры и теги.
Готовый playbook выложите в свой репозиторий, поставьте тег 08-ansible-03-yandex на фиксирующий коммит, в ответ предоставьте ссылку на него.
