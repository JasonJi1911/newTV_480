# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item,Field


class IfVodItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 视频标题
    vod_name = Field()

    # 分集标题
    chapter_name = Field()

    # 格式化标题
    final_title = Field()

    # 视频封面
    vod_pic = Field()

    # 演员
    vod_actor = Field()

    # 导演
    vod_director = Field()

    # 简介
    vod_content = Field()

    # 评分
    vod_score = Field()

    # 频道
    type_name = Field()

    # 类型
    vod_class = Field()

    # 年代
    vod_year = Field()

    # 地区
    vod_area = Field()

    # ifvod链接
    vod_url = Field()

    # 资源站链接
    res_url = Field()

    # 清晰度
    path = Field()

    # 播放渠道
    source = Field()

    proxy = Field()




