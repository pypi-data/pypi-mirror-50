#!/usr/bin/env python
"""
    统一优惠模板
   encoding: utf-8
   2018/12/26 2:28 PM
   
  
   by李博文
"""



from pro.apis.entitys.GA_entitys.promotion_entity import PromotionEntity
from pro.utils.pro_exception import ProException


class Unify_MoneyBack_Cp(PromotionEntity):

    def __init__(self, obj):
        super().__init__(obj)
        # 参加统一打折换购的商品
        self.product_list = obj['specific_activities'][0]['product_list']

        # 满足条件
        self.target_type = str(obj['specific_activities'][0]['target_type']).lower()

        self.value_num = obj['specific_activities'][0]['operation_set'][0]['value_num']

        # 比较符
        comp_symb_type = str(obj['specific_activities'][0]['operation_set'][0]['comp_symb_type']).lower()
        if comp_symb_type is None or (comp_symb_type != 'g' and comp_symb_type != 'ge' and comp_symb_type != "e"):
            raise ProException("comp_symb_type为空或非法")
        self.comp_symb_type = comp_symb_type.lower()

        # 换购条件集合
        self.operation_set = []

        if not obj['specific_activities'][0]['operation_set']:
            raise ProException("换购条件为空")

        for i in obj['specific_activities'][0]['operation_set']:
            k = OperationList(i)
            self.operation_set.append(k)


    def __str__(self):
        return str(self.__dict__)

class OperationList(object):
    def __init__(self, obj):

        # 统一优惠的换购值
        self.purchase_condition = obj["redemption"]["purchase_condition"]

        # 换购商品数量
        self.give_value = obj["redemption"]["give_value"]

        # 可以参见换购商品的集合
        self.product_list = obj["redemption"]["product_list"]
        if not obj["pcond_id"]:
            raise ProException("换购执行明细ID未传入")
        # 换购执行明细ID
        self.pcond_id = obj["pcond_id"]

    def __str__(self):
        return str(self.__dict__)
