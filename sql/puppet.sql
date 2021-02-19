/*
SQLyog Ultimate v11.24 (64 bit)
MySQL - 5.7.30-33-57-log : Database - puppet
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`puppet` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `puppet`;

/*Table structure for table `t_datax_sync_config` */

DROP TABLE IF EXISTS `t_datax_sync_config`;

CREATE TABLE `t_datax_sync_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sync_tag` varchar(100) DEFAULT NULL COMMENT '同步标识',
  `server_id` int(11) DEFAULT NULL COMMENT '同步服务器ID',
  `sour_db_id` int(11) DEFAULT NULL COMMENT '源数据库ID',
  `sync_schema` varchar(100) DEFAULT NULL COMMENT '同步数据库',
  `sync_table` varchar(2000) DEFAULT NULL COMMENT '同步表',
  `sync_columns` varchar(2000) DEFAULT NULL COMMENT '同步列名列表',
  `sync_incr_col` varchar(50) DEFAULT NULL COMMENT '增量同步列名',
  `sync_incr_where` varchar(1000) DEFAULT NULL COMMENT '增量同步条件',
  `zk_hosts` varchar(100) DEFAULT NULL COMMENT 'zookeeper地址',
  `hbase_thrift` varchar(100) DEFAULT NULL COMMENT 'hbase_thrift接口地址',
  `sync_hbase_table` varchar(100) DEFAULT NULL COMMENT 'hbase同步表名',
  `sync_hbase_rowkey` text COMMENT 'hbase行键名称',
  `sync_hbase_rowkey_sour` varchar(50) DEFAULT NULL COMMENT 'hbase行键原始字符串',
  `sync_hbase_columns` text COMMENT 'hbase同步列',
  `sync_hbase_rowkey_separator` varchar(10) DEFAULT NULL COMMENT 'hbase行键分隔符',
  `es_service` varchar(50) DEFAULT NULL COMMENT 'es服务地址',
  `es_index_name` varchar(100) DEFAULT NULL COMMENT 'es索引名称',
  `es_type_name` varchar(100) DEFAULT NULL COMMENT 'es类型名称',
  `sync_es_columns` text COMMENT 'es同步列名列表',
  `sync_ywlx` varchar(11) DEFAULT NULL COMMENT '同步业务类型',
  `sync_type` varchar(50) DEFAULT NULL COMMENT '同步类型',
  `python3_home` varchar(200) DEFAULT NULL COMMENT 'python3目录',
  `script_path` varchar(200) DEFAULT NULL COMMENT '同步客户端脚本',
  `run_time` varchar(100) DEFAULT NULL COMMENT '运行时间',
  `comments` varchar(100) DEFAULT NULL COMMENT '任务描述',
  `datax_home` varchar(200) DEFAULT NULL COMMENT 'datax工具目录',
  `sync_time_type` varchar(50) DEFAULT NULL COMMENT '同步时间类型',
  `sync_gap` int(11) DEFAULT NULL COMMENT '同步间隔',
  `api_server` varchar(100) DEFAULT NULL COMMENT 'api服务地址',
  `status` varchar(1) DEFAULT NULL COMMENT '任务状态',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_t_datax_config_u1` (`sync_tag`),
  KEY `idx_t_datax_sync_config_u1` (`sync_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=150 DEFAULT CHARSET=utf8;

/*Table structure for table `t_datax_sync_log` */

DROP TABLE IF EXISTS `t_datax_sync_log`;

CREATE TABLE `t_datax_sync_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `sync_tag` varchar(100) NOT NULL COMMENT '同步标识',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `table_name` varchar(100) DEFAULT NULL COMMENT '表名称',
  `duration` int(11) DEFAULT NULL COMMENT '同步时长',
  `amount` int(11) DEFAULT NULL COMMENT '同步数量',
  PRIMARY KEY (`id`),
  KEY `idx_create_date_n1` (`create_date`),
  KEY `idx_create_date_u1` (`sync_tag`),
  KEY `idx_sync_tag_create_date` (`sync_tag`,`create_date`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_archive_config` */

DROP TABLE IF EXISTS `t_db_archive_config`;

CREATE TABLE `t_db_archive_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `archive_tag` varchar(100) DEFAULT NULL COMMENT '归档标识',
  `comments` varchar(100) DEFAULT NULL COMMENT '任务描述',
  `archive_db_type` varchar(100) DEFAULT NULL COMMENT '数据库类型',
  `server_id` int(11) DEFAULT NULL COMMENT '归档服务器ID',
  `sour_db_id` varchar(11) DEFAULT NULL COMMENT '源数据库ID',
  `sour_schema` varchar(100) DEFAULT NULL COMMENT '源数据库名',
  `sour_table` varchar(100) DEFAULT NULL COMMENT '源库表名',
  `archive_time_col` varchar(2000) DEFAULT NULL COMMENT '归档时间列名',
  `archive_rentition` varchar(10) DEFAULT NULL COMMENT '归档策略',
  `rentition_time` int(11) DEFAULT NULL COMMENT '保留时间',
  `rentition_time_type` varchar(10) DEFAULT NULL COMMENT '保留时间类型',
  `if_cover` varchar(1) DEFAULT NULL COMMENT '是否覆盖',
  `dest_db_id` varchar(11) DEFAULT NULL COMMENT '目标数据库ID',
  `dest_schema` varchar(100) DEFAULT NULL COMMENT '目标数据库名',
  `python3_home` varchar(200) DEFAULT NULL COMMENT 'python3目录',
  `script_path` varchar(200) DEFAULT NULL COMMENT '归档客户端路径',
  `run_time` varchar(100) DEFAULT NULL COMMENT '运行时间',
  `script_file` varchar(100) DEFAULT NULL COMMENT '归档客户端名称',
  `batch_size` int(11) DEFAULT NULL COMMENT '归档批大小',
  `api_server` varchar(100) DEFAULT NULL COMMENT 'API服务器',
  `status` varchar(1) DEFAULT NULL COMMENT '归档状态',
  PRIMARY KEY (`id`),
  KEY `idx_t_db_archive_config_u1` (`archive_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_archive_log` */

DROP TABLE IF EXISTS `t_db_archive_log`;

CREATE TABLE `t_db_archive_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `archive_tag` varchar(100) DEFAULT NULL COMMENT '归档标识',
  `table_name` varchar(100) DEFAULT NULL COMMENT '表名',
  `create_date` datetime DEFAULT NULL COMMENT '创建日期',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `duration` int(11) DEFAULT NULL COMMENT '归档时长',
  `amount` int(11) DEFAULT NULL COMMENT '归档数量',
  `percent` decimal(10,2) DEFAULT NULL COMMENT '归档进度',
  `message` varchar(1000) DEFAULT NULL COMMENT '归档消息',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_backup_detail` */

DROP TABLE IF EXISTS `t_db_backup_detail`;

CREATE TABLE `t_db_backup_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `db_tag` varchar(100) DEFAULT NULL COMMENT '数据库标识',
  `create_date` date DEFAULT NULL COMMENT '备份日期',
  `db_name` varchar(50) DEFAULT NULL COMMENT '数据库名',
  `file_name` varchar(200) DEFAULT NULL COMMENT '备份文件名',
  `bk_path` varchar(200) DEFAULT NULL COMMENT '备份路径',
  `db_size` varchar(50) DEFAULT NULL COMMENT '文件大小',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `elaspsed_backup` int(11) DEFAULT NULL COMMENT '备份耗时',
  `elaspsed_gzip` int(11) DEFAULT NULL COMMENT '压缩耗时',
  `STATUS` varchar(1) DEFAULT NULL COMMENT '备份状态',
  `error` longtext COMMENT '错误消息',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_backup_total` */

DROP TABLE IF EXISTS `t_db_backup_total`;

CREATE TABLE `t_db_backup_total` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `db_tag` varchar(100) DEFAULT NULL COMMENT '数据库标识',
  `create_date` date DEFAULT NULL COMMENT '备份时间',
  `bk_base` varchar(200) DEFAULT NULL COMMENT '备份目录',
  `total_size` varchar(50) DEFAULT NULL COMMENT '备份大小',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `elaspsed_backup` int(11) DEFAULT NULL COMMENT '备份耗时',
  `elaspsed_gzip` int(11) DEFAULT NULL COMMENT '压缩耗时',
  `STATUS` varchar(1) DEFAULT NULL COMMENT '备份状态',
  PRIMARY KEY (`id`),
  KEY `idx_t_db_backup_total_n1` (`create_date`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_config` */

DROP TABLE IF EXISTS `t_db_config`;

CREATE TABLE `t_db_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID主键',
  `server_id` int(11) DEFAULT NULL COMMENT '备份服务器ID',
  `db_id` int(11) DEFAULT NULL COMMENT '数据源ID',
  `db_type` varchar(50) DEFAULT NULL COMMENT '数据库类型',
  `db_tag` varchar(100) DEFAULT NULL COMMENT '备份标识',
  `expire` int(11) DEFAULT NULL COMMENT '过期时间',
  `bk_base` varchar(200) DEFAULT NULL COMMENT '备份目录',
  `script_path` varchar(200) DEFAULT NULL COMMENT '备份客户端路径',
  `script_file` varchar(100) DEFAULT NULL COMMENT '备份客户端文件名',
  `bk_cmd` varchar(200) DEFAULT NULL COMMENT '备份命令',
  `run_time` varchar(100) DEFAULT NULL COMMENT '运行时间',
  `comments` varchar(100) DEFAULT NULL COMMENT '任务描述',
  `python3_home` varchar(200) DEFAULT NULL COMMENT 'python3路径',
  `backup_databases` varchar(1000) DEFAULT NULL COMMENT '备份数据库列表',
  `api_server` varchar(100) DEFAULT NULL COMMENT 'API接口地址',
  `status` varchar(1) DEFAULT NULL COMMENT '任务状态',
  `task_status` varchar(1) DEFAULT '0' COMMENT '运行状态',
  PRIMARY KEY (`id`),
  KEY `idx_t_db_config_u1` (`db_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_inst` */

DROP TABLE IF EXISTS `t_db_inst`;

CREATE TABLE `t_db_inst` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `inst_name` varchar(50) DEFAULT NULL COMMENT '实例名称',
  `server_id` varchar(11) DEFAULT NULL COMMENT '实例服务器ID',
  `config_id` int(11) DEFAULT NULL COMMENT '配置文件ID',
  `templete_id` int(11) DEFAULT NULL COMMENT '模板ID',
  `inst_ip` varchar(100) DEFAULT NULL COMMENT '实例IP(外网)',
  `inst_ip_in` varchar(100) DEFAULT NULL COMMENT '实例ID(内网)',
  `inst_port` varchar(20) DEFAULT NULL COMMENT '实例端口',
  `inst_mapping_port` varchar(20) DEFAULT NULL COMMENT '实例映射端口',
  `inst_type` varchar(20) DEFAULT NULL COMMENT '实例类型',
  `inst_env` varchar(20) DEFAULT NULL COMMENT '实例环境',
  `inst_ver` varchar(20) DEFAULT NULL COMMENT '实例版本',
  `inst_status` varchar(1) DEFAULT '1' COMMENT '实例状态',
  `inst_reboot_flag` varchar(1) DEFAULT 'N' COMMENT '是否自启动',
  `is_rds` varchar(1) DEFAULT 'N' COMMENT '是否为RDS',
  `is_pxc` varchar(1) DEFAULT 'N' COMMENT '是否为PXC',
  `mgr_user` varchar(20) DEFAULT NULL COMMENT '管理员账号',
  `mgr_pass` varchar(300) DEFAULT NULL COMMENT '管理员密码',
  `created_date` datetime DEFAULT NULL COMMENT '创建时间',
  `api_server` varchar(100) DEFAULT NULL COMMENT 'API服务',
  `python3_home` varchar(100) DEFAULT NULL COMMENT 'PYTHON3目录',
  `script_path` varchar(100) DEFAULT NULL COMMENT '代理路径',
  `script_file` varchar(100) DEFAULT NULL COMMENT '代理文件名',
  `last_update_date` datetime DEFAULT NULL COMMENT '最近更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_inst_log` */

DROP TABLE IF EXISTS `t_db_inst_log`;

CREATE TABLE `t_db_inst_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `inst_id` int(11) DEFAULT NULL COMMENT '实例ID',
  `type` varchar(20) DEFAULT NULL COMMENT '日志类型',
  `message` varchar(1000) DEFAULT NULL COMMENT '日志消息',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_inst_opt_log` */

DROP TABLE IF EXISTS `t_db_inst_opt_log`;

CREATE TABLE `t_db_inst_opt_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` int(11) DEFAULT NULL COMMENT '用户ID',
  `inst_id` int(11) DEFAULT NULL COMMENT '实例ID',
  `db` varchar(50) DEFAULT NULL COMMENT '数据库名称',
  `statement` text COMMENT 'SQL语句',
  `start_time` varchar(20) DEFAULT NULL COMMENT '开始时间',
  `end_time` varchar(20) DEFAULT NULL COMMENT '完成时间',
  `status` varchar(1) DEFAULT NULL COMMENT '执行状态',
  `message` text COMMENT '错误消息',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_inst_parameter` */

DROP TABLE IF EXISTS `t_db_inst_parameter`;

CREATE TABLE `t_db_inst_parameter` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `inst_id` int(11) NOT NULL COMMENT '实例ID',
  `name` varchar(50) DEFAULT NULL COMMENT '参数名',
  `value` varchar(100) DEFAULT NULL COMMENT '参数值',
  `type` varchar(1000) DEFAULT NULL COMMENT '参数类型',
  `status` varchar(1) DEFAULT NULL COMMENT '参数状态',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `last_update_date` datetime DEFAULT NULL COMMENT '最近更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_inst_step` */

DROP TABLE IF EXISTS `t_db_inst_step`;

