# -*- coding:utf-8 -*-
"""
    统一买赠模板单元测试
    2018/10/23
    by李博文
"""
import unittest
import json

from pro.apis.entitys.GA_entitys.buygift.unify_buygift import Unify_BuyGift
from pro.apis.entitys.GA_entitys.discount.unify_discount import UnifyDiscountEntity



class Test_UnifyBuygift(unittest.TestCase):

    @classmethod
    def setUp(self):
        with open("/Users/MIRINDA/gitlab/activity-engine/test/tmp/bg_test.json", encoding="utf8") as f:
            json_python = json.load(f)
            json_product = json_python["product_list"]
            json_promotion = json_python["promotion_list"]
            json_user = json_python["user"]

            b = json_promotion.get("product_activity_list")
            a = b[0]

            self.promotion_list = Unify_BuyGift(a)



    @classmethod
    def tearDown(self):
        pass

    # 买赠商品对象
    def test_product_list(self):
        print(self.promotion_list.product_list)
        self.assertIsNotNone(self.promotion_list.product_list)

    # 满足条件
    def test_target_type(self):
        print(self.promotion_list.target_type)
        self.assertIsNotNone(self.promotion_list.target_type)

    # 比较值
    def test_value_num(self):
        print(self.promotion_list.value_num)
        self.assertIsNotNone(self.promotion_list.value_num)

    # 比较符
    def test_comp_symb_type(self):
        print(self.promotion_list.comp_symb_type)
        self.assertIsNotNone(self.promotion_list.comp_symb_type)

    # 赠送的商品
    def test_buygift_product(self):
        print(self.promotion_list.buygift_product)
        self.assertIsNotNone(self.promotion_list.buygift_product)

    # 赠送数量
    def test_gift_number(self):
        print(self.promotion_list.give_value)
        self.assertIsNotNone(self.promotion_list.give_value)