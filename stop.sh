#!/usr/bin/env bash
echo "Stopping dbops Server..."
for i in {8201..8210}
do
 if [ `ps -ef |grep dbops | grep -v grep | grep ${i} | wc -l` == '1' ]
 then
    ps -ef |grep dbops | awk '{print $2}' | xargs kill -9
 fi
 echo "Stopping dbops Server...ok"
done

echo "Stopping run_db_task Server...ok"

if [ `ps -ef |grep dbops | grep -v grep | grep run_db_task | wc -l` == '1' ]
then
    ps -ef |grep dbops | grep -v grep | grep run_db_task | awk '{print $2}' | xargs kill -9
fi

echo "Stopping run_sql_task Server...ok"
if [ `ps -ef |grep dbops | grep -v grep | grep run_sql_task | wc -l` -gt '1' ]
then
    ps -ef |grep dbops | grep -v grep | grep run_sql_task | awk '{print $2}' | xargs kill -9
fi

echo "Stopping run_sql_task run_sql_timer...ok"
if [ `ps -ef |grep dbops | grep -v grep | grep run_sql_timer | wc -l` == '1' ]
then
    ps -ef |grep dbops | grep -v grep | grep run_sql_timer| awk '{print $2}' | xargs kill -9
fi

echo "Stopping webssh ...ok"
if [ `ps -ef |grep dbops | grep -v grep | grep webssh | wc -l` == '1' ]
then
    ps -ef |grep dbops | grep -v grep | grep webssh| awk '{print $2}' | xargs kill -9
fi
