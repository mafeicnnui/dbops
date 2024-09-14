export MYSQL_HOME=/usr/local/mysql5.6
export PATH=${MYSQL_HOME}/bin:$PATH
mysql -upuppet -pPuppet@123 -h10.2.39.59 -P3306 puppet -e "call proc_trunc_log();"
