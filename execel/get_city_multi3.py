# -*- coding:utf-8 -*-
from store_to_elasticsearch import get_es_client
import logging
import sys
import csv
from get_coordinate import getGeoPoints, getAddressInfo
from tianditu_coordinate import tiandituPoint
from multiprocessing import Process
from test import cut_log
import time

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)

es = get_es_client()

province_code = {"11": u"北京市", "12": u"天津市", "13": u"河北省", "14": u"山西省", "15": u"内蒙古", "21": u"辽宁省", "22": u"吉林省",
                 "23": u"黑龙江省", "31": u"上海市", "32": u"江苏省", "33": u"浙江省", "34": u"安徽省", "35": u"福建省", "36": u"江西省",
                 "37": u"山东省", "41": u"河南省", "42": u"湖北省", "43": u"湖南省", "44": u"广东省", "45": u"广西壮族", "46": u"海南省",
                 "50": u"重庆市", "51": u"四川省", "52": u"贵州省", "53": u"云南省", "54": u"西藏", "61": u"陕西省", "62": u"甘肃省",
                 "63": u"青海省", "64": u"宁夏回族", "65": u"新疆维吾尔", "66": u"新疆建设兵团", "71": u"台湾省", "81": u"香港特别行政区",
                 "82": u"澳门特别行政区"}


def get_city2():
    """获取城市及id"""
    dict = {}
    # 两个字段相等条件查询
    sql = '''{"query":{"bool":{"must":[{"match_all":{}}],"filter":[{"script":{"script":{"inline":"doc['city_id'].value == doc['county_id'].value","lang":"painless"}}}],"must_not":[],"should":[]}},"from":0,"size":5000,"sort":[],"aggs":{}}
    '''
    try:
        results = es.search("region_metadata_2017_cn", "meta", sql)
        if results['hits']['total'] > 0:
            data_list = results['hits']['hits']
            for data_source in data_list:
                data = data_source['_source']
                city_id = data['city_id']
                city = data['city']
                dict[city_id] = city

    except Exception as e:
        logger.debug(e)
    dict.pop('110000')
    dict.pop('310000')
    dict.pop('120000')
    dict.pop('500000')
    return dict


def parse_es_data(success_citys, i):
    """按城市匹配修正es的数据"""
    bd_lat, bd_lon = float(0), float(0)
    tdt_lat, tdt_lon = float(0), float(0)
    district = None
    city_dict = get_city2()
    print 'cities-', len(city_dict.keys())
    for key in city_dict.keys():
        prefix = key[0:4]
        if prefix not in success_citys and prefix[0] == i:
            f1 = open(u'success_data_14/success_data_%s_%s.csv' % (city_dict[key], prefix), 'w+')
            headers1 = ['electr_supervise_no', 'id', 'province', 'city', 'district', 'location', 'bd_lat', 'bd_lon',
                        'tdt_lat', 'tdt_lon', 'flag']
            writer = csv.DictWriter(f1, fieldnames=headers1)
            writer.writeheader()
            f2 = open(u'fail_data_14/fail_data_%s.csv' % city_dict[key], 'w+')
            headers2 = ['electr_supervise_no', 'id', 'province', 'city', 'district', 'location', 'data_source_url',
                        'flag']
            writer = csv.DictWriter(f2, fieldnames=headers2)
            writer.writeheader()
            print u'%s-' % city_dict[key], prefix
            sql = '''{"query":{"bool":{"must":[{"prefix":{"electr_supervise_no":"%s"}}],"must_not":[],"should":[]}},"from":0,"size":10000,"sort":[],"aggs":{}}''' % prefix
            results = es.search("land_transaction_1_cn", "transaction", sql)
            if results['hits']['total'] > 0:
                data_list = results['hits']['hits']
                print 'total-%d' % len(data_list)
                for data in data_list:
                    id = data['_id']
                    electr_supervise_no = data['_source']['electr_supervise_no']
                    province = province_code[prefix[0:2]]
                    city = data['_source']['city']
                    location = data['_source']['location']
                    data_source_url = data['_source']['data_source_url']
                    if city == city_dict[key]:
                        right_city = city_dict[key]
                        flag = 1
                        try:
                            address = city + location
                            bd_lat, bd_lon = getGeoPoints(address)
                            tdt_lat, tdt_lon = tiandituPoint(address)
                            district = getAddressInfo(bd_lat, bd_lon)[1]
                        except Exception as e:
                            logger.debug(e)

                        if (bd_lat == 0 and bd_lon == 0) or len(electr_supervise_no) <= 9:
                            flag = 0
                    else:
                        flag = 0
                        right_city = city_dict[key]
                    if flag == 1:
                        write_line = '\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",%f,%f,%f,%f,%d' % (
                            electr_supervise_no, id, province, city, district, location, bd_lat, bd_lon, tdt_lat,
                            tdt_lon,
                            flag)
                        f1.write(write_line + "\n")
                    else:
                        write_line = '\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",%f,%f,%f,%f,%d' % (
                            electr_supervise_no, id, province, city, right_city, data_source_url, location, bd_lat,
                            bd_lon, tdt_lat,
                            tdt_lon, flag)
                        f2.write(write_line + "\n")
            else:
                print u'%s没有数据' % city_dict[key]
                # f.write('\"%s没有数据\",\"city_id=%s\"' % (city_dict[key], prefix) + "\n")
                continue

            f1.close()
            f2.close()
            success_citys.append(prefix)
            print 'success-%s' % success_citys[-1]


if __name__ == '__main__':
    # f = open(u'city_without_data_14.csv', 'a+')
    cities = [u'4107', u'4416', u'4109', u'1306', u'1101', u'1309', u'4112', u'1509', u'1503', u'4115', u'1522',
              u'1411', u'1507', u'1501', u'1302', u'1402', u'1508', u'1310', u'1307', u'1409', u'1308', u'1407',
              u'1405', u'1406', u'4513', u'4302', u'4416', u'4403', u'4418', u'4331', u'1301', u'4412', u'4409',
              u'4210', u'4208', u'1311', u'4304', u'1504', u'1408', u'1505', u'1305', u'1304', u'1506', u'1525',
              u'1404', u'1403', u'4402', u'4451', u'4505', u'4202', u'4111', u'4406', u'1410', u'1502', u'1401',
              u'4207', u'1303', u'4509', u'1529']
    file_name = u'14_wrong.txt'
    cities += cut_log(file_name)
    print len(cities)
    time.sleep(2)
    p1 = Process(target=parse_es_data, args=(cities, '1',))
    p2 = Process(target=parse_es_data, args=(cities, '4',))
    p1.start()
    p2.start()
    # f.close()
