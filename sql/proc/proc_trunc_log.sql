DELIMITER $$

USE `puppet`$$

DROP PROCEDURE IF EXISTS `proc_trunc_log`$$

CREATE DEFINER=`puppet`@`%` PROCEDURE `proc_trunc_log`()
BEGIN
	TRUNCATE TABLE `t_db_sync_tasks_log`;
	TRUNCATE TABLE `t_db_sync_tasks_log_detail`;
	TRUNCATE TABLE `t_monitor_task_db_log`;
	TRUNCATE TABLE `t_monitor_task_server_log`;
	TRUNCATE TABLE `t_slow_detail`;
	TRUNCATE TABLE `t_slow_detail_mssql`;
	TRUNCATE TABLE `t_slow_detail_oracle`;
	TRUNCATE TABLE `t_db_sync_real_log`;

END$$

DELIMITER ;