# Домашнее задание к занятию "08.06 Создание собственных modules"

## Подготовка к выполнению
1. Создаём пустой публичный репозиторий в любом своём проекте: `my_own_collection`
2. Скачиваем репозиторий ansible: `git clone https://github.com/ansible/ansible.git` по любому удобному вам пути
3. Переходим в директорию ansible: `cd ansible`
4. Создаём виртуальное окружение: `python3 -m venv venv`
5. Активируем виртуальное окружение: `. venv/bin/activate`. Дальнейшие действия производятся только в виртуальном окружении
6. Устанавливаем зависимости `pip3 install -r requirements.txt`
7. Запускаем настройку окружения `. hacking/env-setup`
8. Выходим из виртуального окружения   `deactivate` 
9. Виртуальное окружение настроено. Переходим в директорию ansible: `cd ansible`
   и выполняем конструкцию `. venv/bin/activate && . hacking/env-setup`

## Основная часть. Главная задача - создать свою коллекцию с модулем и опубликовать её.

1. Устанавливаем python3 версии 3.9.14  и  ansible версии 7.1.0
        # pyenv install 3.9.14
        # pip3 install ansible

2. В виртуальном окружении создаём новый `my_own_module.py` файл

        venv [root@centos-host ~]# touch /modules/my_own_module.py


3. Скачиваем и заполняем шаблонный файл в соответствии с требованиями ansible так, чтобы он выполнял основную задачу: 
   module должен создавать текстовый файл на удалённом хосте по пути, определённом в параметре `path`, с содержимым, определённым в параметре `content`.
   
        Вставляем код со страницы https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html#creating-a-module
        Дополняем модуль run_module()  кодом создания файла.

4. Проверяем module на исполняемость локально. Проверяем путь к локальным модулям и копируем созданный модуль по этому пути .
   
       venv [root@centos-host ~]#  ansible-config dump |grep DEFAULT_MODULE_PATH 
       DEFAULT_MODULE_PATH(default) = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
        
       venv [root@centos-host ~]#  cp  my_own_module.py  /usr/share/ansible/plugins/modules
   
       Запускаем модуль, указав параметры: 

       venv [root@centos-host ~]#  ansible localhost -m my_own_module -a 'path="/root/" content="Hello, Edward!" '
        
5. Пишем  single task playbook и используем module в нём. Для этого создаем файлы   site.yml и inventory/prod.yml . Запускаем playbook
          
       venv [root@centos-host ~]#  ansible-playbook -i inventory/prod.yml site.yml --check
       [WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you are modifying the Ansible engine, or trying out
       features under development. This is a rapidly changing source of code and can become unstable at any point.

       PLAY [Create file with new content.] ********************************************************************************************************************************

       TASK [Gathering Facts] **********************************************************************************************************************************************
       ok: [localhost]

       TASK [Fill content] *************************************************************************************************************************************************
       changed: [localhost]

       PLAY RECAP **********************************************************************************************************************************************************
       localhost                  : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
 
      

6. Проверяем через playbook на идемпотентность.

       venv [root@centos-host ~]#  ansible-playbook --diff -i inventory/prod.yml site.yml --check
       [WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you are modifying the Ansible engine, or trying out
       features under development. This is a rapidly changing source of code and can become unstable at any point.

       PLAY [Create file with new content.] ********************************************************************************************************************************

       TASK [Gathering Facts] **********************************************************************************************************************************************
       ok: [localhost]

       TASK [Fill content] *************************************************************************************************************************************************
       changed: [localhost]

       PLAY RECAP **********************************************************************************************************************************************************
       localhost                  : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

7. Выходим из виртуального окружения.
    
       venv [root@centos-host ~]#  deactivate
        
8. Инициализируем новую collection . Заполняем обязательный файл ansible.cfg

       [root@centos-host ~]#  ansible-galaxy collection init my_own_collection

9. В данную collection переносим свой module в соответствующую директорию

       [root@centos-host ~]#  cp  my_own_module.py    /my_own_collection/plugins/modules 
   
        
10. Single task playbook преобразовываем в single task role и перенесим в collection. У role должны быть default всех параметров module
    
      
11. Создаём playbook site.yml  для использования этой role. 
12. Заполните всю документацию по collection, выложите в свой репозиторий, поставьте тег `1.0.1` на этот коммит.
13. Создаём .tar.gz этой collection: `ansible-galaxy collection build` в корневой директории collection. Выкладываем на Github.
14. Создаём ещё одну директорию NEW, переносим  туда single task playbook и архив c collection.
       
        root@centos-host# ls -la NEW
        итого 16
        drwxr-xr-x.  5 root root  122 янв  4 19:24 .
        dr-xr-x---. 11 root root 4096 янв  4 19:01 ..
        -rw-r--r--.  1 root root 8174 янв  4 19:10 edwardburlakov-my_own_collection-1.0.0.tar.gz
        drwxr-xr-x.  3 root root   17 янв  4 15:40 group_vars
        drwxr-xr-x.  2 root root   22 янв  3 10:23 inventory
        -rw-r--r--.  1 root root   92 янв  4 19:20 site.yml
        drwxr-xr-x.  2 root root    6 янв  4 15:41 vars

        root@centos-host# cat  site.yml
        ---
        - name: Create file with new content.
        hosts: all
        roles:
          - name: my_own_role

15. Устанавливаем  collection из локального архива: `ansible-galaxy collection install -p <destination>   <archivename>.tar.gz`

        root@centos-host# ansible-galaxy collection install -p ansible_collections   edwardburlakov-my_own_collection-1.0.0.tar.gz
        Starting galaxy collection install process
        Process install dependency map
        Starting collection install process
        Installing 'edwardburlakov.my_own_collection:1.0.0' to '/root/.ansible/collections/ansible_collections/edwardburlakov/my_own_collection'
        edwardburlakov.my_own_collection:1.0.0 was installed successfully



16 ю Поверяем что новая коллекция развернулась локально:

        root@centos-host# ansible-galaxy collection list | grep edwardburlakov
        edwardburlakov.my_own_collection 1.0.0



        Вопрос: Как сделать видимым модуль my_own_collection из локально развернутой коллекции  для  запускаемого playbook ? 

        Удалось сделать только так, явно указав путь:

        root@centos-host NEW# cat site.yml
        ---
          - name: Create file with new content.
            hosts: localhost
            roles:
              - /root/.ansible/collections/ansible_collections/edwardburlakov/my_own_collection

16. Запускаем playbook NEW и убеждаемся, что он работает.
   
        root@centos-host NEW# ansible-playbook -i inventory/prod.yml site.yml
 
        PLAY [Create file with new content.] ********************************************************************************************************************************
 
        TASK [Gathering Facts] **********************************************************************************************************************************************
        ok: [localhost]

        PLAY RECAP **********************************************************************************************************************************************************
        ocalhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

17. В ответ необходимо прислать ссылку на репозиторий с collection

* ###  <https://github.com/edward-burlakov/my_own_collection> 


## Необязательная часть

1. Используйте свой полёт фантазии: Создайте свой собственный module для тех roles, что мы делали в рамках предыдущих лекций.
2. Соберите из roles и module отдельную collection.
3. Создайте новый репозиторий и выложите новую collection туда.

Если идей нет, но очень хочется попробовать что-то реализовать: реализовать module восстановления из backup elasticsearch.