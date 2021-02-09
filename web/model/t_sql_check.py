#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/12/2 11:57
# @Author : ma.fei
# @File : t_sql_check.py.py
# @Software: PyCharm

import re
import traceback
from web.model.t_ds    import get_ds_by_dsid,get_ds_by_dsid_by_cdb
from web.utils.common  import get_connection_dict,get_connection,get_connection_ds,format_sql,format_exception


def check_mysql_tab_exists(db,tab):
   cr=db.cursor()
   sql="""select count(0) from information_schema.tables
            where table_schema=database() and table_name='{0}'""".format(tab )
   cr.execute(sql)
   rs=cr.fetchone()
   cr.close()
   db.commit()
   return rs[0]

def check_mysql_proc_exists(db,tab):
   cr=db.cursor()
   sql="""select count(0) from information_schema.tables
            where table_schema=database() and table_name='{0}'""".format(tab )
   cr.execute(sql)
   rs=cr.fetchone()
   cr.close()
   db.commit()
   return rs[0]

def process_result(v):
    if isinstance(v, tuple):
        if len(v)==1:
           return str(v)
        else:
           return 'code:{0},error:{1}'.format(str(v[0]),str(v[1]))
    else:
        return v

def query_check_result(user):
    db = get_connection()
    cr = db.cursor()
    sql = """select xh,obj_name,rule_id,rule_name,rule_value,error 
                from  t_sql_audit_rule_err where user_id={} order by id""".format(user['userid'])
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def del_check_results(db,user):
    cr  = db.cursor()
    sql = 'delete from t_sql_audit_rule_err where user_id={}'.format(user['userid'])
    cr.execute(sql)
    db.commit()

def get_obj_name(p_sql):
    if p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("TABLE") > 0 \
        or p_sql.upper().count("TRUNCATE") > 0 and p_sql.upper().count("TABLE") > 0 \
         or p_sql.upper().count("ALTER") > 0 and p_sql.upper().count("TABLE") > 0 \
           or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("TABLE") > 0 \
             or  p_sql.upper().count("CREATE")>0 and p_sql.upper().count("VIEW")>0 \
               or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("FUNCTION") > 0 \
                or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("PROCEDURE") > 0 \
                  or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("INDEX") > 0 \
                    or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("TRIGGER") > 0  :

       if p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("INDEX") > 0 and p_sql.upper().count("UNIQUE") > 0:
           obj = re.split(r'\s+', p_sql)[3].replace('`', '')
       else:
           obj=re.split(r'\s+', p_sql)[2].replace('`', '')

       if ('(') in obj:
          return obj.split('(')[0]
       else:
          return obj

    if get_obj_op(p_sql) in('INSERT','DELETE'):
         return  re.split(r'\s+', p_sql.strip())[2].split('(')[0].strip().replace('`','')

    if get_obj_op(p_sql) in('UPDATE'):
         return re.split(r'\s+', p_sql.strip())[1].split('(')[0].strip().replace('`','')



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
      or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("VIEW") > 0 \
        or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("FUNCTION") > 0 \
          or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("PROCEDURE") > 0 \
            or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("INDEX") > 0 \
              or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("EVENT") > 0 \
                or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("TRIGGER") > 0:

       # if p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("INDEX") > 0 and p_sql.upper().count("UNIQUE") > 0:
       #     obj = 'UNIQUE-INDEX'
       # elif p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("INDEX") > 0 and len(p_sql.upper().split('ON')[1].split('(')[1].replace(')','').split(','))>1:
       #     obj = 'COMPOSITE-INDEX'
       # else:
       #     obj=re.split(r'\s+', p_sql)[1].replace('`', '')

       obj = re.split(r'\s+', p_sql)[1].replace('`', '')

       if ('(') in obj:
          return obj.split('(')[0].upper()
       else:
          return obj.upper()
    else:
       return ''

def get_obj_op(p_sql):
    if re.split(r'\s+', p_sql)[0].upper() in('CREATE','DROP') and re.split(r'\s+', p_sql)[1].upper() in('TABLE','INDEX'):
       return re.split(r'\s+', p_sql)[0].upper()+'_'+re.split(r'\s+', p_sql)[1].upper()
    if re.split(r'\s+', p_sql)[0].upper() in('TRUNCATE'):
       return 'TRUNCATE_TABLE'

    if re.split(r'\s+', p_sql)[0].upper()== 'ALTER' and re.split(r'\s+', p_sql)[1].upper()=='TABLE' and  re.split(r'\s+', p_sql)[3].upper() in('ADD','DROP'):
       return re.split(r'\s+', p_sql)[0].upper()+'_'+re.split(r'\s+', p_sql)[1].upper()+'_'+re.split(r'\s+', p_sql)[3].upper()
    if re.split(r'\s+', p_sql)[0].upper() in('INSERT','UPDATE','DELETE') :
       return re.split(r'\s+', p_sql)[0].upper()


def get_obj_pk_name(p_curdb,p_sql):
    cr  = p_curdb.cursor()
    if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
        return '表:{0}已存在!'.format(get_obj_name(p_sql))
    else:
        cr.execute(p_sql)

    cr.execute('''SELECT column_name
                     FROM  information_schema.columns   
                    WHERE UPPER(table_schema)=DATABASE()  
                      AND UPPER(table_name)=upper('{}')
                      AND column_key='PRI'
               '''.format(get_obj_name(p_sql)))
    rs  = cr.fetchone()
    col = rs[0]
    cr.execute('drop table {}'.format(get_obj_name(p_sql)))
    return col

def get_obj_pk_name_multi(p_curdb,p_sql,config):
    try:
        cr  = p_curdb.cursor()
        op  = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            sql='''SELECT count(0)
                             FROM  information_schema.columns   
                            WHERE UPPER(table_schema)=DATABASE()  
                              AND UPPER(table_name)=upper('{}')
                              AND column_key='PRI'
                              and column_name='id'
                 '''.format(get_obj_name(p_sql))
            cr.execute(sql)
            rs  = cr.fetchone()
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
            return rs[0]
    except Exception as e:
        print(traceback.print_exc())
        return str(e)


def f_get_table_ddl(p_curdb,tab):
    cr_source = p_curdb.cursor()
    v_sql     ="""show create table {0}""".format(tab)
    cr_source.execute(v_sql)
    rs=cr_source.fetchone()
    return rs[1]

def get_obj_privs_grammar(p_curdb,p_sql):
    try:
        op = get_obj_op(p_sql)
        cr  = p_curdb.cursor()
        if op == 'CREATE_TABLE':
            if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
                return '表:{0} 已存在!'.format(get_obj_name(p_sql))
            else:
                cr.execute(p_sql)
            cr.execute('drop table {}'.format(get_obj_name(p_sql)))
        elif op in('ALTER_TABLE_ADD','ALTER_TABLE_DROP'):
            try:
                if check_mysql_tab_exists(p_curdb,get_obj_name(p_sql))>0:
                   cr.execute(f_get_table_ddl(p_curdb,get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_'+get_obj_name(p_sql)))
                else:
                   return '表:{0}不存在!'.format(get_obj_name(p_sql))
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql),'dbops_'+get_obj_name(p_sql)))
                cr.execute('drop table {0}'.format('dbops_'+get_obj_name(p_sql)))
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                return process_result(str(e))
        return '0'
    except Exception as e:
        return process_result(str(e))

def get_obj_privs_grammar_proc(p_curdb,p_sql):
    try:
        op = get_obj_op(p_sql)
        cr  = p_curdb.cursor()
        if op  in('CREATE_PROCEDURE','CREATE_FUNCTION','CREATE_TRIGGER','CREATE_EVENT'):
            if check_mysql_proc_exists(p_curdb, get_obj_name(p_sql)) > 0:
                return '过程:{0} 已存在!'.format(get_obj_name(p_sql))
            else:
                cr.execute(p_sql)
            cr.execute('drop {0} {1}'.format(get_obj_type(p_sql),get_obj_name(p_sql)))
        # 删除前备份过程数据
        elif  op  in('DROP_PROCEDURE','DROP_FUNCTION','DROP_TRIGGER','DROP_EVENT'):
            if check_mysql_proc_exists(p_curdb, get_obj_name(p_sql)) == 0:
                return '过程:{0} 不存在!'.format(get_obj_name(p_sql))
            else:
                cr.execute(p_sql)
            cr.execute('drop {0} {1}'.format(get_obj_type(p_sql),get_obj_name(p_sql)))
        return '0'
    except Exception as e:
        return process_result(str(e))

def get_obj_privs_grammar_multi(p_curdb,p_sql,config):
    try:
        op = get_obj_op(p_sql)
        cr  = p_curdb.cursor()
        if op == 'CREATE_TABLE':
            if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
                return '表:{0}已存在!'.format(get_obj_name(p_sql))
            else:
                cr.execute(p_sql)
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
        elif op in('ALTER_TABLE_ADD','ALTER_TABLE_DROP'):
            if config.get('dbops_' + get_obj_name(p_sql)) is None:
                if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
                    cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),
                                                                                     'dbops_' + get_obj_name(p_sql)))
                else:
                    return '表:{0}不存在!'.format(get_obj_name(p_sql))

            cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
            cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
            cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
            config['dbops_' +get_obj_name(p_sql)] = 'drop table {0}'.format('dbops_' + get_obj_name(p_sql))
        return '0'
    except Exception as e:
        return str(e)

def get_tab_comment(p_curdb,p_sql):
    cr  = p_curdb.cursor()
    if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
        return '表:{0}已存在!'.format(get_obj_name(p_sql))
    else:
        cr.execute(p_sql)

    cr.execute('''SELECT CASE WHEN table_comment!='' THEN 1 ELSE 0 END 
                    FROM  information_schema.tables   
                    WHERE UPPER(table_schema)=DATABASE()  
                     AND UPPER(table_name) =upper('{}')
               '''.format(get_obj_name(p_sql)))
    rs  = cr.fetchone()
    col = rs[0]
    cr.execute('drop table {}'.format(get_obj_name(p_sql)))
    return col

def get_tab_comment_multi(p_curdb,p_sql,config):
    try:
        cr  = p_curdb.cursor()
        op  = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            cr.execute('''SELECT CASE WHEN table_comment!='' THEN 1 ELSE 0 END 
                            FROM  information_schema.tables   
                            WHERE UPPER(table_schema)=DATABASE()  
                              AND UPPER(table_name) =upper('{}')
                       '''.format(get_obj_name(p_sql)))
            rs  = cr.fetchone()
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
            return rs[0]
    except Exception as e:
        return str(e)

def get_col_comment(p_curdb,p_sql):
    try:
        cr = p_curdb.cursor()
        op = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            try:
                if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
                    return  '表:{0}已存在!'.format(get_obj_name(p_sql))
                else:
                    cr.execute(p_sql)

                cr.execute('''SELECT table_name,column_name,
                                     CASE WHEN column_comment!='' THEN 1 ELSE 0 END 
                               FROM  information_schema.columns   
                               WHERE UPPER(table_schema)=DATABASE()  
                                 AND UPPER(table_name) = upper('{}')
                              '''.format(get_obj_name(p_sql)))
                rs  = cr.fetchall()
                col = rs
                cr.execute('drop table {}'.format(get_obj_name(p_sql)))
                return col
            except Exception as e:
                cr.execute('drop table {}'.format(get_obj_name(p_sql)))
                return process_result(str(e))

        elif op == 'ALTER_TABLE_ADD':
            try:
                if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
                    cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql))
                               .replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                else:
                    return '表:{0} 不存在!'.format(get_obj_name(p_sql))
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))

            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                cr.execute('''SELECT table_name,column_name,
                                      CASE WHEN column_comment!='' THEN 1 ELSE 0 END 
                                   FROM  information_schema.columns   
                                   WHERE UPPER(table_schema)=DATABASE()  
                                     AND UPPER(table_name) = upper('{}')
                              '''.format('dbops_' + get_obj_name(p_sql)))
                rs = cr.fetchall()
                col = rs
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                return col
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                return process_result(str(e))

    except Exception as e:
        return process_result(str(e))

