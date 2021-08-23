CREATE TABLE `t_role` (
  `id` int(11) NOT NULL COMMENT '主键',
  `name` varchar(20) DEFAULT NULL COMMENT '角色名称',
  `status` varchar(1) DEFAULT NULL COMMENT '角色状态',
  `creation_date` date DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(20) DEFAULT NULL COMMENT '创建人',
  `last_update_date` date DEFAULT NULL COMMENT '更新时间',
  `updator` varchar(20) DEFAULT NULL COMMENT '更新人',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `t_role_func_privs` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `role_id` varchar(100) DEFAULT NULL COMMENT '角色ID',
  `func_id` varchar(100) DEFAULT NULL COMMENT '功能ID',
  `creation_date` date DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(20) DEFAULT NULL COMMENT '创建人',
  `last_update_date` date DEFAULT NULL COMMENT '更新时间',
  `updator` varchar(20) DEFAULT NULL COMMENT '更新人',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23924 DEFAULT CHARSET=utf8;

CREATE TABLE `t_role_privs` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `role_id` int(11) NOT NULL COMMENT '角色ID',
  `priv_id` varchar(20) DEFAULT NULL COMMENT '权限ID',
  `creation_date` date DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(20) DEFAULT NULL COMMENT '创建人',
  `last_update_date` date DEFAULT NULL COMMENT '更新时间',
  `updator` varchar(20) DEFAULT NULL COMMENT '更新人',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3370 DEFAULT CHARSET=utf8