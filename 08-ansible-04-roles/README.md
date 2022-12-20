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
#### 2) На managemenеt хосте  с Ansible cоздаем  публичный репозиторий vector-role локально и  публикуем его  в личном кабинете GITHUB - vector-role .
        
---
#### 3)  Внутри репозитория создаём новую структуры каталог с ролью vector-role при помощи ansible-galaxy из шаблона  по умолчанию

        root@docker:/ # ansible-galaxy role init vector-role
---
#### 4) На основе tasks из старого playbook заполняем  новую role. Из старого проекта (LESSON_8.3 ) переносим все такси касающиеся роли vector .
        Также разнсим переменные  из старых каталогов group_vars между vars и default.
---
#### 5) Переносим нужные шаблоны конфигов  из старого проекта (LESSON_8.3 )  в  папку templates.

---
###  6) Публикуем изменения проекта vector-role на GITHUB . Добавляем на итоговый коммит  tag "1.0.0" для версионирования  опубликованной роли.

---
#### 7) Повторяем шаги 2)-5) для lighthouse.  Помним, что одна роль должна настраивать один продукт. 
####    Создаём новый пустой каталог с ролью  lighthouse  при помощи ansible-galaxy из шаблона  по умолчанию

        root@docker:/ # ansible-galaxy role init lighthouse-role

---
#### 8) Описываем в README.md обе роли и их параметры.

---
#### 9) Добавляем обе roles, опубликованные  в стороннем репозитории  в requirements.yml в playbook.

         root@docker:/# cat playbook /requirements.yml
         ---
           - name: ansible-clickhouse 
             src: git@github.com:AlexeySetevoi/ansible-clickhouse.git
             scm: git
             version: "1.11.0"
           - name: ansible-vector-role
             src: git@github.com/edward-burlakov/vector-role.git
             scm: git
             version: "1.0.0"
           - name ansible-lighthouse-role           
             src: git@github.com/edward-burlakov/lighthouse-role.git
             scm: git
             version: "1.0.0"

---
#### 10) Проставляем тэги, используя семантическую нумерацию  

---
#### 11) Выкладываем все roles в репозитории. 

           # cat /playbook/site.yml
           ---
           - name Assert lighthouse role
             hosts: lighthouse
             roles:
               - ansible-lighthouse-role 

           - name Assert lighthouseclickhouse role
             hosts: vector
             roles:
               - ansible-vector-role

           - name Assert clickhouse role
             hosts: clickhouse
             roles:
               - ansible-clickhouse



12) Переработайте playbook на использование roles. Не забудьте про зависимости lighthouse и возможности совмещения roles с tasks.



13) Выкладываем итоговый playbook в репозиторий.

В ответ приведите ссылки на оба репозитория с roles и одну ссылку на репозиторий с playbook.