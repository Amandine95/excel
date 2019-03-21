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
    # dis_no = titles.index('district')
    location_no = titles.index('location')
    data_title = ['id', 'province', 'city', 'location', 'baidu_geopoint', 'tiditu_geopoint', 'district']
    # with open('data_csv.csv', 'w',) as cvs_obj:
    #     writer = csv.writer(cvs_obj)
    #     writer.writerows(data_title)
    for i in range(2, 5):
        data = []
        data.append(sheet.cell_value(i, id_no))
        data.append(sheet.cell_value(i, province_no))
        city = sheet.cell_value(i, city_no)
        location = sheet.cell_value(i, location_no)
        data.append(city)
        data.append(location)
        address = city + location
        bd_lat, bd_lon = getGeoPoints(address)
        tdt_lat, tdt_lon = tiandituPoint(address)
        district = getAddressInfo(bd_lat, bd_lon)
        data.append((bd_lat, bd_lon))
        data.append((tdt_lat, tdt_lon))
        data.append(district)
        print data[-1].encode('utf-8')
        break

        # writer.writerows(data)


if __name__ == '__main__':
    filename = u'土地成交案例.xls'
    excelToCsv(filename)
