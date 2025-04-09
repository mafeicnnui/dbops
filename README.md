## 一、平台介绍  

   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Easebase平台是一款基于python3.6.8+tornado+bootstrap开发的数据库自动化运维平台，功能非常丰富，将DBA日常绝大多数工作都自动化管理，提升DBA工作效率
   
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;EaseBase数据库运维平台是为了提高DBA运维效率设计研发的，结合公司现状态将日常工作中重复性多的工作程序化，提高数据库运维效率，DBA可以更高效工作，同时为公司节省运营成本。 
平台将DBA工作中最常用的功能“数据库备份”、“数据库同步”、“数据库传输”、“数据库归档”、“大数据同步”、“数据源管理”、“服务器管理”、“数据库监控”、“工单管理”、数据库管理”、“数据库恢复”、 “数据库部署”、“慢查询管理”等功能。
另外，数据库同步、数据库传输以后会集成更多的功能，支持更丰富的数据源。该平台依赖dbapi平台接口服务，需要在部署后再部署dbapi服务 
   
## 二、平台架构

   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;平台由dbops WEB服务+dbapi接口服务+客户端（备份客户端、同步客户端、传输客户端、归档客户端）组成，dbops服务负责做元数据增、删、查、改、及图表展示，api接口服务为各种客户端提供数据交换。  
   
   ![平台架构](https://gitee.com/mafeicnnui/csdn-blog-gallery/raw/master/framework.png)
   

## 三、功能概述
       
   | 功能名称   | 功能描述                       | 备注                        |
| ---------- |:---------------------------| --------------------------- |
| 用户管理   | 用户新增、查询、维护、项目授权            | 项目授权：用户数据源授权    |
| 功能管理     | 功能新增、查询、维护                 |                             |
| 菜单管理   | 菜单的新增、查询、变更操作              |                             |
| 角色管理   | 角色新增、查询、维护                 | 可配置菜单及功能权限        |
| 数据源管理 | 数据源定义、查询、维护、控制台管理          |                             |
| 服务器管理 | 数据库服务器配置、查询、维护、webssh控制台 |                             |
| 数据库管理 | 数据库实例创建、维护、远程启停、控制台等功能     |                             |
| 数据库监控 | 数据库指标、监控模板、监控告警任务、监控大屏管理   |                             |
| 数据库工具 | 数据字典工具、记录数对比、表结构对比工具       |                             |
| 数据库备份 | 数据库备份配置、查询、维护、分析、任务推送功能    | 部署dbapi服务                            |
| 数据库同步 | 数据库同步任务配置、查询、维护、分析、任务推送功能  | 部署dbapi服务          |
| 数据库传输 | 数据库传输任务定义、查询、维护操作          |                             |
| 数据库归档 | 数据库归档任务定义、查询、维护操作          |                             |
| 大数据同步 | 支持NOSQL同步                  | 支持HBASE、ES、DORIS        |
| 慢日志管理 | 慢查询配置、查询、维护、分析功能           |                             |
| 工单管理   | 工单查询、工单发布、工单导出、工单审核、工单运行等  | 支持MySQL、Mongo、ES、Redis |
| 报表平台   | 自定义报表、报表维护、报表查询、报表预处理等     | 支持MySQL、CH数据源         |
| 系统管理   | 系统设置、工单审核规则、代码管理           |                             |

### 3.1 项目授权

- 为用户授于工单平台数据源权限，分为工单查询、工单发布、工单审核、工单执行、工单导出权限，同一数据源支持同步授于或取消多个权限。

### 3.2 数据源管理

- 数据源配置、变更、可通过web控制台管理数据源，支持数据源有:MySQL、MSSQL、PostgreSQL、MongoDB、ES、REDIS、DORIS、Clickhouse等

### 3.3 服务器管理

- 服务器配置、变更、可通过web控制台管理服务器，进行日常维护，支持windows、linux系统、支持webssh，rdb连接linux及windows桌面

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

- 备份类型： 

        MySQL、MSSQL、ES、Redis、Oracle、MongoDB，支持阿里云、腾讯云oss备份，MySQL支持binlog备份


- 操作界面：

        备份服务器：列出“服务器管理-新增服务器”模块中的备份服务器
        
        数据库类型：mysql，redis，elasticsearch、mongo
        
        备份有效期：备份文件保留时长（天）
        
        备份主目录：远程备份服务器上备份文件存放目录
        
        脚本主目录：远程备份服务器上备份客户端脚本存放目录
        
        备份脚本名：脚本名称是固定的，不能修改
        
        备份命令名：数据库备份命令绝对路径
        
        运行时间：备份脚本定时执行时间，通过将配置推送至服务器以crontab方式运行
        
        PYTHON3_HOME：python3绝对路径
        
        备份数据库：备份指定的数据库，以逗号分隔可以写多个库名
        
        API服务器：备份客户端依赖数据库平台API接口服务来实现数据交互，日志写入
        
        任务状态：设置“启用”或“禁用”任务，已禁用的任务crontab无法启动

### 3.8 数据库同步

- 实时同步类型：


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

- 离线同步类型：
       

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
       
- 操作界面：
       
        同步服务器：列出“服务器管理-新增服务器”模块中的同步服务器
        
        数据库类型：MySQL，SQLServer
        
        源端数据库：源数据库数据源信息，列表框数据来源（数据源管理-新增数据源）
        
        目标数据库：目标数据库数据源信息，列表框数据来源（数据源管理-新增数据源）
        
        同步业务类型：对同步的不同类型打标签
        
        同步数据方向：目前有效的有mysql->mysql,mssql->mysql
        
        同步主目录：远程同步服务器上同步客户端脚本文件存放目录
        
        脚本主目录：远程备份服务器上备份客户端脚本存放目录
        
        同步脚本名：脚本名称是固定的，不能修改。
        
        运行时间：同步脚本定时执行时间，通过将配置推送至服务器以crontab方式运行。
        
        同步数据库名：同步源端数据库名称
        
        同步表列表：源库中同步表列表，格式：表名：增量列名：时间
        
        全量批大小：全量同步多少条数据打成一批进行同步
        
        增量批大小：增量同步多少条数据打成一批进行同步
        
        新增列名：同步时可以配置目标库中增加的列名，目前只支持一个列名     
        
        PYTHON3_HOME：python3绝对路径
        
        同步时间类型：天，小时，分钟
        
        API服务器：同步客户端依赖数据库平台API接口服务来实现数据交互，日志写入
        
        任务状态：设置“启用”或“禁用”任务，已禁用的任务crontab无法启动。
       
## 四、安装部署  


### 4.1 安装python3环境 

    系统：CentOS Linux release 7.6.1810 
    
    yum -y install python3    
    yum -y install python3-devel
    yum -y install fontconfig 
    

### 4.2 安装python3及依赖  
    cd dbops
    pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
    
### 4.3  数据库连接配置

    vi /config/config.json 
    {
        "db_ip"        : "192.168.1.100",
        "db_port"      : "3306",
        "db_user"      : "puppet",
        "db_pass"      : "xxxxxx",
        "db_service"   : "puppet",
        "db_charset"   : "utf8"
    }
    
        
### 4.4 数据库初始化
    
    详见：sql/README.md

## 五、停启服务

### 首次运行执行：

    cd dbops    
    chmod +x *.sh
    
### 安装字体

    cd dbops/doc/font
    sudo mkdir -p /usr/share/fonts/dejavu
    cd dbops/doc/font
    tar xf dejavu.tar.gz
    sudo cp DejaVuSans.ttf /usr/share/fonts/dejavu
    fc-cache
    fc-list    
    

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

    详见 docker/README.md
    
### 6.4 访问 easebase
    
    http://x.x.x.x:8081
    user:admin/admin

## 七、联系方式

    zhdn_791005@163.com

![image](https://github.com/mafeicnnui/dbops/blob/master/static/doc/images/qq.png)