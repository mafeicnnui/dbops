insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (1,'cpu使用率','cpu_total_usage','1','','1','0.85','','','1',10,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (2,'内存使用率','mem_usage','1','','1','0.85','','','1',10,2);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (5,'mysql连接数','mysql_total_connect','2','0','1','300','','','1',10,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (26,'磁盘使用率','disk_usage','1','','1','0.8','','','1',10,1);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (28,'磁盘读','disk_read','1','','2','','7','3','1',10,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (29,'磁盘写','disk_write','1','','2','','7','3','1',10,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (31,'网络流出','net_out','1','','2','','7','3','1',9,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (32,'网络流入','net_in','1','','2','','7','3','1',10,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (33,'mysql服务是否可用','mysql_available','2','0','3','0','','','1',5,1);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (34,'mysql活动连接数','mysql_active_connect','2','0','3','100','','','1',9,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (37,'mssql服务是否可用','mssql_available','2','2','3','0','','','1',5,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (38,'CPU使用率[核]','cpu_core_usage','1','','1','0.86','','','1',10,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (39,'mssql连接数','mssql_total_connect','2','2','3','300','','','1',10,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (40,'mssql活动连接数','mssql_active_connect','2','2','3','30','','','1',10,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (41,'redis服务是否可用','redis_available','2','5','3','0','','','1',5,1);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (42,'mongo服务是否可用','mongo_available','2','6','3','0','','','1',5,1);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (43,'es服务是否可用','es_available','2','4','3','0','','','1',5,1);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (46,'服务器可用性','server_available','1','','3','0','','','0',3,1);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (47,'oracle连接数','oracle_total_connect','2','1','1','200','','','1',10,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (48,'oracle服务是否可用','oracle_available','2','1','3','0','','','1',10,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (49,'oracle活跃连接数','oracle_active_connect','2','1','3','100','','','1',10,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (51,'oracle表空间使用率','oracle_tablespace','2','1','1','80','','','1',10,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (54,'mysql每秒查询率','mysql_qps','2','0','3','1000','','','1',10,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (55,'mysql每秒事务数','mysql_tps','2','0','3','1000','','','1',10,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (56,'oracle每秒查询率','oracle_qps','2','1','3','100','','','1',10,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (58,'oracle每秒事务数','oracle_tps','2','1','3','100','','','1',10,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (61,'mssql每秒查询率','mssql_qps','2','2','1','100','','','1',10,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (63,'mssql每秒事务数','mssql_tps','2','2','3','100','','','1',10,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (66,'mongo总连接数','mongo_total_connect','2','6','3','10000','','','1',10,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (68,'mongo活动连接数','mongo_active_connect','2','6','3','300','','','1',10,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (69,'mongo每秒事务数','mongo_tps','2','6','3','100','','','1',10,3);
insert  into `t_monitor_index`(`id`,`index_name`,`index_code`,`index_type`,`index_db_type`,`index_threshold_type`,`index_threshold`,`index_threshold_day`,`index_threshold_times`,`status`,`trigger_time`,`trigger_times`) values (72,'mongo每秒查询率','mongo_qps','2','6','3','100','','','1',10,3);