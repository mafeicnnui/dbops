#!/usr/bin/env bash
export WORKDIR="/home/hopson/apps/usr/webserver/dbops"
export PYTHONUNBUFFERED="1"
export PYTHONPATH=${WORKDIR}
echo "Testing dbops Server..."
for i in {8201..8210}
do
    if [ `ps -ef |grep dbops | grep -v grep | grep ${i} | wc -l` == '0' ]
    then
      cd ${WORKDIR} && python3 -u ${WORKDIR}/web/controller/server.py ${i} &>/dev/null &
      echo "Startup dbops server ${i} ...ok"
    fi
done
echo "Testing dbops Server...ok"


if [ `ps -ef |grep nginx  | grep -v grep | wc -l` == '0' ]
then
      sudo nginx &
      echo "Startup nginx server...ok"
fi