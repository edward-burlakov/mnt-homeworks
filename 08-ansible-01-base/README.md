--
## Домашнее задание к занятию "08.01 Введение в Ansible"

---
### Основная часть
1. Запускаем playbook на окружении из `test.yml`. Факт `some_fact` имеет значение 12  .

         root@docker:/# ansible-playbook site.yml -i  inventory/test.yml -k
         SSH password:
    
         PLAY [Print os facts] ***********************************************************************************************************************************************
    
         TASK [Gathering Facts] **********************************************************************************************************************************************
         ok: [localhost]
    
         TASK [Print OS] *****************************************************************************************************************************************************
         ok: [localhost] => {
             "msg": "Ubuntu"
         }
    
         TASK [Print fact] ***************************************************************************************************************************************************
         ok: [localhost] => {
             "msg": 12
         }
    
         PLAY RECAP **********************************************************************************************************************************************************
         localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

2. Найдите файл с переменными (group_vars) в котором задаётся найденное в первом пункте значение и поменяйте его на 'all default fact'.
         
         Результат: 

         root@docker:/#  cat group_vars/all/examp.yml 
         ---
           some_fact: "all default fact"

         Вывод ansible:

         root@docker:~/# ansible-playbook site.yml -i inventory/test.yml
         ....
         TASK [Print fact] **************************************************************************************************************************************************
         ok: [localhost] => {
              "msg": "all default fact"
         }
   
         PLAY RECAP *********************************************************************************************************************************************************
         localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
         ....

         root@docker:~/#

3. Cоздаём собственное окружение для проведения дальнейших испытаний.
   
        1) Проверяем путь, где находятся плагины ansible

          root@docker:/#   ansible --version
          ...
          configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
          ...

       2) Устанавливаем плагин  поддержки docker  (!!!) для текущего пользователя (!!!)

          root@docker:/#  ansible-galaxy collection install community.docker 
          Starting galaxy collection install process
          Process install dependency map
          Starting collection install process
          Downloading https://galaxy.ansible.com/download/community-docker-3.2.1.tar.gz to /root/.ansible/tmp/ansible-local-6743rq0vztb2/tmpa0nveont/community-docker-3.2.1-5ieckqan
          Installing 'community.docker:3.2.1' to '/root/.ansible/collections/ansible_collections/community/docker'
          community.docker:3.2.1 was installed successfully

       3)  Проверяем установку модулей 
        
          root@docker:~/.ansible/collections/ansible_collections/community/docker/plugins/connection# ls -la
          total 60
          drwxr-xr-x 2 root root  4096 Nov 21 02:00 .
          drwxr-xr-x 8 root root  4096 Nov 21 02:00 ..
          -rw-r--r-- 1 root root 17190 Nov 21 02:00 docker_api.py
          -rw-r--r-- 1 root root 19294 Nov 21 02:00 docker.py
          -rw-r--r-- 1 root root 10161 Nov 21 02:00 nsenter.py

       4) Собираем и запускаем контейнеры  Centos и  Ubuntu

         root@docker:/#  docker run -dit --name centos7   pycontribs/centos:7      sleep 6000000
         root@docker:/#  docker run -dit --name ubuntu    pycontribs/ubuntu:latest  sleep 6000000
         root@docker:/#  docker ps -a
         CONTAINER ID   IMAGE                      COMMAND           CREATED          STATUS          PORTS     NAMES
         80f1d7019ea2   pycontribs/ubuntu:latest   "sleep 6000000"   9 minutes ago    Up 9 minutes              ubuntu
         346ad5c71fe9   pycontribs/centos:7        "sleep 6000000"   13 minutes ago   Up 13 minutes             centos7

