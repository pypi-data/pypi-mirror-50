"""
    梯度特价模板 单元测试
    2018/11/12
    by李博文
"""

import json
import unittest

from pro.apis.entitys.GA_entitys.specialprice.gradient_Special_price import Gradient_Special_price

with open("/Users/MIRINDA/gitlab/activity-engine/test/tmp/productest.json", encoding="utf8") as f:
    json_python = json.load(f)
    json_product = json_python["product_list"]
    json_promotion = json_python["promotion_list"]
    json_user = json_python["user"]
    b = json_promotion.get("product_activity_list")
    a = b[0]


class Test_Gradient_Special_price(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.special_price = Gradient_Special_price(a)

    def test_up(self):
        # 测试满足条件
        self.assertEqual(self.special_price.target_type, "qtty")

        # 测试梯度特价的详细条件
        for i in self.special_price.operation_set:
            # pos端行号是否满足
            self.assertEqual(i.promotion_lineno, 2)

            # 测试比较值
            self.assertEqual(i.value_num,50)

            # 测试特价值
            self.assertEqual(i.special_price,50)

            # 测试比较符
            self.assertEqual(i.comp_symb_type,"ge")