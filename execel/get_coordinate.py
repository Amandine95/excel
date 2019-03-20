# -*- coding:utf-8 -*-
from urllib import quote, urlopen
import json


# 根据地址获取经纬度坐标（From BaiduMap Api）
# 传入地址数据格式必须为str,不能是unicode
def getGeoPoints(address):
    while True:
        try:
            address = address.encode('utf-8') if type(address) != 'str' else address
            url = 'http://api.map.baidu.com/geocoder/v2/'
            output = 'json'
            ak = 'jTkxA1kZ0tGqTpPGYv0DVT701vOQRowI'
            add = quote(address)  # 信息格式化
            uri = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak
            req = urlopen(uri)
            res = req.read()
            temp = json.loads(res)
            if temp['status'] == 0:
                lat = temp['result']['location']['lat']
                lng = temp['result']['location']['lng']
                return lat, lng
            else:
                continue

        except Exception, e:
            print 'ex', e
            continue


if __name__ == '__main__':
    address = u'密云县密云镇密云新城0102街区中部'
    lat, lon = getGeoPoints(address)
    print lat, lon