def get_col_comment_multi(p_curdb,p_sql,config):
    try:
        cr = p_curdb.cursor()
        op = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            try:
                cr.execute('''SELECT table_name,
                                     column_name,
                                     CASE WHEN column_comment!='' THEN 1 ELSE 0 END 
                               FROM  information_schema.columns   
                               WHERE UPPER(table_schema)=DATABASE()  
                                 AND UPPER(table_name) = upper('{}')
                              '''.format(get_obj_name(p_sql)))
                rs  = cr.fetchall()
                config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
                return rs
            except Exception as e:
                return str(e)

        elif op == 'ALTER_TABLE_ADD':
            if config.get('dbops_' + get_obj_name(p_sql)) is None:
                if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
                    cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),
                                                                                     'dbops_' + get_obj_name(p_sql)))
                else:
                    return '表:{0}不存在!'.format(get_obj_name(p_sql))

            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                cr.execute('''SELECT table_name,
                                    column_name,
                                      CASE WHEN column_comment!='' THEN 1 ELSE 0 END 
                                   FROM  information_schema.columns   
                                   WHERE UPPER(table_schema)=DATABASE()  
                                     AND UPPER(table_name) = upper('{}')
                              '''.format('dbops_' + get_obj_name(p_sql)))
                rs = cr.fetchall()
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                config['dbops_' + get_obj_name(p_sql)] = 'drop table {0}'.format('dbops_' + get_obj_name(p_sql))
                return rs
            except Exception as e:
                return process_result(str(e))

    except Exception as e:
        return process_result(str(e))


def get_col_default_value(p_curdb,p_sql):
    try:
        cr  = p_curdb.cursor()
        op  = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            try:
                if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
                    return  '表:{0}已存在!'.format(get_obj_name(p_sql))
                else:
                    cr.execute(p_sql)

                cr.execute('''SELECT table_name,column_name,
                                       CASE WHEN column_default is NULL AND is_nullable='NO' THEN 0 ELSE 1 END 
                                FROM  information_schema.columns   
                                WHERE UPPER(table_schema)=DATABASE()  
                                  AND column_key!='PRI'
                                  AND UPPER(table_name) = upper('{}')
                           '''.format(get_obj_name(p_sql)))
                rs  = cr.fetchall()
                col = rs
                cr.execute('drop table {}'.format(get_obj_name(p_sql)))
                return col
            except Exception as e:
                cr.execute('drop table {}'.format(get_obj_name(p_sql)))
                return str(e)

        elif op == 'ALTER_TABLE_ADD':
            try:
                if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
                    cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),
                                                                                     'dbops_' + get_obj_name(p_sql)))
                else:
                    return '表:{0}不存在!'.format(get_obj_name(p_sql))
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))

            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
                v_sql ='''SELECT table_name,column_name,
                                     CASE WHEN column_default is NULL AND is_nullable='NO' THEN 0 ELSE 1 END 
                                FROM  information_schema.columns   
                                WHERE UPPER(table_schema)=DATABASE()  
                                  AND column_key!='PRI'
                                  AND UPPER(table_name) = upper('{}')
                           '''.format('dbops_' + get_obj_name(p_sql))
                cr.execute(v_sql)
                rs = cr.fetchall()
                col = rs
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                return col
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                return process_result(str(e))

    except Exception as e:
        return process_result(str(e))

def get_col_default_value_multi(p_curdb,p_sql,config):
    try:
        cr  = p_curdb.cursor()
        op  = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            cr.execute('''SELECT table_name,column_name,
                                   CASE WHEN column_default is NULL AND is_nullable='NO' THEN 0 ELSE 1 END 
                            FROM  information_schema.columns   
                            WHERE UPPER(table_schema)=DATABASE()  
                              AND column_key!='PRI'
                              AND UPPER(table_name) = upper('{}')
                       '''.format(get_obj_name(p_sql)))
            rs  = cr.fetchall()
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
            return rs
        elif op == 'ALTER_TABLE_ADD':
            if config.get('dbops_' + get_obj_name(p_sql)) is None:
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql))
                           .replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))

            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
                v_sql ='''SELECT table_name,column_name,
                                     CASE WHEN column_default is NULL AND is_nullable='NO' THEN 0 ELSE 1 END 
                            FROM  information_schema.columns   
                            WHERE UPPER(table_schema)=DATABASE()  
                              AND column_key!='PRI'
                              AND UPPER(table_name) = upper('{}')
                           '''.format('dbops_' + get_obj_name(p_sql))
                cr.execute(v_sql)
                rs = cr.fetchall()
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                config['dbops_' + get_obj_name(p_sql)] = 'drop table {0}'.format('dbops_' + get_obj_name(p_sql))
                return rs
            except Exception as e:
                return process_result(str(e))

    except Exception as e:
        return process_result(str(e))

def get_time_col_default_value(p_curdb,p_sql):
    try:
        cr = p_curdb.cursor()
        op = get_obj_op(p_sql)
        sql = '''SELECT 
                        table_name,
                        column_name,
                        'CURRENT_TIMESTAMP',
                        CASE WHEN column_default='CURRENT_TIMESTAMP'  THEN  1 ELSE 0 END
                  FROM  information_schema.columns   
                  WHERE UPPER(table_schema)=DATABASE()  
                   AND data_type IN('datetime','timestamp')
                   AND column_key!='PRI'
                   AND UPPER(table_name) = upper('{0}')
                   AND column_name='create_time'
                  union all  
                  SELECT 
                        table_name,
                        column_name,
                        'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
                        CASE WHEN column_default='CURRENT_TIMESTAMP' AND extra='on update CURRENT_TIMESTAMP' THEN  1 ELSE 0 END
                  FROM  information_schema.columns   
                  WHERE UPPER(table_schema)=DATABASE()  
                   AND data_type IN('datetime','timestamp')
                   AND column_key!='PRI'
                   AND UPPER(table_name) = upper('{0}')
                   AND column_name='update_time'
               '''
        if op == 'CREATE_TABLE':
            try:
                if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
                    return  '表:{0}已存在!'.format(get_obj_name(p_sql))
                else:
                    cr.execute(p_sql)

                cr.execute(sql.format(get_obj_name(p_sql), get_obj_name(p_sql)))
                rs = cr.fetchall()
                col = rs
                cr.execute('drop table {}'.format(get_obj_name(p_sql)))
                return col
            except Exception as e:
                cr.execute('drop table {}'.format(get_obj_name(p_sql)))
                return process_result(str(e))

        elif op == 'ALTER_TABLE_ADD':
            try:
                if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
                    cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),
                                                                                     'dbops_' + get_obj_name(p_sql)))
                else:
                    return '表:{0}不存在!'.format(get_obj_name(p_sql))
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),
                                                                                 'dbops_' + get_obj_name(p_sql)))

            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
                sql = sql.format('dbops_' + get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql))
                cr.execute(sql)
                rs = cr.fetchall()
                col = rs
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                return col
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                return process_result(str(e))

    except Exception as e:
        return process_result(str(e))


def get_time_col_default_value_multi(p_curdb,p_sql,config):
    try:
        cr = p_curdb.cursor()
        op = get_obj_op(p_sql)
        sql = '''SELECT 
                      table_name,
                      column_name,
                      'CURRENT_TIMESTAMP',
                      CASE WHEN column_default='CURRENT_TIMESTAMP'  THEN  1 ELSE 0 END
                   FROM  information_schema.columns   
                   WHERE UPPER(table_schema)=DATABASE()  
                    AND data_type IN('datetime','timestamp')
                    AND column_key!='PRI'
                    AND UPPER(table_name) = upper('{0}')
                    AND column_name='create_time'
                   union all  
                   SELECT 
                         table_name,
                         column_name,
                         'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
                         CASE WHEN column_default='CURRENT_TIMESTAMP' AND extra='on update CURRENT_TIMESTAMP' THEN  1 ELSE 0 END
                   FROM  information_schema.columns   
                   WHERE UPPER(table_schema)=DATABASE()  
                     AND data_type IN('datetime','timestamp')
                     AND column_key!='PRI'
                     AND UPPER(table_name) = upper('{0}')
                     AND column_name='update_time'
              '''
        if op == 'CREATE_TABLE':
            try:
                cr.execute(sql.format(get_obj_name(p_sql), get_obj_name(p_sql)))
                rs = cr.fetchall()
                config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
                return rs
            except Exception as e:
                return process_result(str(e))

        elif op == 'ALTER_TABLE_ADD':
            if config.get('dbops_' + get_obj_name(p_sql)) is None:
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql))
                           .replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
                cr.execute('dbops_' + get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql))
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                rs = cr.fetchall()
                config['dbops_' + get_obj_name(p_sql)] = 'drop table {0}'.format('dbops_' + get_obj_name(p_sql))
                return rs
            except Exception as e:
                return process_result(str(e))

    except Exception as e:
        return process_result(str(e))

def get_tab_char_col_len(p_curdb,p_sql,rule):
    cr  = p_curdb.cursor()
    cr.execute(p_sql)
    cr.execute('''SELECT 
                    table_name,column_name,
                    CASE WHEN character_maximum_length<={0} THEN 1 ELSE 0 END AS val
                  FROM  information_schema.columns   
                  WHERE UPPER(table_schema)=DATABASE()  
                   AND data_type IN('varchar','char')
                   AND column_key!='PRI'
                   AND UPPER(table_name) = upper('{1}')
               '''.format(rule['rule_value'],get_obj_name(p_sql)))
    rs  = cr.fetchall()
    col = rs
    cr.execute('drop table {}'.format(get_obj_name(p_sql)))
    return col


def get_tab_char_col_total_len(p_curdb,p_sql,rule):
    cr  = p_curdb.cursor()
    cr.execute(p_sql)
    cr.execute('''SELECT 
                     CASE WHEN IFNULL(SUM(character_maximum_length),0)<={0} THEN 1 ELSE 0 END AS val
                  FROM  information_schema.columns   
                  WHERE UPPER(table_schema)=DATABASE()  
                   AND data_type IN('varchar','char')
                   AND column_key!='PRI'
                   AND UPPER(table_name) = upper('{1}')
               '''.format(rule['rule_value'],get_obj_name(p_sql)))
    rs  = cr.fetchone()
    col = rs[0]
    cr.execute('drop table {}'.format(get_obj_name(p_sql)))
    return col

def check_tab_rule(p_db,p_sql,p_user,n_sxh):
    obj = get_obj_name(p_sql.strip()).lower()
    ret = True
    cr  = p_db.cursor()
    sql = """select id,rule_code,rule_name,rule_value,error 
              from t_sql_audit_rule 
               where rule_type='ddl' and status='1' 
                and rule_code in('switch_tab_max_len','switch_tab_not_digit_first',
                                 'switch_tab_two_digit_end','switch_tab_disable_prefix') order by id"""
    cr.execute(sql)
    rs = cr.fetchall()
    for rule in rs:
        if rule['rule_code'] == 'switch_tab_max_len' :
            if get_obj_op(p_sql) == 'CREATE_TABLE' and  get_obj_type(p_sql.strip()) == 'TABLE':
                print('检查表名最大长度...')
                if len(obj)>int(rule['rule_value']):
                    rule['error'] = format_sql(rule['error'].format(obj,rule['rule_value']))
                    save_check_results(p_db, rule, p_user, p_sql.strip(), n_sxh)
                    ret = False

        if rule['rule_code'] == 'switch_tab_not_digit_first' and rule['rule_value'] == 'true':
            if get_obj_op(p_sql) == 'CREATE_TABLE' and  get_obj_type(p_sql.strip()) == 'TABLE':
                print('检查表名表名不能以数字开头...')
                if obj[0] in  "0123456789":
                    rule['error'] = format_sql(rule['error'].format(obj,rule['rule_value']))
                    save_check_results(p_db, rule, p_user, p_sql.strip(), n_sxh)
                    ret = False

        if rule['rule_code'] == 'switch_tab_two_digit_end' and rule['rule_value'] == 'true':
            if get_obj_op(p_sql) == 'CREATE_TABLE' and  get_obj_type(p_sql.strip()) == 'TABLE':
                print('禁止表名以连续2位及以上数字为后缀...')
                if len(re.findall(r'\d{2,9}$', obj, re.M)) > 0:
                    rule['error'] = format_sql(rule['error'].format(obj,rule['rule_value']))
                    save_check_results(p_db, rule, p_user, p_sql.strip(), n_sxh)
                    ret = False

        if rule['rule_code'] == 'switch_tab_disable_prefix' :
            if get_obj_op(p_sql) == 'CREATE_TABLE' and  get_obj_type(p_sql.strip()) == 'TABLE':
               print('检查表名称禁止前缀...')
               for t in rule['rule_value'].lower().split(','):
                   if len(re.findall(r'{0}$'.format(t), obj, re.M)) > 0 \
                           or len(re.findall(r'^{0}'.format(t), obj, re.M)) > 0 :
                       rule['error'] = format_sql(rule['error'].format(obj, t))
                       save_check_results(p_db, rule, p_user, p_sql.strip(), n_sxh)
                       ret = False

    return ret


