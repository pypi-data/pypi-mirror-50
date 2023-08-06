# -*- coding: utf-8 -*-

import os
import sqlite3
import threading
from webapp.tools.publiccon import ConfingObj


class MySqlite:

    def __init__(self):
        pass

    def setConnetion(self, _dbname):
        self.conn = sqlite3.connect(ConfingObj.DATAROOT_PATH + os.sep + "db" + os.sep + _dbname + ".db")
        self.setcurrsor()

    def setConnetionWithPath(self, path):
        self.conn = sqlite3.connect(path)
        self.setcurrsor()

    def setcurrsor(self):
        self.currsor = self.conn.cursor()
        # self.currsor.execute("PRAGMA key='123'")

    def execute(self, sql, values=[]):
        return self.currsor.execute(sql, values)

    def executemany(self, sql, values=[]):
        return self.currsor.executemany(sql, values)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def closedb(self):
        self.conn.close()

    def querylist(self, sql, values=[]):
        cursor = self.currsor.execute(sql, values)
        descriptions = cursor.description
        # print("descriptions:" + str(descriptions))
        col_name_list = [tuple[0] for tuple in descriptions]
        res = []
        for row in cursor:
            rowdict = {}
            columns = row
            # print(columns)
            for l in range(len(columns)):
                column = columns[l]
                rowdict[col_name_list[l]] = column

            res.append(rowdict)

        return res


if __name__ == '__main__':

    # mySqlite3 = MySqlite3("/Users/zhoucheng/poscloud/core/sqlite3db/mytest1.db")
    # print(id(mySqlite3.conn))
    #
    # mySqlite31 = MySqlite3("/Users/zhoucheng/poscloud/core/sqlite3db/mytest1.db")
    # print(id(mySqlite31.conn))
    #
    # mySqlite32 = MySqlite3("/Users/zhoucheng/poscloud/core/sqlite3db/mytest1.db")
    # print(id(mySqlite32.conn))

    mysqlite = MySqlite()
    mysqlite.setConnetionWithPath("/Users/zhoucheng/poscloud/core/sqlite3db/mytest1.db")
    sql = "CREATE TABLE IF NOT EXISTS tester(timestamp DATETIME, uuid TEXT)"
    mysqlite.execute(sql)
    mysqlite.commit()
    mysqlite.closedb()


    def aa():
        mysqlite = MySqlite()
        mysqlite.setConnetionWithPath("/Users/zhoucheng/poscloud/core/sqlite3db/mytest1.db")
        sql = "SELECT *  from tester "
        mysqlite.querylist(sql)
        mysqlite.querylist(sql)
        mysqlite.commit()
        mysqlite.closedb()


    def bb():
        mysqlite = MySqlite()
        mysqlite.setConnetionWithPath("/Users/zhoucheng/poscloud/core/sqlite3db/mytest1.db")
        # sql = "INSERT into tester values (?, ?)",("2010-01-01 13:00:00", "bow1")
        # mysqlite.execute("INSERT into tester values (?, ?)",("2010-01-02 13:00:00", "bow1"))
        # mysqlite.execute("INSERT into tester values (?, ?)",("2010-01-03 13:00:00", "bow1"))
        mysqlite.commit()
        mysqlite.closedb()


    for i in range(5):
        t1 = threading.Thread(target=aa())
        # t2 = threading.Thread(target=bb())
        t1.start()
        # t2.start()

    for i in range(5):
        t1 = threading.Thread(target=aa())
        t1.start()
