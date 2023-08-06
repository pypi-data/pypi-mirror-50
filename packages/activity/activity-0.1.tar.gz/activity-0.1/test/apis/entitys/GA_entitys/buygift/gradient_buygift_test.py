# -*- coding:utf-8 -*-
"""
    梯度买赠模板
    2018/10/23
    by李博文
"""
import unittest
import json

from pro.apis.entitys.GA_entitys.buygift.gradient_buygift import Gradient_BuyGift




class Test_GradientBuyGift(unittest.TestCase):

    @classmethod
    def setUp(self):
        with open("/Users/MIRINDA/gitlab/activity-engine/test/tmp/bg_test.json", encoding="utf8") as f:
            json_python = json.load(f)
            json_product = json_python["product_list"]
            json_promotion = json_python["promotion_list"]
            json_user = json_python["user"]

            shangpinhuodong = json_promotion.get("product_activity_list")
            promotion = shangpinhuodong[0]

            self.promotion_list = Gradient_BuyGift(promotion)

    def tearDown(self):
        pass

    # 参加买赠商品集合
    def test_product_list(self):
        print(self.promotion_list.product_list)
        self.assertIsNotNone(self.promotion_list.product_list)

    # 参见梯度买赠的商品
    def test_target_type(self):
        print(self.promotion_list.target_type)
        self.assertIsNotNone(self.promotion_list.target_type)

    # 梯度买赠条件集合
    def test_operation_set(self):
        for i in self.promotion_list.operation_set:
            self.assertIsNotNone(i.comp_symb_type)
            print(i.comp_symb_type)

            self.assertIsNotNone(i.value_num)
            print(i.value_num)

            self.assertIsNotNone(i.gift_number)
            print(i.gift_number)

            self.assertIsNotNone(i.buygift_product)
            print(i.buygift_product)
            for j in i.buygift_product:
                print(j)

            print(i.promotion_lineno)
            self.assertEqual(i.promotion_lineno,1)
        self.assertIsNotNone(self.promotion_list.operation_set)