def check_idx_name_null(p_curdb,p_sql,rule):
    cr  = p_curdb.cursor()
    sql = """SELECT count(0) FROM mysql.innodb_index_stats a 
              WHERE a.`database_name` = DATABASE()
               AND  a.table_name='{0}' AND index_name='{1}'
          """
    try:
        if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
            cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),
                                                                             'dbops_' + get_obj_name(p_sql)))
        else:
            return '表:{0}不存在!'.format(get_obj_name(p_sql))
    except Exception as e:
        cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
        cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))

    try:
        t = re.split(r'\s+', p_sql.strip())
        if len(t) == 6  and t[5].find('(')==0:
            col = p_sql.strip().split('(')[1].split(')')[0]
            cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
            sql = sql.format('dbops_' + get_obj_name(p_sql), col)
            cr.execute(sql)
            rs = cr.fetchone()
            col= rs[0]
            cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
            return col
        return 0
    except Exception as e:
        cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
        return process_result(str(e))

def check_idx_name_col(p_sql,rule):
    t = re.split(r'\s+', p_sql.strip())
    if len(t) == 6:
        if t[5].split(')')[0].split('(')[0] ==  t[5].split(')')[0].split('(')[1]:
           return rule['error'].format(get_obj_name(p_sql))

    if len(t) == 7:
        if t[5] == t[6].replace('(','').replace(')',''):
           return rule['error'].format(get_obj_name(p_sql))
    return None

def check_idx_name_rule(p_curdb,p_sql,rule):
    cr  = p_curdb.cursor()
    op  = get_obj_op(p_sql)
    obj = ''
    if op == "ALTER_TABLE_ADD":
       obj = get_obj_name(p_sql).lower()
       idx = re.split(r'\s+', p_sql.strip())[5].split('(')[0].strip()
    elif op == "CREATE_INDEX":
       obj = re.split(r'\s+', p_sql.strip())[4].split('(')[0].strip()
       idx = re.split(r'\s+', p_sql.strip())[2].split('(')[0].strip()

    sql = """select column_name 
             from information_schema.columns
              where table_schema=database() 
                and table_name='{}' and column_key!='PRI'""".format(obj)
    cr.execute(sql)
    rs = cr.fetchall()
    flag = False
    for r in rs:
        exp= 'idx_$$COL$$_n[1-9]{1,2}'.replace('$$COL$$',r[0])
        if re.search(exp, idx) is not None:
           flag = True

    if not flag:
       return rule['error'].format(obj,idx)
    else:
       return None

def check_idx_numbers(p_curdb,p_sql,rule):
    cr  = p_curdb.cursor()
    op  = get_obj_op(p_sql)
    obj = ''
    if  op == "ALTER_TABLE_ADD":
        obj = get_obj_name(p_sql).lower()
    elif op == "CREATE_INDEX":
        obj = re.split(r'\s+', p_sql.strip())[4].split('(')[0].strip()

    try:
        if check_mysql_tab_exists(p_curdb, obj) > 0:
            cr.execute(f_get_table_ddl(p_curdb, obj).replace(obj,'dbops_' +obj))
        else:
            return '表:{0}不存在!'.format(obj)
    except Exception as e:
        cr.execute('drop table {0}'.format('dbops_' + obj))
        cr.execute(f_get_table_ddl(p_curdb, obj).replace(obj,'dbops_' + obj))

    try:
        cr.execute(p_sql.strip().replace(obj,'dbops_' +obj))

        sql = """SELECT COUNT(DISTINCT index_name) 
                 FROM mysql.innodb_index_stats a 
                  WHERE a.database_name = DATABASE()
                    AND a.table_name='{0}' AND index_name!='PRIMARY'
              """.format('dbops_' + obj)
        cr.execute(sql)
        rs = cr.fetchone()
        cr.execute('drop table {0}'.format('dbops_' + obj))
        print('check_idx_numbers=',rs[0])
        if rs[0] > int(rule['rule_value']):
           return rule['error'].format(obj)
        return  None
    except:
        cr.execute('drop table {0}'.format('dbops_' + obj))
        return process_result(str(e))

def check_idx_col_numbers(p_curdb,p_sql,rule):
    cr  = p_curdb.cursor()
    op  = get_obj_op(p_sql)
    obj = ''
    if  op == "ALTER_TABLE_ADD":
        obj = get_obj_name(p_sql).lower()
        idx = re.split(r'\s+', p_sql.strip())[5].split('(')[0].strip()
    elif op == "CREATE_INDEX":
        obj = re.split(r'\s+', p_sql.strip())[4].split('(')[0].strip()
        idx = re.split(r'\s+', p_sql.strip())[2].split('(')[0].strip()

    try:
        if check_mysql_tab_exists(p_curdb, obj) > 0:
            cr.execute(f_get_table_ddl(p_curdb, obj).replace(obj, 'dbops_' + obj))
        else:
            return '表:{0}不存在!'.format(obj)
    except Exception as e:
        cr.execute('drop table {0}'.format('dbops_' + obj))
        cr.execute(f_get_table_ddl(p_curdb, obj).replace(obj, 'dbops_' + obj))

    try:
        cr.execute(p_sql.strip().replace(obj, 'dbops_' + obj))
        sql = """SELECT n_fields FROM information_schema.INNODB_SYS_INDEXES WHERE `name`='{0}'""".format(idx)
        cr.execute(sql)
        rs = cr.fetchone()
        cr.execute('drop table {0}'.format('dbops_' + obj))
        if rs[0] > int(rule['rule_value']):
           return rule['error'].format(obj,idx)
        return  None
    except:
        cr.execute('drop table {0}'.format('dbops_' + obj))
        return process_result(str(e))


def check_idx_rule(p_db,p_curdb,p_sql,p_user,n_sxh):
    obj = get_obj_name(p_sql.strip()).lower()
    ret = True
    cr = p_db.cursor()
    sql = """select id,rule_code,rule_name,rule_value,error 
                from t_sql_audit_rule 
                 where rule_type='ddl' and status='1' 
                  and rule_code in('switch_idx_name_null','switch_idx_name_rule',
                                   'switch_idx_numbers','switch_idx_col_numbers',
                                   'switch_idx_name_col') order by id"""
    cr.execute(sql)
    rs = cr.fetchall()
    for rule in rs:
        if rule['rule_code'] == 'switch_idx_name_null' and rule['rule_value'] == 'false':
            if get_obj_op(p_sql) == 'ALTER_TABLE_ADD' and get_obj_type(p_sql.strip()) == 'TABLE'\
                  and p_sql.strip().upper().count('INDEX')  \
                    and p_sql.strip().upper().find("INDEX")>p_sql.strip().upper().find("ADD") :
                print('检查允许索引名为空...')
                v = check_idx_name_null(p_curdb,p_sql,rule)
                try:
                    if int(v) > 0 :
                       rule['error'] = format_sql(rule['error'].format(obj))
                       save_check_results(p_db, rule, p_user, p_sql.strip(), n_sxh)
                       ret = False
                except:
                    rule['error'] = format_sql(v)
                    save_check_results(p_db, rule, p_user, p_sql.strip(), n_sxh)
                    ret = False

        if rule['rule_code'] == 'switch_idx_name_rule' and rule['rule_value'] == 'true':
            if (get_obj_op(p_sql) == 'ALTER_TABLE_ADD' and get_obj_type(p_sql.strip()) == 'TABLE' \
                  and p_sql.strip().upper().count('INDEX') \
                    and p_sql.strip().upper().find("INDEX") > p_sql.strip().upper().find("ADD")) \
                      or (get_obj_op(p_sql) == 'CREATE_INDEX' and get_obj_type(p_sql.strip()) == 'INDEX'):
                print('检查索引名规则...')
                v = check_idx_name_rule(p_curdb,p_sql.strip(),rule)
                if v is not None:
                    rule['error'] = format_sql(v)
                    save_check_results(p_db, rule, p_user, p_sql.strip(), n_sxh)
                    ret = False

        if rule['rule_code'] == 'switch_idx_numbers' :
            if (get_obj_op(p_sql) == 'ALTER_TABLE_ADD' and get_obj_type(p_sql.strip()) == 'TABLE' \
                  and p_sql.strip().upper().count('INDEX') \
                    and p_sql.strip().upper().find("INDEX") > p_sql.strip().upper().find("ADD")) \
                      or (get_obj_op(p_sql) == 'CREATE_INDEX' and get_obj_type(p_sql.strip()) == 'INDEX'):
                print('检查单表索引数上限...')
                v = check_idx_numbers(p_curdb,p_sql.strip(),rule)
                if v is not None:
                    rule['error'] = format_sql(v)
                    save_check_results(p_db, rule, p_user, p_sql.strip(), n_sxh)
                    ret = False

        if rule['rule_code'] == 'switch_idx_col_numbers':
            if (get_obj_op(p_sql) == 'ALTER_TABLE_ADD' and get_obj_type(p_sql.strip()) == 'TABLE' \
                  and p_sql.strip().upper().count('INDEX') \
                    and p_sql.strip().upper().find("INDEX") > p_sql.strip().upper().find("ADD")) \
                      or (get_obj_op(p_sql) == 'CREATE_INDEX' and get_obj_type(p_sql.strip()) == 'INDEX'):
                print('检查单个索引字段上限...')
                v = check_idx_col_numbers(p_curdb,p_sql.strip(),rule)
                if v is not None:
                    rule['error'] = format_sql(v)
                    save_check_results(p_db, rule, p_user, p_sql.strip(), n_sxh)
                    ret = False


        if rule['rule_code'] == 'switch_idx_name_col' and rule['rule_value'] == 'false':
            if get_obj_op(p_sql) == 'ALTER_TABLE_ADD' and get_obj_type(p_sql.strip()) == 'TABLE' \
                  and p_sql.strip().upper().count('INDEX') \
                    and p_sql.strip().upper().find("INDEX") > p_sql.strip().upper().find("ADD"):
                print('检查索引名与列名是否相同...')
                v = check_idx_name_col(p_sql,rule)
                if v is not None:
                    rule['error'] = format_sql(v)
                    save_check_results(p_db, rule, p_user, p_sql.strip(), n_sxh)
                    ret = False

    return ret


def get_tab_char_col_len_multi(p_curdb,p_sql,rule,config):
    try:
        cr  = p_curdb.cursor()
        op = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            cr.execute('''SELECT 
                            table_name,column_name,
                            CASE WHEN character_maximum_length<={0} THEN 1 ELSE 0 END AS val
                          FROM  information_schema.columns   
                          WHERE UPPER(table_schema)=DATABASE()  
                           AND data_type IN('varchar','char')
                           AND column_key!='PRI'
                           AND UPPER(table_name) = upper('{1}')
                       '''.format(rule['rule_value'],get_obj_name(p_sql)))
            rs  = cr.fetchall()
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
            return rs
        elif op == 'ALTER_TABLE_ADD':
            if config.get('dbops_' + get_obj_name(p_sql)) is None:
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).
                           replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
            try:
                cr.execute('''SELECT 
                                  table_name,column_name,
                                  CASE WHEN character_maximum_length<={0} THEN 1 ELSE 0 END AS val
                              FROM  information_schema.columns   
                              WHERE UPPER(table_schema)=DATABASE()  
                               AND data_type IN('varchar','char')
                               AND column_key!='PRI'
                               AND UPPER(table_name) = upper('{1}')
                           '''.format(rule['rule_value'], 'dbops_' + get_obj_name(p_sql)))
                rs = cr.fetchall()
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                config['dbops_' + get_obj_name(p_sql)] = 'drop table {0}'.format('dbops_' + get_obj_name(p_sql))
                return rs
            except Exception as e:
                return process_result(str(e))
    except Exception as e:
        return process_result(str(e))

