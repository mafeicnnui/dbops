## 一、平台介绍  

   Easebase平台是一款基于python3.6+tornado+bootstrap开发的数据库自动化运维平台，功能非常丰富，将DBA日常绝大多数工作都自动化管理，提升DBA工作效率
   该平台依赖dbapi平台接口服务，需要在部署后再部署dbapi服务 
   
## 二、平台架构
   
   ![平台架构](https://github.com/mafeicnnui/dbops/blob/master/static/doc/images/framework.png)
   

## 三、功能概述
       
   | 功能名称   | 功能描述                                           | 备注                        |
| ---------- | :------------------------------------------------- | --------------------------- |
| 用户管理   | 用户新增、查询、维护、项目授权                     | 项目授权：用户数据源授权    |
| 能管理     | 功能新增、查询、维护                               |                             |
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
    
     mysql -upuppet -p12345678 -h'192.168.1.1' <puppet.sql

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
