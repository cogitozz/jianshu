# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors
class JianshuPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '090200',
            'database': 'jianshu',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dbparams)     # 会将上面的数据以关键字形式传入如：host=127.0.0.1
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (item['title'], item['content'], item['author'], item['avatar'],
                                       item['pub_time'], item['origin_url'], item['article_id']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            # self._sql = """
            # insert into article(id,title,content,author,avatar,pub_time,origin_url,article_id,) values (null ,%s,%s,%s,%s,%s,%s,%s)
            # """
            # 上面的sql语句有语法错误？
            self._sql = "insert into article(id,title,content,author,avatar,pub_time," \
                        "origin_url,article_id) values (null,%s,%s,%s,%s,%s,%s,%s)"
            return self._sql
        return self._sql
# **************************************上面的代码在是同步的，下面的代码是异步的*******************************************#
class JianshuTwistedPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '090200',
            'database': 'jianshu',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor   # 指定cursor的类
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = "insert into article(id,title,content,author,avatar,pub_time," \
                        "origin_url,article_id,read_count,like_count,word_count,subjects,comment_count) values (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.inster_item, item)
        defer.addErrback(self.handle_error, item, spider)

    def inster_item(self, cursor, item):
        cursor.execute(self.sql, (item['title'], item['content'], item['author'], item['avatar'],
                                       item['pub_time'], item['origin_url'], item['article_id'],
                                        item['read_count'], item['like_count'], item['word_count'],
                                        item['subjects'], item['comment_count'])
                       )

    def handle_error(self, error, item, spider):     # 错误处理函数
        print('='*10 + "error" + '='*10)
        print(error)
        print('=' * 10 + "error" + '=' * 10)








