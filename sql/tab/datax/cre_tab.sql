CREATE TABLE `t_datax_sync_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sync_tag` varchar(100) DEFAULT NULL COMMENT '同步标识',
  `server_id` int(11) DEFAULT NULL COMMENT '同步服务器ID',
  `sour_db_id` int(11) DEFAULT NULL COMMENT '源数据库ID',
  `sync_schema` varchar(100) DEFAULT NULL COMMENT '同步数据库',
  `sync_table` varchar(2000) DEFAULT NULL COMMENT '同步表',
  `sync_columns` varchar(2000) DEFAULT NULL COMMENT '同步列名列表',
  `sync_incr_col` varchar(50) DEFAULT NULL COMMENT '增量同步列名',
  `sync_incr_where` varchar(1000) DEFAULT NULL COMMENT '增量同步条件',
  `zk_hosts` varchar(100) DEFAULT NULL COMMENT 'zookeeper地址',
  `hbase_thrift` varchar(100) DEFAULT NULL COMMENT 'hbase_thrift接口地址',
  `sync_hbase_table` varchar(100) DEFAULT NULL COMMENT 'hbase同步表名',
  `sync_hbase_rowkey` text COMMENT 'hbase行键名称',
  `sync_hbase_rowkey_sour` varchar(50) DEFAULT NULL COMMENT 'hbase行键原始字符串',
  `sync_hbase_columns` text COMMENT 'hbase同步列',
  `sync_hbase_rowkey_separator` varchar(10) DEFAULT NULL COMMENT 'hbase行键分隔符',
  `es_service` varchar(50) DEFAULT NULL COMMENT 'es服务地址',
  `es_index_name` varchar(100) DEFAULT NULL COMMENT 'es索引名称',
  `es_type_name` varchar(100) DEFAULT NULL COMMENT 'es类型名称',
  `sync_es_columns` text COMMENT 'es同步列名列表',
  `sync_ywlx` varchar(11) DEFAULT NULL COMMENT '同步业务类型',
  `sync_type` varchar(50) DEFAULT NULL COMMENT '同步类型',
  `python3_home` varchar(200) DEFAULT NULL COMMENT 'python3目录',
  `script_path` varchar(200) DEFAULT NULL COMMENT '同步客户端脚本',
  `run_time` varchar(100) DEFAULT NULL COMMENT '运行时间',
  `comments` varchar(100) DEFAULT NULL COMMENT '任务描述',
  `datax_home` varchar(200) DEFAULT NULL COMMENT 'datax工具目录',
  `sync_time_type` varchar(50) DEFAULT NULL COMMENT '同步时间类型',
  `sync_gap` int(11) DEFAULT NULL COMMENT '同步间隔',
  `api_server` varchar(100) DEFAULT NULL COMMENT 'api服务地址',
  `status` varchar(1) DEFAULT NULL COMMENT '任务状态',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_t_datax_config_u1` (`sync_tag`),
  KEY `idx_t_datax_sync_config_u1` (`sync_tag`)
) ENGINE=InnoDB AUTO_INCREMENT=150 DEFAULT CHARSET=utf8;

CREATE TABLE `t_datax_sync_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `sync_tag` varchar(100) NOT NULL COMMENT '同步标识',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `table_name` varchar(100) DEFAULT NULL COMMENT '表名称',
  `duration` int(11) DEFAULT NULL COMMENT '同步时长',
  `amount` int(11) DEFAULT NULL COMMENT '同步数量',
  PRIMARY KEY (`id`),
  KEY `idx_create_date_n1` (`create_date`),
  KEY `idx_create_date_u1` (`sync_tag`),
  KEY `idx_sync_tag_create_date` (`sync_tag`,`create_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `t_templete` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `templete_id` int(11) DEFAULT NULL COMMENT '模板ID',
  `contents` text COMMENT '模板内容',
  `description` varchar(100) DEFAULT NULL COMMENT '模板描述',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;