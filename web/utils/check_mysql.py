#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/11 23:31
# @Author : 马飞
# @File : check_mysql.py
# @Software: PyCharm

import re
from  web.settings.config   import devconfig
from  web.model.t_role      import is_dba
from web.model.t_ds         import get_ds_by_dsid
from web.utils.common       import get_connection,get_connection_ds,get_connection_ds_uat
from web.utils.common       import get_connection_ds_sqlserver,get_connection_ds_uat_sqlserver
from web.utils.common       import exception_info_mysql,format_error,format_check

def check_view_ddl(p_sql):
    result = {}
    if p_sql.upper().count("CREATE")>0 and p_sql.upper().count("VIEW")>0:
        if  p_sql.upper().count("ALGORITHM")>0  and p_sql.upper().find("ALGORITHM")>p_sql.upper().find("CREATE") and p_sql.upper().find("ALGORITHM")<p_sql.upper().find("VIEW") :
            result['code'] = 1
            result['message'] = 'CREATE VIEW 间不允许出现以下关键字！ALGORITHM'
            return result
        if p_sql.upper().count("DEFINER") > 0 and p_sql.upper().find("DEFINER") > p_sql.upper().find("CREATE") and p_sql.upper().find("DEFINER") < p_sql.upper().find("VIEW"):
            result['code'] = 1
            result['message'] = 'CREATE VIEW 间不允许出现以下关键字！DEFINER'
            return result
        if p_sql.upper().count("SQL") > 0 and p_sql.upper().find("SQL") > p_sql.upper().find("CREATE") and p_sql.upper().find("SQL") < p_sql.upper().find("VIEW"):
            result['code'] = 1
            result['message'] = 'CREATE VIEW 间不允许出现以下关键字！SQL'
            return result
        if p_sql.upper().count("SECURITY") > 0 and p_sql.upper().find("SECURITY") > p_sql.upper().find("CREATE") and p_sql.upper().find("SECURITY") < p_sql.upper().find("VIEW"):
            result['code'] = 1
            result['message'] = 'CREATE VIEW 间不允许出现以下关键字！SECURITY'
            return result
    result['code'] = 0
    result['message'] = ''
    return result

def check_func_ddl(p_sql):
    result = {}
    if p_sql.upper().count("CREATE")>0 and p_sql.upper().count("FUNCTION")>0:
        if  p_sql.upper().count("DEFINER")>0  and p_sql.upper().find("DEFINER")>p_sql.upper().find("CREATE") and p_sql.upper().find("DEFINER")<p_sql.upper().find("FUNCTION") :
            result['code'] = 1
            result['message'] = 'CREATE FUNCTION 间不允许出现以下关键字！DEFINER'
            return result
    result['code'] = 0
    result['message'] = ''
    return result

def check_proc_ddl(p_sql):
    result = {}
    if p_sql.upper().count("CREATE")>0 and p_sql.upper().count("PROCEDURE")>0:
        if  p_sql.upper().count("DEFINER")>0  and p_sql.upper().find("DEFINER")>p_sql.upper().find("CREATE") and p_sql.upper().find("DEFINER")<p_sql.upper().find("PROCEDURE") :
            result['code'] = 1
            result['message'] = 'CREATE PROCEDURE 间不允许出现以下关键字！DEFINER'
            return result
    result['code'] = 0
    result['message'] = ''
    return result

def check_trg_ddl(p_sql):
    result = {}
    if p_sql.upper().count("CREATE")>0 and p_sql.upper().count("TRIGGER")>0:
        if  p_sql.upper().count("DEFINER")>0  and p_sql.upper().find("DEFINER")>p_sql.upper().find("CREATE") and p_sql.upper().find("DEFINER")<p_sql.upper().find("TRIGGER") :
            result['code'] = 1
            result['message'] = 'CREATE TRIGGER 间不允许出现以下关键字！DEFINER'
            return result
    result['code'] = 0
    result['message'] = ''
    return result

def get_obj_name(p_sql):
    if p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("TABLE") > 0\
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
    else:
       return ''

def get_obj_type(p_sql):
    if p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("TABLE") > 0\
          or  p_sql.upper().count("CREATE")>0 and p_sql.upper().count("VIEW")>0 \
            or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("FUNCTION") > 0 \
             or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("PROCEDURE") > 0 \
               or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("INDEX") > 0 \
                  or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("TRIGGER") > 0:

       if p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("INDEX") > 0 and p_sql.upper().count("UNIQUE") > 0:
           obj = 'UNIQUE-INDEX'
       elif p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("INDEX") > 0 and len(p_sql.upper().split('ON')[1].split('(')[1].replace(')','').split(','))>1:
           obj = 'COMPOSITE-INDEX'
       else:
           obj=re.split(r'\s+', p_sql)[1].replace('`', '')

       if ('(') in obj:
          return obj.split('(')[0].upper()
       else:
          return obj.upper()
    else:
       return ''

