一、配置数据源

    mkdir /home/dbops
    vi config.json 
    {
        "db_ip"        : "x.x.x.x”,
        "db_port"      : "3306",
        "db_user"      : "puppet",
        "db_pass"      : "Puppet@123",
        "db_service"   : "puppet",
        "db_charset"   : "utf8"
    }

二、启动容器web服务

    docker run \
        --name dbops \
        -p 8080:8080 \
        -v /home/dbops/config.json:/opt/dbops/config/config.json:ro \
        -d mafeicnnui/dbops:3.0


三、启动容器(web,api两个服务)

    docker run \
        --name easebase \
        -p 8081:8081 \
        -p 8080:8080 \
        -v /home/dbops/config.json:/opt/config/config.json:ro \
        -d mafeicnnui/easebase:1.0