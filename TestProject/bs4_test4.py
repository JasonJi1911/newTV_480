import requests
import re
from bs4 import BeautifulSoup

r = requests.get("https://www.baidu.com/")
r.encoding = 'utf-8'

html = r.text
soup = BeautifulSoup(html, 'html.parser')

# for link in soup.find_all('a'):
#     print(link.get('href'))

# for tag in soup.find_all(re.compile('b')):
#     print(tag.name)

# for tag in soup.find_all('a', href=re.compile('baidu')):
#     print(tag)

# for tag in soup.find_all('a', string='新闻'):
# for tag in soup.find_all('a', string=re.compile('新闻')):
#     print(tag)

soup.a.find()
soup.a.find_parents()
soup.a.find_parent()
soup.a.find_siblings()
soup.a.find_sibling()
soup.a.previous_siblings()
soup.a.previous_sibling()


