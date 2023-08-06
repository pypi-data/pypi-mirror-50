#!/usr/bin/env python
"""

   encoding: utf-8
   2018/12/11 4:03 PM
   
  
   by李博文
"""

from unittest import TestCase
from pro.apis.GA_utils import GA_retail_carryway


class TestRecovery_seat(TestCase):

    def test_recovery(self):
        # 1(保留小数位);2(四舍五入取整);3(直接取整);4(进位取整);5(四舍五入到角);6(取整到角);

        self.assertEqual(GA_retail_carryway("1", 133.333), 133.33)
        self.assertEqual(GA_retail_carryway("2", 133.333), 133)
        self.assertEqual(GA_retail_carryway("3", 133.333), 133)
        self.assertEqual(GA_retail_carryway("4", 133.333), 134)
        self.assertEqual(GA_retail_carryway("5", 133.333), 133.3)
        self.assertEqual(GA_retail_carryway("6", 133.333), 133.3)
