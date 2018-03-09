# -*- coding:utf-8 -*-
import requests
import json
import pandas as pd

def request_hospital_data():
    ak="xxxxxxxxxxx"  # 换成自己的 AK，需要申请
    url = "http://api.map.baidu.com/place/v2/search?query=医疗&page_size=20&scope=1&region=辽中&output=json&ak="
    params = {'page_num':0}  # 请求参数，页码
    request = requests.get(url,params=params)  # 请求数据
    total = json.loads(request.text)['total']  # 数据的总条数
    # print(total)
    total_page_num = (total+19) // 20  # 每个页面大小是20，计算总页码
    items = []  # 存放所有的记录，每一条记录是一个元素
    for i in range(total_page_num):
        params['page_num'] = i
        request = requests.get(url,params=params)
        for item in json.loads(request.text)['results']:
            name = item['name']
            lat = item['location']['lat']
            lng = item['location']['lng']
            address = item.get('address', '')
            street_id = item.get('street_id', '')
            telephone = item.get('telephone', '')
            detail = item.get('detail', '')
            uid = item.get('uid', '')
            # print(name, lat, lng, address, street_id, telephone, detail, uid)
            new_item = (name, lat, lng, address, street_id, telephone, detail, uid)
            items.append(new_item)

    # 使用pandas的DataFrame对象保存二维数组
    df = pd.DataFrame(items, columns=['name', 'lat', 'lng', 'adderss', 'street_id', 'telephone', 'detail', 'uid'])
    df.to_csv('liaozhong_hospital_info.csv', header=True, index=False)

request_hospital_data()
