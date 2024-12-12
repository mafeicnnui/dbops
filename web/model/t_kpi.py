#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : ma.fei
# @File    : t_user.py
# @Software: PyCharm

import os
import traceback
import zipfile

import xlwt

from web.utils.common import current_rq
from web.utils.mysql_async import async_processer


async def query_kpi_item(p_month, p_market_id):
    v_where = ' where 1=1 '
    if p_month != '':
        v_where = v_where + " and month='{0}'\n".format(p_month)

    if p_market_id != '':
        v_where = v_where + " and market_id='{0}'\n".format(p_market_id)

    sql = """SELECT market_id,market_name,month,item_code,item_name,item_value
              FROM kpi_item_plan 
              {}""".format(v_where)

    return await async_processer.query_list(sql)


async def query_kpi_item_market():
    sql = """SELECT market_id,market_name FROM `kpi_po`  ORDER BY market_id+0"""
    return await async_processer.query_list(sql)


async def query_kpi(p_month, p_market_id):
    v_where = ' '
    if p_market_id != '':
        v_where = v_where + " and a.market_id='{0}'\n".format(p_market_id)

    sql = """select date_format(a.bbrq,'%Y-%m-%d') as bbrq,
                    a.month,
                    a.market_id,a.market_name,
                    a.item_code,a.item_name,
                    (select case when type=1 then '当月考核' else '累计考核' end  from kpi_item x where x.code=a.item_code) as item_type,
                    a.goal,a.actual_completion,a.completion_rate,
                    a.`annual_target`,a.completion_sum_finish,a.completion_sum_rate,                 
                    c.`if_stat`,
                    date_format(a.update_time,'%Y-%m-%d %H:%i:%s') as update_time
            from kpi_po_hz a,kpi_po b ,kpi_item_sql c
            WHERE a.market_id=b.market_id  AND a.`item_code`=c.`item_code`
              and a.item_code not in('9','13','2.1','2.2','12.1','12.2') 
              and a.month='{}' {}
            ORDER BY b.sxh,a.item_code+0""".format(p_month, v_where)
    return await async_processer.query_list(sql)


async def query_kpi_task(p_task):
    sql = """select  
                    a.comments, 
                    a.month,
                    date_format(a.start_time,'%Y-%m-%d') as start_time,
                    date_format(a.end_time,'%Y-%m-%d') as end_time,
                    a.run_time,
                    case a.status when '1' then '启用' when '0' then '禁用' end  status
            from kpi_config a
            where instr(a.comments,'{0}')>0
            ORDER BY a.id""".format(p_task)
    return await async_processer.query_list(sql)


async def query_kpi_hst(p_bbrq):
    sql = """SELECT market_id,
                    b.dmmc AS market_name, 
                    a.tjrq,
                    a.v1,a.v2,a.v3,a.v4,a.v5,                
                    DATE_FORMAT(a.create_time,'%Y-%m-%d %H:%i:%s') AS create_time
                FROM t_bbtj_log a ,t_dmmx b
                 WHERE a.market_id=b.dmm AND b.dm='05' 
                   AND a.tjrq='{}' ORDER BY market_id""".format(p_bbrq)
    return await async_processer.query_list(sql)


