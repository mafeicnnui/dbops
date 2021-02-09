#!/usr/bin/env bash
echo "Stopping dbops Server..."
for i in {8201..8210}
do
 if [ `ps -ef |grep dbops | grep -v grep | grep ${i} | wc -l` == '1' ]
 then
    ps -ef |grep dbops | grep ${i} | awk '{print $2}' | xargs kill -9
 fi
done
echo "Stopping dbops Server...ok"