#!/usr/bin/env python
"""

   encoding: utf-8
   2018/12/29 2:33 PM
   
  
   by李博文
"""
from unittest import TestCase
from pro.apis.GA_api.CP_api.cp_utils import contion,calculation_current


class Combination_Moneyback_Cp(object):
    pass

class Mock_bean(object):
    def __init__(self):
        self.rela_symb_type = None







class TestContion(TestCase):

    def test_contion(self):
        # 构造参数
        response = ["amt_retail", "qtty", "2"]
        result1, result2 = contion(response)
        self.assertEqual(result1, "amt_retail")
        self.assertEqual(result2, None)

    def test_contion_one(self):
        # 构造参数
        response = ["qqq", "1"]
        result1, result2 = contion(response)
        self.assertEqual(result1, "qqq")
        self.assertEqual(result2, None)

    def Test_calculation_current(self):
        # 构造参数
        result = calculation_current(200, 100)
        self.assertEqual(result, 2)

