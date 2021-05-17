#!/usr/bin/env pyhton3
# -*- coding:utf-8 -*-

#For golden spliter fetch code list 

__author__ = "LicenceETer Huang"

import os
import tushare as ts
from sqlalchemy import create_engine
import pymysql

ts.set_token('99684bcfdd007d62f1993d6fc226dda2bf4439104d469ac464360a13')  #设置个人token
pro = ts.pro_api()

def get_hs300s():
    "获取中证500股票清单"
    df = ts.get_hs300s()
    engine = create_engine('mysql+pymysql://huangqian:huangqian@localhost/Stock?charset=utf8MB4')
    print(df)
    df.to_sql('hs300',engine,if_exists='append')

def get_zz500s():
    "获取中证500股票清单"
    df = ts.get_zz500s()
    engine = create_engine('mysql+pymysql://huangqian:huangqian@localhost/Stock?charset=utf8MB4')
    print(df)
    df.to_sql('zz500',engine,if_exists='append')

def get_stocks():
    "获取所有股票清单"
    #df = ts.get_stock_basics()
    df = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    engine = create_engine('mysql+pymysql://huangqian:huangqian@localhost/Stock?charset=utf8MB4')
    print(df)
    df.to_sql('stock_basics',engine,if_exists='append')