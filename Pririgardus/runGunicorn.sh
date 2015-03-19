#!/bin/bash

iptables -I INPUT -p tcp --dport 5000 -j ACCEPT;
fuser -k 5000/tcp;
python gunicorn -w 2 -b 192.168.1.112:5000 pririgardus:app ;

