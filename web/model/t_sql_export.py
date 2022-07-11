#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/7/5 9:44
# @Author : ma.fei
# @File : t_sql_export.py
# @Software: PyCharm

import xlwt
import json
import traceback
import os,zipfile
import datetime
import openpyxl
from web.utils.common  import format_sql as fmt_sql,get_seconds
from web.model.t_ds    import get_ds_by_dsid
from web.utils.common  import send_mail_param,get_sys_settings,current_time, send_message,current_rq
from web.model.t_user   import get_user_by_loginame
from web.model.t_dmmx    import get_dmmc_from_dm
from web.utils.mysql_async import async_processer
from web.model.t_sql_release import get_html_contents,get_html_contents_release_wx
from web.model.t_sql  import exe_query_exp

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
                    a.dbid, 
                    a.db, 
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

async def get_sql_export(p_id):
    sql="select * from t_sql_export where id={}".format(p_id)
    return await async_processer.query_dict_one(sql)

async def upd_exp_sql(p_sqlid,p_user,p_status,p_message,p_host):
    result={}
    try:
        sql="""update t_sql_export 
                  set  status ='{}' ,
                       last_update_date =now(),
                       updator='{}',
                       audit_date =now() ,
                       auditor='{}',
                       audit_message='{}'
                where id='{}'""".format(p_status,p_user['login_name'],p_user['login_name'],p_message,p_sqlid)
        print(sql)
        await async_processer.exec_sql(sql)

        wkno = await get_sql_export(p_sqlid)
        p_ds = await get_ds_by_dsid(wkno['dbid'])
        p_ds['service'] = wkno['db']
        email     = p_user['email']
        settings  = await get_sys_settings()
        v_title   = '工单导出审核情况[{}]'.format(wkno['id'])
        nowTime   = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        creator   = (await get_user_by_loginame(wkno['creator']))['name']
        cmail     =  (await get_user_by_loginame(wkno['creator']))['email']
        auditor   = (await get_user_by_loginame(wkno['auditor']))['name']
        status    = (await get_dmmc_from_dm('41', wkno['status']))[0]

        if p_host=="124.127.103.190":
           p_host = "124.127.103.190:65482"
        elif p_host in('10.2.39.18','10.2.39.20','10.2.39.21'):
           p_host = '{}:81'.format(p_host)
        else:
           p_host = p_host

        # send audit mail
        v_content = get_html_contents()
        v_content = v_content.replace('$$TIME$$', nowTime)
        v_content = v_content.replace('$$DBINFO$$',p_ds['url'] + p_ds['service']
                                                   if p_ds['url'].find(p_ds['service']) < 0 else p_ds['url'])
        v_content = v_content.replace('$$CREATOR$$', creator)
        v_content = v_content.replace('$$AUDITOR$$', auditor)
        v_content = v_content.replace('$$TYPE$$', 'SQL导出')
        v_content = v_content.replace('$$STATUS$$', status)
        v_content = v_content.replace('$$DETAIL$$', 'http://{}/sql/detail?release_id={}'.format(p_host,p_sqlid))
        v_content = v_content.replace('$$ERROR$$', '')
        send_mail_param(settings.get('send_server'), settings.get('sender'), settings.get('sendpass'), email,
                        cmail, v_title, v_content)

        # send to wx 2022.03.07
        v_content_wx = get_html_contents_release_wx()
        v_content_wx = v_content_wx.replace('$$TIME$$', nowTime)
        v_content_wx = v_content_wx.replace('$$DBINFO$$',
                                            p_ds['url'] + p_ds['service'] if p_ds['url'].find(p_ds['service']) < 0 else
                                            p_ds['url'])
        v_content_wx = v_content_wx.replace('$$CREATOR$$', auditor)
        v_content_wx = v_content_wx.replace('$$TYPE$$', 'SQL导出')
        v_content_wx = v_content_wx.replace('$$STATUS$$', status)
        v_content_wx = v_content_wx.replace('$$ERROR$$', '')
        v_detail_url = 'http://{}/sql/detail?release_id={}'.format(p_host, p_sqlid)
        await send_message('{}|{}'.format(p_user['wkno'],
                                          (await get_user_by_loginame(wkno['creator']))['wkno']),
                           v_title,
                           v_content_wx,
                           v_detail_url)

        result['code']='0'
        result['message']='审核成功!'
        return result
    except :
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '审核异常!'
        return result

