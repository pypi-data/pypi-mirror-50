
from lmf.dbv2 import db_command ,db_query
from lmf.bigdata import pg2csv
import sys 
import os 
import time 
import traceback

def est_gg_meta(conp):
    user,password,ip,db,schema=conp
    sql="""
    CREATE TABLE dst.gg_meta (
    html_key bigint,
    guid text,
    gg_name text,
    href text,
    fabu_time timestamp,
    ggtype text,
    jytype text,
    diqu text,
    quyu text,
    info text,
    create_time timestamp,
    xzqh text,
    ts_title text,
    bd_key bigint,
    person text,
    price text,

    zhaobiaoren text ,

    zhongbiaoren  text ,

    zbdl   text ,

    zhongbiaojia float ,

    kzj  float ,

    xmmc  text ,

    xmjl text ,

    xmjl_zsbh text ,



    xmdz  text , 

    zbfs text ,

    xmbh  text ,

    mine_info text 
    )
    partition by list(quyu)
      (partition hunan_huaihua_gcjs values('hunan_huaihua_gcjs'),
        partition hunan_changde_zfcg values('hunan_changde_zfcg')
        )

    """
    db_command(sql,dbtype='postgresql',conp=conp)



#为 gg表新增\删除分区
def add_partition_gg_meta(quyu,conp):
    user,password,ip,db,schema=conp
    sql="alter table %s.gg_meta add partition %s values('%s')"%(schema,quyu,quyu)
    db_command(sql,dbtype='postgresql',conp=conp)

def drop_partition_gg_meta(quyu,conp):
    user,password,ip,db,schema=conp
    sql="alter table %s.gg_meta drop partition for('%s')"%(schema,quyu)
    db_command(sql,dbtype='postgresql',conp=conp)



#通用anhui_chaohu_ggzy
def update_gg_meta_prt1(quyu,conp):

    user,password,ip,db,schema=conp

    sql="""

    insert into dst.gg_meta_1_prt_anhui_chaohu_ggzy(html_key    ,guid   ,gg_name,   href    ,fabu_time, ggtype  ,jytype,    diqu    ,quyu,  info
    ,   create_time ,xzqh   ,ts_title   
    ,bd_key ,person ,price  ,zhongbiaoren   ,zhaobiaoren    ,zbdl   ,zhongbiaojia   ,kzj    ,xmmc   ,xmjl   ,xmjl_zsbh  ,xmdz   
    ,zbfs   ,xmbh   ,mine_info)
    with a as (select html_key, guid,   gg_name,    href,   fabu_time,  ggtype, jytype, diqu,   quyu,   info,   create_time 
    ,dst.parse_diqu_code(quyu,page) as xzqh,dst.title2ts(gg_name) as ts_title
    from src.t_gg as t1  where quyu='anhui_chaohu_ggzy' 

    and not exists(select 1 from dst.gg_meta_1_prt_anhui_chaohu_ggzy  as t2 where t2.html_key=t1.html_key )
    )

    ,b as (select html_key, dst.kv(minfo) as info  from algo.m_gg where  quyu='anhui_chaohu_ggzy')

    ,c as (select html_key
    ,algo.get_js_v(info,'zhongbiaoren') as zhongbiaoren 
    ,algo.get_js_v(info,'zhaobiaoren') as zhaobiaoren 
    ,algo.get_js_v(info,'zbdl') as zbdl
    ,algo.get_js_v(info,'zhongbiaojia') as zhongbiaojia
    ,algo.get_js_v(info,'kzj') as kzj
    ,algo.get_js_v(info,'xmmc') as xmmc
    ,algo.get_js_v(info,'xmjl') as xmjl
    ,algo.get_js_v(info,'xmdz') as xmdz
    ,algo.get_js_v(info,'zbfs') as zbfs
    ,algo.get_js_v(info,'xmbh') as xmbh
     from b )
    ,d as (
    select a.*
    ,null::bigint bd_key    
    ,null::text person  
    ,null::float  price
    ,zhongbiaoren 
    ,zhaobiaoren
    ,zbdl
    ,zhongbiaojia::float     zhongbiaojia
    ,kzj::float kzj     
    ,xmmc   
    ,xmjl   
    ,null as xmjl_zsbh  
    ,xmdz   
    ,zbfs   
    ,xmbh   
    ,null::text  mine_info
     from a ,c where a.html_key=c.html_key )
    select * from d  
    
    """
    sql=sql.replace('anhui_chaohu_ggzy',quyu)
    db_command(sql,dbtype='postgresql',conp=conp)
