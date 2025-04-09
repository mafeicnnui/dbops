#!/usr/bin/env bash
export WORKDIR=`pwd`
export PYTHONUNBUFFERED="1"
export PYTHONPATH=${WORKDIR}
export PYTHON3_HOME=/home/hopson/apps/usr/webserver/dba/python3.6.8
export LD_LIBRARY_PATH=${PYTHON3_HOME}/lib
echo "Starting dbops Server..."
for i in {8201..8206}
do
  if [ `ps -ef |grep dbops | grep ${i} | wc -l` == '1' ]
  then
     echo "dbops Server ${i} already running..."
  else
     ${PYTHON3_HOME}/bin/python3 -u ${WORKDIR}/web/controller/server.py ${i} &>/dev/null &
  fi
  echo "Starting dbops Server...ok"
done

if [ `ps -ef |grep run_db_task | grep -v grep | wc -l` == '0' ]
then
   echo run_db_task running success...
   ${PYTHON3_HOME}/bin/python3 -u ${WORKDIR}/web/task/run_db_task.py &>/dev/null &
else
   echo run_db_task already running...
fi

if [ `ps -ef |grep run_sql_task | grep -v grep | wc -l` == '0' ]
then
  echo run_sql_task running success...
  ${PYTHON3_HOME}/bin/python3 -u ${WORKDIR}/web/task/run_sql_task.py &>/dev/null &
else
   echo run_sql_task already running...
fi

if [ `ps -ef |grep run_sql_timer | grep -v grep | wc -l` == '0' ]
then
  echo run_sql_timer running success...
  ${PYTHON3_HOME}/bin/python3 -u ${WORKDIR}/web/task/run_sql_timer.py &>/dev/null &
else
   echo run_sql_timer already running...
fi