def check_obj_prefix(p_sql):
    result = {}
    result['code'] = '0'
    result['message'] = ''

    if get_obj_type(p_sql)=='TABLE' and get_obj_name(p_sql).split('_')[0]=='':
        result['code'] = '1'
        result['message'] = '表名必须有对象类型前缀!'
        return result

    if get_obj_type(p_sql)=='VIEW':
         if get_obj_name(p_sql).split("_")[0]=='':
             result['code'] = '1'
             result['message'] = '视图名必须有对象类型前缀!'
             return result
         elif get_obj_name(p_sql).split("_")[0]!='V':
             result['code'] = '1'
             result['message'] = '视图名对象类型前缀必须为V!'
             return result

    if get_obj_type(p_sql) == 'FUNCTION':
        if get_obj_name(p_sql).split("_")[0] == '':
            result['code'] = '1'
            result['message'] = '函数名必须有对象类型前缀!'
            return result
        elif get_obj_name(p_sql).split("_")[0] !='F':
            result['code'] = '1'
            result['message'] = '函数名对象类型前缀必须为F!'
            return result

    if get_obj_type(p_sql) == 'PROCEDURE':
        if get_obj_name(p_sql).split("_")[0] == '':
            result['code'] = '1'
            result['message'] = '过程名必须有对象类型前缀!'
            return result
        elif get_obj_name(p_sql).split("_")[0] != 'PROC':
            result['code'] = '1'
            result['message'] = '过程名对象类型前缀必须为PROC!'
            return result

    if get_obj_type(p_sql) == 'TRIGGER':
        if get_obj_name(p_sql).split("_")[0] == '':
            result['code'] = '1'
            result['message'] = '触发器名必须有对象类型前缀!'
            return result
        elif get_obj_name(p_sql).split("_")[0] != 'TR':
            result['code'] = '1'
            result['message'] = '触发器名对象类型前缀必须为TR!'
            return result

    if get_obj_type(p_sql) == 'INDEX':
        if get_obj_name(p_sql).split("_")[0] == '':
            result['code'] = '1'
            result['message'] = '索引名必须有对象类型前缀!'
            return result
        elif get_obj_name(p_sql).split("_")[0] != 'IX':
            result['code'] = '1'
            result['message'] = '普通索引名对象类型前缀必须为IX!'
            return result

    if get_obj_type(p_sql) == 'UNIQUE-INDEX':
        if get_obj_name(p_sql).split("_")[0] == '':
            result['code'] = '1'
            result['message'] = '索引名必须有对象类型前缀!'
            return result
        elif get_obj_name(p_sql).split("_")[0] != 'UIX':
            result['code'] = '1'
            result['message'] = '唯一索引名对象类型前缀必须为UIX!'
            return result

    if get_obj_type(p_sql) == 'COMPOSITE-INDEX':
        if get_obj_name(p_sql).split("_")[0] == '':
            result['code'] = '1'
            result['message'] = '索引名必须有对象类型前缀!'
            return result
        elif get_obj_name(p_sql).split("_")[0] != 'CIX':
            result['code'] = '1'
            result['message'] = '复合索引名对象类型前缀必须为CIX!'
            return result

    return result

def check_object_length(p_sql):
    result = {}
    #检测对象：表
    if p_sql.upper().count("CREATE")>0 and p_sql.upper().count("TABLE")>0:
        v_obj = re.split(r'\s+', p_sql)[2].replace('`', '')
        if v_obj.find('(')>0:
           v_obj=v_obj.split('(')[0]
           if len(v_obj)>30:
               result['code'] = 1
               result['message'] = '表名长度不能超过30个字符!'
               return result
           else:
               result['code'] = 0
               result['message'] = ''
               return result
        elif len(v_obj)>30:
           result['code'] = 1
           result['message'] = '表名长度不能超过30个字符!'
           return result
        else:
            result['code'] = 0
            result['message'] = ''
            return result

    #检测对象：视图
    elif p_sql.upper().count("CREATE")>0 and p_sql.upper().count("VIEW")>0:

        #栓查视图创建语句是否合法
        if check_view_ddl(p_sql)['code']==1:
            return check_view_ddl(p_sql)

        v_obj = re.split(r'\s+', p_sql)[2].replace('`', '')
        if v_obj.find('(')>0:
           v_obj=v_obj.split('(')[0]
           if len(v_obj)>30:
               result['code'] = 1
               result['message'] = '视图名长度不能超过30个字符!'
               return result
           else:
               result['code'] = 0
               result['message'] = ''
               return result
        elif len(v_obj)>30:
           result['code'] = 1
           result['message'] = '视图名长度不能超过30个字符!'
           return result
        else:
            result['code'] = 0
            result['message'] = ''
            return result

    #检测对象：函数
    elif p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("FUNCTION") > 0:

        # 栓查函数创建语句是否合法
        if check_func_ddl(p_sql)['code'] == 1:
            return check_func_ddl(p_sql)

        v_obj = re.split(r'\s+',p_sql)[2].replace('`', '')
        if v_obj.find('(') > 0:
            v_obj = v_obj.split('(')[0]
            if len(v_obj) > 30:
                result['code'] = 1
                result['message'] = '函数名长度不能超过30个字符!'
                return result
            else:
                result['code'] = 0
                result['message'] = ''
                return result
        elif len(v_obj) > 30:
            result['code'] = 1
            result['message'] = '函数名长度不能超过30个字符!'
            return result
        else:
            result['code'] = 0
            result['message'] = ''
            return result

    #检测对象：过程
    elif p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("PROCEDURE") > 0:

        # 栓查过程创建语句是否合法
        if check_proc_ddl(p_sql)['code'] == 1:
            return check_proc_ddl(p_sql)

        v_obj = re.split(r'\s+', p_sql)[2].replace('`', '')
        if v_obj.find('(') > 0:
            v_obj = v_obj.split('(')[0]
            if len(v_obj) > 30:
                result['code'] = 1
                result['message'] = '过程名长度不能超过30个字符!'
                return result
            else:
                result['code'] = 0
                result['message'] = ''
                return result
        elif len(v_obj) > 30:
            result['code'] = 1
            result['message'] = '过程名长度不能超过30个字符!'
            return result
        else:
            result['code'] = 0
            result['message'] = ''
            return result

    #检测对象：触发器
    elif p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("TRIGGER") > 0:

        # 栓查触发器创建语句是否合法
        if check_trg_ddl(p_sql)['code'] == 1:
            return check_trg_ddl(p_sql)

        v_obj = re.split(r'\s+', p_sql)[2].replace('`', '')
        if v_obj.find('(') > 0:
            v_obj = v_obj.split('(')[0]
            if len(v_obj) > 30:
                result['code'] = 1
                result['message'] = '触发器长度不能超过30个字符!'
                return result
            else:
                result['code'] = 0
                result['message'] = ''
                return result
        elif len(v_obj) > 30:
            result['code'] = 1
            result['message'] = '触发器长度不能超过30个字符!'
            return result
        else:
            result['code'] = 0
            result['message'] = ''
            return result
    else:
        result['code'] = 0
        result['message'] = ''
        return result

