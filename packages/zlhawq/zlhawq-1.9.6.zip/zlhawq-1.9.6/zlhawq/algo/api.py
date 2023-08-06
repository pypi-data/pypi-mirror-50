from lmf.dbv2 import db_command ,db_query
from lmf.bigdata import pg2csv
import sys 
import os 
import time 
from zlhawq.algo.core import add_quyu_tmp,restart_quyu_tmp
import traceback

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<阿里云<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def add_quyu_aliyun(quyu):
    conp_hawq=['gpadmin','since2015','192.168.4.179','base_db','algo']
    add_quyu_tmp(quyu,conp_hawq)

def restart_quyu_aliyun(quyu,tag):
    conp_hawq=['gpadmin','since2015','192.168.4.179','base_db','algo']
    restart_quyu_tmp(quyu,conp_hawq)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>阿里云>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def add_quyu(quyu,loc='aliyun'):
    if loc=='aliyun':
        add_quyu_aliyun(quyu)
    # elif loc=='kunming':
    #     add_quyu_kunming(quyu,tag)

def restart_quyu(quyu,loc='aliyun'):
    if loc=='aliyun':
        restart_quyu_aliyun(quyu)
    # elif loc=='kunming':
    #     add_quyu_kunming(quyu,tag)

