#!/usr/bin/python
# -*- coding: utf-8 -*-

from copy import deepcopy
from functools import wraps
from flask import request
# from src.misc.render import json_detail_render
# from configs.settings import YML_JSON, logger


def transfer(column):
    def dec(func):
        @wraps(func)
        def _(*args, **kwargs):
            tmap = {
                '?': "",
                '!': "",
                '@': [],
                '#': {},
                '$': False,
            }
            result = func(*args, **kwargs)
            if not isinstance(result, list):
                raise('should be a list')

            cols = [i.strip() for i in column.split('|')]
            pure_cols = map(lambda x : x[1:], cols)
            template = {col[1:]: tmap.get(col[0]) for col in cols}
            key_col = filter(lambda x: '?' in x, cols)[0][1:]
            tdata = [{item: getattr(res, item) for item in pure_cols} for res in result]

            data = []
            
            for d in tdata:
                tpl = deepcopy(template)
                for k, v in d.iteritems():
                    if isinstance(tpl[k], basestring) and v:
                        tpl[k] = v
                    elif isinstance(tpl[k], list) and v:
                        tlist = deepcopy(tpl[k])
                        tlist.append(v)
                        tpl[k] = tlist
                    elif isinstance(tpl[k], dict) and v:
                        tdict = deepcopy(tpl[k])
                        tdict.update(v)
                        tpl[k] = tdict
                    elif isinstance(tpl[k], bool):
                        t = deepcopy(tpl[k])
                        t = bool(v)
                        tpl[k] = t

                data.append(tpl)
            return data
        return _
    return dec


def transfer2json(column):
    """
    ? : key
    ! : string
    @ : list
    # : dict
    $ : bool
    & : tuple
    """
    def dec(func):
        @wraps(func)
        def _(*args, **kwargs):
            tmap = {
                '?': "",
                '!': "",
                '@': [],
                '#': {},
                '$': False,
                '&': (),
            }
            result = func(*args, **kwargs)
            if not isinstance(result, list):
                raise('should be a list')
            cols = [i.strip() for i in column.split('|')]
            pure_cols = map(lambda x : x[1:], cols)
            template = {col[1:]: tmap.get(col[0]) for col in cols}
            key_col = filter(lambda x: '?' in x, cols)[0][1:]
            tdata = [{item: getattr(res, item) for item in pure_cols} for res in result]
            data = []
            for d in tdata:
                fu = [i for i in data if i.get(key_col) == d.get(key_col)]
                if len(fu) == 0:
                    tpl = deepcopy(template)
                    for k,v in d.iteritems():
                        if isinstance(tpl[k], basestring) and v:
                            tpl[k] = v
                        elif isinstance(tpl[k], list) and v:
                            tlist = deepcopy(tpl[k])
                            tlist.append(v)
                            tpl[k] = tlist
                        elif isinstance(tpl[k], dict) and v:
                            tdict = deepcopy(tpl[k])
                            tdict.update(v)
                            tpl[k] = tdict
                        elif isinstance(tpl[k], bool):
                            t = deepcopy(tpl[k])
                            t = bool(v)
                            tpl[k] = t
                        elif isinstance(tpl[k], tuple) and v:
                            tlist = deepcopy(tpl[k])
                            tmp = []
                            tmp.append(v)
                            tlist += tuple(tmp)
                            tpl[k] = tlist

                    data.append(tpl)
                else:
                    fu = fu[0]
                    for k,v in d.iteritems():
                        if isinstance(fu[k], basestring) and v:
                            fu[k] = v
                        elif isinstance(fu[k], list) and v:
                            tlist = deepcopy(fu[k])
                            tlist.append(v)
                            fu[k] = list(set(tlist))
                            fu[k].sort(key=tlist.index)
                        elif isinstance(fu[k], dict) and v:
                            tdict = deepcopy(fu[k])
                            tdict.update(v)
                            fu[k] = tdict
                        elif isinstance(tpl[k], bool):
                            t = deepcopy(tpl[k])
                            t = bool(v)
                            tpl[k] = t
                        elif isinstance(fu[k], tuple) and v:
                            tlist = deepcopy(fu[k])
                            tmp = []
                            tmp.append(v)
                            tlist += tuple(tmp)
                            fu[k] = tuple(tlist)
            return data
        return _
    return dec


def slicejson(settings):

    config = [setting.split('|') for setting in settings]

    def _slicejson(ret):
        for conf in config:
            na = [[dict(i) for i in map(lambda x: zip((conf[1],conf[2]), x), zip(r.get(conf[3]),r.get(conf[4])))] for r in ret]
            for index, item in enumerate(ret):
                for k in [conf[3], conf[4]]:
                    del item[k]
                item[conf[0]] = na[index]
        return ret

    def wrapper(func):
        @wraps(func)
        def _(*args, **kwargs):
            ret = func(*args, **kwargs)
            return _slicejson(ret)
        return _
    return wrapper





# def validation(validate_name = None):

#     def validate_required(key, value):
#         request_value = request.json.get(key)
#         expect_value = value
#         if request_value is None:
#             return False, json_detail_render(201, [], "{} is required".format(key))
#         return True, 1


#     def validate_min_length(key, value):
#         request_value = request.json.get(key)
#         expect_value = value
#         if request_value is not None and len(request_value) < expect_value:
#             return False, json_detail_render(202, [], "{} min length is {}".format(key, value))
#         return True, 1


#     def validate_max_length(key, value):
#         request_value = request.json.get(key)
#         expect_value = value
#         if request_value is not None and len(request_value) > expect_value:
#             return False, json_detail_render(202, [], "{} max length is {}".format(key, value))
#         return True, 1

#     def validate_type(key, value):
#         ttype_dict = {
#             'list': list,
#             'basestring': basestring,
#             'dict': dict,
#             'int': int,
#             'bool': bool,
#         }
#         request_value = request.json.get(key)
#         expect_value = value
#         if request_value is not None and not isinstance(request_value, ttype_dict.get(value)):
#             return False, json_detail_render(203, [], "{} should be a {}".format(key, value))
#         return True, 1

#     KEY_FUNC_MAP = {
#         'required': validate_required,
#         'min_length': validate_min_length,
#         'max_length': validate_max_length,
#         'type': validate_type,
#     }

#     def wrapper(func):
#         @wraps(func)
#         def _(*args, **kwargs):
#             protocol, vname = validate_name.split(':')
#             if request.method == protocol:
#                 all_json = YML_JSON
#                 validate_json = deepcopy(all_json.get(vname))
#                 del validate_json['returnvalue']
#                 for item, settings in validate_json.items():
#                     for key, value in settings.items():
#                         f = KEY_FUNC_MAP.get(key)
#                         ret = f(item, value)
#                         if not ret[0]:
#                             return ret[1]
#             return func(*args, **kwargs)
#         return _
#     return wrapper










