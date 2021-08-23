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
) ENGINE=InnoDB AUTO_INCREMENT=957996 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=40605 DEFAULT CHARSET=utf8;