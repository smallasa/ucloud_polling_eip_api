#!/bin/bash

cat > /etc/supervisord.d/eip_polling_release_unbind.ini <<EOF
[program:eip_polling_release_unbind]
directory=/root/ucloud-sdk-python
command=/usr/local/pyenv/shims/python eip_polling_release_unbind.py
process_name=%(program_name)s
numprocs=1
user=root
autorstart=true
autorestart=true
stdout_logfile=/var/log/supervisor/eip_polling_release_unbind.log
EOF