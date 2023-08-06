#!/usr/bin/env python
"""
   梯度满减模板
   encoding: utf-8
   2018/12/18 1:49 PM
   
  
   by李博文
"""

from pro.apis.entitys.GA_entitys.promotion_entity import PromotionEntity
from pro.utils.pro_exception import ProException


class Gradient_Moneyback(PromotionEntity):
    def __init__(self,obj):
        super().__init__(obj)

        if obj['specific_activities'][0]['product_list'] is None:
            raise ProException("商品列表不能为空")
        # 参加梯度满减的商品
        self.product_list = obj['specific_activities'][0]['product_list']

        # 满足条件 qtty：数量  amt_list：吊牌金额  amt_retail：零售金额  amt_receivable：应收金额
        self.target_type = str(obj['specific_activities'][0]['target_type']).lower()

        # 梯度买赠条件集合
        self.operation_set = []

        if not obj['specific_activities'][0]['operation_set']:
            raise ProException("梯度买赠条件为空")

        for i in obj['specific_activities'][0]['operation_set']:
            k = OperationList(i)
            self.operation_set.append(k)


    def __str__(self):
        return str(self.__dict__)





class OperationList(object):
    def __init__(self, obj):
        # 比较符"GE/G/E"
        comp_symb_type = str(obj['comp_symb_type']).lower()
        if comp_symb_type is None or (comp_symb_type != 'g' and comp_symb_type != 'ge' and comp_symb_type != "e"):
            raise ProException("comp_symb_type为空或非法")
        self.comp_symb_type = comp_symb_type

        # 活动行号pos要用
        # self.promotion_lineno = obj["promotion_lineno"] if["promotion_lineno"] in obj else None

        # 满减值
        self.moenyback = obj["money_off_value"]

        # 比较值
        self.value_num = obj['value_num']


    def __str__(self):
        return str(self.__dict__)