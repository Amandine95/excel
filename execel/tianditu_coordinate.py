# -*- coding:utf-8 -*-
# 调用天地图接口获取坐标信息
# 请求： http://api.tianditu.gov.cn/geocoder?ds={"keyWord":"延庆区北京市延庆区延庆镇莲花池村前街50夕阳红养老院"}&tk=您的密钥
import json
from urllib import urlopen, quote
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def tiandituPoint(address):
    """天地图获取坐标"""
    tries = 5
    while tries > 0:
        try:
            ds_dict = {}
            address = address.encode('utf-8') if type(address) != 'str' else address
            url = 'http://api.tianditu.gov.cn/geocoder'
            tk = 'fd0b585cad4c92e1440c10a0c6bd3c76'
            address = quote(address)
            ds_dict["keyWord"] = address
            data = json.dumps(ds_dict)
            uri = url + '?' + 'ds=' + data + '&tk=' + tk
            resp = urlopen(uri)
            resp_data = json.loads(resp.read())
            if resp_data['status'] == '0':
                lat = resp_data['location']['lat']
                lon = resp_data['location']['lon']
                return float(lat), float(lon)
            else:
                tries -= 1
                continue
        except Exception as e:
            print 'tianditu-1', e
            tries -= 1
            continue
    lat = float(0)
    lon = float(0)
    return lat, lon


# 请求：http://api.tianditu.gov.cn/geocoder?postStr={'lon':116.37304,'lat':39.92594,'ver':1}&type=geocode&tk=您的密钥
def tiandituAddress(lat, lon):
    """天地图获取地址"""
    city = None
    district = None
    tries = 5
    while tries > 0:
        try:
            post_dict = {}
            url = 'http://api.tianditu.gov.cn/geocoder'
            tk = 'fd0b585cad4c92e1440c10a0c6bd3c76'
            post_dict['lon'] = float(lon)
            post_dict['lat'] = float(lat)
            post_dict['ver'] = 1
            data = json.dumps(post_dict)
            uri = url + '?' + 'postStr=' + data + '&type=geocode&tk=' + tk
            resp = urlopen(uri)
            resp_data = json.loads(resp.read())
            if resp_data['status'] == '0':
                city = resp_data['result']['addressComponent']['city']
                district = resp_data['result']['addressComponent']['address']
                address = resp_data['result']['formatted_address']
                print address
                return city, district
            else:
                tries -= 1
                continue
        except Exception as e:
            print 'tianditu-2', e
            tries -= 1
            continue

    return city, district


if __name__ == '__main__':
    # print tiandituPoint(u'临汾市县城车站路')
    c, d = tiandituAddress(36.065732,111.511400)
    print c, d
