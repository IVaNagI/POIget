# -*- coding:utf-8 -*-
import json
import arcpy
import urllib2
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')

class GaoDePOI(object):
    def __init__(self,api_key,itemy,loc):
        self.api_key = api_key
        self.itemy = itemy
        self.loc = loc

    def urls(self):
        urls = []
        for pages in range(0,25):
            url = 'http://restapi.amap.com/v3/place/polygon?polygon=' + self.loc +'&offset=25&page=' + str(pages) + '&keywords=' + self.itemy + '&output=json&key=' + self.api_key
            urls.append(url)
        return urls

    def baidu_search(self):
        json_sel = []
        for url in self.urls():
            json_obj = urllib2.urlopen(url)

            data = json.load(json_obj)

            for item in data['pois']:

                jname = item["name"]
                jaddress = item["address"]
                jlocation = item["location"]
                jtel = item.get("tel")

                jlon =str(jlocation).split(',')[0]
                jlat =str(jlocation).split(',')[1]
                js_sel = jname + ',' + jlat + ',' + jlon + ',' + str(jaddress) + ',' + str(jtel)
                json_sel.append(js_sel)

        return json_sel


class LocaDiv(object):
    def __init__(self, loc_all, divd):
        self.loc_all = loc_all
        self.divd = divd

    def lat_all(self):
        lat_sw = float(self.loc_all.split(',')[1])
        lat_ne = float(self.loc_all.split(',')[3])
        lat_list = [str(lat_ne)]
        while lat_ne - lat_sw >= 0:
            m = lat_ne - self.divd
            lat_ne = lat_ne - self.divd
            lat_list.append('%.2f' % m)
        return sorted(lat_list)

    def lng_all(self):
        lng_sw = float(self.loc_all.split(',')[0])
        lng_ne = float(self.loc_all.split(',')[2])
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
                ab = b + ',' + a
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
                ab = b + ',' + a
                ls.append(ab)
        return ls


arcpy.AddMessage("start get data,loading...")
start_time = time.time()
loc = LocaDiv('120.65941,31.23746,120.854761,31.432176', 0.05)
# c ="餐饮服务，道路附属设施，地名地址信息，风景名胜，公共设施，公司企业，购物服务，交通设施服务，金融保险服务，科教文化服务，摩托车服务，汽车服务，汽车维修，汽车销售，商务住宅，生活服务，事件活动，室内设施，体育休闲服务，通行设施，医疗保健服务，住宿服务，政府机构及社会团体"
c = arcpy.GetParameterAsText(0)
txt = arcpy.GetParameterAsText(0)
# arcpy.AddMessage(c)
n = c.split(",")
for item in n:
    print item
    # cate = item.decode('utf-8')
    cate = item
    locs_to_use = loc.ls_row()
    for loc_to_use in locs_to_use:

        api_key = ""
        arcpy.AddMessage(loc_to_use)
        par = GaoDePOI(api_key, cate, loc_to_use)            #请修改这里的参数
        a = par.baidu_search()
        doc = open(txt+'.csv', 'a')
        for ax in a:
            doc.write(ax)
            doc.write('\n')
        doc.close()

end_time = time.time()
time = end_time - start_time
arcpy.AddMessage("finish get data,total" + str(time) + "s")
