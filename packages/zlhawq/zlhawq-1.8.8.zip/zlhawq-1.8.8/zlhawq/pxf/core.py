

from lmf.dbv2 import db_command ,db_query
from lmf.bigdata import pg2csv
import sys 
import os 
from fabric import Connection

import traceback
def est_t_gg(conp):
    user,password,ip,db,schema=conp
    sql="""
    create table %s.t_gg (
    html_key  serial,
    guid text not null ,
    gg_name text not null ,
    href text  not null ,

    fabu_time timestamp(0) not null ,

    ggtype text not null ,
    jytype text  ,
    diqu text,
    quyu text not null,
    info text,
    page text ,
    create_time timestamp(0))
    partition by list(quyu)
    (partition hunan_huaihua_gcjs values('hunan_huaihua_gcjs'),
    partition hunan_changde_zfcg values('hunan_changde_zfcg')
    )

    """%schema 
    db_command(sql,dbtype='postgresql',conp=conp)

#为 gg表新增\删除分区
def add_partition_t_gg(quyu,conp):
    user,password,ip,db,schema=conp
    sql="alter table src.t_gg add partition %s values('%s')"%(quyu,quyu)
    db_command(sql,dbtype='postgresql',conp=conp)

def drop_partition_t_gg(quyu,conp):
    user,password,ip,db,schema=conp
    sql="alter table src.t_gg drop partition for('%s')"%(quyu)
    db_command(sql,dbtype='postgresql',conp=conp)


def est_t_gg_cdc(quyu,conp_pg,conp_hawq,pxf_ip):
    db,schema=conp_pg[3],quyu
    # sql="select count(*) from %s.t_gg_hawq"%quyu
    # row_count=db_query(sql,dbtype="postgresql",conp=conp_pg).iat[0,0]+1
    # print("拟导出总量:%d"%row_count)
    # row_count=max(row_count,500000)
    row_count=1000000
    sql="""drop external table if exists cdc.t_gg_cdc_hunan_huaihua_gcjs;
    create  external table cdc.t_gg_cdc_hunan_huaihua_gcjs(guid text,gg_name text ,fabu_time text,href  text  ,ggtype text,jytype text
     , diqu text,quyu text  ,info text,page text ) 
    LOCATION ('pxf://192.168.4.183:51200/hunan_huaihua_gcjs.t_gg_hawq?PROFILE=JDBC&JDBC_DRIVER=org.postgresql.Driver&DB_URL=jdbc:postgresql://192.168.4.199:5432/hunan&USER=postgres&PASS=since2015&PARTITION_BY=rowid:int&RANGE=1:1000000&INTERVAL=10000')
    FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    """
    sql=sql.replace('192.168.4.183',pxf_ip)
    sql=sql.replace('hunan_huaihua_gcjs',quyu)
    sql=sql.replace('192.168.4.199',conp_pg[2])
    sql=sql.replace('1000000',str(row_count))
    sql=sql.replace("""USER=postgres""","""USER=%s"""%conp_pg[0])
    sql=sql.replace("""PASS=since2015""","""PASS=%s"""%conp_pg[1])
    sql=sql.replace(""":5432/hunan""",""":5432/%s"""%db)
    print(sql[:100])
    db_command(sql,dbtype="postgresql",conp=conp_hawq)

def drop_t_gg_cdc(quyu,conp_hawq):
    sql="""drop external table cdc.t_gg_cdc_%s; """%(quyu)
    db_command(sql,dbtype="postgresql",conp=conp)



