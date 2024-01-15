# -*- coding: utf-8 -*-
import random
import time

import redis

REDIS_CONFIG = {
    'host': "127.0.0.1",
    'port': 6379,
    'db': 0,
    'password': None
}
#连接池重要参数，最多允许多少连接存在
REDIS_POOL_CONFIG = {
    'max_connections': 10
}
REDIS_POOL_CONFIG.update(REDIS_CONFIG)


def t0():
    # r = redis.Redis(**REDIS_CONFIG)  # 获取连接
    with redis.Redis(**REDIS_CONFIG) as r:
        for k in range(100):
            rr = r.set(f'u:{k:04d}', k)
            print(k, rr, type(rr))
        print("-" * 100)
        print(r.get('u:0058'))
        print(str(r.get('u:0058'), encoding='utf-8'))
    # r.close()  # 关闭连接


def t1():
    pool = redis.ConnectionPool(**REDIS_POOL_CONFIG)
    with redis.Redis(connection_pool=pool) as r:
        # String类型数据的操作
        o = r.set(
            name='u_name',  # key字符串
            value='小明',  # 保存的value字符串
            ex=None,  # 设定过期时间：单位秒，和参数px冲突
            px=None,  # 设定过期时间：单位毫秒，和参数ex冲突
            nx=False,  # 当nx为True的时候，表示仅name(key)在redis中有不存在数据的时候，进行插入操作；和参数xx不能同时为True
            xx=False  # 当xx为True的时候，表示仅name(key)在redis中有存在数据的时候，进行更新操作；和参数nx不能同时为True
        )
        print(o)
    pool.close()


def t2():
    pool = redis.ConnectionPool(**REDIS_POOL_CONFIG)
    with redis.Redis(connection_pool=pool) as r:
        st = time.time()
        n = 10000
        for k in range(n):
            key = f'u:{k:04d}'
            r.set(key, f"name_{n}_{k}")
            r.expire(key, 100)#设置过期时间
        et = time.time()
        print(f"总耗时:{et - st}")
    pool.close()

#管道流操作
def t3():
    pool = redis.ConnectionPool(**REDIS_POOL_CONFIG)
    with redis.Redis(connection_pool=pool) as r:
        st = time.time()
        n = 10000
        _pipeline = r.pipeline()
        for k in range(n):
            key = f'u:{k:04d}'
            _pipeline.set(key, f"name_{n}_{k}")
            _pipeline.expire(key, 100 + random.randint(0, 50))
        _pipeline.execute()  # 提交服务器，等待返回
        et = time.time()
        print(f"总耗时:{et - st}")
    pool.close()


def t4():
    pool = redis.ConnectionPool(**REDIS_POOL_CONFIG)
    with redis.Redis(connection_pool=pool) as r:
        _pipeline = r.pipeline()
        _pipeline.set('name', f"小明")
        _pipeline.smembers('names2')  # 获取set数据集
        _pipeline.hgetall('user:1001')
        _pipeline.hmget('user:1002', ['name', 'age'])
        _result = _pipeline.execute()  # 提交服务器，等待返回
        print(_result)
    pool.close()


if __name__ == '__main__':
    t2()
