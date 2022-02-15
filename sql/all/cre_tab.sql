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

/*Table structure for table `docker_log` */

DROP TABLE IF EXISTS `docker_log`;

CREATE TABLE `docker_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cmd` varchar(1000) DEFAULT NULL,
  `msg` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;

/*Table structure for table `docker_log_data` */

DROP TABLE IF EXISTS `docker_log_data`;

CREATE TABLE `docker_log_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `msg` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=384 DEFAULT CHARSET=utf8mb4;

/*Table structure for table `t_bbgl_config` */

DROP TABLE IF EXISTS `t_bbgl_config`;

CREATE TABLE `t_bbgl_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bbdm` varchar(50) DEFAULT NULL,
  `bbmc` varchar(100) DEFAULT NULL,
  `dsid` varchar(10) DEFAULT NULL,
  `db` varchar(100) DEFAULT NULL,
  `statement` longtext,
  `description` varchar(100) DEFAULT NULL,
  `header_status` varchar(20) DEFAULT NULL,
  `filter_status` varchar(20) DEFAULT NULL,
  `pre_process_status` varchar(20) DEFAULT NULL,
  `creator` varchar(50) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `last_update_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_bbdm_u1` (`bbdm`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4;

/*Table structure for table `t_bbgl_export` */

DROP TABLE IF EXISTS `t_bbgl_export`;

CREATE TABLE `t_bbgl_export` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bbdm` varchar(50) DEFAULT NULL,
  `filter` varchar(200) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL COMMENT 'dm=43',
  `file` varchar(100) DEFAULT NULL,
  `real_file` varchar(200) DEFAULT NULL,
  `size` varchar(50) DEFAULT NULL,
  `process` varchar(50) DEFAULT NULL,
  `creator` varchar(50) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `error` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8mb4;

/*Table structure for table `t_bbgl_filter` */

DROP TABLE IF EXISTS `t_bbgl_filter`;

CREATE TABLE `t_bbgl_filter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bbdm` varchar(50) DEFAULT NULL,
  `xh` int(11) DEFAULT NULL,
  `filter_name` varchar(100) DEFAULT NULL,
  `filter_code` varchar(50) DEFAULT NULL,
  `filter_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

/*Table structure for table `t_bbgl_header` */

DROP TABLE IF EXISTS `t_bbgl_header`;

CREATE TABLE `t_bbgl_header` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bbdm` varchar(50) DEFAULT NULL,
  `xh` int(11) DEFAULT NULL,
  `header_name` varchar(50) DEFAULT NULL,
  `header_width` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4;

/*Table structure for table `t_bbgl_preproccess` */

DROP TABLE IF EXISTS `t_bbgl_preproccess`;

CREATE TABLE `t_bbgl_preproccess` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bbdm` varchar(50) DEFAULT NULL,
  `xh` int(11) DEFAULT NULL,
  `statement` longtext,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4;

/*Table structure for table `t_bbtj_log` */

DROP TABLE IF EXISTS `t_bbtj_log`;

CREATE TABLE `t_bbtj_log` (
  `market_id` varchar(20) NOT NULL,
  `bbdm` varchar(20) NOT NULL,
  `tjrq` varchar(10) NOT NULL,
  `v1` varchar(20) DEFAULT NULL,
  `v2` varchar(20) DEFAULT NULL,
  `v3` varchar(20) DEFAULT NULL,
  `v4` varchar(20) DEFAULT NULL,
  `v5` varchar(20) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`market_id`,`bbdm`,`tjrq`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_bbtj_sql` */

DROP TABLE IF EXISTS `t_bbtj_sql`;

