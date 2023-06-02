数据库脚本创建步骤


一、切换数据库

    CREATE DATABASE `puppet` default CHARACTER SET utf8mb4;
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

    mysql 5.6/5.7:                    
     grant all privileges on *.* to 'puppet'@'%' identified by 'Puppet@123'    
     
    mysql 8.0:
     create user 'puppet'@'%' identified by 'Puppet@123';
     grant all privileges on *.* to 'puppet'@'%';
   

五、定时任务
                        
    */1 * * * *  /dbops/crontab/proc_tj_service.sh &>>/tmp/proc_tj_service.log 
    */2 * * * *  /dbops/crontab/proc_tj_sync_monitor.sh &>>/tmp/proc_tj_sync_monitor.log
    0 */1 * * *  /dbops/crontab/proc_clear_log.sh &>>/tmp/proc_clear_log.log
    0 0 15 * *   /dbops/crontab/proc_trunc_log.sh &>>/tmp/proc_trunc_log.log
 
六、执行SQL

    cd dbops/sql
    mysql -uroot -p123456 -h10.16.44.89 -e 'create database if not exists `puppet` default character set utf8mb4'
    mysql -uroot -p123456 -h10.16.44.89 puppet < table/cre_tab.sql
    mysql -uroot -p123456 -h10.16.44.89 puppet < view/cre_view.sql
    mysql -uroot -p123456 -h10.16.44.89 puppet < proc/proc_clear_log.sql
    mysql -uroot -p123456 -h10.16.44.89 puppet < proc/proc_tj_service.sql
    mysql -uroot -p123456 -h10.16.44.89 puppet < proc/proc_tj_sync_monitor.sql
    mysql -uroot -p123456 -h10.16.44.89 puppet < proc/proc_trunc_log.sql
    mysql -uroot -p123456 -h10.16.44.89 puppet < data/initialize.sql
   