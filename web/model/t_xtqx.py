#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/1 7:14
# @Author  : ma.fei
# @File    : t_xtqx.py
# @Software: PyCharm

import traceback
from web.utils.common import current_rq, get_connection_ds_sqlserver, get_connection_ds_ck
from web.model.t_user      import get_user_by_loginame,get_user_by_userid,get_user_by_userid_sync
from web.model.t_ds import get_ds_by_dsid, get_dss_sql_query_grants
from web.model.t_sql import get_mysql_proxy_result_dict, get_sqlserver_proxy_result_dict, get_mysql_proxy_result, \
    get_ck_proxy_result_dict
from web.utils.mongo_query import mongo_client
from web.utils.mysql_async import async_processer
from web.utils.mysql_sync import  sync_processer

async def upd_menu(p_menu):
    try:
        menuid       = p_menu['menuid']
        name         = p_menu['name']
        status       = p_menu['status']
        url          = p_menu['url']
        parent_id    = p_menu['parent_id']
        sql="""update t_xtqx 
                  set  name      ='{0}',                      
                       status    ='{1}' ,
                       url       ='{2}' ,
                       parent_id ='{3}',
                       last_update_date ='{4}' ,
                       updator='{5}'
                where id='{6}'""".format(name,status,url,parent_id,current_rq(),'DBA',menuid)
        await async_processer.exec_sql(sql)
        res = {}
        res['code']='0'
        res['message']='更新成功!'
        return res
    except :
        res = {}
        res['code'] = '-1'
        res['message'] = '更新失败!'
        return res

async def upd_func(p_func):
    try:
        funcid       = p_func['funcid']
        func_name    = p_func['func_name']
        func_url     = p_func['func_url']
        priv_id      = p_func['priv_id']
        status       = p_func['status']
        sql="""update t_func 
                  set  func_name  ='{0}',       
                       func_url   ='{1}' ,    
                       priv_id    ='{2}' ,        
                       status     ='{3}' ,                  
                       last_update_date ='{4}' ,
                       updator='{5}'
                where id='{6}'""".format(func_name,func_url,priv_id,status,current_rq(),'DBA',funcid)
        await async_processer.exec_sql(sql)
        res = {}
        res['code']='0'
        res['message']='更新成功!'
        return res
    except :
        res = {}
        res['code'] = '-1'
        res['message'] = '更新失败!'
        return res

async def get_child_count(menuid):
    sql="select count(0) from t_xtqx  where parent_id='{0}'".format(menuid)
    rs = await async_processer.query_one(sql)
    return rs[0]

async def del_menu(menuid):
    try:
        res = {}
        if await get_child_count(menuid)>0:
            res['code'] = '-1'
            res['message'] = '父菜单下有子菜单，不能删除!'
            return res
        await async_processer.exec_sql("delete from t_xtqx  where id='{0}'".format(menuid))
        res['code']='0'
        res['message']='删除成功！'
        return res
    except :
        res = {}
        res['code'] = '-1'
        res['message'] = '删除失败！'
        return res

async def del_func(funcid):
    try:
        await async_processer.exec_sql("delete from t_func  where id='{0}'".format(funcid))
        res={}
        res['code']='0'
        res['message']='删除成功!'
        return res
    except :
        res = {}
        res['code'] = '-1'
        res['message'] = '删除失败!'
        return res

async def get_menu_by_menuid(p_menuid):
    sql="select id as menuid,name,status,url,parent_id,creation_date,creator,last_update_date,updator from t_xtqx where id={0}".format(p_menuid)
    return await async_processer.query_dict_one(sql)

async def get_func_by_funcid(p_funcid):
    sql="select id as funcid,func_name,func_url,priv_id,status from t_func where id={0}".format(p_funcid)
    return await async_processer.query_dict_one(sql)

async def get_url_by_userid(p_userid):
    sql ="""SELECT url
             FROM t_xtqx
              WHERE STATUS='1'
                 AND id IN(SELECT b.priv_id
                   FROM t_user_role a ,t_role_privs b
                   WHERE a.role_id=b.role_id
                     AND a.user_id='{0}')
            UNION
            SELECT func_url
              FROM t_func
                   WHERE STATUS='1'
                 AND id IN(SELECT b.func_id
                       FROM t_user_role a ,t_role_func_privs b
                       WHERE a.role_id=b.role_id
                         AND a.user_id='{1}')
         """.format(p_userid,p_userid)
    rs = await async_processer.query_list(sql)
    uris = []
    for i in range(len(rs)):
        if rs[i][0] is not None:
            for j in rs[i][0].split(','):
               uris.append(j)
    return uris

