#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : ma.fei
# @File    : t_user.py
# @Software: PyCharm

import json
import os
import re
import traceback

import pymysql

from web.model.t_sql_check import get_audit_rule
from web.utils.common import aes_encrypt, aes_decrypt, get_connection_ds_read_limit, get_connection_ds_sqlserver
from web.utils.common import exception_info_mysql, exception_info_sqlserver, format_mysql_error, format_sqlserver_error
from web.utils.common import format_sql
from web.utils.mysql_async import async_processer

'''
  数据库管理-新建实例
'''


async def query_inst_list():
    sql = "SELECT  a.id,a.inst_name FROM  t_db_inst a  order by a.created_date"
    return await async_processer.query_list(sql)


async def query_inst(inst_name):
    v_where = ''
    if inst_name != '':
        v_where = "  where a.inst_name like '%{0}%' ".format(inst_name)

    sql = """SELECT  
                 a.id,a.inst_name,
                 CASE WHEN a.is_rds='Y' THEN
                   concat(substr(a.inst_ip,1,20),'...')
                 ELSE
                   (SELECT server_ip FROM t_server b WHERE b.id=a.server_id) 
                 END AS  inst_ip,   
                 a.inst_port,a.inst_type,
                 (SELECT dmmc FROM t_dmmx X WHERE x.dm='02' AND x.dmm=a.inst_type) AS inst_type_name,
                 a.inst_env,
                 (SELECT dmmc FROM t_dmmx X WHERE x.dm='03' AND x.dmm=a.inst_env) AS inst_env_name,
                 a.inst_status,
                 (SELECT dmmc FROM t_dmmx X WHERE x.dm='32' AND x.dmm=a.inst_status) AS inst_status_name,
                 (SELECT dmmc FROM t_dmmx X WHERE x.dm='27' AND x.dmm=a.inst_ver) AS inst_ver_name,
                 CASE is_rds WHEN 'Y' THEN '是'  WHEN 'N' THEN '否' END  STATUS,
                 a.inst_reboot_flag,DATE_FORMAT(a.created_date,'%Y-%m-%d %h:%i:%s')  AS created_date
            FROM  t_db_inst a  {0}  order by a.inst_name """.format(v_where)
    return await async_processer.query_list(sql)


async def query_inst_by_id(p_inst_id):
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
    rs = await async_processer.query_dict_one(sql)
    rs['mgr_pass'] = await aes_decrypt(rs['mgr_pass'], rs['mgr_user'])
    return rs


async def get_ds_by_instid(p_inst_id):
    sql = """SELECT a.id  as dsid,
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
             FROM t_db_inst a  WHERE  a.id='{0}'""".format(p_inst_id)
    rs = await async_processer.query_dict_one(sql)
    rs['password'] = await aes_decrypt(rs['password'], rs['user'])
    return rs


async def get_inst_id():
    rs = await async_processer.query_one('select max(id)+1 from t_db_inst for update')
    return rs[0]


