#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : 马飞
# @File    : t_user.py
# @Software: PyCharm

from web.utils.common import exception_info,get_connection
from web.utils.common import current_rq
import traceback
import xlrd,xlwt
import os,zipfile
import re

def query_port(p_market_id):
    db = get_connection()
    cr = db.cursor()
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
             AND b.dm='05'
             {}
             order by a.market_id
          """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def save_port(p_port):
    result = {}

    val=check_port(p_port)
    if val['code']=='-1':
        return val
    try:
        db                = get_connection()
        cr                = db.cursor()
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

def upd_port(p_port):
    result={}
    val = check_port(p_port)
    if  val['code'] == '-1':
        return val
    try:
        db              = get_connection()
        cr              = db.cursor()
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

def del_port(p_portid):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        sql="delete from t_port  where id='{0}'".format(p_portid)
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

def check_port_rep(p_port):
    db = get_connection()
    cr = db.cursor()
    sql = "select count(0) from t_port  where  instr(app_port,'{0}')>0".format(p_port['app_port'])
    print(sql)
    cr.execute(sql)
    rs=cr.fetchone()
    cr.close()
    db.commit()
    return rs[0]

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

def get_port_by_portid(p_portid):
    db = get_connection()
    cr = db.cursor()
    sql = """select  id,market_id,app_desc,local_ip,local_port,mapping_port,mapping_domain,mapping_type from t_port where id={0}
          """.format(p_portid)
    print(sql)
    cr.execute(sql)
    rs = cr.fetchall()
    d_port = {}
    d_port['id']             = rs[0][0]
    d_port['market_id']      = rs[0][1]
    d_port['app_desc']       = rs[0][2]
    d_port['local_ip']       = rs[0][3]
    d_port['local_port']     = rs[0][4]
    d_port['mapping_port']   = rs[0][5]
    d_port['mapping_domain'] = rs[0][6]
    d_port['mapping_type']   = rs[0][7]
    cr.close()
    db.commit()
    print(d_port)
    return d_port

def imp_port(p_file,p_name):
    try:
        result={}
        file  = xlrd.open_workbook(p_file)
        name  = file.sheet_names()[0]
        sheet = file.sheet_by_name(name)
        vals  = ''
        for i in range(1, sheet.nrows):
            val=''
            for j in range(0, sheet.ncols):
                val=val+"'"+str(sheet.cell(i, j).value)+"',"
            vals =vals +'('+val[0:-1]+'),'

        print('vals=',vals)
        db = get_connection()
        cr = db.cursor()
        sql="insert into t_port(market_id,market_name,app_desc,local_ip,local_port,mapping_port,mapping_domain) values {0}".format(vals[0:-1])
        print(sql)
        cr.execute(sql)
        sql2 = """update t_port set creater='{}',create_date=now()""".format(p_name)
        print(sql2)
        cr.execute(sql2)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='导入成功！'
    except :
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
    # 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon,
    # 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta,
    # 21 = Teal, 22 = Light Gray, 23 = Dark Gray
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

def exp_port(static_path):
    db   = get_connection()
    cr1  = db.cursor()
    cr2  = db.cursor()
    cr3  = db.cursor()
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
    cr1.execute(sql_header)
    desc = cr1.description
    for k in range(len(desc)):
        worksheet.write(row_data, k, desc[k][0], header_styles)
        if k == len(desc) - 1:
            worksheet.col(k).width = 8000
        else:
            worksheet.col(k).width = 4000

    #循环项目写单元格
    row_data = row_data + 1
    cr2.execute(sql_market)
    rs2 = cr2.fetchall()
    for m in range(len(rs2)):
        print('sql_content=',sql_content.format(rs2[m][0]))
        cr3.execute(sql_content.format(rs2[m][0]))
        rs3 = cr3.fetchall()
        for i in rs3:
            for j in range(len(i)):
                if i[j] is None:
                    worksheet.write(row_data, j, '', cell_styles)
                else:
                    cell_styles = set_row_styles(30, (m+3)*2-1)
                    worksheet.write(row_data, j, str(i[j]), cell_styles)
            row_data = row_data + 1

    workbook.save(file_name)
    db.commit()
    cr1.close()
    cr2.close()
    cr3.close()
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
    print('zip_file=', zip_file)

    # 删除json文件
    os.system('rm -f {0}'.format(file_name))
    return rzip_file