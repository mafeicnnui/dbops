#!/usr/bin/env bash
export WORKDIR=`pwd`
export PYTHONUNBUFFERED="1"
export PYTHONPATH=${WORKDIR}
#export PYTHON3_HOME=/usr/local/python3.6
export PYTHON3_HOME=/home/hopson/apps/usr/webserver/dba/python3.6.0

export LD_LIBRARY_PATH=${PYTHON3_HOME}/lib
echo "Starting schedule_multi task Server..."

if [ `ps -ef |grep schedule | grep -v grep | wc -l` == '1' ]
then
   echo "schedule Server ${i} already running..."
else
   ${PYTHON3_HOME}/bin/python3 -u ${WORKDIR}/web/task/schedule_multi.py &>/dev/null &
fi

echo "Starting schedule_multi Server...ok"
