#!/usr/bin/env bash
export WORKDIR=`pwd`
export PYTHONUNBUFFERED="1"
export PYTHONPATH=${WORKDIR}
echo "Starting schedule task Server..."

if [ `ps -ef |grep schedule | grep -v grep | wc -l` == '1' ]
then
   echo "schedule Server already running..."
else
   python3 -u ${WORKDIR}/web/task/schedule.py &>/dev/null &
fi

echo "Starting schedule Server...ok"
