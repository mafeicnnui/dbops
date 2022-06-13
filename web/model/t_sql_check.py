#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/12/2 11:57
# @Author : ma.fei
# @File : t_sql_check.py.py
# @Software: PyCharm

import re
import logging
import traceback
from web.model.t_ds    import get_ds_by_dsid_by_cdb
from web.utils.common  import format_sql,format_exception
from web.utils.mysql_async import async_processer,reReplace

def is_number(str):
  try:
    if str=='NaN':
      return False
    float(str)
    return True
  except ValueError:
    return False


def get_db_name(p_sql):
    if p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("TABLE") > 0 \
            or p_sql.upper().count("TRUNCATE") > 0 and p_sql.upper().count("TABLE") > 0 \
            or p_sql.upper().count("ALTER") > 0 and p_sql.upper().count("TABLE") > 0 \
            or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("TABLE") > 0 \
            or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("VIEW") > 0 \
            or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("FUNCTION") > 0 \
            or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("PROCEDURE") > 0 \
            or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("INDEX") > 0 \
            or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("TRIGGER") > 0:
        if p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("INDEX") > 0 and p_sql.upper().count("UNIQUE") > 0:
            obj = re.split(r'\s+', p_sql)[3].replace('`', '')
        else:
            obj = re.split(r'\s+', p_sql)[2].replace('`', '')

        if ('(') in obj:
            if obj.find('.') < 0:
                return None
            else:
                return obj.split('(')[0].split('.')[0]
        else:
            if obj.find('.') < 0:
                return None
            else:
                return obj.split('.')[0]

    if get_obj_op(p_sql) in ('INSERT', 'DELETE'):
        if re.split(r'\s+', p_sql.strip())[2].split('(')[0].strip().replace('`', '').find('.') < 0:
            return None
        else:
            return re.split(r'\s+', p_sql.strip())[2].split('(')[0].strip().replace('`', '').split('.')[0]

    if get_obj_op(p_sql) in ('UPDATE'):
        if re.split(r'\s+', p_sql.strip())[1].split('(')[0].strip().replace('`', '').find('.') < 0:
            return None
        else:
            return re.split(r'\s+', p_sql.strip())[1].split('(')[0].strip().replace('`', '').split('.')[0]

def get_obj_name(p_sql):
    if p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("TABLE") > 0 \
        or p_sql.upper().count("TRUNCATE") > 0 and p_sql.upper().count("TABLE") > 0 \
         or p_sql.upper().count("ALTER") > 0 and p_sql.upper().count("TABLE") > 0 \
           or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("TABLE") > 0 \
             or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("DATABASE") > 0 \
                or  p_sql.upper().count("CREATE")>0 and p_sql.upper().count("VIEW")>0 \
                   or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("FUNCTION") > 0 \
                    or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("PROCEDURE") > 0 \
                      or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("INDEX") > 0 \
                        or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("TRIGGER") > 0  \
                           or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("DATABASE") > 0:

       if p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("INDEX") > 0 and p_sql.upper().count("UNIQUE") > 0:
           obj = re.split(r'\s+', p_sql)[3].replace('`', '')
       else:
           obj=re.split(r'\s+', p_sql)[2].replace('`', '')

       if ('(') in obj:
           if obj.find('.')<0:
              return obj.split('(')[0]
           else:
              return obj.split('(')[0].split('.')[1]
       else:
           if obj.find('.') < 0:
              return obj
           else:
              return obj.split('.')[1]

    if get_obj_op(p_sql) in('INSERT','DELETE'):
         if re.split(r'\s+', p_sql.strip())[2].split('(')[0].strip().replace('`','').find('.')<0:
            return  re.split(r'\s+', p_sql.strip())[2].split('(')[0].strip()
         else:
            return re.split(r'\s+', p_sql.strip())[2].split('(')[0].strip().split('.')[1]

    if get_obj_op(p_sql) in('UPDATE'):
        if re.split(r'\s+', p_sql.strip())[1].split('(')[0].strip().replace('`','').find('.')<0:
           return re.split(r'\s+', p_sql.strip())[1].split('(')[0].strip()
        else:
           return re.split(r'\s+', p_sql.strip())[1].split('(')[0].strip().split('.')[1]

def get_obj_type(p_sql):
    if p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("TABLE") > 0 \
       or p_sql.upper().count("ALTER") > 0 and p_sql.upper().count("TABLE") > 0 \
         or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("TABLE") > 0 \
            or  p_sql.upper().count("CREATE")>0 and p_sql.upper().count("VIEW")>0 \
              or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("FUNCTION") > 0 \
                or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("PROCEDURE") > 0 \
                   or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("INDEX") > 0 \
                       or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("EVENT") > 0 \
                          or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("TRIGGER") > 0 \
                              or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("DATABASE") > 0 \
        or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("VIEW") > 0 \
        or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("FUNCTION") > 0 \
          or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("PROCEDURE") > 0 \
            or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("INDEX") > 0 \
              or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("EVENT") > 0 \
                or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("TRIGGER") > 0 \
                  or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("DATABASE") > 0:
       obj = re.split(r'\s+', p_sql)[1].replace('`', '')
       if ('(') in obj:
          return obj.split('(')[0].upper()
       else:
          return obj.upper()
    else:
       return ''

def get_obj_op(p_sql):
    if re.split(r'\s+', p_sql)[0].upper() in('CREATE','DROP') and re.split(r'\s+', p_sql)[1].upper() in('TABLE','INDEX','DATABASE'):
       return re.split(r'\s+', p_sql)[0].upper()+'_'+re.split(r'\s+', p_sql)[1].upper()
    if re.split(r'\s+', p_sql)[0].upper() in('TRUNCATE'):
       return 'TRUNCATE_TABLE'
    if re.split(r'\s+', p_sql)[0].upper()== 'ALTER' and re.split(r'\s+', p_sql)[1].upper()=='TABLE' and  re.split(r'\s+', p_sql)[3].upper() in('ADD','DROP','MODIFY'):
       return re.split(r'\s+', p_sql)[0].upper()+'_'+re.split(r'\s+', p_sql)[1].upper()+'_'+re.split(r'\s+', p_sql)[3].upper()
    if re.split(r'\s+', p_sql)[0].upper() in('INSERT','UPDATE','DELETE') :
       return re.split(r'\s+', p_sql)[0].upper()

def process_result(v):
    if isinstance(v, tuple):
        if len(v)==1:
           return str(v)
        else:
           return 'code:{0},error:{1}'.format(str(v[0]),str(v[1]))
    else:
        return str(v)

def check_idx_name_col(p_sql,rule):
    ob = get_obj_name(p_sql)
    t  = re.split(r'\s+', p_sql.strip())
    if len(t) == 6:
        if t[5].split(')')[0].split('(')[0] ==  t[5].split(')')[0].split('(')[1]:
           return rule['error'].format(ob)
    if len(t) == 7:
        if t[5] == t[6].replace('(','').replace(')',''):
           return rule['error'].format(ob)
    return None

async def check_mysql_tab_exists(ds,tab):
   sql="""select count(0) from information_schema.tables 
            where table_schema=database() and table_name='{0}'""".format(tab.replace('`',''))
   rs = await async_processer.query_one_by_ds(ds,sql)
   print('check_mysql_tab_exists=>rs=>',rs,rs[0])
   return rs[0]

async def check_mysql_proc_exists(ds,tab):
   sql="""select count(0) from information_schema.routines 
            where routine_schema=database() and routine_name='{0}'""".format(tab)
   rs = await async_processer.query_one(ds,sql)
   return rs[0]

async def query_check_result(user):
    sql = """select xh,obj_name,rule_id,rule_name,rule_value,
                    case when error!='检测通过!' then
                       concat("<span style='color:red;'>",error,"</span")
                    else
                       error 
                    end error    
                from  t_sql_audit_rule_err where user_id={} order by id""".format(user['userid'])
    return await async_processer.query_list(sql)

async def del_check_results(user):
    sql = 'delete from t_sql_audit_rule_err where user_id={}'.format(user['userid'])
    await async_processer.exec_sql(sql)

async def get_obj_pk_name(p_ds,p_sql):
    if (await check_mysql_tab_exists(p_ds, get_obj_name(p_sql))) > 0:
       return '表:{0}已存在!'.format(get_obj_name(p_sql))
    else:
      await async_processer.exec_sql_by_ds(p_ds,p_sql)

    sql = '''SELECT column_name  FROM  information_schema.columns 
                WHERE upper(table_schema)=DATABASE()  AND upper(table_name)=upper('{}')  AND column_key='PRI'
          '''.format(get_obj_name(p_sql))
    rs  = await async_processer.query_one_by_ds(p_ds,sql)
    col = rs[0]
    await async_processer.exec_sql_by_ds(p_ds,'drop table {}'.format(get_obj_name(p_sql)))
    return col

async def get_obj_pk_name_multi(p_ds,p_sql,config):
    try:
        ob  = get_obj_name(p_sql)
        op  = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            sql='''SELECT count(0)
                     FROM  information_schema.columns   
                       WHERE UPPER(table_schema)=DATABASE() AND UPPER(table_name)=upper('{}')
                         AND column_key='PRI' and column_name='id' '''.format(ob)
            rs = await async_processer.query_one_by_ds(p_ds,sql)
            config[ob] = 'drop table {}'.format(ob)
            return rs[0]
    except Exception as e:
        traceback.print_exc()
        return str(e)

async def f_get_table_ddl(p_ds,tab):
    sql = """show create table {0}""".format(tab)
    rs = await async_processer.query_one_by_ds(p_ds, sql)
    return rs[1]

async def get_obj_privs_grammar(p_ds,p_sql):
    try:
        op = get_obj_op(p_sql)
        ob = get_obj_name(p_sql)
        db = get_db_name(p_sql)
        dp = 'drop table {}'
        if db is not None:
            if db != p_ds['service']:
               return '语句中库名:{}与运行库名{}不同!'.format(db,p_ds['service'])

        if op == 'CREATE_TABLE':
            if await check_mysql_tab_exists(p_ds,ob) > 0:
               return '表:{0} 已存在!'.format(ob)
            else:
               await async_processer.exec_sql_by_ds(p_ds, p_sql)
               await async_processer.exec_sql_by_ds(p_ds, dp.format(ob))
               return '0'
        if op in('ALTER_TABLE_ADD','ALTER_TABLE_DROP'):
            tb = await f_get_table_ddl(p_ds, ob)
            if await check_mysql_tab_exists(p_ds,ob) == 0:
               return '表:{0} 不存在!'.format(ob)
            else:
               try:
                   await async_processer.exec_sql_by_ds(p_ds, tb.replace(ob,get_tmp_name(ob)))
                   await async_processer.exec_sql_by_ds(p_ds, p_sql.replace(ob, get_tmp_name(ob)))
                   await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
               except:
                   print('>>>>>>', dp.format(get_tmp_name(ob)))
                   await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
               return '0'
    except :
        e = traceback.format_exc().split('Error: ')[1]
        return e

async def get_obj_privs_grammar_proc(p_ds,p_sql):
    try:
        op = get_obj_op(p_sql)
        ob = get_obj_name(p_sql)
        tp = get_obj_type(p_sql)
        dp = 'drop {} {}'
        if op  in('CREATE_PROCEDURE','CREATE_FUNCTION','CREATE_TRIGGER','CREATE_EVENT'):
            if await check_mysql_proc_exists(p_ds, ob) > 0:
               return '过程:{0} 已存在!'.format(get_obj_name(p_sql))
            else:
               await async_processer.exec_sql_by_ds(p_ds, p_sql)
               await async_processer.exec_sql_by_ds(p_ds, dp.format(tp,ob))

        elif  op  in('DROP_PROCEDURE','DROP_FUNCTION','DROP_TRIGGER','DROP_EVENT'):
            if await check_mysql_proc_exists(p_ds, ob) == 0:
               return '过程:{0} 不存在!'.format(ob)
            else:
               await async_processer.exec_sql_by_ds(p_ds, p_sql.replace(ob, get_tmp_name(ob)))
               await async_processer.exec_sql_by_ds(p_ds, dp.format(tp,get_tmp_name(ob)))
        return '0'
    except Exception as e:
        return process_result(str(e))