#将pg数据导入到文件系统下的csv
def est_funs(conp):
    sql="""
create extension if not exists pgcrypto;
create extension if not exists plpython3u ;


create or replace function "public".t_time (t1 text ) returns timestamp(0)

as $$

import re
import time

if t1 is None:return None 



a=re.findall('([1-9][0-9]{3})[\-\./\\\\年]([0-9]{1,2})[\-\./\\\\月]([0-9]{1,2}) ([0-9]{2}):([0-9]{2}):([0-9]{2})',t1)

if a!=[]:
    x='-'.join(a[0][:3]) +' '+':'.join(a[0][3:])
    return x


a=re.findall('([1-9][0-9]{3})[\-\./\\\\年]([0-9]{1,2})[\-\./\\\\月]([0-9]{1,2})',t1)
if a!=[]:
    x='-'.join(a[0])
    return x


a=re.findall('^([0-2][0-9])[\-\./\\\\年]([0-9]{1,2})[\-\./\\\\月]([0-9]{1,2})',t1)
if a!=[]:
    x='20'+'-'.join(a[0])
    return x


a=re.findall('^20[0-9]{2}[0-2][0-9][0-3][0-9]',t1)

if a!=[]:
   x=a[0]
   return x

#2018--1-1-

a=re.findall('^(20[0-9]{2})--([0-9]{1,2})-([0-9]{1,2})',t1)

if a!=[]:

         
   x='-'.join([a[0][0],a[0][1] if a[0][1]!='0' else '1' ,a[0][2] if a[0][2]!='0' else '1'])

   
   return x



if ' CST ' in t1:
    try:
       x=time.strptime(t1,'%a %b %d %H:%M:%S CST %Y')
       x=time.strftime('%Y-%m-%d %H:%M:%S',x)
    except:
       x=''
    if x!='':return x


return None 


$$ language plpython3u;


create or replace function  "public".exttime(ggtime text,page text ,quyu text ) returns timestamp(0) 

as $$


from lntime.route import exttime 

time1=exttime(ggtime,page,quyu)

return time1


$$ language plpython3u ;

    """

    conp1=[*conp[:-1],'public']
    db_command(sql,dbtype="postgresql",conp=conp1)


def out_t_gg_all(quyu,conp):
    arr=quyu.split("_")
    sql="drop table if exists %s.t_gg_hawq;"%quyu

    print(sql)
    db_command(sql=sql,dbtype="postgresql",conp=conp)

    sql="""with a as (select distinct on(gg_name,href,quyu)  encode(digest(concat(name,a.href),'md5'),'hex') as guid ,
        name as gg_name,ggstart_time as fabu_time,a.href,ggtype,jytype,diqu,'hunan_huaihua_gcjs' as quyu,info
        ,page
        from hunan_huaihua_gcjs.gg as a ,hunan_huaihua_gcjs.gg_html  as b where a.href=b.href  and b.page!='None'  )
    select row_number() over() as rowid,*

    into hunan_huaihua_gcjs.t_gg_hawq
     from a 
        """
    sql=sql.replace('hunan_huaihua_gcjs',quyu)
    print(sql)
    db_command(sql=sql,dbtype="postgresql",conp=conp)



def out_t_gg_cdc(quyu,conp):

    arr=quyu.split("_")
    s1,s2=arr[0],quyu
    db,shema=arr[0],'_'.join(arr[1:])
    sql="drop table if exists %s.t_gg_hawq;"%quyu

    print(sql)
    db_command(sql=sql,dbtype="postgresql",conp=conp)

    sql1="select table_name  from information_schema.tables where table_schema='%s' and table_name ~'.*gg_cdc$'"%(s2)
    df1=db_query(sql=sql1,dbtype="postgresql",conp=conp)

    sqls=["""select name,href,ggstart_time from %s.%s """%(s2,w) for w in df1['table_name']]
    sql=" union all ".join(sqls)

    sql="""with b as(%s)
        , b1 as (
       select name ,href,ggstart_time,ggtype,jytype,diqu,info from %s.gg as a where  exists(select 1 from b where a.name=b.name and 
       a.href=b.href and a.ggstart_time=b.ggstart_time and b.name is not null and b.href is not null and b.ggstart_time is not null ) )
        ,c as(
        select distinct on(gg_name,href,quyu) encode(digest(name||b1.href,'md5'),'hex') as guid ,
        name as gg_name,ggstart_time as fabu_time,b1.href,ggtype,jytype,diqu,'%s' as quyu,info
        ,replace(replace(replace(replace(b.page,'\001',''),'\002',''),'\r',''),'\n','') as page
        from b1 ,%s.gg_html  as b where b1.href=b.href  and b.page!='None' 
        )
    select row_number() over() as rowid,*

    into %s.t_gg_hawq
     from c
     """%(sql,s2,quyu,s2,s2)
    print(sql)
    db_command(sql=sql,dbtype="postgresql",conp=conp)
    #df=db_query(sql=sql,dbtype="postgresql",conp=conp)
    #df.to_csv(path1,sep='\001',quotechar='\002',index=False)






