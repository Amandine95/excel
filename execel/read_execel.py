# -*- coding:utf-8 -*-
# 读取execel表格获取地址信息
# 安装包 xlrd xlwt


import xlrd
from get_coordinate import getGeoPoints
from tianditu_coordinate import tiandituPoint
import sys
from datetime import datetime
from store_to_elasticsearch import get_es_client
from xlrd import xldate_as_datetime
import json

reload(sys)
sys.setdefaultencoding('utf-8')


def read_excel(file_name):
    workbook = xlrd.open_workbook(file_name)
    worksheet = workbook.sheets()[0]
    nrows = worksheet.nrows
    ncols = worksheet.ncols
    strs = worksheet.row_values(0)
    for i in range(1, nrows - 7):
        dict = {}
        geopoint_baidu = {}
        geopoint_tianditu = {}
        for j in range(ncols):
            str = strs[j]
            object = None
            if worksheet.cell_value(0, j) == 'location':
                state_index = j
                object = location = worksheet.cell_value(i, state_index)
                geopoint_baidu['lat'], geopoint_baidu['lon'] = getGeoPoints(location)
                geopoint_tianditu['lat'], geopoint_tianditu['lon'] = tiandituPoint(location)
            elif worksheet.cell_value(0, j) == 'lon' or worksheet.cell_value(0, j) == 'lat':
                continue
            elif worksheet.cell(i, j).ctype == 3:
                cell = worksheet.cell_value(i, j)

                date = xldate_as_datetime(cell, 0)

                date = datetime.strftime(date, '%Y%m%d')
                object = date
            elif worksheet.cell_value(0, j) == 'land_name':
                land_index = j
                object = worksheet.cell_value(i, j)
            else:
                object = worksheet.cell_value(i, j)
            dict[str] = object
        dict['geopoint'] = geopoint_baidu
        dict['geopoint_tianditu'] = geopoint_tianditu
        state_no = worksheet.cell_value(i, 0)
        code = state_no + worksheet.cell_value(i, land_index)
        id_ = abs(hash(code))
        print '存入%d' % i

        es = get_es_client()
        es.index('land_transaction_cn_test', 'transaction', dict, id_)


if __name__ == '__main__':
    filename = u'北京土地市场法.xls'
    read_excel(filename)