async def get_obj_privs_grammar_multi(p_ds,p_sql,config):
    try:
        op = get_obj_op(p_sql)
        ob = get_obj_name(p_sql)
        dp = 'drop table {}'
        if op == 'CREATE_TABLE':
            if await check_mysql_tab_exists(p_ds, ob) > 0:
                return '表:{0}已存在!'.format(ob)
            else:
                await async_processer.exec_sql_by_ds(p_ds, p_sql)
            config[ob] = dp.format(ob)
        elif op in('ALTER_TABLE_ADD','ALTER_TABLE_DROP'):
            tb = await f_get_table_ddl(p_ds, ob)
            if config.get(get_tmp_name(ob)) is None:
                if await check_mysql_tab_exists(p_ds, ob) ==  0:
                   return '表:{0}不存在!'.format(ob)
                else:
                   await async_processer.exec_sql_by_ds(p_ds, tb.replace(ob, get_tmp_name(ob)))
                   await async_processer.exec_sql_by_ds(p_ds, p_sql.replace(ob, get_tmp_name(ob)))
            config['dbops_' +ob] = dp.format(get_tmp_name(ob))
        return '0'
    except Exception as e:
        return str(e)

async def get_tab_comment(p_ds,p_sql):
    ob = get_obj_name(p_sql)
    dp = 'drop table {}'.format(ob)
    if await check_mysql_tab_exists(p_ds, ob) > 0:
        return '表:{0}已存在!'.format(ob)
    else:
        await async_processer.exec_sql_by_ds(p_ds, p_sql)
        st = '''SELECT CASE WHEN table_comment!='' THEN 1 ELSE 0 END 
                  FROM  information_schema.tables   
                  WHERE upper(table_schema)=DATABASE()  AND upper(table_name) =upper('{}')'''.format(ob)
        rs = await async_processer.query_one_by_ds(p_ds,st)
        await async_processer.exec_sql_by_ds(p_ds,dp)
        return rs[0]

async def get_tab_comment_multi(p_ds,p_sql,config):
    try:
        ob = get_obj_name(p_sql)
        op = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            sql = '''SELECT CASE WHEN table_comment!='' THEN 1 ELSE 0 END 
                      FROM  information_schema.tables   
                        WHERE UPPER(table_schema)=DATABASE()  AND UPPER(table_name) =upper('{}')'''.format(ob)
            rs  = await async_processer.query_one_by_ds(p_ds,sql)
            config[ob] = 'drop table {}'.format(ob)
            return rs[0]
    except Exception as e:
        return str(e)

async def get_col_comment(p_ds,p_sql):
    ob = get_obj_name(p_sql)
    op = get_obj_op(p_sql)
    dp = 'drop table {}'
    try:
        st = '''SELECT table_name,column_name,CASE WHEN column_comment!='' THEN 1 ELSE 0 END 
                  FROM  information_schema.columns   
                     WHERE UPPER(table_schema)=DATABASE()  AND UPPER(table_name) = upper('{}')'''

        if op == 'CREATE_TABLE':
            if (await check_mysql_tab_exists(p_ds,ob)) > 0:
                return  '表:{0}已存在!'.format(ob)
            else:
                await async_processer.exec_sql_by_ds(p_ds, p_sql)

                col = await async_processer.query_list_by_ds(p_ds,st.format(ob))
                await async_processer.exec_sql_by_ds(p_ds, 'drop table {}'.format(ob))
                return col
        elif op == 'ALTER_TABLE_ADD':
            if await (check_mysql_tab_exists(p_ds, ob)) ==  0:
               return '表:{0} 不存在!'.format(get_obj_name(p_sql))
            else:
               tb = await f_get_table_ddl(p_ds, ob)
               await async_processer.exec_sql_by_ds(p_ds, tb.replace(ob, get_tmp_name(ob)))
               await async_processer.exec_sql_by_ds(p_ds, p_sql.replace(ob, get_tmp_name(ob)))
               col = await async_processer.query_list_by_ds(p_ds, st.format(get_tmp_name(ob)))
               await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
               return col
    except Exception as e:
        try:
            await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
        except:
            pass
        return process_result(str(e))

async def get_col_comment_multi(p_ds,p_sql,config):
    try:
        ob = get_obj_name(p_sql)
        op = get_obj_op(p_sql)
        tb = await f_get_table_ddl(p_ds, ob)
        dp = 'drop table {}'
        st = '''SELECT table_name,column_name,CASE WHEN column_comment!='' THEN 1 ELSE 0 END 
                 FROM information_schema.columns   
                   WHERE UPPER(table_schema)=DATABASE() AND UPPER(table_name) = upper('{}')'''
        if op == 'CREATE_TABLE':
           rs = await async_processer.query_list_by_ds(p_ds,st.format(ob))
           config[ob] = 'drop table {}'.format(ob)
           return rs
        elif op == 'ALTER_TABLE_ADD':
            if config.get(get_tmp_name(ob)) is None:
                if await check_mysql_tab_exists(p_ds, ob) > 0:
                   await async_processer.exec_sql_by_ds(p_ds, tb.replace(ob, get_tmp_name(ob)))
                   await async_processer.exec_sql_by_ds(p_ds, p_sql.replace(ob, get_tmp_name(ob)))
                   rs = await async_processer.query_lisst_by_ds(p_ds, st.format(get_tmp_name(ob)))
                   config[get_tmp_name(ob)] = 'drop table {0}'.format(get_tmp_name(ob))
                   return rs
                else:
                   return '表:{0}不存在!'.format(ob)
    except Exception as e:
        traceback.print_exc()
        return process_result(str(e))

async def get_col_default_value(p_ds,p_sql):
    ob = get_obj_name(p_sql)
    op = get_obj_op(p_sql)
    tb = await f_get_table_ddl(p_ds, ob)
    dp = 'drop table {}'
    try:
        st = '''SELECT table_name,column_name,CASE WHEN column_default is NULL AND is_nullable='NO' THEN 0 ELSE 1 END 
                 FROM  information_schema.columns   
                  WHERE UPPER(table_schema)=DATABASE()  
                    and column_key!='PRI' AND UPPER(table_name) = upper('{}')'''
        if op == 'CREATE_TABLE':
            if await check_mysql_tab_exists(p_ds, ob) > 0:
               return  '表:{0}已存在!'.format(ob)
            else:
               await async_processer.exec_sql_by_ds(p_ds, p_sql)
               rs = await async_processer.query_list_by_ds(p_ds,st.format(ob))
               await async_processer.exec_sql_by_ds(p_ds, dp.format(ob))
               return rs
        elif op == 'ALTER_TABLE_ADD':
            if await check_mysql_tab_exists(p_ds, ob) == 0:
               return '表:{0}不存在!'.format(get_obj_name(p_sql))
            else:
               await async_processer.exec_sql_by_ds(p_ds, tb.replace(ob, get_tmp_name(ob)))
               await async_processer.exec_sql_by_ds(p_ds, p_sql.replace(ob, get_tmp_name(ob)))
               rs = await async_processer.query_list_by_ds(p_ds, st.format('dbops_' +ob))
               await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
               return rs
    except Exception as e:
        traceback.print_exc()
        try:
            await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
        except:
            pass
        return process_result(str(e))

async def get_col_default_value_multi(p_ds,p_sql,config):
    try:
        ob = get_obj_name(p_sql)
        op = get_obj_op(p_sql)
        dp = 'drop table {}'
        tb = await f_get_table_ddl(p_ds, ob)
        st = '''SELECT table_name,column_name,case when column_default is NULL and is_nullable='NO' then 0 ELSE 1 end 
                   FROM  information_schema.columns   
                    WHERE upper(table_schema)=DATABASE() AND column_key!='PRI'
                      AND upper(table_name) = upper('{}')'''
        if op == 'CREATE_TABLE':
           rs = await async_processer.query_list_by_ds(p_ds,st.format(ob))
           config[ob] = dp.format(ob)
           return rs
        elif op == 'ALTER_TABLE_ADD':
            if config.get(get_tmp_name(ob)) is None:
               await async_processer.exec_sql_by_ds(p_ds, tb.replace(ob, get_tmp_name(ob)))
               await async_processer.exec_sql_by_ds(p_ds, p_sql.replace(ob, get_tmp_name(ob)))
               rs = await async_processer.query_list_by_ds(p_ds, st.format(get_tmp_name(ob)))
               #await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
               config[get_tmp_name(ob)] = dp.format(get_tmp_name(ob))
               return rs
    except Exception as e:
        return process_result(str(e))

async def get_time_col_default_value(p_ds,p_sql):
    ob = get_obj_name(p_sql)
    op = get_obj_op(p_sql)
    dp = 'drop table {}'
    try:
        st = '''SELECT  table_name, column_name,'CURRENT_TIMESTAMP',
                        CASE WHEN column_default='CURRENT_TIMESTAMP'  THEN  1 ELSE 0 END
                  FROM  information_schema.columns   
                  WHERE upper(table_schema)=DATABASE()  
                    AND data_type IN('datetime','timestamp')
                    AND column_key!='PRI'
                    AND UPPER(table_name) = upper('{}')
                    AND column_name='create_time'
                UNION ALL  
                  SELECT table_name,column_name,'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
                         CASE WHEN column_default='CURRENT_TIMESTAMP' AND extra='on update CURRENT_TIMESTAMP' THEN  1 ELSE 0 END
                  FROM  information_schema.columns   
                  WHERE upper(table_schema)=DATABASE()  
                    AND data_type IN('datetime','timestamp')
                    AND column_key!='PRI'
                    AND UPPER(table_name) = upper('{}')
                    AND column_name='update_time'
              '''
        if op == 'CREATE_TABLE':
           if await check_mysql_tab_exists(p_ds, ob) > 0:
              return  '表:{0}已存在!'.format(ob)
           else:
              await async_processer.exec_sql_by_ds(p_ds, p_sql)
              rs = await async_processer.query_list_by_ds(p_ds, st.format(ob,ob))
              await async_processer.exec_sql_by_ds(p_ds, dp.format(ob))
              return rs
        elif op == 'ALTER_TABLE_ADD':
           if await check_mysql_tab_exists(p_ds, ob) ==  0:
              return '表:{0}不存在!'.format(get_obj_name(p_sql))
           else:
              tb   = await f_get_table_ddl(p_ds, ob)
              await async_processer.exec_sql_by_ds(p_ds, tb.replace(ob, get_tmp_name(ob)))
              await async_processer.exec_sql_by_ds(p_ds, p_sql.replace(ob, get_tmp_name(ob)))
              rs = await async_processer.query_list_by_ds(p_ds, st.format(get_tmp_name(ob),get_tmp_name(ob)))
              await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
              return rs
    except Exception as e:
        traceback.print_exc()
        try:
            await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
        except:
            pass
        return process_result(str(e))

async def get_time_col_default_value_multi(p_ds,p_sql,config):
    try:
        ob = get_obj_name(p_sql)
        op = get_obj_op(p_sql)
        dp = 'drop table {}'
        st = '''SELECT  table_name, column_name,'CURRENT_TIMESTAMP',
                        CASE WHEN column_default='CURRENT_TIMESTAMP'  THEN  1 ELSE 0 END
                  FROM  information_schema.columns   
                  WHERE upper(table_schema)=DATABASE()  
                    AND data_type IN('datetime','timestamp')
                    AND column_key!='PRI'
                    AND UPPER(table_name) = upper('{}')
                    AND column_name='create_time'
                UNION ALL  
                  SELECT table_name,column_name,'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
                         CASE WHEN column_default='CURRENT_TIMESTAMP' AND extra='on update CURRENT_TIMESTAMP' THEN  1 ELSE 0 END
                  FROM  information_schema.columns   
                  WHERE upper(table_schema)=DATABASE()  
                    AND data_type IN('datetime','timestamp')
                    AND column_key!='PRI'
                    AND UPPER(table_name) = upper('{}')
                    AND column_name='update_time'
              '''
        if op == 'CREATE_TABLE':
              rs = await async_processer.query_list_by_ds(p_ds, st.format(ob,ob))
              config[ob] = dp.format(ob)
              return rs
        elif op == 'ALTER_TABLE_ADD':
              tb   = await f_get_table_ddl(p_ds, ob)
              await async_processer.exec_sql_by_ds(p_ds, tb.replace(ob, get_tmp_name(ob)))
              await async_processer.exec_sql_by_ds(p_ds, p_sql.replace(ob, get_tmp_name(ob)))
              rs = await async_processer.query_list_by_ds(p_ds, st.format(get_tmp_name(ob),get_tmp_name(ob)))
              config[get_tmp_name(ob)] = dp.format(get_tmp_name(ob))
              return rs
    except Exception as e:
        return process_result(str(e))

