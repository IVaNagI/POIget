# -*- coding:utf8 -*-
import json
import os
import urllib2
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')
urls = []
for page in range(0,20):
    url = 'http://api.map.baidu.com/place/v2/search?query=公园&region=224&coord_type=gcj02ll&page_size=20&page_num=' + str(page) + '&output=json&ak=id6STZSbOsnWkkMiMy08rDQMKiOejhTD'
    urls.append(url)
# print urls

json_sel = []
for url in urls:
    json_obj = urllib2.urlopen(url)
    data = json.load(json_obj)
    for item in data['results']:
        jname = item["name"]
        jlat = item["location"]["lat"]
        jlng = item["location"]["lng"]
        jadr = item["address"]
        js_sel = jname + ',' + str(jlat) + ',' + str(jlng) + ',' + str(jadr)
        json_sel.append(js_sel)
# print json_sel

doc = open('park.csv','a')
for ax in json_sel:
    doc.write(ax)
    doc.write('\n')
doc.close()
print 'finsh'