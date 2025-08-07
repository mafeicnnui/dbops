/*
SQLyog Ultimate v12.08 (64 bit)
MySQL - 5.6.44-log : Database - puppet
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
/*Table structure for table `v_db_compare` */

DROP TABLE IF EXISTS `v_db_compare`;

/*!50001 CREATE TABLE  `v_db_compare`(
 `id` int(11) ,
 `dsid` int(11) ,
 `table_schema` varchar(64) ,
 `table_name` varchar(64) ,
 `column_name` varchar(64) ,
 `is_nullable` varchar(3) ,
 `data_type` varchar(64) ,
 `column_default` longtext ,
 `character_maximum_length` varchar(50) ,
 `numeric_precision` varchar(50) ,
 `character_set_name` varchar(100) ,
 `collation_name` varchar(100) ,
 `column_type` longtext ,
 `column_key` varchar(3) ,
 `extra` mediumtext ,
 `column_comment` longtext 
)*/;

/*Table structure for table `v_db_compare_idx` */

DROP TABLE IF EXISTS `v_db_compare_idx`;

/*!50001 CREATE TABLE  `v_db_compare_idx`(
 `dsid` int(11) ,
 `table_schema` varchar(100) ,
 `table_name` varchar(100) ,
 `index_name` varchar(100) ,
 `index_type` varchar(100) ,
 `is_unique` varchar(100) ,
 `nullable` varchar(100) ,
 `visible` varchar(100) ,
 `column_name` text 
)*/;

/*Table structure for table `v_kpi_bbtj` */

DROP TABLE IF EXISTS `v_kpi_bbtj`;

/*!50001 CREATE TABLE  `v_kpi_bbtj`(
 `id` int(11) ,
 `bbrq` date ,
 `market_id` varchar(200) ,
 `market_name` varchar(100) ,
 `item_name` varchar(100) ,
 `item_month_value` varchar(100) ,
 `item_finish_value` varchar(100) ,
 `create_time` varchar(24) 
)*/;

/*Table structure for table `v_monitor_service` */

DROP TABLE IF EXISTS `v_monitor_service`;

/*!50001 CREATE TABLE  `v_monitor_service`(
 `server_id` int(11) ,
 `server_desc` text ,
 `service_service` text ,
 `flag` varchar(10) 
)*/;

/*Table structure for table `v_week_last` */

DROP TABLE IF EXISTS `v_week_last`;

/*!50001 CREATE TABLE  `v_week_last`(
 `id` bigint(20) ,
 `rq` date 
)*/;

/*Table structure for table `v_week_this` */

DROP TABLE IF EXISTS `v_week_this`;

/*!50001 CREATE TABLE  `v_week_this`(
 `id` bigint(20) ,
 `rq` date 
)*/;

/*View structure for view v_db_compare */

/*!50001 DROP TABLE IF EXISTS `v_db_compare` */;
/*!50001 CREATE ALGORITHM=UNDEFINED DEFINER=`puppet`@`%` SQL SECURITY DEFINER VIEW `v_db_compare` AS select `t_db_compare`.`id` AS `id`,`t_db_compare`.`dsid` AS `dsid`,`t_db_compare`.`table_schema` AS `table_schema`,`t_db_compare`.`table_name` AS `table_name`,`t_db_compare`.`column_name` AS `column_name`,`t_db_compare`.`is_nullable` AS `is_nullable`,`t_db_compare`.`data_type` AS `data_type`,`t_db_compare`.`column_default` AS `column_default`,`t_db_compare`.`character_maximum_length` AS `character_maximum_length`,`t_db_compare`.`numeric_precision` AS `numeric_precision`,`t_db_compare`.`character_set_name` AS `character_set_name`,`t_db_compare`.`collation_name` AS `collation_name`,`t_db_compare`.`column_type` AS `column_type`,`t_db_compare`.`column_key` AS `column_key`,replace(`t_db_compare`.`extra`,'DEFAULT_GENERATED ','') AS `extra`,`t_db_compare`.`column_comment` AS `column_comment` from `t_db_compare` */;

/*View structure for view v_db_compare_idx */

