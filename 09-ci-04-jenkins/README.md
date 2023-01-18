# Домашнее задание к занятию "10.Jenkins"

---
## Подготовка к выполнению


## 1. Создаём 2 VM: для jenkins-master и jenkins-agent.

    1) На management хосте создаём  нового юзера bes ,отличного от root .  
    2) Генерируем для него ключ id_rsa.pub .  
    3) На YC под данным юзером  cоздаем 2 виртуалки с заданными параметрами .   
    4) Вносим данного пользователя bes  в файл hosts.yml
---
![img_6.png](images/img_6.png)
---

## 2. Прописываем в [inventory](./infrastructure/inventory/cicd/hosts.yml) [playbook'a](./infrastructure/site.yml) созданные хосты.

## 3. Проверяем линтером ansible-lint  файл  [playbook'a](./infrastructure/site.yml)  на ошибки. Исправляем ошибки .

## 4. Устанавливаем используемую библиотеку ansible.posix

    [root@centos-host 09-ci-04-jenkins]#  sudo ansible-galaxy collection install ansible.posix

## 5. Меняем собственника на директорию проекта на пользователя bes.

    [root@centos-host 09-ci-04-jenkins]#  chown -R bes:bes ./infrastructure/

## 6. Запускаем сеанс пользователя bes на management хосте.
        
    [root@centos-host infrastructure]#  su bes

## 7. !!!!  На management хосте входим в cecсию  юзера bes и из-под него разово открываем ssh-соединение с каждым из созданных хостов !!!! иначе плейбук зависнет.

## 8. Устанавливаем  jenkins при помощи playbook'a.  Для этого запускаем и проверяем работоспособность плейбука для развертывания двух серверов - jenkins-master  и  jenkins-agent 
          
    [bes@centos-host infrastructure]$    ansible-playbook  -i inventory/cicd/hosts.yml site.yml

![img.png](images/img.png)

## 9. Выполняем первоначальную настройку Jenkins.

### 1) Входим на удаленный хост и забирем дефолтовый пароль

      [bes@jenkins-master-001 ~]$ sudo cat /var/lib/jenkins/secrets/initialAdminPassword   -  d068cf767e0940d99d64480ed78e37bf

### 2) Входим в интерфейс через браузер http://62.84.122.87:8080/login?from=%2F  и вводим вышеуказанный пароль  чтобы разблокировать.   

### 3) Запускаем установку плагинов

![img_1.png](images/img_1.png)

### 4) Создаем нового админа и его пароль.

### 5) Записываем строку подключения со стороны внешних репозиториев ( bitbucket, gitgub etc.) - http://62.84.122.87:8080/

### 6) Настраиваем внешний узел- агент.

![img_2.png](images/img_2.png)

### 7) Указываем рабочих каталог и  коману запуска процесса JAVA на узле-агенте  . Путь берем из переменной jenkins_agent_dir: ( /opt/jenkins_agent/ )

![img_3.png](images/img_3.png)

### 8) Отключаем внутренние executors- сборщики  на мастере . 

![img_4.png](images/img_4.png)

###      9) Убеждаемся что ипользуются только сборщики на удаленном агенте.

![img_5.png](images/img_5.png)

---
## Основная часть


1. Сделать Freestyle Job, который будет запускать `molecule test` из любого вашего репозитория с ролью.
   
![img_7.png](img_7.png)

2. Сделать Declarative Pipeline Job, который будет запускать `molecule test` из любого вашего репозитория с ролью.

  В сценарии предусматриваем :
   1) Установку пакета-фреймворка molecule.
   2) Установку линтеров YAMLLINT и  ANSIBLE-LINT  .


### 3) Проверяем версию Python / Устанавливаем  версии Python  3.6.15, 3.8.10  и 3.9.16  на основании статьи
[https://medium.datadriveninvestor.com/how-to-install-and-manage-multiple-python-versions-on-linux-916990dabe4b]

             root@dockerhost:/# git clone https://github.com/pyenv/pyenv.git ~/.pyenv
             Добавляем ~/.pyenv в $PATH
             root@dockerhost:/# pyenv install 3.6.15
             root@dockerhost:/# pyenv install 3.8.6
             root@dockerhost:/# pyenv install 3.9.16 

###  4) Устанавливаем версию Python 3.9.16  версией по умолчанию   -  Press ( Ctrl + Z ).

            root@dockerhost:/# pyenv global 3.9.16
            root@dockerhost:/# python3
            Python 3.9.16 (main, Dec 24 2022, 03:29:44)
            [GCC 9.4.0] on linux
            Type "help", "copyright", "credits" or "license" for more information.
            >>>
            [2]+  Stopped                 python3



###  5) Убеждаемся, что необходимые линтеры YAMLLINT и  ANSIBLE-LINT установлены:

            root@dockerhost:/# pip3 install ansible-lint yamllint
            root@dockerhost:/# yamllint --version
            yamllint 1.28.0

            root@dockerhost:/# ansible-lint --version
            ansible-lint 6.8.6 using ansible 2.13.6
            A new release of ansible-lint is available: 6.8.6 → 6.10.0

            root@dockerhost:/# pip3 install git+https://github.com/ansible/ansible-lint.git
            Successfully installed ansible-compat-2.2.7 ansible-lint-6.10.1.dev2 pyyaml-6.0
            root@dockerhost:/home/bes/vector-role/molecule/default# ansible-lint --version
            ansible-lint 6.10.1.dev2 using ansible 2.13.6
            You are using a pre-release version of ansible-lint.
   

3. Перенести Declarative Pipeline в репозиторий в файл `Jenkinsfile`.
4. Создать Multibranch Pipeline на запуск `Jenkinsfile` из репозитория.
5. Создать Scripted Pipeline, наполнить его скриптом из [pipeline](./pipeline).
6. Внести необходимые изменения, чтобы Pipeline запускал `ansible-playbook` без флагов `--check --diff`, если не установлен параметр при запуске джобы (prod_run = True), по умолчанию параметр имеет значение False и запускает прогон с флагами `--check --diff`.
7. Проверить работоспособность, исправить ошибки, исправленный Pipeline вложить в репозиторий в файл `ScriptedJenkinsfile`.
8. Отправить ссылку на репозиторий с ролью и Declarative Pipeline и Scripted Pipeline.