def get_tab_has_fields(p_curdb,p_sql,rule):
    try:
        cr  = p_curdb.cursor()
        sql = '''SELECT table_name,'create_time' AS column_name 
                     FROM  information_schema.tables a  
                    WHERE a.table_schema=DATABASE()  
                      AND a.table_name= LOWER('{0}')
                      AND NOT EXISTS(SELECT 1 FROM information_schema.columns b
                                     WHERE a.table_schema=b.table_schema
                                       AND b.table_schema=DATABASE()
                                       AND a.table_name=b.table_name
                                       AND b.column_name='create_time')
                    UNION ALL
                    SELECT table_name,'update_time' AS column_name 
                     FROM  information_schema.tables a  
                    WHERE a.table_schema=DATABASE()  
                      AND a.table_name = LOWER('{1}')
                      AND NOT EXISTS(SELECT 1 FROM information_schema.columns b
                                     WHERE a.table_schema=b.table_schema
                                       AND b.table_schema=DATABASE()
                                       AND a.table_name=b.table_name
                                       AND b.column_name='update_time')
               '''
        op  = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            try:
                if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
                    return  '表:{0}已存在!'.format(get_obj_name(p_sql))
                else:
                    cr.execute(p_sql)

                cr.execute(sql.format(get_obj_name(p_sql),get_obj_name(p_sql)))
                rs = cr.fetchall()
                col = rs
                cr.execute('drop table {}'.format(get_obj_name(p_sql)))
                return col
            except Exception as e:
                cr.execute('drop table {}'.format(get_obj_name(p_sql)))
                return process_result(str(e))

        elif op == 'ALTER_TABLE_ADD':
            try:
                if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
                    cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),
                                                                                     'dbops_' + get_obj_name(p_sql)))
                else:
                    return '表:{0}不存在!'.format(get_obj_name(p_sql))
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),
                                                                                 'dbops_' + get_obj_name(p_sql)))

            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
                v_sql = sql.format('dbops_' + get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql))
                cr.execute(v_sql)
                rs = cr.fetchall()
                col = rs
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                return col
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                return process_result(str(e))

    except Exception as e:
        return process_result(str(e))


def get_tab_rows(p_curdb,p_sql):
    op  = get_obj_op(p_sql)
    cr  = p_curdb.cursor()
    if op in ('CREATE_TABLE', 'ALTER_TABLE_ADD', 'ALTER_TABLE_DROP'):
        sql = "select count(0) from {0}".format(get_obj_name(p_sql))
        cr.execute(sql)
        rs=cr.fetchone()
        return rs[0]
    return 0


def get_tab_has_fields_multi(p_curdb,p_sql,config):
    try:
        cr = p_curdb.cursor()
        op = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            cr.execute('''SELECT table_name,'create_time' AS column_name 
                             FROM  information_schema.tables a  
                            WHERE a.table_schema=DATABASE()  
                              AND a.table_name= LOWER('{0}')
                              AND NOT EXISTS(SELECT 1 FROM information_schema.columns b
                                             WHERE a.table_schema=b.table_schema
                                               AND b.table_schema=DATABASE()
                                               AND a.table_name=b.table_name
                                               AND b.column_name='create_time')
                            UNION ALL
                            SELECT table_name,'update_time' AS column_name 
                             FROM  information_schema.tables a  
                            WHERE a.table_schema=DATABASE()  
                              AND a.table_name = LOWER('{1}')
                              AND NOT EXISTS(SELECT 1 FROM information_schema.columns b
                                             WHERE a.table_schema=b.table_schema
                                               AND b.table_schema=DATABASE()
                                               AND a.table_name=b.table_name
                                               AND b.column_name='update_time')
                       '''.format(get_obj_name(p_sql),get_obj_name(p_sql)))
            rs  = cr.fetchall()
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
            return rs

        elif op in('ALTER_TABLE_ADD','ALTER_TABLE_DROP'):
            if config.get('dbops_' + get_obj_name(p_sql)) is None:
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql))
                           .replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))

            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
                cr.execute('''SELECT table_name,'create_time' AS column_name 
                                 FROM  information_schema.tables a  
                                WHERE a.table_schema=DATABASE()  
                                  AND a.table_name= LOWER('{0}')
                                  AND NOT EXISTS(SELECT 1 FROM information_schema.columns b
                                                 WHERE a.table_schema=b.table_schema
                                                   AND b.table_schema=DATABASE()
                                                   AND a.table_name=b.table_name
                                                   AND b.column_name='create_time')
                                UNION ALL
                                SELECT table_name,'update_time' AS column_name 
                                 FROM  information_schema.tables a  
                                WHERE a.table_schema=DATABASE()  
                                  AND a.table_name = LOWER('{1}')
                                  AND NOT EXISTS(SELECT 1 FROM information_schema.columns b
                                                 WHERE a.table_schema=b.table_schema
                                                   AND b.table_schema=DATABASE()
                                                   AND a.table_name=b.table_name
                                                   AND b.column_name='update_time')
                           '''.format('dbops_' + get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                rs = cr.fetchall()
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql))
                          .replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                config['dbops_' + get_obj_name(p_sql)] = 'drop table {0}'.format('dbops_' + get_obj_name(p_sql))
                return rs
            except Exception as e:
                return process_result(str(e))
    except Exception as e:
        return process_result(str(e))


def get_tab_tcol_datetime(p_curdb,p_sql,rule):
    try:
        cr  = p_curdb.cursor()
        sql = '''SELECT table_name,
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
                                       AND b.data_type!='datetime') 
               '''
        op  = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            try:
                if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
                    return  '表:{0}已存在!'.format(get_obj_name(p_sql))
                else:
                    cr.execute(p_sql)

                cr.execute(sql.format(get_obj_name(p_sql),get_obj_name(p_sql)))
                rs = cr.fetchall()
                col = rs
                cr.execute('drop table {}'.format(get_obj_name(p_sql)))
                return col
            except Exception as e:
                cr.execute('drop table {}'.format(get_obj_name(p_sql)))
                return process_result(str(e))

        elif op == 'ALTER_TABLE_ADD':
            try:
                if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
                    cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql))
                               .replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                else:
                    return '表:{0}不存在!'.format(get_obj_name(p_sql))
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),
                                                                                 'dbops_' + get_obj_name(p_sql)))

            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
                cr.execute(sql.format('dbops_' + get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                rs = cr.fetchall()
                col = rs
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                return col
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                return process_result(str(e))

    except Exception as e:
        return process_result(str(e))


def get_tab_tcol_datetime_multi(p_curdb,p_sql,config):
    try:
        cr  = p_curdb.cursor()
        op = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            cr.execute('''SELECT   table_name,
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
                                               AND b.data_type!='datetime') 
                       '''.format(get_obj_name(p_sql),get_obj_name(p_sql)))
            rs  = cr.fetchall()
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
            return rs

        elif op == 'ALTER_TABLE_ADD':
            if config.get('dbops_' + get_obj_name(p_sql)) is None:
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql))
                           .replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))

            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
                cr.execute('''SELECT table_name,
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
                                                  AND b.data_type!='datetime') 
                          '''.format('dbops_' + get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                rs = cr.fetchall()
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),
                                                                                 'dbops_' + get_obj_name(p_sql)))
                config['dbops_' + get_obj_name(p_sql)] = 'drop table {0}'.format('dbops_' + get_obj_name(p_sql))
                return rs
            except Exception as e:
                return process_result(str(e))
    except Exception as e:
        return process_result(str(e))

def get_col_not_null(p_curdb,p_sql):
    try:
        cr  = p_curdb.cursor()
        op = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
                return '表:{0}已存在!'.format(get_obj_name(p_sql))
            else:
                cr.execute(p_sql)

            cr.execute('''SELECT table_name,column_name,
                               CASE WHEN is_nullable='YES' THEN 0 ELSE 1 END 
                            FROM  information_schema.columns   
                            WHERE UPPER(table_schema)=DATABASE()  
                              AND UPPER(table_name) = upper('{}')
                       '''.format(get_obj_name(p_sql)))
            rs  = cr.fetchall()
            col = rs
            cr.execute('drop table {}'.format(get_obj_name(p_sql)))
            return col
        elif op == 'ALTER_TABLE_ADD':
            try:
                if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
                    cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),
                                                                                     'dbops_' + get_obj_name(p_sql)))
                else:
                    return '表:{0}不存在!'.format(get_obj_name(p_sql))
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),
                                                                                 'dbops_' + get_obj_name(p_sql)))

            try:
                cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
                cr.execute('''SELECT table_name,column_name,
                               CASE WHEN is_nullable='YES' THEN 0 ELSE 1 END 
                              FROM  information_schema.columns   
                               WHERE UPPER(table_schema)=DATABASE()  
                                 AND UPPER(table_name) = upper('{}')
                                          '''.format('dbops_' + get_obj_name(p_sql)))
                rs = cr.fetchall()
                col = rs
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                return process_result(str(e))
            return col
    except Exception as e:
        return process_result(str(e))

def get_col_not_null_multi(p_curdb,p_sql,config):
    try:
        cr  = p_curdb.cursor()
        op = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            cr.execute('''SELECT table_name,column_name,
                               CASE WHEN is_nullable='YES' THEN 0 ELSE 1 END 
                            FROM  information_schema.columns   
                              WHERE UPPER(table_schema)=DATABASE()  
                                AND UPPER(table_name) = upper('{}')
                       '''.format(get_obj_name(p_sql)))
            rs  = cr.fetchall()
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
            return rs
        elif op in('ALTER_TABLE_ADD'):
            if config.get('dbops_' + get_obj_name(p_sql)) is None:
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql))
                           .replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))

            try:
                p_tmp = p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql))
                print(p_tmp)
                cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
                cr.execute('''SELECT table_name,column_name,
                               CASE WHEN is_nullable='YES' THEN 0 ELSE 1 END 
                              FROM  information_schema.columns   
                               WHERE UPPER(table_schema)=DATABASE()  
                                 AND UPPER(table_name) = upper('{}')
                                          '''.format('dbops_' + get_obj_name(p_sql)))
                rs = cr.fetchall()
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
                config['dbops_' + get_obj_name(p_sql)] = 'drop table {0}'.format('dbops_' + get_obj_name(p_sql))
                return rs
            except Exception as e:
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                return process_result(str(e))
    except Exception as e:
        return process_result(str(e))

def get_obj_pk_exists_auto_incr(p_curdb,p_sql):
    cr  = p_curdb.cursor()
    if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
        return '表:{0}已存在!'.format(get_obj_name(p_sql))
    else:
        cr.execute(p_sql)

    cr.execute('''SELECT count(0)
                     FROM  information_schema.columns   
                    WHERE UPPER(table_schema)=DATABASE()  
                      AND UPPER(table_name)='{}'
                      AND column_key='PRI'
                      AND extra='auto_increment'
               '''.format(get_obj_name(p_sql)))
    rs  = cr.fetchone()
    col = rs[0]
    cr.execute('drop table {}'.format(get_obj_name(p_sql)))
    return rs[0]

def get_obj_pk_exists_auto_incr_multi(p_curdb,p_sql,config):
    try:
        cr  = p_curdb.cursor()
        op  = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            cr.execute('''SELECT count(0)
                             FROM  information_schema.columns   
                            WHERE UPPER(table_schema)=DATABASE()  
                              AND UPPER(table_name)='{}'
                              AND column_key='PRI'
                              AND extra='auto_increment'
                       '''.format(get_obj_name(p_sql)))
            rs  = cr.fetchone()
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
            return rs[0]
    except Exception as e:
        print(traceback.print_exc())
        return str(e)

