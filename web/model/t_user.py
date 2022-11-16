#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/3 15:46
# @Author  : ma.fei
# @File    : t_user.py
# @Software: PyCharm

import traceback
import datetime
from web.utils.common      import current_rq,aes_encrypt,aes_decrypt,aes_decrypt_sync
from web.model.t_user_role import del_user_roles,save_user_role,upd_user_role
from web.utils.common      import now,exception_info
from web.model.t_dmmx      import get_dmmc_from_dm,get_dmmc_from_dm_sync
from web.utils.jwt_auth import kill_session_log
from web.utils.mysql_async import async_processer
from web.utils.mysql_sync  import sync_processer

def check_modify_password(user,newpass,reppass,auth_str):
    result={}
    result['code']='0'
    if newpass == "":
        result['code'] = '-1'
        result['message'] = '新口令不能为空！'
        return result

    if reppass == "":
        result['code'] = '-1'
        result['message'] = '重复口令不能为空！'
        return result

    if  not (newpass == reppass) :
        result['code'] = '-1'
        result['message'] = '口令输入不一致！'
        return result
    return result

def dif_time(p_tm):
    now_time = datetime.datetime.now()
    now_time = now_time.strftime('%Y%m%d%H%M%S')
    d1       = datetime.datetime.strptime(p_tm, '%Y%m%d%H%M%S')
    d2       = datetime.datetime.strptime(now_time,'%Y%m%d%H%M%S')
    sec      = (d2 - d1).seconds
    return sec

async def logon_user_check(login_name,password,verify_code,verify_img):
    result={}
    if login_name == "":
        result['code'] = '-1'
        result['message'] = '用户名不能为空！'
        return result

    if password == "":
        result['code'] = '-1'
        result['message'] = '口令不能为空！'
        return result

    if verify_code == "":
        result['code'] = '-1'
        result['message'] = '验证码不能为空！'
        return result

    if verify_code.upper() != verify_img.upper():
        result['code'] = '-1'
        result['message'] = '验证码不正确！'
        return result

    if await check_user_exist(login_name)==0:
        result['code'] = '-1'
        result['message'] = '用户名不存在！'
        return result

    user = await get_user_by_loginame(login_name)

    if user['password']!=password:
        result['code'] = '-1'
        result['message'] = '口令有误！'
        return result

    if user['status']=='0':
        result['code'] = '-1'
        result['message'] = '用户已禁用，请联系管理员！'
        return result

    if user['expire_date']<now():
        result['code'] = '-1'
        result['message'] = '该用户已过期，请联系管理员！'
        return result

    if (await async_processer.query_one("""select count(0) 
                                           from t_session 
                                           where username='{}' 
                                             and TIMESTAMPDIFF(SECOND,last_update_time,NOW())<60 
                                             order by last_update_time desc limit 1""".format(login_name)))[0]>0:
        sec = (await async_processer.query_one("""select 60-TIMESTAMPDIFF(SECOND,last_update_time,NOW())  
                                                 from t_session 
                                                 where username='{}' order by last_update_time desc limit 1""".format(login_name)))[0]
        result['code'] = '-1'
        result['message'] = '用户已登陆,请{}秒后重试!'.format(sec)
        return result


    result['code'] = '0'
    result['message'] ='验证成功！'
    return result

async def check_forget_password(login_name,email):
    result={}
    result['url']=''
    if login_name == "":
        result['code'] = '-1'
        result['message'] = '用户名不能为空！'
        return result

    if email == "":
        result['code'] = '-1'
        result['message'] = '邮箱不能为空！'
        return result

    if (await check_user_exist(login_name))==0:
        result['code'] = '-1'
        result['message'] = '用户名不存在！'
        return result

    if (await check_email_exist(login_name,email)) == 0:
        result['code'] = '-1'
        result['message'] = '非注册邮箱！'
        return result

    if (await get_user_by_loginame(login_name))['status']=='0':
        result['code'] = '-1'
        result['message'] = '用户已禁用，请联系管理员！'
        return result

    if (await get_user_by_loginame(login_name))['expire_date']<now():
        result['code'] = '-1'
        result['message'] = '该用户已过期，请联系管理员！'
        return result

    result['code'] = '0'
    result['message'] ='验证成功！'
    return result