def get_url_by_userid_sync(p_userid):
    sql ="""SELECT url
             FROM t_xtqx
              WHERE STATUS='1'
                 AND id IN(SELECT b.priv_id
                   FROM t_user_role a ,t_role_privs b
                   WHERE a.role_id=b.role_id
                     AND a.user_id='{0}')
            UNION
            SELECT func_url
              FROM t_func
                   WHERE STATUS='1'
                 AND id IN(SELECT b.func_id
                       FROM t_user_role a ,t_role_func_privs b
                       WHERE a.role_id=b.role_id
                         AND a.user_id='{1}')
         """.format(p_userid,p_userid)
    rs =  sync_processer.query_list(sql)
    uris = []
    for i in range(len(rs)):
        if rs[i][0] is not None:
            for j in rs[i][0].split(','):
               uris.append(j)
    return uris

async def check_url(userid,uri):
    uuri = await get_url_by_userid(userid)
    user = await get_user_by_userid(userid)
    if user['loginname'] =='admin':
       return True
    if uri not in uuri:
        return False
    else:
        return True

def check_url_sync(userid,uri):
    uuri =  get_url_by_userid_sync(userid)
    print('uuri=',uuri)
    user =  get_user_by_userid_sync(userid)
    if user['loginname'] =='admin':
       return True
    if uri not in uuri:
        return False
    else:
        return True

async def init_menu():
    sql = """SELECT   id,
                      CONCAT(REPEAT('&nbsp;',(LENGTH(id)-2)*8),NAME) AS NAME,
                      url,
                      CASE STATUS WHEN '1' THEN '是'  WHEN '0' THEN '否'  END  STATUS,
                      creator,DATE_FORMAT(creation_date,'%Y-%m-%d')    creation_date,
                      updator,DATE_FORMAT(last_update_date,'%Y-%m-%d') last_update_date           
            FROM t_xtqx 
             WHERE id<>'0' 
            ORDER BY id,NAME
          """
    return await async_processer.query_list(sql)

async def get_menuid(p_parent_id):
    sql="SELECT count(0),CAST(CONCAT('0',MAX(id)+1) AS CHAR) AS ID FROM t_xtqx WHERE parent_id='{0}'".format(p_parent_id)
    rs = await async_processer.query_one(sql)
    if rs[0]==0:
        return str(p_parent_id)+'01'
    else:
        return rs[1]

async def save_menu(p_menu):
    try:
        name      = p_menu['name']
        url       = p_menu['url']
        status    = p_menu['status']
        parent_id = p_menu['parent_id']
        menu_id   = await get_menuid(parent_id)
        sql="""insert into t_xtqx(id,name,url,status,parent_id,creation_date,creator,last_update_date,updator) 
                    values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')
            """.format(menu_id,name,url,status,parent_id,current_rq(),'DBA',current_rq(),'DBA')
        await async_processer.exec_sql(sql)
        res = {}
        res['code']='0'
        res['message']='保存成功！'
        return res
    except:
        traceback.print_exc()
        res = {}
        res['code'] = '-1'
        res['message'] = '保存失败！'
        return res

async def save_func(p_func):
    val = check_func(p_func)
    if val['code'] == '-1':
        return val
    try:
        sql="""insert into t_func(func_name,func_url,priv_id,status,creation_date,creator,last_update_date,updator) 
                    values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')
            """.format(p_func['func_name'],p_func['func_url'],p_func['priv_id'],p_func['status'],current_rq(),'DBA',current_rq(),'DBA')
        await async_processer.exec_sql(sql)
        res = {}
        res['code']='0'
        res['message']='保存成功！'
        return res
    except:
        res = {}
        traceback.print_exc()
        res['code'] = '-1'
        res['message'] = '保存失败！'
        return res

async def get_privs():
    sql="""select cast(a.id as char) as id,
                  CONCAT((SELECT NAME FROM t_xtqx b WHERE b.id=a.parent_id),'=>',NAME) AS NAME 
           from t_xtqx a where a.status='1' AND a.url !=''"""
    return await async_processer.query_list(sql)

async def get_func_privs():
    sql="""SELECT  id,func_name AS NAME FROM t_func a WHERE a.status='1' ORDER BY id"""
    return await async_processer.query_list(sql)

