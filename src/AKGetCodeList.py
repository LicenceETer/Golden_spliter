#!/usr/bin/env pyhton3
# -*- coding:utf-8 -*-

#Get stock data from akshare

__author__ = "LicenceETer Huang"


import os
import akshare as ak
from sqlalchemy import create_engine
import pymysql

def AKetbasic():
    stock_zh_a_spot_df = ak.stock_zh_a_spot()
    engine = create_engine('mysql+pymysql://huangqian:huangqian@localhost/Stock?charset=utf8MB4')
    stock_zh_a_spot_df.to_sql('AKbasic',engine,if_exists='append')

def AKGetdata(code,start_date,end_date):
    df = ak.stock_zh_a_daily(code, start_date, end_date, adjust="qfq")
    engine = create_engine('mysql+pymysql://huangqian:huangqian@localhost/Stock')
    df['code'] = code
    df.to_sql('daily_data',engine,if_exists='append')  #使用mysql保存方式

def main():
    AKGetdata('sz000063','20200303','20210519')

if __name__ == '__main__':
    main()


