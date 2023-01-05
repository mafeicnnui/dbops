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
   