async def get_privs_sys(p_roleid):
    sql="""select cast(a.id as char) as id,
                  CONCAT((SELECT NAME FROM t_xtqx c WHERE c.id=a.parent_id),'=>',NAME) AS NAME  
           from t_xtqx a
           where a.status='1' AND a.url !=''
             and a.id not in(select priv_id from t_role_privs b where b.role_id='{0}')""".format(p_roleid)
    return await async_processer.query_list(sql)

async def get_privs_role(p_roleid):
    sql="""select cast(a.id as char) as id,
                  CONCAT((SELECT NAME FROM t_xtqx c WHERE c.id=a.parent_id),'=>',NAME) AS NAME  
           from t_xtqx a
            where a.status='1'  AND url !=''
              AND a.id in(select priv_id from t_role_privs b where b.role_id='{0}')""".format(p_roleid)
    return await async_processer.query_list(sql)

async def get_privs_func(p_roleid):
    sql="""SELECT  id,func_name AS NAME 
            FROM t_func a
            WHERE a.status='1'
            and a.id not in(select func_id from t_role_func_privs b where b.role_id='{0}')""".format(p_roleid)
    return await async_processer.query_list(sql)

async def get_privs_func_role(p_roleid):
    sql="""SELECT  id,func_name AS NAME FROM t_func a WHERE a.status='1'
            and a.id  in(select func_id from t_role_func_privs b where b.role_id='{0}')""".format(p_roleid)
    return await async_processer.query_list(sql)

async def get_parent_menus():
    sql="select cast(id as char) as id,name from t_xtqx where status='1' AND url ='' order by id"
    return await async_processer.query_list(sql)

async def get_tree_by_userid(p_username):
    try:
        result = {}
        v_html = ""
        d_user = await get_user_by_loginame(p_username)
        sql1   = """select id,name,icon
                     from t_xtqx 
                     where parent_id ='0' and status='1'
                      and  id in(select distinct parent_id from t_xtqx 
                                 where id in(select b.priv_id 
                                            from t_user_role a ,t_role_privs b,t_role c
                                             where a.role_id=b.role_id                                          
                                               and a.role_id=c.id and c.status='1'
                                               and a.user_id='{0}' )) order by id""".format(d_user['userid'])
        sql2 = """select id,name,url 
                    from t_xtqx 
                       where parent_id ='{0}' and status='1'
                         and id IN(select b.priv_id 
                                   from t_user_role a ,t_role_privs b,t_role c
                                   where a.role_id=b.role_id
                                     and a.role_id=c.id and c.status='1'
                                     and a.user_id='{1}')  order by id"""
        rs1 = await async_processer.query_list(sql1)
        v_menu_header="""
                      <li class="has_sub">
                         <a href="javascript:void(0);" class="waves-effect"><i class="{0}"></i><span>{1}</span> <span class="menu-arrow"></span></a>
                         <ul class="list-unstyled">
                      """
        v_menu_footer="""</ul>
                      </li>
                      """
        for i in range(len(rs1)):
            rs2 = await async_processer.query_list(sql2.format(rs1[i][0],d_user['userid']))
            v_node = v_menu_header.format(rs1[i][2],rs1[i][1])
            v_html = v_html+v_node
            for j in range(len(rs2)):
                v_node = """<li><a id="{0}^{1}" class="file" href="#">{2}</a></li>""".format(rs2[j][2][1:].replace('/','_'),rs2[j][2],rs2[j][1])
                v_html = v_html + "\n" + v_node;
            v_html=v_html+"\n"+v_menu_footer+"\n"
        result['code'] = '0'
        result['message'] = v_html
    except:
        result['code'] = '-1'
        result['message'] = '加载失败！'
    return result

async def get_tab_ddl_by_tname(dbid,tab,cur_db):
    try:
        res = {}
        pds = await get_ds_by_dsid(dbid)
        pds['service'] = cur_db
        sql    = """show create table {0}""".format(tab)
        rs = await async_processer.query_one_by_ds(pds,sql)
        res['code'] = '0'
        res['message'] = rs[1]
        return res
    except :
        res = {}
        traceback.print_exc()
        res['code'] = '-1'
        res['message'] = '获取表定义失败！'
        return res

