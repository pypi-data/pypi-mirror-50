# -*- coding:utf-8 -*-
# author:李旭辉
# datetime:2018/10/23 14:00
from unittest import TestCase
from pro.apis.PA_api.BG_api.bg_main import *
from pro.apis.PA_api.DC_api.dc_main import *
from pro.apis.PA_api.main_api import *
from pro.apis.entitys.products_entitys.product import *
from pro.apis.main import *
# from pro.apis.main_Mock import *

import json

with open('pa_bg_test.json','r') as ff:
    ceshi=json.load(ff)

product_list=ceshi['product_list']
promotion_list=ceshi["promotion_list"]
# promotion_list1=ceshi["promotion_list"]["fullcourt_activity_list"][0]
user=ceshi["user"]
retail_carryway=ceshi["retail_carryway"]
print(acceptParams(product_list,promotion_list,user,retail_carryway))
class testUnit(TestCase):
    def setUp(self):
        print("单测开始")
    def tearDown(self):
        print("单测结束")
    def test_total(self):
        self.assertIsNotNone(acceptParams(product_list,promotion_list,user,retail_carryway))
    def test_compare(self):
        self.assertTrue(checkdis("ge",6,4, "qtty"))

