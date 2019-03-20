# -*- coding:utf-8 -*-
"""
json存入elasticsearch
"""
import os
import sys
from elasticsearch import Elasticsearch


reload(sys)

settings = {"elsticsearch_nodes": ['192.168.1.135:29200']}
es_client = None
region_dict = {}
es_dict = {}


def get_es_client():
    pid = os.getpid()
    if pid in es_dict:
        return es_dict[pid]
    else:
        es_client = Elasticsearch(
            settings['elsticsearch_nodes'],
            sniff_on_start=True,
            sniff_on_connection_fail=True,
            sniffer_timeout=60,
            maxsize=10
        )
        es_dict[pid] = es_client
        return es_client