async def get_db_name(dbid):
    res = {}
    pds = await get_ds_by_dsid(dbid)
    print('get_db_name=', pds)
    sql = """select schema_name FROM information_schema.`SCHEMATA` 
                where schema_name NOT IN('information_schema','mysql','performance_schema') order by schema_name"""
    try:
        res['code'] = '0'
        res['message'] = await async_processer.query_list_by_ds(pds,sql)
        return res
    except:
        try:
            print('from agent server:{} get db name!'.format(pds['proxy_server']))
            res = get_mysql_proxy_result(pds, sql, 'information_schema')
            res['code'] = '0'
            res['message'] = res['data']
            return res
        except:
            traceback.print_exc()
            return {'code':-1,'message':['获取数据库名失败!']}

async def get_tab_name(dbid,db_name):
    res = {}
    pds = await get_ds_by_dsid(dbid)
    sql = """SELECT table_name FROM information_schema.tables  
               WHERE table_schema='{0}' ORDER BY table_name""".format(db_name)
    try:
        res['code'] = '0'
        res['message'] = await async_processer.query_list_by_ds(pds,sql)
        return res
    except:
        try:
            print('from agent server:{} get table name!'.format(pds['proxy_server']))
            res = get_mysql_proxy_result(pds, sql, 'information_schema')
            res['code'] = '0'
            res['message'] = res['data']
            return res
        except:
            traceback.print_exc()
            return {'code': -1, 'message': ['获取表名失败!']}

async def get_tab_columns(dbid,db_name,tab_name):
    res = {}
    pds = await get_ds_by_dsid(dbid)
    sql = """SELECT column_name,column_comment 
                         FROM information_schema.columns
                        WHERE table_schema='{0}'  AND table_name='{1}'
                          ORDER BY ordinal_position""".format(db_name, tab_name)
    try:
        res['code'] = '0'
        res['message'] = await async_processer.query_list_by_ds(pds,sql)
        return res
    except:
        try:
            print('from agent server:{} get column name!'.format(pds['proxy_server']))
            res = get_mysql_proxy_result(pds, sql, 'information_schema')
            res['code'] = '0'
            res['message'] = res['data']
            return res
        except:
            traceback.print_exc()
            return {'code': -1, 'message': ['获取数据库列名失败!']}

async def get_tab_columns_by_query_grants(dbid,db_name,tab_name):
    res = {}
    pds = await get_ds_by_dsid(dbid)
    sql = """SELECT column_name 
                         FROM information_schema.columns
                        WHERE table_schema='{0}'  AND table_name='{1}'
                          ORDER BY ordinal_position""".format(db_name, tab_name)
    try:
        res['code'] = '0'
        res['message'] = await async_processer.query_list_by_ds(pds,sql)
        return res
    except:
        traceback.print_exc()
        return {'code': -1, 'message': ['获取数据库列名失败!']}

async def get_tab_keys(dbid,db_name,tab_name):
    res = {}
    pds = await get_ds_by_dsid(dbid)
    sql = """SELECT GROUP_CONCAT(column_name)
                        FROM information_schema.columns
                       WHERE table_schema='{0}'  AND table_name='{1}'
                          AND column_key='PRI'
                         ORDER BY ordinal_position""".format(db_name, tab_name)
    try:
        rs = await async_processer.query_one_by_ds(pds,sql)
        res['code'] = '0'
        res['message'] = rs[0]
        return res
    except:
        try:
            print('from agent server:{} get tab key!'.format(pds['proxy_server']))
            res = get_mysql_proxy_result(pds, sql, 'information_schema')
            res['code'] = '0'
            res['message'] = res['data']
            return res
        except:
            traceback.print_exc()
            return {'code': -1, 'message': ['获取数据库列名失败!']}

async def query_ds(dsid):
    try:
       return {"code":"0","message":await get_ds_by_dsid(dsid)}
    except Exception as e:
       traceback.print_exc()
       return {"code":"-1","message":"获取数据源信息失败!"}

async def get_dss_by_query_grants(userid):
    try:
       return {"code":"0","message":await get_dss_sql_query_grants(userid)}
    except Exception as e:
       traceback.print_exc()
       return {"code":"-1","message":"获取数据源信息失败!"}

async def get_tab_incr_col(dbid,db_name,tab_name):
    res = {}
    pds = await get_ds_by_dsid(dbid)
    sql = """SELECT column_name,column_comment 
                FROM information_schema.columns
                    WHERE table_schema='{0}'  AND table_name='{1}'
                        AND data_type IN('timestamp','datetime','date')
                            ORDER BY ordinal_position""".format(db_name, tab_name)
    try:
        res['code'] = '0'
        res['message'] = await async_processer.query_list_by_ds(pds,sql)
        return res
    except:
        try:
            print('from agent server:{} get tab incr column!'.format(pds['proxy_server']))
            res = get_mysql_proxy_result(pds, sql, 'information_schema')
            res['code'] = '0'
            res['message'] = res['data']
            return res
        except:
            traceback.print_exc()
            return {'code': -1, 'message': ['获取数据库增量列名失败!']}