async def update_kpi(p_month, p_market_id):
    result = {}
    result['code'] = '0'
    result['message'] = '保存成功!'
    v_where = ''
    if p_market_id != '':
        v_where = v_where + " and a.market_id='{0}'\n".format(p_market_id)

    st0 = "SELECT DISTINCT market_name as market_name FROM kpi_item_plan a WHERE a.MONTH='2021-06' AND a.item_value='' {} ".format(
        v_where)
    res = await async_processer.query_dict_list(st0)
    print('update_kpi=', res)
    if res != []:
        s = ''
        for m in res:
            s = s + m['market_name'] + ','
        result['code'] = '-1'
        result['message'] = '[' + s[0:-1] + ']月度指标未录入完成!'
        return result

    st1 = """
            UPDATE  kpi_po_hz a ,kpi_item_plan b
               SET a.goal=b.item_value,
                   a.completion_rate=
                   CASE  WHEN  REPLACE(b.item_value,'%','')+0 = 0 THEN
                      ''
                   WHEN INSTR(a.actual_completion,'%') >0 THEN
                      CONCAT(ROUND(ROUND(REPLACE(actual_completion,'%','')/REPLACE(b.item_value,'%',''),4)*100,2),'%')
                   ELSE
                      CONCAT(ROUND(ROUND(a.actual_completion/b.item_value,4)*100,2),'%')
                   END,
                   a.completion_sum_finish='',
                   a.update_time=now()
             WHERE a.market_id=b.market_id
               AND a.month=b.month
               AND a.item_code=b.item_code
               AND a.month='{}' {}
               AND a.item_code IN(SELECT CODE FROM kpi_item WHERE TYPE='1')""".format(p_month, v_where)
    st2 = """
         UPDATE  kpi_po_hz a ,kpi_item_plan b
           SET a.`annual_target`=b.item_value,
               a.`completion_sum_rate`=
               CASE WHEN  REPLACE(b.item_value,'%','')+0 =0 THEN
                  ''  
               WHEN INSTR(a.completion_sum_finish,'%') >0 THEN
                  CONCAT(ROUND(ROUND(REPLACE(a.completion_sum_finish,'%','')/REPLACE(b.item_value,'%',''),4)*100,2),'%')
               WHEN a.completion_sum_finish='' OR a.completion_sum_finish IS NULL THEN
                   '' 
               ELSE
                  CONCAT(ROUND(ROUND(a.completion_sum_finish/b.item_value,4)*100,2),'%')
               END,
               a.actual_completion='',
               a.update_time=now()
         WHERE a.market_id=b.market_id
           AND a.month=b.month
           AND a.item_code=b.item_code
           AND a.month='{}'  {}
           AND a.item_code IN(SELECT CODE FROM kpi_item WHERE TYPE='2')""".format(p_month, v_where)
    try:
        print(st1)
        print(st2)
        await async_processer.exec_sql(st1)
        await async_processer.exec_sql(st2)
        return result
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '保存失败！'
        return result


async def update_item_kpi(p_month, p_market_id, p_item_code, p_item_value):
    result = {}
    result['code'] = '0'
    result['message'] = '更新成功!'
    st1 = """UPDATE  kpi_item_plan a SET a.item_value='{}' WHERE a.month='{}'  AND a.market_id='{}' AND a.item_code='{}'
          """.format(p_item_value, p_month, p_market_id, p_item_code)
    try:
        print(st1)
        await async_processer.exec_sql(st1)
        return result
    except:
        result['code'] = '-1'
        result['message'] = '保存失败！'
        return result


async def update_item_data_kpi(p_month, p_market_id, p_item_code, p_item_month_value, p_item_sum_value):
    result = {}
    result['code'] = '0'
    result['message'] = '更新成功!'
    st1 = """UPDATE  kpi_po_hz a
               SET a.`actual_completion`='{}', a.completion_sum_finish='{}' 
                  WHERE a.month='{}'  AND a.market_id='{}' AND a.item_code='{}'
           """.format(p_item_month_value, p_item_sum_value, p_month, p_market_id, p_item_code)
    try:
        print(st1)
        await async_processer.exec_sql(st1)
        return result
    except:
        result['code'] = '-1'
        result['message'] = '保存失败！'
        return result


async def check_kpi_item_plan(p_month):
    st = """SELECT count(0)  FROM kpi_item_plan where month='{}'""".format(p_month)
    print("check_kpi_item_plan=", st)
    return await async_processer.query_one(st)


async def generate_item_kpi(p_month):
    st1 = """INSERT INTO kpi_item_plan(market_id,market_name,MONTH,item_code,item_name,item_value)
              SELECT market_id,market_name,'{}',item_code,item_name,item_value FROM kpi_item_plan_templete""".format(
        p_month)
    try:
        print(st1)
        res = await check_kpi_item_plan(p_month)
        if res[0] > 0:
            print('res=', res)
            return {"code": '-1', "message": p_month + '月数据已存在!'}

        await async_processer.exec_sql(st1)
        return {"code": '0', "message": '生成成功!'}
    except:
        traceback.print_exc()
        return {"code": '-1', "message": '生成失败!'}