/*!50001 DROP TABLE IF EXISTS `v_db_compare_idx` */;
/*!50001 CREATE ALGORITHM=UNDEFINED DEFINER=`puppet`@`%` SQL SECURITY DEFINER VIEW `v_db_compare_idx` AS select `t_db_compare_idx`.`dsid` AS `dsid`,`t_db_compare_idx`.`table_schema` AS `table_schema`,`t_db_compare_idx`.`table_name` AS `table_name`,`t_db_compare_idx`.`index_name` AS `index_name`,`t_db_compare_idx`.`index_type` AS `index_type`,`t_db_compare_idx`.`is_unique` AS `is_unique`,`t_db_compare_idx`.`nullable` AS `nullable`,ifnull(`t_db_compare_idx`.`visible`,'') AS `visible`,group_concat('`',`t_db_compare_idx`.`column_name`,'`' separator ',') AS `column_name` from `t_db_compare_idx` group by `t_db_compare_idx`.`dsid`,`t_db_compare_idx`.`table_schema`,`t_db_compare_idx`.`table_name`,`t_db_compare_idx`.`index_name`,`t_db_compare_idx`.`index_type`,`t_db_compare_idx`.`is_unique`,`t_db_compare_idx`.`nullable`,`t_db_compare_idx`.`visible` */;

/*View structure for view v_kpi_bbtj */

/*!50001 DROP TABLE IF EXISTS `v_kpi_bbtj` */;
/*!50001 CREATE ALGORITHM=UNDEFINED DEFINER=`kpi`@`%` SQL SECURITY DEFINER VIEW `v_kpi_bbtj` AS select `a`.`id` AS `id`,`a`.`bbrq` AS `bbrq`,`a`.`market_id` AS `market_id`,`a`.`market_name` AS `market_name`,`a`.`item_name` AS `item_name`,(select `x`.`item_value` from `t_kpi_item_value` `x` where ((`x`.`item_month` = convert(substr(`a`.`bbrq`,1,7) using utf8mb4)) and (`x`.`market_name` = `a`.`market_name`) and (`x`.`item_name` = `a`.`item_name`))) AS `item_month_value`,`a`.`item_value` AS `item_finish_value`,date_format(`a`.`create_time`,'%Y-%m-%d %H:%i:%s') AS `create_time` from `t_kpi_bbtj` `a` where ((`a`.`item_name` in ('GMV（万）','会员销售占比','上线SPU数量（个）','POS GMV（万）','会员运营GMV（万）','商城+本地生活GMV（万）','数字账单GMV（万）','物业增值GMV（万）','数字支付GMV（万）','会员拉新人数（人）','累计注册用户数（万个）','会员销售占比（%）','商户线上活动参与率（%）','积分商城SKU入驻数量','线上商城SKU上传数量指标达成(个)')) and (`a`.`market_name` not in ('直管区域','上海区域','广州区域','商业事业部'))) order by `a`.`id` */;

/*View structure for view v_monitor_service */

/*!50001 DROP TABLE IF EXISTS `v_monitor_service` */;
/*!50001 CREATE ALGORITHM=UNDEFINED DEFINER=`puppet`@`%` SQL SECURITY DEFINER VIEW `v_monitor_service` AS select `t_monitor_service`.`server_id` AS `server_id`,`t_monitor_service`.`server_desc` AS `server_desc`,`t_monitor_service`.`mysql_proj` AS `service_service`,'mysql' AS `flag` from `t_monitor_service` where (`t_monitor_service`.`mysql_proj` <> '') union all select `t_monitor_service`.`server_id` AS `server_id`,`t_monitor_service`.`server_desc` AS `server_desc`,`t_monitor_service`.`mssql_park` AS `mssql_park`,'mssql_park' AS `flag` from `t_monitor_service` where (`t_monitor_service`.`mssql_park` <> '') union all select `t_monitor_service`.`server_id` AS `server_id`,`t_monitor_service`.`server_desc` AS `server_desc`,`t_monitor_service`.`mssql_flow` AS `mssql_flow`,'mssql_flow' AS `flag` from `t_monitor_service` where (`t_monitor_service`.`mssql_flow` <> '') union all select `t_monitor_service`.`server_id` AS `server_id`,`t_monitor_service`.`server_desc` AS `server_desc`,`t_monitor_service`.`mssql_car` AS `mssql_car`,'mssql_car' AS `flag` from `t_monitor_service` where (`t_monitor_service`.`mssql_car` <> '') union all select `t_monitor_service`.`server_id` AS `server_id`,`t_monitor_service`.`server_desc` AS `server_desc`,`t_monitor_service`.`redis` AS `redis`,'redis' AS `flag` from `t_monitor_service` where (`t_monitor_service`.`redis` <> '') union all select `t_monitor_service`.`server_id` AS `server_id`,`t_monitor_service`.`server_desc` AS `server_desc`,`t_monitor_service`.`mongo` AS `mongo`,'mongo' AS `flag` from `t_monitor_service` where (`t_monitor_service`.`mongo` <> '') union all select `t_monitor_service`.`server_id` AS `server_id`,`t_monitor_service`.`server_desc` AS `server_desc`,`t_monitor_service`.`es` AS `es`,'es' AS `flag` from `t_monitor_service` where (`t_monitor_service`.`es` <> '') order by `server_id` */;

