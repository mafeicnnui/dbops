CREATE TABLE `kpi_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `kpi_tag` varchar(100) DEFAULT NULL COMMENT '传输标识',
  `server_id` int(11) DEFAULT NULL COMMENT '传输服务器ID',
  `month` varchar(20) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `comments` varchar(100) DEFAULT NULL COMMENT '任务描述',
  `script_path` varchar(200) DEFAULT NULL COMMENT '传输代理路径',
  `script_file` varchar(100) DEFAULT NULL COMMENT '传输代理文件名',
  `run_time` varchar(100) DEFAULT NULL COMMENT '运行时间',
  `python3_home` varchar(200) DEFAULT NULL COMMENT 'PYTHON3路径',
  `api_server` varchar(100) DEFAULT NULL COMMENT 'API服务器',
  `status` varchar(1) DEFAULT NULL COMMENT '任务状态',
  PRIMARY KEY (`id`),
  KEY `idx_t_db_kpi_config_u1` (`kpi_tag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `kpi_ds` (
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
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf8;

CREATE TABLE `kpi_item` (
  `code` varchar(10) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `if_stat` varchar(1) DEFAULT NULL COMMENT '是否统计',
  `type` varchar(1) DEFAULT NULL COMMENT '考核类型(1:当月,2:累计)',
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `kpi_item_plan` (
  `market_id` varchar(10) NOT NULL DEFAULT '',
  `market_name` varchar(100) DEFAULT NULL,
  `month` varchar(7) NOT NULL DEFAULT '',
  `item_code` varchar(20) NOT NULL DEFAULT '',
  `item_name` varchar(100) DEFAULT NULL,
  `item_value` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`market_id`,`month`,`item_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `kpi_item_plan_templete` (
  `market_id` varchar(10) NOT NULL DEFAULT '',
  `market_name` varchar(100) DEFAULT NULL,
  `month` varchar(7) NOT NULL DEFAULT '',
  `item_code` varchar(20) NOT NULL DEFAULT '',
  `item_name` varchar(100) DEFAULT NULL,
  `item_value` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`market_id`,`month`,`item_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `kpi_item_sql` (
  `item_code` varchar(10) NOT NULL,
  `item_name` varchar(100) DEFAULT NULL,
  `item_type` varchar(1) DEFAULT NULL COMMENT '批标大类(1:项目及区域,2:合生通)',
  `if_stat` varchar(1) DEFAULT NULL COMMENT '是否统计',
  `statement` text COMMENT '本月统计语句',
  `statement_sum` text COMMENT '累计统计语句',
  `ds_id` int(11) DEFAULT NULL COMMENT '数据源ID',
  `status` varchar(1) DEFAULT NULL COMMENT '是否统计(1:启用,1:禁用)',
  PRIMARY KEY (`item_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `kpi_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `month` varchar(100) DEFAULT NULL COMMENT '报表月',
  `bbrqq` varchar(20) DEFAULT NULL COMMENT '开始日期',
  `bbrqz` varchar(20) DEFAULT NULL COMMENT '结束日期',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `duration` int(11) DEFAULT NULL COMMENT '生成时长',
  `percent` varchar(20) DEFAULT NULL COMMENT '传输进度',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;


CREATE TABLE `kpi_log_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `month` varchar(7) DEFAULT NULL,
  `message` varchar(1000) DEFAULT NULL,
  `create_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23196 DEFAULT CHARSET=utf8;

CREATE TABLE `kpi_po` (
  `market_id` int(11) NOT NULL,
  `market_name` varchar(100) DEFAULT NULL,
  `summary_formula` varchar(100) DEFAULT NULL COMMENT '计算公式',
  `if_stat` varchar(3) DEFAULT NULL COMMENT '是否汇总',
  `sxh` int(11) DEFAULT NULL COMMENT '生成序号',
  PRIMARY KEY (`market_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `kpi_po_hz` (
  `bbrq` date DEFAULT NULL COMMENT '统计日期',
  `month` varchar(7) NOT NULL DEFAULT '' COMMENT '报表月',
  `market_id` int(20) NOT NULL COMMENT '项目编码',
  `market_name` varchar(100) DEFAULT NULL COMMENT '项目名称',
  `item_code` varchar(10) NOT NULL DEFAULT '' COMMENT '指标编码',
  `item_name` varchar(100) DEFAULT NULL COMMENT '指标名称',
  `goal` varchar(20) DEFAULT '' COMMENT '月度目标',
  `actual_completion` varchar(20) DEFAULT NULL COMMENT '月度完成',
  `completion_rate` varchar(20) DEFAULT '' COMMENT '月度完成率',
  `create_time` datetime DEFAULT NULL COMMENT '生成时间',
  `update_time` datetime DEFAULT NULL COMMENT '最后更新时间',
  `annual_target` varchar(20) DEFAULT '' COMMENT '年度指标',
  `completion_sum_finish` varchar(20) DEFAULT NULL COMMENT '年度完成',
  `completion_sum_rate` varchar(20) DEFAULT '' COMMENT '年度完成率',
  PRIMARY KEY (`market_id`,`month`,`item_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `kpi_po_mx` (
  `bbrq` date DEFAULT NULL COMMENT '统计日期',
  `month` varchar(7) NOT NULL DEFAULT '' COMMENT '报表月',
  `market_id` int(20) NOT NULL COMMENT '项目编码',
  `market_name` varchar(100) DEFAULT NULL COMMENT '项目名称',
  `item_code` varchar(10) NOT NULL DEFAULT '' COMMENT '指标代码',
  `item_name` varchar(100) DEFAULT NULL COMMENT '指标名称',
  `item_value` varchar(50) DEFAULT NULL COMMENT '月度指标值',
  `item_value_sum` varchar(50) DEFAULT NULL COMMENT '累计指标值(4月1-当月）',
  `create_time` datetime DEFAULT NULL COMMENT '生成时间',
  `update_time` datetime DEFAULT NULL COMMENT '最后更新时间',
  PRIMARY KEY (`market_id`,`month`,`item_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


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











