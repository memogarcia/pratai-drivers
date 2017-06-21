# -*- coding: utf-8 -*-

"""
drivers.cluster
~~~~~~~~~~~~~~~
This module allows the scheduler to announce the joining and leaving of the
cluster.
"""
import logging

from datetime import datetime

from elasticsearch import Elasticsearch
from elasticsearch import TransportError

from log import prepare_log
prepare_log()
logging.getLogger('pratai-driver')


es = Elasticsearch(hosts=['127.0.0.1'])


def join(daemon_id, daemon_type):
    """Join the scheduler to the cluster.
    """
    doc = {
        "daemon_type": daemon_type,
        "daemon_id": daemon_id,
        "joined_at": datetime.now(),
        "status": "running"
    }
    try:
        res = es.index(index='pratai',
                       doc_type='daemon',
                       body=doc,
                       id=daemon_id)

        es.indices.refresh(index='pratai')
    except TransportError as error:
        logging.error(error)
        raise
    return res['created']


def leave(daemon_id):
    """Announce the scheduler is leaving.
    """
    try:
        return es.delete(index='pratai', doc_type='daemon', id=daemon_id)
    except TransportError as error:
        logging.error(error)
        raise