async def get_tab_char_col_len(p_ds,p_sql,rule):
    ob = get_obj_name(p_sql)
    dp = 'drop table {}'
    try:
        st = '''SELECT 
                    table_name,column_name,CASE WHEN character_maximum_length<={0} THEN 1 ELSE 0 END AS val
                  FROM  information_schema.columns   
                  WHERE UPPER(table_schema)=DATABASE()  AND data_type IN('varchar','char')
                    AND column_key!='PRI' AND UPPER(table_name) = upper('{1}')'''.format(rule['rule_value'], ob)
        await async_processer.exec_sql_by_ds(p_ds, p_sql)
        rs = await async_processer.query_list_by_ds(p_ds,st)
        await async_processer.exec_sql_by_ds(p_ds, dp.format(ob))
        return rs
    except:
       traceback.print_exc()
       try:
           await async_processer.exec_sql_by_ds(p_ds, dp.format(ob))
       except:
           pass
       return  0

async def get_tab_char_col_total_len(p_ds,p_sql,rule):
    ob = get_obj_name(p_sql)
    dp = 'drop table {}'
    st = '''SELECT 
                 CASE WHEN IFNULL(SUM(character_maximum_length),0)<={0} THEN 1 ELSE 0 END AS val
              FROM  information_schema.columns   
              WHERE UPPER(table_schema)=DATABASE()  AND data_type IN('varchar','char')
               AND column_key!='PRI' AND UPPER(table_name) = upper('{1}')'''.format(rule['rule_value'], ob)
    await async_processer.exec_sql_by_ds(p_ds, p_sql)
    rs = await async_processer.query_one_by_ds(p_ds, st)
    await async_processer.exec_sql_by_ds(p_ds, dp.format(ob))
    return rs[0]

async def check_tab_rule(p_sql,p_user,n_sxh):
    obj = get_obj_name(p_sql.strip()).lower()
    ret = True
    sql = """select id,rule_code,rule_name,rule_value,error 
              from t_sql_audit_rule 
               where rule_type='ddl' and status='1' 
                and rule_code in('switch_tab_max_len','switch_tab_not_digit_first',
                                 'switch_tab_two_digit_end','switch_tab_disable_prefix') order by id"""
    rs = await async_processer.query_dict_list(sql)
    for rule in rs:
        if rule['rule_code'] == 'switch_tab_max_len' :
            if get_obj_op(p_sql) == 'CREATE_TABLE' and  get_obj_type(p_sql.strip()) == 'TABLE':
                print('检查表名最大长度...')
                if len(obj)>int(rule['rule_value']):
                    rule['error'] = format_sql(rule['error'].format(obj,rule['rule_value']))
                    await save_check_results(rule, p_user, p_sql.strip(), n_sxh)
                    ret = False

        if rule['rule_code'] == 'switch_tab_not_digit_first' and rule['rule_value'] == 'true':
            if get_obj_op(p_sql) == 'CREATE_TABLE' and  get_obj_type(p_sql.strip()) == 'TABLE':
                print('检查表名表名不能以数字开头...')
                if obj[0] in  "0123456789":
                    rule['error'] = format_sql(rule['error'].format(obj,rule['rule_value']))
                    await save_check_results(rule, p_user, p_sql.strip(), n_sxh)
                    ret = False

        if rule['rule_code'] == 'switch_tab_two_digit_end' and rule['rule_value'] == 'true':
            if get_obj_op(p_sql) == 'CREATE_TABLE' and  get_obj_type(p_sql.strip()) == 'TABLE':
                print('禁止表名以连续2位及以上数字为后缀...')
                if len(re.findall(r'\d{2,9}$', obj, re.M)) > 0:
                    rule['error'] = format_sql(rule['error'].format(obj,rule['rule_value']))
                    await save_check_results(rule, p_user, p_sql.strip(), n_sxh)
                    ret = False

        if rule['rule_code'] == 'switch_tab_disable_prefix' :
            if get_obj_op(p_sql) == 'CREATE_TABLE' and  get_obj_type(p_sql.strip()) == 'TABLE':
               print('检查表名称禁止前缀...')
               for t in rule['rule_value'].lower().split(','):
                   if len(re.findall(r'{0}$'.format(t), obj, re.M)) > 0 \
                           or len(re.findall(r'^{0}'.format(t), obj, re.M)) > 0 :
                       rule['error'] = format_sql(rule['error'].format(obj, t))
                       await save_check_results(rule, p_user, p_sql.strip(), n_sxh)
                       ret = False

    return ret

async def check_idx_name_null(p_ds,p_sql):
    ob = get_obj_name(p_sql)
    tb = await f_get_table_ddl(p_ds, ob)
    dp = 'drop table {}'
    st = """SELECT count(0) FROM mysql.innodb_index_stats a 
              WHERE a.`database_name` = DATABASE() AND  a.table_name='{0}' AND index_name='{1}'"""
    if await check_mysql_tab_exists(p_ds, ob) ==  0:
       return '表:{0}不存在!'.format(ob)
    else:
       await async_processer.exec_sql_by_ds(p_ds, tb.replace(ob, get_tmp_name(ob)))
       t = re.split(r'\s+', p_sql.strip())
       if len(t) == 6 and t[5].find('(') == 0:
          col = p_sql.strip().split('(')[1].split(')')[0]
          await async_processer.exec_sql_by_ds(p_ds, p_sql.replace(ob, get_tmp_name(ob)))
          rs = await async_processer.query_one_by_ds(p_ds, st.format(get_tmp_name(ob), col))
          await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
          return rs[0]
    return 0

async def check_idx_name_rule(p_ds,p_sql,rule):
    op  = get_obj_op(p_sql)
    if op == "ALTER_TABLE_ADD":
       obj = get_obj_name(p_sql).lower()
       idx = re.split(r'\s+', p_sql.strip())[5].split('(')[0].strip()
    elif op == "CREATE_INDEX":
       obj = re.split(r'\s+', p_sql.strip())[4].split('(')[0].strip()
       idx = re.split(r'\s+', p_sql.strip())[2].split('(')[0].strip()

    sql = """select column_name from information_schema.columns
              where table_schema=database() and table_name='{}' and column_key!='PRI'""".format(obj)
    rs = await async_processer.query_list_by_ds(p_ds, sql)
    flag = False
    for r in rs:
        exp= 'idx_$$COL$$_n[1-9]{1,2}'.replace('$$COL$$',r[0])
        if re.search(exp, idx) is not None:
           flag = True
    if not flag:
       return rule['error'].format(obj,idx)
    else:
       return None

async def check_idx_numbers(p_ds,p_sql,rule):
    op  = get_obj_op(p_sql)
    dp = 'drop table {}'
    if  op == "ALTER_TABLE_ADD":
        ob = get_obj_name(p_sql).lower()
    elif op == "CREATE_INDEX":
        ob = re.split(r'\s+', p_sql.strip())[4].split('(')[0].strip()
    tb = await f_get_table_ddl(p_ds, ob)
    st = """SELECT COUNT(DISTINCT index_name) FROM mysql.innodb_index_stats a 
                    WHERE a.database_name = DATABASE() AND a.table_name='{0}' 
                      AND index_name!='PRIMARY'""".format(get_tmp_name(ob))
    if await check_mysql_tab_exists(p_ds, ob) > 0:
        await async_processer.exec_sql_by_ds(p_ds, tb.replace(ob, get_tmp_name(ob)))
        await async_processer.exec_sql_by_ds(p_ds, p_sql.replace(ob, get_tmp_name(ob)))
        rs = await async_processer.query_one_by_ds(p_ds, st.format(get_tmp_name(ob)))
        await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
        if rs[0] > int(rule['rule_value']):
            return rule['error'].format(ob)
        return None
    else:
        return '表:{0}不存在!'.format(ob)

async def check_idx_col_numbers(p_ds,p_sql,rule):
    op  = get_obj_op(p_sql)
    dp  = 'drop table {}'
    if  op == "ALTER_TABLE_ADD":
        ob = get_obj_name(p_sql).lower()
        idx = re.split(r'\s+', p_sql.strip())[5].split('(')[0].strip().replace('`','')
    elif op == "CREATE_INDEX":
        ob = re.split(r'\s+', p_sql.strip())[4].split('(')[0].strip()
        idx = re.split(r'\s+', p_sql.strip())[2].split('(')[0].strip().replace('`','')

    tb = await f_get_table_ddl(p_ds, ob)
    st = """SELECT count(0) FROM information_schema.INNODB_SYS_INDEXES 
            WHERE `table_id`=(SELECT table_id FROM information_schema.`INNODB_SYS_TABLES` WHERE NAME='{}/{}')
              and `name`='{}' and n_fields>{}""".format(p_ds['service'],ob,idx,rule['rule_value'])
    print('st=',st)

    if await check_mysql_tab_exists(p_ds, ob) > 0:
        await async_processer.exec_sql_by_ds(p_ds, tb.replace(ob,get_tmp_name(ob)))
        await async_processer.exec_sql_by_ds(p_ds, p_sql.replace(ob, get_tmp_name(ob)))
        rs = await async_processer.query_one_by_ds(p_ds, st.format(get_tmp_name(ob)))
        await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
        print('rs=',rs)
        if rs[0] > 0:
           return rule['error'].format(ob,idx)
        return  None
    else:
        return '表:{0}不存在!'.format(ob)

async def check_idx_rule(p_ds,p_sql,p_user,n_sxh):
    obj = get_obj_name(p_sql.strip()).lower()
    ret = True
    sql = """select id,rule_code,rule_name,rule_value,error 
                from t_sql_audit_rule 
                 where rule_type='ddl' and status='1' 
                  and rule_code in('switch_idx_name_null','switch_idx_name_rule',
                                   'switch_idx_numbers','switch_idx_col_numbers',
                                   'switch_idx_name_col') order by id"""
    rs = await async_processer.query_dict_list(sql)
    for rule in rs:
        if rule['rule_code'] == 'switch_idx_name_null' and rule['rule_value'] == 'false':
            if get_obj_op(p_sql) == 'ALTER_TABLE_ADD' and get_obj_type(p_sql.strip()) == 'TABLE'\
                  and p_sql.strip().upper().count('INDEX')  \
                    and p_sql.strip().upper().find("INDEX")>p_sql.strip().upper().find("ADD") :
                print('检查允许索引名为空...')
                v = await check_idx_name_null(p_ds,p_sql,rule)
                try:
                    if int(v) > 0 :
                       rule['error'] = format_sql(rule['error'].format(obj))
                       await save_check_results(rule, p_user, p_sql.strip(), n_sxh)
                       ret = False
                except:
                    rule['error'] = format_sql(v)
                    await save_check_results(rule, p_user, p_sql.strip(), n_sxh)
                    ret = False

        if rule['rule_code'] == 'switch_idx_name_rule' and rule['rule_value'] == 'true':
            if (get_obj_op(p_sql) == 'ALTER_TABLE_ADD' and get_obj_type(p_sql.strip()) == 'TABLE' \
                  and p_sql.strip().upper().count('INDEX') \
                    and p_sql.strip().upper().find("INDEX") > p_sql.strip().upper().find("ADD")) \
                      or (get_obj_op(p_sql) == 'CREATE_INDEX' and get_obj_type(p_sql.strip()) == 'INDEX'):
                print('检查索引名规则...')
                v = await check_idx_name_rule(p_ds,p_sql.strip(),rule)
                if v is not None:
                    rule['error'] = format_sql(v)
                    await save_check_results(rule, p_user, p_sql.strip(), n_sxh)
                    ret = False

        if rule['rule_code'] == 'switch_idx_numbers' :
            if (get_obj_op(p_sql) == 'ALTER_TABLE_ADD' and get_obj_type(p_sql.strip()) == 'TABLE' \
                  and p_sql.strip().upper().count('INDEX') \
                    and p_sql.strip().upper().find("INDEX") > p_sql.strip().upper().find("ADD")) \
                      or (get_obj_op(p_sql) == 'CREATE_INDEX' and get_obj_type(p_sql.strip()) == 'INDEX'):
                print('检查单表索引数上限...')
                v = await check_idx_numbers(p_ds,p_sql.strip(),rule)
                if v is not None:
                    rule['error'] = format_sql(v)
                    await save_check_results(rule, p_user, p_sql.strip(), n_sxh)
                    ret = False

        if rule['rule_code'] == 'switch_idx_col_numbers':
            if (get_obj_op(p_sql) == 'ALTER_TABLE_ADD' and get_obj_type(p_sql.strip()) == 'TABLE' \
                  and p_sql.strip().upper().count('INDEX') \
                    and p_sql.strip().upper().find("INDEX") > p_sql.strip().upper().find("ADD")) \
                      or (get_obj_op(p_sql) == 'CREATE_INDEX' and get_obj_type(p_sql.strip()) == 'INDEX'):
                print('检查单个索引字段上限...')
                v = await check_idx_col_numbers(p_ds,p_sql.strip(),rule)
                if v is not None:
                    rule['error'] = format_sql(v)
                    await save_check_results(rule, p_user, p_sql.strip(), n_sxh)
                    ret = False

        if rule['rule_code'] == 'switch_idx_name_col' and rule['rule_value'] == 'false':
            if get_obj_op(p_sql) == 'ALTER_TABLE_ADD' and get_obj_type(p_sql.strip()) == 'TABLE' \
                  and p_sql.strip().upper().count('INDEX') \
                    and p_sql.strip().upper().find("INDEX") > p_sql.strip().upper().find("ADD"):
                print('检查索引名与列名是否相同...')
                v = await check_idx_name_col(p_sql,rule)
                if v is not None:
                    rule['error'] = format_sql(v)
                    await save_check_results(rule, p_user, p_sql.strip(), n_sxh)
                    ret = False
    return ret

