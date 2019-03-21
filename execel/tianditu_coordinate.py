# -*- coding:utf-8 -*-
# 调用天地图接口获取坐标信息
# 请求： http://api.tianditu.gov.cn/geocoder?ds={"keyWord":"延庆区北京市延庆区延庆镇莲花池村前街50夕阳红养老院"}&tk=您的密钥
import json
from urllib import urlopen, quote


def tiandituPoint(address):
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
            tries -= 1
            continue
    lat = float(0)
    lon = float(0)
    return lat, lon


if __name__ == '__main__':
    tiandituPoint(u'延庆区北京市延庆区延庆镇莲花池村前街50夕阳红养老院')
