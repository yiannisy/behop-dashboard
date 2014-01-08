#!/bin/bash

#Gets list of client from phpliteadmin and transfers them to DashBoard
sqlite3 /home/yiannis/be-hop-misc/utils/nodeDB.sqlite "select ip_addr,addr,type,OS,username,bands from active_nodes" > /tmp/clients_all.txt
sed -i 's/5GHz,2.4GHz/2.4GHz,5GHz/g' /tmp/clients_all.txt
sed -i 's/2.4GHz,5GHz/1,1/g' /tmp/clients_all.txt
sed -i 's/2.4GHz/1,0/g' /tmp/clients_all.txt
sed -i 's/5GHz/0,1/g' /tmp/clients_all.txt
sed -i 's/|/,/g' /tmp/clients_all.txt
sed -i '1iip_address,mac_address,type,os,user,bands_2GHz,bands_5GHz,' /tmp/clients_all.txt
python manage.py csvimport --mappings='' --model='logs.Client' /tmp/clients_all.txt