def check_tab_drop(p_sql):
    result = {}
    result['code'] = '0'
    result['message'] = ''
    if p_sql.upper().count("ALTER") > 1  and p_sql.upper().count("TABLE") > 1 and p_sql.upper().count("DROP") > 1\
            and p_sql.upper().find("TABLE") > p_sql.upper().find("ALTER") \
            and p_sql.upper().find("DROP") > p_sql.upper().find("TABLE")\
            and get_obj_type(p_sql)=='TABLE':
        result['code'] = '1'
        result['message'] = '不允许发布 ALTER TABLE DROP 操作!'
        return result

    if p_sql.upper().count("DROP") > 1 and p_sql.upper().count("TABLE") > 1 \
            and p_sql.upper().find("TABLE") > p_sql.upper().find("DROP") \
            and get_obj_type(p_sql) == 'TABLE' :
        result['code'] = '1'
        result['message'] = '不允许发布 DROP TABLE 操作!'
        return result
    return result

def check_ddl_syntax(p_dbid,p_sql):
    result = {}
    result['code'] = '0'
    result['message'] = ''
    p_ds    = get_ds_by_dsid(p_dbid)
    db_uat  = get_connection_ds_uat(p_ds)
    cr_uat  = db_uat.cursor()
    v_sql_check = ''
    v_sql_roll = ''

    if p_sql.upper().count("CREATE")>0 and get_obj_type(p_sql)=='TABLE':
        try:
           v_sql_check=p_sql.replace(get_obj_name(p_sql),get_obj_name(p_sql)+'_test')
           v_sql_roll='drop table '+get_obj_name(p_sql)+'_test'
           cr_uat.execute (v_sql_check)
           cr_uat.execute (v_sql_roll)
           db_uat.commit()
           cr_uat.close()
        except:
           v_env = 'UAT'
           result['code'] = '1'
           result['message'] =format_error(v_env,exception_info_mysql())
           return result

    if p_sql.upper().count("CREATE")>0 and get_obj_type(p_sql)=='VIEW':
        try:
            v_sql_check = p_sql.replace(get_obj_name(p_sql), get_obj_name(p_sql) + '_test')
            v_sql_roll = 'drop view ' + get_obj_name(p_sql) + '_test'
            cr_uat.execute(v_sql_check)
            cr_uat.execute(v_sql_roll)
            db_uat.commit()
            cr_uat.close()
        except:
            v_env = 'UAT'
            result['code'] = '1'
            result['message'] = format_error(v_env, exception_info_mysql())
            return result

    if p_sql.upper().count("CREATE")>0 and get_obj_type(p_sql)=='INDEX':
        try:
            v_tab_name  = p_sql.upper().split('ON')[1].split('(')[0].replace(' ','')
            v_sql_check = p_sql
            v_sql_roll  = 'drop index ' + get_obj_name(p_sql) + ' on '+v_tab_name
            cr_uat.execute(v_sql_check)
            cr_uat.execute(v_sql_roll)
            db_uat.commit()
            cr_uat.close()
        except:
            v_env = 'UAT'
            result['code'] = '1'
            result['message'] = format_error(v_env, exception_info_mysql())
            return result

    if get_obj_type(p_sql)=='FUNCTION':
        try:
           v_sql_check=p_sql.replace(get_obj_name(p_sql),get_obj_name(p_sql)+'_test')
           v_sql_roll='drop function '+get_obj_name(p_sql)+'_test'
           cr_uat.execute (v_sql_check)
           cr_uat.execute (v_sql_roll)
           db_uat.commit()
           cr_uat.close()
        except:
           v_env = 'UAT'
           result['code'] = '1'
           result['message'] =format_error(v_env,exception_info_mysql())
           return result

    if get_obj_type(p_sql)=='PROCEDURE':
        try:
            v_sql_check = p_sql.replace(get_obj_name(p_sql), get_obj_name(p_sql) + '_test')
            v_sql_roll = 'drop procedure ' + get_obj_name(p_sql) + '_test'
            cr_uat.execute(v_sql_check)
            cr_uat.execute(v_sql_roll)
            db_uat.commit()
            cr_uat.close()
        except:
            v_env = 'UAT'
            result['code'] = '1'
            result['message'] = format_error(v_env, exception_info_mysql())
            return result

    if get_obj_type(p_sql)=='TRIGGER':
        try:
            v_sql_check = p_sql.replace(get_obj_name(p_sql), get_obj_name(p_sql) + '_test')
            v_sql_roll = 'drop trigger ' + get_obj_name(p_sql) + '_test'
            cr_uat.execute(v_sql_check)
            cr_uat.execute(v_sql_roll)
            db_uat.commit()
            cr_uat.close()
        except:
            v_env = 'UAT'
            result['code'] = '1'
            result['message'] = format_error(v_env, exception_info_mysql())
            return result

    return result

