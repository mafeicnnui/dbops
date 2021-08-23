CREATE TABLE `t_port` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `market_id` int(11) DEFAULT NULL COMMENT '项目ID',
  `market_name` varchar(100) DEFAULT NULL COMMENT '项目名称',
  `app_desc` varchar(100) DEFAULT NULL COMMENT '应用描述',
  `local_ip` varchar(20) DEFAULT NULL COMMENT '应用IP',
  `local_port` varchar(10) DEFAULT NULL COMMENT '应用PORT',
  `mapping_port` varchar(10) DEFAULT NULL COMMENT '映射PORT',
  `mapping_domain` varchar(50) DEFAULT NULL COMMENT '映射域名',
  `mapping_type` varchar(1) DEFAULT NULL COMMENT '映射类型',
  `creater` varchar(20) DEFAULT NULL COMMENT '创建人',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `update_date` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=161 DEFAULT CHARSET=utf8;