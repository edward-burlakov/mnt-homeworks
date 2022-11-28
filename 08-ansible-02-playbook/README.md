---
## Домашнее задание к занятию "08.02 Работа с Playbook"

----
### 1. Изменяем файл  prod.yml в соответствии с заданием

      Создаем  третий play  для развертывания пакета kibana .
      Также создаем файл vars.yml  с переменными  пакета kibana   в каталоге /group_vars/kibana .

----
### 2. Tasks должны: скачать нужной версии дистрибутив, выполнить распаковку в выбранную директорию, сгенерировать конфигурацию с параметрами.
   
       ПРИМЕЧАНИЕ:  Из-за недоступности сервера дистрибутивов https://artifacts.elastic.co  дистрибутивы скачаны 
       через VPN на другом сервере и также положены  в директорию  `playbook/files/`   домашнего задания `LESSON_8.1.`

----
### 3. Запускаем  `ansible-lint site.yml` и исправляем ошибки. Результат:

       root@ubuntu22:~/# ansible-lint site.yml
       WARNING  Overriding detected file kind 'yaml' with 'playbook' for given positional argument: site.yml
       root@ubuntu22:~/#

----
### 4. Запускаем playbook на этом окружении с флагом `--check`.


      root@ubuntu22:~/# ansible-playbook -i inventory/prod.yml site.yml --check

      PLAY [Install Java Developers Kit] ***************************************************************************************************

      TASK [Gathering Facts] **************************************************************************************************************
      ok: [localhost]

      TASK [Set facts for Java 11 vars] ***************************************************************************************************
      ok: [localhost]

      TASK [Upload .tar.gz file containing binaries from local storage] ********************************************************************
      changed: [localhost]

      TASK [Ensure installation dir exists] *************************************************************************************************
      changed: [localhost]

      TASK [Extract java in the installation directory] *************************************************************************************
      skipping: [localhost]

      TASK [Export environment variables] ***************************************************************************************************
      ok: [localhost]

      PLAY [Install Elasticsearch] **********************************************************************************************************

      TASK [Gathering Facts] ****************************************************************************************************************
      ok: [localhost]

      TASK [Upload tar.gz Elasticsearch from remote URL] *************************************************************************************
      changed: [localhost]

      TASK [Create directrory for Elasticsearch] *********************************************************************************************
      ok: [localhost]

      TASK [Extract Elasticsearch in the installation directory] ****************************************************************************
      skipping: [localhost]

      TASK [Set environment Elastic] ********************************************************************************************************
      ok: [localhost]

      PLAY [Install Kibana] *****************************************************************************************************************

      TASK [Gathering Facts] ****************************************************************************************************************
      ok: [localhost]

      TASK [Upload tar.gz Kibana from remote URL] *******************************************************************************************
      ok: [localhost]

      TASK [Create directrory Kibana] *******************************************************************************************************
      ok: [localhost]

      TASK [Extract Kibana in the installation directory] ************************************************************************************
      skipping: [localhost]

      TASK [Set environment kibana] **********************************************************************************************************
      ok: [localhost]

      PLAY RECAP *****************************************************************************************************************************
      localhost                  : ok=13   changed=3    unreachable=0    failed=0    skipped=3    rescued=0    ignored=0


----
### 5. Запускаем  playbook на `prod.yml` окружении с флагом `--diff`. Убеждаемся, что изменения на системе произведены.

       root@ubuntu22:~/# ansible-playbook -i inventory/prod.yml site.yml --diff

       PLAY [Install Java Developers Kit] *****************************************************************************************************

       TASK [Gathering Facts] *****************************************************************************************************************
       ok: [localhost]

       TASK [Set facts for Java 11 vars] ******************************************************************************************************
       ok: [localhost]

       TASK [Upload .tar.gz file containing binaries from local storage] ***********************************************************************
       --- before
       +++ after
       @@ -1,4 +1,4 @@
       {
       -    "mode": "0644",
       +    "mode": "0755",
            "path": "/tmp/jdk-11.0.17_linux-x64_bin.tar.gz"
       }

       changed: [localhost]

      TASK [Ensure installation dir exists] ****************************************************************************************************
      --- before
      +++ after
      @@ -1,4 +1,4 @@
      {
      -    "mode": "0755",
      +    "mode": "0644",
           "path": "/opt/jdk/11.0.17"
      }

      changed: [localhost]

      TASK [Extract java in the installation directory] ****************************************************************************************
      skipping: [localhost]

      TASK [Export environment variables] ******************************************************************************************************
      ok: [localhost]
 
      PLAY [Install Elasticsearch] *************************************************************************************************************

      TASK [Gathering Facts] *******************************************************************************************************************
      ok: [localhost]

      TASK [Upload tar.gz Elasticsearch from remote URL] ***************************************************************************************
      --- before
      +++ after
      @@ -1,4 +1,4 @@
      {
      -    "mode": "0644",
      +    "mode": "0755",
           "path": "/tmp/elasticsearch-7.10.1-linux-x86_64.tar.gz"
      }

      changed: [localhost]

     TASK [Create directrory for Elasticsearch] *************************************************************************************************
     ok: [localhost]

     TASK [Extract Elasticsearch in the installation directory] *********************************************************************************
     skipping: [localhost]

     TASK [Set environment Elastic] *************************************************************************************************************
     ok: [localhost]

     PLAY [Install Kibana] **********************************************************************************************************************

     TASK [Gathering Facts] ********************************************************************************************************************
     ok: [localhost]

     TASK [Upload tar.gz Kibana from remote URL] ************************************************************************************************
     ok: [localhost]

     TASK [Create directrory Kibana] ************************************************************************************************************
     ok: [localhost]

     TASK [Extract Kibana in the installation directory] ****************************************************************************************
     skipping: [localhost]

     TASK [Set environment kibana] ************************************************************************************************************
     ok: [localhost]

     PLAY RECAP *******************************************************************************************************************************
     localhost                  : ok=13   changed=3    unreachable=0    failed=0    skipped=3    rescued=0    ignored=0

