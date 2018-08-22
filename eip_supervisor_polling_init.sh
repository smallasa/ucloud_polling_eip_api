#!/bin/bash

IPADDR=$1
IPID=$2

cat > /etc/supervisord.d/${IPADDR}.ini <<EOF
[program:$IPADDR]
directory=/root/ucloud-sdk-python
command=/usr/local/pyenv/shims/python eip_uhost_polling.py --uhost-id $IPID --uhost-ip $IPADDR --time 600
process_name=%(program_name)s
numprocs=1
user=root
autorstart=true
autorestart=true
stdout_logfile=/var/log/supervisor/${IPADDR}.log
EOF
