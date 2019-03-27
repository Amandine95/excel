# -*- coding:utf-8 -*-

from store_to_elasticsearch import get_es_client
import logging
import sys
import csv
from get_coordinate import getGeoPoints, getAddressInfo
from tianditu_coordinate import tiandituPoint
from multiprocessing import Process

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


def get_city():
    """获取城市及ID"""

    dict = {}
    for pre in [4603]:
        sql = '''
                {"query":{"bool":{"must":[{"prefix":{"city_id":"%d"}}],"must_not":[],"should":[]}},"from":0,"size":50,"sort":[],"aggs":{}}
                ''' % pre

        try:
            results = es.search("region_metadata_2017_cn", "meta", sql)
            if results['hits']['total'] > 0:
                data = results['hits']['hits'][0]['_source']
                city_id = data['city_id']
                city = data['city']
                dict[city_id] = city

        except Exception as e:
            logger.debug(e)

    return dict


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


def parse_es_data(f, i):
    """按城市匹配修正es的数据"""
    city_dict = get_city2()
    print 'cities-', len(city_dict.keys())
    # f = open(u'city_without_data.csv', 'a+')
    success_citys = [u'3608', u'2111', u'2309', u'2307', u'3401', u'3608', u'3304', u'2203', u'2306', u'2224', u'3203',
                     u'2104', u'3301', u'2207', u'2101', u'2204', u'2110', u'2107', u'2303', u'2202', u'2327', u'2102',
                     u'3605', u'3711', u'3602', u'2113', u'2105', u'3506', u'3706', u'2208', u'2312', u'3205', u'2108',
                     u'2114', u'3211', u'2304', u'3410', u'2312', u'2311', u'3717', u'2206', u'3705', u'2112', u'3417',
                     u'3311', u'3402', u'2201', u'2109', u'2310', u'3501', u'3405', u'2106', u'3609']
    for key in city_dict.keys():
        prefix = key[0:4]
        if prefix not in success_citys and prefix[0] == i:
            f1 = open(u'success_data_23/success_data_%s_%s.csv' % (city_dict[key], prefix), 'w+')
            headers1 = ['electr_supervise_no', 'id', 'province', 'city', 'district', 'location', 'bd_lat', 'bd_lon',
                        'tdt_lat', 'tdt_lon', 'flag']
            writer = csv.DictWriter(f1, fieldnames=headers1)
            writer.writeheader()
            f2 = open(u'fail_data_23/fail_data_%s.csv' % city_dict[key], 'w+')
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
                f.write('\"%s没有数据\",\"city_id=%s\"' % (city_dict[key], prefix) + "\n")
                continue

            f1.close()
            f2.close()
            success_citys.append(prefix)
            print 'success-%s' % success_citys[-1]

    # f.close()


if __name__ == '__main__':
    # parse_es_data("land_transaction_1_cn", "transaction")
    # print get_city2()
    f = open(u'city_without_data_23.csv', 'a+')
    p1 = Process(target=parse_es_data, args=(f, '2',))
    p2 = Process(target=parse_es_data, args=(f, '3',))
    p1.start()
    p2.start()
    f.close()
