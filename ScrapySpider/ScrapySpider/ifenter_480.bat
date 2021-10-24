@echo off

echo "这里的D:和D:\Python 是Python文件所在的盘及路径"
cd C:\Users\Administrator\Desktop\ifvod480\ScrapySpider\ScrapySpider
echo "开始抓取综艺"
scrapy crawl ifenter
echo "运行完毕"
pause