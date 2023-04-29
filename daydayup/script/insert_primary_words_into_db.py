# coding: gbk

import re
import requests
from bs4 import BeautifulSoup
import string

for i in range(1, 41):
#    print i
    if i == 1:
        result = requests.get('http://zhongkao.xdf.cn/201809/10810191.html')
    else:
        result = requests.get('http://zhongkao.xdf.cn/201809/10810191_%s.html' % i)

    soup = BeautifulSoup(result.text, "html")
    table = soup.table


    tr_arr = table.find_all("tr")

    for tr in tr_arr:
        tds = tr.find_all('td')
        #print tds[0].get_text()
        word = tds[1].get_text()
        pronunciation = tds[2].get_text() 
        meaning = tds[3].get_text()

        word = word.replace(' ', '')
        word = ' '.join(re.findall('[a-zA-Z]+', word))
#        print word
        #print len([x for x in word if x in ss])
        #print len(word)
        print "insert into words (spell, pronunciation, meaning) values ('%s', '', '');"%(word, )
