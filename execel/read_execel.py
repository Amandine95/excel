# -*- coding:utf-8 -*-
# 读取execel表格获取地址信息
# 安装包 xlrd xlwt


import xlrd
from get_coordinate import getGeoPoints
import sys
import json
from store_to_elasticsearch import get_es_client

reload(sys)
sys.setdefaultencoding('utf-8')


def read_excel(file_name):
    workbook = xlrd.open_workbook(file_name)
    worksheet = workbook.sheets()[0]
    nrows = worksheet.nrows
    ncols = worksheet.ncols
    strs = worksheet.row_values(0)

    for i in range(nrows - 2):
        dict = {}
        geopoint = {}
        for j in range(ncols):
            str = strs[j]

            if worksheet.cell_value(0, j) == 'location':
                state_index = j
                object = location = worksheet.cell_value(i, state_index)
                geopoint['lat'], geopoint['lon'] = getGeoPoints(location)
            elif worksheet.cell_value(0, j) == 'lon' or worksheet.cell_value(0, j) == 'lat':
                continue
            else:
                object = worksheet.cell_value(i + 1, j)
            dict[str] = object
        dict['geopoint'] = geopoint
        # es = get_es_client()
        # es.index('land_transaction_cn_test', 'transaction', dict, id)


if __name__ == '__main__':
    filename = u'北京土地市场法.xls'
    read_excel(filename)