async def get_tab_char_col_len_multi(p_ds,p_sql,rule,config):
    try:
        op = get_obj_op(p_sql)
        ob = get_obj_name(p_sql)
        dp = 'drop table {}'
        tb = await f_get_table_ddl(p_ds, ob)
        st = '''SELECT table_name,column_name,CASE WHEN character_maximum_length<={0} THEN 1 ELSE 0 END AS val
                FROM  information_schema.columns   
                  WHERE UPPER(table_schema)=DATABASE()  AND data_type IN('varchar','char')
                     AND column_key!='PRI' AND UPPER(table_name) = upper('{1}')'''

        if op == 'CREATE_TABLE':
            rs = await async_processer.query_list_by_ds(p_ds,st.format(rule['rule_value'],ob))
            config[ob] = dp.format(ob)
            return rs
        elif op == 'ALTER_TABLE_ADD':
            rs = await async_processer.query_list_by_ds(p_ds, st.format(rule['rule_value'], 'dbops_' +ob))
            config[get_tmp_name(ob)] = dp.format(get_tmp_name(ob))
            return rs
    except Exception as e:
        return process_result(str(e))

async def get_tab_has_fields(p_ds,p_sql,p_rule):
    ob = get_obj_name(p_sql)
    op = get_obj_op(p_sql)
    dp = 'drop table {}'
    try:
        st =''
        for col in p_rule['rule_value'].split(','):
            if op == 'CREATE_TABLE':
                st = st +'''SELECT table_name,'{}' AS column_name
                                    FROM  information_schema.tables a
                                   WHERE a.table_schema=DATABASE()
                                     AND a.table_name= LOWER('{}')
                                     AND NOT EXISTS(SELECT 1 FROM information_schema.columns b
                                                    WHERE a.table_schema=b.table_schema
                                                      AND b.table_schema=DATABASE()
                                                      AND a.table_name=b.table_name
                                                      AND b.column_name='{}')  union all \n'''.format(col,ob,col)
            elif op == 'ALTER_TABLE_ADD':
                st = st + '''SELECT table_name,'{}' AS column_name
                                    FROM  information_schema.tables a
                                   WHERE a.table_schema=DATABASE()
                                     AND a.table_name= LOWER('{}')
                                     AND NOT EXISTS(SELECT 1 FROM information_schema.columns b
                                                    WHERE a.table_schema=b.table_schema
                                                      AND b.table_schema=DATABASE()
                                                      AND a.table_name=b.table_name
                                                      AND b.column_name='{}')  union all \n'''.format(col,get_tmp_name(ob), col)
        if op == 'CREATE_TABLE':
            if (await check_mysql_tab_exists(p_ds, ob)) > 0:
                return {'code': -1, 'msg': '表:{0}已存在!'.format(ob)}
            else:
                await async_processer.exec_sql_by_ds(p_ds, p_sql)
                col = await async_processer.query_list_by_ds(p_ds, st[0:-12])
                await async_processer.exec_sql_by_ds(p_ds, dp.format(ob))
                return {'code': 0, 'msg': col}
        elif op == 'ALTER_TABLE_ADD':
            if await (check_mysql_tab_exists(p_ds, ob)) == 0:
                return {'code': -1, 'msg': '表:{0}不存在!'.format(get_obj_name(p_sql))}
            else:
                tb = await f_get_table_ddl(p_ds, ob)
                await async_processer.exec_sql_by_ds(p_ds, tb.replace(ob, get_tmp_name(ob)))
                await async_processer.exec_sql_by_ds(p_ds, p_sql.replace(ob, get_tmp_name(ob)))
                rs = await async_processer.query_list_by_ds(p_ds, st[0:-12].format(get_tmp_name(ob),get_tmp_name(ob)))
                await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
                return {'code':0,'msg':rs}
    except Exception as e:
        try:
            await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
        except:
            pass
        return {'code':-1,'msg':process_result(e)}

async def get_tab_rows(p_ds,p_sql):
    ob = get_obj_name(p_sql)
    op = get_obj_op(p_sql)
    if op in ('CREATE_TABLE', 'ALTER_TABLE_ADD', 'ALTER_TABLE_DROP'):
        st = "select count(0) from {0}".format(ob)
        rs = await async_processer.query_one_by_ds(p_ds,st)
        return rs[0]
    return 0

async def get_tab_has_fields_multi(p_ds,p_sql,p_rule,config):
    ob = get_obj_name(p_sql)
    op = get_obj_op(p_sql)
    dp = 'drop table {}'
    try:
        st = ''
        for col in p_rule['rule_value'].split(','):
            if op == 'CREATE_TABLE':
                st = st + '''SELECT table_name,'{}' AS column_name
                                        FROM  information_schema.tables a
                                       WHERE a.table_schema=DATABASE()
                                         AND a.table_name= LOWER('{}')
                                         AND NOT EXISTS(SELECT 1 FROM information_schema.columns b
                                                        WHERE a.table_schema=b.table_schema
                                                          AND b.table_schema=DATABASE()
                                                          AND a.table_name=b.table_name
                                                          AND b.column_name='{}')  union all \n'''.format(col, ob, col)
            elif op == 'ALTER_TABLE_ADD':
                st = st + '''SELECT table_name,'{}' AS column_name
                                        FROM  information_schema.tables a
                                       WHERE a.table_schema=DATABASE()
                                         AND a.table_name= LOWER('{}')
                                         AND NOT EXISTS(SELECT 1 FROM information_schema.columns b
                                                        WHERE a.table_schema=b.table_schema
                                                          AND b.table_schema=DATABASE()
                                                          AND a.table_name=b.table_name
                                                          AND b.column_name='{}')  union all \n'''.format(col,
                                                                                                          get_tmp_name(ob),
                                                                                                          col)
        print('st------------------>',st)
        if op == 'CREATE_TABLE':
            rs = await async_processer.query_list_by_ds(p_ds, st[0:-12].format(ob,ob))
            config[ob] = dp.format(ob)
            return rs
        elif op in('ALTER_TABLE_ADD','ALTER_TABLE_DROP'):
            if config.get(get_tmp_name(ob)) is None:
                await async_processer.exec_sql_by_ds(p_ds, tb.replace(ob, get_tmp_name(ob)))
                await async_processer.exec_sql_by_ds(p_ds, p_sql.replace(ob, get_tmp_name(ob)))
                rs = await async_processer.query_list_by_ds(p_ds, st[0:-12].format(get_tmp_name(ob),get_tmp_name(ob)))
                config[get_tmp_name(ob)] = dp.format('dbops_' +ob)
                return rs
    except Exception as e:
        return process_result(str(e))

async def get_tab_tcol_datetime(p_ds,p_sql,p_rule):
    ob = get_obj_name(p_sql)
    op = get_obj_op(p_sql)
    dp = 'drop table {}'
    try:
        st = '''SELECT table_name,
                           'create_time' AS column_name
                     FROM  information_schema.tables a
                    WHERE a.table_schema=DATABASE()
                      AND a.table_name= LOWER('{0}')
                      AND EXISTS(SELECT 1 FROM information_schema.columns b
                                     WHERE a.table_schema=b.table_schema
                                       AND b.table_schema=DATABASE()
                                       AND a.table_name=b.table_name
                                       AND b.column_name='create_time'
                                       AND b.data_type!='datetime')
                    UNION ALL
                    SELECT table_name,
                           'update_time' AS column_name
                     FROM  information_schema.tables a
                    WHERE a.table_schema=DATABASE()
                      AND a.table_name= LOWER('{1}')
                      AND EXISTS(SELECT 1 FROM information_schema.columns b
                                     WHERE a.table_schema=b.table_schema
                                       AND b.table_schema=DATABASE()
                                       AND a.table_name=b.table_name
                                       AND b.column_name='update_time'
                                       AND b.data_type!='datetime')'''
        if op == 'CREATE_TABLE':
           if await check_mysql_tab_exists(p_ds, ob) > 0:
              return  '表:{0}已存在!'.format(ob)
           else:
              await async_processer.exec_sql_by_ds(p_ds, p_sql)
              rs = await async_processer.query_list_by_ds(p_ds, st.format(ob,ob))
              await async_processer.exec_sql_by_ds(p_ds, dp.format(ob))
              return rs
        elif op == 'ALTER_TABLE_ADD':
            tb = await f_get_table_ddl(p_ds, ob)
            if await check_mysql_tab_exists(p_ds, ob) == 0:
                return '表:{0}不存在!'.format(get_obj_name(p_sql))
            else:
               await async_processer.exec_sql_by_ds(p_ds, tb.replace(ob, get_tmp_name(ob)))
               await async_processer.exec_sql_by_ds(p_ds, p_sql.replace(ob, get_tmp_name(ob)))
               rs = await async_processer.query_list_by_ds(p_ds, st.format(get_tmp_name(ob),get_tmp_name(ob)))
               await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
               return rs
    except Exception as e:
        try:
            await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
        except:
            pass
        return process_result(str(e))

async def get_tab_tcol_datetime_multi(p_ds,p_sql,config):
    ob = get_obj_name(p_sql)
    op = get_obj_op(p_sql)
    tb = await f_get_table_ddl(p_ds, ob)
    dp = 'drop table {}'
    try:
        st ='''SELECT   table_name,
                       'create_time' AS column_name
                 FROM  information_schema.tables a  
                WHERE a.table_schema=DATABASE()  
                  AND a.table_name= LOWER('{0}')
                  AND EXISTS(SELECT 1 FROM information_schema.columns b
                                 WHERE a.table_schema=b.table_schema
                                   AND b.table_schema=DATABASE()
                                   AND a.table_name=b.table_name
                                   AND b.column_name='create_time'
                                   AND b.data_type!='datetime')   
                UNION ALL
                SELECT table_name,
                       'update_time' AS column_name
                 FROM  information_schema.tables a  
                WHERE a.table_schema=DATABASE()  
                  AND a.table_name= LOWER('{1}')
                  AND EXISTS(SELECT 1 FROM information_schema.columns b
                                 WHERE a.table_schema=b.table_schema
                                   AND b.table_schema=DATABASE()
                                   AND a.table_name=b.table_name
                                   AND b.column_name='update_time'
                                   AND b.data_type!='datetime')'''
        if op == 'CREATE_TABLE':
           rs = await async_processer.query_list_by_ds(p_ds, st.format(ob,ob))
           config[ob] = dp.format(ob)
           return rs
        elif op == 'ALTER_TABLE_ADD':
            if config.get(get_tmp_name(ob)) is None:
                await async_processer.exec_sql_by_ds(p_ds, tb.replace(ob, get_tmp_name(ob)))
                await async_processer.exec_sql_by_ds(p_ds, p_sql.replace(ob, get_tmp_name(ob)))
                rs = await async_processer.query_list_by_ds(p_ds, st.format(get_tmp_name(ob),get_tmp_name(ob)))
                #await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
                config[get_tmp_name(ob)] = dp.format('dbops_' + dp)
                return rs
    except Exception as e:
        return process_result(str(e))

async def get_col_not_null(p_ds,p_sql):
    ob = get_obj_name(p_sql)
    op = get_obj_op(p_sql)
    dp = 'drop table {}'
    try:
        st = '''SELECT table_name,column_name,CASE WHEN is_nullable='YES' THEN 0 ELSE 1 END 
                FROM  information_schema.columns  WHERE UPPER(table_schema)=DATABASE()  AND UPPER(table_name) = upper('{}')'''
        if op == 'CREATE_TABLE':
            if await check_mysql_tab_exists(p_ds, ob) > 0:
                return '表:{0}已存在!'.format(ob)
            else:
                await async_processer.exec_sql_by_ds(p_ds, p_sql)
                rs = await async_processer.query_list_by_ds(p_ds, st.format(ob))
                await async_processer.exec_sql_by_ds(p_ds, dp.format(ob))
                return rs
        elif op == 'ALTER_TABLE_ADD':
            if await check_mysql_tab_exists(p_ds, ob) == 0:
                return '表:{0}不存在!'.format(ob)
            else:
                tb = await f_get_table_ddl(p_ds, ob)
                await async_processer.exec_sql_by_ds(p_ds, tb.replace(ob, get_tmp_name(ob)))
                await async_processer.exec_sql_by_ds(p_ds, p_sql.replace(ob, get_tmp_name(ob)))
                rs = await async_processer.query_list_by_ds(p_ds, st.format(get_tmp_name(ob)))
                await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
                return rs
    except Exception as e:
        try:
            await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
        except:
            pass
        return process_result(str(e))

