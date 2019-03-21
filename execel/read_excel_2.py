# -*- coding:utf-8 -*-

import sys
import xlrd
import csv
from get_coordinate import getGeoPoints, getAddressInfo
from tianditu_coordinate import tiandituPoint

reload(sys)
sys.setdefaultencoding('utf-8')


def excelToCsv(filename):
    book = xlrd.open_workbook(filename)
    sheet = book.sheets()[0]
    rows = sheet.nrows
    cols = sheet.ncols
    titles = sheet.row_values(1)
    id_no = titles.index('id')
    province_no = titles.index('province')
    city_no = titles.index('city')
    location_no = titles.index('location')
    data_list = []
    for i in range(2, 5):
        data = {}
        data['id'] = sheet.cell_value(i, id_no)
        data['province'] = sheet.cell_value(i, province_no)
        city = sheet.cell_value(i, city_no)
        location = sheet.cell_value(i, location_no)
        data['city'] = city
        data['location'] = location
        address = city + location
        bd_lat, bd_lon = getGeoPoints(address)
        data['tdt_lat'], data['tdt_lon'] = tiandituPoint(address)
        district = getAddressInfo(bd_lat, bd_lon)
        data['bd_lat'], data['bd_lon'] = bd_lat, bd_lon
        data['district'] = district
        data_list.append(data)
    with open('data_csv.csv', 'wb+', ) as csv_obj:
        headers = data_list[0].keys()
        writer = csv.DictWriter(csv_obj, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data_list)


if __name__ == '__main__':
    filename = u'土地成交案例.xls'
    excelToCsv(filename)
