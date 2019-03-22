# -*- coding:utf-8 -*-

import xlrd
import csv
from get_coordinate import getGeoPoints, getAddressInfo
from tianditu_coordinate import tiandituPoint, tiandituAddress
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def excelToCsv(filename):
    book = xlrd.open_workbook(filename)
    sheet = book.sheets()[0]
    rows = sheet.nrows
    titles = sheet.row_values(1)
    id_no = titles.index('id')
    province_no = titles.index('province')
    city_no = titles.index('city')
    location_no = titles.index('location')
    for i in range(2, rows):
        data = {}
        data['id'] = sheet.cell_value(i, id_no)
        data['province'] = sheet.cell_value(i, province_no)
        city = sheet.cell_value(i, city_no)
        location = sheet.cell_value(i, location_no)
        data['city'] = city
        data['location'] = location
        address = city + location
        bd_lat, bd_lon = getGeoPoints(address)
        tdt_lat, tdt_lon = tiandituPoint(address)
        if bd_lat == 0 and bd_lon == 0:
            district = tiandituAddress(tdt_lat, tdt_lon)
            data['status'] = 0
        else:
            district = getAddressInfo(bd_lat, bd_lon)
            data['status'] = 1
        data['bd_lat'], data['bd_lon'] = bd_lat, bd_lon
        data['tdt_lat'], data['tdt_lon'] = tdt_lat, tdt_lon
        data['district'] = district
        yield data


def writeCsv(file_xls, file_csv, file_csv_failed):
    with open(file_csv, 'wb+') as csv_obj:
        headers = ['id', 'province', 'city', 'district', 'location', 'bd_lat', 'bd_lon', 'tdt_lat', 'tdt_lon', 'status']
        writer = csv.DictWriter(csv_obj, fieldnames=headers)
        writer.writeheader()
        with open(file_csv_failed, 'wb+') as csv_obj1:
            headers1 = ['id', 'province', 'city', 'district', 'location', 'bd_lat', 'bd_lon', 'tdt_lat',
                        'tdt_lon', 'status']
            writer1 = csv.DictWriter(csv_obj1, fieldnames=headers1)
            writer1.writeheader()
            for data in excelToCsv(file_xls):
                if data['status'] == 0:
                    writer1.writerow(data)
                else:
                    writer.writerow(data)


if __name__ == '__main__':
    file1 = u'土地成交案例.xls'
    file2 = u'new_data.csv'
    file3 = u'failed_data.csv'
    writeCsv(file1, file2, file3)
