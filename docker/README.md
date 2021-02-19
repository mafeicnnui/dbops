一、编写Dockerfile

    more Dockerfile
    FROM python:3.6
    ADD req.txt /opt
    ADD dbops.tar /opt/
    RUN /usr/local/bin/python -m pip install --upgrade pip && pip3 install -r /opt/req.txt -i https://pypi.douban.com/simple && chmod a+x /opt/dbops/*.sh
    WORKDIR /opt/dbops
    ENTRYPOINT ["/opt/dbops/start_docker"]

二、打包为镜像

    docker build -t dbops:2.0 .

三、进入容器

    docker exec -it 7afe808da8ae /bin/sh

四、上传hub

    docker tag dbops:2.0 mafeicnnui/dbops:2.0
    docker push mafeicnnui/dbops:2.0

五、拉取镜像

    docker pull mafeicnnui/dbops:2.0

六、配置数据源

    mkdir /home/dbops
    vi config.json
    {
        "db_ip"         : "rm-2ze2k586u0g2hnbaqfo.mysql.rds.aliyuncs.com",
        "db_port"      : "3306",
        "db_user"      : "puppet",
        "db_pass"      : "Puppet@123",
        "db_service"   : "easebase",
        "db_charset"   : "utf8"
    }

七、启动容器

    docker run \
       --name easebase \
       -p 8080:8000 \
       -v /home/dbops/config.json:/opt/dbops/config/config.json:ro \
       -d mafeicnnui/dbops:2.0