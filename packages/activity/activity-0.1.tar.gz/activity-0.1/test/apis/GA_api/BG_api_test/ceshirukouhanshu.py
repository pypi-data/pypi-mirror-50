#!/usr/bin/env python
"""

   encoding: utf-8
   2018/12/13 5:03 AM
   
  
   by李博文
"""

from pro.apis.entitys.GA_entitys.buygift.unify_buygift import Unify_BuyGift
from pro.apis.entitys.user_info import UserInfo
from pro.apis.entitys.products_entitys.product import Product
from pro.apis.GA_api.BG_api.unify_buygift import unify_buygift

from unittest import TestCase
import json


# 构造对象类
with open("/Users/MIRINDA/gitlab/activity-engine/test/tmp/productest.json", encoding="utf8") as f:
    json_python = json.load(f)
    json_product = json_python["product_list"]
    json_promotion = json_python["promotion_list"]
    json_user = json_python["user"]
product_activity_list = json_promotion.get('product_activity_list')

# print(product_activity_list[0])

bean = Unify_BuyGift(product_activity_list[0])

user = UserInfo(json_user)

product = Product(json_product[0], 1)
product_List = [product]
kaiguan = False


class TestUnfy_buygift(TestCase):
    def test_unify_buygift(self):
        print(unify_buygift(product_List, bean, user , kaiguan))
        self.assertIsNotNone(unify_buygift(product_List, bean, user , kaiguan))
