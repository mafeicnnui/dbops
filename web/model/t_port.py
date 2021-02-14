#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : ma.fei
# @File    : t_user.py
# @Software: PyCharm

import re
import traceback
import xlrd,xlwt
import os,zipfile

from web.utils.common import current_rq
from web.utils.mysql_async import async_processer

async def query_port(p_market_id):
    v_where =''
    if p_market_id != '':
        v_where = "  and a.market_id='{}'".format(p_market_id)
    sql = """SELECT a.id, 
                   b.dmmc,
                   app_desc,
                   local_ip,
                   local_port,
                   mapping_port,
                   mapping_domain,
                   c.name,
                   date_format(create_date,'%Y-%m-%d')  create_date
            FROM   t_port a,t_dmmx b,t_user c 
            WHERE a.market_id=b.dmm
             AND a.creater=c.login_name
             AND b.dm='05' {} order by a.market_id""".format(v_where)
    return  await async_processer.query_list(sql)

async def save_port(p_port):
    val = check_port(p_port)
    if val['code']=='-1':
        return val
    try:
        result            = {}
        market_id         = p_port['market_id']
        market_name       = p_port['market_name']
        app_desc          = p_port['app_desc']
        local_ip          = p_port['local_ip']
        local_port        = p_port['local_port']
        mapping_port      = p_port['mapping_port']
        mapping_domain    = p_port['mapping_domain']
        mapping_type      = p_port['mapping_type']
        creater           = p_port['creater']
        sql="""insert into t_port(market_id,market_name,app_desc,local_ip,local_port,mapping_port,mapping_domain,mapping_type,creater,create_date) 
                 values('{}','{}','{}','{}','{}','{}','{}','{}','{}',now())
            """.format(market_id,market_name,app_desc,local_ip,local_port,mapping_port,mapping_domain,mapping_type,creater)
        await async_processer.exec_sql(sql)
        result['code']='0'
        result['message']='保存成功！'
        return result
    except:
        result = {}
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '保存失败！'
        return result

async def upd_port(p_port):
    result={}
    val = check_port(p_port)
    if  val['code'] == '-1':
        return val
    try:
        port_id         = p_port['port_id']
        market_id       = p_port['market_id']
        market_name     = p_port['market_name']
        app_desc        = p_port['app_desc']
        local_ip        = p_port['local_ip']
        local_port      = p_port['local_port']
        mapping_port    = p_port['mapping_port']
        mapping_domain  = p_port['mapping_domain']
        mapping_type    = p_port['mapping_type']
        sql="""update t_port
                  set  
                      market_id       ='{}',
                      market_name     ='{}',
                      app_desc        ='{}', 
                      local_ip        ='{}', 
                      local_port      ='{}', 
                      mapping_port    ='{}',
                      mapping_domain  ='{}', 
                      mapping_type    ='{}', 
                      update_date     = now()            
                where id={}""".\
            format(market_id,market_name,app_desc,local_ip,local_port,mapping_port,mapping_domain,mapping_type,port_id)
        await async_processer.exec_sql(sql)
        result={}
        result['code']='0'
        result['message']='更新成功!'
        return result
    except :
        print(traceback.format_exc())
        result['code'] = '-1'
        result['message'] = '更新失败!'
        return result

async def del_port(p_portid):
    try:
        sql="delete from t_port  where id='{0}'".format(p_portid)
        await async_processer.exec_sql(sql)
        result={}
        result['code']='0'
        result['message']='删除成功!'
        return result
    except :
        result = {}
        result['code'] = '-1'
        result['message'] = '删除失败!'
        return result

async def check_port_rep(p_port):
    sql = "select count(0) from t_port  where  instr(app_port,'{0}')>0".format(p_port['app_port'])
    return (await async_processer.query_one(sql))[0]

def check_port(p_port):
    result = {}
    if p_port["market_id"]=="":
        result['code']='-1'
        result['message']='项目名不能为空!'
        return result

    if p_port["app_desc"] == "":
        result['code'] = '-1'
        result['message'] = '项目描述不能为空!'
        return result

    if p_port["local_ip"]=="":
        result['code']='-1'
        result['message']='本地IP不能为空!'
        return result

    if not re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
                    ,p_port["local_ip"]):
        result['code'] = '-1'
        result['message'] = '本地IP地址不合法!'
        return result

    if p_port["local_port"]=="":
        result['code']='-1'
        result['message']='本地PORT不能为空!'
        return result

    if len(re.findall(r'^\d{4,5}$', p_port["local_port"]))==0:
        result['code'] = '-1'
        result['message'] = '本地PORT必须为连续4-5位数字!'
        return result

    if p_port["mapping_port"] == "":
        result['code'] = '-1'
        result['message'] = '映射PORT不能为空!'
        return result

    if len(re.findall(r'^\d{4,5}$', p_port["mapping_port"]))==0:
        result['code'] = '-1'
        result['message'] = '映射PORT必须为连续4-5位数字!'
        return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result

async def get_port_by_portid(p_portid):
    sql = """select  id,market_id,app_desc,local_ip,local_port,mapping_port,mapping_domain,mapping_type from t_port where id={0}""".format(p_portid)
    return await async_processer.query_dict_one(sql)