def get_obj_pk_type_not_int_bigint(p_curdb,p_sql):
    val = 0
    cr  = p_curdb.cursor()
    if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
        return '表:{0}已存在!'.format(get_obj_name(p_sql))
    else:
        cr.execute(p_sql)

    cr.execute('''SELECT data_type
                     FROM  information_schema.columns   
                    WHERE UPPER(table_schema)=DATABASE()  
                      AND UPPER(table_name)='{}'
                      AND column_key='PRI'
               '''.format(get_obj_name(p_sql)))
    rs  = cr.fetchall()
    for i in rs:
        if i[0] not in('int','bigint'):
           val=1
           break
    cr.execute('drop table {}'.format(get_obj_name(p_sql)))
    return val

def get_obj_pk_type_not_int_bigint_multi(p_curdb,p_sql,config):
    try:
        val = 0
        cr  = p_curdb.cursor()
        op  = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            cr.execute('''SELECT data_type
                             FROM  information_schema.columns   
                            WHERE UPPER(table_schema)=DATABASE()  
                              AND UPPER(table_name)='{}'
                              AND column_key='PRI'
                       '''.format(get_obj_name(p_sql)))
            rs  = cr.fetchall()
            for i in rs:
                if i[0] not in('int','bigint'):
                   val=1
                   break
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
            return val
    except Exception as e:
        print(traceback.print_exc())
        return str(e)

def get_obj_exists_auto_incr_not_1(p_curdb,p_sql):
    cr  = p_curdb.cursor()
    if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) > 0:
        return '表:{0}已存在!'.format(get_obj_name(p_sql))
    else:
        cr.execute(p_sql)

    cr.execute('''SELECT  AUTO_INCREMENT
                     FROM  information_schema.tables   
                    WHERE UPPER(table_schema)=upper(DATABASE())
                      AND UPPER(table_name)=upper('{}')
               '''.format(get_obj_name(p_sql)))
    rs  = cr.fetchone()
    col = rs[0]
    cr.execute('drop table {}'.format(get_obj_name(p_sql)))
    return rs[0]

def get_obj_exists_auto_incr_not_1_multi(p_curdb,p_sql,config):
    try:
        cr  = p_curdb.cursor()
        op  = get_obj_op(p_sql)
        if op == 'CREATE_TABLE':
            cr.execute('''SELECT  count(0)
                             FROM  information_schema.tables   
                            WHERE UPPER(table_schema)=upper(DATABASE())
                              AND UPPER(table_name)=upper('{}')
                              and AUTO_INCREMENT=1
                       '''.format(get_obj_name(p_sql)))
            rs  = cr.fetchone()
            config[get_obj_name(p_sql)] = 'drop table {}'.format(get_obj_name(p_sql))
            return rs[0]
    except Exception as e:
        print(traceback.print_exc())
        return str(e)

def process_single_ddl(p_dbid,p_cdb,p_sql,p_user):
    n_sxh  = 1
    result = True
    ds_cur = get_ds_by_dsid_by_cdb(p_dbid, p_cdb)
    db_cur = get_connection_ds(ds_cur)
    db_ops = get_connection_dict()
    cr_ops = db_ops.cursor()
    ops_sql = """select id,rule_code,rule_name,rule_value,error 
                    from t_sql_audit_rule
                     where rule_type='ddl' and status='1' and id not in (27,28,29,30) order by id"""
    cr_ops.execute(ops_sql)
    rs_ops = cr_ops.fetchall()

    print('输出检测项...')
    print('-'.ljust(150, '-'))
    for r in rs_ops:
        print(r)

    #清空检查表
    del_check_results(db_ops, p_user)

    #检查语句
    for rule in rs_ops:

        rule['error'] = format_sql(rule['error'])

        if rule['rule_code'] == 'switch_check_ddl' and rule['rule_value'] == 'true':
            if get_obj_op(p_sql) in('CREATE_TABLE','ALTER_TABLE_ADD','ALTER_TABLE_DROP'):
                print('检测DDL语法及权限...')
                v = get_obj_privs_grammar(db_cur, p_sql.strip())
                if v != '0':
                    if v.count('存在') >0 :
                        rule['error'] = format_sql(format_exception(v))
                        save_check_results(db_ops, rule, p_user, p_sql.strip(),n_sxh)
                        result = False
                        break
                    else:
                        rule['error'] = format_sql(format_exception(v))
                        save_check_results(db_ops, rule, p_user, p_sql.strip(),n_sxh)
                        result = False

        if rule['rule_code'] == 'switch_tab_not_exists_pk' and rule['rule_value'] == 'true':
            if get_obj_op(p_sql) == 'CREATE_TABLE':
                print('检查表必须为主键...')
                if get_obj_type(p_sql.strip()) == 'TABLE' and not (
                        p_sql.upper().count('PRIMARY') > 0 and p_sql.upper().count('KEY') > 0):
                    rule['error'] = rule['error'].format(get_obj_name(p_sql.strip()))
                    save_check_results(db_ops, rule, p_user, p_sql.strip(),n_sxh)
                    result = False

        if rule['rule_code'] == 'switch_tab_pk_id' and rule['rule_value'] == 'true':
            if get_obj_op(p_sql) == 'CREATE_TABLE':
                print('强制主键名为ID...')
                if get_obj_type(p_sql) == 'TABLE' and (p_sql.upper().count('PRIMARY') > 0 \
                        and p_sql.upper().count('KEY') > 0) and get_obj_pk_name(db_cur,p_sql) != 'id':
                    rule['error'] = rule['error'].format(get_obj_name(p_sql.strip()))
                    save_check_results(db_ops, rule, p_user, p_sql,n_sxh)
                    result = False

        if rule['rule_code'] == 'switch_tab_pk_auto_incr' and rule['rule_value'] == 'true':
            if get_obj_op(p_sql) == 'CREATE_TABLE':
                print('强制主键为自增列...')
                if get_obj_type(p_sql) == 'TABLE' and (p_sql.upper().count('PRIMARY') > 0 \
                            and p_sql.upper().count('KEY') > 0) and get_obj_pk_exists_auto_incr(db_cur, p_sql) == 0:
                    rule['error'] = rule['error'].format(get_obj_name(p_sql.strip()))
                    save_check_results(db_ops, rule, p_user, p_sql,n_sxh)
                    result = False

        if rule['rule_code'] == 'switch_tab_pk_autoincrement_1' and rule['rule_value'] == 'true':
            if get_obj_op(p_sql) == 'CREATE_TABLE':
                print('强制自增列初始值为1...')
                if get_obj_type(p_sql) == 'TABLE' \
                        and (p_sql.upper().count('PRIMARY') > 0  and p_sql.upper().count('KEY') > 0) \
                           and get_obj_exists_auto_incr_not_1(db_cur, p_sql) != 1:
                    rule['error'] = rule['error'].format(get_obj_name(p_sql.strip()))
                    save_check_results(db_ops, rule, p_user, p_sql,n_sxh)
                    result = False

        if rule['rule_code'] == 'switch_pk_not_int_bigint' and rule['rule_value'] == 'false':
            if get_obj_op(p_sql) == 'CREATE_TABLE':
                print('不允许主键类型非int/bigint...')
                if get_obj_type(p_sql) == 'TABLE' and (p_sql.upper().count('PRIMARY') > 0 \
                        and p_sql.upper().count('KEY') > 0) and get_obj_pk_type_not_int_bigint(db_cur, p_sql) > 0:
                    rule['error'] = rule['error'].format(get_obj_name(p_sql.strip()))
                    save_check_results(db_ops, rule, p_user, p_sql,n_sxh)
                    result = False

        if rule['rule_code'] == 'switch_tab_comment' and rule['rule_value'] == 'true':
            if get_obj_op(p_sql) == 'CREATE_TABLE':
                print('检查表注释...')
                if get_obj_type(p_sql) == 'TABLE' and get_tab_comment(db_cur, p_sql) == 0:
                    rule['error'] = rule['error'].format(get_obj_name(p_sql.strip()))
                    save_check_results(db_ops, rule, p_user, p_sql,n_sxh)
                    result = False

        if rule['rule_code'] == 'switch_col_comment' and rule['rule_value'] == 'true' and get_obj_type(
                p_sql) == 'TABLE':
            if get_obj_op(p_sql) in ('CREATE_TABLE', 'ALTER_TABLE_ADD'):
                print('检查列注释...')
                v = get_col_comment(db_cur, p_sql)
                e = rule['error']
                try:
                    for i in v:
                        if i[2] == 0:
                            result = False
                            rule['error'] = e.format(i[0].replace('dbops_' + get_obj_name(p_sql), get_obj_name(p_sql)),
                                                     i[1])
                            save_check_results(db_ops, rule, p_user, p_sql,n_sxh)
                except IndexError as e:
                    result = False
                    rule['error'] = v
                    save_check_results(db_ops, rule, p_user, p_sql.strip(),n_sxh)
                except:
                    result = False
                    rule['error'] = v
                    save_check_results(db_ops, rule, p_user, p_sql.strip(),n_sxh)

        if rule['rule_code'] == 'switch_col_not_null' and rule['rule_value'] == 'true' and get_obj_type(
                p_sql) == 'TABLE':
            if get_obj_op(p_sql) in ('CREATE_TABLE', 'ALTER_TABLE_ADD'):
                print('检查列是否为空...')
                v = get_col_not_null(db_cur, p_sql)
                e = rule['error']
                try:
                    for i in v:
                        if i[2] == 0:
                            result = False
                            rule['error'] = e.format(i[0].replace('dbops_' + get_obj_name(p_sql), get_obj_name(p_sql)),
                                                     i[1])
                            save_check_results(db_ops, rule, p_user, p_sql,n_sxh)
                except IndexError as e:
                    result = False
                    rule['error'] = v
                    save_check_results(db_ops, rule, p_user, p_sql.strip(),n_sxh)
                except:
                    result = False
                    rule['error'] = v
                    save_check_results(db_ops, rule, p_user, p_sql.strip(),n_sxh)

        if rule['rule_code'] == 'switch_col_default_value' and rule['rule_value'] == 'true' and get_obj_type(
                p_sql) == 'TABLE':
            if get_obj_op(p_sql) in ('CREATE_TABLE', 'ALTER_TABLE_ADD'):
                print('检查列默认值...')
                v = get_col_default_value(db_cur, p_sql)
                e = rule['error']
                try:
                    if v is not None:
                        for i in v:
                            if i[2] == 0:
                                result = False
                                rule['error'] = e.format(i[0].
                                                  replace('dbops_' + get_obj_name(p_sql), get_obj_name(p_sql)),i[1])
                                save_check_results(db_ops, rule, p_user, p_sql,n_sxh)
                except IndexError as e:
                    result = False
                    rule['error'] = v
                    save_check_results(db_ops, rule, p_user, p_sql.strip(),n_sxh)
                except:
                    result = False
                    rule['error'] = v
                    save_check_results(db_ops, rule, p_user, p_sql.strip(),n_sxh)


        if rule['rule_code'] == 'switch_time_col_default_value' and rule['rule_value'] == 'true' and get_obj_type(
                p_sql) == 'TABLE':
            if get_obj_op(p_sql) in ('CREATE_TABLE'):
                print('检查时间字段默认值...')
                v = get_time_col_default_value(db_cur, p_sql)
                e = rule['error']
                try:
                    for i in v:
                        if i[3] == 0:
                            result = False
                            rule['error'] = e.format(i[0], i[1], i[2])
                            save_check_results(db_ops, rule, p_user, p_sql,n_sxh)
                except IndexError as e:
                    result = False
                    rule['error'] = v
                    save_check_results(db_ops, rule, p_user, p_sql.strip(),n_sxh)
                except:
                    result = False
                    rule['error'] = v
                    save_check_results(db_ops, rule, p_user, p_sql.strip(),n_sxh)

        if rule['rule_code'] == 'switch_char_max_len' and get_obj_type(p_sql) == 'TABLE':
            if get_obj_op(p_sql) == 'CREATE_TABLE':
                print('字符字段最大长度...')
                v = get_tab_char_col_len(db_cur, p_sql, rule)
                e = rule['error']
                for i in v:
                    if i[2] == 0:
                        result = False
                        rule['error'] = e.format(i[0], i[1], rule['rule_value'])
                        save_check_results(db_ops, rule, p_user, p_sql,n_sxh)

        if rule['rule_code'] == 'switch_tab_has_time_fields' and get_obj_type(p_sql) == 'TABLE':
            if get_obj_op(p_sql) in('CREATE_TABLE','ALTER_TABLE_ADD','ALTER_TABLE_DROP'):
                print('表必须拥有字段...')
                v = get_tab_has_fields(db_cur, p_sql, rule)
                e = rule['error']
                try:
                    for i in v:
                        result = False
                        rule['error'] = e.format(i[0], i[1])
                        save_check_results(db_ops, rule, p_user, p_sql,n_sxh)
                except IndexError as e:
                    result = False
                    rule['error'] = v
                    save_check_results(db_ops, rule, p_user, p_sql.strip(),n_sxh)
                except:
                    result = False
                    rule['error'] = v
                    save_check_results(db_ops, rule, p_user, p_sql.strip(),n_sxh)

        if rule['rule_code'] == 'switch_tab_tcol_datetime' \
                and rule['rule_value'] == 'true' and get_obj_type(p_sql) == 'TABLE':
            if get_obj_op(p_sql) == 'CREATE_TABLE':
                print('时间字段类型为datetime...')
                v = get_tab_tcol_datetime(db_cur, p_sql, rule)
                e = rule['error']
                try:
                    for i in v:
                        result = False
                        rule['error'] = e.format(i[0], i[1])
                        save_check_results(db_ops, rule, p_user, p_sql,n_sxh)
                except IndexError as e:
                    result = False
                    rule['error'] = v
                    save_check_results(db_ops, rule, p_user, p_sql.strip(),n_sxh)
                except:
                    result = False
                    rule['error'] = v
                    save_check_results(db_ops, rule, p_user, p_sql.strip(),n_sxh)

        if rule['rule_code'] == 'switch_tab_char_total_len' and get_obj_type(p_sql.strip()) == 'TABLE':
            if get_obj_op(p_sql.strip()) == 'CREATE_TABLE':
                print('字符列总长度...')
                v = get_tab_char_col_total_len(db_cur, p_sql, rule)
                if v == 0:
                    result = False
                    rule['error'] = rule['error'].format(get_obj_name(p_sql.strip()), rule['rule_value'])
                    save_check_results(db_ops, rule, p_user, p_sql,n_sxh)

        if rule['rule_code'] == 'switch_tab_ddl_max_rows' and get_obj_type(p_sql) == 'TABLE':
            if get_obj_op(p_sql) in ('TRUNCATE_TABLE','ALTER_TABLE_ADD', 'ALTER_TABLE_DROP'):
                print('DDL最大影响行数...')
                r = get_tab_rows(db_cur, p_sql)
                if r > int(rule['rule_value']):
                    result = False
                    rule['error'] = rule['error'].format(get_obj_name(p_sql.strip()),rule['rule_value'])
                    save_check_results(db_ops, rule, p_user, p_sql, n_sxh)


        if rule['rule_code'] == 'switch_disable_trigger' and rule['rule_value'] == 'true':
            if get_obj_type(p_sql) == 'TRIGGER':
               pass

        if rule['rule_code'] == 'switch_disable_func' and rule['rule_value'] == 'true':
            if get_obj_type(p_sql) == 'FUNCTION':
               pass

        if rule['rule_code'] == 'switch_disable_proc' and rule['rule_value'] == 'true':
             if get_obj_type(p_sql) == 'PROCEDURE':
                pass

        if rule['rule_code'] == 'switch_disable_event' and rule['rule_value'] == 'true':
             if get_obj_type(p_sql) == 'EVENT':
                pass


        if rule['rule_code'] == 'switch_tab_name_check' \
                and get_obj_type(p_sql.strip()) == 'TABLE'  and rule['rule_value'] == 'true' :
            if get_obj_op(p_sql) == 'CREATE_TABLE':
                print('表名规范检查...')
                if not check_tab_rule(db_ops, p_sql.strip(),p_user,n_sxh):
                   result = False

        if rule['rule_code'] == 'switch_idx_name_check' \
                and get_obj_type(p_sql.strip()) in('TABLE','INDEX') and rule['rule_value'] == 'true':
            print('switch_idx_name_check=',get_obj_op(p_sql))
            if get_obj_op(p_sql) in('CREATE_INDEX','ALTER_TABLE_ADD'):
                print('索引规范检查...')
                if  not check_idx_rule(db_ops,db_cur, p_sql.strip(), p_user, n_sxh):
                    result = False

    if result:
        rule['id'] = '0'
        rule['error'] = '检测通过!'
        save_check_results(db_ops, rule, p_user, p_sql,n_sxh)
    return result

