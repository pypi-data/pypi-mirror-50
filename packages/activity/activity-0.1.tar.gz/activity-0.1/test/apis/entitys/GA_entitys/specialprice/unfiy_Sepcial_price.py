# -*- coding:utf-8 -*-
"""
    统一特价模板
    2018/11/12
    by李博文
"""
import json
import unittest

from pro.apis.entitys.GA_entitys.specialprice.unify_Special_price import Unify_Special_price

with open("/Users/MIRINDA/gitlab/activity-engine/test/tmp/productest.json", encoding="utf8") as f:
    json_python = json.load(f)
    json_product = json_python["product_list"]
    json_promotion = json_python["promotion_list"]
    json_user = json_python["user"]
    b = json_promotion.get("product_activity_list")
    a = b[0]


class Test_Unify_Special_price(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.special_price = Unify_Special_price(a)

    def test_up(self):
        # 测试特价值50
        self.assertEqual(self.special_price.special_price, 50)

        # 测试比较值
        self.assertEqual(self.special_price.value_num, 50)

        # 测试满足条件
        self.assertEqual(self.special_price.target_type, "qtty")

        # 测试比较值
        self.assertEqual(self.special_price.comp_symb_type, "ge")
