# -*-coding: utf-8-*-
import multiprocessing

import gevent.monkey

gevent.monkey.patch_all()

# 并行工作进程数
workers = multiprocessing.cpu_count()
# 每个进程的开启线程
threads = 2
# 监听端口 8001
bind = '0.0.0.0:8889'
# 设置守护进程,将进程交给supervisor管理
daemon = 'false'
# 开启debug模式
debug = True
# 工作模式协程
worker_class = 'gevent'
# 设置最大并发量
worker_connections = 2000
# 设置进程文件目录
pidfile = '{{gunicorn_pidfile}}/{{project_name}}_gunicorn.pid'
errorlog = '{{gunicorn_errorlog}}/{{project_name}}_gunicorn.err'
