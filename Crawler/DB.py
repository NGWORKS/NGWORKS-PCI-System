"""
@author: NGWORKS-夏姬八彻
@contact: wl@ngworks.com
@version: 0.a1
@file: DB.py
@time: 2020/12/12   21:18
@detail: 数据库操作的上下文管理器。
"""
import sqlite3,traceback,redis

class SqliteDB(object):
    'Sqlite数据库的上下文管理器'
    def __init__(self, database='sqlitedb', isolation_level='', ignore_exc=False):
        self.database = database
        self.isolation_level = isolation_level
        self.ignore_exc = ignore_exc
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = sqlite3.connect(database=self.database, isolation_level=self.isolation_level)
            self.cursor = self.connection.cursor()
            return self.cursor
        except Exception as ex:
            traceback.print_exc()
            raise ex

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if not exc_type is None:
                self.connection.rollback()
                return self.ignore_exc
            else:
                self.connection.commit()
        except Exception as ex:
            traceback.print_exc()
            raise ex
        finally:
            self.cursor.close()
            self.connection.close()
            
class RedisDB(object):
    'redis数据库的上下文管理器'
    def __init__(self, database = '0' ,host='localhost', port='6379',decode_responses=True):
        self.database = database
        self.host = host
        self.port = port
        self.decode_responses = decode_responses
        self.connection = None

    def __enter__(self):
        try:
            self.connection = redis.StrictRedis(host = self.host , port = self.port, db = self.database, decode_responses = self.decode_responses)
            return self.connection
        except Exception as ex:
            traceback.print_exc()  #traceback.print_exc()来代替print ex 来输出详细的异常信息
            raise ex

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 异常类型，异常值，异常追踪
        try:
            if not exc_type is None:
                return self.ignore_exc
        except Exception as ex:
            traceback.print_exc()
            raise ex
        finally:
            self.connection.close()

#if __name__ == '__main__':
#     with RedisDB(2) as db:
#         data = db.get('DedeUserID')
#         print(data)
#     # 建表
#     with SqliteDB('dynamic.db') as db:
#         db.execute('create table if not exists user (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(100), age INTEGER)')

#     # 创建一条记录, 如果抛出异常, 可以测试事务回滚
#     with SqliteDB('dynamic.db') as db:
#         db.execute('insert into user (name, age) values (?, ?)', ('Tom', 10))
#     #     #raise Exception()

#     # 查询记录
#     with SqliteDB('dynamic.db') as db:
#         query_set = db.execute('select * from user where name=? limit ?', ('Tom', 100,)).fetchall()
#         print(len(query_set))
#         for item in query_set:
#             print(item)

#     # 删除记录
#     with SqliteDB('dynamic.db') as db:
#         query_set = db.execute('delete from user where name=?', ('Tom',))