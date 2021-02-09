一、概述  

   Easebase 数据库自动化运维平台是基本python3.6开发，后端使用tornado框架，前端使用bootstrap框架。  
   
   说明：该平台依赖dbapi平台接口服务，需要在部署后再部署dbapi服务。  

   功能：  
   
       1.1 用户管理、角色管理、功能管理、菜单管理、系统设置
       
       1.2 数据源管理、服务器管理、数据库库管理、慢日志管理、数据库监控
       
       1.3 数据库备份、数据库同步、数据库传办理、数据库归档、大数据同步
       
       1.4 工单管理、图片管理、端口管理  
       
       
二、安装部署  


2.1 安装python3环境 
    
    yum -y install python3
    

2.2 安装python3及依赖  

    pip3 install -r requirements.txt -i https://pypi.douban.com/simple
    
2.3  数据库连接配置

    编辑：./config/config.json 文件：
    {
        "db_ip"        : "10.2.39.17",
        "db_port"      : "23306",
        "db_user"      : "puppet",
        "db_pass"      : "12345678",
        "db_service"   : "puppet",
        "db_charset"   : "utf8"
    }
        
2.5 数据库初始化
    
      结构：devops.sql  
      数据：devops_init.sql
    

三、停启服务

3.1 启动服务  

    cd dbops
    # 通过yum 安装python3
    ./start.sh 
    
    # 自定义安装 python3情况
    ./start_env.sh   

3.2 重启服务  

   cd dbops
   ./restart.sh


3.3 停止服务  

   cd dbops
   ./stop.sh

3.4 访问devops  
    
    http://localhost:81
    user:admin/admin

三、docker部署 

3.1 打镜像

    FROM python:3.6
    ADD req.txt /opt
    ADD dbops.tar /opt/
    RUN /usr/local/bin/python -m pip install --upgrade pip && pip3 install -r /opt/req.txt -i https://pypi.douban.com/simple && chmod a+x /opt/dbops/*.sh
    WORKDIR /opt/dbops
    ENTRYPOINT ["/opt/dbops/start.sh"]

3.2 构建镜像

    docker build -t dbops:v1 .


3.2 运行容器

    docker run dbops:v1