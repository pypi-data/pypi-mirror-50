# -*- coding:utf-8 -*-
"""
    当前活动的择优单元测试
    2018/10/29
    by李博文
"""

from pro.apis.GA_api.BG_api import current_promotions_preferential

import unittest

class SeatMock(object):
    def __init__(self):
        self.amt_list = 10
        self.is_buy_gifts = "y"

g1 = SeatMock()
g2 = SeatMock()
g3 = SeatMock()
g4 = SeatMock()




class ProductMock(object):

    def __init__(self):
        self.productSeatList = [g1,g2,g3]

class Product(object):
    def __init__(self):
        self.productSeatList = [g1,g2]


product = ProductMock()
product1 = ProductMock()

list11 = [product1,product,product]

product = ProductMock()
list1 = [product,product]

list_data = [list11,list1]

class Test_current_promitions_preferential(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.response = current_promotions_preferential.current_promitions_preferential(list_data)


    def test_max(self):
        self.assertEqual(self.response[-1].give_sum,90)