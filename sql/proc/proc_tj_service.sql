DELIMITER $$

USE `puppet`$$

DROP PROCEDURE IF EXISTS `proc_tj_service`$$

CREATE  PROCEDURE `proc_tj_service`()
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
END$$

DELIMITER ;
