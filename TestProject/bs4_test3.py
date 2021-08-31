import requests
from bs4 import BeautifulSoup

r = requests.get("https://www.baidu.com/")
r.encoding = 'utf-8'

html = r.text
soup = BeautifulSoup(html, 'html.parser')

print(soup.a.prettify())