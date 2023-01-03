# Домашнее задание к занятию "08.04 Создание собственных modules"

## Подготовка к выполнению
1. Создайте пустой публичный репозиторий в любом своём проекте: `my_own_collection`
2. Скачайте репозиторий ansible: `git clone https://github.com/ansible/ansible.git` по любому удобному вам пути
3. Зайдите в директорию ansible: `cd ansible`
4. Создайте виртуальное окружение: `python3 -m venv venv`
5. Активируйте виртуальное окружение: `. venv/bin/activate`. Дальнейшие действия производятся только в виртуальном окружении
6. Установите зависимости `pip3 install -r requirements.txt`
7. Запустить настройку окружения `. hacking/env-setup`
8. Если все шаги прошли успешно - выйти из виртуального окружения   `deactivate` 
9. Ваше окружение настроено, для того чтобы запустить его, нужно находиться в директории `ansible` 
   и выполнить конструкцию `. venv/bin/activate && . hacking/env-setup`

## Основная часть

1. Устанавливаем python3 версии 3.9.14  и  ansible версии 7.1.0
        # pyenv install 3.9.14
        # pip3 install ansible

2. В виртуальном окружении создаём новый `my_own_module.py` файл

        venv [root@centos-host ~]# touch /modules/my_own_module.py


3. Заполняем файл в соответствии с требованиями ansible так, чтобы он выполнял основную задачу: 
   module должен создавать текстовый файл на удалённом хосте по пути, определённом в параметре `path`, с содержимым, определённым в параметре `content`.
   
        Вставляем код со страницы https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html#creating-a-module
        Дополняем модуль run_module()  кодом создания файла .

4. Проверяем module на исполняемость локально. Проверяем путь к локальным модулям и копируем созданный модуль по этому пути .
   Запускаем модуль, указав параметры: 
       
       venv [root@centos-host ~]#  ansible-config dump |grep DEFAULT_MODULE_PATH 
       DEFAULT_MODULE_PATH(default) = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
         
       venv [root@centos-host ~]#  cp  my_own_module.py  /usr/share/ansible/plugins/modules

       venv [root@centos-host ~]#  ansible localhost -m my_own_module -a 'path="/root/" content="Hello, Edward!" '
        
4. Пишем  single task playbook и используем module в нём. Для этого создаем файлы   site .yml и inventory/prod.yml . Запускаем playbook
          
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
 
      

5. Проверяем через playbook на идемпотентность.

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

6. Выходим из виртуального окружения.
    
       venv [root@centos-host ~]#  deactivate
        
7. Инициализируем новую collection:

       [root@centos-host ~]#  ansible-galaxy collection init edward-burlakov.ansible_collection

9. В данную collection перенесите свой module в соответствующую директорию.
10. Single task playbook преобразуйте в single task role и перенесите в collection. У role должны быть default всех параметров module
11. Создайте playbook для использования этой role.
12. Заполните всю документацию по collection, выложите в свой репозиторий, поставьте тег `1.0.1` на этот коммит.
13. Создайте .tar.gz этой collection: `ansible-galaxy collection build` в корневой директории collection.
14. Создайте ещё одну директорию любого наименования, перенесите туда single task playbook и архив c collection.
15. Установите collection из локального архива: `ansible-galaxy collection install <archivename>.tar.gz`
16. Запустите playbook, убедитесь, что он работает.
17. В ответ необходимо прислать ссылку на репозиторий с collection

## Необязательная часть

1. Используйте свой полёт фантазии: Создайте свой собственный module для тех roles, что мы делали в рамках предыдущих лекций.
2. Соберите из roles и module отдельную collection.
3. Создайте новый репозиторий и выложите новую collection туда.

Если идей нет, но очень хочется попробовать что-то реализовать: реализовать module восстановления из backup elasticsearch.