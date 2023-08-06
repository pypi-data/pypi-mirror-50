# -*- coding: utf8 -*-
import time
import pymysql
from pymysql.err import OperationalError
from .err import ParamError, ConnectErrorContent, DatabaseErrorContent, DbNameErrContent, EnvParamErrorContent
from os import getenv

Cursor = pymysql.cursors.Cursor
DictCursor = pymysql.cursors.DictCursor
SSCursor = pymysql.cursors.SSCursor
SSDictCursor = pymysql.cursors.SSDictCursor


class database(object):
    __instance = {}

    def __init__(self, db_name=""):
        self.db_name = db_name if db_name else getenv("DB_DEFAULT")
        if not self.db_name:
            # DbNameErrContent
            print(DbNameErrContent)
            raise ParamError(DbNameErrContent)

    def connection(self, charset="utf8mb4", autocommit=True, cursor=Cursor):
        try:
            if not self.__instance or (self.db_name not in self.__instance) or (self.db_name in self.__instance and
                                                                                self.__instance[self.db_name] is None):
                DB_HOST = getenv('DB_' + self.db_name + '_HOST', '<YOUR DB HOST>')
                DB_PORT = getenv('DB_' + self.db_name + '_PORT', '<YOUR DB PORT>')
                DB_USER = getenv('DB_' + self.db_name + '_USER', '<YOUR DB USER>')
                DB_PASSWORD = getenv('DB_' + self.db_name + '_PASSWORD', '<YOUR DB PASSWORD>')
                DB_DATABASE = getenv('DB_' + self.db_name + '_DATABASE', '<YOUR DB DATABASE>')

                # EnvParamErrorContent
                if not DB_HOST or not DB_PORT or not DB_USER or not DB_PASSWORD or not DB_DATABASE:
                    print(EnvParamErrorContent)
                    raise ParamError(EnvParamErrorContent)

                connect = pymysql.connect(
                    host=DB_HOST,
                    port=int(DB_PORT),
                    user=DB_USER,
                    password=DB_PASSWORD,
                    db=DB_DATABASE,
                    charset=charset,
                    autocommit=autocommit,
                    cursorclass=cursor
                )

                self.__instance[self.db_name] = Mysql(self.db_name, connect)
                return self.__instance[self.db_name]
            else:
                print("Mysql reuse connect")
                return self.__instance[self.db_name]
        except Exception as e:
            e.args += (ConnectErrorContent,)
            raise

    def close_connection(self, db_name):
        self.__instance[db_name] = None


class Mysql(object):
    _cursor = None

    def __init__(self, _db_name, _conn):
        self._db_name = _db_name
        self._conn = _conn

    def cursor(self):
        global _cursor
        """
        Helper function to get a cursor
          PyMySQL does NOT automatically reconnect,
          so we must reconnect explicitly using ping()
        """
        try:
            self._conn.ping()
            _cursor = self._conn.cursor()
            return self
        except OperationalError:
            print("Mysql reconnect")
            self._conn.ping(reconnect=True)
            _cursor = self._conn.cursor()
            return self
        except Exception as e:
            e.args += (DatabaseErrorContent,)
            raise

    def close(self):
        """
        Close mysql conn
        """
        try:
            print("Mysql close connect")
            database().close_connection(self._db_name)
            self._conn.close()
        except Exception as e:
            e.args += (DatabaseErrorContent,)
            raise

    def autocommit(self):
        try:
            self._conn.autocommit()
        except Exception as e:
            e.args += (DatabaseErrorContent,)
            raise

    def begin(self):
        try:
            self._conn.begin()
        except Exception as e:
            e.args += (DatabaseErrorContent,)
            raise

    def commit(self):
        try:
            self._conn.commit()
        except Exception as e:
            e.args += (DatabaseErrorContent,)
            raise

    def rollback(self):
        try:
            self._conn.rollback()
        except Exception as e:
            e.args += (DatabaseErrorContent,)
            raise

    def open(self):
        try:
            self._conn.open()
        except Exception as e:
            e.args += (DatabaseErrorContent,)
            raise

    def ping(self):
        try:
            self._conn.open()
        except Exception as e:
            e.args += (DatabaseErrorContent,)
            raise

    def select_db(self):
        try:
            self._conn.select_db()
        except Exception as e:
            e.args += (DatabaseErrorContent,)
            raise

    def set_charset(self):
        try:
            self._conn.set_charset()
        except Exception as e:
            e.args += (DatabaseErrorContent,)
            raise

    def execute(self, query, args=None):
        global _cursor
        try:
            self.cursor()
            start = time.time()

            result = _cursor.execute(query, args)

            elapsed = (time.time() - start)
            print("Sql execute time: %fs, query: %s" % (elapsed, query))
            return result
        except Exception as e:
            e.args += (DatabaseErrorContent,)
            raise

    def executemany(self, query, args=None):
        global _cursor
        try:
            self.cursor()
            start = time.time()

            result = _cursor.executemany(query, args)

            elapsed = (time.time() - start)
            print("Sql execute time: %fs, query: %s" % (elapsed, query))
            return result
        except Exception as e:
            e.args += (DatabaseErrorContent,)
            raise

    @staticmethod
    def fetchone():
        global _cursor
        try:
            result = _cursor.fetchone()
            return result
        except Exception as e:
            e.args += (DatabaseErrorContent,)
            raise

    @staticmethod
    def fetchmany(size=None):
        global _cursor
        try:
            result = _cursor.fetchmany(size)
            return result
        except Exception as e:
            e.args += (DatabaseErrorContent,)
            raise

    @staticmethod
    def fetchall():
        global _cursor
        try:
            result = _cursor.fetchall()
            return result
        except Exception as e:
            e.args += (DatabaseErrorContent,)
            raise

    @staticmethod
    def scroll(value, mode='relative'):
        global _cursor
        try:
            result = _cursor.scroll(value, mode)
            return result
        except Exception as e:
            e.args += (DatabaseErrorContent,)
            raise

    @staticmethod
    def mogrify(query, args=None):
        global _cursor
        try:
            result = _cursor.mogrify(query, args)
            return result
        except Exception as e:
            e.args += (DatabaseErrorContent,)
            raise

    @staticmethod
    def callproc(procname, args=()):
        global _cursor
        try:
            result = _cursor.callproc(procname, args)
            return result
        except Exception as e:
            e.args += (DatabaseErrorContent,)
            raise
