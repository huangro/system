#!/usr/bin/python
# -*- coding:utf-8 -*-

import marshal

def marshal_dump_obj(obj):
    """
    :param obj:
    :return:
    """
    result = marshal.dumps(obj)
    return result

def marshal_load_obj(obj_str):
    """
    :param obj_str:
    :return:
    """
    result = marshal.loads(obj_str)
    return result

