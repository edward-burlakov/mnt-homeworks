--
## Домашнее задание к занятию "4. Работа с roles"

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
1) Создаем в старой версии playbook файл requirements.yml и заполняем его следующим содержимым:

       # cd playbook
       # touch  requirements.yml 
       # cat   playbook /requirements.yml 
       ---
         - src: git@github.com:AlexeySetevoi/ansible-clickhouse.git
           scm: git
           version: "1.11.0"
           name: clickhouse

---    
2) При помощи ansible-galaxy скачиваем  роль  ansible-clickhouse.  папка назначения  на основании  /etc/ansible/ansible.cfg - 
   cat 
       #  ansible-galaxy role init ansible-clickhouse


3) Создать новый каталог с ролью при помощи ansible-galaxy

       # ansible-galaxy role init vector-role.

На основе tasks из старого playbook заполните новую role. Разнесите переменные между vars и default.

Перенести нужные шаблоны конфигов в templates.

Описать в README.md обе роли и их параметры.

Повторите шаги 3-6 для lighthouse. Помните, что одна роль должна настраивать один продукт.

Выложите все roles в репозитории. Проставьте тэги, используя семантическую нумерацию Добавьте roles в requirements.yml в playbook.

Переработайте playbook на использование roles. Не забудьте про зависимости lighthouse и возможности совмещения roles с tasks.

Выложите playbook в репозиторий.

В ответ приведите ссылки на оба репозитория с roles и одну ссылку на репозиторий с playbook.