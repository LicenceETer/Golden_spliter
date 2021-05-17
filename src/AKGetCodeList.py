#!/usr/bin/env pyhton3
# -*- coding:utf-8 -*-

#Get stock data from akshare

__author__ = "LicenceETer Huang"

import os
import akshare as ak
from sqlalchemy import create_engine
import pymysql

def Getbasic():
    stock_zh_a_spot_df = ak.stock_zh_a_spot()
    engine = create_engine('mysql+pymysql://huangqian:huangqian@localhost/Stock?charset=utf8MB4')
    stock_zh_a_spot_df.to_sql('AKbasic',engine,if_exists='append')

