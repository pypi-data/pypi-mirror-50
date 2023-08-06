# encoding=utf-8
"""
 author:${何小霞}
 datetime:2018/9/30 10:42
 software: PyCharm
 全场活动具体条件和优惠项模板类
"""

from pro.apis.entitys.PA_entitys.promotion_entity import PromotionEntity


class UnifyDiscountEntity(PromotionEntity):
    def __init__(self, obj):
        super().__init__(obj)
        #参与全场活动的商品筛选
        self.specific_target_type = str(obj['specific_activities'][0]['specific_target_type']).lower() # 条件amt_receivable：应收金额     discount：折扣
        self.comp_symb_type = str(obj['specific_activities'][0]['comp_symb_type']).lower() # 比较符"GE/G/E"
        self.value_num = obj['specific_activities'][0]['value_num'] # 比较值

        #优惠具体活动信息
        self.target_type = obj['specific_activities'][0]['target_type'] # 满足的条件 qtty：数量  amt_list：吊牌金额  amt_retail：零售金额  amt_receivable：应收金额
        self.operation_set = obj['specific_activities'][0]['operation_set'] # 具体优惠方案集合
    def __str__(self):
        return str(self.__dict__)