async def get_col_not_null_multi(p_ds,p_sql,config):
    try:
        ob = get_obj_name(p_sql)
        op = get_obj_op(p_sql)
        tb = await f_get_table_ddl(p_ds, ob)
        dp = 'drop table {}'
        st = '''SELECT table_name,column_name,CASE WHEN is_nullable='YES' THEN 0 ELSE 1 END 
                 FROM information_schema.columns WHERE UPPER(table_schema)=DATABASE() AND UPPER(table_name) = upper('{}')'''

        if op == 'CREATE_TABLE':
            await async_processer.exec_sql_by_ds(p_ds, p_sql)
            rs = await async_processer.query_list_by_ds(p_ds, st.format(ob))
            config[ob] = dp.format(ob)
            return rs
        elif op in('ALTER_TABLE_ADD'):
            if config.get(get_tmp_name(ob)) is None:
                await async_processer.exec_sql_by_ds(p_ds, tb.replace(ob, get_tmp_name(ob)))
                await async_processer.exec_sql_by_ds(p_ds, p_sql.replace(ob, get_tmp_name(ob)))
                rs = await async_processer.query_list_by_ds(p_ds, st.format(get_tmp_name(ob)))
                config[get_tmp_name(ob)] = dp.format('dbops_' + dp)
                return rs
    except Exception as e:
        return process_result(str(e))

async def get_obj_pk_exists_auto_incr(p_ds,p_sql):
    ob = get_obj_name(p_sql)
    dp = 'drop table {}'
    st = """SELECT count(0) FROM  information_schema.columns 
              WHERE UPPER(table_schema)=DATABASE() AND UPPER(table_name)='{}'
                 AND column_key='PRI' AND extra='auto_increment'"""
    if await check_mysql_tab_exists(p_ds, ob) > 0:
        return '表:{0}已存在!'.format(ob)
    else:
        await async_processer.exec_sql_by_ds(p_ds, p_sql)
        rs = await async_processer.query_one_by_ds(p_ds, st.format(ob))
        await async_processer.exec_sql_by_ds(p_ds, dp.format(ob))
        return rs[0]

async def get_obj_pk_exists_auto_incr_multi(p_ds,p_sql,config):
    try:
        ob = get_obj_name(p_sql)
        op = get_obj_op(p_sql)
        dp = 'drop table {}'
        st = """SELECT count(0)
                 FROM information_schema.columns   
                  WHERE UPPER(table_schema)=DATABASE()  AND UPPER(table_name)='{}'
                    AND column_key='PRI' AND extra='auto_increment'"""

        if op == 'CREATE_TABLE':
            rs = await async_processer.query_one_by_ds(p_ds, st.format(ob))
            config[ob] = dp.format(ob)
            return rs[0]
    except Exception as e:
        return process_result(str(e))

async def get_obj_pk_type_not_int_bigint(p_ds,p_sql):
    try:
        ob = get_obj_name(p_sql)
        dp = 'drop table {}'
        st = """SELECT data_type FROM  information_schema.columns   
                 WHERE UPPER(table_schema)=DATABASE()  AND UPPER(table_name)='{}' AND column_key='PRI'"""
        val = 0
        if await check_mysql_tab_exists(p_ds, ob) > 0:
            return '表:{0}已存在!'.format(ob)
        else:
            await async_processer.exec_sql_by_ds(p_ds, p_sql)
            rs = await async_processer.query_list_by_ds(p_ds, st.format(ob))
            await async_processer.exec_sql_by_ds(p_ds, dp.format(ob))
            for i in rs:
                if i[0] not in ('int', 'bigint'):
                    val = 1
                    break
            return val
    except Exception as e:
        return process_result(str(e))

async def get_obj_pk_type_not_int_bigint_multi(p_ds,p_sql,config):
    try:
        val = 0
        ob = get_obj_name(p_sql)
        dp = 'drop table {}'
        op = get_obj_op(p_sql)
        st ="""SELECT data_type FROM  information_schema.columns   
                WHERE UPPER(table_schema)=DATABASE() AND UPPER(table_name)='{}' AND column_key='PRI'"""
        if op == 'CREATE_TABLE':
            rs = await async_processer.query_list_by_ds(p_ds, st.format(ob))
            for i in rs:
                if i[0] not in('int','bigint'):
                   val=1
                   break
            config[ob] = dp.format(ob)
            return val
    except Exception as e:
        return process_result(str(e))

async def get_obj_exists_auto_incr_not_1(p_ds,p_sql):
    ob = get_obj_name(p_sql)
    dp = 'drop table {}'
    st = '''SELECT  AUTO_INCREMENT FROM  information_schema.tables   
            WHERE UPPER(table_schema)=upper(DATABASE()) AND UPPER(table_name)=upper('{}') '''
    if await check_mysql_tab_exists(p_ds, ob) > 0:
        return '表:{0}已存在!'.format(ob)
    else:
        await async_processer.exec_sql_by_ds(p_ds, p_sql)
        rs = await async_processer.query_one_by_ds(p_ds, st.format(ob))
        await async_processer.exec_sql_by_ds(p_ds, dp.format(ob))
        return rs[0]

async def get_obj_exists_auto_incr_not_1_multi(p_ds,p_sql,config):
    try:
        ob = get_obj_name(p_sql)
        op = get_obj_op(p_sql)
        st ='''SELECT  count(0)
                 FROM  information_schema.tables   
                WHERE UPPER(table_schema)=upper(DATABASE())
                  AND UPPER(table_name)=upper('{}')
                  and AUTO_INCREMENT=1'''
        if op == 'CREATE_TABLE':
            rs = await async_processer.query_one_by_ds(p_ds, st.format(ob))
            config[ob] = 'drop table {}'.format(ob)
            return rs[0]
    except Exception as e:
        return process_result(str(e))

async def process_single_ddl(p_dbid,p_cdb,p_sql,p_user):
    sxh    = 1
    res    = True
    ob     = get_obj_name(p_sql.strip())
    db     = get_db_name(p_sql.strip())
    op     = get_obj_op(p_sql.strip())
    tp     = get_obj_type(p_sql.strip())
    ds     = await get_ds_by_dsid_by_cdb(p_dbid, p_cdb)
    st     = p_sql.strip().replace("\\","\\\\")
    ru     = """select id,rule_code,rule_name,rule_value,error 
                  from t_sql_audit_rule where rule_type='ddl' and status='1' and id not in (27,28,29,30) order by id"""
    rs     = await async_processer.query_dict_list(ru)
    print('输出检测项...')
    print('-'.ljust(150, '-'))
    print('ob:{}'.format(ob))
    print('db:{}'.format(db))
    print('ds:{}'.format(ds))
    print('op:{}'.format(op))
    print('tp:{}'.format(tp))
    print('-'.ljust(150, '-'))
    for r in rs:
        print(r)
    # delete check table
    await del_check_results(p_user)
    # check sql rule
    for rule in rs:
        rule['error'] = format_sql(rule['error'])
        if rule['rule_code'] == 'switch_check_ddl' and rule['rule_value'] == 'true':
            if op in('CREATE_TABLE','ALTER_TABLE_ADD','ALTER_TABLE_DROP'):
                print('检测DDL语法及权限...')
                v = await get_obj_privs_grammar(ds,st)
                if v != '0':
                    rule['error'] = format_sql(v)
                    await save_check_results(rule, p_user, st, sxh)
                    res = False
                    break

        if rule['rule_code'] == 'switch_tab_not_exists_pk' and rule['rule_value'] == 'true':
            if op == 'CREATE_TABLE':
                print('检查表必须为主键...')
                if tp == 'TABLE' and not (p_sql.upper().count('PRIMARY') > 0 and p_sql.upper().count('KEY') > 0):
                    rule['error'] = rule['error'].format(ob)
                    await save_check_results(rule, p_user,st,sxh)
                    res = False

        if rule['rule_code'] == 'switch_tab_pk_id' and rule['rule_value'] == 'true':
            if op == 'CREATE_TABLE':
                print('强制主键名为ID...')
                if tp == 'TABLE' and (p_sql.upper().count('PRIMARY') > 0 \
                        and p_sql.upper().count('KEY') > 0) and (await get_obj_pk_name(ds,st)) != 'id':
                    rule['error'] = rule['error'].format(ob)
                    await save_check_results(rule, p_user,st,sxh)
                    res = False

        if rule['rule_code'] == 'switch_tab_pk_auto_incr' and rule['rule_value'] == 'true':
            if op == 'CREATE_TABLE':
                print('强制主键为自增列...')
                if tp== 'TABLE' and (p_sql.upper().count('PRIMARY') > 0 \
                            and p_sql.upper().count('KEY') > 0) and (await get_obj_pk_exists_auto_incr(ds, p_sql)) == 0:
                    rule['error'] = rule['error'].format(get_obj_name(p_sql.strip()))
                    await save_check_results(rule, p_user,st,sxh)
                    res = False

        if rule['rule_code'] == 'switch_tab_pk_autoincrement_1' and rule['rule_value'] == 'true':
            if op == 'CREATE_TABLE':
                print('强制自增列初始值为1...')
                if tp == 'TABLE' and (p_sql.upper().count('PRIMARY') > 0  and p_sql.upper().count('KEY') > 0) \
                      and (await get_obj_exists_auto_incr_not_1(ds, p_sql)) != 1:
                    rule['error'] = rule['error'].format(ob)
                    await save_check_results(rule,p_user,st,sxh)
                    res = False

        if rule['rule_code'] == 'switch_pk_not_int_bigint' and rule['rule_value'] == 'false':
            if get_obj_op(p_sql) == 'CREATE_TABLE':
                print('不允许主键类型非int/bigint...')
                if tp == 'TABLE' and (p_sql.upper().count('PRIMARY') > 0 \
                        and p_sql.upper().count('KEY') > 0) and (await get_obj_pk_type_not_int_bigint(ds, p_sql)) > 0:
                    rule['error'] = rule['error'].format(get_obj_name(p_sql.strip()))
                    await save_check_results(rule, p_user, p_sql,sxh)
                    res = False

        if rule['rule_code'] == 'switch_tab_comment' and rule['rule_value'] == 'true':
            if op == 'CREATE_TABLE':
                print('检查表注释...')
                if tp == 'TABLE' and ((await get_tab_comment(ds, p_sql)) == 0):
                    rule['error'] = rule['error'].format(ob)
                    await save_check_results(rule, p_user, p_sql,sxh)
                    res = False

        if rule['rule_code'] == 'switch_col_comment' and rule['rule_value'] == 'true' and tp == 'TABLE':
            if get_obj_op(p_sql) in ('CREATE_TABLE', 'ALTER_TABLE_ADD'):
                print('检查列注释...')
                v = await get_col_comment(ds,st)
                e = rule['error']
                try:
                    for i in v:
                        if i[2] == 0:
                            res = False
                            rule['error'] = e.format(i[0].replace('dbops_' + get_obj_name(p_sql), get_obj_name(p_sql)),
                                                     i[1])
                            await save_check_results(rule,p_user,st,sxh)
                except:
                    res = False
                    rule['error'] = v
                    await save_check_results(rule,p_user,st,sxh)

        if rule['rule_code'] == 'switch_col_not_null' and rule['rule_value'] == 'true' and tp == 'TABLE':
            if op in ('CREATE_TABLE', 'ALTER_TABLE_ADD'):
                print('检查列是否为空...')
                v = await get_col_not_null(ds, st)
                e = rule['error']
                try:
                    for i in v:
                        if i[2] == 0:
                            res = False
                            rule['error'] = e.format(i[0].replace(get_tmp_name(ob), ob),i[1])
                            await save_check_results(rule, p_user, p_sql,sxh)
                except:
                    res = False
                    rule['error'] = v
                    await save_check_results(rule,p_user,st,sxh)

        if rule['rule_code'] == 'switch_col_default_value' and rule['rule_value'] == 'true' and tp == 'TABLE':
            if op in ('CREATE_TABLE', 'ALTER_TABLE_ADD'):
                print('检查列默认值...')
                v = await get_col_default_value(ds, st)
                e = rule['error']
                try:
                    if v is not None:
                        for i in v:
                            if i[2] == 0:
                                res = False
                                rule['error'] = e.format(i[0].replace(get_tmp_name(ob), ob),i[1])
                                await save_check_results(rule, p_user, st,sxh)
                except:
                    res = False
                    rule['error'] = v
                    await save_check_results(rule,p_user,st,sxh)

        if rule['rule_code'] == 'switch_tcol_default_value' and rule['rule_value'] == 'true' and tp == 'TABLE':
            if op in ('CREATE_TABLE'):
                print('检查时间字段默认值...')
                v = await get_time_col_default_value(ds, st)
                e = rule['error']
                try:
                    for i in v:
                        if i[3] == 0:
                            res = False
                            rule['error'] = e.format(i[0], i[1], i[2])
                            await save_check_results(rule, p_user, st,sxh)
                except:
                    res = False
                    rule['error'] = v
                    await save_check_results(rule, p_user, p_sql.strip(),sxh)

        if rule['rule_code'] == 'switch_char_max_len' and tp == 'TABLE':
            if op == 'CREATE_TABLE':
                print('字符字段最大长度...')
                v = await get_tab_char_col_len(ds,st,rule)
                e = rule['error']
                for i in v:
                    if i[2] == 0:
                        res = False
                        rule['error'] = e.format(i[0], i[1], rule['rule_value'])
                        await save_check_results(rule, p_user,st,sxh)

        if rule['rule_code'] == 'switch_tab_has_time_fields' and tp == 'TABLE':
            if op in('CREATE_TABLE','ALTER_TABLE_ADD'):
                print('表必须拥有字段...'+rule['rule_value'])
                if rule['rule_value']!='':
                    v = await get_tab_has_fields(ds, st, rule)
                    if v['code'] == 0:
                        for i in v['msg']:
                            res = False
                            rule['error'] = rule['error'].format(i[0], i[1])
                            await save_check_results(rule,p_user,st,sxh)
                    else:
                        res = False
                        rule['error'] = format_sql(v['msg'])
                        await save_check_results(rule, p_user, st, sxh)

        if rule['rule_code'] == 'switch_tab_tcol_datetime' and rule['rule_value'] == 'true' and tp == 'TABLE':
            if op == 'CREATE_TABLE':
                print('时间字段类型为datetime...')
                v = await get_tab_tcol_datetime(ds, p_sql,rule)
                e = rule['error']
                try:
                    for i in v:
                        res = False
                        rule['error'] = e.format(i[0], i[1])
                        await save_check_results(rule,p_user,st,sxh)
                except:
                    res = False
                    rule['error'] = v
                    await save_check_results(rule,p_user,st,sxh)

        if rule['rule_code'] == 'switch_tab_char_total_len' and tp == 'TABLE':
            if get_obj_op(p_sql.strip()) == 'CREATE_TABLE':
                print('字符列总长度...')
                v = await get_tab_char_col_total_len(ds, st, rule)
                if v == 0:
                    res = False
                    rule['error'] = rule['error'].format(ob, rule['rule_value'])
                    await save_check_results(rule,p_user,st,sxh)

        if rule['rule_code'] == 'switch_tab_ddl_max_rows' and tp == 'TABLE':
            if op in ('TRUNCATE_TABLE','ALTER_TABLE_ADD', 'ALTER_TABLE_DROP'):
                print('DDL最大影响行数...')
                r = await get_tab_rows(ds, st)
                if r > int(rule['rule_value']):
                    res = False
                    rule['error'] = rule['error'].format(ob,rule['rule_value'])
                    await save_check_results(rule,p_user,st,sxh)

        if rule['rule_code'] == 'switch_disable_trigger' and rule['rule_value'] == 'true':
            if get_obj_type(p_sql) == 'TRIGGER':
                res = False
                await save_check_results(rule, p_user, st, sxh)

        if rule['rule_code'] == 'switch_disable_func' and rule['rule_value'] == 'true':
            if get_obj_type(p_sql) == 'FUNCTION':
                res = False
                await save_check_results(rule, p_user, st, sxh)

        if rule['rule_code'] == 'switch_disable_proc' and rule['rule_value'] == 'true':
             if get_obj_type(p_sql) == 'PROCEDURE':
                 res = False
                 await save_check_results(rule, p_user, st, sxh)

        if rule['rule_code'] == 'switch_disable_event' and rule['rule_value'] == 'true':
             if get_obj_type(p_sql) == 'EVENT':
                 res = False
                 await save_check_results(rule, p_user, st, sxh)

        if rule['rule_code'] == 'switch_drop_database' and tp == 'DATABASE'  and rule['rule_value'] == 'false' :
            if get_obj_op(p_sql) == 'DROP_DATABASE':
               res = False
               await save_check_results(rule, p_user, st, sxh)


        if rule['rule_code'] == 'switch_drop_table' and tp == 'TABLE'  and rule['rule_value'] == 'false' :
            if get_obj_op(p_sql) in('DROP_TABLE','TRUNCATE_TABLE'):
               res = False
               await save_check_results(rule, p_user, st, sxh)


        if rule['rule_code'] == 'switch_tab_name_check' and tp == 'TABLE'  and rule['rule_value'] == 'true' :
            if get_obj_op(p_sql) == 'CREATE_TABLE':
                print('表名规范检查...')
                if not await check_tab_rule(st,p_user,sxh):
                   res = False

        if rule['rule_code'] == 'switch_idx_name_check' and tp in('TABLE','INDEX') and rule['rule_value'] == 'true':
            print('switch_idx_name_check=',get_obj_op(p_sql))
            if op in('CREATE_INDEX','ALTER_TABLE_ADD'):
                print('索引规范检查...')
                if  not await check_idx_rule(ds, st, p_user, sxh):
                    res = False

    if res:
        rule['id'] = '0'
        rule['error'] = '检测通过!'
        await save_check_results(rule, p_user, st,sxh)
    return res

