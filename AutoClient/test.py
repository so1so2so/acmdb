# from concurrent.futures import ThreadPoolExecutor
# from concurrent.futures import ProcessPoolExecutor
# import time
# def task(arg):
#     print(arg)
#     time.sleep(1)
#
# # pool = ProcessPoolExecutor(5)
# pool = ThreadPoolExecutor(5)
#
# for i in range(50):
#     pool.submit(task,i)


import json
from datetime import date
from datetime import datetime


# class JsonCustomEncoder(json.JSONEncoder):
#     def default(self, field):
#         if isinstance(field, datetime):
#             return field.strftime('%Y-%m-%d %H')
#         elif isinstance(field, date):
#             return field.strftime('%Y-%m-%d')
#         elif isinstance(field, Response):
#             return field.__dict__
#         else:
#             return json.JSONEncoder.default(self, field)
#
# class Response(object):
#     def __init__(self):
#         self.status =True
#         self.data = "asdf"
# data = {
#     'k1': 123,
#     'k2': datetime.now(),
#     'k3': Response()
# }
# ds = json.dumps(data, cls=JsonCustomEncoder)
# print(ds)
# class test1():
#     def __init__(self, a):
#         self.a = a
#
#     def get_a_type(self):
#         return self.get_a_nou_num()
#
#     @classmethod
#     def get_a_num(cls):
#         return cls
#
#     @staticmethod
#     def get_a_nou_num():
#         return "aaa"
#
#
# a = test1(a=10)
# print(a.get_a_type())
# print()
# print(a.get_a_nou_num())

from config import settings
import hashlib,time
from src.checkpython_version import check
class AutoBase(object):
    def __init__(self):
        self.asset_api = settings.ASSET_API
        self.key = settings.KEY
        self.key_name = settings.AUTH_KEY_NAME

    def auth_key(self):
        """
        接口认证
        :return:
        """
        ha = hashlib.md5(self.key.encode('utf-8'))
        time_span = time.time()
        # print(sys.version_info>2.7)
        if check():
            ha.update(bytes("%s|%f" % (self.key, time_span), encoding='utf-8'))
        else:
            ha.update(bytes("%s|%f" % (self.key, time_span), ))
        encryption = ha.hexdigest()
        result = "%s|%f" % (encryption, time_span)
        return {self.key_name: result}

a=AutoBase()
a.auth_key()