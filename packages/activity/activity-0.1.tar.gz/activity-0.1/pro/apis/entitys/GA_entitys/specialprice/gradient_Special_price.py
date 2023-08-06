# -*- coding:utf-8 -*-
"""
    梯度特价模板
    2018/11/12
    by李博文
"""

from pro.apis.entitys.GA_entitys.promotion_entity import PromotionEntity
from pro.utils.pro_exception import ProException


class Gradient_Special_price(PromotionEntity):
    def __init__(self, obj):
        super().__init__(obj)

        if obj['specific_activities'][0]['product_list'] is None:
            raise ProException("商品列表不能为空")
        # 可以参加梯度特价的商品
        self.product_list = obj['specific_activities'][0]['product_list']

        # 满足条件 qtty：数量  amt_list：吊牌金额  amt_retail：零售金额  amt_receivable：Gradient_Special_price应收金额
        self.target_type = str(obj['specific_activities'][0]['target_type']).lower()

        # 梯度特价条件集合
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

        # 比较值
        self.value_num = obj['value_num']

        # 特价值
        self.special_price = obj["special_offer_value"]



    def __str__(self):
        return str(self.__dict__)
