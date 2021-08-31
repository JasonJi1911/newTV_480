import bs4.element
import requests
import re
from bs4 import BeautifulSoup
import bs4

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status();
        r.encoding = r.apparent_encoding;
        return r.text;
    except:
        return ""

def fillUnivList(uList, html):
    soup = BeautifulSoup(html, 'html.parser')
    for tr in soup('tbody').children:
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            # for td in tds:
            #     uList.append(td.string)
            uList.append(tds[0].string, tds[1].string, tds[4].string)
    pass

def printUnivList(uList, num):
    tplt = "{0:^10}\t{1:{3}^10}\t{2:^10}"
    print(tplt.format('排名', '学校名称', '总分', chr(12288)))
    for i in range(num):
        u =uList[i]
        print(tplt.format(u[0], u[1], u[2], chr(12288)))
    print("Suc" + str(num))

def main():
    uInfo = []
    url = "https://www.shanghairanking.cn/rankings/bcur/2021"
    html = getHTMLText(url)
    fillUnivList(uInfo, html)
    printUnivList(uInfo, 20)

main()