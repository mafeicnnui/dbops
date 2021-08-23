CREATE TABLE `t_db_weekly_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `item_type` varchar(20) DEFAULT NULL COMMENT '统计项目类型',
  `item_code` varchar(50) DEFAULT NULL COMMENT '项目代码',
  `item_desc` varchar(50) DEFAULT NULL COMMENT '项目描述',
  `item_tjsql` text COMMENT '统计语句',
  `status` varchar(1) DEFAULT NULL COMMENT '项目状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8;