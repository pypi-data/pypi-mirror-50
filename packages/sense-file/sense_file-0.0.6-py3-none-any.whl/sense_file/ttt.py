#!/usr/bin/env python
# -*- coding: utf-8 -*-

############################################################
#
# Copyright (C) 2019 SenseDeal AI, Inc. All Rights Reserved
#
############################################################

"""
File: server.py
Author: liuguangbin
Editor: liuguangbin
E-mail:
Last modified: 2019-08-12 16:15
Description:
"""

import os
import re
import sys
import grpc
import json
import time

from rpc import token_ner_pb2, token_ner_pb2_grpc

from concurrent import futures
from configobj import ConfigObj

from lib.InferenceSolverOfNews import InferenceSolver
from lib.news_token_ner import TokenNER
from sense_core import config, log_init_config
from sense_file.load_file import log_alg_exec

log_init_config('token_ner_new', config('log_path'))
os.environ["CUDA_VISIBLE_DEVICES"] = ""


@log_alg_exec
def serve(mode):
    _confobj = ConfigObj('/conf/all.ini', encoding='utf8')
    _conf = _confobj[mode]
    _host = _conf['Alg']['news_token_ner']['node_host']
    _port = _conf['Alg']['news_token_ner']['node_port']
    alg_version = _conf['Alg']['news_token_ner']['version']

    _model_base = _conf['Alg']['news_token_ner']['modelpath']
    _embedding_path = _model_base

    ckpt_dirs = []
    data_dirs = []

    for file_name in os.listdir(_model_base):
        model_path = os.path.join(_model_base, file_name)
        if os.path.isdir(model_path) and 'seg' not in model_path:
            ckpt_dirs.append(os.path.join(model_path, 'checkpoints'))
            data_dirs.append(os.path.join(model_path, 'data'))

    _workers = int(_conf['Alg']['news_token_ner']['workers'])
    _solver = InferenceSolver(
        os.path.join(_model_base, 'seg_data/'),
        os.path.join(_model_base, 'seg_checkpoint/'),
        data_dirs,
        ckpt_dirs,
        _embedding_path
    )
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=_workers))
    token_ner_pb2_grpc.add_TokenNERServicer_to_server(TokenNER(_solver, alg_version), server)
    server.add_insecure_port(_host + ':' + _port)
    server.start()
    _ONE_DAY_IN_SECONDS = 60 * 60 * 24
    print(_host,_port , _model_base)
    while True:
        time.sleep(_ONE_DAY_IN_SECONDS)

if __name__ == '__main__':
    mode = str(sys.argv[1])
    serve(mode)