async def check_authcode(user,auth_str):
    result = {}
    result['code']='0'
    result['message'] = '认证成功!'

    if auth_str == '' or auth_str is None:
        result['code'] = '-1'
        result['message'] = '授权码不能为空！'
        return result

    if not await check_auth_str_exist(auth_str):
       result['code'] = '-1'
       result['message'] = '授权码不正确!'
       return result

    v_max_rq = await get_create_date_by_auth((await get_user_by_loginame(user))['userid'],auth_str)
    if dif_time(v_max_rq)>60:
       result['code'] = '-1'
       result['message'] = '授权码已过期!'
       return result

    return result

async def save_forget_authention_string(p_username,p_auth_string):
    result = {}
    try:
        userid= (await get_user_by_loginame(p_username))['userid']
        sql = """insert into t_forget_password(user_id,authentication_string,creation_date,creator) 
                       values('{0}','{1}',now(),'{2}')
                    """.format(userid, p_auth_string,p_username)
        await async_processer.exec_sql(sql)
        result = {}
        result['code'] = '0'
        result['message'] = '保存成功！'
        return result
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '写入授权码异常!'

    return result

async def query_user(p_name):
    v_where = ''
    if p_name != "":
       v_where =  " where binary name like '%{0}%' or a.login_name like '%{1}%' ".format(p_name,p_name)
    sql = """select a.id,a.login_name,
                 CONCAT(a.file_path,'/',a.file_name) as user_image,
                 a.wkno, 
                 name,
                 (select dmmc from t_dmmx where dm='04' and dmm=a.gender) as gender,
                 a.email,a.phone,
                 -- (select dmmc from t_dmmx where dm='18' and dmm=a.project_group) as project_group,
                 (select dmmc from t_dmmx where dm='01' and dmm=a.dept) as dept,
                 date_format(a.expire_date,'%Y-%m-%d') as expire_date,
                 case a.status when '1' then '启用'
                             when '0' then '禁用'
                 end  status,
                 -- date_format(a.creation_date,'%Y-%m-%d')    creation_date,
                 date_format(a.last_update_date,'%Y-%m-%d') last_update_date 
             from t_user a  {}
             order by convert(name using gbk) asc""".format(v_where)
    v_list = await async_processer.query_list(sql)
    return v_list

async def query_user_proj_privs(p_name,p_dsid,is_grants):
    if p_name == "":
        sql = """select u.id,u.login_name,u.name,u.email,u.phone,u.dept,
                       (select count(0) from t_user_proj_privs 
                        where proj_id='{0}' and user_id=u.id and priv_id='1') as query_priv,
                       (select count(0) from t_user_proj_privs 
                        where proj_id='{1}' and user_id=u.id and priv_id='2') as release_priv         
              from t_user  u order by convert(name using gbk) asc""".format(p_dsid,p_dsid)
    else:
        sql = """select u.id,u.login_name,u.name,u.email,u.phone,u.dept,
                       (select count(0) from t_user_proj_privs 
                        where proj_id='{0}' and user_id=u.id and priv_id='1') as query_priv,
                       (select count(0) from t_user_proj_privs 
                        where proj_id='{1}' and user_id=u.id and priv_id='2') as release_priv  
                 from t_user u 
                where binary u.name like '%{2}%'              
                 order by convert(name using gbk) asc""".format(p_dsid,p_dsid,p_name)
    return await async_processer.query_list(sql)

async def get_userid():
    sql = "select max(id)+1 from t_user"
    rs = await async_processer.query_one(sql)
    return rs[0]

