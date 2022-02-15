/*
SQLyog Ultimate v11.24 (64 bit)
MySQL - 5.6.44-log : Database - puppet
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`puppet` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `puppet`;

/* Procedure structure for procedure `proc_clear_log` */

/*!50003 DROP PROCEDURE IF EXISTS  `proc_clear_log` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`puppet`@`%` PROCEDURE `proc_clear_log`()
BEGIN
	DELETE FROM t_monitor_task_db_log
	  WHERE create_date <DATE_ADD(CONCAT(DATE_FORMAT(NOW(),'%Y-%m-%d'),' 0:0:0'),INTERVAL -7 DAY);
	DELETE FROM t_monitor_task_server_log
	  WHERE create_date <DATE_ADD(CONCAT(DATE_FORMAT(NOW(),'%Y-%m-%d'),' 0:0:0'),INTERVAL -7 DAY);
	DELETE FROM t_db_sync_tasks_log
	  WHERE create_date <DATE_ADD(CONCAT(DATE_FORMAT(NOW(),'%Y-%m-%d'),' 0:0:0'),INTERVAL -7 DAY);
	DELETE FROM  t_db_sync_tasks_log_detail
	  WHERE create_date <DATE_ADD(CONCAT(DATE_FORMAT(NOW(),'%Y-%m-%d'),' 0:0:0'),INTERVAL -7 DAY);
	DELETE FROM t_datax_sync_log
	  WHERE create_date <DATE_ADD(CONCAT(DATE_FORMAT(NOW(),'%Y-%m-%d'),' 0:0:0'),INTERVAL -7 DAY);
	DELETE FROM t_db_backup_total
	  WHERE create_date <DATE_ADD(CONCAT(DATE_FORMAT(NOW(),'%Y-%m-%d'),' 0:0:0'),INTERVAL -7 DAY);
	DELETE FROM `t_db_backup_detail`
	  WHERE create_date <DATE_ADD(CONCAT(DATE_FORMAT(NOW(),'%Y-%m-%d'),' 0:0:0'),INTERVAL -7 DAY);
        DELETE FROM `t_slow_detail`
	  WHERE finish_time <DATE_ADD(CONCAT(DATE_FORMAT(NOW(),'%Y-%m-%d'),' 0:0:0'),INTERVAL -7 DAY);
END */$$
DELIMITER ;

/* Procedure structure for procedure `proc_tj_service` */

