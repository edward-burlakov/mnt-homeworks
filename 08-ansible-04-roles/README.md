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

---
#### 1) Создаем в старой версии playbook файл requirements.yml и заполняем его следующим содержимым:

       root@docker:/#   cd playbook
       root@docker:/#   touch  requirements.yml 
       root@docker:/# cat playbook /requirements.yml
         ---
           - name: ansible-clickhouse 
             src: git@github.com:AlexeySetevoi/ansible-clickhouse.git
             scm: git
             version: "1.11.0"

---
#### 2) Создаём новый пустой каталог с ролью vector-role при помощи ansible-galaxy из шаблона  по умолчанию

        root@docker:/ # ansible-galaxy role init vector-role
---
#### 3) На основе tasks из старого playbook заполяем  новую role. Разнесите переменные между vars и default.

---
#### 4) Переносим нужные шаблоны конфигов в templates.

---
#### 5) Описываем в README.md обе роли и их параметры.

---
#### 6) Повторяем шаги 2)-5) для lighthouse.  Помним, что одна роль должна настраивать один продукт. 
####    Создаём новый пустой каталог с ролью  lighthouse  при помощи ansible-galaxy из шаблона  по умолчанию

        root@docker:/ # ansible-galaxy role init lighthouse-role

---   
#### 7) Добавляем обе roles, опубликованные  в стороннем репозитории  в requirements.yml в playbook.

         root@docker:/# cat playbook /requirements.yml
         ---
           - name: ansible-clickhouse 
             src: git@github.com:AlexeySetevoi/ansible-clickhouse.git
             scm: git
             version: "1.11.0"
           - name: vector-role
             src: git@github.com:aragastmatb/vector_role.git
             scm: git
             version: "1.0.0"
           - name lighthouse-role           
             src: git@github.com:olezhuravlev/lighthouse-role.git
             scm: git
             version: "1.0.0"

         root@docker:/ # ansible-galaxy role init ansible-lighthouse

---
#### 10) Просталяем тэги, используя семантическую нумерацию  

---
#### 11) Выкладываем все roles в репозитории. 

           # cat /playbook/site.yml
           ---
           - name Assert lighthouse role
             hosts: lighthouse
             roles:
               - ansible-lighthouse

           - name Assert lighthouseclickhouse role
             hosts: vector
             roles:
               - ansible-vector

           - name Assert clickhouse role
             hosts: clickhouse
             roles:
               - ansible-clickhouse




12) Переработайте playbook на использование roles. Не забудьте про зависимости lighthouse и возможности совмещения roles с tasks.

Выложите playbook в репозиторий.

В ответ приведите ссылки на оба репозитория с roles и одну ссылку на репозиторий с playbook.