# -*- coding:utf-8 -*-
# author:何小霞
# datetime:2018/9/28 10:28

from pro.utils.pro_exception import ProException
from pro.utils import util


class PromotionEntity(object):
    def __init__(self, obj):
        if obj['prom_type_two'] is None or not obj['prom_type_two']  or (obj['prom_type_two'] not in range(1, 7)):
            raise ProException("活动二类prom_type_two为空或非法")
        self.prom_type_two = obj['prom_type_two']  # 【销售类型】来源字段选项组值 --2019-07-16

        # 区分是否可叠加的二类编码--2019-07-16
        try:
            if obj['prom_type_two_code'] is None:
                self.prom_type_two_code = str(self.prom_type_two)
            else:
                self.prom_type_two_code = obj['prom_type_two_code']  # 二类编码
        except:
            self.prom_type_two_code = str(self.prom_type_two)  # 没有新的二类字段就当是原来的逻辑就是使用上面的促销类型来区分叠加的，这样可以兼容前端功能新功能没有部署但是同一套引擎也可以同时使用

        if obj['prom_type_three'] is None  or not obj['prom_type_three']:
            raise ProException("活动三类ID为空")
        self.prom_type_three = obj['prom_type_three']  # 三类id

        if obj['ename'] is None  or not obj['ename']:
            raise ProException("活动名称为空")
        self.ename = obj['ename']  # 活动名称

        if obj['prom_type_two_c'] is None  or not obj['prom_type_two_c']:
            raise ProException("二类活动级别为空")
        self.prom_type_two_c = int(obj['prom_type_two_c'])  # 活动级别

        if obj['publish_date'] is None or not obj['publish_date'] or int(obj['publish_date']) < 0:
            raise ProException("活动发布时间不正确")
        self.publish_date = int(obj['publish_date'])  # 活动发布时间

        # if obj['members_only'] is None or not obj['members_only'] or (str(obj['members_only']).lower() != 'y' and str(obj['members_only']).lower() != 'n'):
        #     raise ProException("members_only参数不正确")
        # 是否仅会员参加
        if obj.get("members_only") and str(obj['members_only']).lower() == 'y':
            self.members_only = True
        else:
            self.members_only = False

        if self.members_only:
            if obj['members_group'] is None or len(obj['members_group']) < 1:
                raise ProException("会员等级列表为空")
            else:
                self.members_group = obj['members_group']  # 会员等级列表


        if obj['is_run_store_act'] is None or not obj['is_run_store_act'] or (str(obj['is_run_store_act']).lower() != 'y' and str(obj['is_run_store_act']).lower() != 'n'):
            self.is_run_store_act = "N"
            #raise ProException("is_run_store_act参数不正确")
        else:
            # 是否与其它全场活动同时执行
            self.is_run_store_act = obj.get('is_run_store_act', "N")

        # if obj['is_run_vip_discount'] is None or not obj['is_run_vip_discount'] or (str(obj['is_run_vip_discount']).lower() != 'y' and str(obj['is_run_vip_discount']).lower() != 'n'):
        #     raise ProException("is_run_vip_discount参数不正确")
        # 是否享受vip折上折
        if obj.get("is_run_vip_discount") and str(obj['is_run_vip_discount']).lower() == 'y':
            self.is_run_vip_discount = True
        else:
            self.is_run_vip_discount = False

        if obj['max_times'] is None:
            self.max_times = 0
        else:
            self.max_times = obj['max_times']  # 最大翻倍条件

        if obj['id'] is None or not obj['id']:
            raise ProException("id参数不正确")
        self.id = obj['id']    #活动唯一id值

        #执行促销活动使用的计算值：AMT_LIST：吊牌金额、AMT_RETAIL：零售金额、AMT_RECEIVABLE：应收金额
        self.target_item=obj.get("target_item","amt_receivable").lower()

        # 参与全场活动的商品筛选
        self.specific_target_type = str(obj['specific_activities'][0]['specific_target_type']).lower()  # 条件amt_receivable：应收金额     discount：折扣
        self.comp_symb_type = str(obj['specific_activities'][0]['comp_symb_type']).lower()  # 比较符"GE/G/E"
        self.value_num = obj['specific_activities'][0]['value_num']  # 比较值

        # 优惠具体活动信息
        self.target_type = obj['specific_activities'][0]['target_type'].lower()  # 满足的条件 qtty：数量  amt_list：吊牌金额  amt_retail：零售金额  amt_receivable：应收金额
        self.operation_set = obj['specific_activities'][0]['operation_set']  # 具体优惠方案集合
        self.pitem_id = obj['specific_activities'][0].get("pitem_id")
        # 集合
        self.specific_activities = []
        if str(self.prom_type_two)=="4":
            for bean in obj['specific_activities']:
                rowspe = SpecificActivities(bean)
                rowspe.max_times = obj["max_times"]
                self.specific_activities.append(rowspe)

    def __str__(self):
        return str(self.__dict__)

class SpecificActivities(object):
    def __init__(self, obj):
        # 比较符"GE/G/E"
        comp_symb_type = str(obj['operation_set'][0]['comp_symb_type']).lower()
        if comp_symb_type is None or (comp_symb_type != 'g' and comp_symb_type != 'ge' and comp_symb_type != "e"):
            raise ProException("comp_symb_type为空或非法")
        self.comp_symb_type = comp_symb_type
        self.value_num = obj['operation_set'][0].get('value_num',1)
        self.pitem_id = obj.get("pitem_id", 1)
        # 比较执行项/赠品集合
        self.operation_set = []

        if not obj['operation_set']:
            raise ProException("线上梯度比较项为空")

        # 添加各个比较项
        for i in obj['operation_set']:
            k = OperationList(i)
            self.operation_set.append(k)

    def __str__(self):
        return str(self.__dict__)


class OperationList(object):
    def __init__(self, obj):

        # 赠送的商品
        self.buygift_product = []
        self.give_value = 0
        if "buy_gifts" in obj:
            self.buygift_product = obj["buy_gifts"]["product_list"]

            # 赠送数量
            self.give_value = int(obj["buy_gifts"]["give_value"])

        self.pcond_id = obj.get("pcond_id", 1)

    def __str__(self):
        return str(self.__dict__)
