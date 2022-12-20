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
### публикуем его  в личном кабинете GITHUB с именем vector-role  [https://github.com/edward-burlakov/vector-role.git].
         
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
###         В vars- те,что сможет менять пользователь опубликованного нами плейбука.

---
### 5) Переносим нужные шаблоны конфигов  из каталога templates основного проекта "LESSON_8.4"  в  папку templates.

---
###  6) Публикуем изменения проекта vector-role на GITHUB . Добавляем  tag "1.0.0"  на итоговый коммит для версионирования  опубликованной роли
        и публикации релиза в виде архива .

---
### 7)  На management хосте  с установленным Ansible  создаём публичный репозиторий для роли  lighthouse-role.
### И  публикуем его  в личном кабинете GITHUB с именем vector-role  [https://github.com/edward-burlakov/lighthouse-role.git].  

          root@docker:/#  git init
          root@docker:/#  git branch -M main
          root@docker:/#  git remote add origin https://github.com/edward-burlakov/lighthouse-role .git
          root@docker:/#  git push -u origin main
          
--- 
### 8)   Развертываем пустой каталог  lighthouse  при помощи ansible-galaxy из шаблона  по умолчанию
       
         root@docker:/#  ansible-galaxy role init lighthouse-role
---
### 9)  Повторяем шаги 4)-5)-6) для  проекта lighthouse.  Помним, что одна роль должна настраивать один продукт. 

---
### 10) Описываем в README.md  основного проекта обе роли и их параметры.

---
### 11) Добавляем обе roles, опубликованные  в стороннем репозитории  в requirements.yml в playbook.

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
### 12) Проставляем тэги , в обоих проектах , используя семантическую нумерацию. 

---
### 13) Выкладываем все roles в репозитории. 

           # cat /playbook/site.yml
           ---
           - name Assert lighthouse role
             hosts: lighthouse
             roles:
               - ansible-lighthouse-role 
           - name Assert vector role
             hosts: vector
             roles:
               - ansible-vector-role
           - name Assert clickhouse role
             hosts: clickhouse
             roles:
               - ansible-clickhouse

---
### 14) Запускаем плейбук и добиваемся работоспособности проекта.  
        Перерабаьываем playbook на использование roles. 
        Не забываем про зависимости lighthouse и возможности совмещения roles с tasks.


### 15) Выкладываем итоговый playbook в репозиторий.


Ниже- ссылки на оба репозитория с roles и одна ссылку на репозиторий с playbook.

[https://github.com/edward-burlakov/lighthouse-role.git]
[https://github.com/edward-burlakov/vector-role.git]
[https://github.com/edward-burlakov/mnt-homeworks/tree/master/08-ansible-04-roles]





