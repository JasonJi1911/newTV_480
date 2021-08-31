import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import json
from ScrapySpider.ifvodItems import IfVodItem
import pymysql
from pymysql.cursors import DictCursor
from scrapy import signals

config = {
    'user': 'root',
    'password': '874527a8bdd8ec2a',
    'port': 3306,
    'host': '47.88.17.122',
    'db': 'beiwo2',
    'charset': 'utf8'
}

class IfaiqiyiSpider(scrapy.Spider):
    name = 'ifaiqiyi'
    # allowed_domains = ['www.jxsp.tv']
    base_jiexi_url = 'http://jxsp.tv/jx/?url='
    custom_settings = {
        'ITEM_PIPELINES': {
            'ScrapySpider.pipelines.ifIqiyiPipeline': 300,
        },
    }
    start_urls = list()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(IfaiqiyiSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider.conn = pymysql.Connect(**config)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        spider.conn.close()
        print('爬虫结束了')

    def start_requests(self):
        with self.conn.cursor(cursor=DictCursor) as c:
            # 查询语句
            query_table_sql = """
                SELECT a.video_id, b.title as vod_name, a.title, a.resource_url 
                from sf_video_chapter AS a 
                inner join sf_video as b on a.video_id = b.id
                WHERE a.resource_url like '%.iqiyi.%' limit 5
            """
            c.execute(query_table_sql)
            results = c.fetchall()
            print('视频数量: ' + str(len(results)))
            # for i in range(0, 1, 1):
            for i in range(0, len(results), 1):
                chapter = results[i]
                resource_str = chapter['resource_url']
                resource_arr = json.loads(resource_str)
                source = ""
                response_url = ''
                for key in resource_arr:
                    source = key
                    value = resource_arr[key]
                    if ".iqiyi." in value:
                        response_url = self.base_jiexi_url + value

                print(response_url)
                video_id = chapter['video_id']
                title = chapter['title']
                vod_name = chapter['vod_name']
                if response_url != '':
                    yield scrapy.Request(response_url, callback=self.parseDetail
                                         , meta={'source': source, 'title': title, 'vod_name': vod_name})

    def parseDetail(self, response):
        source = response.meta['source']
        title = response.meta['title']
        vod_name = response.meta['vod_name']

        j = json.loads(response.text)
        if not ('code' in j.keys()) or j['code'] != '200':
            print("解析失败")
            return

        m3u8_url = j['url']
        item = IfVodItem()
        item['vod_name'] = vod_name
        item['chapter_name'] = title
        item['vod_url'] = m3u8_url
        item['source'] = source
        item['type_name'] = 'iqiyi'

        yield item


