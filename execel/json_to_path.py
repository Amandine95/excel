# -*- coding:utf-8 -*-
import json


def dict_generator(indict, pre=None):
    """提取json——>路径和值"""
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                if len(value) == 0:
                    yield pre + [key, '{}']
                else:
                    for d in dict_generator(value, pre + [key]):
                        yield d
            elif isinstance(value, list):
                if len(value) == 0:
                    yield pre + [key, '[]']
                else:
                    for v in value:
                        for d in dict_generator(v, pre + [key]):
                            yield d
            elif isinstance(value, tuple):
                if len(value) == 0:
                    yield pre + [key, '()']
                else:
                    for v in value:
                        for d in dict_generator(v, pre + [key]):
                            yield d
            else:
                yield pre + [key, value]
    else:
        yield indict


if __name__ == "__main__":
    sJOSN = ''
    sValue = json.loads(sJOSN)
    for i in dict_generator(sValue):
        print('.'.join(i[0:-1]), ':', i[-1])


# --------------------------------------------#

def add_value(dict_obj, path, value):
    """空字典按照路径插入值"""
    obj = dict_obj
    for i, v in enumerate(path):
        if i + 1 == len(path):
            if not isinstance(obj.get(v, ''), list):
                obj[v] = list()
            obj[v].append(value)
            continue
        obj[v] = obj.get(v, '') or dict()
        obj = obj[v]
    return dict_obj


d = {}
print add_value(d, ['A', 'B', 'C'], ('output.txt', '2mb'))
print add_value(d, ['X', 'Y'], ('log.txt', '10kb'))
print add_value(d, ['A', 'B', 'C'], ('video.mp4', '2GB'))