def check_obj_exists(p_dbid,p_sql):
    result = {}
    result['code'] = '0'
    result['message'] = ''
    p_ds    = get_ds_by_dsid(p_dbid)
    db_uat  = get_connection_ds_uat(p_ds)
    db_prod = get_connection_ds(p_ds)
    cr_uat  = db_uat.cursor()
    cr_prod = db_prod.cursor()
    v_sql_check = ''

    if get_obj_type(p_sql) == 'TABLE' and p_sql.upper().count("CREATE")>0:
           v_sql_check ='''select COUNT(0) from information_schema.tables
                           where upper(table_schema)='{0}' 
                             and upper(table_type)='BASE TABLE' 
                             and upper(table_name)='{1}'
                        '''.format(p_ds['uat_service'].upper(),get_obj_name(p_sql).upper())
           print(v_sql_check)
           cr_uat.execute(v_sql_check)
           rs_uat=cr_uat.fetchone()
           if rs_uat[0]>0:
               v_env = 'UAT'
               result['code'] = '1'
               result['message'] = format_check(v_env, '表已经存在！')
               return result
           else:
               v_sql_check = '''select COUNT(0) from information_schema.tables
                                          where upper(table_schema)='{0}' 
                                            and upper(table_type)='BASE TABLE' 
                                            and upper(table_name)='{1}'
                                       '''.format(p_ds['service'].upper(), get_obj_name(p_sql).upper())
               cr_prod.execute(v_sql_check)
               rs_prod = cr_prod.fetchone()
               if  rs_prod[0] >0:
                   v_env = 'PROD'
                   result['code'] = '1'
                   result['message'] = format_check(v_env,'表已经存在！')
                   return result


    if get_obj_type(p_sql) == 'VIEW' and p_sql.upper().count("CREATE")>0:
        v_sql_check = '''select COUNT(0) from information_schema.tables
                                  where upper(table_schema)='{0}' 
                                    and upper(table_type)='VIEW' 
                                    and upper(table_name)='{1}'
                               '''.format(p_ds['uat_service'].upper(), get_obj_name(p_sql).upper())
        print(v_sql_check)
        cr_uat.execute(v_sql_check)
        rs_uat = cr_uat.fetchone()
        if rs_uat[0] > 0:
            v_env = 'UAT'
            result['code'] = '1'
            result['message'] = format_check(v_env, '视图已经存在！')
            return result
        else:
            v_sql_check = '''select COUNT(0) from information_schema.tables
                                                 where upper(table_schema)='{0}' 
                                                   and upper(table_type)='VIEW' 
                                                   and upper(table_name)='{1}'
                                              '''.format(p_ds['service'].upper(), get_obj_name(p_sql).upper())
            cr_prod.execute(v_sql_check)
            rs_prod = cr_prod.fetchone()
            if rs_prod[0] > 0:
                v_env = 'PROD'
                result['code'] = '1'
                result['message'] = format_check(v_env, '视图已经存在！')
                return result

    if get_obj_type(p_sql) == 'INDEX' and p_sql.upper().count("CREATE")>0:
        v_sql_check = '''select COUNT(0) from information_schema.statistics
                                  where upper(table_schema)='{0}'                                   
                                    and upper(index_name)='{1}'
                               '''.format(p_ds['uat_service'].upper(), get_obj_name(p_sql).upper())
        print(v_sql_check)
        cr_uat.execute(v_sql_check)
        rs_uat = cr_uat.fetchone()
        if rs_uat[0] > 0:
            v_env = 'UAT'
            result['code'] = '1'
            result['message'] = format_check(v_env, '索引已经存在！')
            return result
        else:
            v_sql_check = '''select COUNT(0) from information_schema.statistics
                                                 where upper(table_schema)='{0}'                                                  
                                                   and upper(index_name)='{1}'
                                              '''.format(p_ds['service'].upper(), get_obj_name(p_sql).upper())
            cr_prod.execute(v_sql_check)
            rs_prod = cr_prod.fetchone()
            if rs_prod[0] > 0:
                v_env = 'PROD'
                result['code'] = '1'
                result['message'] = format_check(v_env, '索引已经存在！')
                return result

    if get_obj_type(p_sql) == 'FUNCTION' and p_sql.upper().count("CREATE")>0:
        v_sql_check = '''select COUNT(0) from information_schema.routines
                                  where upper(routine_schema)='{0}' 
                                    and upper(routine_type)='FUNCTION' 
                                    and upper(routine_name)='{1}'
                               '''.format(p_ds['uat_service'].upper(), get_obj_name(p_sql).upper())
        print(v_sql_check)
        cr_uat.execute(v_sql_check)
        rs_uat = cr_uat.fetchone()
        if rs_uat[0] > 0:
            v_env = 'UAT'
            result['code'] = '1'
            result['message'] = format_check(v_env, '函数已经存在！')
            return result
        else:
            v_sql_check = '''select COUNT(0) from information_schema.routines
                                                 where upper(routine_schema)='{0}' 
                                                   and upper(routine_type)='FUNCTION' 
                                                   and upper(routine_name)='{1}'
                                              '''.format(p_ds['service'].upper(), get_obj_name(p_sql).upper())
            cr_prod.execute(v_sql_check)
            rs_prod = cr_prod.fetchone()
            if rs_prod[0] > 0:
                v_env = 'PROD'
                result['code'] = '1'
                result['message'] = format_check(v_env, '函数已经存在！')
                return result

    if get_obj_type(p_sql) == 'PROCEDURE' and p_sql.upper().count("CREATE")>0:
        v_sql_check = '''select COUNT(0) from information_schema.routines
                                          where upper(routine_schema)='{0}' 
                                            and upper(routine_type)='PROCEDURE' 
                                            and upper(routine_name)='{1}'
                                       '''.format(p_ds['uat_service'].upper(), get_obj_name(p_sql).upper())
        print(v_sql_check)
        cr_uat.execute(v_sql_check)
        rs_uat = cr_uat.fetchone()
        if rs_uat[0] > 0:
            v_env = 'UAT'
            result['code'] = '1'
            result['message'] = format_check(v_env, '过程已经存在！')
            return result
        else:
            v_sql_check = '''select COUNT(0) from information_schema.routines
                                                         where upper(routine_schema)='{0}' 
                                                           and upper(routine_type)='PROCEDURE' 
                                                           and upper(routine_name)='{1}'
                                                      '''.format(p_ds['service'].upper(), get_obj_name(p_sql).upper())
            cr_prod.execute(v_sql_check)
            rs_prod = cr_prod.fetchone()
            if rs_prod[0] > 0:
                v_env = 'PROD'
                result['code'] = '1'
                result['message'] = format_check(v_env, '过程已经存在！')
                return result

    if get_obj_type(p_sql) == 'TRIGGER' and p_sql.upper().count("CREATE")>0:
        v_sql_check = '''select COUNT(0) from information_schema.triggers
                                                  where upper(trigger_schema)='{0}'                                                    
                                                    and upper(trigger_name)='{1}'
                                               '''.format(p_ds['uat_service'].upper(), get_obj_name(p_sql).upper())
        print(v_sql_check)
        cr_uat.execute(v_sql_check)
        rs_uat = cr_uat.fetchone()
        if rs_uat[0] > 0:
            v_env = 'UAT'
            result['code'] = '1'
            result['message'] = format_check(v_env, '触发器已经存在！')
            return result
        else:
            v_sql_check = '''select COUNT(0) from information_schema.triggers
                                                                 where upper(trigger_schema)='{0}'                                                                
                                                                   and upper(trigger_schema)='{1}'
                                                              '''.format(p_ds['service'].upper(),get_obj_name(p_sql).upper())
            cr_prod.execute(v_sql_check)
            rs_prod = cr_prod.fetchone()
            if rs_prod[0] > 0:
                v_env = 'PROD'
                result['code'] = '1'
                result['message'] = format_check(v_env, '触发器已经存在！')
                return result
    cr_uat.close()
    cr_prod.close()
    return result

