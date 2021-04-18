#!/usr/bin/env pyhton3
# -*- coding:utf-8 -*-

#a golden spliter for stock analyze

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

def get_daily_data(code):
    "获取对应股票的历史数据"
    #df = ts.get_hist_data(code,start='2020-01-01',end='2021-03-11')  #获取指定股票数据，不复权
    df = ts.get_k_data(code,start='2020-01-01',end='2021-03-30',autype='qfq') #获取指定股票数据，前复权
    #print(df)
    engine = create_engine('mysql+pymysql://huangqian:huangqian@localhost/Stock')
    df['code'] = code
    df.to_sql('daily_data',engine,if_exists='append')  #使用mysql保存方式

def ConnectSQL():
    "连接数据库，返回数据库指针"
    conn = pymysql.connect(host='localhost',port=3306,user='huangqian',passwd='huangqian',db='Stock',cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
    return cur

def get_lowest_point(code):
    """获取股票的最低价和对应日期，返回 lowpoint-低价，date-对应的日期
    """
    sql = "SELECT low,date FROM daily_data WHERE code = %s AND low = (SELECT MIN(low) FROM daily_data WHERE code = %s);" % (code,code)
    #'SELECT low,date FROM daily_data WHERE low=30.16;'
    cur = ConnectSQL()
    cur.execute(sql)
    result = cur.fetchone()
    lowpoint = result['low']
    date = result['date']
    #print("Lowpoint is %s at day %s" % (lowpoint,date))
    return lowpoint,date

def get_highest_point(code):
    "获取股票的最低价和对应日期，返回 highpoint-高价，date-对应的日期"
    sql = "SELECT high,date FROM daily_data WHERE code = %s AND high = (SELECT MAX(high) FROM daily_data WHERE code = %s);" % (code,code)
    #'SELECT low,date FROM daily_data WHERE low=30.16;'
    cur = ConnectSQL()
    cur.execute(sql)
    result = cur.fetchone()
    highpoint = result['high']
    date = result['date']
    #print("Highpoint is %s at day %s" % (highpoint,date))
    return highpoint,date

def get_golden_price(highpoint,lowpoint):
    "获取股票的黄金分割值，返回五个黄金分割点，分别为23.6% 38.2% 50% 61.8% 76.4%"
    ndigit = 2 #设置小数点位数
    P1 = round((highpoint-lowpoint)*0.236+lowpoint,ndigit)
    P2 = round((highpoint-lowpoint)*0.382+lowpoint,ndigit)
    P3 = round((highpoint-lowpoint)*0.500+lowpoint,ndigit)
    P4 = round((highpoint-lowpoint)*0.618+lowpoint,ndigit)
    P5 = round((highpoint-lowpoint)*0.764+lowpoint,ndigit)
    #print(P1,P2,P3,P4,P5)
    return P1,P2,P3,P4,P5

def CheckHits(price,mark):
    if abs(mark-price)/mark < 0.001:
        return True
    else:
        return False

def Scan(code,mode='single'):
    """扫描区间内股价命中黄金分隔线的次数，返回命中次数和对应股票代码
    
    Parameters:

        code:string    股票代码

        mode:string    扫描模式 single-默认，输出黄金分割高低点和对应的日期  all-不输出详细高低点

    Return:
        hits:int       命中黄金分割次数

        code:string    对应的股票代码
    """
    cur = ConnectSQL()
    sql = "SELECT high,open,close,low,date FROM daily_data WHERE code = %s" % (code)
    cur.execute(sql)
    result = cur.fetchall()
    hits = 0
    lowpoint,low_date = get_lowest_point(code)
    hipoint,hi_date = get_highest_point(code)
    golden_price = get_golden_price(hipoint,lowpoint)
    if mode =='all':
        for i in result:
            for price in ('high','low','open','close'):
                for mark in golden_price:
                    if CheckHits(i[price],mark) == True :
                        hits += 1
                        #print("Hit day in %s ,price is %s,mark is %s" % (i['date'],price,mark))
        return hits,code 

    else :
        for i in result:
            for price in ('high','low','open','close'):
                for mark in golden_price:
                    if CheckHits(i[price],mark) == True :
                        hits += 1
        print("Lowpoint is %s at day %s" % (lowpoint,low_date))
        print("Highpoint is %s at day %s" % (hipoint,hi_date))
        return hits,code


def fetchdata():#抓取数据
    cur = ConnectSQL()
    sql = "SELECT code FROM hs300 limit 10"
    cur.execute(sql)
    result = cur.fetchall()
    for i in result:
        get_daily_data(i['code'])
        print("Fetch data for %s success." % (i['code']))

def main():
    cur = ConnectSQL()
    sql = "SELECT code FROM hs300 limit 5"
    cur.execute(sql)
    result = cur.fetchall()
    sdict = []
    for i in result:
        hits,code = Scan(i['code'],mode='all')
        sdict.append((code,hits))
    print(sdict)
    sdict = sorted(sdict,key=lambda x: x[1])
    print(sdict)
    print(sdict[-2:-1])

main()

