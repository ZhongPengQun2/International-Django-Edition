# coding: utf-8
import re
import psycopg2
import requests
from lxml import etree
#
conn = psycopg2.connect(database="jiya", user="postgres", password="postgres", host="139.196.39.92", port="6432")
print("Opened database successfully")

cursor = conn.cursor()
cursor.execute("select id, spell from words where short_meaning is null;")
rows = cursor.fetchall()


for row in rows:
    _id = row[0]

    try:
        r = requests.get("https://fanyi.youdao.com/openapi.do?keyfrom=11pegasus11&key=273646050&type=data&doctype=json&version=1.1&q=%s"%row[1])
        result = r.json()
        print "-------------",  result, '###########'
        if result.get('basic'):
            pronunciation = result.get('basic').get('uk-phonetic')
            meaning = '\n'.join(result.get('basic').get('explains'))
            short_meaning = u"\n".join(result.get("translation"))
            cursor.execute("update words set pronunciation=%s, short_meaning=%s, meaning=%s where id=%s;", (pronunciation, short_meaning, meaning, _id))
            conn.commit()
            print _id, row[1], short_meaning
    except Exception, e:
        print "-----Exception:", str(e)
        print u"==========", _id, row[1]

conn.close()

