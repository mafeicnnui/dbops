FROM python:3.6
ADD req.txt /opt
ADD supervisord.conf /etc
ADD dbops.tar /opt/
RUN /usr/local/bin/python -m pip install --upgrade pip \
 && pip3 install -r /opt/req.txt -i https://pypi.douban.com/simple \
 && pip3 install git+https://github.com/Supervisor/supervisor -i https://pypi.douban.com/simple \
 && chmod a+x /opt/dbops/*.sh
WORKDIR /opt/dbops
ENTRYPOINT ["/usr/local/bin/supervisord -f /etc/supervisord.conf"]
