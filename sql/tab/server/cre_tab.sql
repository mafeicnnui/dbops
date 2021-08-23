CREATE TABLE `t_server` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `market_id` varchar(20) NOT NULL,
  `server_type` varchar(100) DEFAULT NULL,
  `server_desc` varchar(100) DEFAULT NULL,
  `server_ip` varchar(100) NOT NULL,
  `server_port` varchar(10) NOT NULL,
  `server_user` varchar(20) NOT NULL,
  `server_pass` varchar(200) NOT NULL,
  `server_os` varchar(100) NOT NULL,
  `server_cpu` varchar(100) NOT NULL,
  `server_mem` varchar(100) NOT NULL,
  `status` varchar(20) NOT NULL,
  `flag1` varchar(100) DEFAULT NULL COMMENT '商管周报',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=163 DEFAULT CHARSET=utf8;