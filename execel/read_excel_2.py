# -*- coding:utf-8 -*-

import xlrd
import csv
from get_coordinate import getGeoPoints, getAddressInfo
from tianditu_coordinate import tiandituPoint, tiandituAddress
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def excelToCsv(filename):
    """读取excel写入csv"""
    book = xlrd.open_workbook(filename)
    sheet = book.sheets()[0]
    rows = sheet.nrows
    titles = sheet.row_values(1)
    id_no = titles.index('id')
    electr_supervise = titles.index('electr_supervise_no')
    location_no = titles.index('location')
    with open(u'new_data_1.csv', 'w+') as f:
        headers = ['electr_supervise_no', 'id', 'province', 'city', 'district', 'location', 'bd_lat', 'bd_lon',
                   'tdt_lat', 'tdt_lon', 'status']
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        with open(u'fail_data_1.csv', 'w+') as f1:
            headers = ['electr_supervise_no', 'id', 'province', 'city', 'district', 'location', 'bd_lat', 'bd_lon',
                       'tdt_lat', 'tdt_lon', 'status']
            writer = csv.DictWriter(f1, fieldnames=headers)
            writer.writeheader()

            for i in range(2, rows):

                id = sheet.cell_value(i, id_no)
                electr_supervise_no = sheet.cell_value(i, electr_supervise)
                province = u'北京市'
                location = sheet.cell_value(i, location_no)
                address = u'北京市' + location
                bd_lat, bd_lon = getGeoPoints(address)
                tdt_lat, tdt_lon = tiandituPoint(address)
                if bd_lat != 0 and bd_lon != 0:
                    info = getAddressInfo(bd_lat, bd_lon)
                    city = info[0]
                    district = info[1]
                    status = 1
                    if city != u'北京市':
                        status = 0
                else:
                    status = 0

                write_lines = '\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",%f,%f,%f,%f,%d' % (
                    electr_supervise_no, id, province, city, district, location, bd_lat, bd_lon, tdt_lat, tdt_lon,
                    status)
                print write_lines
                if status == 1:
                    f.write(write_lines + "\n")
                else:
                    f1.write(write_lines + "\n")
    # data['bd_lat'], data['bd_lon'] = bd_lat, bd_lon
    # data['tdt_lat'], data['tdt_lon'] = tdt_lat, tdt_lon
    # province = u'北京市'
    # city = city
    # yield data


# def writeCsv(file_xls, file_csv, file_csv_failed):
#     with open(file_csv, 'wb+') as csv_obj:
#         headers = ['electr_supervise_no', 'id', 'province', 'city', 'district', 'location', 'bd_lat', 'bd_lon',
#                    'tdt_lat', 'tdt_lon', 'status']
#         writer = csv.DictWriter(csv_obj, fieldnames=headers)
#         writer.writeheader()
#         with open(file_csv_failed, 'wb+') as csv_obj1:
#             headers1 = ['electr_supervise_no', 'id', 'province', 'city', 'district', 'location', 'bd_lat', 'bd_lon',
#                         'tdt_lat',
#                         'tdt_lon', 'status']
#             writer1 = csv.DictWriter(csv_obj1, fieldnames=headers1)
#             writer1.writeheader()
#             for data in excelToCsv(file_xls):
#                 if data['status'] == 0:
#                     writer1.writerow(data)
#                 else:
#                     writer.writerow(data)


if __name__ == '__main__':
    file1 = u'土地成交案例.xls'
    # file2 = u'new_data_2.csv'
    # file3 = u'failed_data_2.csv'
    excelToCsv(file1)