def check_column_null(p_dbid,p_sql):
    result = {}
    result['code'] = '0'
    result['message'] = ''
    p_ds   = get_ds_by_dsid(p_dbid)
    db_uat = get_connection_ds_uat(p_ds)
    cr_uat = db_uat.cursor()
    v_sql_check = ''
    if get_obj_type(p_sql) == 'TABLE' and p_sql.upper().count("CREATE")>0:
        v_sql_check = '''select count(0) from information_schema.`columns`   
                         where upper(table_schema)='{0}'   
                           and upper(table_name)='{1}'
                           and is_nullable='YES'
                      '''.format(p_ds['uat_service'].upper(), get_obj_name(p_sql).upper())
        print(v_sql_check)
        cr_uat.execute(p_sql)
        cr_uat.execute(v_sql_check)
        rs_uat = cr_uat.fetchone()
        if rs_uat[0] > 0:
            cr_uat.execute('drop table ' + get_obj_name(p_sql))
            cr_uat.close()
            db_uat.commit()
            v_env = 'UAT'
            result['code'] = '1'
            result['message'] = format_check(v_env, '表中列不能为空！')
            return result
        else:
           cr_uat.execute('drop table ' + get_obj_name(p_sql))
           cr_uat.close()
           db_uat.commit()
    return result

