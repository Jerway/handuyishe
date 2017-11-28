import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "handu.settings")
django.setup()

import random
from urllib.parse import urlencode
import json
import math
import requests
import os
from pymongo import MongoClient
from App.models import ProType, Product

likeTypeName = ''


def start():


    choose = input(' 是否开启mysql服务 是否有 handuyishe 库  是否修改 setting 密码  是否迁移  y/n')
    if choose == 'y':
        return True
    else:
        start()


def getType():
    type_list = []
    qsp = {
        'callback': 'jQuery1102010757311608594966_1508333185479',
        'brand_id': 936036,
        'access_type': 0,
    }

    url = 'https://mst.vip.com/Special/getCategory?' + urlencode(qsp)

    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}).text
    result = json.loads(response[response.find('(') + 1:-1])
    if result and 'result' in result.keys():
        data = result.get('result').get('data')
        print('获取 韩都衣舍商品分类列表信息 成功 ')
        for item in data:
            type_list.append([item.get('cat_id'), item.get('cnt'), item.get('name')])

    return type_list


def getChooseTypeEvery():
    proInfoList = []
    type_list = getType()
    for info in type_list:
        catId = info[0]
        cnt = info[1]
        product_ids = ''
        index = 0
        for offset in range(int(math.ceil(cnt / 120))):
            for proId in getChooseTypeList(offset * 120, catId):
                try:
                    index += 1
                    product_ids = product_ids + proId + ','
                    if index % 20 == 0 or index == cnt:
                        print(product_ids[:-1])
                        qsp = {

                            'callback': 'jQuery1102009271360702725451_1508372963111',
                            'brand_id': 936036,
                            'warehouse': 'VIP_NH',
                            'client': 'pc',
                            'product_ids': "'" + product_ids[:-1] + "'",

                        }
                        product_ids = ''
                        url = 'https://mst.vip.com/special/getVisProductDataV2?' + urlencode(qsp)
                        urlHandle = url.split('%27')
                        response = requests.get(urlHandle[0] + urlHandle[1],
                                                headers={
                                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}).text

                        result = response[43:-1]
                        data = json.loads(result)
                        if data and 'data' in data.keys():
                            data = data.get('data')
                            for item in data:
                                proInfoList.append([item.get('product_id'), item.get('product_name'), 'https:' + item.get('small_image'), item.get('vipshop_price'), info[2]])
                except:
                    pass

    return proInfoList


def getChooseTypeList(offset, catId):
    data_list = []
    qsp = {
        'callback': 'jQuery1102007049795961507344_1508335937797',
        'brand_id': 936036,
        'offset': offset,
        'warehouse': 'VIP_NH',
        'cat_id': catId,
        'sort': 0,
    }

    url = 'https://mst.vip.com/special/getVisProductIds?' + urlencode(qsp)

    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}).text
    result = json.loads(response[response.find('(') + 1:-1])
    if result and 'data' in result.keys():
        data = result.get('data')
        for item in data:
            data_list.append(item)

    return data_list


def data_to_mysql():

    try:
        type_list = getType()
        print('存储 商品分类信息 ........')
        for every_type in type_list:
            pro_type = ProType()
            pro_type.tid = every_type[0]
            pro_type.total = every_type[1]
            pro_type.name = every_type[2]
            pro_type.save()
        print('end-----------------')
        print('存储 商品详细信息 .........')

        for every_info in getChooseTypeEvery():

            pro_info = Product()
            pro_info.pid = every_info[0]
            pro_info.name = every_info[1]
            pro_info.imgurl = every_info[2]
            pro_info.price = every_info[3]
            pro_info.ptype = ProType.objects.filter(name=every_info[4]).first()
            pro_info.save()

        print('存储商品信息 end ---------------------')
    except:
        pass


def main():

    if start():
        data_to_mysql()


if __name__ == '__main__':
    main()