async def query_exp_audit(p_name,p_dsid,p_creator,p_userid,p_username):
    print('p_creator=',p_creator,'p_userid',p_username)
    v_where = ''
    if p_name != '':
       v_where = v_where + " and a.sqltext like '%{0}%'\n".format(p_name)

    if p_dsid != '':
        v_where = v_where + " and a.dbid='{0}'\n".format(p_dsid)
    else:
        v_where = v_where + """ and exists(select 1 from t_user_proj_privs x 
                                           where x.proj_id=b.id and x.user_id='{0}' and priv_id='3')""".format(p_userid)
    if p_creator != '':
        v_where = v_where + " and a.creator='{0}'\n".format(p_creator)

    if p_username != 'admin':
        v_where = v_where + " and a.creator='{0}'\n".format(p_username)

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
              {0}
            order by a.creation_date desc
          """.format(v_where)
    print(sql)
    return await async_processer.query_list(sql)

async def update_export(p_id,p_status,p_process,p_file='',p_real_file='',p_size='',p_error=''):
    st = "update t_sql_export_task a " \
            " set a.status='{}',a.process='{}',a.file='{}',a.real_file='{}',a.size='{}',a.error='{}' where id={}"\
        .format(p_status,p_process,p_file,p_real_file,p_size,p_error,p_id)
    await async_processer.exec_sql(st)

async def export_insert(p_userid):
    st = """insert into t_sql_export_task(status,process,creator,create_date)
                values('1','0%','{}',now())""".format(p_userid)
    id = await async_processer.exec_ins_sql(st)
    return id

async def exp_data_xlsx(static_path,p_bbid,p_data,p_id):
    try:
        row_data  = 1
        wb = openpyxl.Workbook()
        ws = wb.create_sheet(index=0,title=p_bbid)
        file_path = static_path + '/downloads/sql'
        os.system('cd {0}'.format(file_path))
        file_name   = static_path + '/downloads/sql/exp_bbtj_{}_{}.xlsx'.format(p_bbid,current_rq())
        file_name_s = 'exp_sql_{}_{}.xls'.format(p_bbid,current_rq())
        # write header
        for k in range(len(p_data['column'])):
            ws.cell(column = k+1,row=row_data,value = p_data['column'][k]['title'])
        await update_export(p_id, '3', '25%')

        # write body
        n_batch_size = 500
        n_total_rows = len(p_data['data'])
        row_data = row_data + 1
        for i in p_data['data']:
            for j in range(len(i)):
                if i[j] is None:
                   ws.cell(row=row_data, column=j+1,value='')
                else:
                   ws.cell(row=row_data, column=j+1,value = str(i[j]))
            row_data = row_data + 1
            if row_data % n_batch_size == 0:
               await update_export(p_id, '3', str(round(row_data/75,2)*100)+'%')

        await update_export(p_id, '3', '98%')

        wb.save(file_name)
        print("{0} export complete!".format(file_name))
        zip_file = static_path + '/downloads/sql/exp_sql_{}_{}.zip'.format(p_bbid,current_rq())
        rzip_file = '/static/downloads/sql/exp_sql_{}_{}.zip'.format(p_bbid,current_rq())

        if os.path.exists(zip_file):
            os.system('rm -f {0}'.format(zip_file))

        z = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED, allowZip64=True)
        z.write(file_name, arcname=file_name_s)
        z.close()

        file_size = os.path.getsize(file_name)
        os.system('rm -f {0}'.format(file_name))

        #update path,file,size
        await update_export(p_id, '3', '100%',rzip_file,zip_file,file_size)
        return rzip_file
    except:
        await update_export(p_id, '34', '0%', '' ,'','',traceback.print_exc())

async def query_bbgl_data(p_bbid):
    try:
        cfg    = await query_export(p_bbid)
        result = await exe_query_exp(cfg['dbid'], cfg['sqltext'], cfg['db'])
        result = {"data": result['data'], "column": result['column'], "status": result['status'], "msg": result['msg'] }
        return result
    except:
        result = {"data": '', "column": '', "status": '1', "msg": traceback.print_exc()}
        return result

async def export_bbgl_data(p_exp_id,userid,path):
    try:
        id  = await export_insert(p_exp_id,userid)
        res = await query_bbgl_data(p_exp_id)
        if res['status'] == '1':
           return {"code": -1, "message":res['msg']}
        await update_export(id,'2','20%')
        zip_file = await exp_data_xlsx(path,p_exp_id,res,id)
        return {"code": 0, "message": zip_file}
    except:
        return {"code": -1, "message": traceback.print_exc()}

async def get_download(p_id):
      st = "select *from t_sql_export_task where id={}".format(p_id)
      return  await async_processer.query_dict_one(st)

async def del_export(p_id):
    try:
        res = await get_download(p_id)
        os.system('rm -f {0}'.format(res.get('real_file')))
        st = "delete from t_sql_export_task where id={}".format(p_id)
        await async_processer.exec_sql(st)
        return {'code': 0, 'message': '删除成功!'}
    except Exception as e:
        traceback.print_exc()
        return {'code': -1, 'message': '删除失败!'}