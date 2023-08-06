# -*- coding:utf-8 -*-
"""
    统一买赠模板
    2018/11/12
    by李博文
"""

from pro.apis.entitys.GA_entitys.promotion_entity import PromotionEntity
from pro.utils.pro_exception import ProException


class Unify_Maimian(PromotionEntity):
    def __init__(self, obj):
        super().__init__(obj)

        if obj['specific_activities'][0]['product_list'] is None:
            raise ProException("商品列表不能为空")
        # 参加买免的商品
        self.product_list = obj['specific_activities'][0]['product_list']

        # target_tyep = str(obj['specific_activities'][0]['target_type']).lower()
        # if target_tyep != "qtty":
        #     raise ProException("买免必须是数量")
        #  满足条件
        # self.target_type = str(obj['specific_activities'][0]['target_type']).lower()

        # 比较符
        comp_symb_type = str(obj['specific_activities'][0]['operation_set'][0]['comp_symb_type']).lower()
        if comp_symb_type is None or (comp_symb_type != 'g' and comp_symb_type != 'ge' and comp_symb_type != "e"):
            raise ProException("comp_symb_type为空或非法")
        self.comp_symb_type = comp_symb_type.lower()

        # 比较值
        self.value_num = obj['specific_activities'][0]['operation_set'][0]['value_num']

        # 买免值
        self.buy_from_value = obj['specific_activities'][0]['operation_set'][0]["buy_from"]