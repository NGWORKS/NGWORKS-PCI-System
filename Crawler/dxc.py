"""
@author: NGWORKS-夏姬八彻
@contact: wl@ngworks.com
@version: 0.a1
@file: dxc.py
@time: 2020/12/12   22:39
@detail: 用来实现多账号多线程爬取。
"""
from concurrent.futures import Future
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor
from active import *
from fuc import *

did = [464473959712225496,464490332131821793,464503504793433297]
#创建线程池
pool = ThreadPoolExecutor(max_workers=10)
#建立cookie池
cookie = BCookies()
#创建进程池
#pool = ProcessPoolExecutor(max_workers=5)

for i in did:
    fut = pool.submit(get_new_dynamic(i,cookie))