def update_t_gg(quyu,conp_hawq):

    user,password,ip,db,schema=conp_hawq

    sql="""
    insert into src.t_gg(guid,gg_name,fabu_time,href,ggtype,jytype,diqu,quyu,info,create_time,page)
    SELECT 
    distinct on(guid)
    guid,gg_name,cdc.exttime(fabu_time,page,'%s') as fabu_time,href,ggtype,jytype,diqu,quyu,info,now()::timestamp(0) as create_time,page

     FROM cdc.t_gg_cdc_%s a where  gg_name is not null and 
     cdc.exttime(fabu_time,page,'%s') is not null and not exists (select 1 from src.t_gg_1_prt_%s as b where   a.guid=b.guid)  
    
    """%(quyu,quyu,quyu,quyu)

    db_command(sql,dbtype='postgresql',conp=conp_hawq)



def add_quyu_tmp(quyu,conp_pg,conp_hawq,pxf_ip,tag='all'):
    print("t_gg表更新")
    user,password,ip,db,schema=conp_hawq
    print("1、准备创建分区")
    sql="""
    SELECT  partitionname
    FROM pg_partitions
    WHERE tablename='t_gg' and schemaname='src'
    """
    df=db_query(sql,dbtype="postgresql",conp=conp_hawq)
    if quyu in df["partitionname"].values:
        print("%s-partition已经存在"%quyu)

    else:
        print('%s-partition还不存在'%quyu)
        add_partition_t_gg(quyu,conp_hawq)

    print("2、准备创建外部表")


    est_t_gg_cdc(quyu,conp_pg,conp_hawq,pxf_ip)

    print("3、准备待入库的数据")
    
    print("创建函数")

    est_funs(conp_pg)


    if tag=='all':
        out_t_gg_all(quyu,conp_pg)
    else:
        out_t_gg_cdc(quyu,conp_pg)

    print("4、hawq中执行更新、插入语句")

    update_t_gg(quyu,conp_hawq)



def restart_quyu_tmp(quyu,conp_pg,conp_hawq,pxf_ip,tag='all'):
    print("t_gg 一个区域rebuild")
    user,password,ip,db,schema=conp_hawq
    print("1、准备删除分区")
    sql="""
    SELECT  partitionname
    FROM pg_partitions
    WHERE tablename='t_gg' and schemaname='src'
    """
    df=db_query(sql,dbtype="postgresql",conp=conp_hawq)
    if quyu in df["partitionname"].values:
        print("%s-partition已经存在,删之"%quyu)
        drop_partition_t_gg(quyu,conp_hawq)

    else:
        print('%s-partition还不存在'%quyu)

    add_quyu_tmp(quyu,conp_pg,conp_hawq,pxf_ip,'all')
        






#conp=['postgres','since2015','192.168.4.199','hunan','hunan_huaihua_gcjs']
#out_t_gg_cdc('hunan_huaihua_gcjs',conp)

# quyu="anhui_hefei_ggzy"
# conp_pg=['postgres','since2015','192.168.4.198','anhui','anhui_hefei_ggzy']
# conp_hawq=['gpadmin','since2015','192.168.4.179','base_db','public']
# pxf_ip='192.168.4.183'
#est_t_gg_cdc('hunan_huaihua_gcjs',conp_pg,conp_hawq,pxf_ip)

#out_t_gg_all('hunan_huaihua_gcjs',conp_pg)

#update_t_gg('hunan_huaihua_gcjs',conp_hawq)

#add_quyu_tmp(quyu,conp_pg,conp_hawq,pxf_ip,'cdc')