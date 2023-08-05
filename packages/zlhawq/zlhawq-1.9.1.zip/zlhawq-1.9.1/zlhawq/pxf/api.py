from lmf.dbv2 import db_command ,db_query
from lmf.bigdata import pg2csv
import sys 
import os 

from zlhawq.pxf.core import add_quyu_tmp,restart_quyu_tmp
import traceback

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<阿里云<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def get_conp_aliyun(quyu):
    conp=['postgres','since2015','192.168.4.201','postgres','public']
    sql="select usr,password,host,db,schema from cfg where quyu='%s' "%quyu
    df=db_query(sql,dbtype="postgresql",conp=conp)
    conp=df.values[0].tolist()
    return conp

def add_quyu_aliyun(quyu,tag):
    conp_pg=get_conp_aliyun(quyu)
    conp_hawq=['gpadmin','since2015','192.168.4.179','base_db','public']
    pxf_ip='192.168.4.183'
    add_quyu_tmp(quyu,conp_pg,conp_hawq,pxf_ip,tag)

def restart_quyu_aliyun(quyu,tag):
    conp_pg=get_conp_aliyun(quyu)
    conp_hawq=['gpadmin','since2015','192.168.4.179','base_db','public']
    pxf_ip='192.168.4.183'
    restart_quyu_tmp(quyu,conp_pg,conp_hawq,pxf_ip,tag)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>阿里云>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<昆明<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def get_conp_kunming(quyu):
    conp=['postgres','since2015','192.168.169.89','postgres','public']
    sql="select usr,password,host,db,schema from cfg where quyu='%s' "%quyu
    df=db_query(sql,dbtype="postgresql",conp=conp)
    conp=df.values[0].tolist()
    return conp

def add_quyu_kunming(quyu,tag):
    conp_pg=get_conp_kunming(quyu)
    conp_hawq=['gpadmin','since2015','192.168.169.91','base_db','public']
    pxf_ip='192.168.169.90'
    add_quyu_tmp(quyu,conp_pg,conp_hawq,pxf_ip,tag)

def restart_quyu_kunming(quyu,tag):
    conp_pg=get_conp_aliyun(quyu)
    conp_hawq=['gpadmin','since2015','192.168.169.91','base_db','public']
    pxf_ip='192.168.169.90'
    restart_quyu_tmp(quyu,conp_pg,conp_hawq,pxf_ip,tag)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>昆明>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>







def add_quyu(quyu,tag='all',loc='aliyun'):
    if loc=='aliyun':
        add_quyu_aliyun(quyu,tag)
    elif loc=='kunming':
        add_quyu_kunming(quyu,tag)

def restart_quyu(quyu,tag='all',loc='aliyun'):
    if loc=='aliyun':
        restart_quyu_aliyun(quyu,tag)
    elif loc=='kunming':
        add_quyu_kunming(quyu,tag)
