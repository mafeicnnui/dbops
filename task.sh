#!/usr/bin/env bash
export WORKDIR=`pwd`
export PYTHONUNBUFFERED="1"
export PYTHONPATH=${WORKDIR}
python3  -u ${WORKDIR}/web/task/run_task.py &>>task.log &
