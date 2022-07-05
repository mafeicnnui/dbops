#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/7/5 9:44
# @Author : ma.fei
# @File : t_sql_export.py
# @Software: PyCharm

import xlwt
import traceback
import os,zipfile
from web.utils.common import current_rq
from web.utils.mysql_async import async_processer
from web.utils.common import current_time
from web.utils.common  import format_sql as fmt_sql

def set_header_styles(p_fontsize,p_color):
    header_borders = xlwt.Borders()
    header_styles  = xlwt.XFStyle()
    # add table header style
    header_borders.left   = xlwt.Borders.THIN
    header_borders.right  = xlwt.Borders.THIN
    header_borders.top    = xlwt.Borders.THIN
    header_borders.bottom = xlwt.Borders.THIN
    header_styles.borders = header_borders
    header_pattern = xlwt.Pattern()
    header_pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    header_pattern.pattern_fore_colour = p_color
    # add font
    font = xlwt.Font()
    font.name = u'微软雅黑'
    font.bold = True
    font.size = p_fontsize
    header_styles.font = font
    #add alignment
    header_alignment = xlwt.Alignment()
    header_alignment.horz = xlwt.Alignment.HORZ_CENTER
    header_alignment.vert = xlwt.Alignment.VERT_CENTER
    header_styles.alignment = header_alignment
    header_styles.borders = header_borders
    header_styles.pattern = header_pattern
    return header_styles

async def save_exp_sql(p_dbid,p_cdb,p_sql,p_flag,p_user):
    result = {}
    try:
        sql="""insert into t_sql_export(dbid,db,sqltext,status,creation_date,creator,last_update_date,updator) 
                 values('{0}','{1}',"{2}",'{3}','{4}','{5}','{6}','{7}')
            """.format(p_dbid,p_cdb,fmt_sql(p_sql),p_flag,
                       current_time(),p_user['login_name'],
                       current_time(),p_user['login_name'])

        await async_processer.exec_sql(sql)
        result['code']='0'
        result['message']='发布成功！'
        return result
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '发布失败!'
        return result

async def update_exp_sql(p_dbid,p_cdb,p_sql,p_flag,p_user,p_id):
    result = {}
    try:
        st="""update t_sql_export
               set dbid={},
                   db='{}',
                   sqltext='{}',
                   status='{}',
                   updator='{}',
                   last_update_date=now() 
                where id={}
           """.format(p_dbid,p_cdb,fmt_sql(p_sql),p_flag,p_user['login_name'],p_id)
        await async_processer.exec_sql(st)
        result['code']='0'
        result['message']='更新成功！'
        return result
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '更新失败!'
        return result

async def export_query(p_dbid,p_creator,p_key,p_username):
    v_where=''
    if p_creator != '':
        v_where = v_where + " and a.creator='{}'\n".format(p_creator)

    if p_dbid != '':
        v_where = v_where + " and a.dbid='{}'\n".format(p_dbid)

    if p_username != 'admin':
        v_where = v_where + "  and  a.creator='{0}'".format(p_username)

    if p_key != '':
        v_where = v_where + " and a.sqltext like '%{}%'\n".format(p_key)

    sql = """SELECT  a.id, 
                     b.db_desc,
                     a.db,
                     (SELECT NAME FROM t_user e WHERE e.login_name=a.creator) creator,
                     DATE_FORMAT(a.creation_date,'%Y-%m-%d %h:%i:%s')  creation_date,
                     (SELECT NAME FROM t_user e WHERE e.login_name=a.auditor) auditor,
                     DATE_FORMAT(a.audit_date,'%y-%m-%d %h:%i:%s')   audit_date,
                     c.dmmc as status      
                FROM t_sql_export a,t_db_source b,t_dmmx c
                WHERE a.dbid=b.id
                AND c.dm='41'
                AND a.status=c.dmm
                {} ORDER BY a.creation_date desc""".format(v_where)
    print(sql)
    return await async_processer.query_list(sql)

async def exp_data(static_path,p_ds,p_sql):
    row_data  = 0
    workbook  = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet('kpi')
    header_styles = set_header_styles(45,1)
    os.system('cd {0}'.format(static_path + '/downloads/sql'))
    file_name   = static_path + '/downloads/sql/exp_sql_{0}.xls'.format(current_rq())
    file_name_s = 'exp_sql_{0}.xls'.format(current_rq())
    sql_header = """select * from ({}) x limit 1""".format(p_sql)

    # 写表头
    desc = await async_processer.query_one_desc_by_ds(p_ds,sql_header)
    for k in range(len(desc)):
        worksheet.write(row_data, k, desc[k][0], header_styles)
        if k in (3, 5):
            worksheet.col(k).width = 8000
        else:
            worksheet.col(k).width = 4000

    #循环项目写单元格
    row_data = row_data + 1
    rs3 = await async_processer.query_list_by_ds(p_ds,p_sql)
    for i in rs3:
        for j in range(len(i)):
            if i[j] is None:
                worksheet.write(row_data, j, '')
            else:
                worksheet.write(row_data, j, str(i[j]))
        row_data = row_data + 1

    workbook.save(file_name)
    print("{0} export complete!".format(file_name))

    #生成zip压缩文件
    zip_file = static_path + '/downloads/port/exp_kpi_{0}.zip'.format(current_rq())
    rzip_file = '/static/downloads/port/exp_kpi_{0}.zip'.format(current_rq())

    #若文件存在则删除
    if os.path.exists(zip_file):
        os.system('rm -f {0}'.format(zip_file))

    z = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED, allowZip64=True)
    z.write(file_name, arcname=file_name_s)
    z.close()

    # 删除json文件
    os.system('rm -f {0}'.format(file_name))
    return rzip_file

async def query_export(p_id):
    st = """select  a.id,
                    a.dbid, a.db, 
                    a.sqltext, 
                    a.status
           from t_sql_export a where a.id={}""".format(p_id)
    return await async_processer.query_dict_one(st)

async def delete_export(p_id):
    try:
        st = "delete from t_sql_export where id={}".format(p_id)
        await async_processer.exec_sql(st)
        return {'code': '0', 'message': '删除成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '删除失败!'}