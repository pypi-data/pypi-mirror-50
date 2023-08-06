from lmf.dbv2 import db_command ,db_query
from lmf.bigdata import pg2csv
import sys 
import os 
import time 
from zlhawq.dst import algo,bid,bid_bridge 

from zlhawq.dst import api
def add_quyu(quyu,tag='all'):

    bid.api.add_quyu(quyu,tag)

    bid_bridge.add_quyu(quyu,tag)

    algo.api.add_quyu(quyu)

    api.add_quyu(quyu)



def restart_quyu(quyu):

    bid.api.restart_quyu(quyu)

    id_bridge.restart_quyu(quyu)

    algo.api.restart_quyu(quyu)

    api.restart_quyu(quyu)