async def get_userid_by_auth(v_str):
    sql="select max(user_id) from t_forget_password where authentication_string='{0}'".format(v_str)
    rs = await async_processer.query_one(sql)
    return rs[0]

async def get_create_date_by_auth(v_userid,v_str):
    sql="select date_format(creation_date,'%Y%m%d%H%i%s')  from t_forget_password where user_id='{}' and authentication_string='{}'".format(v_userid,v_str)
    rs = await async_processer.query_one(sql)
    return rs[0]

async def check_user_exist(p_login_name):
    sql="select count(0) from t_user where login_name='{0}'".format(p_login_name)
    rs = await async_processer.query_one(sql)
    return rs[0]

async def check_email_exist(p_login_name,p_email):
    sql="select count(0) from t_user where login_name='{0}' and email='{1}'".format(p_login_name,p_email)
    rs = await async_processer.query_one(sql)
    return rs[0]

async def check_auth_str_exist(p_auth_str):
    sql="select count(0) from t_forget_password where authentication_string='{0}'".format(p_auth_str)
    rs = await async_processer.query_one(sql)
    if rs[0]==0:
        return False
    else:
        return True

async def get_user_by_userid(p_userid):
    sql="""select cast(id as char) as userid,
                  login_name as loginname, 
                  name as username,
                  password,
                  gender,
                  email,
                  phone,dept,
                  date_format(expire_date,'%Y-%m-%d') as expire_date,
                  status,
                  ifnull(file_path,' ') as image_path,
                  ifnull(file_name,' ') as image_name,
                  project_group,
                  wkno
        from t_user where id={0}""".format(p_userid)
    user = await async_processer.query_dict_one(sql)
    user['password'] = await aes_decrypt(user['password'],user['loginname'])
    return user

def get_user_by_userid_sync(p_userid):
    sql="""select cast(id as char) as userid,
                  login_name as loginname, 
                  name as username,
                  password,
                  gender,
                  email,
                  phone,dept,
                  date_format(expire_date,'%Y-%m-%d') as expire_date,
                  status,
                  ifnull(file_path,' ') as image_path,
                  ifnull(file_name,' ') as image_name,
                  project_group,
                  wkno
        from t_user where id={0}""".format(p_userid)
    user = sync_processer.query_dict_one(sql)
    user['password'] = aes_decrypt_sync(user['password'],user['loginname'])
    return user

async def get_users(p_dept):
    sql = """select id,name from t_user  WHERE dept='{0}' order by id""".format(p_dept)
    return await async_processer.query_list(sql)

async def get_user_by_loginame(p_login_name):
    sql= """select cast(id as char) as id,
                name,
                login_name,
                password,
                gender,
                email,
                phone,
                dept,
                date_format(expire_date,'%Y-%m-%d') as expire_date,
                status,
                file_path,
                file_name,
                project_group,
                wkno
         from t_user where login_name='{0}'
        """.format(p_login_name)
    d_user              = await async_processer.query_dict_one(sql)
    d_user['userid']    = d_user['id']
    d_user['username']  = d_user['name']
    d_user['password']  = await aes_decrypt(d_user['password'], d_user['login_name'])
    d_user['gender_cn'] = await get_dmmc_from_dm('04', d_user['gender'])
    d_user['dept_cn']   = await get_dmmc_from_dm('01', d_user['dept'])
    return d_user

def get_user_by_loginame_sync(p_login_name):
    sql= """select cast(id as char) as id,
                name,
                login_name,
                password,
                gender,
                email,
                phone,
                dept,
                date_format(expire_date,'%Y-%m-%d') as expire_date,
                status,
                file_path,
                file_name,
                project_group,
                wkno
         from t_user where login_name='{0}'
        """.format(p_login_name)
    d_user              = sync_processer.query_dict_one(sql)
    d_user['userid']    = d_user['id']
    d_user['username']  = d_user['name']
    d_user['password']  = aes_decrypt_sync(d_user['password'], d_user['login_name'])
    d_user['gender_cn'] = get_dmmc_from_dm_sync('04', d_user['gender'])
    d_user['dept_cn']   = get_dmmc_from_dm_sync('01', d_user['dept'])
    return d_user