async def get_tab_structure(dbid,db_name,tab_name):
    p_ds   = await get_ds_by_dsid(dbid)
    sql    = """SELECT c.column_name,
                       c.column_comment,
                       c.data_type,
                       CASE WHEN c.extra='auto_increment' THEN '自增' ELSE '' END AS col_incr,
                       CASE WHEN c.column_key='PRI' THEN '主键' ELSE '' END AS col_pk,
                       CASE WHEN c.is_nullable='NO' THEN '非空' ELSE '' END AS col_null      
                FROM information_schema.columns c
                WHERE c.table_schema='{0}'  
                  AND c.table_name='{1}'
                ORDER BY c.ordinal_position
             """.format(db_name,tab_name)
    return await async_processer.query_list_by_ds(p_ds,sql)

async def get_tab_idx_by_tname(dbid,tab):
    try:
        result = {}
        p_ds   = await get_ds_by_dsid(dbid)
        sql    = '''SHOW INDEXES FROM {0}'''.format(tab)
        rs     = await async_processer.query_list_by_ds(p_ds,sql)
        v_idx_sql = ''
        v_idx_pks = ''
        for i in rs:
            v_idx_name = i[2]
            v_idx_type = i[10]
            v_idx_cols = i[4]
            if v_idx_name=='PRIMARY':
               v_idx_pks=v_idx_pks+v_idx_cols+','
            else:
               v_idx_sql = v_idx_sql+ 'create index {0} on {1}({2}) using {3}'.format(v_idx_name,tab,v_idx_cols,v_idx_type)+';\n'
        if v_idx_pks!='':
           v_idx_sql =  'alter table {0} add primary key({1});\n'.format(tab,v_idx_pks[0:-1])+v_idx_sql[0:-1]
        result['code'] = '0'
        result['message'] = v_idx_sql
        print('rs=',rs,rs[1])
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '未找到索引定义!'
    return result

async def get_tab_idx_by_tname(dbid,tab,cur_db):
    try:
        result = {}
        p_ds   = await get_ds_by_dsid(dbid)
        p_ds['service'] = cur_db
        sql    = '''SHOW INDEXES FROM {0}'''.format(tab)
        rs = await async_processer.query_list_by_ds(p_ds, sql)
        v_idx_sql = ''
        v_idx_pks = ''
        for i in rs:
            v_idx_name = i[2]
            v_idx_type = i[10]
            v_idx_cols = i[4]
            if v_idx_name=='PRIMARY':
               v_idx_pks=v_idx_pks+v_idx_cols+','
            else:
               v_idx_sql = v_idx_sql+ 'create index {0} on {1}({2}) using {3}'.format(v_idx_name,tab,v_idx_cols,v_idx_type)+';\n'
        if v_idx_pks!='':
           v_idx_sql =  'alter table {0} add primary key({1});\n'.format(tab,v_idx_pks[0:-1])+v_idx_sql[0:-1]
        result['code'] = '0'
        result['message'] = v_idx_sql
    except :
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '未找到索引定义!'
    return result

async def get_tree_by_dbid(dbid,msg):
    try:
        result = {}
        p_ds   = await get_ds_by_dsid(dbid)
        sql1   = "SELECT schema_name FROM information_schema.SCHEMATA where instr(schema_name,'{}')>0 order by 1".format(msg.lower())
        sql2   = "SELECT table_name FROM information_schema.tables WHERE table_schema='{0}' order by 1"
        n_tree = []
        rs1    = await async_processer.query_dict_list_by_ds(p_ds,sql1)
        print('rs1=',rs1)
        for db in rs1:
            n_parent = {
                'id'  : db['schema_name'],
                'text': db['schema_name'],
                'icon': 'mdi mdi-database',
            }
            rs2 = await async_processer.query_dict_list_by_ds(p_ds,sql2.format(db['schema_name']))

            n_nodes = []
            for tab in rs2:
                n_child = {
                    'id'  : tab['table_name'],
                    'text': tab['table_name'],
                    'icon': 'mdi mdi-table-large',
                }
                n_nodes.append(n_child)
            n_parent['nodes']=n_nodes
            n_tree.append(n_parent)

        if p_ds['db_type'] =='0':
            db_url ='MySQL://{}:{}/{}'.format(p_ds['ip'],p_ds['port'],p_ds['service'] )
        elif p_ds['db_type'] == '1':
            db_url = 'Oracle://{}:{}'.format(p_ds['ip'], p_ds['port'])
        elif p_ds['db_type'] =='2':
            db_url = 'SQLServer://{}:{}'.format(p_ds['ip'], p_ds['port'])
        else:
            db_url =''

        result['code'] = '0'
        result['message'] = n_tree
        result['desc']    = p_ds['db_desc']
        result['db_url']  = db_url

    except Exception as e:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '加载失败！'
        result['desc'] = ''
        result['db_url'] = ''
    return result

