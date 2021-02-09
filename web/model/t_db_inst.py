#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : 马飞
# @File    : t_user.py
# @Software: PyCharm

from web.utils.common import aes_encrypt,aes_decrypt,get_connection_ds_read_limit,get_connection_ds_write_limit,get_connection_ds_sqlserver
from web.utils.common import exception_info,get_connection,get_connection_ds,get_connection_dict,get_db_conf,format_sql
from web.utils.common import exception_info_mysql,exception_info_sqlserver,format_mysql_error,format_sqlserver_error
from web.model.t_sql_check import get_audit_rule
import traceback
import pymysql
import re
import os,json

'''
  数据库管理-新建实例
'''
def query_inst_list():
    db = get_connection()
    cr = db.cursor()
    sql = """SELECT  a.id,a.inst_name FROM  t_db_inst a  order by a.created_date"""
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def query_inst(inst_name):
    db = get_connection()
    cr = db.cursor()
    v_where =''
    if inst_name != '':
        v_where = "  where a.inst_name like '%{0}%' ".format(inst_name)

    sql = """SELECT  
                 a.id,
                 a.inst_name,
                 CASE WHEN a.is_rds='Y' THEN
                   concat(substr(a.inst_ip,1,20),'...')
                 ELSE
                   (SELECT server_ip FROM t_server b WHERE b.id=a.server_id) 
                 END AS  inst_ip,   
                 a.inst_port,
                 a.inst_type,
                 (SELECT dmmc FROM t_dmmx X WHERE x.dm='02' AND x.dmm=a.inst_type) AS inst_type_name,
                 a.inst_env,
                 (SELECT dmmc FROM t_dmmx X WHERE x.dm='03' AND x.dmm=a.inst_env) AS inst_env_name,
                 a.inst_status,
                 (SELECT dmmc FROM t_dmmx X WHERE x.dm='32' AND x.dmm=a.inst_status) AS inst_status_name,
                 (SELECT dmmc FROM t_dmmx X WHERE x.dm='27' AND x.dmm=a.inst_ver) AS inst_ver_name,
                 CASE is_rds WHEN 'Y' THEN '是'  WHEN 'N' THEN '否' END  STATUS,
                 a.inst_reboot_flag,
                 DATE_FORMAT(a.created_date,'%Y-%m-%d %h:%i:%s')  AS created_date
            FROM  t_db_inst a
            {0}
            order by a.inst_name
          """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def query_inst_by_id(p_inst_id):
    db  = get_connection_dict()
    cr  = db.cursor()
    sql = """SELECT a.id,
                    a.inst_name,
                    (SELECT id FROM t_server b WHERE b.id=a.server_id) as server_id,
                    (SELECT server_desc FROM t_server b WHERE b.id=a.server_id) as server_desc,
                    CASE WHEN a.is_rds='Y' THEN
                       a.inst_ip
                    ELSE
                       (SELECT server_ip FROM t_server b WHERE b.id=a.server_id) 
                    END AS  inst_ip,
                    a.inst_port,
                    a.inst_type,
                    a.inst_env,
                    a.inst_ver,
                    a.templete_id,
                    a.is_rds,
                    a.mgr_user,
                    a.mgr_pass,
                    date_format(a.created_date,'%Y-%m-%d %H:%i:%s')  as created_date,
                    a.api_server,
                    a.python3_home,
                    a.script_path,
                    a.script_file,
                    inst_mapping_port              
             FROM t_db_inst a WHERE  a.id='{0}'""".format(p_inst_id)
    print(sql)
    cr.execute(sql)
    rs=cr.fetchone()
    print('password=',aes_decrypt(rs['mgr_pass'],rs['mgr_user']))
    rs['mgr_pass'] = aes_decrypt(rs['mgr_pass'],rs['mgr_user'])
    print("rs->password=",rs['mgr_pass'])
    cr.close()
    db.commit()
    return rs

