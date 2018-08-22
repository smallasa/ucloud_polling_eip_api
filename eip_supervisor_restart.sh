#!/bin/bash

for i in $(supervisorctl status|awk '{print $1}');do
  echo -e "supervisorctl restart $i && sleep ${RANDOM:1:1} && \c"
done
