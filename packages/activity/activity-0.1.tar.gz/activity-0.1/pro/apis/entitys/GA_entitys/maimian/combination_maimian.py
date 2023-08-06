# -*- coding:utf-8 -*-
# author:weiyanping
# datetime:2019/4/23 19:00
# software: PyCharm

from pro.apis.entitys.GA_entitys.promotion_entity import PromotionEntity
from pro.utils.pro_exception import ProException

# 组合买免模板类
class CombinationMaimian(PromotionEntity):
    def __init__(self, obj):
        super().__init__(obj)

        # 组合条件
        self.rela_symb_type = obj['rela_symb_type']
        # 每条组合条件
        self.specific_activities = []
        if len(obj['specific_activities']) >= 1:
            for bean in obj['specific_activities']:
                self.specific_activities.append(MaimianSpecificActivities(bean))
        else:
            raise ProException("组合买免活动比较条件为空")

        # 组合满减值
        if obj["specific_activities"][0]['operation_set'][0].get("buy_from"):
            try:
                self.buy_from_value = float(obj["specific_activities"][0]['operation_set'][0]['buy_from'])
            except Exception as e:
                raise ProException("组合买免未设置正确的买免值")
        else:
            raise ProException("组合买免未设置正确的买免值")

    def __str__(self):
        return str(self.__dict__)


class MaimianSpecificActivities(object):
    def __init__(self, obj):
        # 每个比较行，参加活动的商品集合
        self.product_list = set(obj['product_list'])

        # 满足活动的条件 qtty：数量
        self.target_type = str(obj['target_type']).lower()

        # 比较符"GE/G/E"
        comp_symb_type = str(obj['operation_set'][0]['comp_symb_type']).lower()

        if comp_symb_type is None or (comp_symb_type != 'g' and comp_symb_type != 'ge' and comp_symb_type != "e"):
            raise ProException("comp_symb_type为空或非法")

        self.comp_symb_type = comp_symb_type
        # 比较值
        self.value_num = obj['operation_set'][0]['value_num']


    def __str__(self):
        return str(self.__dict__)
