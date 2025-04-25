#!/usr/bin/env bash
export WORKDIR="/home/hopson/apps/usr/webserver/dbops"
export PYTHONUNBUFFERED="1"
export PYTHONPATH=${WORKDIR}
export PYTHON3_HOME=/usr/local/python3.6
export LD_LIBRARY_PATH=${PYTHON3_HOME}/lib

echo "Testing dbops Server..."
for i in {8201..8206}
do
    if [ `ps -ef |grep dbops | grep -v grep | grep ${i} | wc -l` == '0' ]
    then
      cd ${WORKDIR} &&  ${PYTHON3_HOME}/bin/python3 -u ${WORKDIR}/web/controller/server.py ${i} &>> ${WORKDIR}/logs/server_${i}.log &
      echo "Startup dbops server ${i} ...ok"
    fi
done
echo "Testing dbops Server...ok"


if [ `ps -ef |grep nginx | wc -l` == '0' ]
then
      sudo nginx &
      echo "Startup nginx server...ok"
fi
