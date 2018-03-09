# -*- coding:utf8 -*-
import json
import arcpy
import urllib2
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')


def TDTPOI(keyword):
    url = 'http://www.tianditu.com/query.shtml?postStr={"keyWord":'+ keyword +',"level":"9","mapBound":"120.668417,31.243466,120.845635,31.435428","queryType":"1","count":"1000000","start":"0"}&type=query '
    json_obj = urllib2.urlopen(url)
    data = json.load(json_obj)
    count = data['count']
    # key = data['keyword']
    print count

    doc = open(keyword.decode('utf-8') + '.csv', 'a')
    doc.write('name' + ',' + 'x' + ',' + 'y' + ',' + 'adrress' + ',' + 'telephone')
    doc.write('\n')
    for item in data['pois']:
        name = item['name']
        lonlat = item['lonlat']
        address = item['address']
        phone = item.get('phone', '无')
        xy = lonlat.split(' ')
        y = xy[1]
        x = xy[0]
        res = name + ',' + x + ',' + y + ',' + address + ',' + phone

        doc.write(res)
        doc.write('\n')

    doc.close()

keyword ='网吧'
TDTPOI(keyword)
