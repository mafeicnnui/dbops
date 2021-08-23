CREATE TABLE `t_minio_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `sync_tag` varchar(50) DEFAULT NULL COMMENT '同步标识',
  `sync_type` varchar(1) DEFAULT NULL COMMENT '同步类型',
  `server_id` int(11) DEFAULT NULL COMMENT '同步服务器ID',
  `sync_path` varchar(200) DEFAULT NULL COMMENT '同步路径',
  `sync_service` varchar(200) DEFAULT NULL COMMENT '同步服务名',
  `minio_server` varchar(200) DEFAULT NULL COMMENT 'minio服务名',
  `minio_user` varchar(100) DEFAULT NULL COMMENT 'minio用户',
  `minio_pass` varchar(100) DEFAULT NULL COMMENT 'minio口令',
  `minio_bucket` varchar(100) DEFAULT NULL COMMENT '同步批大小',
  `minio_dpath` varchar(100) DEFAULT NULL COMMENT 'minio下载路径',
  `minio_incr_type` varchar(10) DEFAULT NULL COMMENT '增量同步类型',
  `minio_incr` int(11) DEFAULT NULL COMMENT '增量同步时长',
  `python3_home` varchar(200) DEFAULT NULL COMMENT 'python3路径',
  `script_path` varchar(200) DEFAULT NULL COMMENT 'minio同步代理路径',
  `script_file` varchar(200) DEFAULT NULL COMMENT 'minio同步代理名称',
  `api_server` varchar(100) DEFAULT NULL COMMENT 'api服务地址',
  `run_time` varchar(100) DEFAULT NULL COMMENT '运行时间',
  `comments` varchar(100) DEFAULT NULL COMMENT '任务描述',
  `status` varchar(1) DEFAULT NULL COMMENT '任务状态',
  PRIMARY KEY (`id`),
  KEY `idx_t_minio_config_u1` (`sync_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;

CREATE TABLE `t_minio_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `sync_tag` varchar(50) DEFAULT NULL COMMENT '同步标识',
  `sync_day` int(11) DEFAULT NULL COMMENT '同步最近天数',
  `server_id` int(11) DEFAULT NULL COMMENT '同步服务器ID',
  `download_time` int(11) DEFAULT NULL COMMENT '下载时长',
  `upload_time` int(11) DEFAULT NULL COMMENT '上传时长',
  `total_time` int(11) DEFAULT NULL COMMENT '总时长',
  `transfer_file` int(11) DEFAULT NULL COMMENT '传输文件数',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=110808 DEFAULT CHARSET=utf8;