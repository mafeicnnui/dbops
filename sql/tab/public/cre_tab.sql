CREATE TABLE `t_dmlx` (
  `dm` varchar(10) NOT NULL COMMENT '大类代码',
  `mc` varchar(100) DEFAULT NULL COMMENT '大类名称',
  `flag` varchar(1) DEFAULT NULL COMMENT '大类状态',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`dm`),
  KEY `idx_t_dmlx` (`dm`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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

CREATE TABLE `t_sys_settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(100) DEFAULT NULL,
  `value` varchar(200) DEFAULT NULL,
  `desc` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

CREATE TABLE `t_sys_stats_idx` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `idx_name` varchar(50) DEFAULT NULL COMMENT '指标名',
  `idx_sql` varchar(2000) DEFAULT NULL COMMENT '指标SQL',
  PRIMARY KEY (`id`),
  KEY `idx_t_sys_stats_idx_u1` (`idx_name`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8 COMMENT='指标统计表';