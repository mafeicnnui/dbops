CREATE TABLE `t_func` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `func_name` varchar(100) DEFAULT NULL COMMENT '功能名称',
  `func_url` varchar(300) DEFAULT NULL COMMENT '功能URL',
  `priv_id` varchar(100) DEFAULT NULL COMMENT '权限ID',
  `status` varchar(1) DEFAULT NULL COMMENT '状态',
  `creation_date` date DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(20) DEFAULT NULL COMMENT '创建人',
  `last_update_date` date DEFAULT NULL COMMENT '最近更新时间',
  `updator` varchar(20) DEFAULT NULL COMMENT '更新人',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=216 DEFAULT CHARSET=utf8;