## 一、平台介绍  

   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Easebase平台是一款基于python3.6+tornado+bootstrap开发的数据库自动化运维平台，功能非常丰富，将DBA日常绝大多数工作都自动化管理，提升DBA工作效率
   
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;EaseBase数据库运维平台是为了提高DBA运维效率设计研发的，结合公司现状态将日常工作中重复性多的工作程序化，提高数据库运维效率，DBA可以更高效工作，同时为公司节省运营成本。 
平台将DBA工作中最常用的功能“数据库备份”、“数据库同步”、“数据库传输”、“数据库归档”、“大数据同步”、“数据源管理”、“服务器管理”、“数据库监控”、“工单管理”、数据库管理”、“数据库恢复”、 “数据库部署”、“慢查询管理”等功能。
另外，数据库同步、数据库传输以后会集成更多的功能，支持更丰富的数据源。该平台依赖dbapi平台接口服务，需要在部署后再部署dbapi服务 
   
## 二、平台架构

   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;平台由dbops WEB服务+dbapi接口服务+客户端（备份客户端、同步客户端、传输客户端、归档客户端）组成，dbops服务负责做元数据增、删、查、改、及图表展示，api接口服务为各种客户端提供数据交换。  
   
   ![平台架构](https://github.com/mafeicnnui/dbops/blob/master/static/doc/images/framework.png)
   

## 三、功能概述
       
   | 功能名称   | 功能描述                                           | 备注                        |
| ---------- | :------------------------------------------------- | --------------------------- |
| 用户管理   | 用户新增、查询、维护、项目授权                     | 项目授权：用户数据源授权    |
| 功能管理     | 功能新增、查询、维护                               |                             |
| 菜单管理   | 菜单的新增、查询、变更操作                         |                             |
| 角色管理   | 角色新增、查询、维护                               | 可配置菜单及功能权限        |
| 数据源管理 | 数据源定义、查询、维护、控制台管理                 |                             |
| 服务器管理 | 数据库服务器配置、查询、维护、控制台管理           |                             |
| 数据库管理 | 数据库实例创建、维护、远程启停、控制台等功能       |                             |
| 数据库监控 | 数据库指标、监控模板、监控告警任务、监控大屏管理   |                             |
| 数据库工具 | 数据字典工具、记录数对比、表结构对比工具           |                             |
| 数据库备份 | 数据库备份配置、查询、维护、分析、任务推送功能     |                             |
| 数据库同步 | 数据库同步任务配置、查询、维护、分析、任务推送功能 | 同步类型详见1.2.3           |
| 数据库传输 | 数据库传输任务定义、查询、维护操作                 |                             |
| 数据库归档 | 数据库归档任务定义、查询、维护操作                 |                             |
| 大数据同步 | 支持NOSQL同步                                      | 支持HBASE、ES、DORIS        |
| 慢日志管理 | 慢查询配置、查询、维护、分析功能                   |                             |
| 工单管理   | 工单查询、工单发布、工单导出、工单审核、工单运行等 | 支持MySQL、Mongo、ES、Redis |
| 报表平台   | 自定义报表、报表维护、报表查询、报表预处理等       | 支持MySQL、CH数据源         |
| 系统管理   | 系统设置、工单审核规则、代码管理                   |                             |

### 3.1 项目授权

- 为用户授于工单平台数据源权限，分为工单查询、工单发布、工单审核、工单执行、工单导出权限，同一数据源支持同步授于或取消多个权限。

### 3.2 数据源管理

- 数据源配置、变更、可通过web控制台管理数据源，支持数据源有:MySQL、MSSQL、PostgreSQL、MongoDB、ES、REDIS、DORIS、Clickhouse等

### 3.3 服务器管理

- 服务器配置、变更、可通过web控制台管理服务器，进行日常维护，支持windows、linux系统

### 3.4 数据库管理

- 可自定义数据库参数、远程一键安装部署、远程启停、自启动设置、数据库控制台管理实例，支持MySQL数据库

### 3.5 数据库监控

- 自定义指标、自定义模板、一键部署采集任务、监控任务、监控大屏、监控图表、告警邮件及微信通知
采集任务、监控任务涉及到调用dbapi接口，由dbapi接口负责推送任务及推送采集告警客户端至远程服务器

### 3.6 数据库工具

- 数据字典工具
   用于从数据源中生成数据字典文档，支持MySQL,MSSQL
   
- 记录数对比
  用于数据源间记录数对比，主要是数据同步后记录数比较
  
- 表结构对比工具
  用于对于开发与生产环境表结构、索引差异，并生成报告

### 3.7 数据库备份

- 数据库备份配置、日常维护、任务查询、图表分析，远程任务推送，需要调用dbapi接口推送备份配置及备份客户端至备份服务器
- 支持备份数据类型：MySQL、MSSQL、ES、Redis、Oracle、MongoDB，支持阿里云、腾讯云oss备份，MySQL支持binlog备份


### 3.8 数据库同步

- 支持的实时同步类型如下：


| 同步类型     | 全量 | 增量 | DDL  | 备注         |
| ------------ | ---- | ---- | ---- | ------------ |
| mysql->mysql | Y    | Y    | Y    | 解析binlog   |
| mysql->kafka | Y    | Y    | Y    | 解析binlog   |
| mysql->ES    | Y    | Y    | Y    | 解析binlog   |
| mysql->mongo | S    | S    | -    | 解析binlog   |
| mysql->clickhouse | S    | S    | -    | 解析binlog   |
| mongo->mongo | S    | S    | -    | 解析rs.oplog |
| mongo->kafka | Y    | Y    | Y    | 解析rs.oplog |
| mongo->ES    | Y    | Y    | Y    | 解析rs.oplog |


说明：S：表示目前不支持以后会支持,   \- ：表示没有意义, 灰色行：表示合生通或会付通已上线该任务

- 支持的离线同步类型如下：
       

| 同步类型     | 全量 | 增量 | DDL  | 自定义列 | 自修复 | 备注      |
| ------------ | ---- | ---- | ---- | -------- | ------ | --------- |
| mysql->mysql | Y    | Y    | Y    | Y        | Y      | 时间戳    |
| mysql->mssql | Y    | Y    | Y    | Y        | Y      | 时间戳    |
| mysql->mongo | Y    | Y    | -    | S        | S      | 时间戳    |
| mysql->pg    | Y    | Y    | Y    | Y        | Y      | 时间戳    |
| mysql->ES    | Y    | Y    | N    | Y        | N      | dataX封装 |
| mysql->doris | Y    | Y    | N    | Y        | N      | dataX封装 |
| mongo->mongo | Y    | Y    | -    | S        | N      | 时间戳    |
| mssql->mssql | Y    | Y    | Y    | S        | S      | 时间戳    |
| mssql->mysql | Y    | Y    | Y    | S        | S      | 时间戳    |

  说明：S：表示目前不支持以后会支持,   \- ：表示没有意义, 灰色行：表示经过生产验证
       
## 四、安装部署  


### 4.1 安装python3环境 
    
    yum -y install python3
    

### 4.2 安装python3及依赖  

    pip3 install -r requirements.txt -i https://pypi.douban.com/simple
    
### 4.3  数据库连接配置

    vi /config/config.json 
    {
        "db_ip"        : "192.168.1.100",
        "db_port"      : "3306",
        "db_user"      : "puppet",
        "db_pass"      : "12345678",
        "db_service"   : "puppet",
        "db_charset"   : "utf8"
    }
    
        
### 4.4 数据库初始化
    
    详见：sql/README.md

## 五、停启服务

### 5.1 启动服务  

    start.sh 


### 5.2 重启服务  

    restart.sh
    
### 5.3 配置nginx  

    详见 /dbops/doc/conf/nginx.conf


### 5.4 停止服务  

    stop.sh

### 5.5 访问EaseBase  
    
    http://IP:81
    user:admin/admin

## 六、docker部署 

### 6.1 获取镜像

    docker pull mafeicnnui/dbops:2.0

### 6.2 配置数据源

    mkdir /home/dbops
    vi config.json 
    {
        "db_ip"        : "192.168.1.100”,
        "db_port"      : "3306",
        "db_user"      : "puppet",
        "db_pass"      : "Abcd@1234",
        "db_service"   : "puppet",
        "db_charset"   : "utf8"
    }


### 6.3 运行容器

    docker run \
       --name dbops \
       -p 8080:8080 \
       -v /home/dbops/config.json:/opt/dbops/config/config.json:ro \
       -d mafeicnnui/dbops:2.3
    
### 6.4 访问 easebase
    
    http://IP:8081
    user:admin/admin

## 七、联系方式

    zhdn_791005@163.com
    
![image](https://github.com/mafeicnnui/dbops/blob/master/static/doc/images/weixin.png)