def get_ds_by_instid(p_inst_id):
    db  = get_connection_dict()
    cr  = db.cursor()
    sql = """SELECT a.id          as dsid,
                    a.inst_name   as db_desc,
                    CASE WHEN a.is_rds='Y' THEN
                       a.inst_ip
                    ELSE
                       (SELECT server_ip FROM t_server b WHERE b.id=a.server_id) 
                    END AS  ip,
                    CASE when a.inst_mapping_port is null or a.inst_mapping_port ='' then 
                       a.inst_port 
                    ELSE 
                       a.inst_mapping_port
                    END as port,
                    a.inst_type   as db_type,
                    a.inst_env    as db_env,
                    a.mgr_user    as user,
                    a.mgr_pass    as password,
                    ''            as service,
                    date_format(created_date,'%Y-%m-%d %H:%i:%s')  as created_date                    
             FROM t_db_inst a 
             WHERE  a.id='{0}'""".format(p_inst_id)
    print(sql)
    cr.execute(sql)
    rs=cr.fetchone()
    rs['password'] = aes_decrypt(rs['password'],rs['user'])
    print("rs->password=",rs['password'])
    cr.close()
    db.commit()
    return rs

def get_inst_id():
    db = get_connection()
    cr = db.cursor()
    cr.execute('select max(id)+1 from t_db_inst for update')
    rs=cr.fetchone()
    cr.close()
    return rs[0]

def save_db_inst(d_inst):
    result = {}
    val=check_db_inst(d_inst,'add')
    if val['code']=='-1':
        return val
    try:
        db        = get_connection()
        cr        = db.cursor()
        result    = {}
        inst_id   = get_inst_id()

        if d_inst['mgr_pass'] != '':
            inst_pass = aes_encrypt(d_inst['mgr_pass'], d_inst['mgr_user'])
        else:
            inst_pass = d_inst['mgr_pass']

        # 保存实例元数据
        sql="""insert into t_db_inst(id,inst_name,server_id,templete_id,inst_ip,inst_port,inst_type,inst_env,
                                     is_rds,inst_ver,mgr_user,mgr_pass,created_date,api_server,python3_home,script_path,script_file,inst_mapping_port)
                   values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}',
                          '{8}','{9}','{10}','{11}',now(),'{12}','{13}','{14}','{15}','{16}')
            """.format(inst_id,d_inst['inst_name'],d_inst['server_id'],d_inst['templete_id'],
                       d_inst['inst_ip'],d_inst['inst_port'],d_inst['inst_type'],d_inst['inst_env'],
                       d_inst['is_rds'],d_inst['inst_ver'],d_inst['mgr_user'],inst_pass,d_inst['api_server'],
                       d_inst['python3_home'], d_inst['script_path'], d_inst['script_file'],d_inst['inst_mapping_port']
                       )
        print(sql)
        cr.execute(sql)

        # 生成实例配置信息
        sql = """insert into t_db_inst_parameter(inst_id,name,value,type,STATUS,create_date)
                 select a.id,b.dmmc,b.dmm,'mysqld',b.flag,NOW() 
                  from t_db_inst a,t_dmmx b 
                  where a.templete_id=b.dm 
                    and b.dm='30' and b.flag='1'
                    and b.dmm NOT LIKE '%default-character-set=utf8mb4%'
                    and a.id={}
                 UNION ALL
                  select a.id,b.dmmc,b.dmm,'mysql',b.flag,NOW() 
                  from t_db_inst a,t_dmmx b 
                  where a.templete_id=b.dm 
                    and b.dm='30' AND b.flag='1' 
                    and b.dmm LIKE 'default-character-set%'
                    and a.id={}                 
                 UNION ALL
                 select a.id,b.dmmc,b.dmm,'client',b.flag,NOW() 
                  from t_db_inst a,t_dmmx b 
                  where a.templete_id=b.dm 
                    and b.dm='30' AND b.flag='1' 
                    and (b.dmm LIKE 'default-character-set%' OR b.dmm LIKE 'socket%')
                    and a.id={}
              """.format(inst_id,inst_id,inst_id)
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result['code']='0'
        result['message']='保存成功！'
        return result
    except:
        e_str = exception_info()
        print(e_str)
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result