async def check_user(p_user):
    result = {}
    if p_user["login"] == "":
        result['code'] = '-1'
        result['message'] = '登陆名不能为空！'
        return result

    if p_user["user"] == "":
        result['code'] = '-1'
        result['message'] = '姓名不能为空！'
        return result

    if p_user["pass"] == "":
        result['code'] = '-1'
        result['message'] = '口令不能为空！'
        return result

    if p_user["gender"] == "":
        result['code'] = '-1'
        result['message'] = '性别不能为空！'
        return result

    if p_user["dept"] == "":
        result['code'] = '-1'
        result['message'] = '部门不能为空！'
        return result

    if p_user["email"] == "":
        result['code'] = '-1'
        result['message'] = '邮箱不能为空！'
        return result

    if p_user["phone"] == "":
        result['code'] = '-1'
        result['message'] = '联系方式不能为空！'
        return result

    if p_user["expire_date"] == "":
        result['code'] = '-1'
        result['message'] = '过期日期不能为空！'
        return result

    if p_user["privs"][0] is None or p_user["privs"][0]=='':
        result['code'] = '-1'
        result['message'] = '用户角色不能为空！'
        return result

    if await check_user_exist(p_user["login"] ) > 0:
        result['code'] = '-1'
        result['message'] = '用户名已存在！'
        return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result

async def save_user(p_user):
    result = {}
    val = await check_user(p_user)
    if val['code'] == '-1':
        return val
    try:
        userid       = await get_userid()
        loginname    = p_user['login']
        wkno         = p_user['wkno']
        username     = p_user['user']
        password     = await aes_encrypt(p_user['pass'],loginname)
        gender       = p_user['gender']
        email        = p_user['email']
        phone        = p_user['phone']
        proj_group   = p_user['proj_group']
        dept         = p_user['dept']
        expire_date  = p_user['expire_date']
        status       = p_user['status']
        privs        = p_user['privs']
        file_path    = p_user['file_path']
        file_name    = p_user['file_name']

        if file_path=='':
           file_path = '/static/assets/images/users'

        if  file_name=='':
            if gender=='1':
                file_name = 'boy.png'
            else:
                file_name = 'girl.png'

        sql="""insert into t_user(id,login_name,wkno,name,password,gender,email,phone,project_group,dept,expire_date,status,file_path,file_name,creation_date,creator,last_update_date,updator) 
                    values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}')
            """.format(userid,loginname,wkno,username,password,gender,email,phone,proj_group,dept,expire_date,status,file_path,file_name,current_rq(),'DBA',current_rq(),'DBA');

        await async_processer.exec_sql(sql)
        await save_user_role(userid,privs)
        result={}
        result['code']='0'
        result['message']='保存成功！'
        return result
    except Exception as e:
        result['code'] = '-1'
        result['message'] = '保存失败！'
        return result

