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
  `status` varchar(1) DEFAULT NULL COMMENT '同步状态',
  `task_status` varchar(1) DEFAULT '0' COMMENT '任务状态',
  `task_create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_t_db_config_u1` (`sync_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=459 DEFAULT CHARSET=utf8 COMMENT='数据库同步配置表';

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
) ENGINE=InnoDB AUTO_INCREMENT=3473 DEFAULT CHARSET=utf8;

CREATE TABLE `t_db_sync_tasks_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `sync_tag` varchar(1000) NOT NULL COMMENT '同步标识',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `duration` int(11) DEFAULT NULL COMMENT '同步时长(s)',
  `amount` int(11) DEFAULT NULL COMMENT '同步数量',
  PRIMARY KEY (`id`),
  KEY `idx_create_date_n1` (`create_date`),
  KEY `idx_create_date_u1` (`sync_tag`),
  KEY `idx_sync_tag_create_date` (`sync_tag`,`create_date`)
) ENGINE=InnoDB AUTO_INCREMENT=212934 DEFAULT CHARSET=utf8;

CREATE TABLE `t_db_sync_tasks_log_detail` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `sync_tag` varchar(1000) NOT NULL COMMENT '同步标识',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `sync_table` varchar(1000) DEFAULT NULL COMMENT '同步表',
  `sync_amount` int(11) DEFAULT NULL COMMENT '同步数量',
  `duration` int(11) DEFAULT NULL COMMENT '同步时长(s)',
  PRIMARY KEY (`id`),
  KEY `idx_create_date_n1` (`create_date`),
  KEY `idx_create_date_u1` (`sync_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=1871592 DEFAULT CHARSET=utf8;