def upd_db_inst(d_inst):
    result={}
    val = check_db_inst(d_inst,'upd')
    if  val['code'] == '-1':
        return val
    try:
        db        = get_connection()
        cr        = db.cursor()
        inst_pass = ''
        if d_inst['mgr_pass'] != '':
            inst_pass = aes_encrypt(d_inst['mgr_pass'], d_inst['mgr_user'])
        else:
            inst_pass = d_inst['mgr_pass']

        sql  = """update t_db_inst
                  set  
                      inst_name         ='{0}',
                      server_id         ='{1}', 
                      inst_ip           ='{2}', 
                      templete_id       ='{3}', 
                      inst_port         ='{4}', 
                      inst_type         ='{5}', 
                      inst_env          ='{6}',
                      inst_ver          ='{7}',
                      is_rds            ='{8}',
                      mgr_user          ='{9}',
                      mgr_pass          ='{10}',
                      api_server        ='{11}',                      
                      python3_home      ='{12}',
                      script_path       ='{13}',
                      script_file       ='{14}',
                      inst_mapping_port ='{15}',
                      last_update_date  = now()
                where id={16}""".format(d_inst['inst_name'],d_inst['server_id'],d_inst['inst_ip'],
                                        d_inst['templete_id'],d_inst['inst_port'],d_inst['inst_type'],
                                        d_inst['inst_env'],d_inst['inst_ver'],d_inst['is_rds'],
                                        d_inst['mgr_user'],inst_pass,d_inst['api_server'],
                                        d_inst['python3_home'], d_inst['script_path'], d_inst['script_file'],
                                        d_inst['inst_mapping_port'],d_inst['inst_id'])
        print(sql)
        cr.execute(sql)

        # 更新实例配置信息
        sql = """delete from t_db_inst_parameter where inst_id={}""".format(d_inst['inst_id'])
        print(sql)
        cr.execute(sql)
        sql = """insert into t_db_inst_parameter(inst_id,name,value,type,STATUS,create_date)
                        select a.id,b.dmmc,b.dmm,'mysqld',b.flag,NOW() 
                         from t_db_inst a,t_dmmx b 
                         where a.templete_id=b.dm 
                           and b.dm='30' and b.flag='1'
                           and b.dmm NOT LIKE '%default-character-set=utf8mb4%'
                           and a.id={}
                        UNION ALL
                         select a.id,b.dmmc,b.dmm,'mysql',b.flag,NOW() 
                         from t_db_inst a,t_dmmx b 
                         where a.templete_id=b.dm 
                           and b.dm='30' AND b.flag='1' 
                           and b.dmm LIKE 'default-character-set%'
                           and a.id={}                 
                        UNION ALL
                        select a.id,b.dmmc,b.dmm,'client',b.flag,NOW() 
                         from t_db_inst a,t_dmmx b 
                         where a.templete_id=b.dm 
                           and b.dm='30' AND b.flag='1' 
                           and (b.dmm LIKE 'default-character-set%' OR b.dmm LIKE 'socket%')
                           and a.id={}
                     """.format(d_inst['inst_id'], d_inst['inst_id'], d_inst['inst_id'])
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='更新成功！'
    except :
        print(traceback.format_exc())
        result['code'] = '-1'
        result['message'] = '更新失败！'
    return result

def del_db_inst(p_instid):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        sql="delete from t_db_inst  where id='{0}'".format(p_instid)
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='删除成功！'
    except :
        result['code'] = '-1'
        result['message'] = '删除失败！'
    return result


def create_db_inst(p_api,p_instid):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '实例正在创建中，详见日志...'
        v_cmd="curl -XPOST {0}/create_db_inst -d 'inst_id={1}'".format(p_api,p_instid)
        print('create_db_inst=',v_cmd)
        r=os.popen(v_cmd).read()
        d=json.loads(r)
        if d['code']==200:
              return result
        else:
           result['code'] = '-1'
           result['message'] = '{0}!'.format(d['msg'])
           return result
    except Exception as e:
        print(traceback.print_exc())
        result['code'] = '-1'
        result['message'] = '实例正在创建失败，详见错误日志!'
        return result

def destroy_db_inst(p_api,p_instid):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '实例正在销毁中，详见日志...'
        v_cmd="curl -XPOST {0}/destroy_db_inst -d 'inst_id={1}'".format(p_api,p_instid)
        print('destroy_db_inst=',v_cmd)
        r=os.popen(v_cmd).read()
        d=json.loads(r)
        if d['code']==200:
              return result
        else:
           result['code'] = '-1'
           result['message'] = '{0}!'.format(d['msg'])
           return result
    except Exception as e:
        print(traceback.print_exc())
        result['code'] = '-1'
        result['message'] = '实例销毁失败，详见错误日志!'
        return result