/*!50003 DROP PROCEDURE IF EXISTS  `proc_tj_service` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`puppet`@`%` PROCEDURE `proc_tj_service`()
BEGIN
  DECLARE n_server_id    INT;
  DECLARE v_server_desc  VARCHAR(100);
  DECLARE v_db_desc      VARCHAR(100);
  DECLARE v_db_type      VARCHAR(100);
  DECLARE n_db_available INT;
  DECLARE d_create_date  DATETIME;
  DECLARE n_mysql_proj   INT;
  DECLARE n_mssql_flow   INT;
  DECLARE n_mssql_park   INT;
  DECLARE n_mssql_car    INT;
  DECLARE n_mssql_dldf   INT;
  DECLARE n_mssql_sg     INT;
  DECLARE n_oracle_sg    INT;
  DECLARE n_elastic      INT;
  DECLARE n_redis        INT;
  DECLARE n_mongo        INT;
  DECLARE v_mysql_proj   VARCHAR(1000);
  DECLARE v_mssql_flow   VARCHAR(1000);
  DECLARE v_mssql_park   VARCHAR(1000);
  DECLARE v_mssql_car    VARCHAR(1000);
  DECLARE v_mssql_dldf   VARCHAR(1000);
  DECLARE v_mssql_sg     VARCHAR(1000);
  DECLARE v_oracle_sg    VARCHAR(1000);
  DECLARE v_elastic      VARCHAR(1000);
  DECLARE v_redis        VARCHAR(1000);
  DECLARE v_mongo        VARCHAR(1000);
  DECLARE _outer INT DEFAULT 0;
  DECLARE _inner INT DEFAULT 0;
  DECLARE cur_server  CURSOR FOR SELECT id,server_desc FROM `t_server` WHERE STATUS='1' ORDER BY id;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET _outer = 1;
  SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
  START TRANSACTION;
  DELETE FROM t_monitor_service;
  OPEN cur_server;
  out_loop:LOOP
     FETCH NEXT FROM cur_server INTO n_server_id,v_server_desc;
     IF _outer = 1 THEN
	LEAVE out_loop;
     END IF;
     SELECT
        COUNT(0),MAX(create_date)  INTO n_mysql_proj,d_create_date
     FROM t_monitor_task_db_log a
        LEFT JOIN t_server b ON a.server_id=b.id
        LEFT JOIN t_db_source c ON a.db_id=c.id
     WHERE (a.db_id,a.create_date) IN(
            SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
       AND b.id=n_server_id
       AND c.db_type='0';
     IF n_mysql_proj >0 THEN
	SELECT
	      GROUP_CONCAT(CONCAT(a.db_available,'@',c.id,'@',a.`create_date`))  INTO v_mysql_proj
	FROM t_monitor_task_db_log a
	   LEFT JOIN t_server b ON a.server_id=b.id
	   LEFT JOIN t_db_source c ON a.db_id=c.id
	WHERE (a.db_id,a.create_date) IN(
	       SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
	  AND b.id=n_server_id
	  AND c.db_type='0' ;
     ELSE
          SET v_mysql_proj = '';
     END IF;
     SELECT
        COUNT(0) INTO n_mssql_flow
     FROM t_monitor_task_db_log a
        LEFT JOIN t_server b ON a.server_id=b.id
        LEFT JOIN t_db_source c ON a.db_id=c.id
     WHERE (a.db_id,a.create_date) IN(
            SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
       AND b.id=n_server_id
       AND c.db_type='2'
       AND INSTR(c.db_desc,'客流')>0;
     IF n_mssql_flow >0 THEN
	SELECT
	      GROUP_CONCAT(CONCAT(a.db_available,'@',c.id,'@',a.`create_date`))   INTO v_mssql_flow
	FROM t_monitor_task_db_log a
	   LEFT JOIN t_server b ON a.server_id=b.id
	   LEFT JOIN t_db_source c ON a.db_id=c.id
	WHERE (a.db_id,a.create_date) IN(
	       SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
	  AND b.id=n_server_id
	  AND c.db_type='2'
	  AND INSTR(c.db_desc,'客流')>0;
     ELSE
          SET v_mssql_flow = '';
     END IF;
     SELECT
        COUNT(0) INTO n_mssql_park
     FROM t_monitor_task_db_log a
        LEFT JOIN t_server b ON a.server_id=b.id
        LEFT JOIN t_db_source c ON a.db_id=c.id
     WHERE (a.db_id,a.create_date) IN(
            SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
       AND b.id=n_server_id
       AND c.db_type='2'
       AND INSTR(c.db_desc,'车流')>0;
     IF n_mssql_park >0 THEN
	SELECT
	      GROUP_CONCAT(CONCAT(a.db_available,'@',c.id,'@',a.`create_date`))   INTO v_mssql_park
	FROM t_monitor_task_db_log a
	   LEFT JOIN t_server b ON a.server_id=b.id
	   LEFT JOIN t_db_source c ON a.db_id=c.id
	WHERE (a.db_id,a.create_date) IN(
	       SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
	  AND b.id=n_server_id
	  AND c.db_type='2'
	  AND INSTR(c.db_desc,'车流')>0;
     ELSE
          SET v_mssql_park = '';
     END IF;
     SELECT
        COUNT(0) INTO n_mssql_car
     FROM t_monitor_task_db_log a
        LEFT JOIN t_server b ON a.server_id=b.id
        LEFT JOIN t_db_source c ON a.db_id=c.id
     WHERE (a.db_id,a.create_date) IN(
            SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
       AND b.id=n_server_id
       AND c.db_type='2'
       AND INSTR(c.db_desc,'寻车')>0;
     IF n_mssql_car >0 THEN
	SELECT
	      GROUP_CONCAT(CONCAT(a.db_available,'@',c.id,'@',a.`create_date`))   INTO v_mssql_car
	FROM t_monitor_task_db_log a
	   LEFT JOIN t_server b ON a.server_id=b.id
	   LEFT JOIN t_db_source c ON a.db_id=c.id
	WHERE (a.db_id,a.create_date) IN(
	       SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
	  AND b.id=n_server_id
	  AND c.db_type='2'
	  AND INSTR(c.db_desc,'寻车')>0;
     ELSE
          SET v_mssql_car = '';
     END IF;
     SELECT
        COUNT(0) INTO n_mssql_dldf
     FROM t_monitor_task_db_log a
        LEFT JOIN t_server b ON a.server_id=b.id
        LEFT JOIN t_db_source c ON a.db_id=c.id
     WHERE (a.db_id,a.create_date) IN(
            SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
       AND b.id=n_server_id
       AND c.db_type='2'
       AND INSTR(c.db_desc,'德利多富')>0;
     IF n_mssql_dldf >0 THEN
	SELECT
	      GROUP_CONCAT(CONCAT(a.db_available,'@',c.id,'@',a.`create_date`))   INTO v_mssql_dldf
	FROM t_monitor_task_db_log a
	   LEFT JOIN t_server b ON a.server_id=b.id
	   LEFT JOIN t_db_source c ON a.db_id=c.id
	WHERE (a.db_id,a.create_date) IN(
	       SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
	  AND b.id=n_server_id
	  AND c.db_type='2'
	  AND INSTR(c.db_desc,'德利多富')>0;
     ELSE
          SET v_mssql_dldf = '';
     END IF;
     SELECT
        COUNT(0) INTO n_mssql_sg
     FROM t_monitor_task_db_log a
        LEFT JOIN t_server b ON a.server_id=b.id
        LEFT JOIN t_db_source c ON a.db_id=c.id
     WHERE (a.db_id,a.create_date) IN(
            SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
       AND b.id=n_server_id
       AND c.db_type='2'
       AND INSTR(c.db_desc,'商管')>0;
     IF n_mssql_sg >0 THEN
	SELECT
	      GROUP_CONCAT(CONCAT(a.db_available,'@',c.id,'@',a.`create_date`))   INTO v_mssql_sg
	FROM t_monitor_task_db_log a
	   LEFT JOIN t_server b ON a.server_id=b.id
	   LEFT JOIN t_db_source c ON a.db_id=c.id
	WHERE (a.db_id,a.create_date) IN(
	       SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
	  AND b.id=n_server_id
	  AND c.db_type='2'
	  AND INSTR(c.db_desc,'商管')>0;
     ELSE
          SET v_mssql_sg = '';
     END IF;
     SELECT
        COUNT(0) INTO n_oracle_sg
     FROM t_monitor_task_db_log a
        LEFT JOIN t_server b ON a.server_id=b.id
        LEFT JOIN t_db_source c ON a.db_id=c.id
     WHERE (a.db_id,a.create_date) IN(
            SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
       AND b.id=n_server_id
       AND c.db_type='1'
       AND INSTR(c.db_desc,'商管')>0;
     IF n_oracle_sg >0 THEN
	SELECT
	      GROUP_CONCAT(CONCAT(a.db_available,'@',c.id,'@',a.`create_date`))   INTO v_oracle_sg
	FROM t_monitor_task_db_log a
	   LEFT JOIN t_server b ON a.server_id=b.id
	   LEFT JOIN t_db_source c ON a.db_id=c.id
	WHERE (a.db_id,a.create_date) IN(
	       SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
	  AND b.id=n_server_id
	  AND c.db_type='1'
	  AND INSTR(c.db_desc,'商管')>0;
     ELSE
          SET v_oracle_sg = '';
     END IF;
     SELECT
        COUNT(0) INTO n_elastic
     FROM t_monitor_task_db_log a
        LEFT JOIN t_server b ON a.server_id=b.id
        LEFT JOIN t_db_source c ON a.db_id=c.id
     WHERE (a.db_id,a.create_date) IN(
            SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
       AND b.id=n_server_id
       AND c.db_type='4' ;
     IF n_elastic >0 THEN
	SELECT
	     GROUP_CONCAT(CONCAT(a.db_available,'@',c.id,'@',a.`create_date`))   INTO v_elastic
	FROM t_monitor_task_db_log a
	   LEFT JOIN t_server b ON a.server_id=b.id
	   LEFT JOIN t_db_source c ON a.db_id=c.id
	WHERE (a.db_id,a.create_date) IN(
	       SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
	  AND b.id=n_server_id
	  AND c.db_type='4';
     ELSE
          SET v_elastic = '';
     END IF;
     SELECT
        COUNT(0) INTO n_redis
     FROM t_monitor_task_db_log a
        LEFT JOIN t_server b ON a.server_id=b.id
        LEFT JOIN t_db_source c ON a.db_id=c.id
     WHERE (a.db_id,a.create_date) IN(
            SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
       AND b.id=n_server_id
       AND c.db_type='5' ;
     IF n_redis >0 THEN
	SELECT
	      GROUP_CONCAT(CONCAT(a.db_available,'@',c.id,'@',a.`create_date`))   INTO v_redis
	FROM t_monitor_task_db_log a
	   LEFT JOIN t_server b ON a.server_id=b.id
	   LEFT JOIN t_db_source c ON a.db_id=c.id
	WHERE (a.db_id,a.create_date) IN(
	       SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
	  AND b.id=n_server_id
	  AND c.db_type='5' ;
     ELSE
          SET v_redis = '';
     END IF;
     SELECT
        COUNT(0) INTO n_mongo
     FROM t_monitor_task_db_log a
        LEFT JOIN t_server b ON a.server_id=b.id
        LEFT JOIN t_db_source c ON a.db_id=c.id
     WHERE (a.db_id,a.create_date) IN(
            SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
       AND b.id=n_server_id
       AND c.db_type='6' ;
     IF n_mongo >0 THEN
	SELECT
	      GROUP_CONCAT(CONCAT(a.db_available,'@',c.id,'@',a.`create_date`))   INTO v_mongo
	FROM t_monitor_task_db_log a
	   LEFT JOIN t_server b ON a.server_id=b.id
	   LEFT JOIN t_db_source c ON a.db_id=c.id
	WHERE (a.db_id,a.create_date) IN(
	       SELECT db_id,MAX(create_date) FROM `t_monitor_task_db_log` GROUP BY db_id )
	  AND b.id=n_server_id
	  AND c.db_type='6' ;
     ELSE
          SET v_mongo = '';
     END IF;
     IF INSTR(v_mysql_proj,'0@')>0 OR INSTR(v_mssql_flow,'0@')>0 OR INSTR(v_mssql_park,'0@')>0
        OR INSTR(v_mssql_car,'0@')>0  OR INSTR(v_mssql_dldf,'0@')>0 OR INSTR(v_mssql_sg,'0@')>0 OR INSTR(v_oracle_sg,'0@')>0
           OR INSTR(v_elastic,'0@')>0  OR INSTR(v_redis,'0@')>0 OR INSTR(v_mongo,'0@')>0 THEN
	INSERT INTO t_monitor_service(server_id,server_desc,mysql_proj,mssql_flow,mssql_park,mssql_car,mssql_dldf,mssql_sg,oracle_sg,redis,mongo,es,create_date,sxh)
          VALUES(n_server_id,v_server_desc,v_mysql_proj,v_mssql_flow,v_mssql_park,v_mssql_car,v_mssql_dldf,v_mssql_sg,v_oracle_sg,v_redis,v_mongo,v_elastic, NOW(),-UNIX_TIMESTAMP());
     ELSE
        INSERT INTO t_monitor_service(server_id,server_desc,mysql_proj,mssql_flow,mssql_park,mssql_car,mssql_dldf,mssql_sg,oracle_sg,redis,mongo,es,create_date,sxh)
          VALUES(n_server_id,v_server_desc,v_mysql_proj,v_mssql_flow,v_mssql_park,v_mssql_car,v_mssql_dldf,v_mssql_sg,v_oracle_sg,v_redis,v_mongo,v_elastic,NOW(),UNIX_TIMESTAMP());
     END IF;
  END LOOP;
  COMMIT;
END */$$
DELIMITER ;