async def process_single_ddl_proc(p_dbid,p_cdb,p_sql,p_user):
    print('process_single_ddl_proc...')
    sxh  = 1
    res  = True
    op   = get_obj_op(p_sql.strip())
    tp   = get_obj_type(p_sql.strip())
    ds   = get_ds_by_dsid_by_cdb(p_dbid, p_cdb)
    st   = p_sql.strip()
    ru   = """select id,rule_code,rule_name,rule_value,error 
                    from t_sql_audit_rule where rule_type='ddl' and status='1' and id in(27,28,29,30) order by id"""

    rs = await async_processer.query_list(ru)
    print('输出检测项...')
    print('-'.ljust(150, '-'))
    for r in rs:
        print(r)

    # delete check table
    del_check_results(p_user)

    # check proc
    for rule in rs:
        rule['error'] = format_sql(rule['error'])

        if rule['rule_code'] == 'switch_check_ddl' and rule['rule_value'] == 'true':
            if op in('CREATE_PROCEDURE','CREATE_FUNCTION','CREATE_TRIGGER','CREATE_EVENT'):
                print('检测过程语法及权限...')
                v = await get_obj_privs_grammar_proc(ds, st)
                if v != '0':
                    rule['error'] = format_sql(format_exception(v))
                    await save_check_results(rule, p_user, st, sxh)
                    res = False

        if rule['rule_code'] == 'switch_disable_trigger' and rule['rule_value'] == 'true':
            if tp== 'TRIGGER':
               await save_check_results(rule, p_user, st, sxh)
               res = False

        if rule['rule_code'] == 'switch_disable_func' and rule['rule_value'] == 'true':
            if tp == 'FUNCTION':
               await save_check_results(rule, p_user, st, sxh)
               res = False

        if rule['rule_code'] == 'switch_disable_proc' and rule['rule_value'] == 'true':
             if tp== 'PROCEDURE':
                await save_check_results(rule, p_user,st, sxh)
                res = False

        if rule['rule_code'] == 'switch_disable_event' and rule['rule_value'] == 'true':
             if tp == 'EVENT':
                await save_check_results(rule, p_user, st, sxh)
                res = False

    if res:
        rule['id'] = '0'
        rule['error'] = '检测通过!'
        await save_check_results(rule, p_user, st,sxh)
    return res

def get_tmp_name(ob):
    o = ob.replace('`','')
    return """{}""".format(ob.replace(o,'dbops_' + o))

async def get_dml_privs_grammar(p_ds,p_sql):
    ob = get_obj_name(p_sql.strip())
    db = p_ds['service'] + '.'
    op = get_obj_op(p_sql)
    tb = await f_get_table_ddl(p_ds, ob)
    dp = 'drop table {}'
    try:
        if op in ('INSERT','UPDATE','DELETE'):
            if await check_mysql_tab_exists(p_ds, ob) == 0:
               return '表:{0}不存在!'.format(ob)
            else:
               await async_processer.exec_sql_by_ds(p_ds, tb.replace(ob, get_tmp_name(ob)))
               await async_processer.exec_sql_by_ds(p_ds, p_sql.replace(db,'').replace(ob, get_tmp_name(ob)))
               await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
               return None
    except Exception as e:
        traceback.print_exc()
        try:
            await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
        except:
            pass
        return process_result(str(e))

async def get_dml_rows(p_ds,p_sql):
    ob = get_obj_name(p_sql.strip())
    db = p_ds['service'] + '.'
    op = get_obj_op(p_sql)
    tb = await f_get_table_ddl(p_ds, ob)
    dp = 'drop table {}'
    try:
        if await check_mysql_tab_exists(p_ds, ob) == 0:
            return '表:{0}不存在!'.format(ob)

        if op == 'INSERT':
           await async_processer.exec_sql_by_ds(p_ds, tb.replace(ob, get_tmp_name(ob)))
           await async_processer.exec_sql_by_ds(p_ds, p_sql.replace(db,'').replace(ob, get_tmp_name(ob)))
           st = 'select count(0) from {0}'.format(get_tmp_name(ob))
           rs = await async_processer.query_one_by_ds(p_ds,st)
           await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
           return rs[0]
        elif op in('UPDATE'):
           if p_sql.upper().find('WHERE')>=0:
               tb = re.split(r'\s+', p_sql)[1]
               if re.split(r'\s+', p_sql)[2].upper()!='SET':
                  tb = tb +' '+ re.split(r'\s+', p_sql)[2]
               vv = p_sql[p_sql.upper().find('WHERE'):]
               st = """select count(0) from {0} {1}""".format(tb,vv)
               # print('tb=',tb)
               # print('vv=',vv)
               # print('st=',st)
           else:
               st = """select count(0) from {0}""". \
                   format(p_sql[6:p_sql.upper().find('SET')-1].strip())
           rs = await async_processer.query_one_by_ds(p_ds, st)
           if rs[0] == 0:
               return '表:{0}更新0行!'.format(ob)
           else:
               return rs[0]
        elif op in ('DELETE'):
            pattern = re.compile(r'(\s*delete\s*)',re.I)
            if pattern.findall(p_sql) != []:
                st = re.sub(pattern, "SELECT count(0) ", p_sql)
            else:
                st = p_sql
            rs = await async_processer.query_one_by_ds(p_ds, st)
            if rs[0] == 0:
                return '表:{0}删除0行!'.format(ob)
            else:
                return rs[0]

    except Exception as e:
        try:
            await async_processer.exec_sql_by_ds(p_ds, dp.format(get_tmp_name(ob)))
        except:
            pass
        return process_result(str(e))