4. Производим запуск playbook на окружении из `prod.yml`. Фиксируем полученные значения `some_fact` для каждого из `managed host`.
       Внимание !!! Имена хостов в prod.xml должны обязательно  совпадать чс именами в поле NAMES docker-контейнеров!!!

         root@ubuntu22:~/# ansible-playbook site.yml -i  inventory/prod.yml
          ... 
          TASK [Print fact] ********************************************************************************************************
          ok: [centos7] => {
              "msg": "some_fact"
          }
          ok: [ubuntu] => {
              "msg": "some_fact"
          }
   
          PLAY RECAP ***************************************************************************************************************
          centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
          ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

5. Добавляем факты в `group_vars` каждой из групп хостов так, чтобы для `some_fact` получились следующие значения: 
   для `deb` - 'deb default fact',  для `el` - 'el default fact'.

          root@ubuntu22:~/# cat group_vars/deb/examp.yml
          ---
          some_fact: "deb default fact"
         
          root@ubuntu22:~/# cat group_vars/el/examp.yml
          ---
          some_fact: "el default fact"


6. Повторяем запуск playbook на окружении `prod.yml`. Убеждаемся, что выдаются корректные значения для всех хостов.
 
          root@ubuntu22:~/# ansible-playbook site.yml -i  inventory/prod.yml
          ...   
          TASK [Print fact] *********************************************************************************************************
          ok: [centos7] => {
              "msg": "el default fact"
          }
          ok: [ubuntu] => {
              "msg": "deb default fact"
          }
   
          PLAY RECAP ****************************************************************************************************************
          centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
          ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


 
7. При помощи `ansible-vault` шифруем  факты в `group_vars/deb` и `group_vars/el` с паролем `netology`.

        #  ansible-vault encrypt group_vars/deb/examp.yml
        #  ansible-vault encrypt group_vars/el/examp.yml

        Результат: 
   
        root@ubuntu22:~/# cat group_vars/deb/examp.yml
        $ANSIBLE_VAULT;1.1;AES256
        38366665303237356433633038303564333464643531613638616161633332306266636539663933
        3735643934353031343361613439306362396338393039620a653762633363303165353664643038
        31323564363863303632333762626431323464663161633965343736666236313461306333656530
        3261383363313565340a643332306533366332363565633931643535303239653464363636646562
        35316263623862366663396363396262386139643562346366386365316166633866303634626337
        6534616435373837646533316361636336333962613036353632


        root@ubuntu22:~/# cat group_vars/el/examp.yml
        $ANSIBLE_VAULT;1.1;AES256
        36653561333931623062663234663333636263343534663435333138313932363133306237306663
        3531386430346535323138303132613638373637353431300a363839333938636633343038626539
        31643137383965326335613963343066636664303037653933396165346363396539353363656439
        3333326233666232310a616132653935313932363832316264396564343831376132333230616636
        66336531663064366537663864633632373061343564376439643733623362343336666331353766
        3737646636616262343537633630393931383535353938373538
    
 
8. Запускаем playbook на окружении `prod.yml`. При запуске `ansible` должен запросить пароль. Убеждаемся в работоспособности.
 
       # ansible-playbook  -i inventory/prod.yml site.yml --ask-vault-pass
        ....
        PLAY RECAP ****************************************************************************************************************
        centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
        ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

