#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import lxml
import re
import pymysql

conn = pymysql.connect(host='localhost', user='root', passwd='xxxx', db='scp_data', charset='utf8')
cur = conn.cursor()

def getNum(num):
    if num < 10: num = '00' + str(num)
    elif num > 99: num = str(num)
    else: num = '0' + str(num)
    return num
def getText(text):
    text = str(text)
    text = re.sub('<.*?>','',text)
    text = re.sub('\n\n','',text)
    text = re.sub('[IOSD].*?: ','',text)
    return text

for num in range(1, 4000):
    soup = BeautifulSoup(requests.get('http://www.scp-wiki.net/scp-' + getNum(num)).text, 'lxml')
    scp_content = soup.find(id='page-content')
    scp_detail = re.split('<strong>', str(scp_content))
    print(num)
    if re.search('Item #:', scp_detail[1]):
        cur.execute("insert into scp_items values (%s,%s,%s,%s)",(getText(scp_detail[1]), getText(scp_detail[2]), getText(scp_detail[3]), getText(scp_detail[4])))
    else:
        cur.execute("insert into scp_items(Item, Description) values (%s,%s) ", (str('scp'+getNum(num)), getText(scp_content)))

cur.close()
conn.commit()
conn.close()