def manager_db_inst(p_api,p_instid,p_op_type):
    try:
        result = {}
        result['code'] = '0'
        if p_op_type == 'start':
           result['message'] = '实例已启动'
        elif p_op_type == 'stop':
           result['message'] = '实例已停止'
        elif p_op_type == 'restart':
           result['message'] = '实例已重启完成'
        elif p_op_type == 'autostart':
           result['message'] = '自启动已配置完成'
        elif p_op_type == 'cancel_autostart':
           result['message'] = '已取消实例自重启'
        else:
           result['message'] =''

        v_cmd="curl -XPOST {0}/manager_db_inst -d 'inst_id={1}&op_type={2}'".format(p_api,p_instid,p_op_type)
        print('destroy_db_inst=',v_cmd)
        r=os.popen(v_cmd).read()
        d=json.loads(r)
        if d['code']==200:
              return result
        else:
           result['code'] = '-1'
           result['message'] = '{0}!'.format(d['msg'])
           return result
    except Exception as e:
        print(traceback.print_exc())
        result['code'] = '-1'
        result['message'] = '操作时发生错误，详见服务日志!'
        return result

def log_db_inst(p_instid):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = ''
        db = get_connection_dict()
        cr = db.cursor()
        sql = """SELECT 
                   concat(DATE_FORMAT(create_date,'%Y-%m-%d %H:%i:%s'),' => ', a.message) AS log
                 FROM t_db_inst_log a 
                 WHERE  a.inst_id='{0}' 
                 ORDER BY a.create_date""".format(p_instid)
        #print(sql)
        cr.execute(sql)
        rs = cr.fetchall()
        v_log=''
        for r in rs:
            v_log=v_log+r['log']+'\n'
        cr.close()
        db.commit()
        result['message'] = v_log[0:-1]
        #print('log_db_inst=',v_log)
        return result
    except:
        print(traceback.print_exc())
        result['code'] = '-1'
        result['message'] = '获取日志失败!'
        return result

def check_inst_rep(d_inst):
    db = get_connection()
    cr = db.cursor()
    if d_inst['is_rds'] == 'N':
        sql = "select count(0) from t_db_inst  where  server_id='{0}' and inst_port='{1}'".\
               format(d_inst['server_id'],d_inst['inst_port'])
    else:
        sql = "select count(0) from t_db_inst  where  inst_ip='{0}' and inst_port='{1}'". \
            format(d_inst['inst_ip'], d_inst['inst_port'])
    print(sql)
    cr.execute(sql)
    rs=cr.fetchone()
    cr.close()
    db.commit()
    return rs[0]

'''
  数据库管理-实例管理
'''

def get_tree_by_instid(instid):
    print('get_tree_by_instid=',instid)
    try:
        result = {}
        v_html = ""
        p_ds   = get_ds_by_instid(instid)
        print('p_ds=',p_ds)
        db     = get_connection_ds(p_ds)
        print('db=',db)
        cr     = db.cursor()
        sql1 = """SELECT schema_name FROM information_schema.SCHEMATA order by 1"""

        sql2 = """SELECT table_name
                   FROM information_schema.tables WHERE table_schema='{0}' order by 1
               """
        cr.execute(sql1)
        rs1 = cr.fetchall()
        for i in range(len(rs1)):
            cr.execute(sql2.format(rs1[i][0]))
            rs2 = cr.fetchall()
            v_node = """<li><span class="folder">{0}</span><ul>""".format(rs1[i][0])
            v_html=v_html+v_node
            for j in range(len(rs2)):
                v_node = """<li><span class="file">{0}<div style="display:none">{1}</div></span></li>""".format(rs2[j][0],rs2[j][0])
                v_html = v_html + "\n" + v_node;
            v_html=v_html+"\n"+"</ul></li>"+"\n"

        cr.close()
        result['code'] = '0'
        result['message'] = v_html
        result['desc']    = p_ds['db_desc']
        result['db_url']  = p_ds['db_desc']
        #print(v_html)
    except Exception as e:
        print('get_tree_by_instid=>ERROR:',str(e))
        result['code'] = '-1'
        result['message'] = '加载失败！'
        result['desc'] = ''
        result['db_url'] = ''
    return result

