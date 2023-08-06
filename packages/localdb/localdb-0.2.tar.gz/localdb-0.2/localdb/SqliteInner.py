# -*- coding: utf-8 -*-
import threading

import sqlite3worker
import os
from webapp.tools.publiccon import ConfingObj
from loggingm import logger



class SqliteInner:
    _db = sqlite3worker.Sqlite3Worker("")
    _db_tables = {}
    connections = {}
    semaphore = threading.Semaphore()

    def __init__(self):
        pass

    def setConnetion(self, _dbname):
        self.dbname = _dbname
        connection = self.__class__.connections[_dbname] = self.onCreate(_dbname,
                                                                         ConfingObj.DATAROOT_PATH + os.sep + "db" + os.sep + _dbname + ".db")
        # logger.debug("初始化的数据库连接:"+connection)


        return self.__class__._db

    def setConnetionWithPath(self, _dbname, path):

        self.dbname = _dbname
        connection = self.__class__.connections[_dbname] = self.onCreate(_dbname, path)
        # logger.debug("初始化的数据库连接:" + connection)

        return self.__class__._db

    def onCreate(self, _dbname, dbpath):
        '''
        创建数据库连接实例
        :param _tablename: 数据库名称
        :param dbpath:数据库路径
        :return:
        '''
        sql_worker = sqlite3worker.Sqlite3Worker(dbpath)
        self.__class__._db = sql_worker
        return dbpath

    def execute(self, sql='', values=None):
        '''
        执行sql语句
        :param sql: sql语句
        :return: 返回执行结果（查询）
        '''
        try:
            if sql:
                return self.__class__._db.execute(sql, values)
        except Exception as e:
            logger.error("执行数据库出错，错误语句:"+sql)
            raise e

    # def execute_list(self, sql='', values=None):
    #     '''
    #     执行sql语句
    #     :param sql: sql语句
    #     :return: 返回执行结果（查询）带key的list
    #     '''
    #     try:
    #         #阻塞线程 -1
    #         self.semaphore.acquire()
    #         if sql:
    #             cur = self.__class__._db.execute(sql, values)
    #             # 转换成字典
    #             res = []
    #             if cur != None and len(cur) > 0:
    #                 if type(cur) == list:
    #                     descriptions = self.__class__._db._sqlite3_cursor.description
    #                     print("descriptions" + str(descriptions))
    #                     col_name_list = [tuple[0] for tuple in descriptions]
    #                     for row in range(len(cur)):
    #                         rowdict = {}
    #                         columns = cur[row]
    #                         print(columns)
    #                         for l in range(len(columns)):
    #                             column = columns[l]
    #                             rowdict[col_name_list[l]] = column
    #                         res.append(rowdict)
    #                 else:
    #                     raise OperationError(-1, "数据库错误" + str(cur))
    #
    #             return res
    #         else:
    #             raise OperationError(-1, "sql为空")
    #
    #     except Exception as e:  # logger.error("执行数据库出错，错误语句:"+sql)
    #         print("执行数据库出错，错误语句:" + sql)
    #         raise e
    #
    #     finally:
    #         #释放+1
    #         self.semaphore.release()


    def closedb(self):
        '''
        关闭数据库连接
        :return:
        '''
        if self.__class__._db:
            self.__class__._db.close()


if __name__ == '__main__':


    # sql = "CREATE TABLE IF NOT EXISTS tester(timestamp DATETIME, uuid TEXT)"
    # cur = sqliteinit.execute(sql)
    # print(cur)

    # cur = sqliteinit.execute("INSERT into tester values (?, ?)",("2010-01-01 13:00:00", "bow1"))
    # print(cur)

    sql = "SELECT *  from tester "
    # cur = sqliteinit.execute(sql)
    # print(cur)
    # for i in range(len(cur)):
    #     print("timestamp = ", cur[i][1])

    # col_name_list = [tuple[0] for tuple in cur.description]
    # print(col_name_list)
    #
    # sqliteinit.closedb()

    sqliteinit = SqliteInner()
    for i in range(2):
        t1 = threading.Thread(target=sqliteinit.execute_list(sql))
        t1.start()

    # sqliteinit1 = SqliteInner("mytest1")
    # print(sqliteinit1.execute("SELECT * from students"))
    # sqliteinit1.execute("insert into students values('测试信息3','aaaaaa',6) ")
    # print(sqliteinit1.execute("SELECT * from students"))
    # sqliteinit1.closedb()

    # print(SqliteInner.connections)
    # os.popen('copy E:\\Work\\FCPOS--R3\\poscloud\\tools\\mytest1.db E:\\Work\\FCPOS--R3\\poscloud\\core\\mytest1.db')
