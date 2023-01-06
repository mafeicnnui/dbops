数据库脚本创建步骤


一、切换数据库

    use puppet
    
二、创建表

    .\table\cre_tab.sql
                           
二、创建视图
                       
    .\sql\view\cre_view.sql
                    
三、创建过程
                        
    .\sql\proc\proc_clear_log.sql
    .\sql\proc\proc_tj_service.sql
    .\sql\proc\proc_tj_sync_monitor.sql
    .\sql\proc\proc_trunc_log.sql
                         
四、初始化数据
                        
    .\sql\data\initialize.sql

四、创建账号
                        
    grant all privileges on *.* to 'puppet'@'%' identified by 'Puppet@123'    


五、定时任务
                        
    */1 * * * *  /dbops/crontab/proc_tj_service.sh &>>/tmp/proc_tj_service.log 
    */2 * * * *  /dbops/crontab/proc_tj_sync_monitor.sh &>>/tmp/proc_tj_sync_monitor.log
    0 */1 * * *  /dbops/crontab/proc_clear_log.sh &>>/tmp/proc_clear_log.log
    0 0 15 * *   /dbops/crontab/proc_trunc_log.sh &>>/tmp/proc_trunc_log.log
 