9. Выводим  при помощи `ansible-doc` список плагинов для подключения. 

    Выбираем коннектор "local", как подходящий для работы на `control node`.

          # ansible-doc -t connection  -F
          ansible.netcommon.grpc         /usr/lib/python3/dist-packages/ansible_collections/ansible/netcommon/plugins/connection/grpc.py
          ansible.netcommon.httpapi      /usr/lib/python3/dist-packages/ansible_collections/ansible/netcommon/plugins/connection/httpapi.py
          ansible.netcommon.libssh       /usr/lib/python3/dist-packages/ansible_collections/ansible/netcommon/plugins/connection/libssh.py
          ansible.netcommon.napalm       /usr/lib/python3/dist-packages/ansible_collections/ansible/netcommon/plugins/connection/napalm.py
          ansible.netcommon.netconf      /usr/lib/python3/dist-packages/ansible_collections/ansible/netcommon/plugins/connection/netconf.py
          ansible.netcommon.network_cli  /usr/lib/python3/dist-packages/ansible_collections/ansible/netcommon/plugins/connection/network_cli.py
          ansible.netcommon.persistent   /usr/lib/python3/dist-packages/ansible_collections/ansible/netcommon/plugins/connection/persistent.py
          community.aws.aws_ssm          /usr/lib/python3/dist-packages/ansible_collections/community/aws/plugins/connection/aws_ssm.py
          community.docker.docker        /root/.ansible/collections/ansible_collections/community/docker/plugins/connection/docker.py
          ......
          ......
          kubernetes.core.kubectl        /usr/lib/python3/dist-packages/ansible_collections/kubernetes/core/plugins/connection/kubectl.py
          local                          /usr/lib/python3/dist-packages/ansible/plugins/connection/local.py
          paramiko_ssh                   /usr/lib/python3/dist-packages/ansible/plugins/connection/paramiko_ssh.py
          psrp                           /usr/lib/python3/dist-packages/ansible/plugins/connection/psrp.py
          ssh                            /usr/lib/python3/dist-packages/ansible/plugins/connection/ssh.py
          winrm                          /usr/lib/python3/dist-packages/ansible/plugins/connection/winrm.py


10. В `prod.yml` добавляем новую группу хостов с именем  `local`, в ней размещаем localhost с необходимым типом подключения.
       
        # cat inventory/prod.yml
        ---
        el:
          hosts:
            centos7:
              ansible_connection: docker
        deb:
          hosts:
            ubuntu:
              ansible_connection: docker
        local:
          hosts:
            localhost:
              ansible_connection: local



11. Запускаем playbook на окружении `prod.yml`. При запуске `ansible` должен запросить пароль. 
   Убеждаемся, что факты `some_fact` для каждого из хостов определены из верных `group_vars`.

        # ansible-playbook  -i inventory/prod.yml site.yml --ask-vault-pass
        Vault password:
 
        PLAY [Print os facts] **********************************************************************************************************************************************

        TASK [Gathering Facts] *********************************************************************************************************************************************
        ok: [localhost]
        ok: [ubuntu]
        ok: [centos7]

        TASK [Print OS] ****************************************************************************************************************************************************
        ok: [centos7] => {
        "msg": "CentOS"
        }
        ok: [ubuntu] => {
             "msg": "Ubuntu"
        }
        ok: [localhost] => {
             "msg": "Ubuntu"
        }

        TASK [Print fact] **************************************************************************************************************************************************
        ok: [centos7] => {
            "msg": "el default fact"
        }
        ok: [ubuntu] => {
            "msg": "deb default fact"
        }
        ok: [localhost] => {
            "msg": "all default fact"
        }

        PLAY RECAP *********************************************************************************************************************************************************
        centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
        localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
        ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
     


12. Заполнил `README1.md` ответами на вопросы. 


## Необязательная часть

1. При помощи `ansible-vault` расшифруем все зашифрованные файлы с переменными.

          root@ubuntu22:~/# ansible-vault decrypt group_vars/deb/examp.yml
          Vault password: 
          Decryption successful

          root@ubuntu22:~/# ansible-vault decrypt group_vars/el/examp.yml
          Vault password:
          Decryption successful

          root@ubuntu22:~/# cat group_vars/deb/examp.yml
          ---
          some_fact: "deb default fact"
          
          root@ubuntu22:~/# cat group_vars/el/examp.yml
          ---
          some_fact: "el default fact"