def check_column_len(p_dbid,p_sql):
    result = {}
    result['code'] = '0'
    result['message'] = ''
    p_ds = get_ds_by_dsid(p_dbid)
    db_uat = get_connection_ds_uat(p_ds)
    cr_uat = db_uat.cursor()
    v_sql_check = ''
    if get_obj_type(p_sql) == 'TABLE' and p_sql.upper().count("CREATE") > 0:
        v_sql_check = '''select IFNULL(SUM(character_maximum_length),0) 
                          from  information_schema.columns   
                         where upper(table_schema)='{0}'   
                             and upper(table_name)='{1}'
                             and data_type='VARCHAR'
                        '''.format(p_ds['uat_service'].upper(), get_obj_name(p_sql).upper())
        print(v_sql_check)
        cr_uat.execute(p_sql)
        cr_uat.execute(v_sql_check)
        rs_uat = cr_uat.fetchone()
        if rs_uat[0] > 8000:
            cr_uat.execute('drop table ' + get_obj_name(p_sql))
            cr_uat.close()
            db_uat.commit()
            v_env = 'UAT'
            result['code'] = '1'
            result['message'] = format_check(v_env, '表中字符列不能超过8000个字符！')
            return result
        else:
            cr_uat.execute('drop table ' + get_obj_name(p_sql))
            cr_uat.close()
            db_uat.commit()
    return result

def check_virtual_column(p_dbid,p_sql):
    result = {}
    result['code'] = '0'
    result['message'] = ''
    p_ds = get_ds_by_dsid(p_dbid)
    db_uat = get_connection_ds_uat(p_ds)
    cr_uat = db_uat.cursor()
    v_sql_check = ''
    if get_obj_type(p_sql) == 'TABLE' and p_sql.upper().count("CREATE") > 0:
        v_sql_check = '''select count(0) from information_schema.columns   
                           where upper(table_schema)='{0}'
                             and upper(table_name)='{1}'
                             and extra='VIRTUAL GENERATED'
                        '''.format(p_ds['uat_service'].upper(), get_obj_name(p_sql).upper())
        print(v_sql_check)
        cr_uat.execute(p_sql)
        cr_uat.execute(v_sql_check)
        rs_uat = cr_uat.fetchone()
        if rs_uat[0] > 0:
            cr_uat.execute('drop table ' + get_obj_name(p_sql))
            cr_uat.close()
            db_uat.commit()
            v_env = 'UAT'
            result['code'] = '1'
            result['message'] = format_check(v_env, '表中不能含有虚拟列！')
            return result
        else:
            cr_uat.execute('drop table ' + get_obj_name(p_sql))
            cr_uat.close()
            db_uat.commit()
    return result

def check_table_valid(p_sql):
    result = {}
    result['code'] = '0'
    result['message'] = ''
    if get_obj_type(p_sql) == 'TABLE':

        if  len(re.findall(r'^TMP',get_obj_name(p_sql).upper(),re.M))>0  :
            result['code'] = '1'
            result['message'] ='表名前缀不能为TMP！'
            return result

        if  len(re.findall(r'TMP$',get_obj_name(p_sql).upper(),re.M))>0  :
            result['code'] = '1'
            result['message'] = '表名后缀不能为TMP！'
            return result

        if len(re.findall(r'^TEMP', get_obj_name(p_sql).upper(), re.M)) > 0:
            result['code'] = '1'
            result['message'] = '表名前缀不能为TEMP！'
            return result

        if len(re.findall(r'TEMP$', get_obj_name(p_sql).upper(), re.M)) > 0:
            result['code'] = '1'
            result['message'] = '表名后缀不能为TEMP！'
            return result

        if  len(re.findall(r'^BAK',get_obj_name(p_sql).upper(),re.M))>0  :
            result['code'] = '1'
            result['message'] ='表名前缀不能为BAK！'
            return result

        if  len(re.findall(r'BAK$',get_obj_name(p_sql).upper(),re.M))>0  :
            result['code'] = '1'
            result['message'] = '表名后缀不能为BAK！'
            return result

        if len(re.findall(r'^BACKUP', get_obj_name(p_sql).upper(), re.M)) > 0:
            result['code'] = '1'
            result['message'] = '表名前缀不能为BACKUP！'
            return result

        if len(re.findall(r'BACKUP', get_obj_name(p_sql).upper(), re.M)) > 0:
            result['code'] = '1'
            result['message'] = '表名后缀不能为BACKUP！'
            return result

        if len(re.findall(r'^SYS', get_obj_name(p_sql).upper(), re.M)) > 0:
            result['code'] = '1'
            result['message'] = '表名前缀不能为SYS！'

        if get_obj_type(p_sql) == 'TABLE' and len(re.findall(r'\d{2,9}$', get_obj_name(p_sql).upper(), re.M)) > 0:
            result['code'] = '1'
            result['message'] = '禁止表名以连续2位及以上数字作为后缀名！'
            return result

    return result

