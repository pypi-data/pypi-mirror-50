# -*- coding:utf-8 -*-
# author:hexiaoxia
# datetime:2019/4/26 10:13
# software: PyCharm
from pro.apis.entitys.GA_entitys.promotion_entity import PromotionEntity
from pro.utils.pro_exception import ProException

# 组合买赠模板类
class Combination_buygiftEntity(PromotionEntity):
    def __init__(self, obj):
        super().__init__(obj)

        # 组合条件
        self.rela_symb_type = obj['rela_symb_type']
        # 每条组合记录
        self.specific_activities = []
        if len(obj['specific_activities']) >= 1:
            for bean in obj['specific_activities']:
                rowspe=buygiftSpecificActivities(bean)
                rowspe.max_times=obj["max_times"]
                self.specific_activities.append(rowspe)
        else:
            raise ProException("组合买赠活动比较条件为空")

        # 赠送商品集合
        if obj["specific_activities"][0]["operation_set"][0]["buy_gifts"]["product_list"]:
            try:
                self.buygift_product = obj["specific_activities"][0]["operation_set"][0]["buy_gifts"]["product_list"]
            except Exception as e:
                raise ProException("组合买赠未设置赠送商品")
        else:
            raise ProException("组合买赠未设置赠送商品")

        # 赠送数量
        self.give_value = 1
        try:
            self.give_value=int(obj['specific_activities'][0]['operation_set'][0]["buy_gifts"]["give_value"])
        except Exception as e:
            pass

    def __str__(self):
        return str(self.__dict__)


class buygiftSpecificActivities(object):
    def __init__(self, obj):
        # 参加组合买赠的商品集合
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

        #最大翻倍次数，组合中每个对像项都是一样的
        self.max_times = 0

    def __str__(self):
        return str(self.__dict__)