CREATE TABLE `t_bbtj_sql` (
  `bbdm` varchar(20) NOT NULL,
  `xh` int(11) NOT NULL,
  `item` varchar(20) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `statement` text,
  `ds_id` int(11) DEFAULT NULL,
  `flag` varchar(1) DEFAULT NULL COMMENT '是否有效',
  `desc` varchar(100) DEFAULT NULL COMMENT '描述',
  PRIMARY KEY (`bbdm`,`xh`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
  `doris_id` varchar(10) DEFAULT NULL COMMENT 'doris数据源ID',
  `doris_db_name` varchar(50) DEFAULT NULL COMMENT 'doris数据库名',
  `doris_tab_name` varchar(100) DEFAULT NULL COMMENT 'doris表名',
  `doris_batch_size` varchar(10) DEFAULT NULL COMMENT 'doris同步批大小',
  `doris_jvm` varchar(100) DEFAULT NULL COMMENT '运行datax工具内存配置',
  `doris_tab_config` varchar(1000) DEFAULT NULL COMMENT 'doris表个性化配置',
  `doris_sync_type` varchar(1) DEFAULT NULL COMMENT 'doris同步类型dm=44',
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
) ENGINE=InnoDB AUTO_INCREMENT=200 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=339361 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=1364 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=1199098 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=49266 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_compare` */

DROP TABLE IF EXISTS `t_db_compare`;

CREATE TABLE `t_db_compare` (
  `dsid` int(11) NOT NULL,
  `table_schema` varchar(64) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `table_name` varchar(64) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `column_name` varchar(64) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `is_nullable` varchar(3) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `data_type` varchar(64) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `column_default` longtext CHARACTER SET utf8,
  `character_maximum_length` varchar(50) DEFAULT NULL,
  `numeric_precision` varchar(50) DEFAULT NULL,
  `character_set_name` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `collation_name` varchar(100) DEFAULT NULL,
  `column_type` longtext CHARACTER SET utf8 NOT NULL,
  `column_key` varchar(3) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `extra` varchar(30) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `column_comment` varchar(1024) CHARACTER SET utf8 NOT NULL DEFAULT '',
  KEY `idx_t_db_compare_c1` (`dsid`,`table_schema`,`table_name`,`column_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Table structure for table `t_db_compare_data` */

DROP TABLE IF EXISTS `t_db_compare_data`;

CREATE TABLE `t_db_compare_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sour_dsid` int(11) DEFAULT NULL,
  `dest_dsid` int(11) DEFAULT NULL,
  `sour_schema` varchar(100) DEFAULT NULL,
  `dest_schema` varchar(100) DEFAULT NULL,
  `dest_table` varchar(100) DEFAULT NULL,
  `sour_rows` int(11) DEFAULT NULL,
  `dest_rows` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;

/*Table structure for table `t_db_compare_detail` */

DROP TABLE IF EXISTS `t_db_compare_detail`;

CREATE TABLE `t_db_compare_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `property_name` varchar(100) DEFAULT NULL,
  `sour_property_value` varchar(500) DEFAULT NULL,
  `desc_property_value` varchar(500) DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL,
  `statement` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4;

/*Table structure for table `t_db_compare_idx` */

DROP TABLE IF EXISTS `t_db_compare_idx`;

CREATE TABLE `t_db_compare_idx` (
  `dsid` int(11) DEFAULT NULL,
  `table_schema` varchar(100) DEFAULT NULL,
  `table_name` varchar(100) DEFAULT NULL,
  `index_name` varchar(100) DEFAULT NULL,
  `index_type` varchar(100) DEFAULT NULL,
  `is_unique` varchar(100) DEFAULT NULL,
  `seq_in_index` varchar(100) DEFAULT NULL,
  `column_name` varchar(100) DEFAULT NULL,
  `nullable` varchar(100) DEFAULT NULL,
  `visible` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_inst_log` */

DROP TABLE IF EXISTS `t_db_inst_log`;

CREATE TABLE `t_db_inst_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `inst_id` int(11) DEFAULT NULL COMMENT '实例ID',
  `type` varchar(20) DEFAULT NULL COMMENT '日志类型',
  `message` varchar(1000) DEFAULT NULL COMMENT '日志消息',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8359 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=326 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=5430 DEFAULT CHARSET=utf8;

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

/*Table structure for table `t_db_opt_log` */

DROP TABLE IF EXISTS `t_db_opt_log`;

CREATE TABLE `t_db_opt_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` int(11) DEFAULT NULL COMMENT '用户ID',
  `ds_id` int(11) DEFAULT NULL COMMENT '数据源ID',
  `db` varchar(50) DEFAULT NULL COMMENT '数据库名称',
  `statement` text COMMENT 'SQL语句',
  `start_time` varchar(20) DEFAULT NULL COMMENT '开始时间',
  `end_time` varchar(20) DEFAULT NULL COMMENT '完成时间',
  `status` varchar(1) DEFAULT NULL COMMENT '执行状态',
  `message` text COMMENT '错误消息',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_source` */

DROP TABLE IF EXISTS `t_db_source`;

CREATE TABLE `t_db_source` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `id_ro` varchar(11) DEFAULT NULL COMMENT '从库数据源ID',
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
  `stream_load` varchar(100) DEFAULT NULL COMMENT 'stream_load服务',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=195 DEFAULT CHARSET=utf8;

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
  `sync_table` text COMMENT '同步表列表',
  `batch_size` int(11) DEFAULT NULL COMMENT '全量批大小',
  `batch_size_incr` int(11) DEFAULT NULL COMMENT '增量批大小',
  `sync_gap` varchar(10) DEFAULT NULL COMMENT '同步间隔',
  `sync_col_val` varchar(100) DEFAULT NULL COMMENT '同步新增列值',
  `sync_col_name` varchar(50) DEFAULT NULL COMMENT '同步新增列名',
  `sync_repair_day` int(11) DEFAULT '7' COMMENT '自动修复天数',
  `sync_time_type` varchar(50) DEFAULT NULL COMMENT '同步时间类型',
  `script_path` varchar(200) DEFAULT NULL COMMENT '同步代理路径',
  `script_file` varchar(100) DEFAULT NULL COMMENT '同步代理文件名',
  `python3_home` varchar(200) DEFAULT NULL COMMENT 'PYTHON3路径',
  `api_server` varchar(1000) DEFAULT NULL COMMENT 'API服务器',
  `status` varchar(1) DEFAULT NULL COMMENT '同步状态',
  `task_status` varchar(1) DEFAULT '0' COMMENT '任务状态',
  `task_create_time` datetime DEFAULT NULL,
  `process_num` int(11) DEFAULT NULL COMMENT '进程数',
  `apply_timeout` int(11) DEFAULT NULL COMMENT '配置更新间隔',
  `desc_db_prefix` varchar(50) DEFAULT NULL COMMENT '目标库前缀',
  `log_db_id` int(11) DEFAULT NULL COMMENT '日志库ID',
  `log_db_name` varchar(100) DEFAULT NULL COMMENT '日志库名称',
  PRIMARY KEY (`id`),
  KEY `idx_t_db_config_u1` (`sync_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=533 DEFAULT CHARSET=utf8 COMMENT='数据库同步配置表';

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

/*Table structure for table `t_db_sync_real_log` */

DROP TABLE IF EXISTS `t_db_sync_real_log`;

CREATE TABLE `t_db_sync_real_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `sync_tag` varchar(1000) NOT NULL COMMENT '同步标识',
  `event_amount` int(11) DEFAULT NULL COMMENT '事件总数',
  `insert_amount` int(11) DEFAULT NULL COMMENT 'insert事件数',
  `update_amount` int(11) DEFAULT NULL COMMENT 'update事件数',
  `delete_amount` int(11) DEFAULT NULL COMMENT 'delete事件数',
  `ddl_amount` int(11) DEFAULT NULL COMMENT 'ddl事件数',
  `c_binlogfile` varchar(100) DEFAULT NULL COMMENT '当前binlogfile',
  `c_binlogpos` varchar(20) DEFAULT NULL COMMENT '当前binlogpos',
  `binlogfile` varchar(100) DEFAULT NULL COMMENT '同步binlogfile',
  `binlogpos` varchar(20) DEFAULT NULL COMMENT '同步binlogpos',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_create_date_n1` (`create_date`),
  KEY `idx_create_date_u1` (`sync_tag`(255)),
  KEY `idx_sync_tag_create_date` (`sync_tag`(255),`create_date`)
) ENGINE=InnoDB AUTO_INCREMENT=1389014 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_sync_tab_config` */

DROP TABLE IF EXISTS `t_db_sync_tab_config`;

CREATE TABLE `t_db_sync_tab_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `sync_tag` varchar(200) DEFAULT NULL COMMENT '同步标识',
  `db_name` varchar(50) DEFAULT NULL COMMENT '数据库名称',
  `schema_name` varchar(50) DEFAULT NULL COMMENT '数据模式名称',
  `tab_name` varchar(50) DEFAULT NULL COMMENT '表名称',
  `sync_cols` text COMMENT '同步列列表',
  `sync_incr_col` varchar(50) DEFAULT NULL COMMENT '增量同步列',
  `sync_time` varchar(10) DEFAULT NULL COMMENT '同步时间',
  `status` varchar(1) DEFAULT NULL COMMENT '同步状态',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `update_date` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_t_db_sync_tab_config_n1` (`sync_tag`),
  KEY `idx_t_db_sync_tab_config_u1` (`sync_tag`,`db_name`,`schema_name`,`tab_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4407 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_sync_tasks_log` */

DROP TABLE IF EXISTS `t_db_sync_tasks_log`;

CREATE TABLE `t_db_sync_tasks_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `sync_tag` varchar(1000) NOT NULL COMMENT '同步标识',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `duration` int(11) DEFAULT NULL COMMENT '同步时长(s)',
  `amount` int(11) DEFAULT NULL COMMENT '同步数量',
  PRIMARY KEY (`id`),
  KEY `idx_create_date_n1` (`create_date`),
  KEY `idx_create_date_u1` (`sync_tag`(255)),
  KEY `idx_sync_tag_create_date` (`sync_tag`(255),`create_date`)
) ENGINE=InnoDB AUTO_INCREMENT=169242 DEFAULT CHARSET=utf8;

/*Table structure for table `t_db_sync_tasks_log_detail` */

DROP TABLE IF EXISTS `t_db_sync_tasks_log_detail`;

CREATE TABLE `t_db_sync_tasks_log_detail` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `sync_tag` varchar(1000) NOT NULL COMMENT '同步标识',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `sync_table` varchar(1000) DEFAULT NULL COMMENT '同步表',
  `sync_amount` int(11) DEFAULT NULL COMMENT '同步数量',
  `duration` int(11) DEFAULT NULL COMMENT '同步时长(s)',
  PRIMARY KEY (`id`),
  KEY `idx_create_date_n1` (`create_date`),
  KEY `idx_create_date_u1` (`sync_tag`(255))
) ENGINE=InnoDB AUTO_INCREMENT=1543901 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8;

/*Table structure for table `t_func` */

DROP TABLE IF EXISTS `t_func`;

CREATE TABLE `t_func` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `func_name` varchar(100) DEFAULT NULL COMMENT '功能名称',
  `func_url` varchar(1000) DEFAULT NULL COMMENT '功能URL',
  `priv_id` varchar(100) DEFAULT NULL COMMENT '权限ID',
  `status` varchar(1) DEFAULT NULL COMMENT '状态',
  `creation_date` date DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(20) DEFAULT NULL COMMENT '创建人',
  `last_update_date` date DEFAULT NULL COMMENT '最近更新时间',
  `updator` varchar(20) DEFAULT NULL COMMENT '更新人',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=227 DEFAULT CHARSET=utf8;

/*Table structure for table `t_kpi_bbtj` */

DROP TABLE IF EXISTS `t_kpi_bbtj`;

CREATE TABLE `t_kpi_bbtj` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bbrq` date DEFAULT NULL,
  `item_type` varchar(10) DEFAULT NULL,
  `item_name` varchar(100) DEFAULT NULL,
  `market_id` varchar(100) DEFAULT NULL,
  `market_name` varchar(100) DEFAULT NULL,
  `item_value` varchar(100) DEFAULT NULL,
  `item_month` varchar(100) DEFAULT NULL,
  `item_rate` varchar(100) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7743 DEFAULT CHARSET=utf8mb4;

/*Table structure for table `t_kpi_item` */

DROP TABLE IF EXISTS `t_kpi_item`;

CREATE TABLE `t_kpi_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_type` varchar(10) DEFAULT NULL,
  `item_name` varchar(100) DEFAULT NULL,
  `market_name` varchar(100) DEFAULT NULL,
  `market_id` varchar(100) DEFAULT NULL,
  `is_stat` varchar(3) DEFAULT NULL,
  `stat_sql_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=151 DEFAULT CHARSET=utf8mb4;

/*Table structure for table `t_kpi_item_log` */

DROP TABLE IF EXISTS `t_kpi_item_log`;

CREATE TABLE `t_kpi_item_log` (
  `item_type` varchar(10) DEFAULT NULL,
  `item_name` varchar(100) DEFAULT NULL,
  `market_id` varchar(100) DEFAULT NULL,
  `market_name` varchar(100) DEFAULT NULL,
  `stat_sql_id` int(11) DEFAULT NULL,
  `xh` int(11) DEFAULT NULL,
  `statement` text,
  `item_value` varchar(100) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Table structure for table `t_kpi_item_sql` */

DROP TABLE IF EXISTS `t_kpi_item_sql`;

CREATE TABLE `t_kpi_item_sql` (
  `stat_sql_id` int(11) DEFAULT NULL,
  `xh` int(11) DEFAULT NULL,
  `statement` text,
  `value` varchar(100) DEFAULT NULL COMMENT '当前统计结果',
  `dsid` varchar(20) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Table structure for table `t_kpi_item_value` */

DROP TABLE IF EXISTS `t_kpi_item_value`;

CREATE TABLE `t_kpi_item_value` (
  `item_month` varchar(7) NOT NULL,
  `market_name` varchar(100) NOT NULL,
  `item_name` varchar(100) NOT NULL,
  `item_value` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`market_name`,`item_month`,`item_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Table structure for table `t_kpi_label` */

DROP TABLE IF EXISTS `t_kpi_label`;

CREATE TABLE `t_kpi_label` (
  `label_id` varchar(20) NOT NULL,
  `market_id` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`label_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=110808 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_project` */

DROP TABLE IF EXISTS `t_monitor_project`;

CREATE TABLE `t_monitor_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `market_id` varchar(11) DEFAULT NULL,
  `market_name` varchar(100) DEFAULT NULL,
  `ip_dx` varchar(20) DEFAULT NULL,
  `ip_lt` varchar(20) DEFAULT NULL,
  `ip_dx_status` varchar(10) DEFAULT NULL,
  `ip_lt_status` varchar(10) DEFAULT NULL,
  `link_status` varchar(10) DEFAULT NULL,
  `strategy` varchar(20) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_project_err` */

DROP TABLE IF EXISTS `t_monitor_project_err`;

CREATE TABLE `t_monitor_project_err` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `market_id` varchar(20) DEFAULT NULL,
  `link_status` varchar(20) DEFAULT NULL,
  `error_times` int(11) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_project_log` */

DROP TABLE IF EXISTS `t_monitor_project_log`;

CREATE TABLE `t_monitor_project_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `market_id` int(11) DEFAULT NULL,
  `ip_dx_status` varchar(10) DEFAULT NULL,
  `ip_lt_status` varchar(10) DEFAULT NULL,
  `link_status` varchar(10) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8923959 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=115 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=57505370 DEFAULT CHARSET=utf8;

/*Table structure for table `t_monitor_task` */

DROP TABLE IF EXISTS `t_monitor_task`;

CREATE TABLE `t_monitor_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `task_tag` varchar(50) DEFAULT NULL COMMENT '任务标识',
  `server_id` varchar(20) DEFAULT NULL COMMENT '服务器ID',
  `db_id` varchar(20) DEFAULT NULL COMMENT '数据源ID',
  `templete_id` varchar(20) DEFAULT NULL COMMENT '模板ID',
  `comments` varchar(50) DEFAULT NULL COMMENT '任务描述',
  `run_time` varchar(20) DEFAULT NULL COMMENT '运行时间',
  `script_path` varchar(200) DEFAULT NULL COMMENT '代理路径',
  `script_file` varchar(100) DEFAULT NULL COMMENT '代理文件名',
  `python3_home` varchar(200) DEFAULT NULL COMMENT 'python3路径',
  `api_server` varchar(100) DEFAULT NULL COMMENT 'api服务地址',
  `status` varchar(1) DEFAULT NULL COMMENT '任务状态',
  `receiver` varchar(100) DEFAULT NULL COMMENT '监控收件人',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_t_monitor_task_u1` (`task_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=359 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=471778 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=358818 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=161 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=28189 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=5261 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=173 DEFAULT CHARSET=utf8;

/*Table structure for table `t_slow_detail` */

DROP TABLE IF EXISTS `t_slow_detail`;

CREATE TABLE `t_slow_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `inst_id` varchar(40) DEFAULT NULL COMMENT '实例ID',
  `db_id` varchar(40) DEFAULT NULL COMMENT '数据源ID',
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
  KEY `idx_t_slow_detail_n4` (`finish_time`),
  KEY `idx_t_slow_detail_n5` (`finish_time`,`inst_id`,`db`),
  KEY `idx_t_slow_detail_n6` (`finish_time`,`inst_id`,`USER`),
  KEY `idx_t_slow_detail_n7` (`db_id`,`finish_time`,`db`),
  KEY `idx_t_slow_detail_n8` (`db_id`,`finish_time`,`USER`)
) ENGINE=InnoDB AUTO_INCREMENT=999352 DEFAULT CHARSET=utf8;

/*Table structure for table `t_slow_detail_mssql` */

DROP TABLE IF EXISTS `t_slow_detail_mssql`;

CREATE TABLE `t_slow_detail_mssql` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ds_id` varchar(40) DEFAULT NULL,
  `sql_id` varchar(40) DEFAULT NULL,
  `dbname` varchar(100) DEFAULT NULL,
  `loginame` varchar(100) DEFAULT NULL,
  `hostname` varchar(100) NOT NULL,
  `first_time` varchar(20) DEFAULT NULL,
  `last_time` varchar(20) DEFAULT NULL,
  `query_time` int(11) DEFAULT NULL,
  `physical_io` int(11) DEFAULT NULL,
  `cmd` varchar(20) DEFAULT NULL,
  `sql_text` longtext,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1097968 DEFAULT CHARSET=utf8;

/*Table structure for table `t_slow_detail_oracle` */

DROP TABLE IF EXISTS `t_slow_detail_oracle`;

CREATE TABLE `t_slow_detail_oracle` (
  `ds_id` varchar(40) DEFAULT NULL,
  `dbid` varchar(20) NOT NULL,
  `username` varchar(20) NOT NULL,
  `sql_id` varchar(50) NOT NULL,
  `priority` varchar(20) DEFAULT NULL,
  `first_time` varchar(20) DEFAULT NULL,
  `last_time` varchar(20) DEFAULT NULL,
  `executions` int(11) DEFAULT NULL,
  `total_time` int(11) DEFAULT NULL,
  `avg_time` int(11) DEFAULT NULL,
  `rows_processed` int(11) DEFAULT NULL,
  `disk_reads` int(11) DEFAULT NULL,
  `buffer_gets` int(11) DEFAULT NULL,
  `sql_text` longtext,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`dbid`,`username`,`sql_id`),
  UNIQUE KEY `idx_t_slow_detail_oracle_sql_id` (`sql_id`),
  KEY `idx_t_slow_detail_oracle_ds_id` (`ds_id`,`first_time`,`last_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `t_slow_log` */

DROP TABLE IF EXISTS `t_slow_log`;

CREATE TABLE `t_slow_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `inst_id` varchar(20) NOT NULL COMMENT '实例ID',
  `server_id` int(11) DEFAULT NULL COMMENT '服务器ID',
  `ds_id` varchar(20) DEFAULT NULL COMMENT '数据源ID',
  `db_type` varchar(20) DEFAULT '0' COMMENT '数据库类型',
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
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=13593 DEFAULT CHARSET=utf8;

/*Table structure for table `t_sql_backup` */

DROP TABLE IF EXISTS `t_sql_backup`;

CREATE TABLE `t_sql_backup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `release_id` bigint(20) DEFAULT NULL,
  `rollback_statement` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16382 DEFAULT CHARSET=utf8;

/*Table structure for table `t_sql_release` */

DROP TABLE IF EXISTS `t_sql_release`;

CREATE TABLE `t_sql_release` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `dbid` int(11) NOT NULL COMMENT '数据源ID',
  `db` varchar(50) DEFAULT NULL COMMENT '数据库名称',
  `sqltext` longtext COMMENT 'SQL文本',
  `status` varchar(1) DEFAULT NULL COMMENT '0:已发布,1:审核成功，2:审核失败,3:执行中,4:执行成功，5:执行失败,6:已驳回,7:准备执行',
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
  `binlog_file` varchar(100) DEFAULT NULL COMMENT '二进制文件名',
  `start_pos` varchar(20) DEFAULT NULL COMMENT '开始位置',
  `stop_pos` varchar(20) DEFAULT NULL COMMENT '结束位置',
  `run_time` varchar(20) DEFAULT NULL COMMENT '运行时间',
  `failure_times` int(11) DEFAULT '0' COMMENT '失败次数',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=701 DEFAULT CHARSET=utf8;

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

/*Table structure for table `t_sys_settings` */

DROP TABLE IF EXISTS `t_sys_settings`;

CREATE TABLE `t_sys_settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(100) DEFAULT NULL,
  `value` varchar(200) DEFAULT NULL,
  `desc` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=157 DEFAULT CHARSET=utf8;

/*Table structure for table `t_user_proj_privs` */

DROP TABLE IF EXISTS `t_user_proj_privs`;

CREATE TABLE `t_user_proj_privs` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `proj_id` int(11) DEFAULT NULL COMMENT '项目ID',
  `user_id` int(11) DEFAULT NULL COMMENT '用户ID',
  `priv_id` int(11) DEFAULT NULL COMMENT '权限ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6532 DEFAULT CHARSET=utf8;

/*Table structure for table `t_user_role` */

DROP TABLE IF EXISTS `t_user_role`;

CREATE TABLE `t_user_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `role_id` int(11) NOT NULL COMMENT '角色ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=523 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

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

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
