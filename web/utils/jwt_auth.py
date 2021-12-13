#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/9/26 14:51
# @Author : ma.fei
# @File : jwt_auth.py.py
# @Software: PyCharm

import jwt
import json
import datetime
from jwt import exceptions
from tornado.web import HTTPError

JWT_SALT = 'Hopson2021@abcd'
ISS_UER  = 'zhitbar.cn'
TIMEOUT  = 60

def create_token(payload, timeout=TIMEOUT):
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
    payload['iat'] = datetime.datetime.utcnow()
    payload['iss'] = ISS_UER
    result =jwt.encode(payload=payload, key=JWT_SALT, algorithm="HS256",headers=headers)
    return result

def refresh_token(token,timeout=TIMEOUT):
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    result = parse_payload(token)
    if not result["status"]:
        raise HTTPError(result['code'], json.dumps(result, ensure_ascii=False))

    payload = result['data']
    print('refresh_token=>payload:', payload)
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
    payload['iat'] = datetime.datetime.utcnow()
    payload['iss'] = ISS_UER
    result = jwt.encode(payload=payload, key=JWT_SALT, algorithm="HS256", headers=headers)
    print('refresh_token=>result:',result)
    return result

def parse_payload(token):
    result = {'status': False,'code':200,'data': None, 'error': None}
    try:
        header= jwt.get_unverified_header(token)
        if header['typ']!= 'jwt':
             result['code'] = 404
             result['error'] = 'token认证方式错误!'
        elif header['alg']!='HS256':
            result['code'] = 405
            result['error'] = 'token认证算法错误!'
        else:
            verified_payload = jwt.decode(token, JWT_SALT,issuer=ISS_UER,algorithms=["HS256"])
            print('verified_payload=',verified_payload)
            result['status'] = True
            result['code'] = 200
            result['data'] = verified_payload
    except exceptions.ExpiredSignatureError:
        result['code']  =  401
        result['error'] = 'token已失效!'
    except jwt.DecodeError:
        result['code'] = 402
        result['error'] = 'token认证失败!'
    except jwt.InvalidTokenError:
        result['code'] = 403
        result['error'] = '非法的token!'
    return result