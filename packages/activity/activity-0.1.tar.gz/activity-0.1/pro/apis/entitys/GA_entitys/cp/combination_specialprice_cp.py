#!/usr/bin/env python
"""

   encoding: utf-8
   2018/12/26 2:26 PM
   
  
   by李博文
"""


from pro.apis.entitys.GA_entitys.promotion_entity import PromotionEntity
from pro.utils.pro_exception import ProException



# 组合特价换购模板类
class Combination_Specialprice_Cp(PromotionEntity):
    def __init__(self, obj):
        super().__init__(obj)
        # 组合条件
        self.rela_symb_type = obj['rela_symb_type']
        # 每条组合记录
        self.specific_activities = []
        n = 0
        if len(obj['specific_activities']) >= 1:
            for bean in obj['specific_activities']:
                rowspe = SpecificActivities(bean)
                rowspe.max_times = obj["max_times"]
                self.specific_activities.append(rowspe)
        else:
            raise ProException("组合活动比较条件为空")


        # 换购条件集合
        self.operation_set = []
        if not obj['specific_activities'][0]['operation_set']:
            raise ProException("换购条件为空")

        for i in obj['specific_activities'][0]['operation_set']:
            k = OperationList(i)
            self.operation_set.append(k)

    def __str__(self):
        return str(self.__dict__)


class SpecificActivities(object):
    def __init__(self, obj):

        # 参加组合打折换购的商品集合
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


    def __str__(self):
        return str(self.__dict__)

class OperationList(object):
    def __init__(self, obj):

        # 组合特价的换购值
        self.purchase_condition = obj["redemption"]["purchase_condition"]

        # 换购商品数量
        self.give_value = obj["redemption"]["give_value"]

        # 可以参见换购商品的集合
        self.product_list = obj["redemption"]["product_list"]
        if not obj["pcond_id"]:
            raise ProException("换购执行明细ID未传入")
        # 换购执行明细ID
        self.pcond_id = obj["pcond_id"]

    def __str__(self):
        return str(self.__dict__)