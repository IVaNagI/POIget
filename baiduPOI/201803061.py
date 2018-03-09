# -*- coding:utf8 -*-
import json
import os
import urllib2
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')


class BaiDuPOI(object):
    def __init__(self, itemy, loc):
        self.itemy = itemy
        self.loc = loc

    def urls(self):
        api_key = baidu_api
        urls = []
        for pages in range(0, 25):
            url = 'http://api.map.baidu.com/place/v2/search?query=' + self.itemy + '&bounds=' + self.loc + '&page_size=20&page_num=' + str(
                pages) + '&output=json&ak=' + api_key
            urls.append(url)
        return urls


    def baidu_search(self):
        json_sel = []
        for url in self.urls():
            json_obj = urllib2.urlopen(url)
            data = json.load(json_obj)
            for item in data['results']:
                jname = item["name"]
                jlat = item.get("location").get('lat')
                jlng = item.get("location").get('lng')
                jadr = item["address"]
                jtel = item.get("telephone")
                js_sel = jname + ',' + str(jlat) + ',' + str(jlng) + ',' + jadr + ',' + str(jtel)
                json_sel.append(js_sel)
        return json_sel


class LocaDiv(object):
    def __init__(self, loc_all, divd):
        self.loc_all = loc_all
        self.divd = divd

    def lat_all(self):
        lat_sw = float(self.loc_all.split(',')[0])
        lat_ne = float(self.loc_all.split(',')[2])
        lat_list = [str(lat_ne)]
        while lat_ne - lat_sw >= 0:
            m = lat_ne - self.divd
            lat_ne = lat_ne - self.divd
            lat_list.append('%.2f' % m)
        return sorted(lat_list)

    def lng_all(self):
        lng_sw = float(self.loc_all.split(',')[1])
        lng_ne = float(self.loc_all.split(',')[3])
        lng_list = [str(lng_ne)]
        while lng_ne - lng_sw >= 0:
            m = lng_ne - self.divd
            lng_ne = lng_ne - self.divd
            lng_list.append('%.2f' % m)
        return sorted(lng_list)

    def ls_com(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ab_list = []
        for i in range(0, len(l1)):
            a = str(l1[i])
            for i2 in range(0, len(l2)):
                b = str(l2[i2])
                ab = a + ',' + b
                ab_list.append(ab)
        return ab_list

    def ls_row(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ls_com_v = self.ls_com()
        ls = []
        for n in range(0, len(l1) - 1):
            for i in range(len(l2) * n, len(l2) * (n + 1) - 1):
                a = ls_com_v[i]
                b = ls_com_v[i + len(l2) + 1]
                ab = a + ',' + b
                ls.append(ab)
        return ls



if __name__ == '__main__':
    baidu_api = 'D'  # 这里填入你的百度API
    print("开始爬数据，请稍等...")
    start_time = time.time()
    loc = LocaDiv('31.240121,120.671538,31.432176,120.854761', 0.05)
    # 120.671538,31.240121, 120.86816,31.436527
    # loc = '苏州'
    locs_to_use = loc.ls_row()
    # print 'locs_to_use:'
    # print locs_to_use
    # locs_to_use = loc
    for loc_to_use in locs_to_use:
        print loc_to_use
        par = BaiDuPOI('美食', loc_to_use)  # 请修改这里的参数
        a = par.baidu_search()
        doc = open('MS.csv', 'a')
        for ax in a:
            doc.write(ax)
            doc.write('\n')
        doc.close()
    end_time = time.time()
    print("数据爬取完毕，用时%.2f秒" % (end_time - start_time))
