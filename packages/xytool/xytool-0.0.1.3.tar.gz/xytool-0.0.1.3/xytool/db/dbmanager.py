#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xytool.config import Config
from xytool.common.xylog import *
from db.dbmanager import func_database
import pymysql

@func_database
def get_all_ip(cur):
    try:
        cur.execute("SELECT * FROM nike_ippool")
        ips = []
        for r in cur:
            ips.append(r)
        return ips
    except BaseException as error:
        faillog(format(error))

def main():
    get_all_ip()

if __name__ == '__main__':
    main()
    