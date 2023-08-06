# -*- coding: utf-8 -*-
import os
import sys
import datetime
import mysql.connector
mswindows = (sys.platform == "win32")
class Mysql(object):
    def __init__(self):
        self.config = {'user': '', 'password': '', 'host': '', 'database': '', 'connection_timeout': 20}
        self.conn = None
        self.cur = None
        self.durations = []

    def connect(self, database, host, user, password):
        try:
            self.config['user'] = str(user)
            self.config['password'] = str(password)
            self.config['host'] = str(host)
            self.config['database'] = str(database)
            self.conn = mysql.connector.connect(**self.config)
            self.cur = self.conn.cursor()
        except Exception as e:
            raise Exception("mysql connect error:{}".format(e))

    def get_table(self, database, host, user, password):
        self.connect(database, host, user, password)
        self.cur.execute("show tables")
        tables = self.cur.fetchall()
        for table in tables:
            if table[0].split("_")[-1] not in ["log", "detail"] and len(table[0].split("_")) > 3:
                if int(table[0].split("_")[-1]) < int(datetime.datetime.now().strftime("%Y%m%d"))\
                        and len(str(table[0].split("_")[-1])) == 8:
                    del_table = "drop table {}".format(table[0])
                    self.cur.execute(del_table)

            if table[0].split("_")[-1] not in ["log", "detail"] and len(table[0].split("_")) == 3:
                if int(table[0].split("_")[-1]) < int(datetime.datetime.now().strftime("%Y%m%d"))\
                        and len(str(table[0].split("_")[-1])) == 8:
                    del_table = "drop table {}".format(table[0])
                    self.cur.execute(del_table)
        self._close()


    def _close(self):
        try:
            self.cur.close()
        except Exception, e:
            print e
        try:
            self.conn.close()
        except Exception, e:
            print e

class log():
    def __init__(self):
        pass

    def get_file_size(self, file_path):
        if os.path.isfile(file_path):
            fsize = os.path.getmtime(file_path)
            size = fsize/float(1024*1024)
            return size

if __name__=="__main__":
    # "52.33.171.87"
    pass
    # my = Mysql()
    # my.get_table("micros_adapter_res", "10.200.0.27", "root", "derbysoft")