# -*- coding:utf-8 -*-

import sys
from get_coordinate import getAddressInfo
import re
import csv
import os


reload(sys)
sys.setdefaultencoding('utf-8')


def parse_data(file_name, path1, path2):
    """处理csv数据"""
    fr = open(file_name, 'rU')
    file_city = re.search(ur'/fail_data_(.*)\.csv', file_name).group(1)
    success = path1 + u'success_' + file_city + u'.csv'
    fail = path2 + u'fail_' + file_city + u'.csv'
    f1 = open(success, 'w+')
    headers1 = ['electr_supervise_no', 'id', 'province', 'city', 'district', 'location', 'bd_lat', 'bd_lon',
                'tdt_lat', 'tdt_lon', 'flag']
    writer = csv.DictWriter(f1, fieldnames=headers1)
    writer.writeheader()
    f2 = open(fail, 'w+')
    headers2 = ['electr_supervise_no', 'id', 'province', 'city', 'right_city', 'location', 'data_source_url', 'bd_lat',
                'bd_lon', 'tdt_lat', 'tdt_lon'
                                     'flag']
    writer = csv.DictWriter(f2, fieldnames=headers2)
    writer.writeheader()
    data_list = csv.reader(fr)
    for row, data in enumerate(data_list):
        print row, data
        if row >= 2:
            print len(data)
            ele_no = data[0]
            id = data[1]
            province = data[2]
            right_city = data[4]
            location = data[6]
            bd_lat, bd_lon = float(data[7]), float(data[8])
            tdt_lat, tdt_lon = float(data[9]), float(data[10])
            source_url = data[5]
            if ele_no and len(ele_no) >= 4 and bd_lat and bd_lon:
                district = getAddressInfo(bd_lat, bd_lon)[1]
                flag = 1
            else:
                flag = 0
            if flag == 1:
                write_line = '\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",%f,%f,%f,%f,%d' % (
                    ele_no, id, province, right_city, district, location, bd_lat, bd_lon, tdt_lat, tdt_lon, flag)
                f1.write(write_line + "\n")
            else:
                write_line = '\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",%f,%f,%f,%f,%d' % (
                    ele_no, id, province, right_city, right_city, location, source_url, bd_lat, bd_lon, tdt_lat,
                    tdt_lon,
                    flag)
                f2.write(write_line + "\n")
    f1.close()
    f2.close()
    fr.close()


def get_files(file_path):
    """获取csv文件列表"""
    file_list = os.listdir(file_path)
    return file_list


if __name__ == '__main__':
    file_pt = u'fail_data_23'
    file_ls = get_files(file_pt)
    path_1 = u'41_success/'
    path_2 = u'41_fail/'
    point = file_ls.index(u'fail_data_绍兴市.csv')
    for fl in file_ls[point:]:
        fl_name = file_pt + u'/' + fl
        print u'open-', fl_name
        parse_data(fl_name, path_1, path_2)
