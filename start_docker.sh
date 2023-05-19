#!/usr/bin/env bash
export WORKDIR='/opt/dbops'
export PYTHONUNBUFFERED="1"
export PYTHONPATH=${WORKDIR}
echo "Starting dbops Server..."
for i in {8080..8080}
do
  if [ `ps -ef |grep dbops | grep -v grep | grep ${i} | wc -l` == '1' ]
  then
     echo "dbops Server ${i} already running..."
  else
     python3 -u ${WORKDIR}/web/controller/server.py ${i}
  fi
done
echo "Starting dbops Server...ok"
