#!/usr/bin/env bash
export WORKDIR=`pwd`
export PYTHONUNBUFFERED="1"
export PYTHONPATH=${WORKDIR}
#export PYTHON3_HOME=/usr/local/python3.6
export PYTHON3_HOME=/home/hopson/apps/usr/webserver/dba/python3.6.0
export LD_LIBRARY_PATH=${PYTHON3_HOME}/lib
${PYTHON3_HOME}/bin/python3  -u ${WORKDIR}/web/task/run_task.py &>>task.log &
