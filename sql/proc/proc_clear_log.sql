DELIMITER $$

USE `puppet`$$

DROP PROCEDURE IF EXISTS `proc_clear_log`$$

CREATE DEFINER=`puppet`@`%` PROCEDURE `proc_clear_log`()
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


END$$

DELIMITER ;