def get_tree_by_instid_mssql(instid):
    print('get_tree_by_instid_mssql=',instid)
    try:
        result = {}
        v_html = ""
        p_ds   = get_ds_by_instid(instid)
        print('p_ds=',p_ds)
        db     = get_connection_ds_sqlserver(p_ds)
        print('db=',db)
        cr     = db.cursor()
        sql1 = ''
        if p_ds['service'] == '':
           sql1 = """ SELECT name FROM Master..SysDatabases  ORDER BY Name"""
        else:
           sql1 = """ SELECT name FROM Master..SysDatabases where name= DB_NAME() ORDER BY Name"""

        sql2 = """SELECT OBJECT_SCHEMA_NAME(id)+'.'+Name FROM SysObjects Where XType='U' ORDER BY Name
               """
        cr.execute(sql1)
        rs1 = cr.fetchall()
        for i in range(len(rs1)):
            cr.execute('use {}'.format(rs1[i][0]))
            cr.execute(sql2.format(rs1[i][0]))
            rs2 = cr.fetchall()
            v_node = """<li><span class="folder">{0}</span><ul>""".format(rs1[i][0])
            v_html=v_html+v_node
            for j in range(len(rs2)):
                v_node = """<li><span class="file">{0}<div style="display:none">{1}</div></span></li>""".format(rs2[j][0],rs2[j][0])
                v_html = v_html + "\n" + v_node;
            v_html=v_html+"\n"+"</ul></li>"+"\n"

        cr.close()
        result['code'] = '0'
        result['message'] = v_html
        result['desc']    = p_ds['db_desc']
        result['db_url']  = p_ds['db_desc']
        #print(v_html)
    except Exception as e:
        print('get_tree_by_instid_mssql=>error:',str(e))
        result['code'] = '-1'
        result['message'] = '加载失败！'
        result['desc'] = ''
        result['db_url'] = ''
    return result

def get_tab_ddl_by_instid(instid,tab,cur_db):
    try:
        result = {}
        p_ds   = get_ds_by_instid(instid)
        p_ds['service'] = cur_db
        print('get_tab_ddl_by_tname(p_ds)=>',p_ds)
        db     = get_connection_ds(p_ds)
        cr     = db.cursor()
        sql    = """show create table {0}""".format(tab)
        cr.execute(sql)
        rs=cr.fetchone()
        cr.close()
        result['code'] = '0'
        result['message'] = rs[1]
        print('rs=',rs,rs[1])
    except Exception as e:
        print('get_tab_ddl_by_tname.ERROR:',str(e))
        result['code'] = '-1'
        result['message'] = '获取表定义失败！'
    return result

def drop_tab_by_instid(instid,tab,cur_db):
    try:
        result = {}
        p_ds   = get_ds_by_instid(instid)
        p_ds['service'] = cur_db
        print('get_tab_ddl_by_tname(p_ds)=>',p_ds)
        db     = get_connection_ds(p_ds)
        cr     = db.cursor()
        sql    = """drop table {0}""".format(tab)
        cr.execute(sql)
        db.commit()
        result['code'] = '0'
        result['message'] = '删除成功!'
    except Exception as e:
        print('del_tab_by_instid:',str(e))
        result['code'] = '-1'
        result['message'] = '删除失败！'
    return result

def get_idx_ddl_by_instid(instid,tab,cur_db):
    try:
        result = {}
        p_ds   = get_ds_by_instid(instid)
        p_ds['service'] = cur_db
        db     = get_connection_ds(p_ds)
        cr     = db.cursor()
        sql    = '''SHOW INDEXES FROM {0}'''.format(tab)
        cr.execute(sql)
        rs=cr.fetchall()
        print('get_tab_idx_by_tname=',rs)
        v_idx_sql = ''
        v_idx_pks = ''
        for i in rs:
            print('r=', i)
            v_idx_name = i[2]
            v_idx_type = i[10]
            v_idx_cols = i[4]
            print('v_idx_name=',v_idx_name,'v_idx_type=',v_idx_type,'v_idx_cols=',v_idx_cols)
            if v_idx_name=='PRIMARY':
               v_idx_pks=v_idx_pks+v_idx_cols+','
            else:
               v_idx_sql = v_idx_sql+ 'create index {0} on {1}({2}) using {3}'.format(v_idx_name,tab,v_idx_cols,v_idx_type)+';\n'
            print('get_tab_idx_by_tname=',v_idx_sql)

        if v_idx_pks!='':
           v_idx_sql =  'alter table {0} add primary key({1});\n'.format(tab,v_idx_pks[0:-1])+v_idx_sql[0:-1]

        cr.close()
        result['code'] = '0'
        result['message'] = v_idx_sql
        print('rs=',rs,rs[1])
    except Exception as e:
        print('get_idx_ddl_by_instid=>error:',str(e))
        result['code'] = '-1'
        result['message'] = '未找到索引定义!'
    return result

