# -*- coding:utf-8 -*-
"""
    梯度买赠模板
    2018/10/23
    by李博文
"""

from pro.apis.entitys.GA_entitys.promotion_entity import PromotionEntity
from pro.utils.pro_exception import ProException


class Gradient_BuyGift(PromotionEntity):
    def __init__(self,obj):
        super().__init__(obj)

        if obj['specific_activities'][0]['product_list'] is None:
            raise ProException("商品列表不能为空")
        # 参加梯度买赠的商品
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
        self.promotion_lineno = obj["promotion_lineno"] if obj["promotion_lineno"] else None

        # 赠送的商品
        self.buygift_product = obj["buy_gifts"]["product_list"]

        # 比较值
        self.value_num = obj['value_num']

        # 赠送数量
        self.give_value = int(obj["buy_gifts"]["give_value"])

    def __str__(self):
        return str(self.__dict__)