async def save_user_proj_privs(d_proj):
    result = {}
    dsid   = d_proj['dsid']
    userid = d_proj['userid']
    priv_query   = d_proj['priv_query']
    priv_release = d_proj['priv_release']
    priv_audit   = d_proj['priv_audit']
    priv_execute = d_proj['priv_execute']
    priv_order   = d_proj['priv_order']
    priv_export  = d_proj['priv_export']

    try:
        # process query privs
        if priv_query=='1':
           sql = """delete from  t_user_proj_privs where proj_id='{0}' and user_id='{1}' and priv_id='1'""".format(dsid,userid)
           await async_processer.exec_sql(sql)
           sql = """insert into t_user_proj_privs(proj_id,user_id,priv_id) values('{0}','{1}','{2}') """.format(dsid,userid, '1')
           await async_processer.exec_sql(sql)
        else:
            sql = """delete from  t_user_proj_privs 
                        where proj_id='{0}' and user_id='{1}' and priv_id='1'""".format(dsid, userid)
            await async_processer.exec_sql(sql)

        # process release privs
        if priv_release == '1':
            sql = """delete from  t_user_proj_privs 
                        where proj_id='{0}' and user_id='{1}' and priv_id='2'""".format(dsid, userid)
            await async_processer.exec_sql(sql)
            sql = """insert into t_user_proj_privs(proj_id,user_id,priv_id) 
                           values('{0}','{1}','{2}') """.format(dsid, userid, '2')
            await async_processer.exec_sql(sql)
        else:
            sql = """delete from  t_user_proj_privs 
                         where proj_id='{0}' and user_id='{1}' and priv_id='2'""".format(dsid, userid)
            await async_processer.exec_sql(sql)

        # process audit privs
        if priv_audit == '1':
            sql = """delete from  t_user_proj_privs 
                           where proj_id='{0}' and user_id='{1}' and priv_id='3'""".format(dsid, userid)
            await async_processer.exec_sql(sql)
            sql = """insert into t_user_proj_privs(proj_id,user_id,priv_id) 
                              values('{0}','{1}','{2}') """.format(dsid, userid, '3')
            await async_processer.exec_sql(sql)
        else:
            sql = """delete from  t_user_proj_privs 
                            where proj_id='{0}' and user_id='{1}' and priv_id='3'""".format(dsid, userid)
            await async_processer.exec_sql(sql)

        #process execute privs
        if priv_execute == '1':
            sql = """delete from  t_user_proj_privs 
                         where proj_id='{0}' and user_id='{1}' and priv_id='4'""".format(dsid, userid)
            await async_processer.exec_sql(sql)
            sql = """insert into t_user_proj_privs(proj_id,user_id,priv_id) 
                         values('{0}','{1}','{2}') """.format(dsid, userid, '4')
            await async_processer.exec_sql(sql)
        else:
            sql = """delete from  t_user_proj_privs 
                          where proj_id='{0}' and user_id='{1}' and priv_id='4'""".format(dsid, userid)
            await async_processer.exec_sql(sql)

        #process order privs
        if priv_order == '1':
            sql = """delete from  t_user_proj_privs 
                            where proj_id='{0}' and user_id='{1}' and priv_id='5'""".format(dsid, userid)
            await async_processer.exec_sql(sql)
            sql = """insert into t_user_proj_privs(proj_id,user_id,priv_id) 
                            values('{0}','{1}','{2}') """.format(dsid, userid, '5')
            await async_processer.exec_sql(sql)
        else:
            sql = """delete from  t_user_proj_privs 
                             where proj_id='{0}' and user_id='{1}' and priv_id='5'""".format(dsid, userid)
            await async_processer.exec_sql(sql)

        # process export privs
        if priv_export == '1':
            sql = """delete from  t_user_proj_privs 
                              where proj_id='{0}' and user_id='{1}' and priv_id='6'""".format(dsid, userid)
            await async_processer.exec_sql(sql)
            sql = """insert into t_user_proj_privs(proj_id,user_id,priv_id) 
                              values('{0}','{1}','{2}') """.format(dsid, userid, '6')
            await async_processer.exec_sql(sql)
        else:
            sql = """delete from  t_user_proj_privs 
                               where proj_id='{0}' and user_id='{1}' and priv_id='6'""".format(dsid, userid)
            await async_processer.exec_sql(sql)

        result={}
        result['code']='0'
        result['message']='保存成功！'
        return result
    except:
        exception_info()
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result

