#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xytool.config import Config
from xytool.common.xylog import *
from functools import wraps
import pymysql
db_type = Config().get_config("Database-config","type")
host = Config().get_config("Database-config","host")
user = Config().get_config("Database-config","user")
password = Config().get_config("Database-config","password")
db = Config().get_config("Database-config","db")
charset = Config().get_config("Database-config","charset")



def func_database(f):
    """
    内建分析器
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            conn = pymysql.connect(host=host, user=user, passwd=password, db=db)
            cur = conn.cursor()#游标
            successlog("connect to database successful!")

            f(cur=cur,*args, **kwargs)
            
            cur.close()
            conn.close()
        except BaseException as error:
            faillog("connect to database failed!")
        finally:
            successlog("colse database successful!")
    return wrapper