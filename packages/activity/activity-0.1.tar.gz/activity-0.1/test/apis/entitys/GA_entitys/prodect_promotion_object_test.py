# -*- coding:utf-8 -*-
"""
    promotion_Obj 单元测试 创建所有活动集合 和 用户模板
    2018/10/24
    by李博文
"""

import unittest
import json

from pro.apis.product_promotion_objcet import promotion_obj,product_object
from pro.apis.entitys.user_info import UserInfo



class Promotion_obje(unittest.TestCase):

    @classmethod
    def setUp(self):
        with open("../../../tmp/bg_test.json", encoding="utf8") as f:
            json_python = json.load(f)
            json_product = json_python["product_list"]
            json_promotion = json_python["promotion_list"]
            json_user = json_python["user"]

            shangpinhuodong = json_promotion.get("product_activity_list")
            promotion = shangpinhuodong[0]

            self.promotion_list = promotion_obj(json_promotion)
            self.product_list = product_object(json_product)
            self.user = UserInfo(json_user)

            # print(json_product)
    def tearDown(self):
        pass

    def test_return(self):
        print(type(self.promotion_list))
        self.assertIsNotNone(self.promotion_list)

    def test_product_object(self):

        for i in self.product_list:
            print(i.productSeatList)
        self.assertIsNotNone(self.product_list)

    def test_user(self):
        print(self.user.id)
        self.assertIsNotNone(self.user)



