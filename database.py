#!/usr/bin/env python

"""
author: ares
date: 2019/5/12
desc:
"""

import pymysql
import pymongo
from redis import StrictRedis

from utils import get_current_func_name, get_current_time
from base import Singleton


class BaseConnector(object):
    def __init__(self):
        pass


@Singleton
class MysqlConnector(object):
    def __init__(self, host="localhost", user='root', password="", port=3306):
        self.db = pymysql.connect(host=host, user=user, password=password, port=port)
        self.cursor = self.db.cursor()
        self.db_list = []
        self.table_dict = {}

    def create_db(self, db):
        try:
            sql = "CREATE DATABASE {db} DEFAULT CHARACTER SET UTF8MB4".format(db=db)
            self.cursor.execute(sql)
            self.db_list.append(db)
            print("{} CREATE DATABASE {} SUCCESS!".format(get_current_time(), db))
        except Exception as e:
            print('%s.%s CREATE DATABASE ERROR: %s' % (self.__class__.__name__, get_current_func_name(), str(e)))

    def delete_db(self, db):
        try:
            sql = "DROP DATABASE {db}".format(db=db)
            self.cursor.execute(sql)
            self.db_list.append(db)
            print('{} DROP DATABASE {} SUCCESS!'.format(get_current_time(), db))
        except Exception as e:
            print('{} {}.{} DROP DATABASE ERROR: {}'.format(get_current_time(), self.__class__.__name__,
                                                            get_current_func_name(), str(e)))

    def select_db(self, db):
        try:
            self.db.select_db(db)
            print("{} SELECT DATABASE {} SUCCESS!".format(get_current_time(), db))
        except Exception as e:
            print('{}.{} SELECT DATABASE ERROR: {}'.format(self.__class__.__name__, get_current_func_name(), str(e)))

    def create_table(self, table, fields_dict):
        try:
            if table in self.table_dict:
                print('{} CREATE TABLE {} ERROR: Table {} already exists'.format(get_current_time(), table, table))
            else:
                fields_str = ", ".join([k + ' ' + v + ' NOT NULL' for k, v in fields_dict.items()])
                sql = "CREATE TABLE IF NOT EXISTS {table}({fields_str})".format(table=table, fields_str=fields_str)
                self.cursor.execute(sql)
                self.table_dict.update({table: tuple(fields_dict.keys())})
                print('{} CREATE TABLE {} SUCCESS!'.format(get_current_time(), table))
        except pymysql.Warning as e:
            print(e)
        except Exception as e:
            print('{} {}.{} CREATE TABLE ERROR: {}'.format(get_current_time(), self.__class__.__name__,
                                                           get_current_func_name(), str(e)))

    def insert(self, table, row):
        try:
            fields = str(self.table_dict[table]).replace("'", '')
            sql = "INSERT INTO {table}{fields} VALUES{data}".format(table=table, fields=fields, data=str(row))
            self.cursor.execute(sql)
            self.db.commit()
            print('{} INSERT INTO TABLE {} SUCCESS!'.format(get_current_time(), table))
        except IndexError as e:
            print('{} {}.{} INDEX ERROR: {}'.format(get_current_time(), self.__class__.__name__,
                                                    get_current_func_name(), table, str(e)))
        except Exception as e:
            print('{} {}.{} INSERT TABLE {} ERROR: {}'.format(get_current_time(), self.__class__.__name__,
                                                              get_current_func_name(), table, str(e)))
            self.db.rollback()

    def update(self, table, update_dict, condition):
        try:
            update_str = ", ".join([i[0] + ' = ' + i[1] for i in update_dict.items()])
            sql = "UPDATE {table} SET {update_str} WHERE {condition}".format(table=table, update_str=update_str
                                                                             , condition=condition)
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print('%s.%s UPDTAE ERROR: %s' % (self.__class__.__name__, get_current_func_name(), str(e)))
            self.db.rollback()

    def delete_table(self, table, condition=None):
        try:
            sql = "DROP TABLE {table}".format(table=table)
            if condition:
                sql = "DELETE FROM {table} WHERE {condition}".format(table=table, condition=condition)
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print('%s.%s DELETE ERROR: %s' % (self.__class__.__name__, get_current_func_name(), str(e)))
            self.db.rollback()

    def select(self, table, condition):
        try:
            if condition:
                condition = "WHERE {condition}".format(condition=condition)
            sql = "SELECT * FROM {table} {condition}".format(table=table, condition=condition)
            print(sql)
            res = self.cursor.execute(sql)
            return res
        except Exception as e:
            print('%s.%s SELECT ERROR: %s' % (self.__class__.__name__, get_current_func_name(), str(e)))
            self.db.rollback()

    def query(self, query):
        try:
            self.cursor.execute(query)
            self.db.commit()
        except Exception as e:
            print('%s.%s QUERY ERROR: %s' % (self.__class__.__name__, get_current_func_name(), str(e)))
            self.db.rollback()


@Singleton
class MongoConnector(object):
    def __init__(self, host="localhost", port=27017):
        self.client = pymongo.MongoClient(host=host, port=port)

    def __getitem__(self, item):
        return self.client[item]


@Singleton
class RedisConnector(object):
    def __init__(self, host="localhost", port=6379, db=0, password=None):
        self.client = StrictRedis(host=host, port=port, db=db, password=password)

    def expire_set(self, name, value, timeout):
        self.client.set(name, value)
        self.client.set(name, timeout)

