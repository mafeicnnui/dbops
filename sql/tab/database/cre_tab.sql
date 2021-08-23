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
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8;

CREATE TABLE `t_db_inst_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `inst_id` int(11) DEFAULT NULL COMMENT '实例ID',
  `type` varchar(20) DEFAULT NULL COMMENT '日志类型',
  `message` varchar(1000) DEFAULT NULL COMMENT '日志消息',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7296 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=316 DEFAULT CHARSET=utf8;


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
) ENGINE=InnoDB AUTO_INCREMENT=5186 DEFAULT CHARSET=utf8;

CREATE TABLE `t_db_inst_step` (
  `id` int(11) NOT NULL COMMENT '主键',
  `cmd` varchar(2000) DEFAULT NULL COMMENT '操作命令',
  `message` varchar(200) DEFAULT NULL COMMENT '操作消息',
  `version` varchar(20) DEFAULT NULL COMMENT '版本',
  `flag` varchar(1) DEFAULT NULL COMMENT '操作类型',
  `desc` varchar(50) DEFAULT NULL COMMENT '操作描述',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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