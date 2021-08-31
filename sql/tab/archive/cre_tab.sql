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
) ENGINE=InnoDB AUTO_INCREMENT=594 DEFAULT CHARSET=utf8;