async def save_db_inst(d_inst):
    val = await check_db_inst(d_inst, 'add')
    if val['code'] == '-1':
        return val
    try:
        inst_id = await get_inst_id()
        if d_inst['mgr_pass'] != '':
            inst_pass = aes_encrypt(d_inst['mgr_pass'], d_inst['mgr_user'])
        else:
            inst_pass = d_inst['mgr_pass']

        sql = """insert into t_db_inst(id,inst_name,server_id,templete_id,inst_ip,inst_port,
                                     inst_type,inst_env,inst_ver,mgr_user,mgr_pass,created_date,
                                     api_server,python3_home,script_path,script_file)
                           values('{0}','{1}','{2}','{3}','{4}','{5}',
                                  '{6}','{7}','{8}','{9}','{10}',now(),
                                 '{11}','{12}','{13}','{14}')
            """.format(inst_id, d_inst['inst_name'], d_inst['server_id'], d_inst['templete_id'], d_inst['inst_ip'],
                       d_inst['inst_port'],
                       d_inst['inst_type'], d_inst['inst_env'], d_inst['inst_ver'], d_inst['mgr_user'], inst_pass,
                       d_inst['api_server'], d_inst['python3_home'], d_inst['script_path'], d_inst['script_file'])
        await async_processer.exec_sql(sql)
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
              """.format(inst_id, inst_id, inst_id)
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '保存成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '保存失败!'}


async def upd_db_inst(d_inst):
    val = await check_db_inst(d_inst, 'upd')
    if val['code'] == '-1':
        return val
    try:
        if d_inst['mgr_pass'] != '':
            inst_pass = await aes_encrypt(d_inst['mgr_pass'], d_inst['mgr_user'])
        else:
            inst_pass = d_inst['mgr_pass']

        sql = """update t_db_inst
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
                where id={16}""".format(d_inst['inst_name'], d_inst['server_id'], d_inst['inst_ip'],
                                        d_inst['templete_id'], d_inst['inst_port'], d_inst['inst_type'],
                                        d_inst['inst_env'], d_inst['inst_ver'], d_inst['is_rds'],
                                        d_inst['mgr_user'], inst_pass, d_inst['api_server'],
                                        d_inst['python3_home'], d_inst['script_path'], d_inst['script_file'],
                                        d_inst['inst_mapping_port'], d_inst['inst_id'])
        await async_processer.exec_sql(sql)
        # update inst config
        sql = """delete from t_db_inst_parameter where inst_id={}""".format(d_inst['inst_id'])
        await async_processer.exec_sql(sql)

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
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '更新成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '更新失败!'}


async def del_db_inst(p_instid):
    try:
        await async_processer.exec_sql("delete from t_db_inst  where id='{0}'".format(p_instid))
        return {'code': '0', 'message': '删除成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '删除失败!'}


def create_db_inst(p_api, p_instid):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '实例正在创建中，详见日志...'
        v_cmd = "curl -XPOST {0}/create_db_inst -d 'inst_id={1}'".format(p_api, p_instid)
        print('create_db_inst=', v_cmd)
        r = os.popen(v_cmd).read()
        d = json.loads(r)
        if d['code'] == 200:
            return result
        else:
            result['code'] = '-1'
            result['message'] = '{0}!'.format(d['msg'])
            return result
    except Exception as e:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '实例创建失败，详见错误日志!'
        return result


def push_db_inst(p_api, p_instid):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '脚本正在推送中，详见日志...'
        v_cmd = "curl -XPOST {0}/push_db_inst -d 'inst_id={1}'".format(p_api, p_instid)
        print('push_db_inst=', v_cmd)
        r = os.popen(v_cmd).read()
        d = json.loads(r)
        if d['code'] == 200:
            return result
        else:
            result['code'] = '-1'
            result['message'] = '{0}!'.format(d['msg'])
            return result
    except Exception as e:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '实例推送失败，详见错误日志!'
        return result


def destroy_db_inst(p_api, p_instid):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '实例正在销毁中，详见日志...'
        v_cmd = "curl -XPOST {0}/destroy_db_inst -d 'inst_id={1}'".format(p_api, p_instid)
        print('destroy_db_inst=', v_cmd)
        r = os.popen(v_cmd).read()
        d = json.loads(r)
        if d['code'] == 200:
            return result
        else:
            result['code'] = '-1'
            result['message'] = '{0}!'.format(d['msg'])
            return result
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '实例销毁失败，详见错误日志!'
        return result


def manager_db_inst(p_api, p_instid, p_op_type):
    try:
        if p_op_type == 'start':
            message = '实例已启动'
        elif p_op_type == 'stop':
            message = '实例已停止'
        elif p_op_type == 'restart':
            message = '实例已重启完成'
        elif p_op_type == 'autostart':
            message = '自启动已配置完成'
        elif p_op_type == 'cancel_autostart':
            message = '已取消实例自重启'
        else:
            message = ''
        v_cmd = "curl -XPOST {0}/manager_db_inst -d 'inst_id={1}&op_type={2}'".format(p_api, p_instid, p_op_type)
        r = os.popen(v_cmd).read()
        d = json.loads(r)
        if d['code'] == 200:
            return {'code': '0', 'message': message}
        else:
            return {'code': '-1', 'message': '{0}!'.format(d['msg'])}
    except Exception as e:
        traceback.print_exc()
        return {'code': '-1', 'message': '操作时发生错误，详见服务日志!'}


async def log_db_inst(p_instid):
    try:
        log = ''
        sql = """SELECT  concat(DATE_FORMAT(create_date,'%Y-%m-%d %H:%i:%s'),' => ', a.message) AS log
                   FROM t_db_inst_log a  WHERE  a.inst_id='{0}'  ORDER BY a.create_date""".format(p_instid)
        for r in await async_processer.query_dict_list(sql):
            log = log + r['log'] + '\n'
        return {'code': '0', 'message': log[0:-1]}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '获取日志失败!'}


async def check_inst_rep(d_inst):
    sql = "select count(0) from t_db_inst  where  server_id='{0}' and inst_port='{1}'".format(d_inst['server_id'],
                                                                                              d_inst['inst_port'])
    # if d_inst['is_rds'] == 'N':
    #     sql = "select count(0) from t_db_inst  where  server_id='{0}' and inst_port='{1}'".format(d_inst['server_id'],d_inst['inst_port'])
    # else:
    #     sql = "select count(0) from t_db_inst  where  inst_ip='{0}' and inst_port='{1}'".format(d_inst['inst_ip'], d_inst['inst_port'])
    rs = await async_processer.query_one(sql)
    return rs[0]


'''
  数据库管理-实例管理
'''


async def get_tree_by_instid(instid, msg):
    # try:
    #     v_html = ""
    #     p_ds   = await get_ds_by_instid(instid)
    #     rs1 = await async_processer.query_list_by_ds(p_ds,"SELECT schema_name FROM information_schema.SCHEMATA order by 1")
    #     for i in range(len(rs1)):
    #         rs2 = await async_processer.query_list_by_ds(p_ds,"SELECT table_name FROM information_schema.tables WHERE table_schema='{0}' order by 1".format(rs1[i][0]))
    #         v_node = """<li><span class="folder">{0}</span><ul>""".format(rs1[i][0])
    #         v_html=v_html+v_node
    #         for j in range(len(rs2)):
    #             v_node = """<li><span class="file">{0}<div style="display:none">{1}</div></span></li>""".format(rs2[j][0],rs2[j][0])
    #             v_html = v_html + "\n" + v_node;
    #         v_html=v_html+"\n"+"</ul></li>"+"\n"
    #     return {'code': '0', 'message': v_html,'desc':p_ds['db_desc'],'db_url':p_ds['db_desc']}
    # except Exception as e:
    #     traceback.print_exc()
    #     return {'code': '-1', 'message': '加载失败!','dbsc':'','db_url':''}

    try:
        result = {}
        p_ds = await get_ds_by_instid(instid)
        sql1 = "SELECT schema_name FROM information_schema.SCHEMATA where instr(schema_name,'{}')>0 order by 1".format(
            msg.lower())
        sql2 = "SELECT table_name FROM information_schema.tables WHERE table_schema='{0}' order by 1"
        n_tree = []
        rs1 = await async_processer.query_dict_list_by_ds(p_ds, sql1)
        print('rs1=', rs1)
        for db in rs1:
            n_parent = {
                'id': db['schema_name'],
                'text': db['schema_name'],
                'icon': 'mdi mdi-database',
            }
            rs2 = await async_processer.query_dict_list_by_ds(p_ds, sql2.format(db['schema_name']))

            n_nodes = []
            for tab in rs2:
                n_child = {
                    'id': tab['table_name'],
                    'text': tab['table_name'],
                    'icon': 'mdi mdi-table-large',
                }
                n_nodes.append(n_child)
            n_parent['nodes'] = n_nodes
            n_tree.append(n_parent)

        if p_ds['db_type'] == '0':
            db_url = 'MySQL://{}:{}/{}'.format(p_ds['ip'], p_ds['port'], p_ds['service'])
        elif p_ds['db_type'] == '1':
            db_url = 'Oracle://{}:{}'.format(p_ds['ip'], p_ds['port'])
        elif p_ds['db_type'] == '2':
            db_url = 'SQLServer://{}:{}'.format(p_ds['ip'], p_ds['port'])
        else:
            db_url = ''

        result['code'] = '0'
        result['message'] = n_tree
        result['desc'] = p_ds['db_desc']
        result['db_url'] = db_url

    except Exception as e:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '加载失败！'
        result['desc'] = ''
        result['db_url'] = ''
    return result


async def get_tree_by_instid_mssql(instid):
    try:
        v_html = ""
        p_ds = await get_ds_by_instid(instid)
        db = get_connection_ds_sqlserver(p_ds)
        cr = db.cursor()
        if p_ds['service'] == '':
            sql1 = """ SELECT name FROM Master..SysDatabases  ORDER BY Name"""
        else:
            sql1 = """ SELECT name FROM Master..SysDatabases where name= DB_NAME() ORDER BY Name"""

        sql2 = """SELECT OBJECT_SCHEMA_NAME(id)+'.'+Name FROM SysObjects Where XType='U' ORDER BY Name"""
        cr.execute(sql1)
        rs1 = cr.fetchall()
        for i in range(len(rs1)):
            cr.execute('use {}'.format(rs1[i][0]))
            cr.execute(sql2.format(rs1[i][0]))
            rs2 = cr.fetchall()
            v_node = """<li><span class="folder">{0}</span><ul>""".format(rs1[i][0])
            v_html = v_html + v_node
            for j in range(len(rs2)):
                v_node = """<li><span class="file">{0}<div style="display:none">{1}</div></span></li>""".format(
                    rs2[j][0], rs2[j][0])
                v_html = v_html + "\n" + v_node;
            v_html = v_html + "\n" + "</ul></li>" + "\n"
        cr.close()
        return {'code': '0', 'message': v_html, 'dbsc': p_ds['db_desc'], 'db_url': p_ds['db_desc']}
    except Exception as e:
        traceback.print_exc()
        return {'code': '-1', 'message': '加载失败!', 'dbsc': '', 'db_url': ''}


async def get_tab_ddl_by_instid(instid, tab, cur_db):
    try:
        p_ds = await get_ds_by_instid(instid)
        p_ds['service'] = cur_db
        rs = await async_processer.query_one_by_ds(p_ds, """show create table {0}""".format(tab))
        return {'code': '0', 'message': rs[1]}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '获取表定义失败!'}


async def drop_tab_by_instid(instid, tab, cur_db):
    try:
        p_ds = await get_ds_by_instid(instid)
        p_ds['service'] = cur_db
        await async_processer.exec_sql_by_ds(p_ds, """drop table {0}""".format(tab))
        return {'code': '0', 'message': '删除成功!'}
    except Exception as e:
        traceback.print_exc()
        return {'code': '-1', 'message': '删除失败!'}


async def get_idx_ddl_by_instid(instid, tab, cur_db):
    try:
        p_ds = await get_ds_by_instid(instid)
        p_ds['service'] = cur_db
        sql = '''SHOW INDEXES FROM {0}'''.format(tab)
        v_idx_sql = ''
        v_idx_pks = ''
        for i in await async_processer.query_list_by_ds(p_ds, sql):
            v_idx_name = i[2]
            v_idx_type = i[10]
            v_idx_cols = i[4]
            if v_idx_name == 'PRIMARY':
                v_idx_pks = v_idx_pks + v_idx_cols + ','
            else:
                v_idx_sql = v_idx_sql + 'create index {0} on {1}({2}) using {3}'.format(v_idx_name, tab, v_idx_cols,
                                                                                        v_idx_type) + ';\n'
        if v_idx_pks != '':
            v_idx_sql = 'alter table {0} add primary key({1});\n'.format(tab, v_idx_pks[0:-1]) + v_idx_sql[0:-1]
        return {'code': '0', 'message': v_idx_sql}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '未找到索引定义!'}


async def get_dss_for_inst(p_inst_id):
    sql = """select cast(id as char) as id,a.inst_name as name from t_db_inst a where id={}""".format(p_inst_id)
    return await async_processer.query_list(sql)


async def check_db_inst(p_inst, p_flag):
    result = {}

    if p_inst["inst_name"] == "":
        result['code'] = '-1'
        result['message'] = '实例名不能为空!'
        return result

    if p_inst["server_id"] == "" and p_inst["is_rds"] == 'N':
        result['code'] = '-1'
        result['message'] = '数据库服务器不能为空!'
        return result

    if p_inst["inst_ip"] == "" and p_inst["is_rds"] == 'Y':
        result['code'] = '-1'
        result['message'] = '数据库地址不能为空!'
        return result

    if p_inst["inst_port"] == "":
        result['code'] = '-1'
        result['message'] = '实例端口不能为空!'
        return result

    if p_inst["inst_type"] == "":
        result['code'] = '-1'
        result['message'] = '实例类型不能为空!'
        return result
    if p_flag == 'add':
        if await check_inst_rep(p_inst) > 0:
            result['code'] = '-1'
            result['message'] = '端口号重复!'
            return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result


def check_sql(p_instid, p_sql, curdb):
    result = {}
    result['status'] = '0'
    result['msg'] = ''
    result['data'] = ''
    result['column'] = ''

    if p_instid == '':
        result['status'] = '1'
        result['msg'] = '请选择数据源!'
        result['data'] = ''
        result['column'] = ''
        return result

    if p_sql == '':
        result['status'] = '1'
        result['msg'] = '请选中查询语句!'
        result['data'] = ''
        result['column'] = ''
        return result

    if p_sql.find('.') == -1 and curdb == '':
        result['status'] = '1'
        result['msg'] = '请选择数据库!'
        result['data'] = ''
        result['column'] = ''
        return result

    return result


async def get_mysql_result(p_ds, p_sql, curdb):
    result = {}
    columns = []
    data = []
    p_env = ''

    # get read timeout
    read_timeout = int((await get_audit_rule('switch_timeout'))['rule_value'])

    p_ds['service'] = curdb
    db = get_connection_ds_read_limit(p_ds, read_timeout)
    cr = db.cursor()
    try:
        cr.execute(p_sql)
        rs = cr.fetchall()
        # get sensitive column
        c_sensitive = (await get_audit_rule('switch_sensitive_columns'))['rule_value'].split(',')
        # process desc
        i_sensitive = []
        desc = cr.description
        for i in range(len(desc)):
            if desc[i][0] in c_sensitive:
                i_sensitive.append(i)
            columns.append({"title": desc[i][0]})

        # check sql rwos
        rule = await get_audit_rule('switch_query_rows')
        if len(rs) > int(rule['rule_value']):
            result['status'] = '1'
            result['msg'] = rule['error'].format(rule['rule_value'])
            result['data'] = ''
            result['column'] = ''
            return result

        # process data
        for i in rs:
            tmp = []
            for j in range(len(desc)):
                if i[j] is None:
                    tmp.append('')
                else:
                    if j in i_sensitive:
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
        err = traceback.format_exc()
        print('get_mysql_result=', err)
        if err.find('timed out') > 0:
            rule = get_audit_rule('switch_timeout')
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
        print('get_mysql_result=', traceback.format_exc())
        result['status'] = '1'
        result['msg'] = format_mysql_error(p_env, exception_info_mysql())
        result['data'] = ''
        result['column'] = ''
        return result


async def write_mysql_opr_log(p_userid, p_instid, p_sql, curdb):
    st = '''insert into t_db_inst_opt_log(user_id,inst_id,db,statement,status) values('{}','{}','{}','{}','{}')
         '''.format(p_userid, p_instid, curdb, format_sql(p_sql), '1')
    await async_processer.exec_sql(st)
    return {'status': '2', 'msg': '发布成功!', 'data': '', 'column': ''}


def get_sqlserver_result(p_ds, p_sql, p_curdb):
    result = {}
    columns = []
    data = []
    p_env = ''
    if p_ds['db_env'] == '1':
        p_env = 'PROD'
    if p_ds['db_env'] == '2':
        p_env = 'DEV'

    try:
        db = get_connection_ds_sqlserver(p_ds)
        cr = db.cursor()
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
        result['msg'] = format_sqlserver_error(p_env, exception_info_sqlserver())
        result['data'] = ''
        result['column'] = ''
        return result


async def exe_query(p_userid, p_instid, p_sql, curdb):
    result = {}

    # 查询校验
    val = check_sql(p_instid, p_sql, curdb)
    if val['status'] != '0':
        return val

    p_ds = await get_ds_by_instid(p_instid)

    # mysql
    if p_ds['db_type'] == '0':
        if len(re.findall(r'^select', p_sql.strip().lower(), re.M)) > 0 or len(
                re.findall(r'^show', p_sql.strip().lower(), re.M)) > 0:
            result = await get_mysql_result(p_ds, p_sql, curdb)
        else:
            result = await write_mysql_opr_log(p_userid, p_instid, p_sql, curdb)

    # sqlserver
    if p_ds['db_type'] == '2':
        result = get_sqlserver_result(p_ds, p_sql, curdb)

    return result


'''
  数据库管理-参数管理
'''


async def check_db_pass_rep(p_para):
    sql = "select count(0) from t_db_inst_para  where  para_name='{0}'".format(p_para['para_name'])
    rs = await async_processer.query_one(sql)
    return rs[0]


def check_db_inst_para(p_para):
    result = {}
    if p_para["para_name"] == "":
        result['code'] = '-1'
        result['message'] = '参数名不能为空！'
        return result

    if p_para["para_value"] == "":
        result['code'] = '-1'
        result['message'] = '参数值不能为空！'
        return result

    if p_para["para_desc"] == "":
        result['code'] = '-1'
        result['message'] = '参数描述不能为空！'
        return result

    if p_para["para_status"] == "":
        result['code'] = '-1'
        result['message'] = '参数状态不能为空！'
        return result

    if check_db_pass_rep(p_para) > 0:
        result['code'] = '-1'
        result['message'] = '参数名不能重复!'
        return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result


async def query_db_inst_para(para_code):
    v_where = ' '
    if para_code != '':
        v_where = " where a.para_code like '%{0}%' or a.para_code like '%{1}%'".format(para_code, para_code)
    sql = """SELECT
                 id,para_name,para_value,para_desc,CASE a.para_status WHEN '1' THEN '启用' WHEN '0' THEN '禁用' END  AS  flag
            FROM t_db_inst_para a {0} order by a.para_name,a.id""".format(v_where)
    return await async_processer.query_list(sql)


async def save_db_inst_para(p_index):
    val = check_db_inst_para(p_index)
    if val['code'] == '-1':
        return val
    try:
        sql = """insert into t_db_inst_para(para_name,para_value,para_desc,para_status) values('{0}','{1}','{2}','{3}')
            """.format(p_index['para_name'], p_index['para_value'], p_index['para_desc'], p_index['para_status'])
        await async_processer.exec_sql_by_ds(sql)
        return {'code': '0', 'message': '保存成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '保存失败!'}


async def upd_db_inst_para(p_para):
    try:
        sql = """update t_db_inst_para 
                 set  para_name ='{0}', para_value='{1}', para_desc ='{2}', para_status ='{3}' where id='{4}'
            """.format(p_para['para_name'], p_para['para_value'], p_para['para_desc'], p_para['para_status'],
                       p_para['para_id'])
        await async_processer.exec_sql_by_ds(sql)
        return {'code': '0', 'message': '更新成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '更新失败!'}


async def del_db_inst_para(p_para_name):
    try:
        sql = "delete from t_db_inst_para  where para_name='{0}'".format(p_para_name)
        await async_processer.exec_sql_by_ds(sql)
        return {'code': '0', 'message': '删除成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '删除失败!'}


'''
  操作日志查询
'''


async def query_db_inst_log(p_log_name):
    v_where = ' '
    if p_log_name != '':
        v_where = " where a.statement like '%{0}%' or a.db like '%{1}%'".format(p_log_name, p_log_name)
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
              AND d.dm='28' {0} ORDER BY a.start_time desc ,a.db,a.id""".format(v_where)
    return await async_processer.query_list(sql)