async def process_single_dml(p_dbid,p_cdb,p_sql,p_user):
    sxh  = 1
    res  = True
    op   = get_obj_op(p_sql.strip())
    print('op=',op)
    ds   = await get_ds_by_dsid_by_cdb(p_dbid, p_cdb)
    st   = p_sql.strip()
    ru   = """select id,rule_code,rule_name,rule_value,error 
                from t_sql_audit_rule where  rule_type='dml' and status='1'  order by id"""
    rs   = await async_processer.query_dict_list(ru)

    print('输出检测项...op=',op)
    print('-'.ljust(150, '-'))
    for r in rs:
        print(r)
    # delete table result
    await del_check_results(p_user)
    # check sql
    for rule in rs:
        rule['error'] = format_sql(rule['error'])

        if op is None :
            await save_check_results_exception('非法DML语句!', p_user, st, sxh)
            res = False
            break

        if rule['rule_code'] == 'switch_dml_where' and rule['rule_value'] == 'true':
            if op in('UPDATE','DELETE'):
               print('检测DML语句条件...')
               match = re.search(r'(\s*where\s*)',p_sql.upper().strip(),re.IGNORECASE)
               if  match is None or match.group() is None:
                    await save_check_results(rule,p_user, st,sxh)
                    res = False

        if rule['rule_code'] == 'switch_dml_order' and rule['rule_value'] == 'true':
            if op in('UPDATE','DELETE'):
               print('DML语句禁用 ORDER BY...')
               if re.search('\s+ORDER\s+BY\s+', st.upper()) is not None:
                  await save_check_results(rule,p_user,st,sxh)
                  res = False

        if rule['rule_code'] == 'switch_dml_select' and rule['rule_value'] == 'true':
            if op in('INSERT','UPDATE','DELETE'):
               print('DML语句禁用 SELECT...')
               if re.search('SELECT\s+', st.upper()) is not None and re.search('\s+FROM\s+', st.upper()) is not None:
                  await save_check_results(rule, p_user,st,sxh)
                  res = False

        if rule['rule_code'] == 'switch_dml_max_rows':
            if op in('INSERT','UPDATE','DELETE'):
               print('DML最大影响行数...')
               v =  await get_dml_rows(ds,st)
               if is_number(str(v)):
                   if v > int(rule['rule_value']):
                      rule['error'] = rule['error'].format(rule['rule_value'])
                      await save_check_results(rule,p_user,st,sxh)
                      res = False
               else:
                   rule['error'] = format_sql(format_exception(v))
                   await save_check_results(rule, p_user,st,sxh)
                   res = False

        if rule['rule_code'] == 'switch_dml_ins_exists_col' and rule['rule_value'] == 'true':
            if op in('INSERT'):
               print('检查插入语句那必须存在列名...')
               n_pos1 = re.split(r'\s+', p_sql.strip())[2].count('(')
               n_pos2 = re.split(r'\s+', p_sql.strip())[3].count('(')
               if n_pos1 == 0 and n_pos2 ==0:
                   await save_check_results(rule, p_user,st,sxh)
                   res = False

        if rule['rule_code'] == 'switch_dml_ins_cols':
            ck = await get_audit_rule('switch_dml_ins_exists_col')
            if ck['rule_value'] == 'true':
               if op in ('INSERT'):
                   print('INSERT语句字段上限...')
                   try:
                       n_cols = re.split(r'\s+',  p_sql.strip())[2].split('(')[1].split(')')[0].count(',')+1
                   except:
                       n_cols = re.split(r'\s+', p_sql.strip())[3].split('(')[1].split(')')[0].count(',')+1
                   if n_cols>int(rule['rule_value']):
                      rule['error'] =rule['error'].format(rule['rule_value'])
                      await save_check_results(rule, p_user, st, sxh)
                      res = False

        if res:
            if rule['rule_code'] == 'switch_check_dml' and rule['rule_value'] == 'true':
                if op in ('INSERT', 'UPDATE', 'DELETE'):
                    print('检测DML语法及权限...')
                    v = await get_dml_privs_grammar(ds, st)
                    if v is not None:
                        rule['error'] = format_sql(format_exception(v))
                        await save_check_results(rule, p_user,st,sxh)
                        res = False

    if res:
        rule['id'] = '0'
        rule['error'] = '检测通过!'
        await save_check_results(rule, p_user, st,sxh)

    return res

# def preProcesses(matched):
#     value = matched.group(0)
#     return value.replace(';','^^^')

# def reReplace(p_sql):
#     p_sql_pre=p_sql
#     pattern0 = re.compile(r'(COMMENT\s+\'[^\']*;[^\']*\')')
#     if pattern0.findall(p_sql) != []:
#        logging.info('一: 将comment中的;替换为^^^ ...')
#        p_sql_pre = re.sub(pattern0,preProcesses,p_sql)
#        logging.info(('1:',p_sql_pre))
#
#     pattern1 = re.compile(r'(\s*\)\s*;\s*)')
#     if pattern1.findall(p_sql_pre)!=[]:
#        logging.info('二: 将);替换为)$$$ ...')
#        p_sql_pre = re.sub(pattern1, ')$$$', p_sql_pre)
#        logging.info(('2:', p_sql_pre))
#
#     pattern2 = re.compile(r'(\s*\'\s*;\s*)')
#     if pattern2.findall(p_sql_pre) != []:
#        logging.info('三: 将\';替换为\'$$$ ...')
#        p_sql_pre = re.sub(pattern2, "'$$$", p_sql_pre)
#        logging.info(('3:', p_sql_pre))
#
#     pattern3 = re.compile(r'(\s*;\s*)')
#     if pattern3.findall(p_sql_pre) != []:
#         logging.info('四: 将;替换为$$$')
#         p_sql_pre = re.sub(pattern3, "$$$\n", p_sql_pre)
#         logging.info(('4:', p_sql_pre))
#
#     logging.info('五: 通过$$$将p_sql_pre处理为列表...')
#     p_sql_pre = [i for i in p_sql_pre.split('$$$') if (i != '' and i!='\n')]
#     logging.info(('5=', p_sql_pre))
#     logging.info('5-len=', len(p_sql_pre))
#
#     logging.info(('六: 将列表中每个语句comment中的^^^替为;...'))
#     p_sql_pre = [i.replace('^^^', ';') for i in p_sql_pre]
#     logging.info(('6=', p_sql_pre))
#     logging.info(('6-len=', len(p_sql_pre)))
#
#     if len(p_sql_pre) == 1:
#        return [p_sql]
#     else:
#        return  p_sql_pre

def check_statement_count(p_sql):
    out = [i for i in reReplace(p_sql) if i != '']
    logging.info(('check_statement_count=>p_sql:',p_sql))
    logging.info(('check_statement_count=>out:',out))
    logging.info(('check_statement_count=>len:',len(out)))
    return len(out)

async def process_multi_ddl(p_dbid,p_cdb,p_sql,p_user):
    sxh  = 1
    rss  = True
    cfg  = {}
    ds   = await get_ds_by_dsid_by_cdb(p_dbid, p_cdb)

    # delete check table
    await del_check_results(p_user)

    # check dml sql
    for s in reReplace(p_sql.replace("\\","\\\\")):
        ob  = get_obj_name(s.strip())
        op  = get_obj_op(s.strip())
        tp  = get_obj_type(s.strip())
        st  = s.strip()
        res = True

        if st.strip() == '':
           continue

        print('check sql :',st.strip())
        ru = """select id,rule_code,rule_name,rule_value,error from t_sql_audit_rule
                  where  rule_type='ddl' and status='1' and id not in (27,28,29,30) order by id"""
        rs = await async_processer.query_dict_list(ru)

        print('输出检测项...')
        print('-'.ljust(150, '-'))
        for r in rs:
            print(r)

        for rule in rs:
            rule['error'] = format_sql(rule['error'])
            if rule['rule_code'] == 'switch_check_ddl' and rule['rule_value'] == 'true':
                if tp == 'TABLE':
                    print('检测DDL语法及权限...')
                    v = await get_obj_privs_grammar_multi(ds,st,cfg)
                    print(' 检测DDL语法及权限 v=',v)
                    if v != '0':
                       rule['error'] = format_sql(format_exception(v))
                       await save_check_results(rule, p_user,st,sxh)
                       res = False

            if rule['rule_code'] == 'switch_tab_not_exists_pk' and rule['rule_value'] == 'true':
                if op == 'CREATE_TABLE':
                    print('检查表必须有主键...')
                    if tp == 'TABLE' and not (st.upper().count('PRIMARY') > 0 and st.upper().count('KEY') > 0):
                        rule['error'] =rule['error'].format(ob)
                        await save_check_results(rule, p_user,st,sxh)
                        res = False

            if rule['rule_code'] == 'switch_tab_pk_id' and rule['rule_value'] == 'true':
                if op == 'CREATE_TABLE':
                    print('强制主键名为ID...')
                    if tp== 'TABLE' and (st.upper().count('PRIMARY') > 0 and st.upper().count('KEY') > 0) :
                       v  = await get_obj_pk_name_multi(ds,st,cfg)
                       if v == 0:
                            rule['error'] = rule['error'].format(ob)
                            await save_check_results(rule,p_user, st,sxh)
                            res = False

                       if v not in (0,1):
                           rule['error'] = v
                           await save_check_results(rule,p_user,st,sxh)
                           res = False

            if rule['rule_code'] == 'switch_tab_pk_auto_incr' and rule['rule_value'] == 'true':
                if op == 'CREATE_TABLE':
                    print('强制主键为自增列...')
                    if get_obj_type(st.strip()) == 'TABLE' and (st.upper().count('PRIMARY') > 0 and st.upper().count('KEY') > 0) :
                        v =  await get_obj_pk_exists_auto_incr_multi(ds, st.strip(),cfg)
                        if v == 0 :
                            rule['error'] = rule['error'].format(ob)
                            await save_check_results(rule, p_user, st,sxh)
                            res = False

                        if v not in (0, 1):
                            rule['error'] = v
                            await save_check_results(rule, p_user,st,sxh)
                            res = False

            if rule['rule_code'] == 'switch_tab_pk_autoincrement_1' and rule['rule_value'] == 'true':
                if op == 'CREATE_TABLE':
                    print('强制自增列初始值为1...')
                    if tp == 'TABLE' and (st.upper().count('PRIMARY') > 0  and st.upper().count('KEY') > 0):
                        v =  await get_obj_exists_auto_incr_not_1_multi(ds, st,cfg)
                        if v == 0:
                            rule['error'] = rule['error'].format(ob)
                            await save_check_results(rule,p_user,st,sxh)
                            res = False

                        if v not in (0, 1):
                            rule['error'] = v
                            await save_check_results(rule,p_user,st,sxh)
                            res = False

            if rule['rule_code'] == 'switch_pk_not_int_bigint' and rule['rule_value'] == 'false':
                if op == 'CREATE_TABLE':
                    print('不允许主键类型非int/bigint...')
                    if tp == 'TABLE' and (st.upper().count('PRIMARY') > 0 and st.upper().count('KEY') > 0):
                        v =  await get_obj_pk_type_not_int_bigint_multi(ds, st,cfg)
                        if v == 1 :
                            rule['error'] = rule['error'].format(ob)
                            await save_check_results(rule,p_user,st,sxh)
                            res = False

                        if v not in (0, 1):
                            rule['error'] = v
                            await save_check_results(rule,p_user, st,sxh)
                            res = False

            if rule['rule_code'] == 'switch_tab_comment' and rule['rule_value'] == 'true':
                if op == 'CREATE_TABLE':
                    print('检查表注释...')
                    if tp == 'TABLE':
                        v = await get_tab_comment_multi(ds,st,cfg)
                        if v ==0:
                            rule['error'] = rule['error'].format(ob)
                            await save_check_results(rule,p_user,st,sxh)
                            res = False

                        if v not in (0, 1):
                            rule['error'] = v
                            await save_check_results(rule,p_user,st,sxh)
                            res = False

            if rule['rule_code'] == 'switch_col_comment'  and rule['rule_value'] == 'true' and tp == 'TABLE':
               if op in ('CREATE_TABLE', 'ALTER_TABLE_ADD'):
                    print('检查列注释...')
                    v = await get_col_comment_multi(ds, st,cfg)
                    e = rule['error']
                    try:
                        for i in v:
                            if i[2] == 0:
                                res = False
                                rule['error'] = e.format(i[0].replace('dbops_'+ ob,ob),i[1])
                                await save_check_results(rule, p_user,st,sxh)
                    except:
                        res = False
                        rule['error'] = v
                        await save_check_results(rule, p_user,st,sxh)

            if rule['rule_code'] == 'switch_col_not_null' and rule['rule_value'] == 'true' and tp == 'TABLE':
                if op in ('CREATE_TABLE', 'ALTER_TABLE_ADD'):
                    print('检查列是否为空...')
                    v = await get_col_not_null_multi(ds, st,cfg)
                    e = rule['error']
                    try:
                        for i in v:
                            if i[2] == 0:
                                result = False
                                rule['error'] = e.format(i[0].replace(get_tmp_name(ob), ob),i[1])
                                await save_check_results(rule, p_user,st,sxh)
                    except:
                        result = False
                        rule['error'] = v
                        await save_check_results(rule, p_user, st,sxh)

            if rule['rule_code'] == 'switch_col_default_value' and rule['rule_value'] == 'true' and tp == 'TABLE':
                if op in ('CREATE_TABLE', 'ALTER_TABLE_ADD'):
                    print('检查列默认值...')
                    v = await get_col_default_value_multi(ds, st,cfg)
                    e = rule['error']
                    try:
                        for i in v:
                            if i[2] == 0:
                                res = False
                                rule['error'] = e.format(i[0].replace('dbops_'+ob, ob),i[1])
                                await save_check_results(rule,p_user,st,sxh)
                    except:
                        res = False
                        rule['error'] = v
                        await save_check_results(rule, p_user, st,sxh)

            if rule['rule_code'] == 'switch_tcol_default_value' and rule['rule_value'] == 'true' and tp == 'TABLE':
                if op in ('CREATE_TABLE'):
                    print('检查时间字段默认值...')
                    v = await get_time_col_default_value_multi(ds, st,cfg)
                    e = rule['error']
                    try:
                        for i in v:
                            if i[3] == 0:
                                res = False
                                rule['error'] = e.format(i[0], i[1], i[2])
                                await save_check_results(rule, p_user,st,sxh)
                    except:
                        res = False
                        rule['error'] = v
                        await save_check_results(rule, p_user,st,sxh)

            if rule['rule_code'] == 'switch_char_max_len' and tp== 'TABLE':
                if op == 'CREATE_TABLE':
                    print('字符字段最大长度...')
                    v = await get_tab_char_col_len_multi(ds, st,rule,cfg)
                    e = rule['error']
                    try:
                        for i in v:
                            if i[2] == 0:
                                res = False
                                rule['error'] = e.format(i[0], i[1], rule['rule_value'])
                                await save_check_results(ds, rule, p_user, st,sxh)
                    except:
                        res = False
                        rule['error'] = v
                        await save_check_results(rule, p_user, st,sxh)

            if rule['rule_code'] == 'switch_tab_has_time_fields' and tp == 'TABLE':
                if op == 'CREATE_TABLE':
                    print('表必须拥有字段...')
                    if rule['rule_value'] != '':
                        v = await get_tab_has_fields_multi(ds, st,rule,cfg)
                        e = rule['error']
                        try:
                            for i in v:
                                res = False
                                rule['error'] = e.format(i[0], i[1])
                                await save_check_results(rule, p_user,st,sxh)
                        except:
                            res = False
                            rule['error'] = v
                            await save_check_results(rule,p_user, st,sxh)

            if rule['rule_code'] == 'switch_tab_tcol_datetime' and rule['rule_value'] == 'true' and tp == 'TABLE':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('时间字段类型为datetime...')
                    v = await get_tab_tcol_datetime_multi(ds, st,cfg)
                    print('时间字段类型为datetime:',v)
                    e = rule['error']
                    try:
                        for i in v:
                            res = False
                            rule['error'] = e.format(i[0], i[1])
                            await save_check_results(rule, p_user,st,sxh)
                    except:
                        res = False
                        rule['error'] = v
                        await save_check_results(rule, p_user,st,sxh)

            if rule['rule_code'] == 'switch_disable_func' and rule['rule_value'] == 'true':
                if get_obj_type(p_sql) == 'FUNCTION':
                    res = False
                    await save_check_results(rule, p_user, st, sxh)

            if rule['rule_code'] == 'switch_disable_proc' and rule['rule_value'] == 'true':
                if get_obj_type(p_sql) == 'PROCEDURE':
                    res = False
                    await save_check_results(rule, p_user, st, sxh)

            if rule['rule_code'] == 'switch_disable_event' and rule['rule_value'] == 'true':
                if get_obj_type(p_sql) == 'EVENT':
                    res = False
                    await save_check_results(rule, p_user, st, sxh)

            if rule['rule_code'] == 'switch_drop_database' and tp == 'DATABASE' and rule['rule_value'] == 'false':
                if get_obj_op(p_sql) == 'DROP_DATABASE':
                    res = False
                    await save_check_results(rule, p_user, st, sxh)

            if rule['rule_code'] == 'switch_drop_table' and tp == 'TABLE' and rule['rule_value'] == 'false':
                if get_obj_op(p_sql) in ('DROP_TABLE', 'TRUNCATE_TABLE'):
                    res = False
                    await save_check_results(rule, p_user, st, sxh)


        print('res=',res,ob)
        if res:
           rule['id'] = '0'
           rule['error'] = '检测通过!'
           await save_check_results(rule,p_user,st,sxh)
        rss = rss and  res
        sxh = sxh +1

    print('删除临时表...')
    print('cfg=', cfg, type(cfg))
    print('-'.ljust(150, '-'))
    for key in cfg:
       try:
          print(cfg[key])
          await async_processer.exec_sql_by_ds(ds,cfg[key])
       except Exception as e:
          traceback.print_exc()
    print('-'.ljust(150, '-')+'\n')
    return rss

