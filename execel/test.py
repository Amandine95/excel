# -*- coding:utf-8 -*-

import sys
import csv

reload(sys)
sys.setdefaultencoding('utf-8')


def cut_log(filename):
    f = open(filename, 'r')
    success_city = []
    for line in f.readlines():
        if line.startswith(u'success'):
            city_id = unicode(line.split('-')[1][0:4])
            success_city.append(city_id)
    return success_city


def read_csv():
    file_name = u'fail_data/fail_data_乌兰察布市.csv'
    f = open(file_name, 'r+')
    data_list = csv.reader(f)
    for row, data in enumerate(data_list):
        print row, data


if __name__ == '__main__':
    # file_name = u'56_wrong.txt'
    # a = [u'110']
    # b = cut_log(file_name)
    # print a + b
    read_csv()
