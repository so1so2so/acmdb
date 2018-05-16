#!/usr/bin/env python
# -*- coding:utf-8 -*-


def convert_to_int(value, default=0):
    """

    :param value: 拿到值进行int ,不能int就返还0
    :param default:
    :return:
    """
    try:
        result = int(value)
    except Exception as e:
        result = default

    return result


def convert_mb_to_gb(value, default=0):
    """

    :param value: 拿到值分开MB ,没有就为0
    :param default:
    :return:
    """
    try:
        value = value.strip('MB')
        result = int(value)
    except Exception as e:
        result = default

    return result