----
### 6. Повторно запускаем  playbook с флагом `--diff` и убеждаемся, что playbook идемпотентен.


     root@ubuntu22:~/# ansible-playbook -i inventory/prod.yml site.yml --diff                                       
     PLAY [Install Java Developers Kit] ********************************************************************************************************

     TASK [Gathering Facts] *******************************************************************************************************************
     ok: [localhost]

     TASK [Set facts for Java 11 vars] *********************************************************************************************************
     ok: [localhost]

     TASK [Upload .tar.gz file containing binaries from local storage] ************************************************************************
     ok: [localhost]

    TASK [Ensure installation dir exists] *****************************************************************************************************
     ok: [localhost]

    TASK [Extract java in the installation directory] *****************************************************************************************
    skipping: [localhost]

    TASK [Export environment variables] *******************************************************************************************************
    ok: [localhost]

    PLAY [Install Elasticsearch] **************************************************************************************************************

    TASK [Gathering Facts] ********************************************************************************************************************
    ok: [localhost]

    TASK [Upload tar.gz Elasticsearch from remote URL] ****************************************************************************************
    ok: [localhost]

    TASK [Create directrory for Elasticsearch] ************************************************************************************************
    ok: [localhost]

    TASK [Extract Elasticsearch in the installation directory] ********************************************************************************
    skipping: [localhost]

    TASK [Set environment Elastic] ************************************************************************************************************
    ok: [localhost]

    PLAY [Install Kibana] *********************************************************************************************************************

    TASK [Gathering Facts] ********************************************************************************************************************
    ok: [localhost]

    TASK [Upload tar.gz Kibana from remote URL] ***********************************************************************************************
    ok: [localhost]

    TASK [Create directrory Kibana] ***********************************************************************************************************
    ok: [localhost]

    TASK [Extract Kibana in the installation directory] ***************************************************************************************
    skipping: [localhost]

    TASK [Set environment kibana] *************************************************************************************************************
    ok: [localhost]

    PLAY RECAP ********************************************************************************************************************************
    localhost                  : ok=13   changed=0    unreachable=0    failed=0    skipped=3    rescued=0    ignored=0

----
### 7. Подготовьте README.md файл по своему playbook. В нём должно быть описано: что делает playbook, какие у него есть параметры и теги.

   
    Плейбук последовательно запускает три play  путем подключения по протоколу ssh к локальному хосту,  и выполняет установку  
    трех пакетов- JDK версии 11.0.17  ,  ELASTICSEARCH версии 7.10.1  и   KIBANA 7.10.1.
    При выполнении пакеты закачиваются с локального ресурса  /playbook/files во временный каталог /tmp, затем разархивируется в рабочие каталоги программ , 
    расположенные  в каталоге /opt.   Также  для локального хоста публикуется переменные каждого пакета в переменной PATH и также формируются 
    скрипты автоматического экпорта данных переменных путем формования скриптов автозапуска в каталоге /etc/profile.d/ .
    Если при проверке целевого рабочего каталога уже присутствует исполняемый скрипт соответствующего пакета, распаковка не производится.
    
    В  трех плеях  использованы три вида тегов :

        Play "Install Java Developers Kit"  : java  
        Play "Install Elasticsearch"        : elastic
        PLay "Install Kibana"               : kibana 
    
    Использованы  переменные  со следующими значениями:
        Play "Install Java Developers Kit"
          java_jdk_version: "11.0.17"
          java_oracle_jdk_package: "jdk-{{java_jdk_version }}_linux-x64_bin.tar.gz"

        Play "Install Elasticsearch"   
          elastic_version: "7.10.1"
          elastic_home: "/opt/elastic/{{ elastic_version }}"

        PLay "Install Kibana"
          kibana_version: "7.10.1"
          kibana_home: "/opt/kibana/{{ kibana_version }}"