async def get_tree_by_dbid_mongo(dbid):
    try:
        result = {}
        p_ds   = await get_ds_by_dsid(dbid)
        mongo = mongo_client(p_ds['ip'], p_ds['port'], auth_db='admin',db='admin', user= p_ds['user'], password=p_ds['password'])
        rs1 = mongo.get_databases()
        n_tree = []
        #print('rs1=',rs1)
        for db in rs1:
            n_parent = {
                'id'  : db,
                'text': db,
                'icon': 'mdi mdi-database',
            }
            rs2 = mongo.get_collections(db)

            n_nodes = []
            for tab in rs2:
                n_child = {
                    'id'  : tab,
                    'text': tab,
                    'icon': 'mdi mdi-table-large',
                }
                n_nodes.append(n_child)
            n_parent['nodes']=n_nodes
            n_tree.append(n_parent)

        if p_ds['db_type'] =='0':
            db_url ='MySQL://{}:{}/{}'.format(p_ds['ip'],p_ds['port'],p_ds['service'] )
        elif p_ds['db_type'] == '1':
            db_url = 'Oracle://{}:{}'.format(p_ds['ip'], p_ds['port'])
        elif p_ds['db_type'] =='2':
            db_url = 'SQLServer://{}:{}'.format(p_ds['ip'], p_ds['port'])
        elif p_ds['db_type'] == '6':
            db_url = 'Mongo://{}:{}'.format(p_ds['ip'], p_ds['port'])
        else:
            db_url =''

        result['code'] = '0'
        result['message'] = n_tree
        result['desc']    = p_ds['db_desc']
        result['db_url']  = db_url

    except Exception as e:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '加载失败！'
        result['desc'] = ''
        result['db_url'] = ''
    return result


def dataConvDict(desc,data):
    res = []
    for i in data:
        tmp = []
        for j in range(len(desc)):
            if i[j] is None:
                tmp.append('')
            else:
                tmp.append(str(i[j]))
            res.append(dict(zip([d[0] for d in desc], tmp)))
    return res

async def get_tree_by_dbid_ck(dbid):
    try:
        result = {}
        ds  = await get_ds_by_dsid(dbid)
        db  = get_connection_ds_ck(ds)
        cr  = db.cursor()
        st1 = "select name as schema_name from system.databases where name not in('information_schema','INFORMATION_SCHEMA','system','default') order by name"
        st2 = "select lower(name) as table_name from system.tables where database='{}' order by 1"
        n_tree = []
        cr.execute(st1)
        ds1 = cr.description
        rs1 = cr.fetchall()
        rs1 = dataConvDict(ds1,rs1)
        for db in rs1:
            n_parent = {
                'id'  : db['schema_name'],
                'text': db['schema_name'],
                'icon': 'mdi mdi-database',
            }
            cr.execute(st2.format(db['schema_name']))
            ds2 = cr.description
            rs2 = cr.fetchall()
            rs2 = dataConvDict(ds2, rs2)
            n_nodes = []
            for tab in rs2:
                n_child = {
                    'id'  : tab['table_name'],
                    'text': tab['table_name'],
                    'icon': 'mdi mdi-table-large',
                }
                n_nodes.append(n_child)
            n_parent['nodes']=n_nodes
            n_tree.append(n_parent)

        if ds['db_type'] =='0':
            db_url ='MySQL://{}:{}/{}'.format(ds['ip'],ds['port'],ds['service'] )
        elif ds['db_type'] == '1':
            db_url = 'Oracle://{}:{}'.format(ds['ip'], ds['port'])
        elif ds['db_type'] =='2':
            db_url = 'SQLServer://{}:{}'.format(ds['ip'], ds['port'])
        else:
            db_url =''

        result['code'] = '0'
        result['message'] = n_tree
        result['desc']    = ds['db_desc']
        result['db_url']  = db_url

    except Exception as e:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '加载失败！'
        result['desc'] = ''
        result['db_url'] = ''
    return result