async def process_multi_dml(p_dbid,p_cdb,p_sql,p_user):
    sxh  = 1
    rss  = True
    cfg  = {}
    ds   = await get_ds_by_dsid_by_cdb(p_dbid, p_cdb)

    # delete check table
    await del_check_results(p_user)

    #逐条检查语句
    for s in reReplace(p_sql):
        ob  = get_obj_name(s.strip())
        op  = get_obj_op(s.strip())
        tp  = get_obj_type(s.strip())
        st  = s.strip()
        res = True
        if st.strip() == '':
           continue

        print('check sql :',st.strip())
        ru = """select id,rule_code,rule_name,rule_value,error 
                        from t_sql_audit_rule where rule_type='dml' and status='1' order by id"""
        rs = await async_processer.query_dict_list(ru)

        print('输出检测项...')
        print('-'.ljust(150, '-'))
        for r in rs:
            print(r)

        # 逐个SQL进行检测
        for rule in rs:
            rule['error'] = format_sql(rule['error'])
            if rule['rule_code'] == 'switch_dml_where' and rule['rule_value'] == 'true':
                if op in ('UPDATE', 'DELETE'):
                    print('检测DML语句条件...')
                    match = re.search(r'(\s*where\s*)', st.upper().strip(), re.IGNORECASE)
                    if match is None:
                        await save_check_results(rule, p_user, st, sxh)
                        res = False

            if rule['rule_code'] == 'switch_dml_order' and rule['rule_value'] == 'true':
                if op in ('UPDATE', 'DELETE'):
                    print('DML语句禁用 ORDER BY...')
                    if re.search('\s+ORDER\s+BY\s+', st.upper()) is not None:
                        await save_check_results(rule, p_user, st, sxh)
                        res = False

            if rule['rule_code'] == 'switch_dml_select' and rule['rule_value'] == 'true':
                if op in ('INSERT', 'UPDATE', 'DELETE'):
                    print('DML语句禁用 SELECT...')
                    if re.search('SELECT\s+', st.upper()) is not None and re.search('\s+FROM\s+',st.upper()) is not None:
                        await save_check_results(rule, p_user, st, sxh)
                        res = False

            if rule['rule_code'] == 'switch_dml_max_rows':
                if op in ('INSERT', 'UPDATE', 'DELETE'):
                    print('DML最大影响行数...')
                    v = await get_dml_rows(ds, st)
                    if is_number(str(v)):
                        if v > int(rule['rule_value']):
                            rule['error'] = rule['error'].format(rule['rule_value'])
                            await save_check_results(rule, p_user, st, sxh)
                            res = False
                    else:
                        rule['error'] = format_sql(format_exception(v))
                        await save_check_results(rule, p_user, st, sxh)
                        res = False

            if rule['rule_code'] == 'switch_dml_ins_exists_col' and rule['rule_value'] == 'true':
                if op in ('INSERT'):
                    print('检查插入语句那必须存在列名...')
                    n_pos1 = re.split(r'\s+', st.strip())[2].count('(')
                    n_pos2 = re.split(r'\s+', st.strip())[3].count('(')
                    if n_pos1 == 0 and n_pos2 == 0:
                        await save_check_results(rule, p_user, st, sxh)
                        res = False

            if rule['rule_code'] == 'switch_dml_ins_cols':
                ck = await get_audit_rule('switch_dml_ins_exists_col')
                if ck['rule_value'] == 'true':
                    if op in ('INSERT'):
                        print('INSERT语句字段上限...')
                        try:
                            n_cols = re.split(r'\s+', st.strip())[2].split('(')[1].split(')')[0].count(',') + 1
                        except:
                            n_cols = re.split(r'\s+', st.strip())[3].split('(')[1].split(')')[0].count(',') + 1
                        if n_cols > int(rule['rule_value']):
                            rule['error'] = rule['error'].format(rule['rule_value'])
                            await save_check_results(rule, p_user, st, sxh)
                            res = False

            if res:
                if rule['rule_code'] == 'switch_check_dml' and rule['rule_value'] == 'true':
                    if op in ('INSERT', 'UPDATE', 'DELETE'):
                        print('检测DML语法及权限...')
                        v = await get_dml_privs_grammar(ds, st)
                        if v is not None:
                            rule['error'] = format_sql(format_exception(v))
                            await save_check_results(rule, p_user, st, sxh)
                            res = False

        if res:
            rule['id'] = '0'
            rule['error'] = '检测通过!'
            await save_check_results(rule, p_user, st, sxh)

        rss = rss and res
        sxh = sxh + 1
    return rss

async def get_audit_rule(p_key):
    sql = "select * from t_sql_audit_rule where rule_code='{0}'".format(p_key)
    return await async_processer.query_dict_one(sql)

async def save_check_results(rule,user,psql,sxh):
    print('检查结果：')
    print('-'.ljust(150, '-'))
    obj = get_obj_name(psql)
    if rule['error'] == '检测通过!':
        sql = '''insert into t_sql_audit_rule_err(xh,obj_name,rule_id,rule_name,rule_value,user_id,error) values ('{}','{}','{}','{}','{}','{}','{}')
              '''.format(sxh, obj,'', '', '', user['userid'],rule['error'])
    else:
        sql = '''insert into t_sql_audit_rule_err(xh,obj_name,rule_id,rule_name,rule_value,user_id,error) values ('{}','{}','{}','{}','{}','{}','{}')
              '''.format(sxh,obj,rule['id'],rule['rule_name'],rule['rule_value'],user['userid'],rule['error'])
    print('save_check_results=',sql)
    await async_processer.exec_sql(sql)

async def save_check_results_exception(error,user,psql,sxh):
    print('检查结果：save_check_results_exception')
    print('-'.ljust(150, '-'))
    sql = '''insert into t_sql_audit_rule_err(xh,obj_name,rule_id,rule_name,rule_value,user_id,error) values ('{}','{}','{}','{}','{}','{}','{}')
          '''.format(sxh, '','', '', '', user['userid'],error)
    print('save_check_results=',sql)
    await async_processer.exec_sql(sql)

async def save_check_results_multi(rule,user,psql,sxh):
    print('检查结果multi:')
    print('-'.ljust(150, '-'))
    if psql == '---':
       sql = '''insert into t_sql_audit_rule_err(xh,obj_name,rule_id,rule_name,rule_value,user_id,error) values ('{}','{}','{}','{}','{}','{}','{}')
             '''.format(sxh,'',rule['id'],rule['rule_name'],rule['rule_value'],user['userid'],rule['error'])
       await async_processer.exec_sql(sql)

async def check_mysql_ddl(p_dbid,p_cdb,p_sql,p_user,p_type):
    await del_check_results(p_user)
    # TYPE: FUNC\PROC\TRI\EVENT
    if p_type == '4':
        print('process_single_ddl....')
        return await process_single_ddl_proc(p_dbid, p_cdb, p_sql.strip(), p_user)
    else:
        # TYPE:DDL、DML、DCL
        if check_statement_count(p_sql) ==1:
            # SINGLE DDL
            if p_type in('1','3'):
               print('process_single_ddl....')
               return await process_single_ddl(p_dbid,p_cdb,p_sql.strip(),p_user)
            # SINGLE DML
            elif p_type == '2':
               print('process_single_dml....')
               return await process_single_dml(p_dbid, p_cdb, p_sql.strip(), p_user)

        # TYPE: MULTI DDL、DML、DCL
        if check_statement_count(p_sql) >1:
            # MULTI DDL
            if p_type in('1','3'):
                rule = await get_audit_rule('switch_ddl_batch')
                if rule['rule_value'] == 'true':
                   print('process_multi_ddl....')
                   return await process_multi_ddl(p_dbid, p_cdb, p_sql.strip(), p_user)
                else:
                   rule['error'] = format_sql(rule['error'])
                   await save_check_results_multi(rule, p_user, '---', 1)
                   return False
            # MULTI DML
            elif p_type == '2':
                rule = await get_audit_rule('switch_dml_batch')
                if rule['rule_value'] == 'true':
                    print('process_multi_dml....')
                    return await process_multi_dml(p_dbid, p_cdb, p_sql.strip(), p_user)
                else:
                    rule['error'] = format_sql(rule['error'])
                    await save_check_results_multi(rule, p_user, '---', 1)
                    return False