def check_proc_valid_ddl(p_sql):
    result = {}
    result['code'] = '0'
    result['message'] = ''

    #规则一：允许有TRUNCATE语句
    if p_sql.upper().count('TRUNCATE') > 0 and p_sql.upper().count('TABLE') > 0  \
            and p_sql.upper().find("CREATE")>p_sql.upper().find("TRUNCATE") :
        return result

    #规则二：允许有CREATE INDEX，DROP INDEX语句,允许创建临时表
    if p_sql.upper().count('CREATE') > 0 and p_sql.upper().count('INDEX') > 0  \
            and p_sql.upper().find("INDEX")>p_sql.upper().find("CREATE") :
        return result

    if p_sql.upper().count('DROP') > 0 and p_sql.upper().count('INDEX') > 0  \
            and p_sql.upper().find("INDEX")>p_sql.upper().find("DROP") :
        return result

    if p_sql.upper().count('CREATE') > 0 and p_sql.upper().count('TABLE') > 0 and p_sql.upper().count('TEMPORARY')>0 \
            and p_sql.upper().find("TEMPORARY") > p_sql.upper().find("CREATE") \
            and p_sql.upper().find("TABLE") > p_sql.upper().find("TEMPORARY"):
        return result

    #规则三：不允许在过程中创建普通表，修改表结构
    if p_sql.upper().count('CREATE') > 0 and p_sql.upper().count('TABLE') > 0 and p_sql.upper().count('TEMPORARY')== 0  \
            and p_sql.upper().find("TABLE") > p_sql.upper().find("CREATE") :
        v_env = 'UAT'
        result['code'] = '1'
        result['message'] = format_check(v_env, '存储过程中不允许创建普通表！')
        return result

    if p_sql.upper().count('ALTER') > 0 and p_sql.upper().count('TABLE') > 0  \
            and p_sql.upper().find("TABLE")>p_sql.upper().find("ALTER") :
        v_env = 'UAT'
        result['code'] = '1'
        result['message'] = format_check(v_env, '存储过程中不允许修改表结构！')
        return result
    return result

def check_proc_valid(p_dbid,p_sql):
    result = {}
    result['code'] = '0'
    result['message'] = ''
    p_ds   = get_ds_by_dsid(p_dbid)
    db_uat = get_connection_ds_uat(p_ds)
    cr_uat = db_uat.cursor()
    if get_obj_type(p_sql) == 'PROCEDURE' and p_sql.upper().count("CREATE") > 0:

       #创建存储过程在UAT环境中
       cr_uat.execute(p_sql)

       #从数据字典中读取过程定义，并将过程中的语句拆分出来，保存至list中
       v_sql_proc = '''select routine_definition from information_schema.`routines`   
                                where upper(routine_schema)='{0}'   
                                  and upper(routine_name)='{1}'                                 
                             '''.format(p_ds['uat_service'].upper(), get_obj_name(p_sql).upper())
       v_sql_drop = 'drop procedure {0}'.format(get_obj_name(p_sql))

       cr_uat.execute(v_sql_proc)
       rs_uat = cr_uat.fetchone()
       v_list = rs_uat[0].upper().replace('\n','').replace('BEGIN','').replace('END','').split(';')

       #逐个验证每一个语句是否满足规则
       for i in range(len(v_list)):
           print(i,v_list[i])
           result=check_proc_valid_ddl(v_list[i])
           if result['code']!='0':
               cr_uat.execute(v_sql_drop)
               db_uat.commit()
               cr_uat.close()
               return result

       cr_uat.execute(v_sql_drop)
       db_uat.commit()
       cr_uat.close()

    return result