2. Зашифруем отдельное значение `PaSSw0rd` для переменной `some_fact` паролем `netology`. Добавляем полученное значение в `group_vars/all/exmp.yml`.

          root@ubuntu22:/# ansible-vault encrypt_string
          New Vault password:
          Confirm New Vault password:
          Reading plaintext input from stdin. (ctrl-d to end input, twice if your content does not already have a newline)
          PaSSw0rd
          Encryption successful
          !vault |
          $ANSIBLE_VAULT;1.1;AES256
          37643263646562636362623062333232626466343534323063306365613564663962636465333765
          6234663862326462333137343566636138323932376533370a383539646161323166333033343732
          36636266363133383230376266343762316132313239356238323663356437656332633264363066
          6163616235353966660a366630643634353833363532353434303339646139393435326461623737
          3438

          # cat group_vars/all/examp.yml
          ---
          some_fact: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          37643263646562636362623062333232626466343534323063306365613564663962636465333765
          6234663862326462333137343566636138323932376533370a383539646161323166333033343732
          36636266363133383230376266343762316132313239356238323663356437656332633264363066
          6163616235353966660a366630643634353833363532353434303339646139393435326461623737
          3438

3. Запускаем `playbook`, убеждаемся, что для нужных хостов применился новый `fact`.
        
        # ansible-playbook  -i inventory/prod.yml site.yml --ask-vault-pass
        Vault password:
 
        PLAY [Print os facts] **********************************************************************************************************************************************

        TASK [Gathering Facts] *********************************************************************************************************************************************
        ok: [localhost]
        ok: [ubuntu]
        ok: [centos7]

        TASK [Print OS] ****************************************************************************************************************************************************
        ok: [centos7] => {
        "msg": "CentOS"
        }
        ok: [ubuntu] => {
             "msg": "Ubuntu"
        }
        ok: [localhost] => {
             "msg": "Ubuntu"
        }

        TASK [Print fact] **************************************************************************************************************************************************
        ok: [centos7] => {
            "msg": "el default fact"
        }
        ok: [ubuntu] => {
            "msg": "deb default fact"
        }
        ok: [localhost] => {
            "msg": "PaSSw0rd"
        }

        PLAY RECAP *********************************************************************************************************************************************************
        centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
        localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
        ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

4. Добавьте новую группу хостов `fedora`, самостоятельно придумайте для неё переменную. 
   В качестве образа можно использовать [этот](https://hub.docker.com/r/pycontribs/fedora).

         root@docker:/#  docker run -dit --name fedora    pycontribs/fedora:latest  sleep 6000000
         root@docker:/#  docker ps -a
         CONTAINER ID   IMAGE                      COMMAND           CREATED              STATUS              PORTS     NAMES
         51eeea3312b6   pycontribs/fedora:latest   "sleep 6000000"   About a minute ago   Up About a minute             fed
         80f1d7019ea2   pycontribs/ubuntu:latest   "sleep 6000000"   2 hours ago          Up 2 hours                    ubuntu
         346ad5c71fe9   pycontribs/centos:7        "sleep 6000000"   2 hours ago          Up 2 hours                    centos7


         # ansible-playbook  -i inventory/prod.yml site.yml --ask-vault-pass
         Vault password:
         
         PLAY [Print os facts] **********************************************************************************************************************************************
         
         TASK [Gathering Facts] *********************************************************************************************************************************************
         ok: [localhost]
         ok: [ubuntu]
         ok: [fed]
         ok: [centos7]
         
         TASK [Print OS] ****************************************************************************************************************************************************
         ok: [centos7] => {
             "msg": "CentOS"
         }
         ok: [ubuntu] => {
             "msg": "Ubuntu"
         }
         ok: [fed] => {
             "msg": "Fedora"
         }
         ok: [localhost] => {
             "msg": "Ubuntu"
         }
         
         TASK [Print fact] **************************************************************************************************************************************************
         ok: [centos7] => {
             "msg": "el default fact"
         }
         ok: [ubuntu] => {
             "msg": "deb default fact"
         }
         ok: [fed] => {
             "msg": "fedora default fact"
         }
         ok: [localhost] => {
             "msg": "PaSSw0rd"
         }
         
         PLAY RECAP *********************************************************************************************************************************************************
         centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
         fed                        : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
         localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
         ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


