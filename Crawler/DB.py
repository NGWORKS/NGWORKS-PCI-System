"""
@author: NGWORKS-夏姬八彻
@contact: wl@ngworks.com
@version: 0.a1
@file: DB.py
@time: 2020/12/12   21:18
@detail: 数据库操作的上下文管理器。
"""
import sqlite3,traceback

#sqlite3数据库的上下文管理器
class SqliteDB(object):

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

# if __name__ == '__main__':
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