async def upd_user(p_user):
    result={}
    try:
        userid      = p_user['userid']
        loginname   = p_user['loginname']
        wkno        = p_user['wkno']
        username    = p_user['username']
        password    = await aes_encrypt(p_user['password'],loginname)
        gender      = p_user['gender']
        email       = p_user['email']
        phone       = p_user['phone']
        proj_group  = p_user['proj_group']
        dept        = p_user['dept']
        expire_date = p_user['expire_date']
        status      = p_user['status']
        roles       = p_user['roles']
        file_path   = p_user['file_path']
        file_name   = p_user['file_name']

        if file_path == '':
            file_path = '/static/assets/images/users'

        if file_name == '':
            if gender == '1':
                file_name = 'boy.png'
            else:
                file_name = 'girl.png'

        sql="""update t_user 
                  set  name     ='{0}',
                       login_name='{1}',
                       password ='{2}',
                       gender   ='{3}',
                       email    ='{4}',
                       phone    ='{5}',
                       dept     ='{6}',
                       expire_date      ='{7}' ,
                       status           ='{8}' ,
                       last_update_date ='{9}' ,
                       updator   ='{10}',
                       file_path ='{11}',
                       file_name = '{12}',
                       project_group = '{13}',
                       wkno          = '{14}'
                where id='{15}'""".format(username,loginname,password,gender,email,phone,dept,expire_date,status,
                                          current_rq(),'DBA',file_path,file_name,proj_group,wkno,userid)
        await async_processer.exec_sql(sql)
        await upd_user_role(userid,roles)
        result={}
        result['code']='0'
        result['message']='更新成功！'
    except :
        exception_info()
        result['code'] = '-1'
        result['message'] = '更新失败！'
    return result

async def upd_password(p_user):
    result={}
    try:
        userid      = p_user['userid']
        loginname   = p_user['loginname']
        password    = await aes_encrypt(p_user['password'],loginname)
        sql="""update t_user 
                  set  password ='{0}',                    
                       last_update_date ='{1}' ,
                       updator='{2}'
                where id='{3}'""".format(password,current_rq(),'DBA',userid)
        await async_processer.exec_sql(sql)
        result={}
        result['code']='0'
        result['message']='修改成功！'
    except :
        exception_info()
        result['code'] = '-1'
        result['message'] = '修改失败！'
    return result

async def del_user(p_user):
    result={}
    try:
        userid   = p_user['userid']
        sql="delete from t_user  where id='{0}'".format(userid)
        await async_processer.exec_sql(sql)
        await del_user_roles(userid)
        result={}
        result['code']='0'
        result['message']='删除成功！'
    except :
        result['code'] = '-1'
        result['message'] = '删除失败！'
    return result

async def get_sys_roles(p_userid):
    sql="""select cast(id as char) as id,name 
           from t_role
           where status='1'
             and id not in(select role_id from t_user_role where user_id='{0}')      
        """.format(p_userid)
    return await async_processer.query_list(sql)

async def get_user_roles(p_userid):
    sql="""select cast(id as char) as id,name
           from t_role 
            where status='1'  
              and id  in(select role_id from t_user_role where user_id='{0}')    
        """.format(p_userid)
    return await async_processer.query_list(sql)


async def query_session(p_name):
    v_where = ''
    if p_name != "":
       v_where =  " where binary username like '%{0}%'  ".format(p_name)

    sql = """select 
                a.session_id,
                a.userid,
                a.username,
                a.name,
                date_format(a.logon_time,'%Y-%m-%d')  as  logon_time,
                a.login_ip,
                case a.state when '1' then '活动' when '2' then '未活动' when '3' then '已杀死' when '4' then '已注销'
                end  state,
                TIMESTAMPDIFF(SECOND,logon_time,NOW()) as online_time,
                date_format(a.last_update_time,'%Y-%m-%d %H:%i:%s') as last_update_time
             from t_session a  {}
             order by session_id""".format(v_where)
    v_list = await async_processer.query_list(sql)
    return v_list


async def kill_session(p_session_id):
     try:
       await kill_session_log(p_session_id)
       return {'code':0,'message':'success'}
     except:
       traceback.print_exc()
       return {'code': -1, 'message': 'failure'}