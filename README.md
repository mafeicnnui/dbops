一、概述  

   Easebase 数据库自动化运维平台,基于python3.6+tornado+bootstrap开发 
   
   说明：该平台依赖dbapi平台接口服务，需要在部署后再部署dbapi服务。  

   功能：  
   
       1.1 用户管理、角色管理、功能管理、菜单管理、系统设置
       
       1.2 数据源管理、服务器管理、数据库库管理、慢日志管理、数据库监控
       
       1.3 数据库备份、数据库同步、数据库传输、数据库归档、大数据同步
       
       1.4 工单管理、图片管理、端口管理  
       
       
二、安装部署  


2.1 安装python3环境 
    
    yum -y install python3
    

2.2 安装python3及依赖  

    pip3 install -r requirements.txt -i https://pypi.douban.com/simple
    
2.3  数据库连接配置

    vi /config/config.json 
    {
        "db_ip"        : "192.168.1.100",
        "db_port"      : "3306",
        "db_user"      : "puppet",
        "db_pass"      : "12345678",
        "db_service"   : "puppet",
        "db_charset"   : "utf8"
    }
    
        
2.5 数据库初始化
    
     mysql -upuppet -p12345678 -h'192.168.1.1' <puppet.sql

三、停启服务

3.1 启动服务  

    start.sh 


3.2 重启服务  

    restart.sh
    
3.4 配置nginx  

    详见 /dbops/doc/conf/nginx.conf


3.3 停止服务  

    stop.sh

3.4 访问devops  
    
    http://IP:81
    user:admin/admin

三、docker部署 

3.1 获取镜像

    docker pull mafeicnnui/dbops:2.0

3.2 配置数据源

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


3.3 运行容器

    docker run \
       --name dbops \
       -p 8080:8080 \
       -v /home/dbops/config.json:/opt/dbops/config/config.json:ro \
       -d mafeicnnui/dbops:2.3
    
3.4 访问 easebase
    
    http://IP:8081
    user:admin/admin
