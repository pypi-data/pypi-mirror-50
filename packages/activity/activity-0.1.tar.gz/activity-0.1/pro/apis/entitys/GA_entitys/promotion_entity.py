# encoding=utf-8

from pro.utils.pro_exception import ProException
from pro.utils import util


class PromotionEntity(object):
    def __init__(self, obj):
        # 该值对应来源修改，来源字段选项组值【促销类型】--2019-07-08
        try:
            if obj['prom_type_two'] is None or (int(obj['prom_type_two']) not in range(1, 7)):
                raise ProException("活动二类ID为空或非法")
            self.prom_type_two = obj['prom_type_two']  # 二类id
        except:
            raise ProException("找不到prom_type_two或ID值非法")

        #区分是否可叠加的二类编码--2019-07-08
        try:
            if obj['prom_type_two_code'] is None :
                self.prom_type_two_code = str(self.prom_type_two)
            else:
                self.prom_type_two_code = obj['prom_type_two_code']  # 二类编码
        except:
            self.prom_type_two_code =str(self.prom_type_two)  #没有新的二类字段就当是原来的逻辑就是使用上面的促销类型来区分叠加的，这样可以兼容前端功能新功能没有部署但是同一套引擎也可以同时使用

        if 'prom_type_three' not in obj:
            raise ProException("prom_type_three is null")
        if obj['prom_type_three'] is None:
            raise ProException("活动三类ID为空")
        self.prom_type_three = str(obj['prom_type_three']).lower()  # 三类id

        if 'ename' not in obj:
            raise ProException("ename is null")
        if obj['ename'] is None:
            raise ProException("活动名称为空")
        self.ename = obj['ename']  # 活动名称

        if 'prom_type_two_c' not in obj:
            raise ProException("prom_type_two_c is null")
        if obj['prom_type_two_c'] is None:
            raise ProException("二类活动级别为空")
        self.prom_type_two_c = int(obj['prom_type_two_c'])  # 活动级别

        try:
            if obj['publish_date'] is None or int(obj['publish_date']) < 0:
                raise ProException("活动发布时间不正确")
            self.publish_date = int(obj['publish_date'])  # 活动发布时间
        except:
            raise ProException("publish_date is null 或 value 非法")

        # if 'members_only' not in obj:
        #     raise ProException("members_only is null")
        # if obj['members_only'] is None or (
        #         str(obj['members_only']).lower() != 'y' and str(obj['members_only']).lower() != 'n'):
        #     raise ProException("members_only参数不正确")
        #
        # if 'members_only' not in obj:
        #     raise ProException("members_only is null")
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

        # if obj['is_run_other_pro'] is None or (
        #         str(obj['is_run_other_pro']).lower() != 'y' and str(obj['is_run_other_pro']).lower() != 'n'):
        #     raise ProException("is_run_other_pro参数不正确")

        # 是否与其他商品活动同时执行
        if obj.get("is_run_other_pro") and str(obj['is_run_other_pro']).lower() == 'y':
            self.is_run_other_pro = True
        else:
            self.is_run_other_pro = False

        # if obj['is_run_store_act'] is None or (
        #         str(obj['is_run_store_act']).lower() != 'y' and str(obj['is_run_store_act']).lower() != 'n'):
        #     raise ProException("is_run_other_pro参数不正确")
        # 是否与全场活动同时执行
        if obj.get("is_run_store_act") and str(obj['is_run_store_act']).lower() == 'y':
            self.is_run_store_act = True
        else:
            self.is_run_store_act = False

        # if obj['is_run_vip_discount'] is None or (
        #         str(obj['is_run_vip_discount']).lower() != 'y' and str(obj['is_run_vip_discount']).lower() != 'n'):
        #     raise ProException("is_run_other_pro参数不正确")
        # 是否享受vip折上折
        if obj.get("is_run_vip_discount") and str(obj['is_run_vip_discount']).lower() == 'y':
            self.is_run_vip_discount = True
        else:
            self.is_run_vip_discount = False

        if obj['max_times'] is None:
            self.max_times = 0
        else:
            self.max_times = obj['max_times']  # 最大翻倍条件

        # 优惠价格基础,默认值按 amt_receivable 应收价
        if obj['target_item'] is None:
            self.target_item="amt_receivable"
        else:
            self.target_item = str(obj['target_item']).lower()
        if self.target_item != "amt_receivable" and self.target_item != "amt_retail" and self.target_item != "amt_list":
            self.target_item = "amt_receivable"

        if obj['id'] is None:
            raise ProException("id参数不正确")
        self.id = obj['id']  # 活动唯一id值

    def __str__(self):
        return str(self.__dict__)
