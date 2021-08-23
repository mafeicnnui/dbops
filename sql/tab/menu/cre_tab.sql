CREATE TABLE `t_xtqx` (
  `id` varchar(10) NOT NULL DEFAULT '' COMMENT '权限ID(主键)',
  `name` varchar(20) DEFAULT NULL COMMENT '权限名称',
  `parent_id` varchar(10) DEFAULT NULL COMMENT '父权限ID',
  `url` varchar(100) DEFAULT NULL COMMENT '后端URL地址',
  `url_front` varchar(100) DEFAULT NULL COMMENT '前端访问地址',
  `status` varchar(1) DEFAULT NULL COMMENT '菜单状态',
  `icon` varchar(50) DEFAULT NULL COMMENT '菜单图标',
  `creation_date` date DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(20) DEFAULT NULL COMMENT '创建人',
  `last_update_date` date DEFAULT NULL COMMENT '更新时间',
  `updator` varchar(20) DEFAULT NULL COMMENT '更新人',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;