def get_dss_for_inst(p_inst_id):
    db = get_connection()
    cr = db.cursor()
    sql="""select cast(id as char) as id,a.inst_name as name from t_db_inst a where id={}""".format(p_inst_id)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def check_db_inst(p_inst,p_flag):
    result = {}

    if p_inst["inst_name"]=="":
        result['code']='-1'
        result['message']='实例名不能为空!'
        return result

    if p_inst["server_id"] == "" and p_inst["is_rds"]=='N':
        result['code'] = '-1'
        result['message'] = '数据库服务器不能为空!'
        return result

    if p_inst["inst_ip"] == "" and p_inst["is_rds"]=='Y':
        result['code'] = '-1'
        result['message'] = '数据库地址不能为空!'
        return result

    if p_inst["inst_port"]=="":
        result['code']='-1'
        result['message']='实例端口不能为空!'
        return result

    if p_inst["inst_type"]=="":
        result['code']='-1'
        result['message']='实例类型不能为空!'
        return result
    if p_flag=='add':
        if check_inst_rep(p_inst)>0:
            result['code'] = '-1'
            result['message'] = '端口号重复!'
            return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result

def check_sql(p_instid,p_sql,curdb):
    result = {}
    result['status'] = '0'
    result['msg']    = ''
    result['data']   = ''
    result['column'] = ''

    if p_instid == '':
        result['status'] = '1'
        result['msg'] = '请选择数据源!'
        result['data'] = ''
        result['column'] = ''
        return result

    if p_sql =='':
        result['status'] = '1'
        result['msg'] = '请选中查询语句!'
        result['data'] = ''
        result['column'] = ''
        return result

    if p_sql.find('.')==-1 and curdb=='':
        result['status'] = '1'
        result['msg'] = '请选择数据库!'
        result['data'] = ''
        result['column'] = ''
        return result

    return result

def get_mysql_result(p_ds,p_sql,curdb):
    result   = {}
    columns  = []
    data     = []
    p_env    = ''

    #get read timeout
    read_timeout = int(get_audit_rule('switch_timeout')['rule_value'])
    print('read_timeout=',read_timeout)
    # if p_ds['db_env']=='1':
    #     p_env='PROD'
    # if p_ds['db_env']=='2':
    #     p_env='DEV'

    p_ds['service'] = curdb
    db = get_connection_ds_read_limit(p_ds, read_timeout)
    cr = db.cursor()

    try:
        cr.execute(p_sql)
        rs = cr.fetchall()

        #get sensitive column
        c_sensitive = get_audit_rule('switch_sensitive_columns')['rule_value'].split(',')

        #process desc
        i_sensitive = []

        desc = cr.description
        for i in range(len(desc)):
            if desc[i][0] in c_sensitive:
                i_sensitive.append(i)
            columns.append({"title": desc[i][0]})
        print('i_sensitive=',i_sensitive)

        #check sql rwos
        rule = get_audit_rule('switch_query_rows')
        if len(rs)>int(rule['rule_value']):
            result['status'] = '1'
            result['msg'] = rule['error'].format(rule['rule_value'])
            result['data'] = ''
            result['column'] = ''
            return result

        #process data
        for i in rs:
            tmp = []
            for j in range(len(desc)):
                if i[j] is None:
                   tmp.append('')
                else:
                   if j in  i_sensitive:
                       tmp.append(get_audit_rule('switch_sensitive_columns')['error'])
                   else:
                       tmp.append(str(i[j]))
            data.append(tmp)

        result['status'] = '0'
        result['msg'] = ''
        result['data'] = data
        result['column'] = columns
        cr.close()
        db.close()
        return result
    except pymysql.err.OperationalError as e:
        err= traceback.format_exc()
        print('get_mysql_result=', err)
        if err.find('timed out')>0:
            rule  = get_audit_rule('switch_timeout')
            result['status'] = '1'
            result['msg'] = rule['error'].format(rule['rule_value'])
            result['data'] = ''
            result['column'] = ''
            return result
        else:
            result['status'] = '1'
            result['msg'] = format_mysql_error(p_env, exception_info_mysql())
            result['data'] = ''
            result['column'] = ''
            return result
    except:
        print('get_mysql_result=',traceback.format_exc())
        result['status'] = '1'
        result['msg'] = format_mysql_error(p_env,exception_info_mysql())
        result['data'] = ''
        result['column'] = ''
        return result

