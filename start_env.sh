#!/usr/bin/env bash
export WORKDIR=`pwd`
export PYTHONUNBUFFERED="1"
export PYTHONPATH=${WORKDIR}
export PYTHON3_HOME=/usr/local/python3.6
export LD_LIBRARY_PATH=${PYTHON3_HOME}/lib
echo "Starting dbops Server..."
for i in {8201..8210}
do
  if [ `ps -ef |grep dbops | grep ${i} | wc -l` == '1' ]
  then
     echo "dbops Server ${i} already running..."
  else
     ${PYTHON3_HOME}/bin/python3 -u ${WORKDIR}/web/controller/server.py ${i} &>/dev/null &
  fi
done
echo "Starting dbops Server...ok"
