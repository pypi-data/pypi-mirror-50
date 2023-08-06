# -*- coding:utf-8 -*-
# author:weiyanping
# datetime:2019/7/9 11:09
# software: PyCharm

from pro.apis.entitys.GA_entitys.promotion_entity import PromotionEntity
from pro.utils.pro_exception import ProException

class Unify_BuyGift_Online(PromotionEntity):
    def __init__(self,obj):
        super().__init__(obj)

        # 参加统一买赠的商品
        self.product_list = obj['specific_activities'][0]['product_list']

        # 满足条件
        self.target_type = str(obj['specific_activities'][0]['target_type']).lower()

        # 买赠条件集合
        self.operation_set = []
        if not obj['specific_activities'][0]['operation_set']:
            raise ProException("线上买赠条件为空")
        # 比较符
        comp_symb_type = str(obj['specific_activities'][0]['operation_set'][0]['comp_symb_type']).lower()
        if comp_symb_type is None or (comp_symb_type != 'g' and comp_symb_type != 'ge' and comp_symb_type != "e"):
            raise ProException("comp_symb_type为空或非法")
        self.comp_symb_type = comp_symb_type.lower()

        # 比较值
        self.value_num = obj['specific_activities'][0]['operation_set'][0]['value_num']
        self.pitem_id = obj['specific_activities'][0].get("pitem_id", 1)
        for i in obj['specific_activities'][0]['operation_set']:
            k = OperationList(i)
            self.operation_set.append(k)

    def __str__(self):
        return str(self.__dict__)

class OperationList(object):
    def __init__(self, obj):

        # 赠品数量
        self.give_value = obj["buy_gifts"]["give_value"]

        # 可以参与买赠商品的集合
        self.buygift_product = obj["buy_gifts"]["product_list"]

        # 买赠执行明细ID
        self.pcond_id = obj.get("pcond_id", 1)

    def __str__(self):
        return str(self.__dict__)