def write_mysql_opr_log(p_userid,p_instid,p_sql,curdb):
    result ={}
    db = get_connection()
    cr = db.cursor()
    st = '''insert into t_db_inst_opt_log(user_id,inst_id,db,statement,status) values('{}','{}','{}','{}','{}')
         '''.format(p_userid,p_instid,curdb,format_sql(p_sql),'1')
    cr.execute(st)
    db.commit()

    result['status'] = '2'
    result['msg'] = '发布成功!'
    result['data'] = ''
    result['column'] = ''

    return result

    # 日志查询功能移至日志查询模块
    # ds = get_db_conf()
    # st = '''
    #       SELECT a.id,
    #              b.inst_name,
    #              a.db,
    #              a.statement,
    #              a.start_time,
    #              a.end_time,
    #              c.dmmc
    #       FROM t_inst_operate_log a ,t_db_inst b,t_dmmx c
    #        WHERE a.user_id={}
    #           AND b.id=a.inst_id
    #           AND c.dm='28' AND c.dmm=a.status
    #         ORDER BY a.status,a.start_time DESC
    #       '''.format(p_userid)
    # print('-------------------------------------------------')
    # print(ds)
    # print(st)
    # print(ds['db'])
    # result = get_mysql_result(ds, st, ds['db'])
    # print('result=',result)
    # return result

def get_sqlserver_result(p_ds,p_sql,p_curdb):
    result  = {}
    columns = []
    data    = []
    p_env   = ''
    if p_ds['db_env']=='1':
        p_env='PROD'
    if p_ds['db_env']=='2':
        p_env='DEV'

    try:
        db = get_connection_ds_sqlserver(p_ds)
        cr = db.cursor()
        print('get_sqlserver_result=>p_ds:', p_ds)
        print('get_sqlserver_result=>p_sql:',p_sql)
        cr.execute('use {}'.format(p_curdb))
        cr.execute(p_sql)
        rs = cr.fetchall()
        desc = cr.description
        for i in range(len(desc)):
            columns.append({"title": desc[i][0]})
        for i in rs:
            tmp = []
            for j in range(len(desc)):
                tmp.append(str(i[j]))
            data.append(tmp)

        result['status'] = '0'
        result['msg'] = ''
        result['data'] = data
        result['column'] = columns
        cr.close()
        db.close()
        return result
    except:
        result['status'] = '1'
        result['msg'] = format_sqlserver_error(p_env,exception_info_sqlserver())
        result['data']   = ''
        result['column'] = ''
        return result

def exe_query(p_userid,p_instid,p_sql,curdb):
    result = {}

    # 查询校验
    val = check_sql(p_instid, p_sql,curdb)
    if val['status'] != '0':
        return val

    p_ds = get_ds_by_instid(p_instid)

    # 查询MySQL数据源
    if p_ds['db_type']=='0':
        print('get_mysql_result=', p_ds)
        if len(re.findall(r'^select',p_sql.strip().lower(),re.M))>0 \
                or len(re.findall(r'^show', p_sql.strip().lower(), re.M)) > 0:
           result=get_mysql_result(p_ds,p_sql,curdb)
        else:
           result=write_mysql_opr_log(p_userid,p_instid,p_sql,curdb)

    # 查询MSQLServer数据源
    if p_ds['db_type'] == '2':
        print('get_sqlserver_result=',p_ds)
        result = get_sqlserver_result(p_ds, p_sql,curdb)

    return result


'''
  数据库管理-参数管理
'''

