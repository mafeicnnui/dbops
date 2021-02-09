/*
SQLyog Ultimate v11.24 (64 bit)
MySQL - 5.6.44-log : Database - puppet
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
USE `puppet`;

/*Table structure for table `t_datax_sync_config` */

DROP TABLE IF EXISTS `t_datax_sync_config`;

CREATE TABLE `t_datax_sync_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sync_tag` varchar(100) DEFAULT NULL,
  `server_id` int(11) DEFAULT NULL,
  `sour_db_id` int(11) DEFAULT NULL,
  `sync_schema` varchar(100) DEFAULT NULL,
  `sync_table` varchar(2000) DEFAULT NULL,
  `sync_columns` varchar(2000) DEFAULT NULL,
  `sync_incr_col` varchar(50) DEFAULT NULL,
  `sync_incr_where` varchar(1000) DEFAULT NULL,
  `zk_hosts` varchar(100) DEFAULT NULL,
  `hbase_thrift` varchar(100) DEFAULT NULL,
  `sync_hbase_table` varchar(100) DEFAULT NULL,
  `sync_hbase_rowkey` text,
  `sync_hbase_rowkey_sour` varchar(50) DEFAULT NULL,
  `sync_hbase_columns` text,
  `sync_hbase_rowkey_separator` varchar(10) DEFAULT NULL,
  `sync_ywlx` varchar(11) DEFAULT NULL,
  `sync_type` varchar(50) DEFAULT NULL,
  `python3_home` varchar(200) DEFAULT NULL,
  `script_path` varchar(200) DEFAULT NULL,
  `run_time` varchar(100) DEFAULT NULL,
  `comments` varchar(100) DEFAULT NULL,
  `datax_home` varchar(200) DEFAULT NULL,
  `sync_time_type` varchar(50) DEFAULT NULL,
  `sync_gap` int(11) DEFAULT NULL,
  `api_server` varchar(100) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_t_datax_config_u1` (`sync_tag`),
  KEY `idx_t_datax_sync_config_u1` (`sync_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=149 DEFAULT CHARSET=utf8;

/*Table structure for table `t_datax_sync_log` */

DROP TABLE IF EXISTS `t_datax_sync_log`;

CREATE TABLE `t_datax_sync_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sync_tag` varchar(100) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `table_name` varchar(100) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_create_date_n1` (`create_date`),
  KEY `idx_create_date_u1` (`sync_tag`),
  KEY `idx_sync_tag_create_date` (`sync_tag`,`create_date`)
) ENGINE=InnoDB AUTO_INCREMENT=7495 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_archive_config` */

DROP TABLE IF EXISTS `t_db_archive_config`;

