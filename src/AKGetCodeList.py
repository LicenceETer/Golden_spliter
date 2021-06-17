#!/usr/bin/env pyhton3
# -*- coding:utf-8 -*-

#Get stock data from akshare

__author__ = "LicenceETer Huang"


import os
import akshare as ak
from sqlalchemy import create_engine
import pymysql

def AKgetbasic():
    stock_zh_a_spot_df = ak.stock_zh_a_spot()
    engine = create_engine('mysql+pymysql://huangqian:huangqian@localhost/Stock?charset=utf8MB4')
    stock_zh_a_spot_df.to_sql('AKbasic',engine,if_exists='append')

def AKGetdata(code,start_date,end_date):
    try:
        df = ak.stock_zh_a_daily(code, start_date, end_date, adjust="qfq")
    except:
        pass
    else:
        engine = create_engine('mysql+pymysql://huangqian:huangqian@localhost/Stock')
        df['code'] = code
        df.to_sql('daily_data',engine,if_exists='append')

def ConnectSQL():
    "连接数据库，返回数据库指针"
    conn = pymysql.connect(host='localhost',port=3306,user='huangqian',passwd='huangqian',db='Stock',cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
    return cur 
 
def fetchdata():#抓取数据
    cur = ConnectSQL()
    sql = "SELECT code FROM AKbasic"
    cur.execute(sql)
    result = cur.fetchall()
    for i in result:
        AKGetdata(i['code'],'20200101','20210616')
        print("Fetch data for %s success." % (i['code']))

def main():
    #AKgetbasic()
    #AKGetdata('sz000063','20200303','20210616')
    fetchdata()

if __name__ == '__main__':
    main()


