# -*- coding:utf-8 -*-
# author:${尹晨}
# datetime:2018/9/26 14:19
# software: PyCharm
from pro.apis.entitys.GA_entitys.promotion_entity import PromotionEntity
from pro.utils.pro_exception import ProException

# 组合折扣模板类
class CombinationDiscountEntity(PromotionEntity):
    def __init__(self, obj):
        super().__init__(obj)

        #优惠商品（不为空该商品参与计算的）--20190411--hexiaoxia
        self.execute_product_list =[]
        if obj["specific_activities"][0].get("execute_product_list"):
            self.execute_product_list=set(obj["specific_activities"][0].get("execute_product_list"))

        # 组合条件
        self.rela_symb_type = obj['rela_symb_type']
        # 每条组合记录
        self.specific_activities = []
        if len(obj['specific_activities']) >= 1:
            for bean in obj['specific_activities']:
                self.specific_activities.append(SpecificActivities(bean))
        else:
            raise ProException("组合活动比较条件为空")

    def __str__(self):
        return str(self.__dict__)


class SpecificActivities(object):
    def __init__(self, obj):
        # 参加组合打折的商品集合
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
        # 组合折扣值
        if float(obj['operation_set'][0]['discount_value']) > 1:
            raise ProException("discount_value折扣率不能大于1")
        self.discount_value = float(obj['operation_set'][0]['discount_value'])
        ##组合位置
        # self.combination_sign = obj['combination_sign']

    def __str__(self):
        return str(self.__dict__)
