# coding: utf-8
import re
import psycopg2
import requests
from lxml import etree
import os

conn = psycopg2.connect(database="jiya", user="postgres", password="postgres", host="139.196.39.92", port="5432")
print("Opened database successfully")

cursor = conn.cursor()

start = False

cursor.execute("select id, spell from words;")
rows=cursor.fetchall()
for row in rows:
    _id, spell = row
    print _id
#    if _id == 1257:
#        start = True
#    if not start:
#        continue
#    r = requests.get("http://dict.youdao.com/dictvoice?audio=%s&type=1"%spell)

#    f = open(r'E:\\audio\\%s.mp3'%_id, 'wb')
#    f.write(r.content)

#    f.close()
    path = "../src/main/resources/static/audio/%s.mp3"%_id
    if not os.path.exists(path):
        print '------------path:', path
        r = requests.get("http://dict.youdao.com/dictvoice?audio=%s&type=1"%spell)
        f = open(path, 'wb')
        f.write(r.content)

#    r = requests.get("https://fanyi.youdao.com/openapi.do?keyfrom=11pegasus11&key=273646050&type=data&doctype=json&version=1.1&q=%s"%spell)

#    print "https://fanyi.youdao.com/openapi.do?keyfrom=11pegasus11&key=273646050&type=data&doctype=json&version=1.1&q=%s"%spell

#    result = r.json()
#    if result.get('basic'):
#        pronunciation = result.get('basic').get('uk-phonetic')
#        meaning = '\n'.join(result.get('basic').get('explains'))

#    meaning = meaning.replace("'", "\'")
#        cursor.execute("update words set pronunciation=%s, meaning=%s where id=%s;", (pronunciation,meaning, _id))
#       conn.commit()

#    else:
#       print '---------', spell

conn.close()