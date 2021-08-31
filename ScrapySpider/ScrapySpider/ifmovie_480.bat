@echo off

echo "这里的D:和D:\Python 是Python文件所在的盘及路径"
cd C:\Users\Administrator\Desktop\newTV_480\ScrapySpider\ScrapySpider
echo "开始抓取综艺"
scrapy crawl ifmovie
echo "运行完毕"