CREATE TABLE `t_db_inst_step` (
  `id` int(11) NOT NULL COMMENT '主键',
  `cmd` varchar(2000) DEFAULT NULL COMMENT '操作命令',
  `message` varchar(200) DEFAULT NULL COMMENT '操作消息',
  `version` varchar(20) DEFAULT NULL COMMENT '版本',
  `flag` varchar(1) DEFAULT NULL COMMENT '操作类型',
  `desc` varchar(50) DEFAULT NULL COMMENT '操作描述',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_source` */

DROP TABLE IF EXISTS `t_db_source`;

CREATE TABLE `t_db_source` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `ip` varchar(100) NOT NULL COMMENT '数据库IP',
  `port` varchar(20) NOT NULL COMMENT '数据库端口',
  `service` varchar(40) NOT NULL COMMENT '数据库名称',
  `status` varchar(1) DEFAULT NULL COMMENT '数据源状态',
  `creation_date` date DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(20) DEFAULT NULL COMMENT '创建人',
  `last_update_date` date DEFAULT NULL COMMENT '最近更新时间',
  `updator` varchar(20) DEFAULT NULL COMMENT '更新人',
  `user` varchar(20) DEFAULT NULL COMMENT '用户名',
  `password` varchar(200) DEFAULT NULL COMMENT '密码',
  `db_type` varchar(20) DEFAULT NULL COMMENT '数据库类型',
  `db_source_type` varchar(10) DEFAULT NULL COMMENT '？',
  `db_desc` varchar(40) DEFAULT NULL COMMENT '数据源描述',
  `db_env` varchar(1) DEFAULT NULL COMMENT '数据库环境',
  `inst_type` varchar(10) DEFAULT NULL COMMENT '实例类型',
  `proxy_status` varchar(1) DEFAULT NULL COMMENT '代理状态',
  `proxy_server` varchar(50) DEFAULT NULL COMMENT '代理服务接口',
  `market_id` varchar(10) DEFAULT NULL COMMENT '项目编码',
  `flag1` varchar(100) DEFAULT NULL COMMENT '商管周报',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_sync_config` */

DROP TABLE IF EXISTS `t_db_sync_config`;

CREATE TABLE `t_db_sync_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `sync_ywlx` varchar(11) DEFAULT NULL COMMENT '同步业务类型',
  `comments` varchar(100) DEFAULT NULL COMMENT '任务描述',
  `sync_type` varchar(50) DEFAULT NULL COMMENT '同步数据类型',
  `sync_tag` varchar(100) DEFAULT NULL COMMENT '同步标识',
  `sour_db_id` int(11) DEFAULT NULL COMMENT '源数据源ID',
  `desc_db_id` int(11) DEFAULT NULL COMMENT '目标数据源ID',
  `server_id` int(11) DEFAULT NULL COMMENT '同步服务器ID',
  `run_time` varchar(100) DEFAULT NULL COMMENT '运行时间',
  `sync_schema` varchar(100) DEFAULT NULL COMMENT '源数据库名',
  `sync_schema_dest` varchar(100) DEFAULT NULL COMMENT '目标数据库名',
  `sync_table` varchar(2000) DEFAULT NULL COMMENT '同步表列表',
  `batch_size` int(11) DEFAULT NULL COMMENT '全量批大小',
  `batch_size_incr` int(11) DEFAULT NULL COMMENT '增量批大小',
  `sync_gap` int(11) DEFAULT NULL COMMENT '同步间隔',
  `sync_col_val` varchar(100) DEFAULT NULL COMMENT '同步新增列值',
  `sync_col_name` varchar(50) DEFAULT NULL COMMENT '同步新增列名',
  `sync_repair_day` int(11) DEFAULT '7' COMMENT '自动修复天数',
  `sync_time_type` varchar(50) DEFAULT NULL COMMENT '同步时间类型',
  `script_path` varchar(200) DEFAULT NULL COMMENT '同步代理路径',
  `script_file` varchar(100) DEFAULT NULL COMMENT '同步代理文件名',
  `python3_home` varchar(200) DEFAULT NULL COMMENT 'PYTHON3路径',
  `api_server` varchar(100) DEFAULT NULL COMMENT 'API服务器',
  `status` varchar(1) DEFAULT NULL COMMENT '任务状态',
  PRIMARY KEY (`id`),
  KEY `idx_t_db_config_u1` (`sync_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='数据库同步配置表';

/*Table structure for table `t_db_sync_monitor` */

DROP TABLE IF EXISTS `t_db_sync_monitor`;

CREATE TABLE `t_db_sync_monitor` (
  `market_id` varchar(10) NOT NULL COMMENT '项目ID',
  `market_name` varchar(100) DEFAULT NULL COMMENT '项目名称',
  `flow_flag` varchar(1000) DEFAULT NULL COMMENT '离线客流标识',
  `flow_real_flag` varchar(1000) DEFAULT NULL COMMENT '实时客流标识',
  `flow_device_flag` varchar(1000) DEFAULT NULL COMMENT '客流设备标识',
  `park_flag` varchar(1000) DEFAULT NULL COMMENT '离线车流标识',
  `park_real_flag` varchar(1000) DEFAULT NULL COMMENT '实时车流标识',
  `sales_dldf_flag` varchar(1000) DEFAULT NULL COMMENT '德利多付销售标识',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`market_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_sync_tab_config` */

DROP TABLE IF EXISTS `t_db_sync_tab_config`;

CREATE TABLE `t_db_sync_tab_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `sync_tag` varchar(50) DEFAULT NULL COMMENT '同步标识',
  `db_name` varchar(50) DEFAULT NULL COMMENT '数据库名称',
  `schema_name` varchar(50) DEFAULT NULL COMMENT '数据模式名称',
  `tab_name` varchar(50) DEFAULT NULL COMMENT '表名称',
  `sync_cols` varchar(2000) DEFAULT NULL COMMENT '同步列列表',
  `sync_incr_col` varchar(50) DEFAULT NULL COMMENT '增量同步列',
  `sync_time` varchar(10) DEFAULT NULL COMMENT '同步时间',
  `status` varchar(1) DEFAULT NULL COMMENT '同步状态',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `update_date` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_t_db_sync_tab_config_n1` (`sync_tag`),
  KEY `idx_t_db_sync_tab_config_u1` (`sync_tag`,`db_name`,`schema_name`,`tab_name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_sync_tasks_log` */

DROP TABLE IF EXISTS `t_db_sync_tasks_log`;

CREATE TABLE `t_db_sync_tasks_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `sync_tag` varchar(100) NOT NULL COMMENT '同步标识',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `duration` int(11) DEFAULT NULL COMMENT '同步时长(s)',
  `amount` int(11) DEFAULT NULL COMMENT '同步数量',
  PRIMARY KEY (`id`),
  KEY `idx_create_date_n1` (`create_date`),
  KEY `idx_create_date_u1` (`sync_tag`),
  KEY `idx_sync_tag_create_date` (`sync_tag`,`create_date`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_sync_tasks_log_detail` */

DROP TABLE IF EXISTS `t_db_sync_tasks_log_detail`;

CREATE TABLE `t_db_sync_tasks_log_detail` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `sync_tag` varchar(100) NOT NULL COMMENT '同步标识',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `sync_table` varchar(100) DEFAULT NULL COMMENT '同步表',
  `sync_amount` int(11) DEFAULT NULL COMMENT '同步数量',
  `duration` int(11) DEFAULT NULL COMMENT '同步时长(s)',
  PRIMARY KEY (`id`),
  KEY `idx_create_date_n1` (`create_date`),
  KEY `idx_create_date_u1` (`sync_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_transfer_config` */

DROP TABLE IF EXISTS `t_db_transfer_config`;

CREATE TABLE `t_db_transfer_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `transfer_tag` varchar(100) DEFAULT NULL COMMENT '传输标识',
  `transfer_type` varchar(100) DEFAULT NULL COMMENT '传输类型',
  `server_id` int(11) DEFAULT NULL COMMENT '传输服务器ID',
  `comments` varchar(100) DEFAULT NULL COMMENT '任务描述',
  `sour_db_id` int(11) DEFAULT NULL COMMENT '传输数据源ID',
  `sour_schema` varchar(100) DEFAULT NULL COMMENT '传输数据库名',
  `sour_table` varchar(100) DEFAULT NULL COMMENT '传输表名称',
  `sour_where` varchar(2000) DEFAULT NULL COMMENT '传输表条件',
  `dest_db_id` int(11) DEFAULT NULL COMMENT '目标数据源ID',
  `dest_schema` varchar(100) DEFAULT NULL COMMENT '目标数据库',
  `script_path` varchar(200) DEFAULT NULL COMMENT '传输代理路径',
  `script_file` varchar(100) DEFAULT NULL COMMENT '传输代理文件名',
  `batch_size` int(11) DEFAULT NULL COMMENT '传输批大小',
  `python3_home` varchar(200) DEFAULT NULL COMMENT 'PYTHON3路径',
  `api_server` varchar(100) DEFAULT NULL COMMENT 'API服务器',
  `status` varchar(1) DEFAULT NULL COMMENT '任务状态',
  PRIMARY KEY (`id`),
  KEY `idx_t_db_transfer_config_u1` (`transfer_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_transfer_log` */

DROP TABLE IF EXISTS `t_db_transfer_log`;

CREATE TABLE `t_db_transfer_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `transfer_tag` varchar(100) DEFAULT NULL COMMENT '传输类型',
  `table_name` varchar(100) DEFAULT NULL COMMENT '表名称',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `duration` int(11) DEFAULT NULL COMMENT '传输时长',
  `amount` int(11) DEFAULT NULL COMMENT '传输数量',
  `percent` decimal(10,2) DEFAULT NULL COMMENT '传输进度',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_user` */

DROP TABLE IF EXISTS `t_db_user`;

CREATE TABLE `t_db_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `inst_id` varchar(50) DEFAULT NULL COMMENT '实例ID',
  `db_user` varchar(50) DEFAULT NULL COMMENT '用户名',
  `db_pass` varchar(100) DEFAULT NULL COMMENT '密码',
  `user_dbs` text COMMENT '数据库名称列表',
  `user_privs` text COMMENT '数据库权限列表',
  `statement` text COMMENT '创建用户语句',
  `status` varchar(1) DEFAULT NULL COMMENT '用户状态',
  `description` varchar(100) DEFAULT NULL COMMENT '用户描述',
  `created_date` datetime DEFAULT NULL COMMENT '创建时间',
  `last_update_date` datetime DEFAULT NULL COMMENT '最近更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_weekly_items` */

DROP TABLE IF EXISTS `t_db_weekly_items`;

CREATE TABLE `t_db_weekly_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `item_type` varchar(20) DEFAULT NULL COMMENT '统计项目类型',
  `item_code` varchar(50) DEFAULT NULL COMMENT '项目代码',
  `item_desc` varchar(50) DEFAULT NULL COMMENT '项目描述',
  `item_tjsql` text COMMENT '统计语句',
  `status` varchar(1) DEFAULT NULL COMMENT '项目状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8;

/*Table structure for table `t_dmlx` */

DROP TABLE IF EXISTS `t_dmlx`;

CREATE TABLE `t_dmlx` (
  `dm` varchar(10) NOT NULL COMMENT '大类代码',
  `mc` varchar(100) DEFAULT NULL COMMENT '大类名称',
  `flag` varchar(1) DEFAULT NULL COMMENT '大类状态',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`dm`),
  KEY `idx_t_dmlx` (`dm`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_dmmx` */

DROP TABLE IF EXISTS `t_dmmx`;

CREATE TABLE `t_dmmx` (
  `dm` varchar(10) NOT NULL DEFAULT '' COMMENT '代码大类',
  `dmm` varchar(200) NOT NULL DEFAULT '' COMMENT '代码小类',
  `dmmc` varchar(100) DEFAULT NULL COMMENT '小类名称',
  `flag` varchar(1) DEFAULT NULL COMMENT '小类状态',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`dm`,`dmm`),
  KEY `idx_t_dmmx` (`dm`,`dmm`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_forget_password` */

DROP TABLE IF EXISTS `t_forget_password`;

CREATE TABLE `t_forget_password` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` int(11) DEFAULT NULL COMMENT '用户ID',
  `authentication_string` varchar(100) DEFAULT NULL COMMENT '认证字符串',
  `creation_date` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(20) DEFAULT NULL COMMENT '创建人',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_func` */

DROP TABLE IF EXISTS `t_func`;

CREATE TABLE `t_func` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `func_name` varchar(100) DEFAULT NULL COMMENT '功能名称',
  `func_url` varchar(300) DEFAULT NULL COMMENT '功能URL',
  `priv_id` varchar(100) DEFAULT NULL COMMENT '权限ID',
  `status` varchar(1) DEFAULT NULL COMMENT '状态',
  `creation_date` date DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(20) DEFAULT NULL COMMENT '创建人',
  `last_update_date` date DEFAULT NULL COMMENT '最近更新时间',
  `updator` varchar(20) DEFAULT NULL COMMENT '更新人',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=212 DEFAULT CHARSET=utf8;

/*Table structure for table `t_minio_config` */

DROP TABLE IF EXISTS `t_minio_config`;

CREATE TABLE `t_minio_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `sync_tag` varchar(50) DEFAULT NULL COMMENT '同步标识',
  `sync_type` varchar(1) DEFAULT NULL COMMENT '同步类型',
  `server_id` int(11) DEFAULT NULL COMMENT '同步服务器ID',
  `sync_path` varchar(200) DEFAULT NULL COMMENT '同步路径',
  `sync_service` varchar(200) DEFAULT NULL COMMENT '同步服务名',
  `minio_server` varchar(200) DEFAULT NULL COMMENT 'minio服务名',
  `minio_user` varchar(100) DEFAULT NULL COMMENT 'minio用户',
  `minio_pass` varchar(100) DEFAULT NULL COMMENT 'minio口令',
  `minio_bucket` varchar(100) DEFAULT NULL COMMENT '同步批大小',
  `minio_dpath` varchar(100) DEFAULT NULL COMMENT 'minio下载路径',
  `minio_incr_type` varchar(10) DEFAULT NULL COMMENT '增量同步类型',
  `minio_incr` int(11) DEFAULT NULL COMMENT '增量同步时长',
  `python3_home` varchar(200) DEFAULT NULL COMMENT 'python3路径',
  `script_path` varchar(200) DEFAULT NULL COMMENT 'minio同步代理路径',
  `script_file` varchar(200) DEFAULT NULL COMMENT 'minio同步代理名称',
  `api_server` varchar(100) DEFAULT NULL COMMENT 'api服务地址',
  `run_time` varchar(100) DEFAULT NULL COMMENT '运行时间',
  `comments` varchar(100) DEFAULT NULL COMMENT '任务描述',
  `status` varchar(1) DEFAULT NULL COMMENT '任务状态',
  PRIMARY KEY (`id`),
  KEY `idx_t_minio_config_u1` (`sync_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_minio_log` */

DROP TABLE IF EXISTS `t_minio_log`;

CREATE TABLE `t_minio_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `sync_tag` varchar(50) DEFAULT NULL COMMENT '同步标识',
  `sync_day` int(11) DEFAULT NULL COMMENT '同步最近天数',
  `server_id` int(11) DEFAULT NULL COMMENT '同步服务器ID',
  `download_time` int(11) DEFAULT NULL COMMENT '下载时长',
  `upload_time` int(11) DEFAULT NULL COMMENT '上传时长',
  `total_time` int(11) DEFAULT NULL COMMENT '总时长',
  `transfer_file` int(11) DEFAULT NULL COMMENT '传输文件数',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_index` */

DROP TABLE IF EXISTS `t_monitor_index`;

CREATE TABLE `t_monitor_index` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `index_name` varchar(50) DEFAULT NULL COMMENT '指标名称',
  `index_code` varchar(50) DEFAULT NULL COMMENT '指标代码',
  `index_type` varchar(1) DEFAULT NULL COMMENT '指标类型',
  `index_db_type` varchar(1) DEFAULT NULL COMMENT '指标数据库类型',
  `index_threshold_type` varchar(1) DEFAULT NULL COMMENT '指标阀值类型',
  `index_threshold` varchar(10) DEFAULT NULL COMMENT '指标阀值',
  `index_threshold_day` varchar(10) DEFAULT NULL COMMENT '指标阀值天数',
  `index_threshold_times` varchar(3) DEFAULT NULL COMMENT '指标阀值倍数',
  `status` varchar(1) DEFAULT NULL COMMENT '指标状态',
  `trigger_time` int(11) DEFAULT NULL COMMENT '触发时间',
  `trigger_times` int(11) DEFAULT NULL COMMENT '触发次数',
  PRIMARY KEY (`id`),
  KEY `idx_t_monitor_index_u1` (`index_code`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_server_warn_log` */

DROP TABLE IF EXISTS `t_monitor_server_warn_log`;

CREATE TABLE `t_monitor_server_warn_log` (
  `server_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '服务器ID',
  `server_desc` varchar(100) DEFAULT NULL COMMENT '服务器描述',
  `index_code` varchar(50) NOT NULL COMMENT '指标代码',
  `index_name` varchar(100) DEFAULT NULL COMMENT '指标名称',
  `index_value` varchar(100) DEFAULT NULL COMMENT '指标值',
  `fail_times` int(11) DEFAULT NULL COMMENT '失败次数',
  `succ_times` int(11) DEFAULT NULL COMMENT '成功次数',
  `is_send_rcv_mail` varchar(10) DEFAULT NULL COMMENT '是否发送邮件',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`server_id`,`index_code`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_service` */

DROP TABLE IF EXISTS `t_monitor_service`;

CREATE TABLE `t_monitor_service` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `server_id` int(11) DEFAULT NULL COMMENT '服务器ID',
  `server_desc` varchar(1000) DEFAULT NULL COMMENT '服务器描述',
  `mysql_proj` varchar(1000) DEFAULT NULL COMMENT 'mysql数据源信息',
  `mssql_park` varchar(1000) DEFAULT NULL COMMENT 'mssql车流数据源信息',
  `mssql_flow` varchar(1000) DEFAULT NULL COMMENT 'mssql客流数据源信息',
  `mssql_car` varchar(1000) DEFAULT NULL COMMENT 'mssql反向寻车数据源信息',
  `mssql_dldf` varchar(1000) DEFAULT NULL COMMENT 'mssql德利多付数据源信息',
  `mssql_sg` varchar(1000) DEFAULT NULL COMMENT 'mssql商管数据源信息',
  `oracle_sg` varchar(1000) DEFAULT NULL COMMENT 'oracle商管数据源信息',
  `redis` varchar(1000) DEFAULT NULL COMMENT 'redis数据源信息',
  `mongo` varchar(1000) DEFAULT NULL COMMENT 'mongo数据源信息',
  `es` varchar(1000) DEFAULT NULL COMMENT 'es数据源信息',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `sxh` bigint(20) DEFAULT NULL COMMENT '顺序号',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_task` */

DROP TABLE IF EXISTS `t_monitor_task`;

CREATE TABLE `t_monitor_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `task_tag` varchar(50) DEFAULT NULL COMMENT '任务标识',
  `server_id` varchar(20) DEFAULT NULL COMMENT '服务器ID',
  `templete_id` varchar(20) DEFAULT NULL COMMENT '模板ID',
  `db_id` varchar(20) DEFAULT NULL COMMENT '数据源ID',
  `comments` varchar(50) DEFAULT NULL COMMENT '任务描述',
  `run_time` varchar(20) DEFAULT NULL COMMENT '运行时间',
  `script_path` varchar(200) DEFAULT NULL COMMENT '代理路径',
  `script_file` varchar(100) DEFAULT NULL COMMENT '代理文件名',
  `python3_home` varchar(200) DEFAULT NULL COMMENT 'python3路径',
  `api_server` varchar(100) DEFAULT NULL COMMENT 'api服务地址',
  `status` varchar(1) DEFAULT NULL COMMENT '任务状态',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_t_monitor_task_u1` (`task_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_task_db_log` */

DROP TABLE IF EXISTS `t_monitor_task_db_log`;

CREATE TABLE `t_monitor_task_db_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `task_tag` varchar(50) DEFAULT NULL COMMENT '任务标识',
  `server_id` int(11) DEFAULT NULL COMMENT '服务器ID',
  `db_id` int(11) DEFAULT NULL COMMENT '数据源ID',
  `total_connect` varchar(11) DEFAULT NULL COMMENT '总连接数',
  `active_connect` varchar(11) DEFAULT NULL COMMENT '活跃连接数',
  `db_available` varchar(20) DEFAULT NULL COMMENT '数据库是否可用',
  `db_tbs_usage` varchar(200) DEFAULT NULL COMMENT '表空间使用率',
  `db_qps` varchar(200) DEFAULT NULL COMMENT 'QPS',
  `db_tps` varchar(200) DEFAULT NULL COMMENT 'TPS',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_t_monitor_task_db_log_n1` (`create_date`),
  KEY `idx_t_monitor_task_db_log_c1` (`db_id`,`create_date`),
  KEY `idx_t_monitor_task_db_log_n2` (`server_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_task_server_log` */

DROP TABLE IF EXISTS `t_monitor_task_server_log`;

CREATE TABLE `t_monitor_task_server_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `task_tag` varchar(50) DEFAULT NULL COMMENT '任务标识',
  `server_id` int(11) DEFAULT NULL COMMENT '服务器ID',
  `cpu_total_usage` varchar(500) DEFAULT NULL COMMENT 'CPU使用率汇总',
  `cpu_core_usage` varchar(500) DEFAULT NULL COMMENT 'CPU使用率分核',
  `mem_usage` varchar(50) DEFAULT NULL COMMENT '内存使用率',
  `disk_usage` varchar(200) DEFAULT NULL COMMENT '磁盘使用率',
  `disk_read` varchar(20) DEFAULT NULL COMMENT '磁盘读(kb)',
  `disk_write` varchar(20) DEFAULT NULL COMMENT '磁盘写(kb)',
  `net_in` varchar(20) DEFAULT NULL COMMENT '网络流入(kb)',
  `net_out` varchar(20) DEFAULT NULL COMMENT '网络流出(kb)',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `market_id` varchar(10) DEFAULT NULL COMMENT '项目ID',
  PRIMARY KEY (`id`),
  KEY `idx_t_monitor_task_server_log_n1` (`create_date`),
  KEY `idx_t_monitor_task_server_log_n2` (`server_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_templete` */

DROP TABLE IF EXISTS `t_monitor_templete`;

CREATE TABLE `t_monitor_templete` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(20) DEFAULT NULL COMMENT '模板名称',
  `code` varchar(20) DEFAULT NULL COMMENT '模板代码',
  `type` varchar(20) DEFAULT NULL COMMENT '模板类型',
  `status` varchar(1) DEFAULT NULL COMMENT '模板状态',
  `creation_date` date DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(20) DEFAULT NULL COMMENT '创建人',
  `last_update_date` date DEFAULT NULL COMMENT '更新时间',
  `updator` varchar(20) DEFAULT NULL COMMENT '更新人',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_t_monitor_templete_u1` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_templete_index` */

DROP TABLE IF EXISTS `t_monitor_templete_index`;

CREATE TABLE `t_monitor_templete_index` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `templete_id` int(11) NOT NULL COMMENT '模板ID',
  `index_id` varchar(20) DEFAULT NULL COMMENT '指标ID',
  `creation_date` date DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(20) DEFAULT NULL COMMENT '创建人',
  `last_update_date` date DEFAULT NULL COMMENT '更新时间',
  `updator` varchar(20) DEFAULT NULL COMMENT '更新人',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_warn_log` */

DROP TABLE IF EXISTS `t_monitor_warn_log`;

CREATE TABLE `t_monitor_warn_log` (
  `server_id` int(11) NOT NULL DEFAULT '0' COMMENT '服务器ID',
  `server_desc` varchar(100) DEFAULT NULL COMMENT '服务器描述',
  `db_id` int(11) NOT NULL DEFAULT '0' COMMENT '数据源ID',
  `db_desc` varchar(100) DEFAULT NULL COMMENT '数据源描述',
  `fail_times` int(11) DEFAULT NULL COMMENT '失败次数',
  `succ_times` int(11) DEFAULT NULL COMMENT '成功次数',
  `is_send_rcv_mail` varchar(10) DEFAULT NULL COMMENT '是否发送邮件',
  `warn_type` varchar(20) DEFAULT NULL COMMENT '告警类型',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`server_id`,`db_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_port` */

DROP TABLE IF EXISTS `t_port`;

CREATE TABLE `t_port` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `market_id` int(11) DEFAULT NULL COMMENT '项目ID',
  `market_name` varchar(100) DEFAULT NULL COMMENT '项目名称',
  `app_desc` varchar(100) DEFAULT NULL COMMENT '应用描述',
  `local_ip` varchar(20) DEFAULT NULL COMMENT '应用IP',
  `local_port` varchar(10) DEFAULT NULL COMMENT '应用PORT',
  `mapping_port` varchar(10) DEFAULT NULL COMMENT '映射PORT',
  `mapping_domain` varchar(50) DEFAULT NULL COMMENT '映射域名',
  `mapping_type` varchar(1) DEFAULT NULL COMMENT '映射类型',
  `creater` varchar(20) DEFAULT NULL COMMENT '创建人',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `update_date` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_role` */

DROP TABLE IF EXISTS `t_role`;

CREATE TABLE `t_role` (
  `id` int(11) NOT NULL COMMENT '主键',
  `name` varchar(20) DEFAULT NULL COMMENT '角色名称',
  `status` varchar(1) DEFAULT NULL COMMENT '角色状态',
  `creation_date` date DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(20) DEFAULT NULL COMMENT '创建人',
  `last_update_date` date DEFAULT NULL COMMENT '更新时间',
  `updator` varchar(20) DEFAULT NULL COMMENT '更新人',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_role_func_privs` */

DROP TABLE IF EXISTS `t_role_func_privs`;

CREATE TABLE `t_role_func_privs` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `role_id` varchar(100) DEFAULT NULL COMMENT '角色ID',
  `func_id` varchar(100) DEFAULT NULL COMMENT '功能ID',
  `creation_date` date DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(20) DEFAULT NULL COMMENT '创建人',
  `last_update_date` date DEFAULT NULL COMMENT '更新时间',
  `updator` varchar(20) DEFAULT NULL COMMENT '更新人',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_role_privs` */

DROP TABLE IF EXISTS `t_role_privs`;

CREATE TABLE `t_role_privs` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `role_id` int(11) NOT NULL COMMENT '角色ID',
  `priv_id` varchar(20) DEFAULT NULL COMMENT '权限ID',
  `creation_date` date DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(20) DEFAULT NULL COMMENT '创建人',
  `last_update_date` date DEFAULT NULL COMMENT '更新时间',
  `updator` varchar(20) DEFAULT NULL COMMENT '更新人',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

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
  `flag1` varchar(100) DEFAULT NULL COMMENT '商管周报',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=148 DEFAULT CHARSET=utf8;

/*Table structure for table `t_slow_detail` */

DROP TABLE IF EXISTS `t_slow_detail`;

CREATE TABLE `t_slow_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `inst_id` int(11) DEFAULT NULL COMMENT '实例ID',
  `sql_id` varchar(100) NOT NULL COMMENT 'SQL标识',
  `templete_id` varchar(100) NOT NULL COMMENT '模板ID',
  `finish_time` datetime DEFAULT NULL COMMENT '完成时间',
  `USER` varchar(50) DEFAULT NULL COMMENT '数据库用户',
  `HOST` varchar(50) DEFAULT NULL COMMENT '主机名',
  `IP` varchar(50) DEFAULT NULL COMMENT '连接IP',
  `thread_id` varchar(50) DEFAULT NULL COMMENT '线程ID',
  `query_time` decimal(20,10) DEFAULT NULL COMMENT '查询时长',
  `lock_time` decimal(20,10) DEFAULT NULL COMMENT '锁定时长',
  `rows_sent` varchar(50) DEFAULT NULL COMMENT '发送行大小',
  `rows_examined` varchar(50) DEFAULT NULL COMMENT '扫描行大小',
  `db` varchar(50) DEFAULT NULL COMMENT '数据库名',
  `cmd` varchar(50) DEFAULT NULL COMMENT '命令类型',
  `finger` longtext COMMENT 'SQL语句(变量)',
  `sql_text` longtext COMMENT '原始SQL',
  `bytes` varchar(50) DEFAULT NULL COMMENT 'SQL大小',
  `pos_in_log` varchar(50) DEFAULT NULL COMMENT 'binlog位置',
  PRIMARY KEY (`id`),
  KEY `idx_t_slow_detail_n1` (`sql_id`),
  KEY `idx_t_slow_detail_n2` (`inst_id`,`finish_time`,`db`),
  KEY `idx_t_slow_detail_n3` (`inst_id`,`finish_time`,`USER`),
  KEY `idx_t_slow_detail_n4` (`finish_time`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_slow_log` */

DROP TABLE IF EXISTS `t_slow_log`;

CREATE TABLE `t_slow_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `inst_id` int(11) NOT NULL COMMENT '实例ID',
  `server_id` int(11) DEFAULT NULL COMMENT '服务器ID',
  `log_file` varchar(200) DEFAULT NULL COMMENT '慢日志文件名',
  `query_time` int(11) DEFAULT NULL COMMENT '慢时间时长',
  `python3_home` varchar(100) DEFAULT NULL COMMENT 'python3目录',
  `run_time` varchar(100) DEFAULT NULL COMMENT '运行时间',
  `exec_time` varchar(100) DEFAULT NULL COMMENT '执行频率',
  `script_path` varchar(100) DEFAULT NULL COMMENT '代理路径',
  `script_file` varchar(100) DEFAULT NULL COMMENT '代理文件',
  `STATUS` varchar(1) DEFAULT NULL COMMENT '任务状态',
  `api_server` varchar(50) DEFAULT NULL COMMENT 'API服务',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `last_update_date` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_sql_audit_rule` */

DROP TABLE IF EXISTS `t_sql_audit_rule`;

CREATE TABLE `t_sql_audit_rule` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `rule_type` varchar(50) DEFAULT NULL COMMENT '规则类型',
  `rule_code` varchar(50) DEFAULT NULL COMMENT '规则代码',
  `rule_name` varchar(100) DEFAULT NULL COMMENT '规则名称',
  `rule_value` varchar(100) DEFAULT NULL COMMENT '规则值',
  `error` varchar(100) DEFAULT NULL COMMENT '错误消息',
  `status` varchar(1) DEFAULT NULL COMMENT '是否启用',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_t_sql_audit_rule_u1` (`rule_code`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8;

/*Table structure for table `t_sql_audit_rule_err` */

DROP TABLE IF EXISTS `t_sql_audit_rule_err`;

CREATE TABLE `t_sql_audit_rule_err` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `xh` int(11) DEFAULT NULL COMMENT '序号',
  `rule_id` varchar(100) DEFAULT NULL COMMENT '规则ID',
  `rule_name` varchar(100) DEFAULT NULL COMMENT '规则名称',
  `rule_value` varchar(100) DEFAULT NULL COMMENT '规则值',
  `user_id` int(11) DEFAULT NULL COMMENT '用户ID',
  `obj_name` varchar(100) DEFAULT NULL COMMENT '对象ID',
  `error` text COMMENT '错误消息',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_sql_release` */

DROP TABLE IF EXISTS `t_sql_release`;

CREATE TABLE `t_sql_release` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `dbid` int(11) NOT NULL COMMENT '数据源ID',
  `db` varchar(50) DEFAULT NULL COMMENT '数据库名称',
  `sqltext` longtext COMMENT 'SQL文本',
  `status` varchar(1) DEFAULT NULL COMMENT '0:已发布,1:审核成功，2:审核失败,3:执行成功，4：执行失败',
  `message` varchar(2000) DEFAULT NULL COMMENT '发部消息',
  `creation_date` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(20) DEFAULT NULL COMMENT '创建人',
  `last_update_date` datetime DEFAULT NULL COMMENT '更新时间',
  `updator` varchar(20) DEFAULT NULL COMMENT '更新人',
  `audit_date` datetime DEFAULT NULL COMMENT '审核时间',
  `auditor` varchar(20) DEFAULT NULL COMMENT '审核人',
  `audit_message` varchar(100) DEFAULT NULL COMMENT '审核消息',
  `version` varchar(20) DEFAULT NULL COMMENT '版本',
  `type` varchar(1) DEFAULT NULL COMMENT '类型',
  `executor` varchar(20) DEFAULT NULL COMMENT '执行人',
  `exec_start` datetime DEFAULT NULL COMMENT '开始时间',
  `exec_end` datetime DEFAULT NULL COMMENT '完成时间',
  `error` varchar(1000) DEFAULT NULL COMMENT '错误消息',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_sql_release_results` */

DROP TABLE IF EXISTS `t_sql_release_results`;

CREATE TABLE `t_sql_release_results` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `release_id` int(11) DEFAULT NULL COMMENT '发送ID',
  `db_env` varchar(1) DEFAULT NULL COMMENT '数据库环境',
  `db_status` varchar(1) DEFAULT NULL COMMENT '数据库状态',
  `db_msg` varchar(100) DEFAULT NULL COMMENT '数据库消息',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_sys_stats_idx` */

DROP TABLE IF EXISTS `t_sys_stats_idx`;

CREATE TABLE `t_sys_stats_idx` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `idx_name` varchar(50) DEFAULT NULL COMMENT '指标名',
  `idx_sql` varchar(2000) DEFAULT NULL COMMENT '指标SQL',
  PRIMARY KEY (`id`),
  KEY `idx_t_sys_stats_idx_u1` (`idx_name`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8 COMMENT='指标统计表';

/*Table structure for table `t_templete` */

DROP TABLE IF EXISTS `t_templete`;

CREATE TABLE `t_templete` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `templete_id` int(11) DEFAULT NULL COMMENT '模板ID',
  `contents` text COMMENT '模板内容',
  `description` varchar(100) DEFAULT NULL COMMENT '模板描述',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

/*Table structure for table `t_user` */

DROP TABLE IF EXISTS `t_user`;

CREATE TABLE `t_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户ID(主键)',
  `name` varchar(20) DEFAULT NULL COMMENT '用户名称',
  `wkno` varchar(20) DEFAULT NULL COMMENT '员工编号',
  `gender` varchar(2) DEFAULT NULL COMMENT '性别',
  `email` varchar(40) DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机',
  `project_group` varchar(1) DEFAULT NULL COMMENT '项目组',
  `dept` varchar(20) DEFAULT NULL COMMENT '部门',
  `expire_date` date DEFAULT NULL COMMENT '过期时间',
  `password` varchar(200) DEFAULT NULL COMMENT '口令',
  `status` varchar(1) DEFAULT NULL COMMENT '状态',
  `creation_date` date DEFAULT NULL COMMENT '创建日期',
  `creator` varchar(20) DEFAULT NULL COMMENT '创建人',
  `last_update_date` date DEFAULT NULL COMMENT '更新时间',
  `updator` varchar(20) DEFAULT NULL COMMENT '更新人',
  `login_name` varchar(20) DEFAULT NULL COMMENT '登陆名',
  `file_path` varchar(200) DEFAULT NULL COMMENT '图标路径',
  `file_name` varchar(100) DEFAULT NULL COMMENT '图标名称',
  PRIMARY KEY (`id`),
  KEY `idx_login_name_n1` (`login_name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_user_proj_privs` */

DROP TABLE IF EXISTS `t_user_proj_privs`;

CREATE TABLE `t_user_proj_privs` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `proj_id` int(11) DEFAULT NULL COMMENT '项目ID',
  `user_id` int(11) DEFAULT NULL COMMENT '用户ID',
  `priv_id` int(11) DEFAULT NULL COMMENT '权限ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_user_role` */

DROP TABLE IF EXISTS `t_user_role`;

CREATE TABLE `t_user_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `role_id` int(11) NOT NULL COMMENT '角色ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_wtd` */

DROP TABLE IF EXISTS `t_wtd`;

CREATE TABLE `t_wtd` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `order_no` varchar(50) NOT NULL COMMENT '问题单编号',
  `order_env` varchar(50) NOT NULL COMMENT '问题单环境',
  `order_type` varchar(50) DEFAULT NULL COMMENT '问题单类型',
  `order_status` varchar(50) DEFAULT NULL COMMENT '问题单状态',
  `order_handler` varchar(50) DEFAULT NULL COMMENT '处理人',
  `order_desc` varchar(1000) DEFAULT NULL COMMENT '问题单描述',
  `creator` varchar(50) DEFAULT NULL COMMENT '创建人',
  `create_date` datetime DEFAULT NULL COMMENT '创建日期',
  `handler_date` datetime DEFAULT NULL COMMENT '处理时间',
  `attachment_path` varchar(1000) DEFAULT NULL COMMENT '附件路径',
  `attachment_name` varchar(1000) DEFAULT NULL COMMENT '附件名称',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_order_no_u1` (`order_no`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*Table structure for table `t_xtqx` */

DROP TABLE IF EXISTS `t_xtqx`;

CREATE TABLE `t_xtqx` (
  `id` varchar(10) NOT NULL DEFAULT '' COMMENT '权限ID(主键)',
  `name` varchar(20) DEFAULT NULL COMMENT '权限名称',
  `parent_id` varchar(10) DEFAULT NULL COMMENT '父权限ID',
  `url` varchar(100) DEFAULT NULL COMMENT '后端URL地址',
  `url_front` varchar(100) DEFAULT NULL COMMENT '前端访问地址',
  `status` varchar(1) DEFAULT NULL COMMENT '菜单状态',
  `icon` varchar(50) DEFAULT NULL COMMENT '菜单图标',
  `creation_date` date DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(20) DEFAULT NULL COMMENT '创建人',
  `last_update_date` date DEFAULT NULL COMMENT '更新时间',
  `updator` varchar(20) DEFAULT NULL COMMENT '更新人',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_role_privs` */

DROP TABLE IF EXISTS `t_role_privs`;

CREATE TABLE `t_role_privs` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `role_id` int(11) NOT NULL COMMENT '角色ID',
  `priv_id` varchar(20) DEFAULT NULL COMMENT '权限ID',
  `creation_date` date DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(20) DEFAULT NULL COMMENT '创建人',
  `last_update_date` date DEFAULT NULL COMMENT '更新时间',
  `updator` varchar(20) DEFAULT NULL COMMENT '更新人',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;


/*Data for the table `t_dmlx` */

insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('01','部门','1','2020-05-11 09:14:29','2020-05-14 15:28:20');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('02','数据源类型','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('03','数据库环境','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('04','性别','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('05','项目编码','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('06','服务器类型','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('07','数据库实例类型','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('08','同步业务类型','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('09','同步数据类型','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('10','同步时间类型','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('11','数据源类型','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('12','版本号','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('13','工单类型','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('14','测试大类','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('15','zookeeper地址','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('16','hbase thrift接口地址','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('17','工单类型','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('18','项目组','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('19','工单状态','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('20','归档时间类型','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('21','归档策略','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('22','迁移策略','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('23','指标类型','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('24','阀值类型','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('25','数据库用户状态','1','2020-05-11 09:14:29','2020-05-11 09:14:29');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('26','数据源代理','1','2020-07-28 17:09:43','2020-07-28 17:09:43');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('27','mysql版本','1','2020-07-29 13:58:41','2020-07-29 13:58:41');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('28','数据库实例sql状态','1','2020-07-30 17:20:10','2020-07-30 17:20:10');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('29','数据库-控制台-SQL状态','1','2020-08-05 17:34:20','2020-08-05 17:34:20');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('30','mysql5.6配置文件','1','2020-08-06 14:32:50','2020-08-06 14:32:50');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('31','mysql5.6权限列表','1','2020-08-06 14:32:50','2020-08-06 14:32:50');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('32','mysql实例状态','1','2020-08-17 18:05:36','2020-08-17 18:05:38');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('33','mysql下载目录','1','2020-08-19 17:38:31','2020-08-19 17:38:31');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('34','MinIO同步类型','1','2020-09-21 11:07:03','2020-09-21 11:07:03');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('35','端口映射类型','1','2020-11-13 11:31:56','2020-11-13 11:31:56');
insert  into `t_dmlx`(`dm`,`mc`,`flag`,`create_time`,`update_time`) values ('36','数据库代理本地端口','1','2020-11-21 13:37:43','2020-11-21 13:37:45');

/*Data for the table `t_dmmx` */

insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('01','01','研发部','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('01','02','测试部','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('01','03','项目部','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('01','04','人力部','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('01','05','行政部','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('01','06','平台组','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('01','07','实施组','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('02','0','mysql','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('02','1','oracle','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('02','2','mssql','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('02','3','postgresql','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('02','4','elasticsearch','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('02','5','redis','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('02','6','mongodb','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('02','7','mysql-pxc','1','2020-10-29 08:54:58','2020-10-29 08:55:01');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('03','1','生产环境','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('03','2','测试环境','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('03','3','开发环境','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('03','4','预生产环境','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('03','5','大数据环境','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('03','6','平台组环境','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('03','7','克隆环境','1','2020-11-18 10:03:22','2020-11-18 10:03:24');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('04','1','男','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('04','2','女','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('05','000','测试项目一','2','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('05','001','测试项目二','2','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('06','1','备份服务器','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('06','2','同步服务器','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('06','3','数据库服务器','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('06','4','应用服务器','1','2020-07-16 15:14:18','2020-07-16 15:14:18');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('07','1','ECS','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('07','2','RDS','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('08','1','离线客流','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('08','10','CMS数据','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('08','11','商户数据','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('08','12','卡券数据','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('08','13','订单数据','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('08','14','水单数据','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('08','15','好房业务','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('08','16','dataX同步','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('08','17','店铺商户关系','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('08','18','BI统计','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('08','19','收费员收费口','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('08','2','实时客流','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('08','3','离线车流','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('08','4','实时车流','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('08','5','客流设备','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('08','6','反向寻车','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('08','7','收费员结算','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('08','8','业绩上报','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('08','9','会员数据','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('09','1','mssql->mysql','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('09','2','mysql->mysql','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('09','3','mssql->mssql','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('09','4','mongo->mongo','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('09','5','mysql->hbase','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('09','6','mysql->elasticsearch','1','2020-10-26 14:50:49','2020-10-26 14:50:52');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('10','day','天','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('10','hour','小时','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('10','min','分','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('11','1','备份数据源','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('11','2','同步数据源','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('12','1','V3.7.5','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('12','2','V3.7.6','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('13','1','DDL工单','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('13','2','DML工单','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('13','3','DCL工单','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('13','4','存储过程','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('15','10.2.39.165:2181,10.2.39.166:2181,10.2.39.182:2181','大数据开发zookeeper地址','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('15','10.2.39.84:2181,10.2.39.89:2181,10.2.39.67:2181','大数据测试zookeeper地址','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('15','192.168.100.63:2181,192.168.100.64:2181,192.168.100.69:2181','大数据生产zookeeper地址','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('16','10.2.39.165:9090','大数据开发thrift接口地址','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('16','10.2.39.84:9090','大数据测试thrift接口地址','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('16','192.168.100.63:9090','大数据生产thrift接口地址','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('17','1','数据传输','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('17','2','数据同步','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('17','3','账号权限','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('17','4','数据迁移','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('17','5','主从同步','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('17','6','数据备份','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('17','7','查询支持  ','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('17','8','查询优化','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('17','9','其它类型','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('18','1','研发中心','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('18','2','大数据平台','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('19','1','已新增','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('19','2','已发布','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('19','3','处理中','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('19','4','已完成','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('19','5','已驳回','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('19','6','已转派','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('19','7','已撤销','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('19','8','已关闭','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('20','1','hour','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('20','2','day','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('20','3','month','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('21','1','删除','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('21','2','迁移','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('22','1','周期','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('22','2','范围','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('23','1','服务器','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('23','2','数据库','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('24','1','百分比','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('24','2','计算型','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('24','3','标量值','1','2020-05-11 09:15:35','2020-05-11 09:15:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('25','1','正常','1','2020-05-14 18:57:14','2020-05-14 18:57:20');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('25','2','  停用','1','2020-05-14 18:57:17','2020-05-14 18:57:22');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('25','3','锁定','1','2020-05-15 11:27:57','2020-05-15 11:27:57');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('26','10.16.33.10:8888','北京合生广场代理服务','1','2020-11-12 10:39:41','2020-11-12 10:39:44');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('26','10.16.34.14:8888','北京朝阳合生汇代理服务','1','2020-11-02 14:26:59','2020-11-02 14:27:01');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('26','10.19.53.205:8888','广州南方花园代理服务','1','2020-11-12 10:53:08','2020-11-12 10:53:12');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('26','10.19.72.205:8888','广州合生骏景广场代理服务','1','2020-11-12 10:53:05','2020-11-12 10:53:10');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('26','10.25.128.84:8888','广州嘉和南代理服务','1','2020-07-28 17:11:15','2020-07-28 17:11:53');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('26','10.28.8.233:8888','成都珠江广场代理服务','1','2020-11-12 10:20:44','2020-11-12 10:20:46');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('26','10.5.232.214:8888','广州增城合生汇代理服务','1','2020-11-12 14:16:18','2020-11-12 14:16:20');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('26','10.5.3.26:8888','上海青浦米格代理服务','1','2020-11-12 10:29:51','2020-11-12 10:29:53');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('26','10.61.101.241:8888','上海五角场代理服务','1','2020-11-05 10:29:46','2020-11-05 10:29:48');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('26','39.106.226.140:8888','合生通生产业务库代理服务','1','2020-11-18 16:31:40','2020-11-18 16:31:42');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('26','47.94.197.105:8888','阿里云中转库代理服务','1','2020-11-12 14:33:15','2020-11-12 14:33:17');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('26','bjcfpark.hopsontong.com:60138','北京合生财富广场代理服务','1','2020-11-21 13:28:05','2020-11-21 13:28:07');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('26','bjdespark.hopsontong.com:60128','北京德胜合生财富广场代理服务','1','2020-11-21 13:28:47','2020-11-21 13:28:50');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('26','bjwjqlspark.hopsontong.com:60039','合生新天地代理服务','1','2020-11-21 13:25:55','2020-11-21 13:25:58');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('26','gzyhpark.hopsontong.com:60088','广州越华珠江广场代理服务','1','2020-11-21 13:26:30','2020-11-21 13:26:33');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('26','hzkhpark.hopsontong.com:60016','科华数码广场有限公司代理服务','1','2020-11-21 13:30:18','2020-11-21 13:30:20');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('26','shhytpark.hopsontong.com:60118','上海海云天合生财富广场代理服务','1','2020-11-21 13:29:23','2020-11-21 13:29:25');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('26','shjazjpark.hopsontong.com:60158','上海静安珠江创意中心代理服务','1','2020-11-21 13:29:45','2020-11-21 13:29:47');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('27','1','5.6','1','2020-07-29 13:59:16','2020-07-29 13:59:16');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('27','2','5.7','1','2020-07-29 13:59:22','2020-07-29 13:59:22');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('28','1','已就绪','1','2020-07-30 17:20:29','2020-07-30 17:20:29');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('28','2','运行中','1','2020-07-30 17:20:35','2020-07-30 17:20:35');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('28','3','已完成','1','2020-07-30 17:20:42','2020-07-30 17:20:42');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('28','4','运行失败','1','2020-07-30 17:20:49','2020-07-30 17:20:49');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','basedir=/usr/local/mysql5.6.44','mysql服务主目录','1','2020-08-06 14:38:30','2020-08-24 14:08:32');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','binlog-format=row','binlog日志格式','1','2020-08-06 14:37:59','2020-08-06 14:37:59');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','character-set-server=utf8mb4','mysql服务端字符集','1','2020-08-06 14:40:02','2020-08-06 14:40:02');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','datadir=/home/hopson/apps/usr/webserver/mysql/data/{}/{}','mysql数据主目录','1','2020-08-06 14:38:44','2020-08-31 16:28:49');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','default-character-set=utf8mb4','客户端字符集','1','2020-08-24 13:33:16','2020-08-24 13:33:16');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','expire_logs_days=7','binlog保留时间(天)','1','2020-08-06 14:37:12','2020-08-06 14:37:12');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','innodb_buffer_pool_size=4G','innodb缓存池大小','1','2020-08-06 14:44:47','2020-08-06 14:44:47');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','innodb_log_buffer_size=8m','innodb日志缓存池大小','1','2020-08-06 14:45:00','2020-08-06 14:45:00');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','innodb_log_file_size=512m','innodb日志文件大小','1','2020-08-06 14:45:11','2020-08-06 14:45:11');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','interactive_timeout=86400','交互等待时间','1','2020-09-30 08:12:43','2020-09-30 08:12:43');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','log-bin=mysql-bin','mysql binlog日志名称','1','2020-08-06 14:36:53','2020-08-06 14:36:53');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','log-error=/home/hopson/apps/usr/webserver/mysql/data/{}/{}/mysql.err','错误日志','1','2020-08-31 16:32:35','2020-08-31 16:52:23');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','log_bin_trust_function_creators=on','开启日志后是否能创建存储过程','1','2020-08-06 14:36:32','2020-09-03 11:12:05');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','lower_case_table_names=1','mysql是否区分大小写','1','2020-08-24 13:30:25','2020-08-24 13:30:25');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','max_allowed_packet=512M','最大网络包大小','1','2020-08-06 14:43:14','2020-09-03 11:35:29');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','max_connections=2000','最大连接数','1','2020-08-06 14:44:30','2020-08-06 14:44:30');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','pid-file=/home/hopson/apps/usr/webserver/mysql/data/{}/{}/mysql{}.pid','mysql进程文件','1','2020-09-01 16:13:33','2020-09-01 16:13:33');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','port={}','端口号','1','2020-08-06 14:39:35','2020-09-01 16:25:16');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','server_id=1','mysql服务id','1','2020-08-06 14:36:05','2020-08-06 14:36:05');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','socket=/home/hopson/apps/usr/webserver/mysql/data/{}/{}/mysql.sock','socket文件名','1','2020-08-06 14:40:33','2020-08-31 16:26:02');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES','sql模式','1','2020-08-06 14:40:56','2020-08-06 14:40:56');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','symbolic-links=0','禁用符号链接','1','2020-08-06 14:39:21','2020-08-06 14:39:21');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','table_definition_cache=16384','表定义缓存的大小','1','2020-08-06 14:44:16','2020-08-06 14:44:16');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','table_open_cache=16384','表高速缓存的大小','1','2020-08-06 14:43:57','2020-08-06 14:43:57');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','transaction_isolation =\'READ-COMMITTED\'','事务隔离级别','1','2020-08-06 14:42:48','2020-08-06 14:42:48');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','user=hopson','mysql服务启动用户','1','2020-08-06 14:39:05','2020-08-06 14:39:05');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('30','wait_timeout=86400','锁等待时间','1','2020-09-30 08:12:31','2020-09-30 08:12:31');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('31','create','创建对象','1','2020-08-06 14:39:05','2020-08-06 14:39:05');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('31','delete','删除操作','1','2020-08-06 14:39:05','2020-08-06 14:39:05');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('31','drop','删除对象','1','2020-08-06 14:39:05','2020-08-06 14:39:05');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('31','insert','插入操作','1','2020-08-06 14:39:05','2020-08-06 14:39:05');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('31','select','查询操作','1','2020-08-06 14:39:05','2020-08-06 14:39:05');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('31','update','更新操作','1','2020-08-06 14:39:05','2020-08-06 14:39:05');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('32','1','未创建','1','2020-08-06 14:39:05','2020-08-06 14:39:05');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('32','2','已创建','1','2020-08-06 14:39:05','2020-08-06 14:39:05');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('32','3','已运行','1','2020-08-06 14:39:05','2020-08-06 14:39:05');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('32','4','已停止','1','2020-08-06 14:39:05','2020-08-06 14:39:05');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('32','5','已销毁','1','2020-09-02 09:50:25','2020-09-02 09:50:25');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('33','http://10.2.39.18/downloads/mysql-5.7.27-linux-glibc2.12-x86_64.tar','mysql5.7_download_url','1','2020-08-19 17:41:51','2020-08-19 17:41:51');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('33','http://124.127.103.190:65480/downloads/mysql-5.6.44-linux-glibc2.12-x86_64.tar.gz','mysql5.6_download_url','1','2020-08-19 17:42:09','2020-09-07 10:36:11');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('34','1','目录同步','1','2020-09-21 11:07:44','2020-09-21 11:07:44');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('34','2','服务同步','1','2020-09-21 11:07:48','2020-09-21 11:07:48');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('35','1','数据库代理','1','2020-11-13 11:32:19','2020-11-13 11:32:19');
insert  into `t_dmmx`(`dm`,`dmm`,`dmmc`,`flag`,`create_time`,`update_time`) values ('36','01','8888','1','2020-11-21 13:38:26','2020-11-21 13:38:28');

/*Data for the table `t_func` */

insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1,'用户管理-用户查询-查询','/user/_query','00101','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (2,'用户管理-用户新增-保存','/user/add/save','00102','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (3,'用户管理-用户新增-上传图片','/user/add/uploadImage','00102','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'用户管理-用户变更-查询','/user/_query','00103','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (6,'用户管理-用户变更-变更','/user/edit','00103','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (7,'用户管理-用户变更-变更-保存','/user/edit/save','00103','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (8,'用户管理-用户变更-删除','/user/edit/del','00103','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (9,'用户管理-项目授权-查询','/project/_query','00104','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (10,'用户管理-项目授权-保存','/project/privs/save','00104','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (11,'角色管理-角色查询-查询','/role/_query','00201','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (12,'角色管理-角色新增-保存','/role/add/save','00202','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (13,'角色管理-角色变更-查询','/role/_query','00203','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (14,'角色管理-角色变更-变更','/role/edit','00203','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (15,'角色管理-角色变更-变更-保存','/role/edit/save','00203','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (16,'角色管理-角色变更-变更-删除','/role/edit/del','00203','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (17,'菜单管理-菜单查询-查询','/menu/_query','00301','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (18,'菜单管理-菜单新增-保存','/menu/add/save','00302','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (19,'菜单管理-菜单变更-变更','/menu/edit','00303','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (20,'菜单管理-菜单变更-变更-保存','/menu/edit/save','00303','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (21,'菜单管理-菜单变更-变更-删除','/menu/edit/del','00303','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (22,'数据源管理-数据源查询-查询','/ds/_query','00401','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (23,'数据源管理-数据源新增-保存','/ds/add/save','00402','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (24,'数据源管理-数据源变更-变更','/ds/edit','00403','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (25,'数据源管理-数据源变更-变更-保存','/ds/edit/save','00403','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (26,'数据源管理-数据源变更-变更-删除','/ds/edit/del','00403','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (27,'数据源管理-数据源测试-测试','/ds/check/valid','00404','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (28,'数据源管理-数据源变更-克隆','/ds/clone','00403','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (29,'数据源管理-数据源变更-克隆-保存','/ds/clone/save','00403','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (30,'服务器管理-服务器查询-查询','/server/_query','00501','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (31,'服务器管理-服务器新增-保存','/server/add/save','00502','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (32,'服务器管理-服务器变更-变更','/server/edit','00503','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (33,'服务器管理-服务器变更-变更-保存','/server/edit/save','00503','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (34,'服务器管理-服务器变更-变更-删除','/server/edit/del','00503','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (35,'数据库备份-新建备份-保存','/backup/add/save','00901','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (36,'数据库备份-备份维护-变更','/backup/edit','00902','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (37,'数据库备份-备份维护-变更-保存','/backup/edit/save','00902','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (38,'数据库备份-备份维护-变更-删除','/backup/edit/del','00902','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (39,'数据库备份-备份维护-变更-推送','/backup/edit/push','00902','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (40,'数据库备份-备份维护-变更-启动','/backup/edit/run','00902','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (41,'数据库备份-备份维护-变更-停止','/backup/edit/stop','00902','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (42,'数据库备份-任务查询-查询','/backup/_query','00903','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (43,'数据库备份-日志查询-查询','/backup/log/_query','00904','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (44,'数据库备份-日志查询-查询-详情','/backup/log/_query/detail','00904','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (45,'数据库备份-日志分析-查询','/backup/log/_analyze','00905','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (46,'数据库备份-日志分析-查询-任务列表','/get/backup/task','00905','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (47,'数据库同步-新建同步-保存','/sync/add/save','01101','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (48,'数据库同步-同步维护-变更','/sync/edit','01102','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (49,'数据库同步-同步维护-变更-保存','/sync/edit/save','01102','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (50,'数据库同步-同步维护-删除','/sync/edit/del','01102','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (51,'数据库同步-同步维护-克隆','/sync/clone','01102','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (52,'数据库同步-同步维护-克隆-保存','/sync/clone/save','01102','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (53,'数据库同步-同步维护-推送','/sync/edit/push','01102','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (54,'数据库同步-同步维护-运行','/sync/edit/run','01102','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (55,'数据库同步-同步维护-停止','/sync/edit/stop','01102','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (56,'数据库传输-新建传输-保存','/transfer/add/save','01201','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (57,'数据库传输-传输查询-查询','/transfer/_query','01202','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (58,'数据库传输-传输查询-查询-详情','/transfer/_query/detail','01202','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (59,'数据库传输-传输维护-变更','/transfer/edit','01203','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (60,'数据库传输-传输维护-变更-保存','/transfer/edit/save','01203','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (61,'数据库传输-传输维护-删除','/transfer/edit/del','01203','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (62,'数据库传输-传输维护-推送','/transfer/edit/push','01203','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (63,'数据库传输-传输维护-启动','/transfer/edit/run','01203','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (64,'数据库传输-传输维护-停止','/transfer/edit/stop','01203','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (65,'数据库传输-传输维护-克隆','/transfer/clone','01203','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (66,'数据库传输-传输维护-克隆-保存','/transfer/clone/save','01203','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (67,'数据库归档-新建归档-保存','/archive/add/save','01301','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (68,'数据库归档-新建归档-获取数据库类型','/ds/get/db/type','01301','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (69,'大数据同步-新增同步-保存','/bigdata/add/save','01501','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (70,'大数据同步-任务查询-查询','/bigdata/_query','01502','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (71,'大数据同步-任务查询-详情','/bigdata/_query/detail','01502','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (72,'大数据同步-任务查询-预览','/bigdata/_query/templete','01502','1','2020-03-18','DBA','2020-07-21','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (73,'大数据同步-任务查询-下载','/bigdata/_query/downloads','01502','1','2020-03-18','DBA','2020-07-21','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (74,'大数据同步-同步维护-变更','/bigdata/edit','01503','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (75,'大数据同步-同步维护-变更-保存','/bigdata/edit/save','01503','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (76,'大数据同步-同步维护-变更-删除','/bigdata/edit/del','01503','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (77,'大数据同步-同步维护-克隆','/bigdata/clone','01503','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (78,'大数据同步-同步维护-克隆-保存','/bigdata/clone/save','01503','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (79,'大数据同步-同步维护-推送','/bigdata/edit/push','01503','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (80,'大数据同步-同步维护-推送全部','/bigdata/edit/pushall','01503','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (81,'大数据同步-同步维护-停止','/bigdata/edit/stop','01503','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (82,'大数据同步-同步维护-运行','/bigdata/edit/run','01503','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (83,'工单管理-我的工单-SQL工单查询','/order/_query','01701','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (84,'工单管理-我的工单-问题单查询','/wtd/_query','01701','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (85,'工单管理-我的工单-问题单查询-详情','/wtd/detail','01701','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (86,'工单管理-我的工单-问题单查询-详情','/wtd/detail','01701','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (87,'工单管理-我的工单-新增','/get/order/no,/wtd/save,/get_order_env,/get_order_type,/get_order_status,/get_order_handler','01701','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (88,'工单管理-我的工单-新增-上传附件','/wtd/save/uploadImage','01701','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (89,'工单管理-我的工单-发布','/wtd/release','01701','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (91,'工单管理-我的工单-变更-保存','/get/order/no,/wtd/update,/get_order_status,/get_order_handler','01701','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (92,'工单管理-我的工单-删除','/wtd/delete','01701','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (93,'工单管理-我的工单-查看附件','/wtd/attachment','01701','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (94,'工单管理-我的工单-获取附件数量','/wtd/attachment/number','01701','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (95,'工单管理-SQL查询-查询','/sql/_query,/get_tree','01702','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (96,'工单管理-SQL发布-发布','/sql/_release,/get_tree','01703','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (97,'工单管理-SQL发布-检测','/sql/_check,/sql/_check/result','01703','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (98,'工单管理-SQL发布-SQL格式化','/sql/_format','01703','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (99,'工单管理-SQL查询-SQL格式化','/sql/_format','01702','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (100,'工单管理-SQL审核-查询','/sql/audit/query','01704','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (101,'工单管理-SQL审核-SQL格式化','/sql/_format','01704','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (102,'工单管理-SQL审核-查询-详情','/sql/audit/detail','01704','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (103,'工单管理-SQL审核-审核','/sql/_audit','01704','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (104,'工单管理-SQL执行-查询','/sql/run/query','01705','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (105,'工单管理-SQL执行-格式化','/sql/_format','01705','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (106,'工单管理-SQL执行-运行','/sql/_run','01705','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (107,'工单管理-SQL执行-查询-详情','/sql/audit/detail','01705','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (108,'端口管理-新增-保存','/port/add/save','01901','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (109,'端口管理-查询-查询','/port/_query','01901','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (110,'端口管理-变更','/port/edit','01903','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (111,'端口管理-变更-保存','/port/edit/save','01903','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (112,'端口管理-变更-删除','/port/edit/del','01903','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (113,'端口管理-变更-导入','/port/edit/imp','01903','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (114,'端口管理-变更-导出','/port/edit/exp','01903','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (115,'功能管理-查询','/func/_query','02001','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (116,'功能管理-新增-保存','/func/add,/func/add/save','02001','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (117,'功能管理-维护-变更','/func/change,/func/edit','02001','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (118,'功能管理-维护-变更-保存','/func/edit/save','02001','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (119,'功能管理-维护-变更-删除','/func/edit/del','02001','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (120,'系统管理-系统设置','/sys/setting','06101','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (121,'系统管理-代码管理','/sys/code/_query,/sys/code/type/_query,/sys/code/detail/_query,/sys/code/type/add/save,/sys/code/type/upd/save,/sys/code/type/del,/sys/code/detail/add/save,/sys/code/detail/upd/save,/sys/code/detail/del','06102','1','2020-03-18','DBA','2020-05-14','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (122,'系统管理-审核规则-查询','/sys/query_rule','06103','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (123,'系统管理-审核规则-保存','/sys/audit_rule/save','06103','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (125,'数据库归档-归档查询-查询','/archive/_query','01302','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (126,'数据库归档-归档维护-变更','/archive/edit','01303','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (127,'数据库归档-归档维护-变更-保存','/archive/edit/save','01303','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (128,'数据库归档-归档维护-删除','/archive/edit/del','01303','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (129,'数据库归档-归档维护-推送','/archive/edit/push','01303','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (130,'数据库归档-归档维护-运行','/archive/edit/run','01303','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (131,'数据库归档-归档维护-停止','/archive/edit/stop','01303','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (132,'数据库归档-归档维护-克隆','/archive/clone','01303','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (133,'数据库归档-归档维护-克隆-保存','/archive/clone/save','01303','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (134,'数据库归档-日志查询-查询','/archive/log/_query','01304','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (135,'数据库归档-归档查询-查询-详情','/archive/_query/detail','01302','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (136,'数据库同步-日志查询-查询','/sync/log/_query','01104','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (138,'数据库同步-任务查询-查询','/sync/_query','01103','1','2020-03-18','DBA','2020-03-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (139,'数据库同步-任务分析-查询','/sync/log/_analyze','01105','1','2020-03-23','DBA','2020-03-23','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (140,'数据库同步-日志分析-查询-任务列表','/get/sync/task','01105','1','2020-03-23','DBA','2020-03-23','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (141,'数据库同步-日志查询-查询-详情','/sync/log/_query/detail','01105','1','2020-03-23','DBA','2020-03-23','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (142,'数据库传输-日志查询-查询','/transfer/log/_query','01204','1','2020-03-23','DBA','2020-03-23','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (143,'数据库监控-指标管理-新增-保存','/monitor/index/add/save','00701','1','2020-03-31','DBA','2020-03-31','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (144,'数据库监控-指标管理-变更-保存','/monitor/index/edit/save','00701','1','2020-03-31','DBA','2020-03-31','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (145,'数据库监控-指标管理-删除','/monitor/index/edit/del','00701','1','2020-03-31','DBA','2020-03-31','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (146,'数据库监控-指标管理-查询','/monitor/index/query,/monitor/index/_query','00701','1','2020-03-31','DBA','2020-03-31','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (147,'数据库监控-模板管理-新增-保存','/monitor/templete/add/save','00702','1','2020-04-01','DBA','2020-04-01','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (148,'数据库监控-模板管理-变更-保存','/monitor/templete/edit/save','00702','1','2020-04-01','DBA','2020-04-01','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (149,'数据库监控-模板管理-删除','/monitor/templete/edit/del','00702','1','2020-04-01','DBA','2020-04-01','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (150,'数据库监控-模板管理-查询','/monitor/templete/query,/monitor/templete/_query','00702','1','2020-04-01','DBA','2020-04-01','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (151,'数据库监控-任务管理-查询','/monitor/task/query,/monitor/task/_query','00702','1','2020-04-01','DBA','2020-04-01','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (152,'数据库监控-新增任务-采集-保存','/monitor/task/add/save/gather,/get/monitor/templete/type','00702','1','2020-04-01','DBA','2020-04-19','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (153,'数据库监控-任务管理-推送','/monitor/task/push','00703','1','2020-04-07','DBA','2020-04-07','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (154,'数据库监控-任务管理-运行','/monitor/task/run','00703','1','2020-04-07','DBA','2020-04-07','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (155,'数据库监控-任务管理-停止','/monitor/task/stop','00703','1','2020-04-07','DBA','2020-04-07','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (156,'数据库监控-监控图表-查询','/monitor/graph/query,/monitor/graph/_query,/get/monitor/db','00704','1','2020-04-09','DBA','2020-04-20','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (157,'大数据同步-日志分析-查询','/bigdata/log/analyze','01504','1','2020-04-12','DBA','2020-04-12','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (158,'大数据同步-日志分析-分析','/bigdata/log/_analyze','01504','1','2020-04-12','DBA','2020-04-12','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (159,'大数据同步-日志分析-任务列表','/get/bigdata/sync/task','01504','1','2020-04-12','DBA','2020-04-12','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (160,'数据库监控-新增任务-监控-保存','/monitor/task/add/save/monitor','00703','1','2020-04-18','DBA','2020-04-18','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (161,'数据库监控-任务管理-删除','/monitor/task/edit/del','00703','1','2020-04-21','DBA','2020-04-21','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (162,'数据库监控-任务管理-更新-采集','/monitor/task/edit/save/gather','00703','1','2020-04-22','DBA','2020-04-22','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (163,'数据库监控-任务管理-更新-监控','/monitor/task/edit/save/monitor','00703','1','2020-04-22','DBA','2020-04-22','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (164,'数据库监控-监控大屏-查看','/monitor/index/threshold,/monitor/view,/monitor/view/sys,/monitor/view/svr','00705','1','2020-04-30','DBA','2020-04-30','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (165,'数据库管理-实例管理','/db/inst/_query,/db/inst/save,/db/inst/query/id,/db/inst/update','00601','1','2020-05-09','DBA','2020-07-28','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (166,'数据库管理-账号管理','/db/user/_query,/db/user/save','00602','1','2020-05-09','DBA','2020-05-09','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (167,'系统管理-主页面','/,/main,/get/db/active/num,/get/db/slow/num,/get/sync,/platform,/easylife','06101','1','2020-05-15','DBA','2021-02-05','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (168,'数据库管理-实例管理-控制台','/db/inst/mgr,/get/inst/tree,/db/inst/sql/_query','00601','1','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (169,'数据库管理-实例管理-实例删除','/db/inst/del','00601','1','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (170,'数据库管理-实例管理-表删除','/drop/inst/tab','00601','1','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (171,'数据库管理-新增实例-查询','/db/inst/crt/query','00601','1','2020-07-29','DBA','2020-07-29','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (173,'数据库管理-操作日志-查询','/db/inst/opt/log/_query','00607','1','2020-08-05','DBA','2020-08-05','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (174,'图片管理-新建任务','/minio/add','02101','1','2020-09-29','DBA','2020-09-29','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (175,'图片管理-新建任务-保存','/minio/add/save','02101','1','2020-09-29','DBA','2020-09-29','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (177,'图片管理-任务查询','/minio/query,/minio/_query','02102','1','2020-09-29','DBA','2020-09-29','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (180,'图片管理-任务维护','/minio/_query','02103','1','2020-09-29','DBA','2020-09-29','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (183,'图片管理-任务维护-变更','/minio/edit','02103','1','2020-09-29','DBA','2020-09-29','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (186,'图片管理-任务维护-变更-保存','/minio/edit/save','02103','1','2020-09-29','DBA','2020-09-29','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (188,'图片管理-任务维护-删除','/minio/edit/del','02103','1','2020-09-29','DBA','2020-09-29','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (189,'图片管理-任务维护-推送','/minio/edit/push','02103','1','2020-09-29','DBA','2020-09-29','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (191,'图片管理-任务维护-克隆','/minio/clone','02103','1','2020-09-29','DBA','2020-09-29','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (194,'图片管理-日志查询','/minio/log/query,/minio/log/_query','02104','1','2020-09-29','DBA','2020-09-29','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (196,'图片管理-日志分析','/minio/log/analyze,/minio/log/_analyze','02105','1','2020-09-29','DBA','2020-09-29','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (198,'慢日志管理-慢日志新增','/slow/add','01601','1','2020-09-29','DBA','2020-09-29','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (199,'慢日志管理-慢日志新增-保存','/slow/add/save','01601','1','2020-09-29','DBA','2020-09-29','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (200,'慢日志管理-慢日志维护','/slow/_query','01602','1','2020-09-29','DBA','2020-09-29','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (202,'慢日志管理-慢日志维护-变更','/slow/edit/save','01602','1','2020-09-29','DBA','2020-09-29','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (203,'慢日志管理-慢日志维护-删除','/slow/edit/del','01602','1','2020-09-29','DBA','2020-09-29','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (204,'慢日志管理-慢日志维护-推送','/slow/edit/push','01602','1','2020-09-29','DBA','2020-09-29','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (208,'慢日志管理-慢日志查询','/slow/log/query,/slow/log/_query,/slow/query/id,/get/inst/db,/get/inst/user','01603','1','2020-09-29','DBA','2020-09-29','DBA');
insert  into `t_func`(`id`,`func_name`,`func_url`,`priv_id`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (211,'慢日志管理-慢日志分析','/slow/log/analyze,/slow/log/_analyze,/slow/log/detail/id,/slow/log/query/id,/slow/log/plan/id','01604','1','2020-09-29','DBA','2020-10-12','DBA');



/*Data for the table `t_sql_audit_rule` */

insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (0,'ddl','switch_check_ddl','检测DDL语法及权限','true','{0}','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (1,'ddl','switch_tab_not_exists_pk','检查表必须为主键','true','表:\'{0}\'无主键!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (2,'ddl','switch_tab_pk_id','强制主键名为ID','true','表:\'{0}\'主键列名必须为\"id\"!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (3,'ddl','switch_tab_pk_auto_incr','强制主键为自增列','true','表:\'{0}\'主键列名必须为自增列!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (4,'ddl','switch_tab_pk_autoincrement_1','强制自增列初始值为1','true','表:\'{0}\'主键列自增初始值必须为1!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (5,'ddl','switch_pk_not_int_bigint','允许主键类型非int/bigint','false','表:\'{0}\'主键类型非int/bigint','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (6,'ddl','switch_tab_comment','检查表注释','true','表:\'{0}\'没有注释!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (7,'ddl','switch_col_comment','检查列注释','true','表:\'{0}\'列\'{1}\'没有注释!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (8,'ddl','switch_col_not_null','检查列是否为not null','true','表:\'{0}\'列\'{1}\'不能为空!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (9,'ddl','switch_col_default_value','检查列默认值','false','表:\'{0}\'非空列\'{1}\'上没有默认值!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (10,'ddl','switch_tcol_default_value','检查时间字段默认值','true','表:\'{0}\'时间列\'{1}\'默认值必须为\'{2}\'!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (11,'ddl','switch_char_max_len','字符字段最大长度','2000','表:\'{0}\'字符列\'{1}\'长度不能超过{2}!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (12,'ddl','switch_tab_has_time_fields','表必须拥有字段','create_time,update_time','表:\'{0}\'无\'{1}\'列!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (13,'ddl','switch_tab_tcol_datetime','时间字段类型为datetime','true','表:\'{0}\'列\'{1}\'必须为datetime类型!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (14,'ddl','switch_tab_char_total_len','字符列总长度','8000','表:\'{0}\'字符列总长度不能超过{1}个字符!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (15,'ddl','switch_tab_ddl_max_rows','DDL最大影响行数','2000','表:\'{0}\'DDL操作影响行数不能超过{1}行!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (20,'ddl','switch_tab_name_check','开启表名称规范','true','','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (21,'ddl','switch_tab_max_len','表名最大长度','60','表:\'{0}\'名称长度不能超过{1}个字符!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (22,'ddl','switch_tab_not_digit_first','表名不能以数字开头','true','表:\'{0}\'不允许以数字开头!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (23,'ddl','switch_tab_two_digit_end','禁止连续2位数字为后缀','true','表:\'{0}\'不允许连续2位及以上数字结尾!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (24,'ddl','switch_tab_disable_prefix','禁止表名前后缀','temp,tmp,bak,backup','表:\'{0}\'禁止{1}为前后缀!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (25,'ddl','switch_ddl_batch','是否开启批量DDL','true','不允许执行多个DDL语句!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (26,'ddl','switch_ddl_timeout','DDL超时时间','120','表:\'{0}\'执行DDL已超时!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (27,'ddl','switch_disable_trigger','禁止使用触发器','true','禁止使用触发器!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (28,'ddl','switch_disable_func','禁止使用函数','true','禁止使用函数!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (29,'ddl','switch_disable_proc','禁止使用过程','true','禁止使用过程!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (30,'ddl','switch_disable_event','禁止使用过程','true','禁止使用事件!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (31,'ddl','switch_drop_database','允许删除库','false','禁止删除数据库！','0');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (32,'ddl','switch_drop_table','允许删除表','false','禁止删除表！','0');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (33,'ddl','switch_virtual_col','允许便用虚拟列','false','表:\'{0}\'不允许使用虚拟列!','0');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (34,'ddl','switch_tab_migrate','是否允许跨库表迁移','false','表:\'{0}\'不允许跨库迁移操作!','0');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (35,'ddl','switch_col_order_rule','允许设置列排序规则','false','表:\'{0}\'不允许设置列排序规则!','0');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (36,'ddl','switch_col_charset','允许设置列字符集','false','表:\'{0}\'不允许设置列字符集！','0');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (37,'ddl','switch_tab_charset','允许设置表字符集','true','表:\'{0}\'不允许设置列排序规则!','0');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (38,'ddl','switch_tab_charset_range','允许表字符集范围','utf8mb4,utf8','表:\'{0}\'只允许表字符集范围为({1})!','0');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (40,'ddl','switch_idx_name_check','开启索引规范','true','','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (41,'ddl','switch_idx_name_null','允许索引名为空','true','表:\'{0}\'不允许索引名为空!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (42,'ddl','switch_idx_name_rule','启用索引名规则','false','表:\'{0}\'索引名\'{1}\'唯反规则!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (43,'ddl','switch_idx_numbers','单表索引数上限\r\n','2','表:\'{0}\'索引个数超限!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (44,'ddl','switch_idx_col_numbers','单个索引字段上限\r\n','3','表:\'{0}\'的索引\'{1}\'列个数超限!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (45,'ddl','switch_idx_name_col','允许索引名与列名相同','true','表:\'{0}\'索引名与列名不能相同!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (61,'dml','switch_dml_batch','是否开启批量DML','false','不允许执行批量DML语句!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (62,'dml','switch_dml_where','检测DML语句条件','true','DML语句必须存在where条件!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (63,'dml','switch_dml_order','DML语句禁用order','true','DML语句禁止使用order by!\'','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (64,'dml','switch_dml_select','DML语句禁用select','true','DML语句禁用SELECT!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (65,'dml','switch_dml_max_rows','DML最大影响行数\r\n','3','DML最大影响行数\r\n不能超过{0}行!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (66,'dml','switch_dml_ins_exists_col','检查插入语句必须存在列名','true','Insert语句必须指定列名!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (67,'dml','switch_dml_ins_cols','INSERT语句字段上限','8','Insert语句字段数不能超过{0}列!','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (68,'dml','switch_check_dml','验证DML语句语法','true','','1');
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (80,'query','switch_query_rows','限制查询条数','1000','查询超出{0}最大行限制！',NULL);
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (81,'query','switch_timeout','查询超时时间','3','查询超过{0}秒，停止查询!',NULL);
insert  into `t_sql_audit_rule`(`id`,`rule_type`,`rule_code`,`rule_name`,`rule_value`,`error`,`status`) values (82,'query','switch_sensitive_columns','查询敏感列设置','user_mobile,user_email,user_name','***敏感列***',NULL);

/*Data for the table `t_sys_stats_idx` */

insert  into `t_sys_stats_idx`(`id`,`idx_name`,`idx_sql`) values (1,'user_num','select count(0) as val from t_user');
insert  into `t_sys_stats_idx`(`id`,`idx_name`,`idx_sql`) values (4,'db_source_num','select count(0) as val from t_db_source');
insert  into `t_sys_stats_idx`(`id`,`idx_name`,`idx_sql`) values (7,'server_num','select count(0) as val from t_server');
insert  into `t_sys_stats_idx`(`id`,`idx_name`,`idx_sql`) values (10,'wtd_num','select count(0) as val from t_wtd');
insert  into `t_sys_stats_idx`(`id`,`idx_name`,`idx_sql`) values (13,'sql_num','select count(0) as val from t_sql_release');
insert  into `t_sys_stats_idx`(`id`,`idx_name`,`idx_sql`) values (16,'stats_task_num','select count(0) as val from t_monitor_task');
insert  into `t_sys_stats_idx`(`id`,`idx_name`,`idx_sql`) values (19,'agent_num','select count(0) as val from t_db_source where proxy_server !=\'\'');
insert  into `t_sys_stats_idx`(`id`,`idx_name`,`idx_sql`) values (22,'backup_task_num','select count(0) as val from t_db_config where status=\'1\'');
insert  into `t_sys_stats_idx`(`id`,`idx_name`,`idx_sql`) values (25,'sync_task_num','select count(0) as val from t_db_sync_config where status=\'1\'');
insert  into `t_sys_stats_idx`(`id`,`idx_name`,`idx_sql`) values (28,'slow_task','select count(0) as val from t_slow_log where status=\'1\'');
insert  into `t_sys_stats_idx`(`id`,`idx_name`,`idx_sql`) values (31,'minio_task','select count(0) as val from t_minio_config');
insert  into `t_sys_stats_idx`(`id`,`idx_name`,`idx_sql`) values (34,'archive_task','select count(0) as val from t_db_archive_config where status=\'1\'');

/*Data for the table `t_templete` */

insert  into `t_templete`(`id`,`templete_id`,`contents`,`description`) values (1,1,'{\r\n  \"job\": {\r\n    \"setting\": {\r\n      \"speed\": {\r\n        \"channel\": 5\r\n      }\r\n    },\r\n    \"content\": [\r\n      {\r\n       \"reader\": {\r\n                    \"name\": \"mysqlreader\",\r\n                    \"parameter\": {\r\n                        \"username\": \"$$USERNAME$$\",\r\n                        \"password\": \"$$PASSWORD$$\",\r\n                        \"column\": [\r\n                            $$MYSQL_COLUMN_NAMES$$\r\n                        ],\r\n                        \"connection\": [\r\n                            {\r\n                                \"table\": [\r\n                                    \"$$MYSQL_TABLE_NAME$$\"\r\n                                ],\r\n                                \"jdbcUrl\":[\r\n                                  \"jdbc:mysql://$$MYSQL_URL$$?useUnicode=true&characterEncoding=UTF-8\"\r\n                                ]\r\n                            }\r\n                        ]\r\n                    }\r\n                },\r\n         \"writer\": {\r\n          \"name\": \"hbase11xwriter\",\r\n          \"parameter\": {\r\n            \"hbaseConfig\": {\r\n               \"hbase.zookeeper.quorum\": \"$$ZK_HOSTS\"\r\n            },\r\n            \"table\": \"$$HBASE_TABLE_NAME$$\",\r\n            \"mode\": \"normal\",\r\n            \"rowkeyColumn\": [\r\n                $$HBASE_ROWKEY$$\r\n            ],\r\n            \"column\": [\r\n              $$HBASE_COLUMN_NAMES$$\r\n            ],           \r\n            \"encoding\": \"utf-8\"\r\n          }\r\n        }\r\n      }\r\n    ]\r\n  }\r\n}','dataX全量同步模板(mysql->hbase)');
insert  into `t_templete`(`id`,`templete_id`,`contents`,`description`) values (2,2,'{\r\n  \"job\": {\r\n    \"setting\": {\r\n      \"speed\": {\r\n        \"channel\": 5\r\n      }\r\n    },\r\n    \"content\": [\r\n      {\r\n       \"reader\": {\r\n                    \"name\": \"mysqlreader\",\r\n                    \"parameter\": {\r\n                        \"username\": \"$$USERNAME$$\",\r\n                        \"password\": \"$$PASSWORD$$\",\r\n                        \"column\": [\r\n                            $$MYSQL_COLUMN_NAMES$$\r\n                        ],\r\n      \"where\":\"$$MYSQL_WHERE$$\",\r\n                        \"connection\": [\r\n                            {\r\n                                \"table\": [\r\n                                    \"$$MYSQL_TABLE_NAME$$\"\r\n                                ],\r\n                                \"jdbcUrl\":[\r\n                                  \"jdbc:mysql://$$MYSQL_URL$$?useUnicode=true&characterEncoding=UTF-8\"\r\n                                ]\r\n                            }\r\n                        ]\r\n                    }\r\n                },\r\n         \"writer\": {\r\n          \"name\": \"hbase11xwriter\",\r\n          \"parameter\": {\r\n            \"hbaseConfig\": {\r\n               \"hbase.zookeeper.quorum\": \"$$ZK_HOSTS\"\r\n            },\r\n            \"table\": \"$$HBASE_TABLE_NAME$$\",\r\n            \"mode\": \"normal\",\r\n            \"rowkeyColumn\": [\r\n                $$HBASE_ROWKEY$$\r\n            ],\r\n            \"column\": [\r\n              $$HBASE_COLUMN_NAMES$$\r\n            ],           \r\n            \"encoding\": \"utf-8\"\r\n          }\r\n        }\r\n      }\r\n    ]\r\n  }\r\n}\r\n','dataX增量同步模板(mysql->hbase)');
insert  into `t_templete`(`id`,`templete_id`,`contents`,`description`) values (3,3,'{\r\n  \"job\": {\r\n    \"setting\": {\r\n      \"speed\": {\r\n        \"channel\": 5\r\n      }\r\n    },\r\n    \"content\": [\r\n      {\r\n       \"reader\": {\r\n                    \"name\": \"mysqlreader\",\r\n                    \"parameter\": {\r\n                        \"username\": \"$$USERNAME$$\",\r\n                        \"password\": \"$$PASSWORD$$\",\r\n                        \"column\": [\r\n                            $$MYSQL_COLUMN_NAMES$$\r\n                        ],\r\n                        \"connection\": [\r\n                            {\r\n                                \"table\": [\r\n                                    \"$$MYSQL_TABLE_NAME$$\"\r\n                                ],\r\n                                \"jdbcUrl\":[\r\n                                  \"jdbc:mysql://$$MYSQL_URL$$?useUnicode=true&characterEncoding=UTF-8\"\r\n                                ]\r\n                            }\r\n                        ]\r\n                    }\r\n                },\r\n         \"writer\": {\r\n          \"name\": \"elasticsearchwriter\",\r\n          \"parameter\": {\r\n            \"endpoint\" : \"$$ES_SERVICE$$\",\r\n            \"accessId\" : \"xxxx\",\r\n            \"accessKey\": \"xxxx\",\r\n            \"index\"    : \"$$ES_INDEX_NAME$$\",\r\n            \"type\"     : \"$$ES_TYPE_NAME$$\",\r\n            \"cleanup\"  : false,\r\n            \"discovery\": false,\r\n            \"batchSize\": 1000,\r\n            \"splitter\": \",\",\r\n            \"column\": [\r\n              $$ES_COLUMN_NAMES$$\r\n            ],           \r\n            \"encoding\": \"utf-8\"\r\n          }\r\n        }\r\n      }\r\n    ]\r\n  }\r\n}','dataX全量同步模板(mysql->es)');
insert  into `t_templete`(`id`,`templete_id`,`contents`,`description`) values (4,4,'{\r\n  \"job\": {\r\n    \"setting\": {\r\n      \"speed\": {\r\n        \"channel\": 5\r\n      }\r\n    },\r\n    \"content\": [\r\n      {\r\n       \"reader\": {\r\n                    \"name\": \"mysqlreader\",\r\n                    \"parameter\": {\r\n                        \"username\": \"$$USERNAME$$\",\r\n                        \"password\": \"$$PASSWORD$$\",\r\n                        \"column\": [\r\n                            $$MYSQL_COLUMN_NAMES$$\r\n                        ],\r\n      \"where\":\"$$MYSQL_WHERE$$\",\r\n                        \"connection\": [\r\n                            {\r\n                                \"table\": [\r\n                                    \"$$MYSQL_TABLE_NAME$$\"\r\n                                ],\r\n                                \"jdbcUrl\":[\r\n                                  \"jdbc:mysql://$$MYSQL_URL$$?useUnicode=true&characterEncoding=UTF-8\"\r\n                                ]\r\n                            }\r\n                        ]\r\n                    }\r\n                },\r\n         \"writer\": {\r\n          \"name\": \"elasticsearchwriter\",\r\n          \"parameter\": {\r\n            \"endpoint\" : \"$$ES_SERVICE$$\",\r\n            \"accessId\" : \"xxxx\",\r\n            \"accessKey\": \"xxxx\",\r\n            \"index\"    : \"$$ES_INDEX_NAME$$\",\r\n            \"type\"     : \"$$ES_TYPE_NAME$$\",\r\n            \"cleanup\"  : false,\r\n            \"discovery\": false,\r\n            \"batchSize\": 1000,\r\n            \"splitter\": \",\",\r\n            \"column\": [\r\n              $$ES_COLUMN_NAMES$$\r\n            ],           \r\n            \"encoding\": \"utf-8\"\r\n          }\r\n        }\r\n      }\r\n    ]\r\n  }\r\n}\r\n','dataX增量同步模板(mysql->es)');

/*Data for the table `t_user` */

insert  into `t_user`(`id`,`name`,`wkno`,`gender`,`email`,`phone`,`project_group`,`dept`,`expire_date`,`password`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`,`login_name`,`file_path`,`file_name`) values (1,'管理员','190343','1','190343@lifeat.cn','15801620810','1','03','2021-05-30','47508EE611CC14EFB8C805158601FE09','1','2018-08-27','DBA','2020-12-03','DBA','admin','/static/assets/images/users','93d64232-3a5f-11ea-bb2b-000c29cd7d70_admin.jpg');

/*Data for the table `t_role` */

insert  into `t_role`(`id`,`name`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1,'系统管理员','1',NOW(),'DBA',NOW(),'DBA');
insert  into `t_role`(`id`,`name`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (2,'数据库管理员','1',NOW(),'DBA',NOW(),'DBA');

/*Data for the table `t_user_role` */
insert  into `t_user_role`(`id`,`user_id`,`role_id`) values (1,1,1);
insert  into `t_user_role`(`id`,`user_id`,`role_id`) values (2,1,2);

/*Data for the table `t_role_privs` */

insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (53,1,'00101','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (54,1,'00102','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (55,1,'00103','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (56,1,'00104','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (57,1,'00201','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (58,1,'00202','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (59,1,'00203','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (60,1,'00301','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (61,1,'00302','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (62,1,'00303','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (63,1,'00401','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (64,1,'00402','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (65,1,'00403','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (66,1,'00404','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (67,1,'00501','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (68,1,'00502','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (69,1,'00503','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (70,1,'00601','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (71,1,'00602','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (72,1,'00603','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (73,1,'00701','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (74,1,'00702','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (75,1,'00703','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (76,1,'00704','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (77,1,'00705','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (78,1,'00801','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (79,1,'00802','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (80,1,'00901','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (81,1,'00902','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (82,1,'00903','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (83,1,'00904','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (84,1,'00905','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (85,1,'01001','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (86,1,'01002','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (87,1,'01003','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (88,1,'01101','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (89,1,'01102','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (90,1,'01103','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (91,1,'01104','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (92,1,'01105','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (93,1,'01201','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (94,1,'01202','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (95,1,'01203','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (96,1,'01204','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (97,1,'01301','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (98,1,'01302','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (99,1,'01303','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (100,1,'01304','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (101,1,'01501','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (102,1,'01502','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (103,1,'01503','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (104,1,'01504','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (105,1,'01601','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (106,1,'01602','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (107,1,'01603','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (108,1,'01701','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (109,1,'01702','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (110,1,'01703','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (111,1,'01704','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (112,1,'01705','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (113,1,'01706','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (114,1,'01707','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (115,1,'01708','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (116,1,'01801','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (117,1,'01802','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (118,1,'01803','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (119,1,'01901','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (120,1,'01902','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (121,1,'01903','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (122,1,'02001','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (123,1,'02002','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (124,1,'02003','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (125,1,'06001','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (126,1,'06002','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (127,1,'06003','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (128,1,'06101','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (129,1,'06102','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (130,1,'06103','2020-07-28','DBA','2020-07-28','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1316,2,'00101','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1319,2,'00102','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1322,2,'00103','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1325,2,'00104','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1328,2,'00201','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1331,2,'00202','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1334,2,'00203','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1337,2,'00301','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1340,2,'00302','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1343,2,'00303','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1346,2,'00401','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1349,2,'00402','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1352,2,'00403','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1355,2,'00404','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1358,2,'00501','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1361,2,'00502','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1364,2,'00503','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1367,2,'00601','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1370,2,'00602','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1373,2,'00603','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1376,2,'00604','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1379,2,'00701','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1382,2,'00702','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1385,2,'00703','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1388,2,'00704','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1391,2,'00705','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1394,2,'00801','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1397,2,'00802','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1400,2,'00901','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1403,2,'00902','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1406,2,'00903','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1409,2,'00904','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1412,2,'00905','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1415,2,'01001','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1418,2,'01002','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1421,2,'01003','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1424,2,'01101','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1427,2,'01102','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1430,2,'01103','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1433,2,'01104','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1436,2,'01105','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1439,2,'01201','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1442,2,'01202','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1445,2,'01203','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1448,2,'01204','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1451,2,'01301','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1454,2,'01302','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1457,2,'01303','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1460,2,'01304','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1463,2,'01501','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1466,2,'01502','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1469,2,'01503','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1472,2,'01504','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1475,2,'01601','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1478,2,'01602','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1481,2,'01603','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1484,2,'01701','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1487,2,'01702','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1490,2,'01703','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1493,2,'01704','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1496,2,'01705','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1499,2,'01706','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1502,2,'01801','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1505,2,'01802','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1508,2,'01803','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1511,2,'01901','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1514,2,'01902','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1517,2,'01903','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1520,2,'02001','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1523,2,'02002','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1526,2,'02003','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1529,2,'06001','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1532,2,'06002','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1535,2,'06003','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1538,2,'06101','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1541,2,'06102','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1544,2,'06103','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1547,2,'00607','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1550,2,'01604','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1553,2,'02101','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1556,2,'02102','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1559,2,'02103','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1562,2,'02104','2020-10-09','DBA','2020-10-09','DBA');
insert  into `t_role_privs`(`id`,`role_id`,`priv_id`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1565,2,'02105','2020-10-09','DBA','2020-10-09','DBA');


/*Data for the table `t_xtqx` */

insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('0','根节点','','',NULL,'1',NULL,'2018-06-30','DBA','2018-06-30','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('001','用户管理','0','',NULL,'1','fa fa-user','2018-06-30','DBA','2020-03-01','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00101','用户查询','001','/user/query','user_query.html','1',NULL,'2018-06-30','DBA','2019-07-30','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00102','用户新增','001','/user/add','user_add.html','1',NULL,'2018-06-30','DBA','2020-03-12','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00103','用户变更','001','/user/change','user_change.html','1',NULL,'2018-06-30','DBA','2018-06-30','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00104','项目授权','001','/project/query','projectquery.html','1',NULL,'2018-09-02','DBA','2019-10-22','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('002','角色管理','0','',NULL,'1','mdi mdi-account-switch','2018-06-30','DBA','2018-06-30','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00201','角色查询','002','/role/query',NULL,'1',NULL,'2018-06-30','DBA','2018-06-30','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00202','角色新增','002','/role/add',NULL,'1',NULL,'2018-06-30','DBA','2018-06-30','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00203','角色变更','002','/role/change',NULL,'1',NULL,'2018-06-30','DBA','2018-06-30','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('003','菜单管理','0','',NULL,'1','mdi mdi-file-tree','2018-07-01','DBA','2018-09-10','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00301','菜单查询','003','/menu/query',NULL,'1',NULL,'2018-07-01','DBA','2018-07-01','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00302','菜单新增','003','/menu/add',NULL,'1',NULL,'2018-07-01','DBA','2018-07-01','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00303','菜单变更','003','/menu/change',NULL,'1',NULL,'2018-07-01','DBA','2018-09-10','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('004','数据源管理','0','',NULL,'1','mdi mdi-chemical-weapon','2018-07-01','DBA','2018-07-01','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00401','数据源查询','004','/ds/query',NULL,'1',NULL,'2018-07-01','DBA','2019-08-18','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00402','数据源新增','004','/ds/add',NULL,'1',NULL,'2018-07-01','DBA','2019-08-18','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00403','数据源维护','004','/ds/change',NULL,'1',NULL,'2018-07-01','DBA','2020-03-19','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00404','数据源测试','004','/ds/test',NULL,'1',NULL,'2018-07-08','DBA','2018-07-08','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('005','服务器管理','0','',NULL,'1','mdi mdi-monitor','2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00501','服务器查询','005','/server/query',NULL,'1',NULL,'2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00502','新增服务器','005','/server/add',NULL,'1',NULL,'2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00503','服务器变更','005','/server/change',NULL,'1',NULL,'2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('006','数据库管理','0','',NULL,'1','mdi mdi-settings','2018-10-03','DBA','2020-02-19','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00601','实例创建','006','/db/inst/crt/query',NULL,'1','','2018-10-03','DBA','2020-10-17','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00602','实例管理','006','/db/inst/query',NULL,'1','','2018-10-03','DBA','2020-02-19','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00603','账号管理','006','/db/user/query',NULL,'1','','2018-10-03','DBA','2020-02-19','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00604','配置管理','006','/db/inst/cfg/query',NULL,'1','','2018-10-03','DBA','2020-02-19','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00605','权限管理','006','/db/inst/priv',NULL,'0','','2018-10-03','DBA','2020-02-19','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00606','参数管理','006','/db/inst/para/query',NULL,'0','','2018-10-03','DBA','2020-02-19','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00607','操作日志','006','/db/inst/opt/log/query',NULL,'1','','2018-10-03','DBA','2020-02-19','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('007','数据库监控','0','',NULL,'1','ion-eye','2018-09-03','DBA','2018-09-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00701','指标管理','007','/monitor/index/query',NULL,'1','','2018-09-03','DBA','2018-09-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00702','模板管理','007','/monitor/templete/query',NULL,'1','','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00703','任务管理','007','/monitor/task/query',NULL,'1','','2018-11-17','DBA','2018-11-17','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00704','监控图表','007','/monitor/graph/query',NULL,'1','','2018-10-15','DBA','2019-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00705','监控大屏','007','/monitor/view',NULL,'1',NULL,'2018-10-03','DBA','2020-03-19','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('008','数据库工具','0','',NULL,'0','mdi mdi-database','2018-07-08','DBA','2018-07-08','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00801','字典生成','008','/dba/dict',NULL,'1','','2018-07-08','DBA','2018-07-08','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00802','Redis迁移','008','/redis/migrate',NULL,'1','','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('009','数据库备份','0','',NULL,'1','mdi mdi-content-copy','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00901','新建备份','009','/backup/add',NULL,'1','','2018-10-03','DBA','2019-10-21','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00902','备份维护','009','/backup/change',NULL,'1','','2018-10-15','DBA','2019-10-26','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00903','任务查询','009','/backup/query',NULL,'1','','2018-10-15','DBA','2019-10-23','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00904','日志查询','009','/backup/log/query',NULL,'1','','2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('00905','日志分析','009','/backup/log/analyze',NULL,'1','','2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('010','数据库恢复','0','',NULL,'0','mdi mdi-backup-restore','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01001','恢复向导','010','/recover/guide',NULL,'1','','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01002','恢复配置','010','/recover/config',NULL,'1','','2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01003','恢复查询','010','/recover/query',NULL,'1','','2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('011','数据库同步','0','',NULL,'1','mdi mdi-sync','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01101','新建同步','011','/sync/add',NULL,'1','','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01102','同步维护','011','/sync/change',NULL,'1','','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01103','任务查询','011','/sync/query',NULL,'1','','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01104','日志查询','011','/sync/log/query',NULL,'1','','2018-10-15','DBA','2019-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01105','日志分析','011','/sync/log/analyze',NULL,'1','','2018-10-15','DBA','2019-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01107','同步拓扑','011','/sync/log/graph',NULL,'0','','2018-10-15','DBA','2020-01-06','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('012','数据库传输','0','',NULL,'1','mdi mdi-swap-horizontal','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01201','新建传输','012','/transfer/add',NULL,'1','','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01202','传输查询','012','/transfer/query',NULL,'1','','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01203','传输维护','012','/transfer/change',NULL,'1','','2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01204','日志查询','012','/transfer/log/query',NULL,'1','','2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('013','数据库归档','0','',NULL,'1','mdi mdi-lan-connect','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01301','新建归档','013','/archive/add',NULL,'1','','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01302','归档查询','013','/archive/query',NULL,'1','','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01303','归档维护','013','/archive/change',NULL,'1','','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01304','日志查询','013','/archive/log/query',NULL,'1','','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('014','数据库部署','0','',NULL,'0','mdi mdi-polymer','2018-10-03','DBA','2020-03-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('015','大数据同步','0','',NULL,'1','ion-ios7-pulse-strong','2018-10-03','DBA','2020-03-03',NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01501','新增同步','015','/bigdata/add',NULL,'1','','2018-10-03','DBA','2020-03-03',NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01502','任务查询','015','/bigdata/query',NULL,'1','','2018-10-03','DBA','2020-03-03',NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01503','同步维护','015','/bigdata/change',NULL,'1','','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01504','日志分析','015','/bigdata/log/analyze',NULL,'1','','2018-10-03','DBA','2020-03-19','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('016','慢日志管理','0','',NULL,'1','mdi mdi-crop','2018-10-03','DBA','2020-02-19','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01601','慢日志新增','016','/slow/add',NULL,'1','','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01602','慢日志维护','016','/slow/change',NULL,'1','','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01603','慢日志查询','016','/slow/log/query',NULL,'1','','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01604','慢日志分析','016','/slow/log/analyze',NULL,'1','','2018-10-03','DBA','2020-03-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('017','工单管理','0','',NULL,'1','mdi mdi-format-align-left','2018-10-03','DBA','2020-01-04','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01701','我的工单','017','/order/query',NULL,'1','','2018-10-03','DBA','2020-03-03',NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01702','SQL查询','017','/sql/query',NULL,'1','','2018-10-03','DBA','2020-03-03',NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01703','SQL发布','017','/sql/release',NULL,'1','','2018-10-03','DBA','2020-03-03',NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01704','SQL审核','017','/sql/audit',NULL,'1','','2018-10-03','DBA','2020-03-03',NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01705','SQL执行','017','/sql/run',NULL,'1','','2018-10-03','DBA','2020-03-03',NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01706','SQL导出','017','/sql/exp',NULL,'1','','2018-07-08','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01707','phoenix查询','017','/sql/phoenix/sql',NULL,'0','','2020-03-31','DBA','2020-03-19','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01708','phoenix发布','017','/sql/phoenix/release',NULL,'0','','2018-10-03','DBA','2020-03-19','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('018','任务管理','0','',NULL,'0','mdi mdi-alarm','2018-10-03','DBA','2020-01-04','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01801','新建任务','018','/task/new',NULL,'1','','2018-10-03','DBA','2020-01-04',NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01802','任务查询','018','/task/query',NULL,'1','','2018-10-03','DBA','2020-01-04',NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01803','任务变更','018','/task/change',NULL,'1','','2018-10-03','DBA','2020-01-04',NULL);
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('019','端口管理','0','',NULL,'1','mdi mdi-code-brackets','2018-10-03','DBA','2020-02-19','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01901','端口新增','019','/port/add',NULL,'1','','2018-10-03','DBA','2020-02-19','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01902','端口查询','019','/port/query',NULL,'1','','2018-10-03','DBA','2020-02-19','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('01903','端口维护','019','/port/change',NULL,'1','','2018-10-03','DBA','2020-02-19','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('020','功能管理','0','',NULL,'1','mdi mdi-function','2018-06-30','DBA','2018-06-30','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('02001','功能查询','020','/func/query',NULL,'1','','2018-06-30','DBA','2018-06-30','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('02002','功能新增','020','/func/add',NULL,'1','','2018-06-30','DBA','2018-06-30','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('02003','功能变更','020','/func/change',NULL,'1','','2018-06-30','DBA','2018-06-30','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('021','图片管理','0','',NULL,'1','ion-images','2020-09-21','DBA','2020-09-21','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('02101','新建任务','021','/minio/add',NULL,'1','','2020-09-21','DBA','2020-09-21','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('02102','任务查询','021','/minio/query',NULL,'1','','2020-09-21','DBA','2020-09-21','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('02103','任务维护','021','/minio/change',NULL,'1','','2020-09-21','DBA','2020-09-21','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('02104','日志查询','021','/minio/log/query',NULL,'1','','2020-09-21','DBA','2020-09-21','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('02105','日志分析','021','/minio/log/analyze',NULL,'1','','2020-09-21','DBA','2020-09-21','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('060','公告管理','0','',NULL,'0','mdi mdi-message-text-outline','2018-10-03','DBA','2020-01-04','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('06001','公告发布','060','/message/release',NULL,'1','','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('06002','公告查询','060','/message/query',NULL,'1','','2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('06003','公告变更','060','/message/change',NULL,'1','','2018-10-15','DBA','2018-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('061','系统管理','0','',NULL,'1','mdi mdi-settings','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('06101','系统设置','061','/sys/setting',NULL,'1','','2018-10-15','DBA','2020-02-19','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('06102','代码管理','061','/sys/code',NULL,'1','mdi mdi-code-brackets','2018-10-03','DBA','2018-10-03','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('06103','审核规则','061','/sys/audit_rule',NULL,'1','mdi mdi-crop','2018-10-15','DBA','2019-10-15','DBA');
insert  into `t_xtqx`(`id`,`name`,`parent_id`,`url`,`url_front`,`status`,`icon`,`creation_date`,`creator`,`last_update_date`,`updator`) values ('06104','测试页面','061','/sys/test',NULL,'0','','2018-10-03','DBA','2020-03-19','DBA');

/*Data for the table `t_db_weekly_items` */

insert  into `t_db_weekly_items`(`id`,`item_type`,`item_code`,`item_desc`,`item_tjsql`,`status`) values (1,'server','cpu','CPU使用率[%]','SELECT  DATE_FORMAT(create_date,\'%Y-%m-%d %H\') AS rq,\r\n   ROUND(AVG(cpu_total_usage),2) AS val \r\nFROM `t_monitor_task_server_log` \r\nWHERE server_id={}  \r\nAND  create_date between \'{} 0:0:0\' and \'{} 23:59:59\' \r\nGROUP BY DATE_FORMAT(create_date,\'%Y-%m-%d %H\') \r\norder by 1','1');
insert  into `t_db_weekly_items`(`id`,`item_type`,`item_code`,`item_desc`,`item_tjsql`,`status`) values (4,'server','memory','内存使用率[%]','SELECT  DATE_FORMAT(create_date,\'%Y-%m-%d %H:%i\') AS rq,\r\n   ROUND(AVG(mem_usage),2)  AS val \r\nFROM `t_monitor_task_server_log` \r\nWHERE server_id={}  \r\nAND  create_date between \'{} 0:0:0\' and \'{} 23:59:59\' \r\nGROUP BY DATE_FORMAT(create_date,\'%Y-%m-%d %H:%i\') \r\norder by 1','1');
insert  into `t_db_weekly_items`(`id`,`item_type`,`item_code`,`item_desc`,`item_tjsql`,`status`) values (7,'server','disk_usage','磁盘使用率[%]','SELECT  DATE_FORMAT(create_date, \'%Y-%m-%d %H\') AS rq, \r\n        max(disk_usage) AS val \r\nFROM  `t_monitor_task_server_log` \r\nWHERE server_id = {} \r\nAND  create_date between \'{} 0:0:0\' and \'{} 23:59:59\' \r\nGROUP BY DATE_FORMAT(create_date, \'%Y-%m-%d %H\')\r\nORDER BY 1','1');
insert  into `t_db_weekly_items`(`id`,`item_type`,`item_code`,`item_desc`,`item_tjsql`,`status`) values (10,'server','disk_read','磁盘读[KB]','SELECT  DATE_FORMAT(create_date,\'%Y-%m-%d %H:%i\') AS rq,\r\n   ROUND(AVG(disk_read/1024),2)  AS val \r\nFROM `t_monitor_task_server_log` \r\nWHERE server_id={}  \r\nAND  create_date between \'{} 0:0:0\' and \'{} 23:59:59\' \r\nGROUP BY DATE_FORMAT(create_date,\'%Y-%m-%d %H:%i\') \r\norder by 1','1');
insert  into `t_db_weekly_items`(`id`,`item_type`,`item_code`,`item_desc`,`item_tjsql`,`status`) values (13,'server','disk_write','磁盘写[KB]','SELECT  DATE_FORMAT(create_date,\'%Y-%m-%d %H:%i\') AS rq,\r\n   ROUND(AVG(disk_write/1024),2)  AS val \r\nFROM `t_monitor_task_server_log` \r\nWHERE server_id={}  \r\nAND  create_date between \'{} 0:0:0\' and \'{} 23:59:59\' \r\nGROUP BY DATE_FORMAT(create_date,\'%Y-%m-%d %H:%i\') \r\norder by 1','1');
insert  into `t_db_weekly_items`(`id`,`item_type`,`item_code`,`item_desc`,`item_tjsql`,`status`) values (16,'server','net_in','网络流入[KB]','SELECT  DATE_FORMAT(create_date,\'%Y-%m-%d %H:%i\') AS rq,\r\n   ROUND(AVG(net_in/1024),2)  AS val \r\nFROM `t_monitor_task_server_log` \r\nWHERE server_id={}  \r\nAND  create_date between \'{} 0:0:0\' and \'{} 23:59:59\' \r\nGROUP BY DATE_FORMAT(create_date,\'%Y-%m-%d %H:%i\') \r\norder by 1','1');
insert  into `t_db_weekly_items`(`id`,`item_type`,`item_code`,`item_desc`,`item_tjsql`,`status`) values (19,'server','net_out','网络流出[KB]','SELECT  DATE_FORMAT(create_date,\'%Y-%m-%d %H:%i\') AS rq,\r\n ROUND(AVG(net_out/1024),2)  AS val \r\nFROM `t_monitor_task_server_log` \r\nWHERE server_id={}  \r\nAND  create_date between \'{} 0:0:0\' and \'{} 23:59:59\' \r\nGROUP BY DATE_FORMAT(create_date,\'%Y-%m-%d %H:%i\') \r\norder by 1','1');
insert  into `t_db_weekly_items`(`id`,`item_type`,`item_code`,`item_desc`,`item_tjsql`,`status`) values (20,'db','total_conn','总连接数','SELECT \r\n DATE_FORMAT(create_date,\'%Y-%m-%d %h:%i\') AS rq,\r\n  ROUND(AVG(total_connect),2) AS val\r\nFROM `t_monitor_task_db_log`\r\nWHERE db_id={}\r\n AND  create_date BETWEEN \'{} 0:0:0\' AND \'{} 23:59:59\' \r\nGROUP BY DATE_FORMAT(create_date,\'%Y-%m-%d %h:%i\') \r\norder by 1','1');
insert  into `t_db_weekly_items`(`id`,`item_type`,`item_code`,`item_desc`,`item_tjsql`,`status`) values (23,'db','active_conn','活跃连接数','SELECT \r\n DATE_FORMAT(create_date,\'%Y-%m-%d %h:%i\') AS rq,\r\n  ROUND(AVG(active_connect),2) AS val\r\nFROM `t_monitor_task_db_log`\r\nWHERE db_id={}\r\n AND  create_date BETWEEN \'{} 0:0:0\' AND \'{} 23:59:59\' \r\nGROUP BY DATE_FORMAT(create_date,\'%Y-%m-%d %h:%i\') \r\norder by 1','1');
insert  into `t_db_weekly_items`(`id`,`item_type`,`item_code`,`item_desc`,`item_tjsql`,`status`) values (26,'db','qps','每秒查询数[QPS]','SELECT \r\n  DATE_FORMAT(create_date,\'%Y-%m-%d %h:%i\') AS rq,\r\n  ROUND(AVG(db_qps),2) AS val\r\nFROM `t_monitor_task_db_log`\r\nWHERE db_id={}\r\nAND  create_date BETWEEN \'{} 0:0:0\' AND \'{} 23:59:59\' \r\nand  db_qps is not null and db_qps!=\'\' \r\nGROUP BY DATE_FORMAT(create_date,\'%Y-%m-%d %h:%i\') \r\norder by 1','1');
insert  into `t_db_weekly_items`(`id`,`item_type`,`item_code`,`item_desc`,`item_tjsql`,`status`) values (29,'db','tps','每秒事务数[TPS]','SELECT \r\n  DATE_FORMAT(create_date,\'%Y-%m-%d %h:%i\') AS rq,\r\n  ROUND(AVG(db_tps),2) AS val\r\nFROM `t_monitor_task_db_log`\r\nWHERE db_id={}\r\nAND  create_date BETWEEN \'{} 0:0:0\' AND \'{} 23:59:59\' \r\nand  db_tps is not null and db_tps!=\'\' \r\nGROUP BY DATE_FORMAT(create_date,\'%Y-%m-%d %h:%i\') \r\norder by 1','1');
insert  into `t_db_weekly_items`(`id`,`item_type`,`item_code`,`item_desc`,`item_tjsql`,`status`) values (32,'db','backup_size','备份大小[MB]','SELECT \r\nDATE_FORMAT(create_date,\'%Y-%m-%d\') AS rq,\r\nCASE \r\n    WHEN INSTR(total_size,\'G\')>0 THEN REPLACE(total_size,\'G\',\'\')*1024\r\n    WHEN INSTR(total_size,\'M\')>0 THEN REPLACE(total_size,\'M\',\'\')\r\n    ELSE REPLACE(total_size,\'K\',\'\')/1024\r\nEND AS val\r\nFROM `t_db_backup_total`\r\nWHERE db_tag=(SELECT db_tag FROM t_db_config WHERE db_id={}) \r\n AND  create_date BETWEEN \'{} 0:0:0\' AND \'{} 23:59:59\' \r\norder by 1','1');
insert  into `t_db_weekly_items`(`id`,`item_type`,`item_code`,`item_desc`,`item_tjsql`,`status`) values (34,'db','backup_time','备份时长[s]','SELECT \r\nDATE_FORMAT(create_date,\'%Y-%m-%d\') AS rq,\r\nelaspsed_backup AS val\r\nFROM `t_db_backup_total`\r\nWHERE db_tag=(SELECT db_tag FROM t_db_config WHERE db_id={}) \r\n AND  create_date BETWEEN \'{} 0:0:0\' AND \'{} 23:59:59\' \r\norder by 1','1');
insert  into `t_db_weekly_items`(`id`,`item_type`,`item_code`,`item_desc`,`item_tjsql`,`status`) values (37,'db','tbs_usage','表空间使用率[%]','SELECT DATE_FORMAT(create_date, \'%Y-%m-%d\') AS rq, \r\n  MAX(db_tbs_usage) AS val \r\nFROM  `t_monitor_task_db_log` \r\nWHERE db_id = {} \r\nAND  create_date BETWEEN \'{} 0:0:0\' and \'{} 23:59:59\' \r\nAND  db_tbs_usage IS NOT NULL AND db_tbs_usage!=\'\' AND db_tbs_usage!=\'None\'\r\nGROUP BY DATE_FORMAT(create_date, \'%Y-%m-%d\')\r\nORDER BY 1','1');
insert  into `t_db_weekly_items`(`id`,`item_type`,`item_code`,`item_desc`,`item_tjsql`,`status`) values (38,'db_detail','server_info','服务器地址:{}','SELECT  \r\n  \'指标\'      AS flag, \r\n \'最小值\'    AS val_min,\r\n  \'最大值\'    AS val_max,\r\n  \'平均值\'    AS val_avg,\r\n  \'当前值\'    AS val_cur,\r\n  \'告警阀值\'  AS threshold,\r\n \'备注  \'    AS message\r\nUNION ALL\r\nSELECT     \r\n   a.flag,  \r\n   a.val_min,\r\n   a.val_max,\r\n   a.val_avg,\r\n   b.val_cur,\r\n   a.threshold,\r\n   a.message\r\nFROM (SELECT \r\n           \'cpu使用率\'                      AS flag, \r\n           ROUND(MIN(cpu_total_usage),2)   AS val_min,\r\n         ROUND(MAX(cpu_total_usage),2)   AS val_max,\r\n         ROUND(AVG(cpu_total_usage),2)   AS val_avg,\r\n        \'阀值:连续3次>85%\'                AS threshold,\r\n        \'未触发告警\'                      AS message\r\n      FROM `t_monitor_task_server_log`\r\n      WHERE server_id=$$SERVER_ID$$\r\n       AND  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\') a,\r\n     (SELECT \r\n          cpu_total_usage   AS val_cur\r\n      FROM `t_monitor_task_server_log` \r\n      WHERE server_id=$$SERVER_ID$$ \r\n       AND  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\'\r\n  ORDER BY create_date DESC LIMIT 1) b\r\nUNION ALL\r\nSELECT     \r\n   a.flag,  \r\n   a.val_min,\r\n   a.val_max,\r\n   a.val_avg,\r\n   b.val_cur,\r\n   a.threshold,\r\n   a.message\r\nFROM (SELECT \r\n           \'内存使用率\'                   AS flag, \r\n           ROUND(MIN(mem_usage),2)       AS val_min,\r\n         ROUND(MAX(mem_usage),2)       AS val_max,\r\n         ROUND(AVG(mem_usage),2)       AS val_avg,\r\n        \'阀值:连续3次>85%\'              AS threshold,\r\n        \'未触发告警\'                    AS message\r\n      FROM `t_monitor_task_server_log`\r\n      WHERE server_id=$$SERVER_ID$$\r\n       AND  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\') a,\r\n     (SELECT \r\n          mem_usage   AS val_cur\r\n      FROM `t_monitor_task_server_log` \r\n      WHERE server_id=$$SERVER_ID$$ \r\n       AND  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\'\r\n  ORDER BY create_date DESC LIMIT 1) b\r\nUNION ALL\r\nSELECT     \r\n   a.flag,  \r\n   a.val_min,\r\n   a.val_max,\r\n   a.val_avg,\r\n   b.val_cur,\r\n   a.threshold,\r\n   a.message\r\nFROM (SELECT \r\n           \'磁盘使用率\'                     AS flag, \r\n            MIN(disk_usage)               AS val_min,\r\n            MAX(disk_usage)               AS val_max,\r\n          \'\'                            AS val_avg,\r\n        \'阀值:连续3次>80%\'              AS threshold,\r\n        \'未触发告警\'                    AS message\r\n      FROM `t_monitor_task_server_log`\r\n      WHERE server_id=$$SERVER_ID$$\r\n       and  disk_usage is not null and disk_usage!=\'\' and disk_usage!=\'None\'\r\n       and  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\' ) a,\r\n     (SELECT \r\n          disk_usage   AS val_cur\r\n      FROM `t_monitor_task_server_log` \r\n      WHERE server_id=$$SERVER_ID$$ \r\n       and  disk_usage is not null and disk_usage!=\'\' and disk_usage!=\'None\'\r\n       and  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\'\r\n ORDER BY create_date DESC LIMIT 1) b','1');
insert  into `t_db_weekly_items`(`id`,`item_type`,`item_code`,`item_desc`,`item_tjsql`,`status`) values (41,'db_detail','db_info','数据库地址:{}:{}/{}','SELECT  \r\n  \'指标\'      AS flag, \r\n \'最小值\'    AS val_min,\r\n  \'最大值\'    AS val_max,\r\n  \'平均值\'    AS val_avg,\r\n  \'当前值\'    AS val_cur,\r\n  \'告警阀值\'  AS threshold,\r\n \'备注  \'    AS message\r\nUNION ALL\r\nSELECT     \r\n   a.flag,  \r\n   a.val_min,\r\n   a.val_max,\r\n   a.val_avg,\r\n   b.val_cur,\r\n   a.threshold,\r\n   a.message\r\nFROM (SELECT \r\n           \'总连接数\' AS flag,  \r\n         MIN(total_connect+0) AS val_min,\r\n        MAX(total_connect+0) AS val_max,\r\n        ROUND(AVG(total_connect+0),2) AS val_avg,\r\n        \'阀值 >300\'                   AS threshold,\r\n       \'未触发告警\'                   AS message\r\n      FROM `t_monitor_task_db_log`\r\n      WHERE db_id=$$DB_ID$$\r\n       AND  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\') a,\r\n     (SELECT \r\n          total_connect+0  AS val_cur\r\n      FROM `t_monitor_task_db_log` \r\n      WHERE db_id=$$DB_ID$$ AND  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\'\r\n ORDER BY create_date DESC LIMIT 1) b\r\nUNION ALL\r\nSELECT     \r\n   a.flag,  \r\n   a.val_min,\r\n   a.val_max,\r\n   a.val_avg,\r\n   b.val_cur,\r\n   a.threshold,\r\n   a.message\r\nFROM (SELECT \r\n       \'活跃连接数\' AS flag,  \r\n    MIN(active_connect+0) AS val_min,\r\n     MAX(active_connect+0) AS val_max,\r\n     ROUND(AVG(total_connect+0),2) AS val_avg,\r\n     \'阀值 >100\'                   AS threshold,\r\n     \'未触发告警\'                   AS message\r\n      FROM `t_monitor_task_db_log`\r\n      WHERE db_id=$$DB_ID$$\r\n       AND  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\') a,\r\n     (SELECT \r\n          active_connect+0  AS val_cur\r\n      FROM `t_monitor_task_db_log` \r\n      WHERE db_id=$$DB_ID$$ \r\n       AND  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\'\r\n  ORDER BY create_date DESC LIMIT 1) b\r\nUNION ALL\r\nSELECT     \r\n   a.flag,  \r\n   a.val_min,\r\n   a.val_max,\r\n   a.val_avg,\r\n   b.val_cur,\r\n   a.threshold,\r\n   a.message\r\nFROM (SELECT \r\n       \'每秒查询率[QPS]\'       AS flag,  \r\n     MIN(db_qps+0)          AS val_min,\r\n    MAX(db_qps+0)          AS val_max,\r\n    ROUND(AVG(db_qps+0),2) AS val_avg,\r\n    \'阀值 >600\'             AS threshold,\r\n     \'未触发告警\'             AS message\r\n      FROM `t_monitor_task_db_log`\r\n      WHERE db_id=$$DB_ID$$\r\n       and  db_qps is not null and db_qps!=\'\' \r\n       and  create_date BETWEEN \'$$TJRQQ$$\' AND \'$$TJRQZ$$\') a,\r\n     (SELECT \r\n          db_qps+0  AS val_cur\r\n      FROM `t_monitor_task_db_log` \r\n      WHERE db_id=$$DB_ID$$ \r\n       and  db_qps is not null and db_qps!=\'\' \r\n       and  create_date BETWEEN \'$$TJRQQ$$\' AND \'$$TJRQZ$$\' \r\n ORDER BY create_date DESC LIMIT 1) b\r\nUNION ALL\r\nSELECT     \r\n   a.flag,  \r\n   a.val_min,\r\n   a.val_max,\r\n   a.val_avg,\r\n   b.val_cur,\r\n   a.threshold,\r\n   a.message\r\nFROM (SELECT \r\n       \'每秒事务数[TPS]\'        AS flag,  \r\n     MIN(db_tps+0)          AS val_min,\r\n      MAX(db_tps+0)          AS val_max,\r\n      ROUND(AVG(db_tps+0),2) AS val_avg,\r\n     \'阀值 >100\'             AS threshold,\r\n     \'未触发告警\'             AS message\r\n      FROM `t_monitor_task_db_log`\r\n      WHERE db_id=$$DB_ID$$\r\n       and  db_tps is not null and db_tps!=\'\' \r\n       AND  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\') a,\r\n     (SELECT \r\n          db_tps+0  AS val_cur\r\n      FROM `t_monitor_task_db_log` \r\n      WHERE db_id=$$DB_ID$$ \r\n      and  db_tps is not null and db_tps!=\'\' \r\n      and  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\'\r\n  ORDER BY create_date DESC LIMIT 1) b\r\nUNION ALL\r\nSELECT     \r\n   a.flag,  \r\n   a.val_min,\r\n   a.val_max,\r\n   a.val_avg,\r\n   b.val_cur,\r\n   a.threshold,\r\n   a.message\r\nFROM (SELECT \r\n       \'表空间使用率\'            AS flag,  \r\n     IFNULL(MIN(db_tbs_usage),\'-\') AS val_min,\r\n        IFNULL(MAX(db_tbs_usage),\'-\') AS val_max,\r\n        \'\' AS val_avg,\r\n        CASE WHEN MIN(db_tbs_usage) IS NULL THEN \'-\' ELSE \'阀值 >85%\'  END   AS threshold,\r\n        CASE WHEN MIN(db_tbs_usage) IS NULL THEN \'-\' ELSE \'未触发告警\' END   AS message\r\n      FROM `t_monitor_task_db_log`\r\n      WHERE db_id=$$DB_ID$$\r\n       and  db_tbs_usage is not null and db_tbs_usage!=\'\' and db_tbs_usage!=\'None\'\r\n       AND  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\') a,\r\n     (SELECT \r\n          db_tbs_usage  AS val_cur\r\n      FROM `t_monitor_task_db_log` \r\n      WHERE db_id=$$DB_ID$$ \r\n      and  db_tbs_usage is not null and db_tbs_usage!=\'\' and db_tbs_usage!=\'None\'\r\n      and  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\'\r\n ORDER BY create_date DESC LIMIT 1) b\r\nUNION ALL\r\nSELECT     \r\n   a.flag,  \r\n   a.val_min,\r\n   a.val_max,\r\n   a.val_avg,\r\n   b.val_cur,\r\n   a.threshold,\r\n   a.message\r\nFROM (SELECT \r\n            \'备份大小[MB]\' AS flag,\r\n            MIN(CASE \r\n                WHEN INSTR(total_size,\'G\')>0 THEN REPLACE(total_size,\'G\',\'\')*1024\r\n                WHEN INSTR(total_size,\'M\')>0 THEN REPLACE(total_size,\'M\',\'\')\r\n                ELSE REPLACE(total_size,\'K\',\'\')/1024\r\n            END) AS val_min,\r\n            MAX(CASE \r\n                WHEN INSTR(total_size,\'G\')>0 THEN REPLACE(total_size,\'G\',\'\')*1024\r\n                WHEN INSTR(total_size,\'M\')>0 THEN REPLACE(total_size,\'M\',\'\')\r\n                ELSE REPLACE(total_size,\'K\',\'\')/1024\r\n            END) AS val_max,\r\n            ROUND(AVG(\r\n            CASE \r\n                WHEN INSTR(total_size,\'G\')>0 THEN REPLACE(total_size,\'G\',\'\')*1024\r\n                WHEN INSTR(total_size,\'M\')>0 THEN REPLACE(total_size,\'M\',\'\')\r\n                ELSE REPLACE(total_size,\'K\',\'\')/1024\r\n            END),2) AS val_avg,\r\n            \'\'    AS threshold,\r\n            \'\'    AS message\r\n        FROM `t_db_backup_total`\r\n        WHERE db_tag=(SELECT db_tag FROM t_db_config WHERE db_id=$$DB_ID$$) \r\n         AND  create_date between \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\' ) a,\r\n     (SELECT \r\n          CASE \r\n                WHEN INSTR(total_size,\'G\')>0 THEN REPLACE(total_size,\'G\',\'\')*1024\r\n                WHEN INSTR(total_size,\'M\')>0 THEN REPLACE(total_size,\'M\',\'\')\r\n                ELSE REPLACE(total_size,\'K\',\'\')/1024\r\n          END  AS val_cur\r\n      FROM `t_db_backup_total` \r\n      WHERE db_tag=(SELECT db_tag FROM t_db_config WHERE db_id=$$DB_ID$$) \r\n       and  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\'\r\n     ORDER BY create_date DESC LIMIT 1) b\r\nUNION ALL\r\nSELECT     \r\n   a.flag,  \r\n   a.val_min,\r\n   a.val_max,\r\n   a.val_avg,\r\n   b.val_cur,\r\n   a.threshold,\r\n   a.message\r\nFROM (SELECT \r\n            \'备份时长[S]\' AS flag,\r\n            MIN(elaspsed_backup) AS val_min,\r\n            MAX(elaspsed_backup) AS val_max,\r\n            ROUND(AVG(elaspsed_backup),2) AS val_avg,\r\n            \'\'    AS threshold,\r\n            \'\'    AS message\r\n        FROM `t_db_backup_total`\r\n        WHERE db_tag=(SELECT db_tag FROM t_db_config WHERE db_id=$$DB_ID$$) \r\n         AND  create_date between \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\' ) a,\r\n     (SELECT \r\n         elaspsed_backup AS val_cur\r\n      FROM `t_db_backup_total` \r\n      WHERE db_tag=(SELECT db_tag FROM t_db_config WHERE db_id=$$DB_ID$$) \r\n       and  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\'\r\n      ORDER BY create_date DESC LIMIT 1) b','1');
insert  into `t_db_weekly_items`(`id`,`item_type`,`item_code`,`item_desc`,`item_tjsql`,`status`) values (44,'app_detail','server_info','服务器地址:{}','SELECT  \r\n \'指标\'      AS flag, \r\n \'最小值\'    AS val_min,\r\n  \'最大值\'    AS val_max,\r\n  \'平均值\'    AS val_avg,\r\n  \'当前值\'    AS val_cur,\r\n  \'告警阀值\'  AS threshold,\r\n \'备注  \'    AS message\r\nUNION ALL\r\nSELECT     \r\n   a.flag,  \r\n   a.val_min,\r\n   a.val_max,\r\n   a.val_avg,\r\n   b.val_cur,\r\n   a.threshold,\r\n   a.message\r\nFROM (SELECT \r\n           \'cpu使用率\'                      AS flag, \r\n           ROUND(MIN(cpu_total_usage),2)   AS val_min,\r\n         ROUND(MAX(cpu_total_usage),2)   AS val_max,\r\n         ROUND(AVG(cpu_total_usage),2)   AS val_avg,\r\n        \'阀值:连续3次>85%\'                AS threshold,\r\n        \'未触发告警\'                      AS message\r\n      FROM `t_monitor_task_server_log`\r\n      WHERE server_id=$$SERVER_ID$$\r\n       AND  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\') a,\r\n     (SELECT \r\n          cpu_total_usage   AS val_cur\r\n      FROM `t_monitor_task_server_log` \r\n      WHERE server_id=$$SERVER_ID$$ \r\n       AND  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\'\r\n  ORDER BY create_date DESC LIMIT 1) b\r\nUNION ALL\r\nSELECT     \r\n   a.flag,  \r\n   a.val_min,\r\n   a.val_max,\r\n   a.val_avg,\r\n   b.val_cur,\r\n   a.threshold,\r\n   a.message\r\nFROM (SELECT \r\n           \'内存使用率\'                   AS flag, \r\n           ROUND(MIN(mem_usage),2)       AS val_min,\r\n         ROUND(MAX(mem_usage),2)       AS val_max,\r\n         ROUND(AVG(mem_usage),2)       AS val_avg,\r\n        \'阀值:连续3次>85%\'              AS threshold,\r\n        \'未触发告警\'                    AS message\r\n      FROM `t_monitor_task_server_log`\r\n      WHERE server_id=$$SERVER_ID$$\r\n       AND  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\') a,\r\n     (SELECT \r\n          mem_usage   AS val_cur\r\n      FROM `t_monitor_task_server_log` \r\n      WHERE server_id=$$SERVER_ID$$ \r\n       AND  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\'\r\n  ORDER BY create_date DESC LIMIT 1) b\r\nUNION ALL\r\nSELECT     \r\n   a.flag,  \r\n   a.val_min,\r\n   a.val_max,\r\n   a.val_avg,\r\n   b.val_cur,\r\n   a.threshold,\r\n   a.message\r\nFROM (SELECT \r\n           \'磁盘使用率\'                     AS flag, \r\n            MIN(disk_usage)               AS val_min,\r\n            MAX(disk_usage)               AS val_max,\r\n          \'\'                            AS val_avg,\r\n        \'阀值:连续3次>80%\'              AS threshold,\r\n        \'未触发告警\'                    AS message\r\n      FROM `t_monitor_task_server_log`\r\n      WHERE server_id=$$SERVER_ID$$\r\n       and  disk_usage is not null and disk_usage!=\'\' and disk_usage!=\'None\'\r\n       and  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\' ) a,\r\n     (SELECT \r\n          disk_usage   AS val_cur\r\n      FROM `t_monitor_task_server_log` \r\n      WHERE server_id=$$SERVER_ID$$ \r\n       and  disk_usage is not null and disk_usage!=\'\' and disk_usage!=\'None\'\r\n       and  create_date BETWEEN \'$$TJRQQ$$ 0:0:0\' and \'$$TJRQZ$$ 23:59:59\'\r\n ORDER BY create_date DESC LIMIT 1) b','1');
insert  into `t_db_weekly_items`(`id`,`item_type`,`item_code`,`item_desc`,`item_tjsql`,`status`) values (45,'week_detail','header','周报详情-标题','SELECT \'    本周投资系统、OA系统、BI系统、乐软系统、结算系统、资产租赁系统、招采系统运行良好，服务均正常，本地及异机备份均正常。\' AS v1','1');
insert  into `t_db_weekly_items`(`id`,`item_type`,`item_code`,`item_desc`,`item_tjsql`,`status`) values (46,'week_detail','body','周报详情-表格','SELECT \'系统名称\'   AS v1,\r\n  \'DB服务\'    AS v2,  \r\n  \'GIT服务\'   AS v3,\r\n  \'NGINX服务\' AS v4,\r\n  \'WEB服务\'   AS v5,\r\n  \'SSO服务\'   AS v6,\r\n  \'备份脚本\'  AS v7,\r\n  \'清理脚本\'  AS v8\r\nUNION ALL\r\nSELECT  \'投资系统\'  AS v1,\r\n  \'g\'         AS v2,  \r\n  \'g\'         AS v3,\r\n  \'\'          AS v4,\r\n  \'\'          AS v5,\r\n  \'\'          AS v6,\r\n  \'\'          AS v7,\r\n  \'\'          AS v8\r\nUNION ALL\r\nSELECT  \'OA系统\'    AS v1,\r\n  \'g\'         AS v2,  \r\n  \'\'          AS v3,\r\n  \'g\'         AS v4,\r\n  \'g,g\'       AS v5,\r\n  \'g,g\'       AS v6,\r\n  \'g\'         AS v7,\r\n  \'\'          AS v8\r\nUNION ALL\r\nSELECT  \'BI系统\'    AS v1,\r\n  \'g\'         AS v2,  \r\n  \'\'          AS v3,\r\n  \'\'          AS v4,\r\n  \'g,g\'       AS v5,\r\n  \'\'          AS v6,\r\n  \'g\'         AS v7,\r\n  \'\'          AS v8\r\nUNION ALL\r\nSELECT  \'乐软系统\'  AS v1,\r\n  \'g\'         AS v2,  \r\n  \'\'          AS v3,\r\n  \'\'          AS v4,\r\n  \'g\'         AS v5,\r\n  \'\'          AS v6,\r\n  \'g\'         AS v7,\r\n  \'\'          AS v8\r\nUNION ALL\r\nSELECT  \'结算系统\'  AS v1,\r\n  \'g,g,g\'     AS v2,  \r\n  \'\'          AS v3,\r\n  \'\'          AS v4,\r\n  \'g,g\'       AS v5,\r\n  \'\'          AS v6,\r\n  \'\'          AS v7,\r\n  \'\'          AS v8\r\nUNION ALL\r\nSELECT  \'资产租赁系统\' AS v1,\r\n   \'g,g\'       AS v2,  \r\n  \'\'          AS v3,\r\n  \'\'          AS v4,\r\n  \'g\'         AS v5,\r\n  \'\'          AS v6,\r\n  \'\'          AS v7,\r\n  \'\'          AS v8 \r\nUNION ALL\r\nSELECT  \'招采系统\'  AS v1,\r\n   \'g\'         AS v2,  \r\n  \'\'          AS v3,\r\n  \'g,g\'       AS v4,\r\n  \'g,g\'       AS v5,\r\n  \'\'          AS v6,\r\n  \'\'          AS v7,\r\n  \'\'          AS v8 \r\nUNION ALL\r\nSELECT  \'备份服务器\' AS v1,\r\n   \'\'           AS v2, \r\n  \'\'           AS v3,\r\n   \'\'           AS v4,\r\n   \'\'           AS v5,\r\n   \'\'           AS v6,\r\n   \'\'           AS v7,\r\n   \'g\'          AS v8 ','1');
insert  into `t_db_weekly_items`(`id`,`item_type`,`item_code`,`item_desc`,`item_tjsql`,`status`) values (47,'week_detail','footer','周报详情-说明','SELECT \'表格说明:;  1、表格内容为空表示没有相应服务;  2、绿灯表示服务正常、红灯表示服务严重故障，黄灯表示一般故障;  3、一个单元格内多个灯表示相同的服务有多个。\' AS v1','1');

/*Data for the table `t_monitor_index` */

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

/*Data for the table `t_monitor_templete` */

insert  into `t_monitor_templete`(`id`,`name`,`code`,`type`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (1,'linux主机模板','linux_templete','1','1','2020-04-02','DBA','2020-04-20','DBA');
insert  into `t_monitor_templete`(`id`,`name`,`code`,`type`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (2,'mysql数据库模板','mysql_templete','2','1','2020-04-02','DBA','2020-08-18','DBA');
insert  into `t_monitor_templete`(`id`,`name`,`code`,`type`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (3,'sqlserver数据库模板','mssql_templete','2','1','2020-04-19','DBA','2020-08-19','DBA');
insert  into `t_monitor_templete`(`id`,`name`,`code`,`type`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (4,'redis数据库模板','redis_templete','2','1','2020-04-28','DBA','2020-04-28','DBA');
insert  into `t_monitor_templete`(`id`,`name`,`code`,`type`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (5,'mongo数据库模板','mongo_templete','2','1','2020-04-28','DBA','2021-01-30','DBA');
insert  into `t_monitor_templete`(`id`,`name`,`code`,`type`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (6,'es数据库模板','es_templete','2','1','2020-04-28','DBA','2020-04-28','DBA');
insert  into `t_monitor_templete`(`id`,`name`,`code`,`type`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`) values (7,'oracle数据库模板','oracle_templete','2','1','2020-07-07','DBA','2020-08-19','DBA');

/*Data for the table `t_db_source` */

insert  into `t_db_source`(`id`,`ip`,`port`,`service`,`status`,`creation_date`,`creator`,`last_update_date`,`updator`,`user`,`password`,`db_type`,`db_source_type`,`db_desc`,`db_env`,`inst_type`,`proxy_status`,`proxy_server`,`market_id`,`flag1`) values (1,'rm-2ze2k586u0g2hnbaq125010.mysql.rds.aliyuncs.com','3306','','1','2021-02-19','DBA','2021-02-19','DBA','puppet','7D86F7A83E38AD4DFB15C0AFEFF7D310','0',NULL,'Easebase平台数据库','1','2','0','','000',NULL);

/*Data for the table `t_user_proj_privs` */

insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (1,1,1,1);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (2,1,1,1);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (3,1,1,1);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (4,1,1,1);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (5,1,1,1);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (6,1,1,1);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (7,1,1,2);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (8,1,1,2);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (9,1,1,2);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (10,1,1,2);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (11,1,1,2);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (12,1,1,2);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (13,1,1,3);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (14,1,1,3);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (15,1,1,3);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (16,1,1,3);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (17,1,1,3);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (18,1,1,3);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (19,1,1,4);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (20,1,1,4);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (21,1,1,4);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (22,1,1,4);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (23,1,1,4);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (24,1,1,4);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (26,1,1,5);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (27,1,1,5);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (28,1,1,5);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (29,1,1,5);
insert  into `t_user_proj_privs`(`id`,`proj_id`,`user_id`,`priv_id`) values (30,1,1,5);


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;


/* Procedure structure for procedure `proc_clear_log` */

/*!50003 DROP PROCEDURE IF EXISTS  `proc_clear_log` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`puppet`@`%` PROCEDURE `proc_clear_log`()
BEGIN
  
  DELETE FROM t_monitor_task_db_log
    WHERE create_date <DATE_ADD(CONCAT(DATE_FORMAT(NOW(),'%Y-%m-%d'),' 0:0:0'),INTERVAL -7 DAY);
  DELETE FROM t_monitor_task_server_log
    WHERE create_date <DATE_ADD(CONCAT(DATE_FORMAT(NOW(),'%Y-%m-%d'),' 0:0:0'),INTERVAL -7 DAY);
    
  DELETE FROM t_db_sync_tasks_log
    WHERE create_date <DATE_ADD(CONCAT(DATE_FORMAT(NOW(),'%Y-%m-%d'),' 0:0:0'),INTERVAL -7 DAY);
    
  DELETE FROM  t_db_sync_tasks_log_detail  
    WHERE create_date <DATE_ADD(CONCAT(DATE_FORMAT(NOW(),'%Y-%m-%d'),' 0:0:0'),INTERVAL -7 DAY);
    
  DELETE FROM t_datax_sync_log
    WHERE create_date <DATE_ADD(CONCAT(DATE_FORMAT(NOW(),'%Y-%m-%d'),' 0:0:0'),INTERVAL -7 DAY);  
    
  DELETE FROM t_db_backup_total
    WHERE create_date <DATE_ADD(CONCAT(DATE_FORMAT(NOW(),'%Y-%m-%d'),' 0:0:0'),INTERVAL -7 DAY);    
  
  DELETE FROM `t_db_backup_detail`
    WHERE create_date <DATE_ADD(CONCAT(DATE_FORMAT(NOW(),'%Y-%m-%d'),' 0:0:0'),INTERVAL -7 DAY);   
    
        DELETE FROM `t_slow_detail`
    WHERE finish_time <DATE_ADD(CONCAT(DATE_FORMAT(NOW(),'%Y-%m-%d'),' 0:0:0'),INTERVAL -7 DAY);       
  
  
END */$$
DELIMITER ;

/* Procedure structure for procedure `proc_tj_service` */

/*!50003 DROP PROCEDURE IF EXISTS  `proc_tj_service` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`puppet`@`%` PROCEDURE `proc_tj_service`()
BEGIN
  DECLARE n_server_id    INT;
  DECLARE v_server_desc  VARCHAR(100);
  DECLARE v_db_desc      VARCHAR(100);
  DECLARE v_db_type      VARCHAR(100);
  DECLARE n_db_available INT;
  DECLARE d_create_date  DATETIME;
  
  DECLARE n_mysql_proj   INT;
  DECLARE n_mssql_flow   INT;
  DECLARE n_mssql_park   INT;
  DECLARE n_mssql_car    INT;
  DECLARE n_mssql_dldf   INT;
  DECLARE n_mssql_sg     INT;
  DECLARE n_oracle_sg    INT;
  DECLARE n_elastic      INT;
  DECLARE n_redis        INT;
  DECLARE n_mongo        INT;
  
  DECLARE v_mysql_proj   VARCHAR(1000);
  DECLARE v_mssql_flow   VARCHAR(1000);
  DECLARE v_mssql_park   VARCHAR(1000);
  DECLARE v_mssql_car    VARCHAR(1000);
  DECLARE v_mssql_dldf   VARCHAR(1000);
  DECLARE v_mssql_sg     VARCHAR(1000);
  DECLARE v_oracle_sg    VARCHAR(1000);
  DECLARE v_elastic      VARCHAR(1000);
  DECLARE v_redis        VARCHAR(1000);
  DECLARE v_mongo        VARCHAR(1000);
  
  DECLARE _outer INT DEFAULT 0;
  DECLARE _inner INT DEFAULT 0;
  DECLARE cur_server  CURSOR FOR SELECT id,server_desc FROM `t_server` WHERE STATUS='1' ORDER BY id;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET _outer = 1;
  
  SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
  START TRANSACTION;
 
  
  
  DELETE FROM t_monitor_service;
  OPEN cur_server;
  out_loop:LOOP
     FETCH NEXT FROM cur_server INTO n_server_id,v_server_desc;
     IF _outer = 1 THEN
  LEAVE out_loop;
     END IF;
     
     
     SELECT 
        COUNT(0),MAX(create_date)  INTO n_mysql_proj,d_create_date
     FROM t_monitor_task_db_log a 
        LEFT JOIN t_server b ON a.server_id=b.id
        LEFT JOIN t_db_source c ON a.db_id=c.id
     WHERE (a.db_id,a.create_date) IN(
            SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
       AND b.id=n_server_id
       AND c.db_type='0';
    
     IF n_mysql_proj >0 THEN
  SELECT 
        GROUP_CONCAT(CONCAT(a.db_available,'@',c.id,'@',a.`create_date`))  INTO v_mysql_proj
  FROM t_monitor_task_db_log a 
     LEFT JOIN t_server b ON a.server_id=b.id
     LEFT JOIN t_db_source c ON a.db_id=c.id
  WHERE (a.db_id,a.create_date) IN(
         SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
    AND b.id=n_server_id
    AND c.db_type='0' ;
    
     ELSE
          SET v_mysql_proj = '';
     END IF;   
     
     
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
     
     
     SELECT 
        COUNT(0) INTO n_mssql_dldf
     FROM t_monitor_task_db_log a 
        LEFT JOIN t_server b ON a.server_id=b.id
        LEFT JOIN t_db_source c ON a.db_id=c.id
     WHERE (a.db_id,a.create_date) IN(
            SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
       AND b.id=n_server_id
       AND c.db_type='2' 
       AND INSTR(c.db_desc,'德利多富')>0;
    
     IF n_mssql_dldf >0 THEN
  SELECT 
        GROUP_CONCAT(CONCAT(a.db_available,'@',c.id,'@',a.`create_date`))   INTO v_mssql_dldf
  FROM t_monitor_task_db_log a 
     LEFT JOIN t_server b ON a.server_id=b.id
     LEFT JOIN t_db_source c ON a.db_id=c.id
  WHERE (a.db_id,a.create_date) IN(
         SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
    AND b.id=n_server_id
    AND c.db_type='2' 
    AND INSTR(c.db_desc,'德利多富')>0;
     ELSE
          SET v_mssql_dldf = '';
     END IF;     
     
     
     SELECT 
        COUNT(0) INTO n_mssql_sg
     FROM t_monitor_task_db_log a 
        LEFT JOIN t_server b ON a.server_id=b.id
        LEFT JOIN t_db_source c ON a.db_id=c.id
     WHERE (a.db_id,a.create_date) IN(
            SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
       AND b.id=n_server_id
       AND c.db_type='2' 
       AND INSTR(c.db_desc,'商管')>0;
    
     IF n_mssql_sg >0 THEN
  SELECT 
        GROUP_CONCAT(CONCAT(a.db_available,'@',c.id,'@',a.`create_date`))   INTO v_mssql_sg
  FROM t_monitor_task_db_log a 
     LEFT JOIN t_server b ON a.server_id=b.id
     LEFT JOIN t_db_source c ON a.db_id=c.id
  WHERE (a.db_id,a.create_date) IN(
         SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
    AND b.id=n_server_id
    AND c.db_type='2' 
    AND INSTR(c.db_desc,'商管')>0;
     ELSE
          SET v_mssql_sg = '';
     END IF;    
     
     
     SELECT 
        COUNT(0) INTO n_oracle_sg
     FROM t_monitor_task_db_log a 
        LEFT JOIN t_server b ON a.server_id=b.id
        LEFT JOIN t_db_source c ON a.db_id=c.id
     WHERE (a.db_id,a.create_date) IN(
            SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
       AND b.id=n_server_id
       AND c.db_type='1' 
       AND INSTR(c.db_desc,'商管')>0;
    
     IF n_oracle_sg >0 THEN
  SELECT 
        GROUP_CONCAT(CONCAT(a.db_available,'@',c.id,'@',a.`create_date`))   INTO v_oracle_sg
  FROM t_monitor_task_db_log a 
     LEFT JOIN t_server b ON a.server_id=b.id
     LEFT JOIN t_db_source c ON a.db_id=c.id
  WHERE (a.db_id,a.create_date) IN(
         SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
    AND b.id=n_server_id
    AND c.db_type='1' 
    AND INSTR(c.db_desc,'商管')>0;
     ELSE
          SET v_oracle_sg = '';
     END IF; 
     
      
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
    
     IF INSTR(v_mysql_proj,'0@')>0 OR INSTR(v_mssql_flow,'0@')>0 OR INSTR(v_mssql_park,'0@')>0 
        OR INSTR(v_mssql_car,'0@')>0  OR INSTR(v_mssql_dldf,'0@')>0 OR INSTR(v_mssql_sg,'0@')>0 OR INSTR(v_oracle_sg,'0@')>0 
           OR INSTR(v_elastic,'0@')>0  OR INSTR(v_redis,'0@')>0 OR INSTR(v_mongo,'0@')>0 THEN 
  
  INSERT INTO t_monitor_service(server_id,server_desc,mysql_proj,mssql_flow,mssql_park,mssql_car,mssql_dldf,mssql_sg,oracle_sg,redis,mongo,es,create_date,sxh)
          VALUES(n_server_id,v_server_desc,v_mysql_proj,v_mssql_flow,v_mssql_park,v_mssql_car,v_mssql_dldf,v_mssql_sg,v_oracle_sg,v_redis,v_mongo,v_elastic, NOW(),-UNIX_TIMESTAMP());                           
     ELSE
        INSERT INTO t_monitor_service(server_id,server_desc,mysql_proj,mssql_flow,mssql_park,mssql_car,mssql_dldf,mssql_sg,oracle_sg,redis,mongo,es,create_date,sxh)
          VALUES(n_server_id,v_server_desc,v_mysql_proj,v_mssql_flow,v_mssql_park,v_mssql_car,v_mssql_dldf,v_mssql_sg,v_oracle_sg,v_redis,v_mongo,v_elastic,NOW(),UNIX_TIMESTAMP());
     END IF;     
       
  END LOOP;  
  
  
  COMMIT;
END */$$
DELIMITER ;

/* Procedure structure for procedure `proc_tj_sync_monitor` */

/*!50003 DROP PROCEDURE IF EXISTS  `proc_tj_sync_monitor` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`puppet`@`%` PROCEDURE `proc_tj_sync_monitor`()
BEGIN
  DECLARE v_market_id         VARCHAR(10);
  DECLARE v_market_name       VARCHAR(100);
  DECLARE v_flow_flag         VARCHAR(1000);
  DECLARE v_flow_real_flag    VARCHAR(1000);
  DECLARE v_flow_device_flag  VARCHAR(1000);
  DECLARE v_park_flag         VARCHAR(1000);
  DECLARE v_park_real_flag    VARCHAR(1000);
  declare v_sales_dldf_flag   VARCHAR(1000);
  DECLARE _outer              INT DEFAULT 0;
  DECLARE _inner              INT DEFAULT 0;
  DECLARE cur_market          CURSOR FOR SELECT dmm,dmmc FROM `t_dmmx` WHERE dm='05' AND flag='1' ORDER BY dmm;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET _outer = 1;
  
  SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
  START TRANSACTION;
 
  DELETE FROM t_db_sync_monitor;
  OPEN cur_market;
  out_loop:LOOP
     FETCH NEXT FROM cur_market INTO v_market_id,v_market_name;
     IF _outer = 1 THEN
  LEAVE out_loop;
     END IF;
     
     
     set v_flow_flag='';
     SELECT 
     IFNULL(GROUP_CONCAT(flag,'@',sync_tag,'@',create_date),'') into v_flow_flag
     FROM ( SELECT 
         CASE WHEN TIMESTAMPDIFF(HOUR, MAX(create_date), NOW())>6 THEN 1 ELSE 0 END flag,    
         sync_tag,
         MAX(create_date) AS create_date
       FROM t_db_sync_tasks_log l 
       WHERE l.sync_tag IN(
      SELECT sync_tag FROM `t_db_sync_config` 
        WHERE INSTR(sync_col_val,v_market_id)>0 
         AND STATUS='1' AND sync_ywlx='1' )
     GROUP BY sync_tag
     ORDER BY CASE WHEN INSTR(sync_tag,'proj')>0 THEN 1 
           WHEN INSTR(sync_tag,'stage')>0 THEN 2 
           WHEN INSTR(sync_tag,'bi')>0 THEN 3
           ELSE 4 END 
     ) X;
  
     
     SET v_flow_real_flag='';
     SELECT 
     IFNULL(GROUP_CONCAT(flag,'@',sync_tag,'@',create_date),'') INTO v_flow_real_flag
     FROM ( SELECT 
         CASE WHEN TIMESTAMPDIFF(HOUR, MAX(create_date), NOW())>3 THEN 1 ELSE 0 END flag,    
         sync_tag,
         MAX(create_date) AS create_date
       FROM t_db_sync_tasks_log l
        WHERE l.sync_tag IN(
      SELECT sync_tag FROM `t_db_sync_config` 
        WHERE INSTR(sync_col_val,v_market_id)>0 
         AND STATUS='1' AND sync_ywlx='2' )
     GROUP BY sync_tag
     ORDER BY CASE WHEN INSTR(sync_tag,'proj')>0 THEN 1 
           WHEN INSTR(sync_tag,'stage')>0 THEN 2 
           WHEN INSTR(sync_tag,'bi')>0 THEN 3
           ELSE 4 END 
     ) X;
             
     
     SET v_flow_device_flag='';
     SELECT 
    IFNULL(GROUP_CONCAT(flag,'@',sync_tag,'@',create_date),'') INTO v_flow_device_flag
     FROM ( SELECT 
         CASE WHEN TIMESTAMPDIFF(MINUTE, MAX(create_date), NOW())>30 THEN 1 ELSE 0 END flag,    
         sync_tag,
         MAX(create_date) AS create_date
       FROM t_db_sync_tasks_log l
       WHERE l.sync_tag IN(
      SELECT sync_tag FROM `t_db_sync_config` 
        WHERE INSTR(sync_col_val,v_market_id)>0 
         AND STATUS='1' AND sync_ywlx='5' )
     GROUP BY sync_tag
     ORDER BY CASE WHEN INSTR(sync_tag,'proj')>0 THEN 1 
           WHEN INSTR(sync_tag,'stage')>0 THEN 2 
           WHEN INSTR(sync_tag,'bi')>0 THEN 3
           ELSE 4 END  
     ) X;
     
       
     SET v_park_flag='';
     SELECT 
     IFNULL(GROUP_CONCAT(flag,'@',sync_tag,'@',create_date),'') INTO v_park_flag
     FROM ( SELECT 
         CASE WHEN TIMESTAMPDIFF(HOUR, MAX(create_date), NOW())>6 THEN 1 
        WHEN TIMESTAMPDIFF(HOUR, MAX(create_date), NOW())<=6 AND MAX(amount) = 0 THEN 1        
         ELSE 0 END flag, 
         sync_tag,
         MAX(create_date) AS create_date
       FROM t_db_sync_tasks_log l
       WHERE  l.sync_tag IN(
      SELECT sync_tag FROM `t_db_sync_config` 
        WHERE INSTR(sync_col_val,v_market_id)>0 
         AND STATUS='1' AND sync_ywlx='3' )
     GROUP BY sync_tag
     ORDER BY CASE WHEN INSTR(sync_tag,'proj')>0 THEN 1 
           WHEN INSTR(sync_tag,'stage')>0 THEN 2 
           WHEN INSTR(sync_tag,'bi')>0 THEN 3
           ELSE 4 END  
     ) X;
  
     
     SET v_park_real_flag='';
     SELECT 
     IFNULL(GROUP_CONCAT(flag,'@',sync_tag,'@',create_date),'') INTO v_park_real_flag
     FROM ( SELECT 
         CASE WHEN TIMESTAMPDIFF(HOUR, MAX(create_date), NOW())>3 THEN 1 
        WHEN TIMESTAMPDIFF(HOUR, MAX(create_date), NOW())<=3 AND MAX(amount) = 0 THEN 1          
         ELSE 0 END flag,    
         sync_tag,
         MAX(create_date) AS create_date
       FROM t_db_sync_tasks_log l 
       WHERE  l.sync_tag IN(
      SELECT sync_tag FROM `t_db_sync_config` 
        WHERE INSTR(sync_col_val,v_market_id)>0 
         AND STATUS='1' AND sync_ywlx='4' )
     GROUP BY sync_tag
     ORDER BY CASE WHEN INSTR(sync_tag,'proj')>0 THEN 1 
           WHEN INSTR(sync_tag,'stage')>0 THEN 2 
           WHEN INSTR(sync_tag,'bi')>0 THEN 3
           ELSE 4 END  
     ) X;    
      
     
     SET v_sales_dldf_flag='';
     SELECT 
     IFNULL(GROUP_CONCAT(flag,'@',sync_tag,'@',create_date),'') INTO v_sales_dldf_flag
     FROM ( SELECT 
         CASE WHEN TIMESTAMPDIFF(HOUR, MAX(create_date), NOW())>3 THEN 1 ELSE 0 END flag,    
         sync_tag,
         MAX(create_date) AS create_date
       FROM t_db_sync_tasks_log l
       WHERE l.sync_tag IN(
      SELECT sync_tag FROM `t_db_sync_config` 
        WHERE INSTR(sync_col_val,v_market_id)>0 
         AND STATUS='1' AND sync_ywlx='8' )
     GROUP BY sync_tag
     ORDER BY CASE WHEN INSTR(sync_tag,'proj')>0 THEN 1 
           WHEN INSTR(sync_tag,'stage')>0 THEN 2 
           WHEN INSTR(sync_tag,'bi')>0 THEN 3
           ELSE 4 END  
     ) X;      
      
      INSERT INTO t_db_sync_monitor(market_id,market_name,flow_flag,flow_real_flag,flow_device_flag,park_flag,park_real_flag,sales_dldf_flag,create_date)
          VALUES(v_market_id,v_market_name,v_flow_flag,v_flow_real_flag,v_flow_device_flag,v_park_flag,v_park_real_flag,v_sales_dldf_flag,now());                 
      
  END LOOP;  
  
  
  COMMIT;
END */$$
DELIMITER ;

/* Procedure structure for procedure `proc_trunc_log` */

/*!50003 DROP PROCEDURE IF EXISTS  `proc_trunc_log` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`puppet`@`%` PROCEDURE `proc_trunc_log`()
BEGIN
  
  TRUNCATE TABLE t_monitor_task_db_log;
  TRUNCATE TABLE t_monitor_task_server_log;
  TRUNCATE TABLE t_db_sync_tasks_log;
  TRUNCATE TABLE t_db_sync_tasks_log_detail;
  TRUNCATE TABLE t_datax_sync_log;
  TRUNCATE TABLE t_slow_detail;
  
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
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
