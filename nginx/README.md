# 安装nginx，支持ssl
    sudo yum remove nginx -y
    sudo yum install -y epel-release
    sudo yum install -y nginx
    nginx -V 2>&1 | grep -o with-http_ssl_module**

# 错误日志：
    cat /usr/local/nginx/logs/error.log