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
) ENGINE=InnoDB AUTO_INCREMENT=6107 DEFAULT CHARSET=utf8;

CREATE TABLE `t_sql_backup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `release_id` bigint(20) DEFAULT NULL,
  `rollback_statement` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=206 DEFAULT CHARSET=utf8;

CREATE TABLE `t_sql_release` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `dbid` int(11) NOT NULL COMMENT '数据源ID',
  `db` varchar(50) DEFAULT NULL COMMENT '数据库名称',
  `sqltext` longtext COMMENT 'SQL文本',
  `status` varchar(1) DEFAULT NULL COMMENT '0:已发布,1:审核成功，2:审核失败,3:执行中,4:执行成功，5:执行失败,6:已驳回',
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
) ENGINE=InnoDB AUTO_INCREMENT=107 DEFAULT CHARSET=utf8;

CREATE TABLE `t_sql_release_results` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `release_id` int(11) DEFAULT NULL COMMENT '发送ID',
  `db_env` varchar(1) DEFAULT NULL COMMENT '数据库环境',
  `db_status` varchar(1) DEFAULT NULL COMMENT '数据库状态',
  `db_msg` varchar(100) DEFAULT NULL COMMENT '数据库消息',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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