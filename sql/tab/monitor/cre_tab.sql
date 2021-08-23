


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

CREATE TABLE `t_monitor_project_err` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `market_id` varchar(20) DEFAULT NULL,
  `link_status` varchar(20) DEFAULT NULL,
  `error_times` int(11) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8;

CREATE TABLE `t_monitor_project_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `market_id` int(11) DEFAULT NULL,
  `ip_dx_status` varchar(10) DEFAULT NULL,
  `ip_lt_status` varchar(10) DEFAULT NULL,
  `link_status` varchar(10) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5257080 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=50832033 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=340 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=638886 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=427695 DEFAULT CHARSET=utf8;

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