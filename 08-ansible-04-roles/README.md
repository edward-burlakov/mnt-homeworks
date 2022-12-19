--
## Домашнее задание к занятию "8.4. Работа с roles"

----
### Создайте два пустых публичных репозитория в любом своём проекте: vector-role и lighthouse-role.
Добавьте публичную часть своего ключа к своему профилю в github.
Основная часть
Наша основная цель - разбить наш playbook на отдельные roles. 
Задачи: 
 - сделать roles для clickhouse, vector и lighthouse 
 - написать playbook для использования этих ролей. 
 - Ожидаемый результат: существуют три ваших репозитория: два с roles и один с playbook.

----
1) Создаем в старой версии playbook файл requirements.yml и заполняем его следующим содержимым:

       root@docker:/#   cd playbook
       root@docker:/#   touch  requirements.yml 
       root@docker:/#   cat   playbook /requirements.yml 
       ---
         - src: git@github.com:AlexeySetevoi/ansible-clickhouse.git
           scm: git
           version: "1.11.0"
           name: clickhouse

----    
2) При помощи ansible-galaxy скачиваем  роль  ansible-clickhouse.   
        
        root@docker:/#  cd playbook
        root@docker:/#  mkdir roles
        root@docker:/#  cd roles
        root@docker:/#  ansible-galaxy role init ansible-clickhouse
        root@docker:/# ls -la
        total 12
        drwxr-xr-x  3 root root 4096 Dec 20 02:12 .
        drwxr-xr-x  7 root root 4096 Dec 20 02:11 ..
        drwxr-xr-x 10 root root 4096 Dec 20 02:12 ansible-clickhouse

----
3) Добавляем в файл requirements.yml  путь к второй  роли  vector 


        root@docker:/# cat playbook /requirements.yml
         ---
           - name: ansible-clickhouse 
             src: git@github.com:AlexeySetevoi/ansible-clickhouse.git
             scm: git
             version: "1.11.0"
           - name: ansible-vector
             src git@github.com:aragastmatb/vector_role.git
             scm: git
             version: "1.0.0"
             

----
4) Создаём новый каталог с ролью ansible-vector при помощи ansible-galaxy

        root@docker:/ # ansible-galaxy role init ansible-vector

5) На основе tasks из старого playbook заполните новую role. Разнесите переменные между vars и default.

6) Переносим нужные шаблоны конфигов в templates.


7) Описать в README.md обе роли и их параметры.

8) Повторяем шаги и 3-6 для lighthouse.  Помните, что одна роль должна настраивать один продукт.

         root@docker:/# cat playbook /requirements.yml
         ---
           - name: ansible-clickhouse 
             src: git@github.com:AlexeySetevoi/ansible-clickhouse.git
             scm: git
             version: "1.11.0"
           - name: ansible-vector
             src git@github.com:aragastmatb/vector_role.git
             scm: git
             version: "1.0.0"
           - name ansible-lighthouse           
             git@github.com:olezhuravlev/lighthouse-role.git
             scm: git
             version: "1.0.0"

         root@docker:/ # ansible-galaxy role init ansible-lighthouse

9) 


Выложите все roles в репозитории. Проставьте тэги, используя семантическую нумерацию Добавьте roles в requirements.yml в playbook.

Переработайте playbook на использование roles. Не забудьте про зависимости lighthouse и возможности совмещения roles с tasks.

Выложите playbook в репозиторий.

В ответ приведите ссылки на оба репозитория с roles и одну ссылку на репозиторий с playbook.