/* Procedure structure for procedure `proc_tj_sync_monitor` */

/*!50003 DROP PROCEDURE IF EXISTS  `proc_tj_sync_monitor` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`puppet`@`%` PROCEDURE `proc_tj_sync_monitor`()
BEGIN
  DECLARE v_market_id         VARCHAR(10);
  DECLARE v_market_name       VARCHAR(100);
  DECLARE v_flow_flag         VARCHAR(1000);
  DECLARE v_flow_real_flag    VARCHAR(1000);
  DECLARE v_flow_device_flag  VARCHAR(1000);
  DECLARE v_park_flag         VARCHAR(1000);
  DECLARE v_park_real_flag    VARCHAR(1000);
  DECLARE v_sales_dldf_flag   VARCHAR(1000);
  DECLARE _outer              INT DEFAULT 0;
  DECLARE _inner              INT DEFAULT 0;
  DECLARE cur_market          CURSOR FOR SELECT dmm,dmmc FROM `t_dmmx` WHERE dm='05' AND flag='1' ORDER BY dmm;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET _outer = 1;
  SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
  START TRANSACTION;
  DELETE FROM t_db_sync_monitor;
  OPEN cur_market;
  out_loop:LOOP
     FETCH NEXT FROM cur_market INTO v_market_id,v_market_name;
     IF _outer = 1 THEN
	LEAVE out_loop;
     END IF;
     SET v_flow_flag='';
     SELECT
	   IFNULL(GROUP_CONCAT(flag,'@',sync_tag,'@',create_date),'') INTO v_flow_flag
     FROM ( SELECT
	       CASE WHEN TIMESTAMPDIFF(HOUR, MAX(create_date), NOW())>6 THEN 1 ELSE 0 END flag,
	       sync_tag,
	       MAX(create_date) AS create_date
	     FROM t_db_sync_tasks_log l
	     WHERE l.sync_tag IN(
			SELECT sync_tag FROM `t_db_sync_config`
			  WHERE INSTR(sync_col_val,v_market_id)>0
			   AND STATUS='1' AND sync_ywlx='1' )
		 GROUP BY sync_tag
		 ORDER BY CASE WHEN INSTR(sync_tag,'proj')>0 THEN 1
		       WHEN INSTR(sync_tag,'stage')>0 THEN 2
		       WHEN INSTR(sync_tag,'bi')>0 THEN 3
		       ELSE 4 END
		 ) X;
     SET v_flow_real_flag='';
     SELECT
	   IFNULL(GROUP_CONCAT(flag,'@',sync_tag,'@',create_date),'') INTO v_flow_real_flag
     FROM ( SELECT
	       CASE WHEN TIMESTAMPDIFF(HOUR, MAX(create_date), NOW())>3 THEN 1 ELSE 0 END flag,
	       sync_tag,
	       MAX(create_date) AS create_date
	     FROM t_db_sync_tasks_log l
	      WHERE l.sync_tag IN(
			SELECT sync_tag FROM `t_db_sync_config`
			  WHERE INSTR(sync_col_val,v_market_id)>0
			   AND STATUS='1' AND sync_ywlx='2' )
		 GROUP BY sync_tag
		 ORDER BY CASE WHEN INSTR(sync_tag,'proj')>0 THEN 1
		       WHEN INSTR(sync_tag,'stage')>0 THEN 2
		       WHEN INSTR(sync_tag,'bi')>0 THEN 3
		       ELSE 4 END
		 ) X;
     SET v_flow_device_flag='';
     SELECT
	  IFNULL(GROUP_CONCAT(flag,'@',sync_tag,'@',create_date),'') INTO v_flow_device_flag
     FROM ( SELECT
	       CASE WHEN TIMESTAMPDIFF(MINUTE, MAX(create_date), NOW())>30 THEN 1 ELSE 0 END flag,
	       sync_tag,
	       MAX(create_date) AS create_date
	     FROM t_db_sync_tasks_log l
	     WHERE l.sync_tag IN(
			SELECT sync_tag FROM `t_db_sync_config`
			  WHERE INSTR(sync_col_val,v_market_id)>0
			   AND STATUS='1' AND sync_ywlx='5' )
		 GROUP BY sync_tag
		 ORDER BY CASE WHEN INSTR(sync_tag,'proj')>0 THEN 1
		       WHEN INSTR(sync_tag,'stage')>0 THEN 2
		       WHEN INSTR(sync_tag,'bi')>0 THEN 3
		       ELSE 4 END
		 ) X;
     SET v_park_flag='';
     SELECT
	   IFNULL(GROUP_CONCAT(flag,'@',sync_tag,'@',create_date),'') INTO v_park_flag
     FROM ( SELECT
	       CASE WHEN TIMESTAMPDIFF(HOUR, MAX(create_date), NOW())>6 THEN 1
		    WHEN TIMESTAMPDIFF(HOUR, MAX(create_date), NOW())<=6 AND MAX(amount) = 0 THEN 1
	       ELSE 0 END flag,
	       sync_tag,
	       MAX(create_date) AS create_date
	     FROM t_db_sync_tasks_log l
	     WHERE  l.sync_tag IN(
			SELECT sync_tag FROM `t_db_sync_config`
			  WHERE INSTR(sync_col_val,v_market_id)>0
			   AND STATUS='1' AND sync_ywlx='3' )
		 GROUP BY sync_tag
		 ORDER BY CASE WHEN INSTR(sync_tag,'proj')>0 THEN 1
		       WHEN INSTR(sync_tag,'stage')>0 THEN 2
		       WHEN INSTR(sync_tag,'bi')>0 THEN 3
		       ELSE 4 END
		 ) X;
     SET v_park_real_flag='';
     SELECT
	   IFNULL(GROUP_CONCAT(flag,'@',sync_tag,'@',create_date),'') INTO v_park_real_flag
     FROM ( SELECT
	       CASE WHEN TIMESTAMPDIFF(HOUR, MAX(create_date), NOW())>3 THEN 1
		    WHEN TIMESTAMPDIFF(HOUR, MAX(create_date), NOW())<=3 AND MAX(amount) = 0 THEN 1
	       ELSE 0 END flag,
	       sync_tag,
	       MAX(create_date) AS create_date
	     FROM t_db_sync_tasks_log l
	     WHERE  l.sync_tag IN(
			SELECT sync_tag FROM `t_db_sync_config`
			  WHERE INSTR(sync_col_val,v_market_id)>0
			   AND STATUS='1' AND sync_ywlx='4' )
		 GROUP BY sync_tag
		 ORDER BY CASE WHEN INSTR(sync_tag,'proj')>0 THEN 1
		       WHEN INSTR(sync_tag,'stage')>0 THEN 2
		       WHEN INSTR(sync_tag,'bi')>0 THEN 3
		       ELSE 4 END
		 ) X;
     SET v_sales_dldf_flag='';
     SELECT
	   IFNULL(GROUP_CONCAT(flag,'@',sync_tag,'@',create_date),'') INTO v_sales_dldf_flag
     FROM ( SELECT
	       CASE WHEN TIMESTAMPDIFF(HOUR, MAX(create_date), NOW())>3 THEN 1 ELSE 0 END flag,
	       sync_tag,
	       MAX(create_date) AS create_date
	     FROM t_db_sync_tasks_log l
	     WHERE l.sync_tag IN(
			SELECT sync_tag FROM `t_db_sync_config`
			  WHERE INSTR(sync_col_val,v_market_id)>0
			   AND STATUS='1' AND sync_ywlx='8' )
		 GROUP BY sync_tag
		 ORDER BY CASE WHEN INSTR(sync_tag,'proj')>0 THEN 1
		       WHEN INSTR(sync_tag,'stage')>0 THEN 2
		       WHEN INSTR(sync_tag,'bi')>0 THEN 3
		       ELSE 4 END
		 ) X;
      INSERT INTO t_db_sync_monitor(market_id,market_name,flow_flag,flow_real_flag,flow_device_flag,park_flag,park_real_flag,sales_dldf_flag,create_date)
          VALUES(v_market_id,v_market_name,v_flow_flag,v_flow_real_flag,v_flow_device_flag,v_park_flag,v_park_real_flag,v_sales_dldf_flag,NOW());
  END LOOP;
  COMMIT;
END */$$
DELIMITER ;

