# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from itemadapter import ItemAdapter

import pymysql
from pymysql.cursors import DictCursor
import requests
import time

config = {
    'user': 'root',
    'password': '696d9c48b1875ffe',
    'port': 3306,
    'host': '47.74.90.95',
    'db': 'beiwo2',
    'charset': 'utf8'
}

class ScrapyspiderPipeline:
    def process_item(self, item, spider):
        return item


class IfVodPipeline:
    def process_item(self, item, spider):
        # 480推送地址
        # post_domain = 'http://src.shcdn-qq.com'
        post_domain = 'http://107.155.99.106:2000'
        post_url = post_domain + '/api/importDownload?format=json&key=bWgL6ilF'

        # item['vod_director'] = ''
        millis = int(round(time.time() * 1000)) + 1
        item['final_title'] = str(millis)
        # item['vod_year'] = ''
        print(item['chapter_name'])
        with spider.conn.cursor(cursor=DictCursor) as c:
            # 查询语句
            query_table_sql = """
                SELECT * FROM vod_Play_480 where vod_name = %(vod_name)s and chapter_name = %(chapter_name)s
                and source = 1 and type_name = %(type_name)s
            """
            update_sql = """
                Update vod_Play_480 set path = %(path)s where vod_name = %(vod_name)s and chapter_name = %(chapter_name)s
            """
            # 注意表中字段和values()中的字段要一一对应
            sql = """
                insert into vod_Play_480(vod_name, chapter_name, final_title, vod_pic, vod_actor, vod_director,
                    vod_content, vod_score, type_name, vod_class, vod_year, vod_area, vod_url, path)
                values (%(vod_name)s, %(chapter_name)s, %(final_title)s, %(vod_pic)s, %(vod_actor)s, %(vod_director)s,
                    %(vod_content)s, %(vod_score)s, %(type_name)s, %(vod_class)s, %(vod_year)s, %(vod_area)s, %(vod_url)s, %(path)s)
            """
            # item：dict
            # 将item转换字典
            item_dict = dict(item)

            # --------------查询数据--------------
            c.execute(query_table_sql, item_dict)
            results = c.fetchall()
            print('查询到：' + str(len(results)))
            if len(results) > 0:
                print('该视频已经入库')
                c.execute(update_sql, item_dict)
                spider.conn.commit()
                return item

            # try:
            # 执行sql语句
            c.execute(sql, item_dict)
            # 执行sql语句
            spider.conn.commit()
            # except:
            #     # 发生错误时回滚
            #     spider.conn.rollback()

            name = item_dict['final_title'] + '-' + item_dict['vod_name'] + '-' + item_dict['chapter_name'] + '(480P)'
            d = "{\r\n    \"data\": [\r\n        {\r\n            \"type\": \"direct\",\r\n            \"url\": \"" \
                + item_dict['vod_url'] + "\",\r\n            \"title\": \"" \
                + name \
                + "\",\r\n            \"category\": \"480P\"\r\n        }\r\n    ]\r\n}"
            d = d.encode("utf-8")
            headers = {
                'Content-Type': 'application/json'
            }

            payload = json.dumps({
                "data": [
                    {
                        "type": "direct",
                        "url": item_dict['vod_url'],
                        "title": name,
                        "category": "480P"
                    }
                ]
            })
            payload = payload.encode("utf-8")
            res = requests.request("POST", post_url, headers=headers, data=d)
            print(item_dict['vod_url'])
            print(res.text)
        return item


class ifIqiyiPipeline:
    def process_item(self, item, spider):
        # 720推送地址
        post_domain = 'http://174.139.47.186:2000'
        post_url = post_domain + '/api/importDownload?format=json&key=fOJ6xXuG'
        # post_domain = 'http://67.198.181.58:2000'
        # post_url = post_domain + '/api/importDownload?format=json&key=RvJCmDxB'

        # item['vod_director'] = ''
        millis = int(round(time.time() * 1000)) + 1
        item['final_title'] = str(millis)
        # item['vod_year'] = ''
        print(item['chapter_name'])
        with spider.conn.cursor(cursor=DictCursor) as c:
            # 查询语句
            query_table_sql = """
                SELECT * FROM vod_Play_720 where vod_name = %(vod_name)s and chapter_name = %(chapter_name)s
                and source = %(source)s and type_name = %(type_name)s
            """
            # 注意表中字段和values()中的字段要一一对应
            sql = """
                insert into vod_Play_720(vod_name, chapter_name, final_title, vod_url, source)
                values (%(vod_name)s, %(chapter_name)s, %(final_title)s, %(vod_url)s, %(source)s)
            """
            # item：dict
            # 将item转换字典
            item_dict = dict(item)

            # --------------查询数据--------------
            c.execute(query_table_sql, item_dict)
            results = c.fetchall()
            print('查询到：' + str(len(results)))
            if len(results) > 0:
                print('该视频已经入库')
                return item

            # try:
            # 执行sql语句
            c.execute(sql, item_dict)
            # 执行sql语句
            spider.conn.commit()
            # except:
            #     # 发生错误时回滚
            #     spider.conn.rollback()

            name = item_dict['final_title'] + '-' + item_dict['vod_name'] + '-' + item_dict['chapter_name']
            d = "{\r\n    \"data\": [\r\n        {\r\n            \"type\": \"direct\",\r\n            \"url\": \"" \
                + item_dict['vod_url'] + "\",\r\n            \"title\": \"" \
                + name \
                + "\",\r\n            \"category\": \"" + item_dict[
                    'type_name'] + "\"\r\n        }\r\n    ]\r\n}"
            d = d.encode("utf-8")
            headers = {
                'Content-Type': 'application/json'
            }
            res = requests.request("POST", post_url, headers=headers, data=d)
            print(item_dict['vod_url'])
            print(res.text)
        return item