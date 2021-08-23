CREATE VIEW CREATE ALGORITHM = UNDEFINED DEFINER = `puppet` @`%` SQL SECURITY DEFINER VIEW `v_monitor_service` AS
SELECT 
  `t_monitor_service`.`server_id` AS `server_id`,
  `t_monitor_service`.`server_desc` AS `server_desc`,
  `t_monitor_service`.`mysql_proj` AS `service_service`,
  'mysql' AS `flag` 
FROM
  `t_monitor_service` 
WHERE (
    `t_monitor_service`.`mysql_proj` <> ''
  ) 
UNION
ALL 
SELECT 
  `t_monitor_service`.`server_id` AS `server_id`,
  `t_monitor_service`.`server_desc` AS `server_desc`,
  `t_monitor_service`.`mssql_park` AS `mssql_park`,
  'mssql_park' AS `flag` 
FROM
  `t_monitor_service` 
WHERE (
    `t_monitor_service`.`mssql_park` <> ''
  ) 
UNION
ALL 
SELECT 
  `t_monitor_service`.`server_id` AS `server_id`,
  `t_monitor_service`.`server_desc` AS `server_desc`,
  `t_monitor_service`.`mssql_flow` AS `mssql_flow`,
  'mssql_flow' AS `flag` 
FROM
  `t_monitor_service` 
WHERE (
    `t_monitor_service`.`mssql_flow` <> ''
  ) 
UNION
ALL 
SELECT 
  `t_monitor_service`.`server_id` AS `server_id`,
  `t_monitor_service`.`server_desc` AS `server_desc`,
  `t_monitor_service`.`mssql_car` AS `mssql_car`,
  'mssql_car' AS `flag` 
FROM
  `t_monitor_service` 
WHERE (
    `t_monitor_service`.`mssql_car` <> ''
  ) 
UNION
ALL 
SELECT 
  `t_monitor_service`.`server_id` AS `server_id`,
  `t_monitor_service`.`server_desc` AS `server_desc`,
  `t_monitor_service`.`redis` AS `redis`,
  'redis' AS `flag` 
FROM
  `t_monitor_service` 
WHERE (
    `t_monitor_service`.`redis` <> ''
  ) 
UNION
ALL 
SELECT 
  `t_monitor_service`.`server_id` AS `server_id`,
  `t_monitor_service`.`server_desc` AS `server_desc`,
  `t_monitor_service`.`mongo` AS `mongo`,
  'mongo' AS `flag` 
FROM
  `t_monitor_service` 
WHERE (
    `t_monitor_service`.`mongo` <> ''
  ) 
UNION
ALL 
SELECT 
  `t_monitor_service`.`server_id` AS `server_id`,
  `t_monitor_service`.`server_desc` AS `server_desc`,
  `t_monitor_service`.`es` AS `es`,
  'es' AS `flag` 
FROM
  `t_monitor_service` 
WHERE (`t_monitor_service`.`es` <> '') 
ORDER BY `server_id` 