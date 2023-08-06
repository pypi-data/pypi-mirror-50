#!/usr/bin/env python
"""
    统一满减模板
   encoding: utf-8
   2018/12/18 1:49 PM
   
  
   by李博文
"""

from pro.apis.entitys.GA_entitys.promotion_entity import PromotionEntity
from pro.utils.pro_exception import ProException

class Unify_Moneyback(PromotionEntity):
    def __init__(self,obj):
        super().__init__(obj)

        # 参加统一满减的商品
        self.product_list = obj['specific_activities'][0]['product_list']

        # 满足条件
        self.target_type = str(obj['specific_activities'][0]['target_type']).lower()

        # 比较符
        comp_symb_type = str(obj['specific_activities'][0]['operation_set'][0]['comp_symb_type']).lower()
        if comp_symb_type is None or (comp_symb_type != 'g' and comp_symb_type != 'ge' and comp_symb_type != "e"):
            raise ProException("comp_symb_type为空或非法")
        self.comp_symb_type = comp_symb_type.lower()

        # 比较值
        self.value_num = obj['specific_activities'][0]['operation_set'][0]['value_num']

        # 满减值
        self.moenyback = obj['specific_activities'][0]['operation_set'][0]['money_off_value']



    def __str__(self):
        return str(self.__dict__)