async def imp_port(p_file,p_name):
    try:
        file  = xlrd.open_workbook(p_file)
        name  = file.sheet_names()[0]
        sheet = file.sheet_by_name(name)
        vals  = ''
        for i in range(1, sheet.nrows):
            val=''
            for j in range(0, sheet.ncols):
                val=val+"'"+str(sheet.cell(i, j).value)+"',"
            vals =vals +'('+val[0:-1]+'),'

        sql="insert into t_port(market_id,market_name,app_desc,local_ip,local_port,mapping_port,mapping_domain) values {0}".format(vals[0:-1])
        await async_processer.exec_sql(sql)
        sql = """update t_port set creater='{}',create_date=now()""".format(p_name)
        await async_processer.exec_sql(sql)

        result={}
        result['code']='0'
        result['message']='导入成功！'
        return result
    except :
        traceback.print_exc()
        result = {}
        result['code'] = '-1'
        result['message'] = '导入失败！'
        return result

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

def set_row_styles(p_fontsize,p_color):
    cell_borders   = xlwt.Borders()
    cell_styles    = xlwt.XFStyle()

    # add font
    font = xlwt.Font()
    font.name = u'微软雅黑'
    font.bold = True
    font.size = p_fontsize
    cell_styles.font = font

    #add col style
    cell_borders.left     = xlwt.Borders.THIN
    cell_borders.right    = xlwt.Borders.THIN
    cell_borders.top      = xlwt.Borders.THIN
    cell_borders.bottom   = xlwt.Borders.THIN

    row_pattern           = xlwt.Pattern()
    row_pattern.pattern   = xlwt.Pattern.SOLID_PATTERN
    row_pattern.pattern_fore_colour = p_color

    # add alignment
    cell_alignment        = xlwt.Alignment()
    cell_alignment.horz   = xlwt.Alignment.HORZ_LEFT
    cell_alignment.vert   = xlwt.Alignment.VERT_CENTER

    cell_styles.alignment = cell_alignment
    cell_styles.borders   = cell_borders
    cell_styles.pattern   = row_pattern
    cell_styles.font      = font
    return cell_styles

async def exp_port(static_path):
    row_data  = 0
    workbook  = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet('port')
    header_styles = set_header_styles(30,1)
    os.system('cd {0}'.format(static_path + '/downloads/port'))
    file_name   = static_path + '/downloads/port/exp_port_{0}.xls'.format(current_rq())
    file_name_s = 'exp_port_{0}.xls'.format(current_rq())

    sql_market  = "SELECT distinct a.market_id FROM t_port a ORDER BY a.market_id"

    sql_header  = """
                 SELECT 
                       a.market_id    AS "项目编码",
                       b.dmmc         AS "项目名称",
                       app_desc       AS "项目描述",
                       local_ip       AS "本地IP",
                       local_port     AS "本地PORT" ,
                       mapping_port   AS "映射PORT",
                       mapping_domain AS "映射域名"
                 FROM   t_port a,t_dmmx b,t_user c 
                  WHERE a.market_id=b.dmm  
                    and a.creater=c.login_name  
                    and b.dm='05' limit 1"""

    sql_content = """
                     SELECT 
                           a.market_id    AS "项目编码",
                           b.dmmc         AS "项目名称",
                           app_desc       AS "项目描述",
                           local_ip       AS "本地IP",
                           local_port     AS "本地PORT" ,
                           mapping_port   AS "映射PORT",
                           mapping_domain AS "映射域名"
                    FROM   t_port a,t_dmmx b,t_user c 
                    WHERE a.market_id=b.dmm  
                      and a.creater=c.login_name  
                      and b.dm='05'
                      and a.market_id='{}'
                    ORDER BY a.market_id
                  """
    print(sql_market)

    # 写表头
    desc = await async_processer.query_one_desc(sql_header)
    for k in range(len(desc)):
        worksheet.write(row_data, k, desc[k][0], header_styles)
        if k == len(desc) - 1:
            worksheet.col(k).width = 8000
        else:
            worksheet.col(k).width = 4000

    #循环项目写单元格
    row_data = row_data + 1
    rs2 = await async_processer.query_list(sql_market)
    for m in range(len(rs2)):
        rs3 = await async_processer.query_list(sql_content.format(rs2[m][0]))
        for i in rs3:
            for j in range(len(i)):
                if i[j] is None:
                    worksheet.write(row_data, j, '', cell_styles)
                else:
                    cell_styles = set_row_styles(30, (m+3)*2-1)
                    worksheet.write(row_data, j, str(i[j]), cell_styles)
            row_data = row_data + 1

    workbook.save(file_name)
    print("{0} export complete!".format(file_name))

    #生成zip压缩文件
    zip_file = static_path + '/downloads/port/exp_port_{0}.zip'.format(current_rq())
    rzip_file = '/static/downloads/port/exp_port_{0}.zip'.format(current_rq())

    #若文件存在则删除
    if os.path.exists(zip_file):
        os.system('rm -f {0}'.format(zip_file))

    z = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED, allowZip64=True)
    z.write(file_name, arcname=file_name_s)
    z.close()

    # 删除json文件
    os.system('rm -f {0}'.format(file_name))
    return rzip_file