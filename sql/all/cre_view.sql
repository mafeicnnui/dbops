/*
SQLyog Ultimate v11.24 (64 bit)
MySQL - 5.6.44-log : Database - puppet
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`puppet` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `puppet`;

/*Table structure for table `v_db_compare_idx` */

DROP TABLE IF EXISTS `v_db_compare_idx`;

/*!50001 DROP VIEW IF EXISTS `v_db_compare_idx` */;
/*!50001 DROP TABLE IF EXISTS `v_db_compare_idx` */;

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

/*Table structure for table `v_monitor_service` */

DROP TABLE IF EXISTS `v_monitor_service`;

/*!50001 DROP VIEW IF EXISTS `v_monitor_service` */;
/*!50001 DROP TABLE IF EXISTS `v_monitor_service` */;

/*!50001 CREATE TABLE  `v_monitor_service`(
 `server_id` int(11) ,
 `server_desc` text ,
 `service_service` text ,
 `flag` varchar(10) 
)*/;

/*View structure for view v_db_compare_idx */

/*!50001 DROP TABLE IF EXISTS `v_db_compare_idx` */;
/*!50001 DROP VIEW IF EXISTS `v_db_compare_idx` */;

/*!50001 CREATE ALGORITHM=UNDEFINED DEFINER=`puppet`@`%` SQL SECURITY DEFINER VIEW `v_db_compare_idx` AS select `t_db_compare_idx`.`dsid` AS `dsid`,`t_db_compare_idx`.`table_schema` AS `table_schema`,`t_db_compare_idx`.`table_name` AS `table_name`,`t_db_compare_idx`.`index_name` AS `index_name`,`t_db_compare_idx`.`index_type` AS `index_type`,`t_db_compare_idx`.`is_unique` AS `is_unique`,`t_db_compare_idx`.`nullable` AS `nullable`,ifnull(`t_db_compare_idx`.`visible`,'') AS `visible`,group_concat(`t_db_compare_idx`.`column_name` separator ',') AS `column_name` from `t_db_compare_idx` group by `t_db_compare_idx`.`dsid`,`t_db_compare_idx`.`table_schema`,`t_db_compare_idx`.`table_name`,`t_db_compare_idx`.`index_name`,`t_db_compare_idx`.`index_type`,`t_db_compare_idx`.`is_unique`,`t_db_compare_idx`.`nullable`,`t_db_compare_idx`.`visible` */;

/*View structure for view v_monitor_service */

/*!50001 DROP TABLE IF EXISTS `v_monitor_service` */;
/*!50001 DROP VIEW IF EXISTS `v_monitor_service` */;

/*!50001 CREATE ALGORITHM=UNDEFINED DEFINER=`puppet`@`%` SQL SECURITY DEFINER VIEW `v_monitor_service` AS select `t_monitor_service`.`server_id` AS `server_id`,`t_monitor_service`.`server_desc` AS `server_desc`,`t_monitor_service`.`mysql_proj` AS `service_service`,'mysql' AS `flag` from `t_monitor_service` where (`t_monitor_service`.`mysql_proj` <> '') union all select `t_monitor_service`.`server_id` AS `server_id`,`t_monitor_service`.`server_desc` AS `server_desc`,`t_monitor_service`.`mssql_park` AS `mssql_park`,'mssql_park' AS `flag` from `t_monitor_service` where (`t_monitor_service`.`mssql_park` <> '') union all select `t_monitor_service`.`server_id` AS `server_id`,`t_monitor_service`.`server_desc` AS `server_desc`,`t_monitor_service`.`mssql_flow` AS `mssql_flow`,'mssql_flow' AS `flag` from `t_monitor_service` where (`t_monitor_service`.`mssql_flow` <> '') union all select `t_monitor_service`.`server_id` AS `server_id`,`t_monitor_service`.`server_desc` AS `server_desc`,`t_monitor_service`.`mssql_car` AS `mssql_car`,'mssql_car' AS `flag` from `t_monitor_service` where (`t_monitor_service`.`mssql_car` <> '') union all select `t_monitor_service`.`server_id` AS `server_id`,`t_monitor_service`.`server_desc` AS `server_desc`,`t_monitor_service`.`redis` AS `redis`,'redis' AS `flag` from `t_monitor_service` where (`t_monitor_service`.`redis` <> '') union all select `t_monitor_service`.`server_id` AS `server_id`,`t_monitor_service`.`server_desc` AS `server_desc`,`t_monitor_service`.`mongo` AS `mongo`,'mongo' AS `flag` from `t_monitor_service` where (`t_monitor_service`.`mongo` <> '') union all select `t_monitor_service`.`server_id` AS `server_id`,`t_monitor_service`.`server_desc` AS `server_desc`,`t_monitor_service`.`es` AS `es`,'es' AS `flag` from `t_monitor_service` where (`t_monitor_service`.`es` <> '') order by `server_id` */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