def set_header_styles(p_fontsize, p_color):
    header_borders = xlwt.Borders()
    header_styles = xlwt.XFStyle()
    # add table header style
    header_borders.left = xlwt.Borders.THIN
    header_borders.right = xlwt.Borders.THIN
    header_borders.top = xlwt.Borders.THIN
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
    # add alignment
    header_alignment = xlwt.Alignment()
    header_alignment.horz = xlwt.Alignment.HORZ_CENTER
    header_alignment.vert = xlwt.Alignment.VERT_CENTER
    header_styles.alignment = header_alignment
    header_styles.borders = header_borders
    header_styles.pattern = header_pattern
    return header_styles


def set_row_styles(p_fontsize, p_color):
    cell_borders = xlwt.Borders()
    cell_styles = xlwt.XFStyle()

    # add font
    font = xlwt.Font()
    font.name = u'微软雅黑'
    font.bold = True
    font.size = p_fontsize
    cell_styles.font = font

    # add col style
    cell_borders.left = xlwt.Borders.THIN
    cell_borders.right = xlwt.Borders.THIN
    cell_borders.top = xlwt.Borders.THIN
    cell_borders.bottom = xlwt.Borders.THIN

    row_pattern = xlwt.Pattern()
    row_pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    row_pattern.pattern_fore_colour = p_color

    # add alignment
    cell_alignment = xlwt.Alignment()
    cell_alignment.horz = xlwt.Alignment.HORZ_LEFT
    cell_alignment.vert = xlwt.Alignment.VERT_CENTER

    cell_styles.alignment = cell_alignment
    cell_styles.borders = cell_borders
    cell_styles.pattern = row_pattern
    cell_styles.font = font
    return cell_styles


async def exp_hst_kpi(static_path, p_bbrq):
    row_data = 0
    workbook = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet('hst_kpi')
    header_styles = set_header_styles(45, 1)
    os.system('cd {0}'.format(static_path + '/downloads/kpi'))
    file_name = static_path + '/downloads/port/exp_hst_kpi_{0}.xls'.format(current_rq())
    file_name_s = 'exp_hst_kpi_{0}.xls'.format(current_rq())
    sql_header = """
                 SELECT market_id     AS "项目编码",
                        b.dmmc        AS "项目名称",
                        a.tjrq        AS "报表日期",
                        a.v1          AS "商品上传spu",
                        a.v2          AS "会员拉新(万人)",
                        a.v3          AS "支付即积分覆盖率",
                        a.v4          AS "保底积分率",
                        a.v5          AS "总GMV(万元)",                
                        DATE_FORMAT(a.create_time,'%Y-%m-%d %H:%i:%s') AS "生成时间"
                    FROM t_bbtj_log a ,t_dmmx b
                     WHERE a.market_id=b.dmm AND b.dm='05' 
                       AND a.tjrq='{}' ORDER BY market_id  limit 1 """.format(p_bbrq)
    sql_content = """SELECT market_id,
                    b.dmmc AS market_name, 
                    a.tjrq,
                    a.v1,a.v2,a.v3,a.v4,a.v5,                
                    DATE_FORMAT(a.create_time,'%Y-%m-%d %H:%i:%s') AS create_time
                FROM t_bbtj_log a ,t_dmmx b
                 WHERE a.market_id=b.dmm AND b.dm='05' 
                   AND a.tjrq='{}' ORDER BY market_id""".format(p_bbrq)

    # 写表头
    desc = await async_processer.query_one_desc(sql_header)
    for k in range(len(desc)):
        worksheet.write(row_data, k, desc[k][0], header_styles)
        if k == len(desc) - 1:
            worksheet.col(k).width = 8000
        else:
            worksheet.col(k).width = 4000

    # 循环项目写单元格
    row_data = row_data + 1
    rs3 = await async_processer.query_list(sql_content)
    for i in rs3:
        for j in range(len(i)):
            if i[j] is None:
                worksheet.write(row_data, j, '', cell_styles)
            else:
                cell_styles = set_row_styles(40, 1)
                worksheet.write(row_data, j, str(i[j]), cell_styles)
        row_data = row_data + 1

    workbook.save(file_name)
    print("{0} export complete!".format(file_name))

    # 生成zip压缩文件
    zip_file = static_path + '/downloads/port/exp_hst_kpi_{0}.zip'.format(current_rq())
    rzip_file = '/static/downloads/port/exp_hst_kpi_{0}.zip'.format(current_rq())

    # 若文件存在则删除
    if os.path.exists(zip_file):
        os.system('rm -f {0}'.format(zip_file))

    z = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED, allowZip64=True)
    z.write(file_name, arcname=file_name_s)
    z.close()

    # 删除json文件
    os.system('rm -f {0}'.format(file_name))
    return rzip_file


