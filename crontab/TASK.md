#### EaseBase 统计数据库实例监控状态
*/5 * * * *  /home/hopson/apps/usr/webserver/dba/crontab/proc_tj_service.sh &>>/tmp/proc_tj_service.log 

#### EaseBase 统计各项目数据库同步任务状态
*/5 * * * *  /home/hopson/apps/usr/webserver/dba/crontab/proc_tj_sync_monitor.sh &>>/tmp/proc_tj_sync_monitor.log

#### EaseBase 删除日志表日志
0 */1 * * *  /home/hopson/apps/usr/webserver/dba/crontab/proc_clear_log.sh &>>/tmp/proc_clear_log.log

#### EaseBase 日志表定时清空
0 0 * * 6    /home/hopson/apps/usr/webserver/dba/crontab/proc_trunc_log.sh &>>/tmp/proc_trunc_log.log

#### EaseBase 数据库服务监控
*/3 6-23 * * * /home/hopson/apps/usr/webserver/dba/syncer/dba_monitor/webchat.sh

#### EaseBase 数据库服务器监控
*/3 * * * * /home/hopson/apps/usr/webserver/dba/syncer/dba_monitor/webchat2.sh

