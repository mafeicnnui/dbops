CREATE TABLE `t_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户ID(主键)',
  `name` varchar(20) DEFAULT NULL COMMENT '用户名称',
  `wkno` varchar(20) DEFAULT NULL COMMENT '员工编号',
  `gender` varchar(2) DEFAULT NULL COMMENT '性别',
  `email` varchar(40) DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机',
  `project_group` varchar(1) DEFAULT NULL COMMENT '项目组',
  `dept` varchar(20) DEFAULT NULL COMMENT '部门',
  `expire_date` date DEFAULT NULL COMMENT '过期时间',
  `password` varchar(200) DEFAULT NULL COMMENT '口令',
  `status` varchar(1) DEFAULT NULL COMMENT '状态',
  `creation_date` date DEFAULT NULL COMMENT '创建日期',
  `creator` varchar(20) DEFAULT NULL COMMENT '创建人',
  `last_update_date` date DEFAULT NULL COMMENT '更新时间',
  `updator` varchar(20) DEFAULT NULL COMMENT '更新人',
  `login_name` varchar(20) DEFAULT NULL COMMENT '登陆名',
  `file_path` varchar(200) DEFAULT NULL COMMENT '图标路径',
  `file_name` varchar(100) DEFAULT NULL COMMENT '图标名称',
  PRIMARY KEY (`id`),
  KEY `idx_login_name_n1` (`login_name`)
) ENGINE=InnoDB AUTO_INCREMENT=145 DEFAULT CHARSET=utf8;

CREATE TABLE `t_user_proj_privs` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `proj_id` int(11) DEFAULT NULL COMMENT '项目ID',
  `user_id` int(11) DEFAULT NULL COMMENT '用户ID',
  `priv_id` int(11) DEFAULT NULL COMMENT '权限ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4524 DEFAULT CHARSET=utf8;

CREATE TABLE `t_user_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `role_id` int(11) NOT NULL COMMENT '角色ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=318 DEFAULT CHARSET=utf8;

CREATE TABLE `t_forget_password` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` int(11) DEFAULT NULL COMMENT '用户ID',
  `authentication_string` varchar(100) DEFAULT NULL COMMENT '认证字符串',
  `creation_date` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(20) DEFAULT NULL COMMENT '创建人',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;
