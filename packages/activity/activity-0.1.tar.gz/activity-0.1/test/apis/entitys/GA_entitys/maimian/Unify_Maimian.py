# -*- coding:utf-8 -*-
"""
    统一买赠模板
    2018/11/12
    by李博文
"""

import json
import unittest

from pro.apis.entitys.GA_entitys.maimian.unify_maimian import Unify_Maimian

with open("/Users/MIRINDA/gitlab/activity-engine/test/tmp/productest.json", encoding="utf8") as f:
    json_python = json.load(f)
    json_product = json_python["product_list"]
    json_promotion = json_python["promotion_list"]
    json_user = json_python["user"]
    b = json_promotion.get("product_activity_list")
    a = b[0]


class Test_Unify_Maimian(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.maimian = Unify_Maimian(a)

    def test_up(self):


        # 买免值
        self.assertEqual(self.maimian.buy_from_value,1)

        # 比较符
        self.assertEqual(self.maimian.comp_symb_type,"ge")

