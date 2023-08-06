#!/usr/bin/env python
"""

   encoding: utf-8
   2018/11/20 2:32 PM
   
  
   by李博文
"""

# !/usr/bin/env python
# encoding: utf-8
# @Time    : 2018/11/19 1:34 PM
# by 李博文


import unittest
import json

from pro.apis.main import acceptParams


class Test_gatejia_pamaimian(unittest.TestCase):

    def test_not_in(self):
        # 测试vip存在但vip值不存在于活动范围(买赠)
        with open("../test_data/buy_gift_json/ga-pa_notinvip.json", encoding="utf8") as f:
            json_python = json.load(f)
            json_product = json_python["product_list"]
            json_promotion = json_python["promotion_list"]
            json_user = json_python["user"]
            
            print(acceptParams(json_product, json_promotion, json_user, None))
    def test_disounct_buyfigt(self):
        # 测试vip问题(买赠)
        with open("../test_data/buy_gift_json/ga-pa_vip.json", encoding="utf8") as f:
            json_python = json.load(f)
            json_product = json_python["product_list"]
            json_promotion = json_python["promotion_list"]
            json_user = json_python["user"]

            print(acceptParams(json_product, json_promotion, json_user, None))
    def test_tidumaizengbijiaozhi(self):

        # 测试梯度买赠档比较值为1时候与赠送值为0(买赠)
        with open("../test_data/buy_gift_json/ga_tidumaizeng_zengsongzhi.json", encoding="utf8") as f:
            json_python = json.load(f)
            json_product = json_python["product_list"]
            json_promotion = json_python["promotion_list"]
            json_user = json_python["user"]

            print(acceptParams(json_product, json_promotion, json_user, None))

    def test_GAdiejia(self):
        # 叠加商品
        with open("../test_data/buy_gift_json/GA_diejia.json", encoding="utf8") as f:
            json_python = json.load(f)
            json_product = json_python["product_list"]
            json_promotion = json_python["promotion_list"]
            json_user = json_python["user"]

            print(acceptParams(json_product, json_promotion, json_user, None))


    def test_Pa_A_A(self):
        # 全场活动买A赠A_统一
        with open("../test_data/buy_gift_json/pa_shangpin-in-zengpinlist.json", encoding="utf8") as f:
            json_python = json.load(f)
            json_product = json_python["product_list"]
            json_promotion = json_python["promotion_list"]
            json_user = json_python["user"]

            print(acceptParams(json_product, json_promotion, json_user, None))
    def test_GAdazhe(self):
        # 统一打折 商品
        with open("../test_data/discounts/GA1101.json", encoding="utf8") as f:
            json_python = json.load(f)
            json_product = json_python["product_list"]
            json_promotion = json_python["promotion_list"]
            json_user = json_python["user"]

            print(acceptParams(json_product, json_promotion, json_user, None))
    def test_GAduozhongdazhe(self):
        # 多种打折 商品
        with open("../test_data/discounts/GA1102.json", encoding="utf8") as f:
            json_python = json.load(f)
            json_product = json_python["product_list"]
            json_promotion = json_python["promotion_list"]
            json_user = json_python["user"]

            print(acceptParams(json_product, json_promotion, json_user, None))
    def test_dizengdazhe(self):
        # 递增打折 商品
        with open("../test_data/discounts/GA1103.json", encoding="utf8") as f:
            json_python = json.load(f)
            json_product = json_python["product_list"]
            json_promotion = json_python["promotion_list"]
            json_user = json_python["user"]

            print(acceptParams(json_product, json_promotion, json_user, None))

    def test_zuhedazhe(self):
        # 组合打折 商品
        with open("../test_data/discounts/GA1104.json", encoding="utf8") as f:
            json_python = json.load(f)
            json_product = json_python["product_list"]
            json_promotion = json_python["promotion_list"]
            json_user = json_python["user"]

            print(acceptParams(json_product, json_promotion, json_user, None))

    def test_tiduchucan(self):
        # 梯度买赠出参和不满足商品活动
        with open("../test_data/buy_gift_json/ga-pa_chucan.json", encoding="utf8") as f:
            json_python = json.load(f)
            json_product = json_python["product_list"]
            json_promotion = json_python["promotion_list"]
            json_user = json_python["user"]

            print(acceptParams(json_product, json_promotion, json_user, None))