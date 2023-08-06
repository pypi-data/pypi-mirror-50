# -*- coding:utf-8 -*-
"""
    统一买赠模板
    2018/10/23
    by李博文
"""
from pro.apis.entitys.GA_entitys.promotion_entity import PromotionEntity
from pro.utils.pro_exception import ProException

class Unify_BuyGift(PromotionEntity):
    def __init__(self,obj):
        super().__init__(obj)

        # 参加统一买赠的商品
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

        # 赠送的商品
        self.buygift_product = obj["specific_activities"][0]["operation_set"][0]["buy_gifts"]["product_list"]




        # 赠送数量
        self.give_value = int(obj['specific_activities'][0]['operation_set'][0]["buy_gifts"]["give_value"])

    def __str__(self):
        return str(self.__dict__)

