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