async def query_db_config(p_inst_env, p_inst_id):
    v_where = ''
    if p_inst_id != '':
        v_where = v_where + " and  a.inst_id= '{0}'".format(p_inst_id)
    if p_inst_env != '':
        v_where = v_where + " and  b.inst_env= '{0}'".format(p_inst_env)
    sql = """SELECT 
                  a.id as para_id,
                  SUBSTR(a.value,1,INSTR(a.value,'=')-1) AS para_name,
                  SUBSTR(a.VALUE,INSTR(a.value,'=')+1) AS para_val,
                  a.type AS para_type,
                  a.name AS para_desc,
                  DATE_FORMAT(a.create_date,'%Y-%m-%d %h:%i:%s')  AS create_date
            FROM `t_db_inst_parameter` a ,t_db_inst b
              WHERE a.inst_id = b.id 
                 and SUBSTR(a.value,1,INSTR(a.value,'=')-1) 
                    NOT IN('basedir','port','socket','log-error','pid-file','datadir')
              {}
          """.format(v_where)
    return await async_processer.query_list(sql)


async def update_db_config(d_db_para):
    val = check_db_para(d_db_para)
    if val['code'] == '-1':
        return val
    try:
        sql = """update t_db_inst_parameter set value='{}={}',last_update_date=now() where id={}""".format(
            d_db_para['para_name'], d_db_para['para_val'], d_db_para['para_id'])
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '更新成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '更新失败!'}


def check_db_para(p_db_para):
    result = {}
    if p_db_para["para_val"] == "":
        result['code'] = '-1'
        result['message'] = '参数值不能为空!'
        return result
    result['code'] = '0'
    result['message'] = '验证通过'
    return result