def check_sql_mysql(p_dbid,p_sql):
    '''
    一、DDL验证
        1、不允许发布DML操作（人工审核）
        2、一次是只允许发布的一个DDL语句
        3、禁止使用触发器，触发器逻辑在逻辑层处理.如使用，
        4、DBA允许创建触发器，但是触发器名需要满足命名规则（TR_表名_操作类型）
        5、DDL对象名长度不超过30个字符。
        6、视图创建语句是否合法
        7、对象名不能以数字开头。
        8、对象名只允许包含字母、数字下划线，不允许使用其他符号。
        9、对象命名全部大写，并以“_”分隔中间词组或缩写。
        10、对象名格式需要满足（表：对象类型前缀_实际对象名字、视图：V_业务模块名、  函数：F_业务模块或功能名、过程:PROC_业务模块名）
        11、索引命名规范：唯一索引：UIX_开头，复合索引：CIX_开头，非唯一索引：IX_开头
        12、表结构语句不允许有drop操作（drop table ,alter table .drop column...)
        13、每张表必须有主键。
        14、验证对象是否已存在（分别验证表、视图、函数、过程）
        15、验证DDL对象[表、视图、函数、过程、触发器]语法
        16、列不允许Null值，列应设置默认值
        17、表的单行全部定长列大小总长度不得超过8000字节设置。
        18、不允许使用虚拟列
        19、禁止以bak、sql2doc、temp、tmp等后缀或前缀命名数据库中任何正式业务对象，如数据库名称、表名、视图、存储过程名称等
        20、禁止以连续2位或2位以上数字作为表名后缀名
        21、禁止以sys前缀作为表名。
        22、禁止在存储过程中包含DDL语法（truncate及特殊维护结构的过程除外），如建表、备份表、修改字段等操作。
        23、禁止在存储过程中包含DDL语法。允许：TRUNCATE,CREATE INDEX, DROP INDEX除外， 禁止：建表、备份表、修改字段。
        24、对象名两边的``符号不需要替换为空
    '''
    result={}
    result['code'] = '0'
    result['message'] = ''

    #1.不允许发布DML操作
    '''
    if p_sql.split(" ")[0].upper() in ("INSERT","UPDATE","DELETE"):
       result['code'] ='1'
       result['message']='不允许发布DML操作!'
       return result
    '''

    #2.一次是只允许发布的一个DDL语句
    if (p_sql.upper().count("CREATE") > 1  or p_sql.upper().count("ALTER") > 1 \
            or p_sql.upper().count("DROP") > 1) and get_obj_type(p_sql)=='TABLE':
        result['code'] = '1'
        result['message'] = '一次是只允许发布的一个DDL语句!'
        return result

    # 3-4、普通用户禁止使用触发器，DBA允许创建触发器
    if not is_dba(devconfig.logon_user):
        if p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("TRIGGER") > 0 \
                and p_sql.upper().find("TRIGGER") > p_sql.upper().find("CREATE"):
            result['code'] = '1'
            result['message'] = '普通用户禁止使用触发器!'
            return result

    #5.对象名长度不超过30个字符
    if check_object_length(p_sql)['code']=='1':
        return check_object_length(p_sql)

    #6.对象名不能以数字开头
    if get_obj_name(p_sql)=='':
        result['code'] = '1'
        result['message'] = '不能识别的DDL语句!'
        return result
    elif get_obj_name(p_sql)[0] in "0123456789":
        result['code'] = '1'
        result['message'] = '对象名不能以数字开头!'
        return result

    #7.对象名只允许包含字母、数字下划线，不允许使用其他符号
    if re.search('\W',get_obj_name(p_sql)) is not None:
       result['code'] = '1'
       result['message'] = '对象名只允许包含字母、数字下划线，不允许使用其他符号!'
       return result

    #8.对象命名必须全部大写
    if re.search('[a-z]', get_obj_name(p_sql)) is not None:
        result['code'] = '1'
        result['message'] = '对象名必须全部为大写字母!'
        return result

    #9.对象名需以“_”分隔中间词组或缩写。
    if '_' not in get_obj_name(p_sql):
        result['code'] = '1'
        result['message'] = '对象名需以“_”分隔中间词组或缩写!'
        return result

    #10-11.检测对象名格式是否满足规范.
    result=check_obj_prefix(p_sql)
    if result['code']!='0':
       return result

    #12.表结构语句不允许有drop操作：drop table ,alter table drop column
    result=check_tab_drop(p_sql)
    if result['code']!='0':
       return result

    #13、每张表必须有主键
    if get_obj_type(p_sql)=='TABLE' \
            and  not (p_sql.upper().count('PRIMARY') > 0 and  p_sql.upper().count('KEY') > 0):
        result['code'] = '1'
        result['message'] = '表必须有主键!'
        return result

    #14、验证对象是否已存在[验证表、视图、函数、过程、触发器]
    result = check_obj_exists(p_dbid, p_sql)
    if result['code'] != '0':
        return result

    #15、禁止在存储过程中包含DDL语法。
    result = check_proc_valid(p_dbid, p_sql)
    if result['code'] != '0':
        return result

    #16、表中列不允许NULL值，列应设置默认值
    result =check_column_null(p_dbid,p_sql)
    if result['code'] != '0':
        return result

    #17、表的单行全部定长列大小总长度不得超过8000字节设置
    result = check_column_len(p_dbid, p_sql)
    if result['code'] != '0':
        return result

    #18、不允许使用虚拟列
    result =check_virtual_column(p_dbid,p_sql)
    if result['code'] != '0':
        return result

    #19、禁止以BAK、BACKUP、TEMP、TMP后缀或前缀命名对象,禁止以SYS前缀作为表名、禁止以连续2位或2位以上数字作为表名后缀名
    result =check_table_valid(p_sql)
    if result['code']!='0':
        return result

    # 20、验证DDL对象[表、视图、函数、过程、触发器]语法
    result = check_ddl_syntax(p_dbid, p_sql)
    if result['code'] != '0':
        return result

    return result