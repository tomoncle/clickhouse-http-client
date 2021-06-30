#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/30 15:32
# @Author  : tomoncle
# @Site    : https://github.com/tomoncle/clickhouse-http-client
# @File    : __init__.py.py
# @Software: PyCharm

import json
import logging

import requests


class _ConsoleLogger(logging.Logger):
    def __init__(self, name, level=logging.DEBUG):
        super(_ConsoleLogger, self).__init__(name, level)
        self.formatter = logging.Formatter('[%(asctime)s] %(name)s: %(levelname)s: %(message)s')
        self.handler = logging.StreamHandler()
        self.handler.setFormatter(self.formatter)
        self.addHandler(self.handler)


class ClickHouseQueryError(Exception):
    pass


class DB(object):
    C = "INSERT INTO"
    U = "UPDATE"
    R = "SELECT"
    D = "DELETE"


class ClickHouse(DB):

    def __init__(self, host="127.0.0.1", port="8123", user="default", password="", database="default", show_sql=False):
        self.show_sql = show_sql
        self.database = database
        self.logger = _ConsoleLogger("ClickHouse")
        self.url = "http://{}:{}/?user={}&password={}&database={}".format(host, port, user, password, database)

    def full_table(self, table_name):
        return "{}.{}".format(self.database, table_name)

    def _execute(self, sql, headers=None):
        headers = headers or {"Content-Type": "application/json; charset=UTF-8"}
        if self.show_sql:
            self.logger.debug(sql)

        http_response = requests.post("{}".format(self.url), headers=headers, data="{}".format(sql))
        if not self.show_sql and http_response.status_code != 200:
            self.logger.error("{}, {}".format(sql, http_response.text))
        return http_response

    def update(self, table, where, value):
        """
        更新数据
        :param table: t_student
        :param where: user_id >= 0 / status=1
        :param value: {"id": 1, "name": "tom"}
        :return: True/False
        """
        value = ", ".join("{}='{}'".format(k, v) for k, v in value.items())
        sql = "{} {} {} {} where {}".format("ALTER TABLE", self.full_table(table), self.U, value, where)
        headers = {"Content-Type": "text/tab-separated-values; charset=UTF-8"}
        response = self._execute(sql, headers=headers)
        return response.status_code == 200, response.text

    def delete(self, table, where):
        """
        remove data
        :param table: t_student
        :param where: user_id >= 0  / id IS NOT NULL
        :return: True/False
        """
        sql = "{} {} {} where {} ".format("ALTER TABLE", self.full_table(table), self.D, where)
        headers = {"Content-Type": "text/tab-separated-values; charset=UTF-8"}
        response = self._execute(sql, headers=headers)
        return response.status_code == 200, response.text

    def clear(self, table):
        """
        remove data
        :param table: t_student
        :return: True/False
        """
        sql = "{} {} {} where 1==1 ".format("ALTER TABLE", self.full_table(table), self.D)
        headers = {"Content-Type": "text/tab-separated-values; charset=UTF-8"}
        response = self._execute(sql, headers=headers)
        return response.status_code == 200, response.text

    def insert(self, table, data):
        """
        batch save/ save
        :param table:
        :param data:  list[dict] / dict
        :return: True/False
        """
        if not data:
            raise ValueError("data cannot be None.")
        if isinstance(data, dict):
            json_data = json.dumps(data)
        elif isinstance(data, list) and isinstance(data[0], dict):
            json_data = " ".join(json.dumps(o) for o in data)
        else:
            raise ValueError("data must be list[dict,...] / dict type.")
        sql = "{} {} FORMAT JSONEachRow {}".format(self.C, self.full_table(table), json_data)
        headers = {"Content-Type": "text/tab-separated-values; charset=UTF-8"}
        response = self._execute(sql, headers=headers)
        return response.status_code == 200, response.text

    def json(self, sql):
        """
        :param sql: select * from t_history
        :return:  json
        """
        response = self._execute(
            sql.rstrip(" ").rstrip(";").rstrip("format json").rstrip("FORMAT JSON") + " FORMAT JSON")
        if response.status_code == 200:
            data = response.json()
            data.pop("statistics")
            data.pop("meta")
            return True, data
        return False, response.text

    def _err(self, error):
        # self._err(ClickHouseQueryError(response.text))
        raise error

    def text(self, sql):
        """
        :param sql: select * from t_history
        :return: text
        """
        response = self._execute(sql)
        return response.status_code == 200, response.text

    def authentication(self):
        return self._execute("select 1").text == "1\n"
