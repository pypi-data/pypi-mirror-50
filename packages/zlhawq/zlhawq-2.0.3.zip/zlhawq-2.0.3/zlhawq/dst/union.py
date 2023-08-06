from lmf.dbv2 import db_command ,db_query
from lmf.bigdata import pg2csv
import sys 
import os 
import time 
from zlhawq.dst import algo,bid,bid_bridge 

from zlhawq.dst.api import add_quyu

def add_quyu(quyu,tag='all'):

    bid.api.add_quyu(quyu,tag)

    bid_bridge.add_quyu(quyu,tag)

    algo.api.add_quyu(quyu)



