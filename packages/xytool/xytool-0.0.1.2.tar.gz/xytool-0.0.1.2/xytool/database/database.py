#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xytool.config import Config
from xytool.common.xylog import *
from database_block import func_database
import pymysql

@func_database
def get_all_ip(cur):
    try:
        cur.execute("SELECT * FROM nike_ippool")
        for r in cur:
            print(r,'\n')
    except BaseException as error:
        print(format(error))

def main():
    get_all_ip()

if __name__ == '__main__':
    main()
    