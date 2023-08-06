# -*- coding:utf-8 -*-
"""
    统一特价模板
    2018/11/12
    by李博文
"""

from pro.apis.entitys.GA_entitys.promotion_entity import PromotionEntity
from pro.utils.pro_exception import ProException




class Unify_Special_price(PromotionEntity):

    def __init__(self,obj):
        super().__init__(obj)
        # 参加统一特价的商品
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

        # 特价值
        self.special_price = obj["specific_activities"][0]["operation_set"][0]["special_offer_value"]


