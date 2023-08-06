# -*- coding:utf-8 -*-
# author:hexiaoxia
# datetime:2019/4/12 11:20
# software: PyCharm
from pro.apis.entitys.GA_entitys.promotion_entity import PromotionEntity
from pro.utils.pro_exception import ProException

# 组合特价模板类
class Combination_Special_SpriceEntity(PromotionEntity):
    def __init__(self, obj):
        super().__init__(obj)

        # 组合条件
        self.rela_symb_type = obj['rela_symb_type']
        # 每条组合记录
        self.specific_activities = []
        if len(obj['specific_activities']) >= 1:
            for bean in obj['specific_activities']:
                self.specific_activities.append(SpecialSpriceSpecificActivities(bean))
        else:
            raise ProException("组合特价活动比较条件为空")

        # 组合特价值
        if obj["specific_activities"][0]['operation_set'][0]['special_offer_value']:
            try:
                self.special_price = float(obj["specific_activities"][0]['operation_set'][0]['special_offer_value'])
            except Exception as e:
                raise ProException("组合特价未设置正确的特价值")
        else:
            raise ProException("组合特价未设置正确的特价值")

    def __str__(self):
        return str(self.__dict__)


class SpecialSpriceSpecificActivities(object):
    def __init__(self, obj):
        # 参加组合特价的商品集合
        self.product_list = set(obj['product_list'])
        # 满足活动的条件 qtty：数量  amt_list：吊牌金额  amt_retail：零售金额  amt_receivable：应收金额
        self.target_type = str(obj['target_type']).lower()
        # 比较符"GE/G/E"
        comp_symb_type = str(obj['operation_set'][0]['comp_symb_type']).lower()
        if comp_symb_type is None or (comp_symb_type != 'g' and comp_symb_type != 'ge' and comp_symb_type != "e"):
            raise ProException("comp_symb_type为空或非法")
        self.comp_symb_type = comp_symb_type
        # 比较值
        self.value_num = obj['operation_set'][0]['value_num']

        ##组合位置
        # self.combination_sign = obj['combination_sign']

    def __str__(self):
        return str(self.__dict__)
