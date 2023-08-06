# -*- coding:utf-8 _*-
"""
@author:尹晨
@file: globle_params.py
@time: 2018/10/31
"""
import threading

global_data = threading.local()


def set_retail_carryway(retail_carryway):
    global_data.retail_carryway = retail_carryway


def get_retail_carryway():
    return global_data.retail_carryway
