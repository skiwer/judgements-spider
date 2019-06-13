#-*- coding=utf-8 -*-
from redis_util import OPRedis
import math
import hashlib

class TaskManager:
    page_size = 10
    def __init__(self):
        op_redis = OPRedis()
        self.redis_conn = op_redis.get_redis_conn()

    #获取所有未完成任务
    def get_all_undo_tasks(self):
        list = []
        keywords = self.redis_conn.hkeys('spider-keyword-task-mp')
        for k in keywords:
            undo_pages = self.redis_conn.smembers('spider-undo-pages_' + self.get_md5(k))
            for p in undo_pages:
                list.append((k.decode('utf-8'), int(p)))
        return list

    def task_begin(self, keyword, page):
        md5 = self.get_md5(keyword.encode('utf-8'))
        self.redis_conn.srem('spider-undo-pages_' + md5, page)
        self.redis_conn.sadd('spider-running-pages_' + md5, page)

    def task_end(self, keyword, page):
        md5 = self.get_md5(keyword.encode('utf-8'))
        self.redis_conn.srem('spider-running-pages_' + md5, page)

    def task_failed(self, keyword, page):
        md5 = self.get_md5(keyword.encode('utf-8'))
        self.redis_conn.srem('spider-running-pages_' + md5, page)
        self.redis_conn.sadd('spider-undo-pages_' + md5, page)

    def get_md5(self, s):
        m2 = hashlib.md5()
        m2.update(s)
        return m2.hexdigest()

    #最开始的初始化
    def initialize(self, tasks):
        for k,v in tasks.items():
            pages = math.ceil(v/self.page_size)
            self.redis_conn.hset('spider-keyword-task-mp', k, v)
            for i in range(pages):
                self.redis_conn.sadd('spider-undo-pages_' + self.get_md5(k.encode('utf-8')), i)