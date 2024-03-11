# -*- encoding: utf-8 -*-
import os


bind = '0.0.0.0:8080'
preload_app = True
worker_tmp_dir = '/dev/shm'
workers = 4
loglevel = os.getenv('LOG_LEVEL', 'INFO')
capture_output = True
enable_stdio_inheritance = True