def process_single_ddl_proc(p_dbid,p_cdb,p_sql,p_user):
    n_sxh  = 1
    result = True
    ds_cur = get_ds_by_dsid_by_cdb(p_dbid, p_cdb)
    db_cur = get_connection_ds(ds_cur)
    db_ops = get_connection_dict()
    cr_ops = db_ops.cursor()
    ops_sql = """select id,rule_code,rule_name,rule_value,error 
                    from t_sql_audit_rule 
                    where rule_type='ddl' and status='1' and id in(27,28,29,30) order by id"""
    cr_ops.execute(ops_sql)
    rs_ops = cr_ops.fetchall()

    print('输出检测项...')
    print('-'.ljust(150, '-'))
    for r in rs_ops:
        print(r)

    #清空检查表
    del_check_results(db_ops, p_user)

    #检查语句
    for rule in rs_ops:

        rule['error'] = format_sql(rule['error'])

        if rule['rule_code'] == 'switch_check_ddl' and rule['rule_value'] == 'true':
            if get_obj_op(p_sql) in('CREATE_PROCEDURE','CREATE_FUNCTION','CREATE_TRIGGER','CREATE_EVENT'):
                print('检测过程语法及权限...')
                v = get_obj_privs_grammar_proc(db_cur, p_sql.strip())
                if v != '0':
                    if v.count('存在') >0 :
                        rule['error'] = format_sql(format_exception(v))
                        save_check_results(db_ops, rule, p_user, p_sql.strip(),n_sxh)
                        result = False
                        break
                    else:
                        rule['error'] = format_sql(format_exception(v))
                        save_check_results(db_ops, rule, p_user, p_sql.strip(),n_sxh)
                        result = False

        if rule['rule_code'] == 'switch_disable_trigger' and rule['rule_value'] == 'true':
            if get_obj_type(p_sql) == 'TRIGGER':
               save_check_results(db_ops, rule, p_user, p_sql.strip(), n_sxh)
               result = False

        if rule['rule_code'] == 'switch_disable_func' and rule['rule_value'] == 'true':
            if get_obj_type(p_sql) == 'FUNCTION':
               save_check_results(db_ops, rule, p_user, p_sql.strip(), n_sxh)
               result = False

        if rule['rule_code'] == 'switch_disable_proc' and rule['rule_value'] == 'true':
             if get_obj_type(p_sql) == 'PROCEDURE':
                save_check_results(db_ops, rule, p_user, p_sql.strip(), n_sxh)
                result = False

        if rule['rule_code'] == 'switch_disable_event' and rule['rule_value'] == 'true':
             if get_obj_type(p_sql) == 'EVENT':
                save_check_results(db_ops, rule, p_user, p_sql.strip(), n_sxh)
                result = False

    if result:
        rule['id'] = '0'
        rule['error'] = '检测通过!'
        save_check_results(db_ops, rule, p_user, p_sql,n_sxh)
    return result

def get_dml_privs_grammar(p_curdb,p_sql):
    try:
        op = get_obj_op(p_sql)
        cr  = p_curdb.cursor()
        if op in ('INSERT','UPDATE','DELETE'):
            if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) == 0:
                return '表:{0}不存在!'.format(get_obj_name(p_sql))
            try:
                cr.execute(f_get_table_ddl(p_curdb,get_obj_name(p_sql)).replace(get_obj_name(p_sql),'dbops_'+get_obj_name(p_sql)))
                cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
                cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
                return None
            except Exception as e:
                return process_result(str(e))
    except Exception as e:
        return process_result(str(e))

def get_dml_rows(p_curdb,p_sql):
    try:
        if check_mysql_tab_exists(p_curdb, get_obj_name(p_sql)) == 0:
            return '表:{0}不存在!'.format(get_obj_name(p_sql))

        op = get_obj_op(p_sql)
        cr = p_curdb.cursor()
        if op == 'INSERT':
           cr.execute(f_get_table_ddl(p_curdb, get_obj_name(p_sql)).
                        replace(get_obj_name(p_sql),'dbops_' + get_obj_name(p_sql)))
           cr.execute(p_sql.replace(get_obj_name(p_sql), 'dbops_' + get_obj_name(p_sql)))
           cr.execute('select count(0) from {0}'.format('dbops_' + get_obj_name(p_sql)))
           rs=cr.fetchone()
           cr.execute('drop table {0}'.format('dbops_' + get_obj_name(p_sql)))
           return rs[0]
        elif op in('UPDATE','DELETE'):
           cr.execute('select count(0) from {0} {1}'.
                       format( get_obj_name(p_sql),p_sql[p_sql.upper().find('WHERE'):]))
           rs=cr.fetchone()
           return rs[0]

    except Exception as e:
        return process_result(str(e))

def is_number(str):
  try:
    if str=='NaN':
      return False
    float(str)
    return True
  except ValueError:
    return False

def process_single_dml(p_dbid,p_cdb,p_sql,p_user):
    n_sxh  = 1
    result = True
    ds_cur = get_ds_by_dsid_by_cdb(p_dbid, p_cdb)
    db_cur = get_connection_ds(ds_cur)
    db_ops = get_connection_dict()
    cr_ops = db_ops.cursor()
    ops_sql = """select id,rule_code,rule_name,rule_value,error 
                    from t_sql_audit_rule where  rule_type='dml' and status='1'  order by id"""
    cr_ops.execute(ops_sql)
    rs_ops = cr_ops.fetchall()

    print('输出检测项...op=',get_obj_op(p_sql))
    print('-'.ljust(150, '-'))
    for r in rs_ops:
        print(r)

    #清空检查表
    del_check_results(db_ops, p_user)

    #检查语句
    for rule in rs_ops:

        rule['error'] = format_sql(rule['error'])

        if rule['rule_code'] == 'switch_dml_where' and rule['rule_value'] == 'true':
            if get_obj_op(p_sql) in('UPDATE','DELETE'):
               print('检测DML语句条件...')
               if p_sql.upper().strip().count(' WHERE ') == 0:
                    save_check_results(db_ops, rule, p_user, p_sql.strip(), n_sxh)
                    result = False


        if rule['rule_code'] == 'switch_dml_order' and rule['rule_value'] == 'true':
            if get_obj_op(p_sql) in('UPDATE','DELETE'):
               print('DML语句禁用 ORDER BY...')
               if re.search('\s+ORDER\s+BY\s+', p_sql.strip().upper()) is not None:
                  save_check_results(db_ops, rule, p_user, p_sql.strip(), n_sxh)
                  result = False

        if rule['rule_code'] == 'switch_dml_select' and rule['rule_value'] == 'true':
            if get_obj_op(p_sql) in('INSERT','UPDATE','DELETE'):
               print('DML语句禁用 SELECT...')
               if re.search('SELECT\s+', p_sql.strip().upper()) is not None\
                    and re.search('\s+FROM\s+', p_sql.strip().upper()) is not None:
                  save_check_results(db_ops, rule, p_user, p_sql.strip(), n_sxh)
                  result = False

        if rule['rule_code'] == 'switch_dml_max_rows':
            if get_obj_op(p_sql) in('INSERT','UPDATE','DELETE'):
               print('DML最大影响行数...')
               v =  get_dml_rows(db_cur,p_sql)
               print('v=',v)
               if is_number(str(v)):
                   if v > int(rule['rule_value']):
                      rule['error'] = rule['error'].format(rule['rule_value'])
                      save_check_results(db_ops, rule, p_user, p_sql.strip(), n_sxh)
                      result = False
               else:
                   rule['error'] = rule['error'].format(format_exception(v))
                   save_check_results(db_ops, rule, p_user, p_sql.strip(), n_sxh)
                   result = False

        if rule['rule_code'] == 'switch_dml_ins_exists_col' and rule['rule_value'] == 'true':
            if get_obj_op(p_sql) in('INSERT'):
               print('检查插入语句那必须存在列名...')
               n_pos= re.split(r'\s+', p_sql.strip())[2].count(')')
               if n_pos == 0:
                   n_pos = re.split(r'\s+', p_sql.strip())[3].count(')')
               if n_pos == 0:
                   save_check_results(db_ops, rule, p_user, p_sql.strip(), n_sxh)
                   result = False

        if rule['rule_code'] == 'switch_dml_ins_cols' \
                and get_audit_rule('switch_dml_ins_exists_col')['rule_value'] == 'true':
           if get_obj_op(p_sql) in ('INSERT'):
               print('INSERT语句字段上限...')
               n_cols = 0
               try:
                   n_cols = re.split(r'\s+',  p_sql.strip())[2].split('(')[1].split(')')[0].count(',')+1
               except:
                   n_cols = re.split(r'\s+', p_sql.strip())[3].split('(')[1].split(')')[0].count(',')+1
               if n_cols>int(rule['rule_value']):
                  rule['error'] =rule['error'].format(rule['rule_value'])
                  save_check_results(db_ops, rule, p_user, p_sql.strip(), n_sxh)
                  result = False


        if result:
            if rule['rule_code'] == 'switch_check_dml' and rule['rule_value'] == 'true':
                if get_obj_op(p_sql) in ('INSERT', 'UPDATE', 'DELETE'):
                    print('检测DML语法及权限...')
                    v = get_dml_privs_grammar(db_cur, p_sql.strip())
                    if v is not None:
                        rule['error'] = format_sql(format_exception(v))
                        save_check_results(db_ops, rule, p_user, p_sql.strip(), n_sxh)
                        result = False


    if result:
        rule['id'] = '0'
        rule['error'] = '检测通过!'
        save_check_results(db_ops, rule, p_user, p_sql,n_sxh)

    return result