def check_db_pass_rep(p_para):
    db = get_connection()
    cr = db.cursor()
    sql = "select count(0) from t_db_inst_para  where  para_name='{0}'".format(p_para['para_name'])
    print(sql)
    cr.execute(sql)
    rs=cr.fetchone()
    cr.close()
    db.commit()
    return rs[0]

def check_db_inst_para(p_para):
    result = {}

    if p_para["para_name"]=="":
        result['code']='-1'
        result['message']='参数名不能为空！'
        return result

    if p_para["para_value"] == "":
        result['code'] = '-1'
        result['message'] = '参数值不能为空！'
        return result

    if p_para["para_desc"]=="":
        result['code']='-1'
        result['message']='参数描述不能为空！'
        return result

    if p_para["para_status"] == "":
        result['code'] = '-1'
        result['message'] = '参数状态不能为空！'
        return result

    if check_db_pass_rep(p_para)>0:
        result['code'] = '-1'
        result['message'] = '参数名不能重复!'
        return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result

def query_db_inst_para(para_code):
    db = get_connection()
    cr = db.cursor()
    v_where=' '
    if para_code != '':
        v_where = " where a.para_code like '%{0}%' or a.para_code like '%{1}%'".format(para_code,para_code)

    sql = """SELECT
                 id,  
                 para_name,
                 para_value,                 
                 para_desc,
                 CASE a.para_status WHEN '1' THEN '启用' WHEN '0' THEN '禁用' END  AS  flag
            FROM t_db_inst_para a
            {0}
            order by a.para_name,a.id
          """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def save_db_inst_para(p_index):
    result = {}
    val=check_db_inst_para(p_index)
    if val['code']=='-1':
        return val
    try:
        db      = get_connection()
        cr      = db.cursor()
        result  = {}
        sql="""insert into t_db_inst_para(para_name,para_value,para_desc,para_status) values('{0}','{1}','{2}','{3}')
            """.format(p_index['para_name'],
                       p_index['para_value'],
                       p_index['para_desc'],
                       p_index['para_status']
                     )
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result['code']='0'
        result['message']='保存成功！'
        return result
    except:
        e_str = exception_info()
        print(e_str)
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result

def upd_db_inst_para(p_para):
    result={}
    # val = check_db_inst_para(p_para)
    # if  val['code'] == '-1':
    #     return val
    try:
        db   = get_connection()
        cr   = db.cursor()

        sql="""update t_db_inst_para  set  
                      para_name           ='{0}',
                      para_value          ='{1}',
                      para_desc           ='{2}', 
                      para_status         ='{3}'
                where id='{4}'
            """.format(p_para['para_name'],
                       p_para['para_value'],
                       p_para['para_desc'],
                       p_para['para_status'],
                       p_para['para_id']
                      )
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='更新成功！'
    except :
        print(traceback.format_exc())
        result['code'] = '-1'
        if traceback.format_exc().count('Duplicate')>0:
           result['message'] = '更新失败(违反唯一键)！'
        else:
           result['message'] = '更新失败'
    return result

def del_db_inst_para(p_para_name):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        sql="delete from t_db_inst_para  where para_name='{0}'".format(p_para_name)
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='删除成功！'
    except :
        result['code'] = '-1'
        result['message'] = '删除失败！'
    return result

'''
  操作日志查询
'''

def query_db_inst_log(p_log_name):
    db = get_connection()
    cr = db.cursor()
    v_where=' '
    if p_log_name != '':
        v_where = " where a.statement like '%{0}%' or a.db like '%{1}%'".format(p_log_name,p_log_name)

    sql = """SELECT
                 a.id,  
                 b.name,
                 c.inst_name,                 
                 a.db,
                 DATE_FORMAT(a.start_time,'%Y-%m-%d %H:%i:%s') AS start_time,
                 DATE_FORMAT(a.end_time,'%Y-%m-%d %H:%i:%s') AS end_time,
                 d.dmmc as status,
                 a.statement,
                 a.message
            FROM t_db_inst_opt_log a,t_user b,t_db_inst c,t_dmmx d
            WHERE a.user_id=b.id
              AND a.inst_id=c.id
              AND a.status=d.dmm
              AND d.dm='28' 
               {0}
            ORDER BY a.start_time desc ,a.db,a.id
          """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list