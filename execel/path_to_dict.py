# -*- coding:utf-8 -*-
def get_data(dict, str):
    """按照路径取值"""
    i = 0
    # 多级路径
    if '.' in str:
        path_list = str.split('.')
        while i < len(path_list):
            key = path_list[i]
            # 存在节点
            if key in dict.keys():
                try:
                    if len(path_list) == 2:
                        return dict[path_list[i]][path_list[i + 1]]
                    elif isinstance(dict[key], type({})):
                        path_list.pop(i)
                        n_str = '.'.join(path_list)
                        # print n_str
                        get_data(dict[key], n_str)
                    else:
                        return 'key %s not exist' % path_list[i + 1]
                except Exception as e:
                    return e
            # 不存在节点
            else:
                return 'key %s not exist' % key
    # 单级路径
    else:
        key = str
        if key in dict.keys():
            return dict[key]
        else:
            return 'key %s not exist' % key


# def put_data(dict, str, object):
#     """按照路径在字典插入值"""
#     # 多级路径
#     if '.' in str:
#         path_list = str.split('.')
#         i = 0
#         while i <= len(path_list):
#             key = path_list[i]
#             #  存在节点
#             if key in dict.keys():
#                 # if i + 1 == len(path_list):
#                 if len(path_list) == 2:
#                     dict[path_list[i]][path_list[i + 1]] = object
#                     return dict
#
#                 if isinstance(dict[key], type({})):
#                     path_list.pop(i)
#                     n_str = '.'.join(path_list)
#                     put_data(dict[key], n_str, object)
#                     return dict
#                 else:
#                     return 'not dict'
#             # 不存在节点
#             else:
#                 obj = dict
#                 for i, v in enumerate(path_list):
#                     if i + 1 == len(path_list):
#                         obj[v] = object
#                         continue
#                     obj[v] = obj.get(v, '') or {}
#                     obj = obj[v]
#                 return dict
#     # 单级路径
#     else:
#         key = str
#         if key in dict.keys():
#             if not dict[key]:
#                 dict[key] = object
#                 return dict
#             else:
#                 return 'not empty'
#         else:
#             dict[key] = object
#
#             return dict


def put_data(dict, str, object):
    if '.' in str:
        path_list = str.split('.')
    else:
        path_list = [str]
    if len(path_list) == 1:
        if path_list[0] in dict.keys() and isinstance(dict[path_list[0]],type({})):
            dict[path_list[0]] = object
            return dict
    path_list.pop(0)
    str = '.'.join(path_list)
    dict = dict



# ----------测试数据--------------#


b_dcit = {
    'a': 1,
    'yangwb': {
        'id': 1,
        'sex': 'nan',
        'phone': 250
    },
    'yangwn': {
        'id': 2,
        'sex': 'other',
        'addr': {
            'province': 'bj'
        }
    },
    'hhh': {
        'id': 3,
        'money': 2000,
        'buzhidao': 'xxxx'
    }
}
if __name__ == '__main__':
    res = put_data({}, 'hello.j.lk', 12)
    # res = get_data(b_dcit, 'yangwn.name',12)
    print res
