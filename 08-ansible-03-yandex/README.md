---
## Домашнее задание к занятию "3. Использование Yandex Cloud"
--
Подготовка к выполнению
Подготовьте в Yandex Cloud три хоста: для clickhouse, для vector и для lighthouse.
Ссылка на репозиторий LightHouse: https://github.com/VKCOM/lighthouse

---
## Основная часть
1) Создаем  в YC  три хоста  clickhouse-01, vector-01  , lighthouse-01 .

       Указываем в атрибута хостов польщователя bes  .  
       В атрибутах хостов d поле  ssh ключа копируеb вставляем public ключ с локального хоста, на котором запускаем ansible.
       подключаемся к удаленным хостам по sdsh
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