async def exp_kpi(static_path, p_month, p_market_id):
    row_data = 0
    workbook = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet('kpi')
    header_styles = set_header_styles(45, 1)
    os.system('cd {0}'.format(static_path + '/downloads/kpi'))
    file_name = static_path + '/downloads/port/exp_kpi_{0}.xls'.format(current_rq())
    file_name_s = 'exp_kpi_{0}.xls'.format(current_rq())

    v_where = ' '
    if p_market_id != '':
        v_where = v_where + " and a.market_id='{0}'\n".format(p_market_id)

    sql_header = """select date_format(a.bbrq,'%Y-%m-%d') as "报表日期",
                       a.month                 as "报表月",
                       a.market_id             as "项目编码	",
                       a.market_name           as "项目名称",
                       a.item_code             as "指标编码",
                       a.item_name             as "指标名称",
                       (select case when type=1 then '当月考核' else '累计考核' end  from kpi_item x where x.code=a.item_code) as "指标说明",
                       a.goal                  as "月度指标",
                       a.actual_completion     as "月度完成",
                       a.completion_rate       as "月度完成率",
                       a.`annual_target`       as "年度指标",
                       a.completion_sum_finish as "年度完成	",
                       a.completion_sum_rate   as "年度完成率"
               from kpi_po_hz a,kpi_po b ,kpi_item_sql c
               WHERE a.market_id=b.market_id  AND a.`item_code`=c.`item_code`
                 and a.item_code not in('9','13','2.1','2.2','12.1','12.2') 
                 and a.month='{}' {}
                   ORDER BY b.sxh,a.item_code+0 limit 1""".format(p_month, v_where)

    sql_content = """select 
                       date_format(a.bbrq,'%Y-%m-%d') as bbrq,
                       a.month,
                       a.market_id,a.market_name,
                       a.item_code,a.item_name,
                       (select case when type=1 then '当月考核' else '累计考核' end  from kpi_item x where x.code=a.item_code) as item_type,
                       a.goal,a.actual_completion,a.completion_rate,
                       a.`annual_target`,a.completion_sum_finish,a.completion_sum_rate
               from kpi_po_hz a,kpi_po b ,kpi_item_sql c
               WHERE a.market_id=b.market_id  AND a.`item_code`=c.`item_code`
                 and a.item_code not in('9','13','2.1','2.2','12.1','12.2') 
                 and a.month='{}' {}
                   ORDER BY b.sxh,a.item_code+0""".format(p_month, v_where)

    # 写表头
    desc = await async_processer.query_one_desc(sql_header)
    for k in range(len(desc)):
        worksheet.write(row_data, k, desc[k][0], header_styles)
        if k in (3, 5):
            worksheet.col(k).width = 8000
        else:
            worksheet.col(k).width = 4000

    # 循环项目写单元格
    row_data = row_data + 1
    rs3 = await async_processer.query_list(sql_content)
    for i in rs3:
        for j in range(len(i)):
            cell_styles = set_row_styles(45, 1)
            if i[j] is None:
                worksheet.write(row_data, j, '')
            else:
                worksheet.write(row_data, j, str(i[j]))
        row_data = row_data + 1

    workbook.save(file_name)
    print("{0} export complete!".format(file_name))

    # 生成zip压缩文件
    zip_file = static_path + '/downloads/port/exp_kpi_{0}.zip'.format(current_rq())
    rzip_file = '/static/downloads/port/exp_kpi_{0}.zip'.format(current_rq())

    # 若文件存在则删除
    if os.path.exists(zip_file):
        os.system('rm -f {0}'.format(zip_file))

    z = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED, allowZip64=True)
    z.write(file_name, arcname=file_name_s)
    z.close()

    # 删除json文件
    os.system('rm -f {0}'.format(file_name))
    return rzip_file
