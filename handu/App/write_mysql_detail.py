import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "handu.settings")
django.setup()

import json
from App.models import ProductInfo
import requests
import lxml.etree

from queue import Queue
import threading

import time

from App.models import ProductInfo, Product


# link_queue = Queue()
# downloader_num = 15
# downloader_page = 0
# threads = []
def getpid():
    for i in range(0, 1680, 120):
        baseurl = requests.get('https://mst.vip.com/special/getVisProductIds', headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'},
                               params={'callback': 'jQuery110201414887129721225_1511963203113',
                                       'brand_id': 1819209,
                                       'offset': i,
                                       'warehouse': 'VIP_NH',
                                       'cat_id': '',
                                       'sort': 0,
                                       'size_name': '',
                                       '_': 1511963203121})
        try:
            pid = baseurl.text.split('[')[1].split(']')[0]
            for id in pid.split(','):
                id = id.strip('"')
                yield id
        except:
            pass


def fetch():
    global downloader_page
    for id in getpid():
        url = 'https://detail.vip.com/detail-1819209-%s.html' % str(id)
        # downloader_page +=1
        # link_queue.put(url)
        yield requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'}).text


stotallist = []
ltotallist = []
colorlists = []
dlist = []
delpricelist = []
featurelist = []
errorid = []

miaomiao = 0


def get_simghref():
    global miaomiao
    global stotallist
    global ltotallist
    global colorlists
    global dlist
    global delpricelist, featurelist, errorid
    for response in fetch():
        miaomiao += 1
        try:
            simglist = []
            limglist = []
            colorlist = []
            ahtml = lxml.etree.HTML(response)
            simghrefs = ahtml.xpath('//*[@id="J-sImg-wrap"]/div/img/@data-original')
            for simghref in simghrefs:
                imgurl = 'https:%s' % simghref
                simglist.append(imgurl)
            print('******', simglist)
            stotallist.append(simglist)

            limghrefs = ahtml.xpath('//*[@id="J-mer-ImgReview"]/div[1]/div/a/@href')
            for limghref in limghrefs:
                imgurl = 'https:%s' % limghref
                limglist.append(imgurl)
            print('++++++', limglist)
            ltotallist.append(limglist)

            colorhrefs = ahtml.xpath('//*[@class="color-list-item"]//img/@data-original')

            for colorhref in colorhrefs:
                imgurl = 'https:%s' % colorhref
                colorlist.append(imgurl)
            print('------', colorlist)
            colorlists.append(colorlist)

            namekey = ahtml.xpath('//*[@id="J-FW-detail"]/div/div[2]/div[3]/table/tbody/tr/th/text()')
            values = ahtml.xpath('//*[@id="J-FW-detail"]/div/div[2]/div[3]/table/tbody/tr/td/text()')
            details = dict(zip(namekey, values))
            print('aaaaaaaa', details)
            dlist.append(details)

            delprice = ahtml.xpath('//*[@id="J-pi-price-box"]/div[1]/span/del/text()')[0]
            print('bbbb', delprice)
            delpricelist.append(delprice)

            feature = ahtml.xpath('/html/body/div[5]/div[1]/div[2]/div[2]/div[1]/div[1]/div/p[3]/text()')[0]
            print('ccc', feature)
            featurelist.append(feature)

            # print('remaining queue:%s' % link_queue.qsize())
        except:
            errorid.append(id)
            print(id)
    print(stotallist, ltotallist, colorlists)


sizelist = []

num = 0


def get_size():
    global num
    for id in getpid():
        num += 1
        baseurl = requests.get('https://detail.vip.com/detail-ajax.php?', headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'},
                               params={'callback': "_getSizeTableData",
                                       'act': "getSizeHtml",
                                       'merchandiseId': id,
                                       'brandId': "1819209",
                                       'preview': "0",
                                       'token': " ", })
        data = baseurl.text[baseurl.text.find('{'):-1]
        datajson = json.loads(data)
        # sizename = datajson['content']['size_0']
        sizedict = datajson['content']
        # for size in sizedict:
        #     if size != 'size_0':
        #         sizetype = sizedict[size]
        #         print(sizetype)
        print('单个产品尺寸', sizedict)
        sizelist.append(sizedict)
    print(sizelist)


def save_to_mysql():
    num = 0
    for id in getpid():
        if id not in errorid:
            product = ProductInfo()
            if Product.objects.filter(pid=id):
                p = Product.objects.filter(pid=id)[0]
                product.pid = p
                product.price = p.price
                product.pname = p.name
                product.pdelprice = delpricelist[num]
                product.pcolors = colorlists[num]
                product.pdetails = dlist[num]
                product.pimgl = ltotallist[num]
                product.pimgs = stotallist[num]
                product.psize = sizelist[num]
                product.pfeature = featurelist[num]
                product.save()
                print('保存成功')

        else:
            print('%s CAN NOT FIND' % id)  # def downloader():  # while True:
        num = num + 1


# get_simghref()
#         link = link_queue.get()
#         if link is None:
#             break
#         get_simghref()
#         link_queue.task_done()
#         print('remaining queue:%s' % link_queue.qsize())

if __name__ == '__main__':
    start_time = time.time()
    # for i in range(downloader_num):
    #     t = threading.Thread(target=downloader)
    #     t.start()
    #     threads.append(t)
    #
    # link_queue.join()
    #
    # for i in range(downloader_num):
    #     link_queue.put(None)
    #
    # for t in threads:
    #     t.join()
    get_simghref()
    get_size()
    save_to_mysql()
    costtime = time.time() - start_time
    # print('download %s pages in %.2f seconds' % (downloader_page, costtime))
    print(costtime, miaomiao, num, '--------------------------')
