# encoding=utf-8
"""
 author:${尹晨}
 datetime:2018/9/26 13:08
 software: PyCharm
 统一打折模板类
"""

from pro.apis.entitys.GA_entitys.promotion_entity import PromotionEntity
from pro.utils.pro_exception import ProException


class UnifyDiscountEntity(PromotionEntity):
    def __init__(self, obj):
        super().__init__(obj)
        # 参加统一打折的商品集合
        self.product_list = set(obj['specific_activities'][0]['product_list'])
        # 优惠商品集合
        self.execute_product_list = []
        if obj["specific_activities"][0].get("execute_product_list"):
            self.execute_product_list = set(obj['specific_activities'][0].get("execute_product_list", []))
        # 满足活动的条件 qtty：数量  amt_list：吊牌金额  amt_retail：零售金额  amt_receivable：应收金额
        self.target_type = str(obj['specific_activities'][0]['target_type']).lower()
        # 比较符"GE/G/E"
        comp_symb_type = str(obj['specific_activities'][0]['operation_set'][0]['comp_symb_type']).lower()
        if comp_symb_type is None or (comp_symb_type != 'g' and comp_symb_type != 'ge' and comp_symb_type != "e"):
            raise ProException("comp_symb_type为空或非法")
        self.comp_symb_type = comp_symb_type

        # 比较值
        self.value_num = obj['specific_activities'][0]['operation_set'][0]['value_num']

        # 享受值
        if obj['specific_activities'][0]['operation_set'][0]['discount_value'] > 1:
            raise ProException("discount_value折扣率不能大于1")
        self.discount_value = obj['specific_activities'][0]['operation_set'][0]['discount_value']

    def __str__(self):
        return str(self.__dict__)
