DELIMITER $$

USE `puppet`$$

DROP PROCEDURE IF EXISTS `proc_tj_sync_monitor`$$

CREATE DEFINER=`puppet`@`%` PROCEDURE `proc_tj_sync_monitor`()
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
END$$

DELIMITER ;