async def get_tree_by_dbid_proxy(dbid):
    try:
        result = {}
        p_ds   = await get_ds_by_dsid(dbid)
        sql1   = "SELECT schema_name FROM information_schema.SCHEMATA order by 1"
        sql2   = "SELECT table_name  FROM information_schema.tables WHERE table_schema='{0}' order by 1"
        n_tree = []

        ret1   = get_mysql_proxy_result_dict(p_ds,sql1,p_ds['service'])
        if ret1['status'] == '1':
            result['code'] = '-1'
            result['message'] = '加载失败！'
            result['desc'] = ''
            result['db_url'] = ''
            return result

        rs1 = ret1['data']
        for db in rs1:
            n_parent = {
                'id': db['schema_name'],
                'text': db['schema_name'],
                'icon': 'mdi mdi-database',
            }
            ret2 = get_mysql_proxy_result_dict(p_ds, sql2.format(db['schema_name']), p_ds['service'])
            if ret1['status'] == '1':
                result['code'] = '-1'
                result['message'] = '加载失败！'
                result['desc'] = ''
                result['db_url'] = ''
                return result
            rs2 = ret2['data']

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

async def get_tree_by_dbid_ck_proxy(dbid):
    try:
        result = {}
        p_ds   = await get_ds_by_dsid(dbid)
        st1 = "select name as schema_name from system.databases where name not in('information_schema','INFORMATION_SCHEMA','system','default') order by name"
        st2 = "select lower(name) as table_name from system.tables where database='{0}' order by 1"
        n_tree = []
        ret1   = get_ck_proxy_result_dict(p_ds,st1,p_ds['service'])
        print('ret1=', ret1)
        if ret1['status'] == '1':
            result['code'] = '-1'
            result['message'] = '加载失败！'
            result['desc'] = ''
            result['db_url'] = ''
            return result

        rs1 = ret1['data']
        print('get_tree_by_dbid_ck_proxy=',rs1)

        for db in rs1:
            n_parent = {
                'id': db['schema_name'],
                'text': db['schema_name'],
                'icon': 'mdi mdi-database',
            }
            ret2 = get_ck_proxy_result_dict(p_ds, st2.format(db['schema_name']), p_ds['service'])
            print('ret2=', ret2)
            if ret1['status'] == '1':
                result['code'] = '-1'
                result['message'] = '加载失败！'
                result['desc'] = ''
                result['db_url'] = ''
                return result
            rs2 = ret2['data']

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

async def get_tree_by_dbid_mssql(dbid):
    try:
        result = {}
        p_ds = await get_ds_by_dsid(dbid)
        db   = get_connection_ds_sqlserver(p_ds)
        cr   = db.cursor(as_dict=True)

        if p_ds['service'] == '':
            sql1 = """ SELECT name as schema_name FROM Master..SysDatabases  ORDER BY Name"""
        else:
            sql1 = """ SELECT name as schema_name FROM Master..SysDatabases where name= DB_NAME() ORDER BY Name"""

        sql2 = """use [{}];SELECT OBJECT_SCHEMA_NAME(id)+'.'+Name as table_name  FROM SysObjects Where XType='U' order by name"""

        n_tree = []
        cr.execute(sql1)
        rs1 = cr.fetchall()
        for db in rs1:
            n_parent = {
                'id': db['schema_name'],
                'text': db['schema_name'],
                'icon': 'mdi mdi-database',
            }
            cr.execute(sql2.format(db['schema_name']))
            rs2 = cr.fetchall()
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
        cr.close()

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

