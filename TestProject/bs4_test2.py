import requests
from bs4 import BeautifulSoup

r = requests.get("https://www.baidu.com/")
r.encoding = 'utf-8'

html = r.text
soup = BeautifulSoup(html, 'html.parser')

# 测试HTML下行遍历
# print(soup.head)
# print(soup.head.contents)
# print(soup.body)
# print(soup.body.contents)
# print(len(soup.body.contents))
# print(soup.body.contents[1])

# print(soup.body.children)
# for child in soup.body.children:
#     print(child)

# 测试上行遍历
# print(soup.title.parent)
# print(soup.html.parent)
# # print(soup.parent)
# for parent in soup.a.parents:
#     if parent is None:
#         print(parent)
#     else:
#         print(parent.name)

# 测试平行遍历
# print(soup.a.next_sibling)
# print(soup.a.next_sibling.next_sibling)
# print(soup.a.previous_sibling)
# print(soup.a.previous_sibling.previous_sibling)

# for next in soup.a.next_siblings:
#     print(next)

for previous in soup.a.previous_siblings:
    print(previous)