/* Procedure structure for procedure `proc_truncate_log` */

/*!50003 DROP PROCEDURE IF EXISTS  `proc_truncate_log` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`puppet`@`%` PROCEDURE `proc_truncate_log`()
BEGIN
	TRUNCATE TABLE `t_db_sync_tasks_log`;
	TRUNCATE TABLE `t_db_sync_tasks_log_detail`;
	TRUNCATE TABLE `t_monitor_task_db_log`;
	TRUNCATE TABLE `t_monitor_task_server_log`;
	TRUNCATE TABLE `t_slow_detail`;
	-- TRUNCATE TABLE `t_db_sync_real_log`;
	 
END */$$
DELIMITER ;

/* Procedure structure for procedure `proc_trunc_log` */

/*!50003 DROP PROCEDURE IF EXISTS  `proc_trunc_log` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`puppet`@`%` PROCEDURE `proc_trunc_log`()
BEGIN
	TRUNCATE TABLE `t_db_sync_tasks_log`;
	TRUNCATE TABLE `t_db_sync_tasks_log_detail`;
	TRUNCATE TABLE `t_monitor_task_db_log`;
	TRUNCATE TABLE `t_monitor_task_server_log`;
	TRUNCATE TABLE `t_slow_detail`;
	 
END */$$
DELIMITER ;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
