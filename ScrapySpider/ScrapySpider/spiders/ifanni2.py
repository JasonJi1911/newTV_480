import scrapy
from browsermobproxy import Server
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
from browsermobproxy import Server

config = {
    'user': 'root',
    'password': '874527a8bdd8ec2a',
    'port': 3306,
    'host': '47.88.17.122',
    'db': 'beiwo2',
    'charset': 'utf8'
}

class Ifvod2Spider(scrapy.Spider):
    name = 'ifanni2'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'ScrapySpider.middlewares.SelenuimDownloaderMiddleware': 543,
        }
    }
    # allowed_domains = ['www.ifsp.tv/']
    base_domain = 'https://www.ifsp.tv'
    base_play_url = 'https://www.ifsp.tv/play?id='
    start_urls = list()
    # for i in range(1, 6, 1):
    #     start_urls.append('https://www.ifsp.tv/list?keyword=&star=&pageSize=36&cid=0,1,6&year=今年&language=-1&region=-1&status=-1&orderBy=2&desc=true&page=' + str(i))

    # for i in range(1, 10, 1):
    #     start_urls.append('https://www.ifsp.tv/list?keyword=&star=&pageSize=36&cid=0,1,6&year=去年&language=-1&region=-1&status=-1&orderBy=2&desc=true&page=' + str(i))
    #
    # for i in range(1, 66, 1):
    #     start_urls.append('https://www.ifsp.tv/list?keyword=&star=&pageSize=36&cid=0,1,6&year=更早&language=-1&region=-1&status=-1&orderBy=2&desc=true&page=' + str(i))

    # 抓取连载
    for i in range(1, 5, 1):
        start_urls.append(
            'https://www.ifsp.tv/list?keyword=&star=&pageSize=36&cid=0,1,6&year=今年&language=-1&region=-1&status=-1&orderBy=1&desc=true&page=' + str(
                i))

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(Ifvod2Spider, cls).from_crawler(crawler, *args, **kwargs)
        spider.conn = pymysql.Connect(**config)

        server = Server(r'C:\Users\Administrator\Desktop\newTV_spider_python\ScrapySpider\ScrapySpider\Proxy\browsermob\bin\browsermob-proxy.bat')
        server.start()
        proxy = server.create_proxy()
        spider.proxy = proxy
        spider.server = server

        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        spider.conn.close()
        spider.proxy.close()
        spider.server.stop()
        print('爬虫结束了')

    def start_requests(self):
        for i in range(0, 1, 1):
            # for i in range(0, len(self.start_urls), 1):
            req_url = self.start_urls[i]
            # req_url = 'http://www.baidu.com'
            yield scrapy.Request(req_url, callback=self.parseListPage)

    def parseListPage(self, response):
        j = json.loads(response.text)
        html = j['html']

        if 'api/user/validate?token=' not in response.text:
            print('未登录')
            return False

        page_url = response.url
        soup = BeautifulSoup(html, 'html.parser')
        video_list = soup.select('.search-results .v-c')

        # for i in range(0, 1, 1):
        for i in range(0, len(video_list), 1):
            item = IfVodItem()
            video = video_list[i]

            item['type_name'] = '动漫'
            if not (video.select_one('.video-teaser .title-box .title a') is None):
                item['vod_name'] = video.select_one('.video-teaser .title-box .title a').string
                url = video.select_one('.video-teaser .title-box .title a').attrs['href']
                url = self.base_domain + url

            if not (video.select_one('.video-teaser .title-box .text-small span') is None):
                item['vod_class'] = video.select_one('.video-teaser .title-box .text-small span').string

            if not (video.select_one('.teaser-detail .detail-starring') is None):
                item['vod_actor'] = video.select_one('.teaser-detail .detail-starring').get_text()

            if not (video.select_one('.video-teaser .v-content img') is None):
                item['vod_pic'] = video.select_one('.video-teaser .v-content img').attrs['src']

            if not (video.select_one('.video-teaser .v-content .rating') is None):
                item['vod_score'] = video.select_one('.video-teaser .v-content .rating').string

            if not (video.select_one('.teaser-detail .detail-story span:last-child').get_text() is None):
                item['vod_content'] = video.select_one('.teaser-detail .detail-story span:last-child').get_text()

            item['vod_area'] = ''
            item['vod_year'] = ''
            area_list = ['大陆', '香港', '台湾', '日本', '韩国', '欧美', '英国', '泰国', '其他']
            tag_list = dict()
            if not (video.select('.teaser-detail .detail-tags span') is None):
                tag_list = video.select('.teaser-detail .detail-tags span')

            if "今年" in page_url:
                item['vod_year'] = '2021'
            elif "去年" in page_url:
                item['vod_year'] = '2020'
            else:
                for tag in tag_list:
                    if tag.string.isdigit() and len(tag.string) == 4:
                        item['vod_year'] = tag.string

            for tag in tag_list:
                if tag.string in area_list:
                    item['vod_area'] = tag.string

            print(url)
            if not (url is None):
                yield scrapy.Request(url, callback=self.parse_item, meta={'item': item})

    def parse_item(self, response):
        j = json.loads(response.text)
        html = j['html']
        har = j['har']
        parent_item = response.meta["item"]

        if 'api/user/validate?token=' not in response.text:
            print('未登录')
            return False

        soup = BeautifulSoup(html, 'html.parser')
        play_list = soup.select('.player-media-list-inner .media-button')

        for entry in har['log']['entries']:
            if 'video/detail' in entry['request']['url']:
                detail_urls = entry['request']['url']
                detail_r = requests.get(detail_urls, timeout=20)
                detail_j = json.loads(detail_r.text)
                parent_item['vod_director'] = ''
                if not (detail_j['data']['info'][0]['directors'] is None) and len(
                        detail_j['data']['info'][0]['directors']) > 0:
                    parent_item['vod_director'] = detail_j['data']['info'][0]['directors'][0]

                if not (detail_j['data']['info'][0]['contxt'] is None) and detail_j['data']['info'][0]['contxt'] != '':
                    parent_item['vod_content'] = detail_j['data']['info'][0]['contxt']
        # directors = soup.select_one('.directors span:last-child').string
        # parent_item['vod_director'] = directors
        # content = soup.select_one('.summary').string
        # parent_item['vod_content'] = content

        # for i in range(0, 1, 1):
        ss = len(play_list)
        for i in range(0, len(play_list), 1):
            play = play_list[i]
            try:
                play_name = play.text.strip()
                if play_name.find("花絮") != -1:
                    continue

                item = IfVodItem()
                item = dict(parent_item)
                item['chapter_name'] = play_name
                item['path'] = self.base_domain + play.attrs['href']
                # --------------判断是否存在--------------
                # conn = pymysql.Connect(**config)
                cusor = self.conn.cursor(cursor=DictCursor)
                query_table_sql = """
                                                   SELECT * FROM vod_Play_720 where vod_name = %(vod_name)s and chapter_name = %(chapter_name)s
                                                   and source = 1 and type_name = %(type_name)s
                                               """
                # query_table_sql = """
                #                 SELECT * FROM vod_Play_1080 where vod_name = %(vod_name)s and chapter_name = %(chapter_name)s
                #             """
                item_dict = dict(item)
                # --------------查询数据--------------
                cusor.execute(query_table_sql, item_dict)
                results = cusor.fetchall()
                print('查询到1：' + '/' + item['vod_name'] + '/' + item['chapter_name'])
                if len(results) > 0:
                    print('该视频已经入库:' + '/' + item['vod_name'] + '/' + item['chapter_name'])
                    continue

                # print(item)
                yield scrapy.Request(item['path'], callback=self.parse_detail, meta={'item': item})
            except Exception as e:
                print(e)


    def parse_detail(self, response):
        item = response.meta["item"]
        j = json.loads(response.text)
        har = j['har']

        if 'api/user/validate?token=' not in response.text:
            print('未登录')
            return item

        item['vod_url'] = ""
        for entry in har['log']['entries']:
            if entry['response']['status'] == 200 and 'chunklist.m3u8' in entry['request']['url']:
                item['vod_url'] = entry['request']['url']

        if item['vod_url'] == '':
            print(item)
        else:
            yield item