/*View structure for view v_week_last */

/*!50001 DROP TABLE IF EXISTS `v_week_last` */;
/*!50001 CREATE ALGORITHM=UNDEFINED DEFINER=`puppet`@`%` SQL SECURITY DEFINER VIEW `v_week_last` AS select 1 AS `id`,(curdate() - interval (weekday(curdate()) + 7) day) AS `rq` union select 2 AS `2`,(curdate() - interval (weekday(curdate()) + 6) day) AS `DATE_SUB(CURDATE(),INTERVAL WEEKDAY(CURDATE())+6 DAY)` union select 3 AS `3`,(curdate() - interval (weekday(curdate()) + 5) day) AS `DATE_SUB(CURDATE(),INTERVAL WEEKDAY(CURDATE())+5 DAY)` union select 4 AS `4`,(curdate() - interval (weekday(curdate()) + 4) day) AS `DATE_SUB(CURDATE(),INTERVAL WEEKDAY(CURDATE())+4 DAY)` union select 5 AS `5`,(curdate() - interval (weekday(curdate()) + 3) day) AS `DATE_SUB(CURDATE(),INTERVAL WEEKDAY(CURDATE())+3 DAY)` union select 6 AS `6`,(curdate() - interval (weekday(curdate()) + 2) day) AS `DATE_SUB(CURDATE(),INTERVAL WEEKDAY(CURDATE())+2 DAY)` union select 7 AS `7`,(curdate() - interval (weekday(curdate()) + 1) day) AS `DATE_SUB(CURDATE(),INTERVAL WEEKDAY(CURDATE())+1 DAY)` */;

/*View structure for view v_week_this */

/*!50001 DROP TABLE IF EXISTS `v_week_this` */;
/*!50001 CREATE ALGORITHM=UNDEFINED DEFINER=`puppet`@`%` SQL SECURITY DEFINER VIEW `v_week_this` AS select 1 AS `id`,(curdate() - interval (weekday(curdate()) + 0) day) AS `rq` union select 2 AS `2`,(curdate() - interval (weekday(curdate()) - 1) day) AS `DATE_SUB(CURDATE(),INTERVAL WEEKDAY(CURDATE())-1 DAY)` union select 3 AS `3`,(curdate() - interval (weekday(curdate()) - 2) day) AS `DATE_SUB(CURDATE(),INTERVAL WEEKDAY(CURDATE())-2 DAY)` union select 4 AS `4`,(curdate() - interval (weekday(curdate()) - 3) day) AS `DATE_SUB(CURDATE(),INTERVAL WEEKDAY(CURDATE())-3 DAY)` union select 5 AS `5`,(curdate() - interval (weekday(curdate()) - 4) day) AS `DATE_SUB(CURDATE(),INTERVAL WEEKDAY(CURDATE())-4 DAY)` union select 6 AS `6`,(curdate() - interval (weekday(curdate()) - 5) day) AS `DATE_SUB(CURDATE(),INTERVAL WEEKDAY(CURDATE())-5 DAY)` union select 7 AS `7`,(curdate() - interval (weekday(curdate()) - 6) day) AS `DATE_SUB(CURDATE(),INTERVAL WEEKDAY(CURDATE())-6 DAY)` */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
