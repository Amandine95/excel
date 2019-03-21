# -*- coding:utf-8 -*-
# 调用天地图接口获取坐标信息
# 请求： http://api.tianditu.gov.cn/geocoder?ds={"keyWord":"延庆区北京市延庆区延庆镇莲花池村前街50夕阳红养老院"}&tk=您的密钥
import json
from urllib import urlopen, quote


def tiandituPoint(address):
    ds_dict = {}
    url = 'http://api.tianditu.gov.cn/geocoder'
    tk = 'fd0b585cad4c92e1440c10a0c6bd3c76'
    ds_dict["keyWord"] = quote(address)
    data = json.dumps(ds_dict)
    uri = url + '?' + 'ds=' + data + '&tk=' + tk
    resp = urlopen(uri)
    resp_data = json.loads(resp.read())
    if resp_data['status'] == '0':
        lat = resp_data['location']['lat']
        lon = resp_data['location']['lon']
        return lat, lon


if __name__ == '__main__':
    tiandituPoint('延庆区北京市延庆区延庆镇莲花池村前街50夕阳红养老院')