async def get_tree_by_dbid_mssql_proxy(dbid):
    try:
        result = {}
        p_ds   = await get_ds_by_dsid(dbid)

        if p_ds['service'] == '':
            sql1 = """ SELECT name as schema_name FROM Master..SysDatabases  ORDER BY Name"""
        else:
            sql1 = """ SELECT name as schema_name FROM Master..SysDatabases where name= DB_NAME() ORDER BY Name"""

        sql2 = """use {};SELECT OBJECT_SCHEMA_NAME(id)+'.'+Name as table_name  FROM SysObjects Where XType='U' order by name"""
        n_tree = []

        ret1 = get_sqlserver_proxy_result_dict(p_ds, sql1, p_ds['service'])
        if ret1['status'] == '1':
            result['code'] = '-1'
            result['message'] = '加载失败！'
            result['desc'] = ''
            result['db_url'] = ''
            return result

        rs1 = ret1['data']
        for db in rs1:
            n_parent = {
                'id': db['schema_name'],
                'text': db['schema_name'],
                'icon': 'mdi mdi-database',
            }
            ret2 = get_sqlserver_proxy_result_dict(p_ds, sql2.format(db['schema_name']), p_ds['service'])
            print('ret2=', ret2)
            if ret1['status'] == '1':
                result['code'] = '-1'
                result['message'] = '加载失败！'
                result['desc'] = ''
                result['db_url'] = ''
                return result
            rs2 = ret2['data']

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

async def query_menu(p_name):
    if p_name == "":
        sql = """SELECT   id,
                      CONCAT(REPEAT('&nbsp;',(LENGTH(id)-2)*8),NAME) AS NAME,
                      url,
                      CASE STATUS WHEN '1' THEN '是'  WHEN '0' THEN '否'  END  STATUS,
                      creator,DATE_FORMAT(creation_date,'%Y-%m-%d')    creation_date,
                      updator,DATE_FORMAT(last_update_date,'%Y-%m-%d') last_update_date 
                 from t_xtqx
                 WHERE id<>'0' 
                 order by id,name""".format(p_name)
    else:
        sql = """SELECT   id,
                      CONCAT(REPEAT('&nbsp;',(LENGTH(id)-2)*8),NAME) AS NAME,
                      url,
                      CASE STATUS WHEN '1' THEN '是'  WHEN '0' THEN '否'  END  STATUS,
                      creator,DATE_FORMAT(creation_date,'%Y-%m-%d')    creation_date,
                      updator,DATE_FORMAT(last_update_date,'%Y-%m-%d') last_update_date 
                 from t_xtqx 
                where id<>'0' and ( binary name like '%{0}%' or ID like  '%{1}%')             
                 order by id,name""".format(p_name,p_name)
    return await async_processer.query_list(sql)

async def query_func(p_name):
    if p_name == "":
        sql = """SELECT   id,
                      func_name,
                      func_url,
                      CASE STATUS WHEN '1' THEN '是'  WHEN '0' THEN '否'  END  STATUS,
                      creator,DATE_FORMAT(creation_date,'%Y-%m-%d')    creation_date,
                      updator,DATE_FORMAT(last_update_date,'%Y-%m-%d') last_update_date 
                 from t_func              
                 order by id"""
    else:
        sql = """SELECT   id,
                      func_name,
                      func_url,
                      CASE STATUS WHEN '1' THEN '是'  WHEN '0' THEN '否'  END  STATUS,
                      creator,DATE_FORMAT(creation_date,'%Y-%m-%d')    creation_date,
                      updator,DATE_FORMAT(last_update_date,'%Y-%m-%d') last_update_date 
                 from t_func 
                where  ( binary func_name like '%{0}%' or func_url like  '%{1}%')             
                 order by id""".format(p_name,p_name)
    return await async_processer.query_list(sql)

async def if_exists_menu(p_name):
    sql="select count(0) from t_xtqx where upper(name)='{0}'".format(p_name.upper())
    rs = await async_processer.query_one(sql)
    if rs[0]==0:
        return False
    else:
        return True

def check_menu(p_menu):
    result = {}
    result['code'] = '0'
    result['message'] = '验证通过'

    if p_menu["name"]=="":
        result['code']='-1'
        result['message']='菜单名称不能为空！'
        return result

    if  if_exists_menu(p_menu["name"]):
        result['code'] = '-1'
        result['message'] = '菜单名称已存在！'
        return result
    return result

async def if_exists_func(p_func):
    sql="""select count(0) from t_func where func_url='{0}'""".format(p_func['func_url'])
    rs = await async_processer.query_one(sql)
    if rs[0]==0:
        return False
    else:
        return True

def check_func(p_func):
    result = {}
    result['code'] = '0'
    result['message'] = '验证通过'

    if p_func["priv_id"]=="":
        result['code']='-1'
        result['message']='功能模块不能为空！'
        return result

    if p_func["func_name"]=="":
        result['code']='-1'
        result['message']='功能名称不能为空！'
        return result

    if p_func["func_url"] == "":
        result['code'] = '-1'
        result['message'] = '功能URL不能为空！'
        return result
    return result
