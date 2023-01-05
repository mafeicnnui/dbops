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
ORDER BY `server_id` ;


CREATE  VIEW `v_kpi_bbtj` AS
SELECT
  `a`.`id`          AS `id`,
  `a`.`bbrq`        AS `bbrq`,
  `a`.`market_id`   AS `market_id`,
  `a`.`market_name` AS `market_name`,
  `a`.`item_name`   AS `item_name`,
  (SELECT
     `x`.`item_value`
   FROM `t_kpi_item_value` `x`
   WHERE ((`x`.`item_month` = CONVERT(SUBSTR(`a`.`bbrq`,1,7)USING utf8mb4))
          AND (`x`.`market_name` = `a`.`market_name`)
          AND (`x`.`item_name` = `a`.`item_name`))) AS `item_month_value`,
  `a`.`item_value`  AS `item_finish_value`,
  DATE_FORMAT(`a`.`create_time`,'%Y-%m-%d %H:%i:%s') AS `create_time`
FROM `t_kpi_bbtj` `a`
WHERE ((`a`.`item_name` IN('GMV（万）','会员销售占比','上线SPU数量（个）','POS GMV（万）','会员运营GMV（万）','商城+本地生活GMV（万）','数字账单GMV（万）','物业增值GMV（万）'))
       AND (`a`.`market_name` NOT IN('商管总部及合生通','直管区域','上海区域','广州区域','商业事业部')))
ORDER BY `a`.`id`;

CREATE VIEW `v_db_compare_idx` AS
SELECT
  `t_db_compare_idx`.`dsid`         AS `dsid`,
  `t_db_compare_idx`.`table_schema` AS `table_schema`,
  `t_db_compare_idx`.`table_name`   AS `table_name`,
  `t_db_compare_idx`.`index_name`   AS `index_name`,
  `t_db_compare_idx`.`index_type`   AS `index_type`,
  `t_db_compare_idx`.`is_unique`    AS `is_unique`,
  `t_db_compare_idx`.`nullable`     AS `nullable`,
  IFNULL(`t_db_compare_idx`.`visible`,'') AS `visible`,
  GROUP_CONCAT(`t_db_compare_idx`.`column_name` SEPARATOR ',') AS `column_name`
FROM `t_db_compare_idx`
GROUP BY `t_db_compare_idx`.`dsid`,`t_db_compare_idx`.`table_schema`,`t_db_compare_idx`.`table_name`,`t_db_compare_idx`.`index_name`,`t_db_compare_idx`.`index_type`,`t_db_compare_idx`.`is_unique`,`t_db_compare_idx`.`nullable`,`t_db_compare_idx`.`visible`;