def process_multi_ddl(p_dbid,p_cdb,p_sql,p_user):
    sxh     = 1
    results = True
    config  = {}
    ds_cur  = get_ds_by_dsid_by_cdb(p_dbid, p_cdb)
    db_cur  = get_connection_ds(ds_cur)
    db_ops  = get_connection_dict()

    #清空检查表
    del_check_results(db_ops, p_user)

    #逐条检查语句
    for st in p_sql.split(';'):
        result = True

        if st.strip() == '':
           continue

        print('check sql :',st.strip())
        cr_ops  = db_ops.cursor()
        ops_sql = """select id,rule_code,rule_name,rule_value,error 
                       from t_sql_audit_rule
                        where  rule_type='ddl' and status='1' and id not in (27,28,29,30) order by id"""
        cr_ops.execute(ops_sql)
        rs_ops  = cr_ops.fetchall()

        print('输出检测项...')
        print('-'.ljust(150, '-'))
        for r in rs_ops:
            print(r)

        for rule in rs_ops:

            rule['error'] = format_sql(rule['error'])

            if rule['rule_code'] == 'switch_check_ddl' and rule['rule_value'] == 'true':
                if get_obj_type(st.strip()) == 'TABLE':
                    print('检测DDL语法及权限...')
                    v = get_obj_privs_grammar_multi(db_cur, st.strip(),config)
                    if v != '0':
                        if v.count('存在') > 0:
                            rule['error'] = format_sql(format_exception(v))
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False
                            break
                        else:
                            rule['error'] = format_sql(format_exception(v))
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False

            if rule['rule_code'] == 'switch_tab_not_exists_pk' and rule['rule_value'] == 'true':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('检查表必须有主键...')
                    if get_obj_type(st.strip()) == 'TABLE' and not (
                            st.strip().upper().count('PRIMARY') > 0 and st.strip().upper().count('KEY') > 0):
                        rule['error'] =rule['error'].format(get_obj_name(st.strip()))
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                        result = False

            if rule['rule_code'] == 'switch_tab_pk_id' and rule['rule_value'] == 'true':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('强制主键名为ID...')
                    if get_obj_type(st.strip()) == 'TABLE' \
                            and (st.strip().upper().count('PRIMARY') > 0 and st.strip().upper().count('KEY') > 0) :
                       v  = get_obj_pk_name_multi(db_cur,st.strip(),config)
                       if v == 0:
                            rule['error'] = rule['error'].format(get_obj_name(st.strip()))
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False

                       if v not in (0,1):
                           rule['error'] = v
                           save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                           result = False

            if rule['rule_code'] == 'switch_tab_pk_auto_incr' and rule['rule_value'] == 'true':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('强制主键为自增列...')
                    if get_obj_type(st.strip()) == 'TABLE' \
                            and (st.strip().upper().count('PRIMARY') > 0 and st.strip().upper().count('KEY') > 0) :
                        v =  get_obj_pk_exists_auto_incr_multi(db_cur, st.strip(),config)
                        if v == 0 :
                            rule['error'] = rule['error'].format(get_obj_name(st.strip()))
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False

                        if v not in (0, 1):
                            rule['error'] = v
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False


            if rule['rule_code'] == 'switch_tab_pk_autoincrement_1' and rule['rule_value'] == 'true':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('强制自增列初始值为1...')
                    if get_obj_type(st.strip()) == 'TABLE' \
                            and (st.strip().upper().count('PRIMARY') > 0  and st.strip().upper().count('KEY') > 0):
                        v =  get_obj_exists_auto_incr_not_1_multi(db_cur, st.strip(),config)
                        if v == 0:
                            rule['error'] = rule['error'].format(get_obj_name(st.strip()))
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False

                        if v not in (0, 1):
                            rule['error'] = v
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False

            if rule['rule_code'] == 'switch_pk_not_int_bigint' and rule['rule_value'] == 'false':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('不允许主键类型非int/bigint...')
                    if get_obj_type(st.strip()) == 'TABLE' \
                            and (st.strip().upper().count('PRIMARY') > 0 and st.strip().upper().count('KEY') > 0):
                        v =  get_obj_pk_type_not_int_bigint_multi(db_cur, st.strip(),config)
                        if v == 1 :
                            rule['error'] = rule['error'].format(get_obj_name(st.strip()))
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False

                        if v not in (0, 1):
                            rule['error'] = v
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False

            if rule['rule_code'] == 'switch_tab_comment' and rule['rule_value'] == 'true':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('检查表注释...')
                    if get_obj_type(st.strip()) == 'TABLE':
                        v = get_tab_comment_multi(db_cur, st.strip(),config)
                        if v ==0:
                            rule['error'] = rule['error'].format(get_obj_name(st.strip()))
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False

                        if v not in (0, 1):
                            rule['error'] = v
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False

            if rule['rule_code'] == 'switch_col_comment' \
                    and rule['rule_value'] == 'true' and get_obj_type(st.strip()) == 'TABLE':
                if get_obj_op(st.strip()) in ('CREATE_TABLE', 'ALTER_TABLE_ADD'):
                    print('检查列注释...')
                    v = get_col_comment_multi(db_cur, st.strip(),config)
                    e = rule['error']
                    try:
                        for i in v:
                            if i[2] == 0:
                                result = False
                                rule['error'] = e.format(i[0].
                                                 replace('dbops_'+ get_obj_name(st.strip()),get_obj_name(st.strip())),i[1])
                                save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except IndexError as e:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)

            if rule['rule_code'] == 'switch_col_not_null' \
                    and rule['rule_value'] == 'true' and get_obj_type(st.strip()) == 'TABLE':
                if get_obj_op(st.strip()) in ('CREATE_TABLE', 'ALTER_TABLE_ADD'):
                    print('检查列是否为空...')
                    v = get_col_not_null_multi(db_cur, st.strip(),config)
                    e = rule['error']
                    try:
                        for i in v:
                            if i[2] == 0:
                                result = False
                                rule['error'] = e.format(i[0].
                                                replace('dbops_' + get_obj_name(st.strip()), get_obj_name(st.strip())),i[1])
                                save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except IndexError as e:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)


            if rule['rule_code'] == 'switch_col_default_value' \
                    and rule['rule_value'] == 'true' and get_obj_type(st.strip()) == 'TABLE':
                if get_obj_op(st.strip()) in ('CREATE_TABLE', 'ALTER_TABLE_ADD'):
                    print('检查列默认值...')
                    v = get_col_default_value_multi(db_cur, st.strip(),config)
                    e = rule['error']
                    try:
                        for i in v:
                            if i[2] == 0:
                                result = False
                                rule['error'] = e.format(
                                    i[0].replace('dbops_' + get_obj_name(st.strip()), get_obj_name(st.strip())),
                                    i[1])
                                save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except IndexError as e:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)

            if rule['rule_code'] == 'switch_time_col_default_value' \
                    and rule['rule_value'] == 'true' and get_obj_type(st.strip()) == 'TABLE':
                if get_obj_op(st.strip()) in ('CREATE_TABLE'):
                    print('检查时间字段默认值...')
                    v = get_time_col_default_value_multi(db_cur, st.strip(),config)
                    e = rule['error']
                    try:
                        for i in v:
                            if i[3] == 0:
                                result = False
                                rule['error'] = e.format(i[0], i[1], i[2])
                                save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except IndexError as e:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)

            if rule['rule_code'] == 'switch_char_max_len' and get_obj_type(st.strip()) == 'TABLE':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('字符字段最大长度...')
                    v = get_tab_char_col_len_multi(db_cur, st.strip(), rule,config)
                    e = rule['error']
                    try:
                        for i in v:
                            if i[2] == 0:
                                result = False
                                rule['error'] = e.format(i[0], i[1], rule['rule_value'])
                                save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except IndexError as e:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)


            if rule['rule_code'] == 'switch_tab_has_time_fields' and get_obj_type(st.strip()) == 'TABLE':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('表必须拥有字段...')
                    v = get_tab_has_fields_multi(db_cur, st.strip(),config)
                    e = rule['error']
                    try:
                        for i in v:
                            result = False
                            rule['error'] = e.format(i[0], i[1])
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except IndexError as e:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)

            if rule['rule_code'] == 'switch_tab_tcol_datetime' \
                    and rule['rule_value'] == 'true' and get_obj_type(st.strip()) == 'TABLE':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('时间字段类型为datetime...')
                    v = get_tab_tcol_datetime_multi(db_cur, st.strip(),config)
                    e = rule['error']
                    try:
                        for i in v:
                            result = False
                            rule['error'] = e.format(i[0], i[1])
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except IndexError as e:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)

        cr_ops.close()

        print('result=',result,get_obj_name(st.strip()))
        if result:
           rule['id'] = '0'
           rule['error'] = '检测通过!'
           save_check_results(db_ops, rule, p_user, st.strip(),sxh)

        results =results and  result
        sxh = sxh +1

    print('删除临时表...')
    print('config=', config, type(config))
    print('-'.ljust(150, '-'))
    cr = db_cur.cursor()
    for key in config:
       try:
          print(config[key])
          cr.execute(config[key])
       except Exception as e:
         print(traceback.format_exc())
    print('-'.ljust(150, '-')+'\n')
    return results