CREATE TABLE `t_db_archive_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `archive_tag` varchar(100) DEFAULT NULL,
  `comments` varchar(100) DEFAULT NULL,
  `archive_db_type` varchar(100) DEFAULT NULL,
  `server_id` int(11) DEFAULT NULL,
  `sour_db_id` int(11) DEFAULT NULL,
  `sour_schema` varchar(100) DEFAULT NULL,
  `sour_table` varchar(100) DEFAULT NULL,
  `archive_time_col` varchar(2000) DEFAULT NULL,
  `archive_rentition` varchar(10) DEFAULT NULL,
  `rentition_time` int(11) DEFAULT NULL,
  `rentition_time_type` varchar(10) DEFAULT NULL,
  `if_cover` varchar(1) DEFAULT NULL,
  `dest_db_id` int(11) DEFAULT NULL,
  `dest_schema` varchar(100) DEFAULT NULL,
  `python3_home` varchar(200) DEFAULT NULL,
  `script_path` varchar(200) DEFAULT NULL,
  `run_time` varchar(100) DEFAULT NULL,
  `script_file` varchar(100) DEFAULT NULL,
  `batch_size` int(11) DEFAULT NULL,
  `api_server` varchar(100) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_t_db_archive_config_u1` (`archive_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_archive_log` */

DROP TABLE IF EXISTS `t_db_archive_log`;

CREATE TABLE `t_db_archive_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `archive_tag` varchar(100) DEFAULT NULL,
  `table_name` varchar(100) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `percent` decimal(10,2) DEFAULT NULL,
  `message` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_backup_detail` */

DROP TABLE IF EXISTS `t_db_backup_detail`;

CREATE TABLE `t_db_backup_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `db_tag` varchar(100) DEFAULT NULL,
  `create_date` date DEFAULT NULL,
  `db_name` varchar(50) DEFAULT NULL,
  `file_name` varchar(200) DEFAULT NULL,
  `bk_path` varchar(200) DEFAULT NULL,
  `db_size` varchar(50) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `elaspsed_backup` int(11) DEFAULT NULL,
  `elaspsed_gzip` int(11) DEFAULT NULL,
  `STATUS` varchar(1) DEFAULT NULL,
  `error` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=185453 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_backup_total` */

DROP TABLE IF EXISTS `t_db_backup_total`;

CREATE TABLE `t_db_backup_total` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `db_tag` varchar(100) DEFAULT NULL,
  `create_date` date DEFAULT NULL,
  `bk_base` varchar(200) DEFAULT NULL,
  `total_size` varchar(50) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `elaspsed_backup` int(11) DEFAULT NULL,
  `elaspsed_gzip` int(11) DEFAULT NULL,
  `STATUS` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_t_db_backup_total_n1` (`create_date`)
) ENGINE=InnoDB AUTO_INCREMENT=8182 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_config` */

DROP TABLE IF EXISTS `t_db_config`;

CREATE TABLE `t_db_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_id` int(11) DEFAULT NULL,
  `db_id` int(11) DEFAULT NULL,
  `db_type` varchar(50) DEFAULT NULL,
  `db_tag` varchar(100) DEFAULT NULL,
  `expire` int(11) DEFAULT NULL,
  `bk_base` varchar(200) DEFAULT NULL,
  `script_path` varchar(200) DEFAULT NULL,
  `script_file` varchar(100) DEFAULT NULL,
  `bk_cmd` varchar(200) DEFAULT NULL,
  `run_time` varchar(100) DEFAULT NULL,
  `comments` varchar(100) DEFAULT NULL,
  `python3_home` varchar(200) DEFAULT NULL,
  `backup_databases` varchar(1000) DEFAULT NULL,
  `api_server` varchar(100) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `task_status` varchar(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_t_db_config_u1` (`db_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_inst` */

DROP TABLE IF EXISTS `t_db_inst`;

CREATE TABLE `t_db_inst` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `inst_name` varchar(50) DEFAULT NULL,
  `inst_ip` varchar(20) DEFAULT NULL,
  `inst_port` varchar(20) DEFAULT NULL,
  `inst_type` varchar(20) DEFAULT NULL,
  `mgr_user` varchar(20) DEFAULT NULL,
  `mgr_pass` varchar(100) DEFAULT NULL,
  `start_script` varchar(1000) DEFAULT NULL,
  `stop_script` varchar(1000) DEFAULT NULL,
  `restart_script` varchar(1000) DEFAULT NULL,
  `auto_start_script` varchar(1000) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_source` */

DROP TABLE IF EXISTS `t_db_source`;

CREATE TABLE `t_db_source` (
  `id` int(11) NOT NULL,
  `ip` varchar(100) NOT NULL,
  `port` varchar(20) NOT NULL,
  `service` varchar(40) NOT NULL,
  `status` varchar(1) DEFAULT NULL,
  `creation_date` date DEFAULT NULL,
  `creator` varchar(20) DEFAULT NULL,
  `last_update_date` date DEFAULT NULL,
  `updator` varchar(20) DEFAULT NULL,
  `user` varchar(20) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `db_type` varchar(20) DEFAULT NULL,
  `db_source_type` varchar(10) DEFAULT NULL,
  `db_desc` varchar(40) DEFAULT NULL,
  `db_env` varchar(1) DEFAULT NULL,
  `inst_type` varchar(10) DEFAULT NULL,
  `market_id` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_sync_config` */

DROP TABLE IF EXISTS `t_db_sync_config`;

CREATE TABLE `t_db_sync_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sync_ywlx` varchar(11) DEFAULT NULL,
  `comments` varchar(100) DEFAULT NULL,
  `sync_type` varchar(50) DEFAULT NULL,
  `sync_tag` varchar(100) DEFAULT NULL,
  `sour_db_id` int(11) DEFAULT NULL,
  `desc_db_id` int(11) DEFAULT NULL,
  `server_id` int(11) DEFAULT NULL,
  `run_time` varchar(100) DEFAULT NULL,
  `sync_schema` varchar(100) DEFAULT NULL,
  `sync_schema_dest` varchar(100) DEFAULT NULL,
  `sync_table` varchar(2000) DEFAULT NULL,
  `batch_size` int(11) DEFAULT NULL,
  `batch_size_incr` int(11) DEFAULT NULL,
  `sync_gap` int(11) DEFAULT NULL,
  `sync_col_val` varchar(100) DEFAULT NULL,
  `sync_col_name` varchar(50) DEFAULT NULL,
  `sync_time_type` varchar(50) DEFAULT NULL,
  `script_path` varchar(200) DEFAULT NULL,
  `script_file` varchar(100) DEFAULT NULL,
  `python3_home` varchar(200) DEFAULT NULL,
  `api_server` varchar(100) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_t_db_config_u1` (`sync_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=360 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_sync_tasks_log` */

DROP TABLE IF EXISTS `t_db_sync_tasks_log`;

CREATE TABLE `t_db_sync_tasks_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sync_tag` varchar(100) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_create_date_n1` (`create_date`),
  KEY `idx_create_date_u1` (`sync_tag`),
  KEY `idx_sync_tag_create_date` (`sync_tag`,`create_date`)
) ENGINE=InnoDB AUTO_INCREMENT=243823 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_sync_tasks_log_detail` */

DROP TABLE IF EXISTS `t_db_sync_tasks_log_detail`;

CREATE TABLE `t_db_sync_tasks_log_detail` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sync_tag` varchar(100) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `sync_table` varchar(100) DEFAULT NULL,
  `sync_amount` int(11) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_create_date_n1` (`create_date`),
  KEY `idx_create_date_u1` (`sync_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=1779223 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_transfer_config` */

DROP TABLE IF EXISTS `t_db_transfer_config`;

CREATE TABLE `t_db_transfer_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `transfer_tag` varchar(100) DEFAULT NULL,
  `transfer_type` varchar(100) DEFAULT NULL,
  `server_id` int(11) DEFAULT NULL,
  `comments` varchar(100) DEFAULT NULL,
  `sour_db_id` int(11) DEFAULT NULL,
  `sour_schema` varchar(100) DEFAULT NULL,
  `sour_table` varchar(100) DEFAULT NULL,
  `sour_where` varchar(2000) DEFAULT NULL,
  `dest_db_id` int(11) DEFAULT NULL,
  `dest_schema` varchar(100) DEFAULT NULL,
  `script_path` varchar(200) DEFAULT NULL,
  `script_file` varchar(100) DEFAULT NULL,
  `batch_size` int(11) DEFAULT NULL,
  `python3_home` varchar(200) DEFAULT NULL,
  `api_server` varchar(100) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_t_db_transfer_config_u1` (`transfer_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_transfer_log` */

DROP TABLE IF EXISTS `t_db_transfer_log`;

CREATE TABLE `t_db_transfer_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `transfer_tag` varchar(100) DEFAULT NULL,
  `table_name` varchar(100) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `percent` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_user` */

DROP TABLE IF EXISTS `t_db_user`;

CREATE TABLE `t_db_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `inst_id` varchar(50) DEFAULT NULL,
  `db_user` varchar(20) DEFAULT NULL,
  `db_pass` varchar(100) DEFAULT NULL,
  `statement` varchar(1000) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

/*Table structure for table `t_dmlx` */

DROP TABLE IF EXISTS `t_dmlx`;

CREATE TABLE `t_dmlx` (
  `dm` varchar(10) NOT NULL,
  `mc` varchar(100) DEFAULT NULL,
  `flag` varchar(1) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`dm`),
  KEY `idx_t_dmlx` (`dm`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_dmmx` */

DROP TABLE IF EXISTS `t_dmmx`;

CREATE TABLE `t_dmmx` (
  `dm` varchar(10) NOT NULL DEFAULT '',
  `dmm` varchar(200) NOT NULL DEFAULT '',
  `dmmc` varchar(100) DEFAULT NULL,
  `flag` varchar(1) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`dm`,`dmm`),
  KEY `idx_t_dmmx` (`dm`,`dmm`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_forget_password` */

DROP TABLE IF EXISTS `t_forget_password`;

CREATE TABLE `t_forget_password` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `authentication_string` varchar(100) DEFAULT NULL,
  `flag` varchar(20) DEFAULT NULL,
  `creation_date` datetime DEFAULT NULL,
  `creator` varchar(20) DEFAULT NULL,
  `last_update_date` datetime DEFAULT NULL,
  `updator` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

/*Table structure for table `t_func` */

DROP TABLE IF EXISTS `t_func`;

CREATE TABLE `t_func` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `func_name` varchar(100) DEFAULT NULL,
  `func_url` varchar(300) DEFAULT NULL,
  `priv_id` varchar(100) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `creation_date` date DEFAULT NULL,
  `creator` varchar(20) DEFAULT NULL,
  `last_update_date` date DEFAULT NULL,
  `updator` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=168 DEFAULT CHARSET=utf8;

/*Table structure for table `t_goods` */

DROP TABLE IF EXISTS `t_goods`;

CREATE TABLE `t_goods` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `good_id` varchar(20) DEFAULT NULL,
  `good_name` varchar(100) DEFAULT NULL,
  `opt_type` varchar(3) DEFAULT NULL,
  `good_price` decimal(20,2) DEFAULT NULL,
  `good_amount` int(11) DEFAULT NULL,
  `good_actual` decimal(20,2) DEFAULT NULL,
  `good_payable` decimal(20,2) DEFAULT NULL,
  `discounts` decimal(20,2) DEFAULT NULL,
  `charge` decimal(20,2) DEFAULT NULL,
  `restitution` decimal(20,2) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_index` */

DROP TABLE IF EXISTS `t_monitor_index`;

CREATE TABLE `t_monitor_index` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index_name` varchar(50) DEFAULT NULL,
  `index_code` varchar(50) DEFAULT NULL,
  `index_type` varchar(1) DEFAULT NULL,
  `index_db_type` varchar(1) DEFAULT NULL,
  `index_threshold_type` varchar(1) DEFAULT NULL,
  `index_threshold` varchar(10) DEFAULT NULL,
  `index_threshold_day` varchar(10) DEFAULT NULL,
  `index_threshold_times` varchar(3) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `trigger_time` int(11) DEFAULT NULL,
  `trigger_times` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_t_monitor_index_u1` (`index_code`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_server_warn_log` */

DROP TABLE IF EXISTS `t_monitor_server_warn_log`;

CREATE TABLE `t_monitor_server_warn_log` (
  `server_id` int(11) NOT NULL DEFAULT '0',
  `server_desc` varchar(100) DEFAULT NULL,
  `index_code` varchar(50) NOT NULL,
  `index_name` varchar(100) DEFAULT NULL,
  `index_value` varchar(100) DEFAULT NULL,
  `fail_times` int(11) DEFAULT NULL,
  `succ_times` int(11) DEFAULT NULL,
  `is_send_rcv_mail` varchar(10) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`server_id`,`index_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_service` */

DROP TABLE IF EXISTS `t_monitor_service`;

CREATE TABLE `t_monitor_service` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_id` int(11) DEFAULT NULL,
  `server_desc` varchar(1000) DEFAULT NULL,
  `mysql_proj` varchar(1000) DEFAULT NULL,
  `mssql_park` varchar(1000) DEFAULT NULL,
  `mssql_flow` varchar(1000) DEFAULT NULL,
  `mssql_car` varchar(1000) DEFAULT NULL,
  `redis` varchar(1000) DEFAULT NULL,
  `mongo` varchar(1000) DEFAULT NULL,
  `es` varchar(1000) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `sxh` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6108364 DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_task` */

DROP TABLE IF EXISTS `t_monitor_task`;

CREATE TABLE `t_monitor_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_tag` varchar(50) DEFAULT NULL,
  `server_id` varchar(20) DEFAULT NULL,
  `templete_id` varchar(20) DEFAULT NULL,
  `db_id` varchar(20) DEFAULT NULL,
  `comments` varchar(50) DEFAULT NULL,
  `run_time` varchar(20) DEFAULT NULL,
  `script_path` varchar(200) DEFAULT NULL,
  `script_file` varchar(100) DEFAULT NULL,
  `python3_home` varchar(200) DEFAULT NULL,
  `api_server` varchar(100) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_t_monitor_task_u1` (`task_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=178 DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_task_db_log` */

DROP TABLE IF EXISTS `t_monitor_task_db_log`;

CREATE TABLE `t_monitor_task_db_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `task_tag` varchar(50) DEFAULT NULL,
  `server_id` int(11) DEFAULT NULL,
  `db_id` int(11) DEFAULT NULL,
  `total_connect` varchar(11) DEFAULT NULL,
  `active_connect` varchar(11) DEFAULT NULL,
  `db_available` varchar(20) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_t_monitor_task_db_log_n1` (`create_date`),
  KEY `idx_t_monitor_task_db_log_c1` (`db_id`,`create_date`),
  KEY `idx_t_monitor_task_db_log_n2` (`server_id`)
) ENGINE=InnoDB AUTO_INCREMENT=734220 DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_task_server_log` */

DROP TABLE IF EXISTS `t_monitor_task_server_log`;

CREATE TABLE `t_monitor_task_server_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `task_tag` varchar(50) DEFAULT NULL,
  `server_id` int(11) DEFAULT NULL,
  `cpu_total_usage` varchar(50) DEFAULT NULL,
  `cpu_core_usage` varchar(50) DEFAULT NULL,
  `mem_usage` varchar(50) DEFAULT NULL,
  `disk_usage` varchar(200) DEFAULT NULL,
  `disk_read` varchar(20) DEFAULT NULL,
  `disk_write` varchar(20) DEFAULT NULL,
  `net_in` varchar(20) DEFAULT NULL,
  `net_out` varchar(20) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `market_id` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_t_monitor_task_server_log_n1` (`create_date`),
  KEY `idx_t_monitor_task_server_log_n2` (`server_id`)
) ENGINE=InnoDB AUTO_INCREMENT=375772 DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_templete` */

DROP TABLE IF EXISTS `t_monitor_templete`;

CREATE TABLE `t_monitor_templete` (
  `id` int(11) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `code` varchar(20) DEFAULT NULL,
  `type` varchar(20) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `creation_date` date DEFAULT NULL,
  `creator` varchar(20) DEFAULT NULL,
  `last_update_date` date DEFAULT NULL,
  `updator` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_t_monitor_templete_u1` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_templete_index` */

DROP TABLE IF EXISTS `t_monitor_templete_index`;

CREATE TABLE `t_monitor_templete_index` (
  `templete_id` int(11) NOT NULL,
  `index_id` varchar(20) DEFAULT NULL,
  `creation_date` date DEFAULT NULL,
  `creator` varchar(20) DEFAULT NULL,
  `last_update_date` date DEFAULT NULL,
  `updator` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_warn_log` */

DROP TABLE IF EXISTS `t_monitor_warn_log`;

CREATE TABLE `t_monitor_warn_log` (
  `server_id` int(11) NOT NULL DEFAULT '0',
  `server_desc` varchar(100) DEFAULT NULL,
  `db_id` int(11) NOT NULL DEFAULT '0',
  `db_desc` varchar(100) DEFAULT NULL,
  `fail_times` int(11) DEFAULT NULL,
  `succ_times` int(11) DEFAULT NULL,
  `is_send_rcv_mail` varchar(10) DEFAULT NULL,
  `warn_type` varchar(20) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`server_id`,`db_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_port` */

DROP TABLE IF EXISTS `t_port`;

CREATE TABLE `t_port` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(100) DEFAULT NULL,
  `app_port` varchar(100) DEFAULT NULL,
  `app_dev` varchar(20) DEFAULT NULL,
  `app_desc` varchar(100) DEFAULT NULL,
  `app_ext` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=152 DEFAULT CHARSET=utf8;

/*Table structure for table `t_role` */

DROP TABLE IF EXISTS `t_role`;

CREATE TABLE `t_role` (
  `id` int(11) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `creation_date` date DEFAULT NULL,
  `creator` varchar(20) DEFAULT NULL,
  `last_update_date` date DEFAULT NULL,
  `updator` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_role_func_privs` */

DROP TABLE IF EXISTS `t_role_func_privs`;

CREATE TABLE `t_role_func_privs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` varchar(100) DEFAULT NULL,
  `func_id` varchar(100) DEFAULT NULL,
  `creation_date` date DEFAULT NULL,
  `creator` varchar(20) DEFAULT NULL,
  `last_update_date` date DEFAULT NULL,
  `updator` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15429 DEFAULT CHARSET=utf8;

/*Table structure for table `t_role_privs` */

DROP TABLE IF EXISTS `t_role_privs`;

CREATE TABLE `t_role_privs` (
  `role_id` int(11) NOT NULL,
  `priv_id` varchar(20) DEFAULT NULL,
  `creation_date` date DEFAULT NULL,
  `creator` varchar(20) DEFAULT NULL,
  `last_update_date` date DEFAULT NULL,
  `updator` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_server` */

DROP TABLE IF EXISTS `t_server`;

CREATE TABLE `t_server` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `market_id` varchar(20) NOT NULL,
  `server_type` varchar(100) DEFAULT NULL,
  `server_desc` varchar(100) DEFAULT NULL,
  `server_ip` varchar(100) NOT NULL,
  `server_port` varchar(10) NOT NULL,
  `server_user` varchar(20) NOT NULL,
  `server_pass` varchar(200) NOT NULL,
  `server_os` varchar(100) NOT NULL,
  `server_cpu` varchar(100) NOT NULL,
  `server_mem` varchar(100) NOT NULL,
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8;

/*Table structure for table `t_sql_audit_rule` */

DROP TABLE IF EXISTS `t_sql_audit_rule`;

CREATE TABLE `t_sql_audit_rule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rule_type` varchar(50) DEFAULT NULL,
  `rule_code` varchar(50) DEFAULT NULL,
  `rule_name` varchar(100) DEFAULT NULL,
  `rule_value` varchar(100) DEFAULT NULL,
  `error` varchar(100) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_t_sql_audit_rule_u1` (`rule_code`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8;

/*Table structure for table `t_sql_audit_rule_err` */

DROP TABLE IF EXISTS `t_sql_audit_rule_err`;

CREATE TABLE `t_sql_audit_rule_err` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `xh` int(11) DEFAULT NULL,
  `rule_id` varchar(100) DEFAULT NULL,
  `rule_name` varchar(100) DEFAULT NULL,
  `rule_value` varchar(100) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `obj_name` varchar(100) DEFAULT NULL,
  `error` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3430 DEFAULT CHARSET=utf8;

/*Table structure for table `t_sql_release` */

DROP TABLE IF EXISTS `t_sql_release`;

CREATE TABLE `t_sql_release` (
  `id` int(11) NOT NULL,
  `dbid` int(11) NOT NULL,
  `sqltext` longtext,
  `status` varchar(1) DEFAULT NULL,
  `message` varchar(2000) DEFAULT NULL,
  `creation_date` datetime DEFAULT NULL,
  `creator` varchar(20) DEFAULT NULL,
  `last_update_date` datetime DEFAULT NULL,
  `updator` varchar(20) DEFAULT NULL,
  `audit_date` datetime DEFAULT NULL,
  `auditor` varchar(20) DEFAULT NULL,
  `version` varchar(20) DEFAULT NULL,
  `type` varchar(1) DEFAULT NULL,
  `executor` varchar(20) DEFAULT NULL,
  `exec_start` datetime DEFAULT NULL,
  `exec_end` datetime DEFAULT NULL,
  `error` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_sql_release_results` */

DROP TABLE IF EXISTS `t_sql_release_results`;

CREATE TABLE `t_sql_release_results` (
  `id` int(11) NOT NULL,
  `release_id` int(11) DEFAULT NULL,
  `db_env` varchar(1) DEFAULT NULL,
  `db_status` varchar(1) DEFAULT NULL,
  `db_msg` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_sys_usage` */

DROP TABLE IF EXISTS `t_sys_usage`;

CREATE TABLE `t_sys_usage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(15) DEFAULT NULL,
  `port` varchar(5) DEFAULT NULL,
  `rq` datetime DEFAULT NULL,
  `cpu_usage_rate` decimal(10,2) DEFAULT NULL,
  `memory_usage_rate` decimal(10,2) DEFAULT NULL,
  `disk_read_bytes` bigint(20) DEFAULT NULL,
  `disk_write_bytes` bigint(20) DEFAULT NULL,
  `net_send_bytes` bigint(20) DEFAULT NULL,
  `net_recv_bytes` bigint(20) DEFAULT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_templete` */

DROP TABLE IF EXISTS `t_templete`;

CREATE TABLE `t_templete` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `templete_id` int(11) DEFAULT NULL,
  `contents` text,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*Table structure for table `t_user` */

DROP TABLE IF EXISTS `t_user`;

CREATE TABLE `t_user` (
  `id` int(11) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `wkno` varchar(20) DEFAULT NULL,
  `gender` varchar(2) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `project_group` varchar(1) DEFAULT NULL,
  `dept` varchar(20) DEFAULT NULL,
  `expire_date` date DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `creation_date` date DEFAULT NULL,
  `creator` varchar(20) DEFAULT NULL,
  `last_update_date` date DEFAULT NULL,
  `updator` varchar(20) DEFAULT NULL,
  `login_name` varchar(20) DEFAULT NULL,
  `file_path` varchar(200) DEFAULT NULL,
  `file_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_login_name_n1` (`login_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_user_proj_privs` */

DROP TABLE IF EXISTS `t_user_proj_privs`;

CREATE TABLE `t_user_proj_privs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `proj_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `priv_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2889 DEFAULT CHARSET=utf8;

/*Table structure for table `t_user_role` */

DROP TABLE IF EXISTS `t_user_role`;

CREATE TABLE `t_user_role` (
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_wtd` */

DROP TABLE IF EXISTS `t_wtd`;

CREATE TABLE `t_wtd` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_no` varchar(50) NOT NULL,
  `order_env` varchar(50) NOT NULL,
  `order_type` varchar(50) DEFAULT NULL,
  `order_status` varchar(50) DEFAULT NULL,
  `order_handler` varchar(50) DEFAULT NULL,
  `order_desc` varchar(1000) DEFAULT NULL,
  `creator` varchar(50) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `handler_date` datetime DEFAULT NULL,
  `attachment_path` varchar(1000) DEFAULT NULL,
  `attachment_name` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_order_no_u1` (`order_no`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

/*Table structure for table `t_xtqx` */

DROP TABLE IF EXISTS `t_xtqx`;

CREATE TABLE `t_xtqx` (
  `id` varchar(10) NOT NULL DEFAULT '',
  `name` varchar(20) DEFAULT NULL,
  `parent_id` varchar(10) DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `icon` varchar(50) DEFAULT NULL,
  `creation_date` date DEFAULT NULL,
  `creator` varchar(20) DEFAULT NULL,
  `last_update_date` date DEFAULT NULL,
  `updator` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*!50106 set global event_scheduler = 1*/;

/* Event structure for event `event_clear_log` */

/*!50106 DROP EVENT IF EXISTS `event_clear_log`*/;

DELIMITER $$

/*!50106 CREATE DEFINER=`puppet`@`%` EVENT `event_clear_log` ON SCHEDULE EVERY 1 DAY STARTS '2020-05-29 00:00:00' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN
  CALL `proc_clear_log`();
END */$$
DELIMITER ;

/* Event structure for event `event_proc_tj_service` */

/*!50106 DROP EVENT IF EXISTS `event_proc_tj_service`*/;

DELIMITER $$

/*!50106 CREATE DEFINER=`puppet`@`%` EVENT `event_proc_tj_service` ON SCHEDULE EVERY 30 SECOND STARTS '2020-04-29 17:11:51' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN
     call proc_tj_service();
END */$$
DELIMITER ;

/* Procedure structure for procedure `proc_clear_log` */

/*!50003 DROP PROCEDURE IF EXISTS  `proc_clear_log` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`puppet`@`%` PROCEDURE `proc_clear_log`()
BEGIN
	#TRUNCATE TABLE `t_monitor_task_db_log`;
	#TRUNCATE TABLE `t_monitor_task_server_log`;
	#TRUNCATE TABLE `t_db_sync_tasks_log`;
	#TRUNCATE TABLE `t_db_sync_tasks_log_detail`;
	#TRUNCATE TABLE `t_datax_sync_log`;
END */$$
DELIMITER ;

/* Procedure structure for procedure `proc_tj_service` */

/*!50003 DROP PROCEDURE IF EXISTS  `proc_tj_service` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`puppet`@`%` PROCEDURE `proc_tj_service`()
BEGIN
  DECLARE n_server_id    INT;
  DECLARE v_server_desc  varchar(100);
  DECLARE v_db_desc      VARCHAR(100);
  DECLARE v_db_type      VARCHAR(100);
  DECLARE n_db_available INT;
  DECLARE d_create_date  datetime;
  
  DECLARE n_mysql_proj   INT;
  DECLARE n_mssql_flow   INT;
  DECLARE n_mssql_park   INT;
  DECLARE n_mssql_car    INT;
  DECLARE n_elastic      INT;
  DECLARE n_redis        INT;
  DECLARE n_mongo        INT;
  
  declare v_mysql_proj   VARCHAR(100);
  DECLARE v_mssql_flow   VARCHAR(100);
  DECLARE v_mssql_park   VARCHAR(100);
  DECLARE v_mssql_car    VARCHAR(100);
  DECLARE v_elastic      VARCHAR(100);
  DECLARE v_redis        VARCHAR(100);
  DECLARE v_mongo        VARCHAR(100);
  
  -- 设置终止标记
  DECLARE _outer INT DEFAULT 0;
  DECLARE _inner INT DEFAULT 0;
  DECLARE cur_server  CURSOR FOR SELECT id,server_desc FROM `t_server` WHERE STATUS='1' order by id;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET _outer = 1;
  -- 开启事务
  SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
  START TRANSACTION;
 
  -- 清空数据
  
  delete from t_monitor_service;
  OPEN cur_server;
  out_loop:LOOP
     FETCH NEXT FROM cur_server INTO n_server_id,v_server_desc;
     IF _outer = 1 THEN
	LEAVE out_loop;
     END IF;
     
     -- mysql项目服务
     SELECT 
        count(0),MAX(create_date)  into n_mysql_proj,d_create_date
     FROM t_monitor_task_db_log a 
        LEFT JOIN t_server b ON a.server_id=b.id
        LEFT JOIN t_db_source c ON a.db_id=c.id
     WHERE (a.db_id,a.create_date) IN(
            SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
       AND b.id=n_server_id
       AND c.db_type='0';
	  
     if n_mysql_proj >0 then
	SELECT 
	      GROUP_CONCAT(CONCAT(a.db_available,'@',c.id,'@',a.`create_date`))  into v_mysql_proj
	FROM t_monitor_task_db_log a 
	   LEFT JOIN t_server b ON a.server_id=b.id
	   LEFT JOIN t_db_source c ON a.db_id=c.id
	WHERE (a.db_id,a.create_date) IN(
	       SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
	  AND b.id=n_server_id
	  and c.db_type='0' ;
	  
     else
          set v_mysql_proj = '';
     end if;   
     
     -- 汇纳客流mssql服务
     SELECT 
        COUNT(0) INTO n_mssql_flow
     FROM t_monitor_task_db_log a 
        LEFT JOIN t_server b ON a.server_id=b.id
        LEFT JOIN t_db_source c ON a.db_id=c.id
     WHERE (a.db_id,a.create_date) IN(
            SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
       AND b.id=n_server_id
       AND c.db_type='2' 
       AND INSTR(c.db_desc,'客流')>0;
	  
     IF n_mssql_flow >0 THEN
	SELECT 
	      GROUP_CONCAT(CONCAT(a.db_available,'@',c.id,'@',a.`create_date`))   INTO v_mssql_flow
	FROM t_monitor_task_db_log a 
	   LEFT JOIN t_server b ON a.server_id=b.id
	   LEFT JOIN t_db_source c ON a.db_id=c.id
	WHERE (a.db_id,a.create_date) IN(
	       SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
	  AND b.id=n_server_id
	  AND c.db_type='2' 
	  AND INSTR(c.db_desc,'客流')>0;
     ELSE
          SET v_mssql_flow = '';
     END IF;    
     
     -- 捷顺车流mssql服务
     SELECT 
        COUNT(0) INTO n_mssql_park
     FROM t_monitor_task_db_log a 
        LEFT JOIN t_server b ON a.server_id=b.id
        LEFT JOIN t_db_source c ON a.db_id=c.id
     WHERE (a.db_id,a.create_date) IN(
            SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
       AND b.id=n_server_id
       AND c.db_type='2' 
       AND INSTR(c.db_desc,'车流')>0;
	  
     IF n_mssql_park >0 THEN
	SELECT 
	      GROUP_CONCAT(CONCAT(a.db_available,'@',c.id,'@',a.`create_date`))   INTO v_mssql_park
	FROM t_monitor_task_db_log a 
	   LEFT JOIN t_server b ON a.server_id=b.id
	   LEFT JOIN t_db_source c ON a.db_id=c.id
	WHERE (a.db_id,a.create_date) IN(
	       SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
	  AND b.id=n_server_id
	  AND c.db_type='2' 
	  AND INSTR(c.db_desc,'车流')>0;
     ELSE
          SET v_mssql_park = '';
     END IF;  
     
      -- 捷顺反向寻车mssql服务
     SELECT 
        COUNT(0) INTO n_mssql_car
     FROM t_monitor_task_db_log a 
        LEFT JOIN t_server b ON a.server_id=b.id
        LEFT JOIN t_db_source c ON a.db_id=c.id
     WHERE (a.db_id,a.create_date) IN(
            SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
       AND b.id=n_server_id
       AND c.db_type='2' 
       AND INSTR(c.db_desc,'寻车')>0;
	  
     IF n_mssql_car >0 THEN
	SELECT 
	      GROUP_CONCAT(CONCAT(a.db_available,'@',c.id,'@',a.`create_date`))   INTO v_mssql_car
	FROM t_monitor_task_db_log a 
	   LEFT JOIN t_server b ON a.server_id=b.id
	   LEFT JOIN t_db_source c ON a.db_id=c.id
	WHERE (a.db_id,a.create_date) IN(
	       SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
	  AND b.id=n_server_id
	  AND c.db_type='2' 
	  AND INSTR(c.db_desc,'寻车')>0;
     ELSE
          SET v_mssql_car = '';
     END IF;  
     
      -- ElasticSearch 服务
     SELECT 
        COUNT(0) INTO n_elastic
     FROM t_monitor_task_db_log a 
        LEFT JOIN t_server b ON a.server_id=b.id
        LEFT JOIN t_db_source c ON a.db_id=c.id
     WHERE (a.db_id,a.create_date) IN(
            SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
       AND b.id=n_server_id
       AND c.db_type='4' ;
	  
     IF n_elastic >0 THEN
	SELECT 
	     GROUP_CONCAT(CONCAT(a.db_available,'@',c.id,'@',a.`create_date`))   INTO v_elastic
	FROM t_monitor_task_db_log a 
	   LEFT JOIN t_server b ON a.server_id=b.id
	   LEFT JOIN t_db_source c ON a.db_id=c.id
	WHERE (a.db_id,a.create_date) IN(
	       SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
	  AND b.id=n_server_id
	  AND c.db_type='4';
     ELSE
          SET v_elastic = '';
     END IF;
     
     -- redis 服务1
     SELECT 
        COUNT(0) INTO n_redis
     FROM t_monitor_task_db_log a 
        LEFT JOIN t_server b ON a.server_id=b.id
        LEFT JOIN t_db_source c ON a.db_id=c.id
     WHERE (a.db_id,a.create_date) IN(
            SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
       AND b.id=n_server_id
       AND c.db_type='5' ;    
    	  
     IF n_redis >0 THEN
	SELECT 
	      GROUP_CONCAT(CONCAT(a.db_available,'@',c.id,'@',a.`create_date`))   INTO v_redis
	FROM t_monitor_task_db_log a 
	   LEFT JOIN t_server b ON a.server_id=b.id
	   LEFT JOIN t_db_source c ON a.db_id=c.id
	WHERE (a.db_id,a.create_date) IN(
	       SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
	  AND b.id=n_server_id
	  AND c.db_type='5' ;
     ELSE
          SET v_redis = '';
     END IF;
     
      -- mongo 服务
     SELECT 
        COUNT(0) INTO n_mongo
     FROM t_monitor_task_db_log a 
        LEFT JOIN t_server b ON a.server_id=b.id
        LEFT JOIN t_db_source c ON a.db_id=c.id
     WHERE (a.db_id,a.create_date) IN(
            SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
       AND b.id=n_server_id
       AND c.db_type='6' ;
      
	  
     IF n_mongo >0 THEN
	SELECT 
	      GROUP_CONCAT(CONCAT(a.db_available,'@',c.id,'@',a.`create_date`))   INTO v_mongo
	FROM t_monitor_task_db_log a 
	   LEFT JOIN t_server b ON a.server_id=b.id
	   LEFT JOIN t_db_source c ON a.db_id=c.id
	WHERE (a.db_id,a.create_date) IN(
	       SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
	  AND b.id=n_server_id
	  AND c.db_type='6' ;	 
     ELSE
          SET v_mongo = '';
     END IF;
    
     if instr(v_mysql_proj,'0@')>0 or INSTR(v_mssql_flow,'0@')>0 or INSTR(v_mssql_park,'0@')>0 or INSTR(v_mssql_car,'0@')>0  or INSTR(v_elastic,'0@')>0 then
	INSERT INTO t_monitor_service(server_id,server_desc,mysql_proj,mssql_flow,mssql_park,mssql_car,redis,mongo,es,create_date,sxh)
          VALUES(n_server_id,v_server_desc,v_mysql_proj,v_mssql_flow,v_mssql_park,v_mssql_car,v_redis,v_mongo,v_elastic, NOW(),-UNIX_TIMESTAMP());                           
     else
        INSERT INTO t_monitor_service(server_id,server_desc,mysql_proj,mssql_flow,mssql_park,mssql_car,redis,mongo,es,create_date,sxh)
          VALUES(n_server_id,v_server_desc,v_mysql_proj,v_mssql_flow,v_mssql_park,v_mssql_car,v_redis,v_mongo,v_elastic,NOW(),UNIX_TIMESTAMP());
     end if;     
       
  END LOOP;  
  
  -- 提交事务
  commit;
END */$$
DELIMITER ;

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

/*View structure for view v_monitor_service */

/*!50001 DROP TABLE IF EXISTS `v_monitor_service` */;
/*!50001 DROP VIEW IF EXISTS `v_monitor_service` */;

/*!50001 CREATE ALGORITHM=UNDEFINED DEFINER=`puppet`@`%` SQL SECURITY DEFINER VIEW `v_monitor_service` AS select `t_monitor_service`.`server_id` AS `server_id`,`t_monitor_service`.`server_desc` AS `server_desc`,`t_monitor_service`.`mysql_proj` AS `service_service`,'mysql' AS `flag` from `t_monitor_service` where (`t_monitor_service`.`mysql_proj` <> '') union all select `t_monitor_service`.`server_id` AS `server_id`,`t_monitor_service`.`server_desc` AS `server_desc`,`t_monitor_service`.`mssql_park` AS `mssql_park`,'mssql_park' AS `flag` from `t_monitor_service` where (`t_monitor_service`.`mssql_park` <> '') union all select `t_monitor_service`.`server_id` AS `server_id`,`t_monitor_service`.`server_desc` AS `server_desc`,`t_monitor_service`.`mssql_flow` AS `mssql_flow`,'mssql_flow' AS `flag` from `t_monitor_service` where (`t_monitor_service`.`mssql_flow` <> '') union all select `t_monitor_service`.`server_id` AS `server_id`,`t_monitor_service`.`server_desc` AS `server_desc`,`t_monitor_service`.`mssql_car` AS `mssql_car`,'mssql_car' AS `flag` from `t_monitor_service` where (`t_monitor_service`.`mssql_car` <> '') union all select `t_monitor_service`.`server_id` AS `server_id`,`t_monitor_service`.`server_desc` AS `server_desc`,`t_monitor_service`.`redis` AS `redis`,'redis' AS `flag` from `t_monitor_service` where (`t_monitor_service`.`redis` <> '') union all select `t_monitor_service`.`server_id` AS `server_id`,`t_monitor_service`.`server_desc` AS `server_desc`,`t_monitor_service`.`mongo` AS `mongo`,'mongo' AS `flag` from `t_monitor_service` where (`t_monitor_service`.`mongo` <> '') union all select `t_monitor_service`.`server_id` AS `server_id`,`t_monitor_service`.`server_desc` AS `server_desc`,`t_monitor_service`.`es` AS `es`,'es' AS `flag` from `t_monitor_service` where (`t_monitor_service`.`es` <> '') order by `server_id` */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
