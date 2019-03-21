# -*- coding:utf-8 -*-
from urllib import quote, urlopen
import json


# 根据地址获取经纬度坐标（From BaiduMap Api）
# 传入地址数据格式必须为str,不能是unicode
def getGeoPoints(address):
    tries = 5
    while tries > 0:
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
                tries -= 1
                continue

        except Exception, e:
            print 'ex', e
            tries -= 1
            continue
    lat = float(0)
    lon = float(0)
    return lat, lon


# 根据坐标获取地址
def getAddressInfo(lat, lon):
    tries = 5
    while tries > 0:
        try:
            url = 'http://api.map.baidu.com/geocoder/v2/'
            output = 'json'
            ak = 'jTkxA1kZ0tGqTpPGYv0DVT701vOQRowI'
            location = str(lat) + ',' + str(lon)
            lastest_admin = "1"  # 是否访问最新版行政区划分数据 1是0否
            uri = url + '?location=' + location + "&output=" + output + "&pois=1&ak=" + ak + "&lastest_admin" + lastest_admin

            req = urlopen(uri)
            res = req.read()
            result = json.loads(res)
            if result['status'] == 0:
                address_info = result['result']
                return address_info['addressComponent']['district']
            else:
                tries -= 1
                continue

        except Exception, e:
            print 'x', e
            tries -= 1
            continue
    address_info = None
    return address_info


if __name__ == '__main__':
    address = u'密云县密云镇密云新城0102街区中部'
    lat, lon = getGeoPoints(address)
    print lat, lon
