#-*- coding=utf-8 -*-
import redis

class OPRedis(object):

    def __init__(self):
        if not hasattr(OPRedis, 'pool'):
            OPRedis.init_redis_pool()  #创建redis连接

    @staticmethod
    def init_redis_pool():
        OPRedis.pool = redis.ConnectionPool(host='localhost', password='', port=6379, db=0)

    def get_redis_conn(self):
        return redis.Redis(connection_pool=OPRedis.pool)