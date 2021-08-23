数据库脚本创建步骤

一、切换数据库

    use puppet
    
二、创建表

    .\sql\tab\archive\cre_tab.sql
    .\sql\tab\backup\cre_tab.sql
    .\sql\tab\database\cre_tab.sql
    .\sql\tab\datax\cre_tab.sql
    .\sql\tab\dbsource\cre_tab.sql
    .\sql\tab\func\cre_tab.sql
    .\sql\tab\kpi\cre_tab.sql
    .\sql\tab\menu\cre_tab.sql
    .\sql\tab\minio\cre_tab.sql
    .\sql\tab\monitor\cre_tab.sql
    .\sql\tab\order\cre_tab.sql
    .\sql\tab\port\cre_tab.sql
    .\sql\tab\public\cre_tab.sql
    .\sql\tab\role\cre_tab.sql
    .\sql\tab\server\cre_tab.sql
    .\sql\tab\slowlog\cre_tab.sql
    .\sql\tab\syncer\cre_tab.sql
    .\sql\tab\transfer\cre_tab.sql
    .\sql\tab\user\cre_tab.sql
    .\sql\tab\weekly\cre_tab.sql
                       
二、创建视图
                       
    .\sql\view\cre_view.sql
                    
 二、创建过程
                        
     .\sql\proc\proc_clear_log.sql
     .\sql\proc\proc_tj_service.sql
     .\sql\proc\proc_tj_sync_monitor.sql
     .\sql\proc\proc_trunc_log.sql
                         
                        