def process_multi_dml(p_dbid,p_cdb,p_sql,p_user):
    sxh     = 1
    results = True
    config  = {}
    ds_cur  = get_ds_by_dsid_by_cdb(p_dbid, p_cdb)
    db_cur  = get_connection_ds(ds_cur)
    db_ops  = get_connection_dict()

    #清空检查表
    del_check_results(db_ops, p_user)

    #逐条检查语句
    for st in p_sql.split(';'):
        result = True

        if st.strip() == '':
           continue

        print('check sql :',st.strip())
        cr_ops  = db_ops.cursor()
        ops_sql = """select id,rule_code,rule_name,rule_value,error 
                        from t_sql_audit_rule where rule_type='dml' and status='1' order by id"""
        cr_ops.execute(ops_sql)
        rs_ops  = cr_ops.fetchall()

        print('输出检测项...')
        print('-'.ljust(150, '-'))
        for r in rs_ops:
            print(r)

        for rule in rs_ops:

            rule['error'] = format_sql(rule['error'])

            if rule['rule_code'] == 'switch_check_ddl' and rule['rule_value'] == 'true':
                if get_obj_type(st.strip()) == 'TABLE':
                    print('检测DDL语法及权限...')
                    v = get_obj_privs_grammar_multi(db_cur, st.strip(),config)
                    if v != '0':
                        if v.count('存在') > 0:
                            rule['error'] = format_sql(format_exception(v))
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False
                            break
                        else:
                            rule['error'] = format_sql(format_exception(v))
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False

            if rule['rule_code'] == 'switch_tab_not_exists_pk' and rule['rule_value'] == 'true':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('检查表必须有主键...')
                    if get_obj_type(st.strip()) == 'TABLE' and not (
                            st.strip().upper().count('PRIMARY') > 0 and st.strip().upper().count('KEY') > 0):
                        rule['error'] =rule['error'].format(get_obj_name(st.strip()))
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                        result = False

            if rule['rule_code'] == 'switch_tab_pk_id' and rule['rule_value'] == 'true':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('强制主键名为ID...')
                    if get_obj_type(st.strip()) == 'TABLE' \
                            and (st.strip().upper().count('PRIMARY') > 0 and st.strip().upper().count('KEY') > 0) :
                       v  = get_obj_pk_name_multi(db_cur,st.strip(),config)
                       if v == 0:
                            rule['error'] = rule['error'].format(get_obj_name(st.strip()))
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False

                       if v not in (0,1):
                           rule['error'] = v
                           save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                           result = False

            if rule['rule_code'] == 'switch_tab_pk_auto_incr' and rule['rule_value'] == 'true':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('强制主键为自增列...')
                    if get_obj_type(st.strip()) == 'TABLE' \
                            and (st.strip().upper().count('PRIMARY') > 0 and st.strip().upper().count('KEY') > 0) :
                        v =  get_obj_pk_exists_auto_incr_multi(db_cur, st.strip(),config)
                        if v == 0 :
                            rule['error'] = rule['error'].format(get_obj_name(st.strip()))
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False

                        if v not in (0, 1):
                            rule['error'] = v
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False


            if rule['rule_code'] == 'switch_tab_pk_autoincrement_1' and rule['rule_value'] == 'true':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('强制自增列初始值为1...')
                    if get_obj_type(st.strip()) == 'TABLE' \
                            and (st.strip().upper().count('PRIMARY') > 0  and st.strip().upper().count('KEY') > 0):
                        v =  get_obj_exists_auto_incr_not_1_multi(db_cur, st.strip(),config)
                        if v == 0:
                            rule['error'] = rule['error'].format(get_obj_name(st.strip()))
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False

                        if v not in (0, 1):
                            rule['error'] = v
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False

            if rule['rule_code'] == 'switch_pk_not_int_bigint' and rule['rule_value'] == 'false':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('不允许主键类型非int/bigint...')
                    if get_obj_type(st.strip()) == 'TABLE' \
                            and (st.strip().upper().count('PRIMARY') > 0 and st.strip().upper().count('KEY') > 0):
                        v =  get_obj_pk_type_not_int_bigint_multi(db_cur, st.strip(),config)
                        if v == 1 :
                            rule['error'] = rule['error'].format(get_obj_name(st.strip()))
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False

                        if v not in (0, 1):
                            rule['error'] = v
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False

            if rule['rule_code'] == 'switch_tab_comment' and rule['rule_value'] == 'true':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('检查表注释...')
                    if get_obj_type(st.strip()) == 'TABLE':
                        v = get_tab_comment_multi(db_cur, st.strip(),config)
                        if v ==0:
                            rule['error'] = rule['error'].format(get_obj_name(st.strip()))
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False

                        if v not in (0, 1):
                            rule['error'] = v
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                            result = False

            if rule['rule_code'] == 'switch_col_comment' \
                    and rule['rule_value'] == 'true' and get_obj_type(st.strip()) == 'TABLE':
                if get_obj_op(st.strip()) in ('CREATE_TABLE', 'ALTER_TABLE_ADD'):
                    print('检查列注释...')
                    v = get_col_comment_multi(db_cur, st.strip(),config)
                    e = rule['error']
                    try:
                        for i in v:
                            if i[2] == 0:
                                result = False
                                rule['error'] = e.format(i[0].
                                                 replace('dbops_'+ get_obj_name(st.strip()),get_obj_name(st.strip())),i[1])
                                save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except IndexError as e:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)

            if rule['rule_code'] == 'switch_col_not_null' \
                    and rule['rule_value'] == 'true' and get_obj_type(st.strip()) == 'TABLE':
                if get_obj_op(st.strip()) in ('CREATE_TABLE', 'ALTER_TABLE_ADD'):
                    print('检查列是否为空...')
                    v = get_col_not_null_multi(db_cur, st.strip(),config)
                    e = rule['error']
                    try:
                        for i in v:
                            if i[2] == 0:
                                result = False
                                rule['error'] = e.format(i[0].
                                                replace('dbops_' + get_obj_name(st.strip()), get_obj_name(st.strip())),i[1])
                                save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except IndexError as e:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)


            if rule['rule_code'] == 'switch_col_default_value' \
                    and rule['rule_value'] == 'true' and get_obj_type(st.strip()) == 'TABLE':
                if get_obj_op(st.strip()) in ('CREATE_TABLE', 'ALTER_TABLE_ADD'):
                    print('检查列默认值...')
                    v = get_col_default_value_multi(db_cur, st.strip(),config)
                    e = rule['error']
                    try:
                        for i in v:
                            if i[2] == 0:
                                result = False
                                rule['error'] = e.format(
                                    i[0].replace('dbops_' + get_obj_name(st.strip()), get_obj_name(st.strip())),
                                    i[1])
                                save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except IndexError as e:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)

            if rule['rule_code'] == 'switch_time_col_default_value' \
                    and rule['rule_value'] == 'true' and get_obj_type(st.strip()) == 'TABLE':
                if get_obj_op(st.strip()) in ('CREATE_TABLE'):
                    print('检查时间字段默认值...')
                    v = get_time_col_default_value_multi(db_cur, st.strip(),config)
                    e = rule['error']
                    try:
                        for i in v:
                            if i[3] == 0:
                                result = False
                                rule['error'] = e.format(i[0], i[1], i[2])
                                save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except IndexError as e:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)

            if rule['rule_code'] == 'switch_char_max_len' and get_obj_type(st.strip()) == 'TABLE':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('字符字段最大长度...')
                    v = get_tab_char_col_len_multi(db_cur, st.strip(), rule,config)
                    e = rule['error']
                    try:
                        for i in v:
                            if i[2] == 0:
                                result = False
                                rule['error'] = e.format(i[0], i[1], rule['rule_value'])
                                save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except IndexError as e:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)


            if rule['rule_code'] == 'switch_tab_has_time_fields' and get_obj_type(st.strip()) == 'TABLE':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('表必须拥有字段...')
                    v = get_tab_has_fields_multi(db_cur, st.strip(),config)
                    e = rule['error']
                    try:
                        for i in v:
                            result = False
                            rule['error'] = e.format(i[0], i[1])
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except IndexError as e:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)

            if rule['rule_code'] == 'switch_tab_tcol_datetime' \
                    and rule['rule_value'] == 'true' and get_obj_type(st.strip()) == 'TABLE':
                if get_obj_op(st.strip()) == 'CREATE_TABLE':
                    print('时间字段类型为datetime...')
                    v = get_tab_tcol_datetime_multi(db_cur, st.strip(),config)
                    e = rule['error']
                    try:
                        for i in v:
                            result = False
                            rule['error'] = e.format(i[0], i[1])
                            save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except IndexError as e:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)
                    except:
                        result = False
                        rule['error'] = v
                        save_check_results(db_ops, rule, p_user, st.strip(),sxh)

        cr_ops.close()

        print('result=',result,get_obj_name(st.strip()))
        if result:
           rule['id'] = '0'
           rule['error'] = '检测通过!'
           save_check_results(db_ops, rule, p_user, st.strip(),sxh)

        results =results and  result
        sxh = sxh +1

    print('删除临时表...')
    print('config=', config, type(config))
    print('-'.ljust(150, '-'))
    cr = db_cur.cursor()
    for key in config:
       try:
          print(config[key])
          cr.execute(config[key])
       except Exception as e:
         print(traceback.format_exc())
    print('-'.ljust(150, '-')+'\n')
    return results

def get_audit_rule(p_key):
    db_ops = get_connection_dict()
    cr_ops = db_ops.cursor()
    ops_sql = "select * from t_sql_audit_rule where rule_code='{0}'".format(p_key)
    cr_ops.execute(ops_sql)
    rs=cr_ops.fetchone()
    cr_ops.close()
    return rs


def check_mysql_ddl(p_dbid,p_cdb,p_sql,p_user,p_type):
    db_ops =  get_connection_dict()
    del_check_results(db_ops, p_user)
    # 工单类型为为函数、过程、触发器、事件
    if p_type == '4':
        print('process_single_ddl....')
        return process_single_ddl_proc(p_dbid, p_cdb, p_sql.strip(), p_user)
    else:
        # 工单类型为为单个DDL、DML、DCL
        if p_sql.count(';') == 0:
            # 处理单个DDL
            if p_type in('1','3'):
               print('process_single_ddl....')
               return process_single_ddl(p_dbid,p_cdb,p_sql.strip(),p_user)
            #处理单个DML
            elif p_type == '2':
               print('process_single_dml....')
               return process_single_dml(p_dbid, p_cdb, p_sql.strip(), p_user)
        elif p_sql.count(';') == 1:
            # 处理单个DDL
            if p_type in('1','3'):
                print('process_single_ddl....')
                return process_single_ddl(p_dbid, p_cdb, p_sql.strip().replace(';',''), p_user)
            # 处理单个DML
            elif p_type == '2':
                print('process_single_dml....')
                return process_single_dml(p_dbid, p_cdb, p_sql.strip().replace(';',''), p_user)
        # 工单类型为为多个DDL、DML、DCL
        else:
            # 处理多个DDL
            if p_type in('1','3'):
                rule = get_audit_rule('switch_ddl_batch')
                if rule['rule_value'] == 'true':
                   print('process_multi_ddl....')
                   return process_multi_ddl(p_dbid, p_cdb, p_sql.strip(), p_user)
                else:
                   rule['error'] = format_sql(rule['error'])
                   save_check_results(db_ops, rule, p_user, '---', 1)
                   return False
            # 处理多个DML
            elif p_type == '2':
                rule = get_audit_rule('switch_dml_batch')
                if rule['rule_value'] == 'true':
                    print('process_multi_dml....')
                    return process_multi_dml(p_dbid, p_cdb, p_sql.strip(), p_user)
                else:
                    rule['error'] = format_sql(rule['error'])
                    save_check_results(db_ops, rule, p_user, '---', 1)
                    return False


def save_check_results(db,rule,user,psql,sxh):
    cr  = db.cursor()
    print('检查结果：')
    print('-'.ljust(150, '-'))
    obj = get_obj_name(psql)

    if rule['error'] == '检测通过!':
        sql = '''insert into t_sql_audit_rule_err(xh,obj_name,rule_id,rule_name,rule_value,user_id,error) values ('{}','{}','{}','{}','{}','{}','{}')
              '''.format(sxh, obj,'', '', '', user['userid'],rule['error'])
    else:
        sql = '''insert into t_sql_audit_rule_err(xh,obj_name,rule_id,rule_name,rule_value,user_id,error) values ('{}','{}','{}','{}','{}','{}','{}')
              '''.format(sxh,obj,rule['id'],rule['rule_name'],rule['rule_value'],user['userid'],rule['error'])
    print(sql)
    cr.execute(sql)
    db.commit()