import requests
from bs4 import BeautifulSoup

r = requests.get("https://www.baidu.com/")
r.encoding = 'utf-8'

html = r.text
soup = BeautifulSoup(html, 'html.parser')
# 测试title
# print(soup.title)

# 测试tag
# print(soup.a)

# 测试name
# print(soup.a.name)
# print(soup.a.parent.name)
# print(soup.a.parent.parent.name)


# 测试attribute
# tag = soup.a
# print(tag)
# print(tag.attrs['class'])
# print(tag.attrs['href'])
# print(type(tag.attrs))
# print(type(tag))

# 测试string
# tag = soup.a
# print(tag.string)
# print(type(tag.string))

# 测试comment注释内容
html1 = "<b><!--This is a comment--></b><p>This is not a comment</p>"
soup1 = BeautifulSoup(html1, 'html.parser')
print(soup1.b.string)
print(type(soup1.b.string))
print(soup1.p.string)
print(type(soup1.p))

# print(soup.prettify())