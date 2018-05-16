#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import hashlib
from AutoCmdb.settings import ASSET_AUTH_HEADER_NAME
from AutoCmdb.settings import ASSET_AUTH_KEY
from AutoCmdb.settings import ASSET_AUTH_TIME
from django.http import JsonResponse

ENCRYPT_LIST = [
    # {'encrypt': encrypt, 'time': timestamp
]


def api_auth_method(request):
    auth_key = request.META.get('HTTP_AUTH_KEY')
    print(auth_key,"拿到提交到的auth_key")
    # db5da58d2aa12263c8df2877e60bc45f|1526478003.523982
    if not auth_key:
        return False
    sp = auth_key.split('|')
    if len(sp) != 2:
        return False
    encrypt, timestamp = sp
    timestamp = float(timestamp)
    limit_timestamp = time.time() - ASSET_AUTH_TIME
    print(timestamp,limit_timestamp ,"前面拿到发过来的时间,后面拿当前时间-2,")
    if limit_timestamp > timestamp:
        return False
    ha = hashlib.md5(ASSET_AUTH_KEY.encode('utf-8'))
    ha.update(bytes("%s|%f" % (ASSET_AUTH_KEY, timestamp), encoding='utf-8'))
    # ha.update(bytes("%s|%f" % (ASSET_AUTH_KEY, timestamp), ))
    result = ha.hexdigest()
    # 拿到加密后的字符串,用一样的key,时间 加密 得到的一定的一样的结果
    print(result, encrypt,"前面是服务器加密的值,后面是发送过来的值")
    if encrypt != result:
        return False

    exist = False
    del_keys = []
    print(ENCRYPT_LIST,"开始")
    for k, v in enumerate(ENCRYPT_LIST):
        # print(k, v)
        m = v['time']
        n = v['encrypt']
        # 如果里面有小于当前时间2秒的,即超时的
        if m < limit_timestamp:
            del_keys.append(k)
            print(k,"删除的k")
            continue
            # 如果列表里面已经有发过来的值
        if n == encrypt:
            exist = True
    # 删除所有超时的,重复的
    for k in del_keys:
        del ENCRYPT_LIST[k]

    if exist:
        return False
    ENCRYPT_LIST.append({'encrypt': encrypt, 'time': timestamp})
    print(ENCRYPT_LIST,"奇怪的列表")
    return True


def api_auth(func):
    def inner(request, *args, **kwargs):
        if not api_auth_method(request):
            return JsonResponse({'code': 1001, 'message': 'API授权失败'}, json_dumps_params={'ensure_ascii': False})
        return func(request, *args, **kwargs)

    return inner