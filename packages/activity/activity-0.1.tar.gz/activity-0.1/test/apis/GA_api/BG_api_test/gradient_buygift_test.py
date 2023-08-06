# -*- coding:utf-8 -*-
"""
    单元测试
    2018/11/4
    by李博文
"""

from pro.apis.GA_api.BG_api import basics_bg
from pro.apis.GA_api.BG_api import gradient_buygift
from pro.apis.GA_api.BG_api import current_promotions_preferential
import unittest

# 当前商品明细
class SeatMock(object):
    def __init__(self):
        self.is_buy_gifts = "n"
        # 占位
        self.seat = False
        # 判断当前商品是否可以跟其他活动同时进行进行
        self.is_run_other_pro = True
        self.ecode = "ecode"
        # 是否可以进行全场活动
        self.is_run_store_act = True
        # 记录当前活动id
        self.discountId = set()

        self.amt_retail = 80
        # 是否参加个vip折中折
        self.is_run_vip_discount = False

        # 应收价
        self.amt_receivable = 78.2
        # 记录折扣
        self.discountPrice = []
        self.amt_list = 78.2

# 当前商品
class ProductMock(object):
    def __init__(self):
        self.qtty = 11
        self.productSeatList = []
        self.discountId = set()
        self.qttyCount = self.qtty
        self.ecode = "ecode"
        if self.qtty > 0:
            for i in range(self.qtty):
                self.productSeatList.append(SeatMock())
        # 当前二类中未占位的商品的数量
    def notOccupiedOne(self):
        sum = 0
        for bean in self.productSeatList:
            if bean.is_run_other_pro:
                sum = sum + 1
        return sum

    # 当前三类中未占位的数量
    def notOccupiedThree(self):
        sum = 0
        for bean in self.productSeatList:
            if bean.seat == False:
                sum = sum + 1

        return sum

    # 当前未占位商品的总吊牌价
    def getCountAmtList(self):
        sum = 0
        for bean in self.productSeatList:
            if bean.is_run_other_pro and bean.seat == False:
                sum += bean.amt_list
        return sum

    # 当前未占位商品的总零售价
    def getCountAmtRetail(self):
        sum = 0
        for bean in self.productSeatList:
            if bean.is_run_other_pro and bean.seat == False:
                sum += bean.amt_retail
        return sum

    # 当前未占位商品的总应收价
    def getCountAmtReceivable(self):
        sum = 0
        for bean in self.productSeatList:
            if bean.is_run_other_pro and bean.seat == False:
                sum += bean.amt_receivable
        return sum

    class UserInfo(object):
        def __init__(self):
            self.discount = 0.8
            self.id = 1


class PromotionMock(object):
    def __init__(self,value_num):
        self.id = 1
        self.is_run_other_pro = True
        self.is_run_store_act = True
        self.target_item = "amt_list"
        # 当前活动是否可以参加vip
        self.is_run_vip_discount = True

        # 参加梯度买赠的商品
        self.product_list = ['as001', 'as002']

        # 梯度买赠条件集合
        self.operation_set = [Bean_Mock(value_num),Bean_Mock(value_num),Bean_Mock(value_num)]
        # 满足条件 qtty：数量  amt_list：吊牌金额  amt_retail：零售金额  amt_receivable：应收金额
        self.members_only = False


        self.target_type = "qtty"

# 当前活动
class Bean_Mock(object):
    def __init__(self,value_num):
        self.id = 1
        self.is_run_other_pro = True
        self.is_run_store_act = True
        self.target_item = "amt_list"
        # 当前活动是否可以参加vip
        self.is_run_vip_discount = True

        self.members_only = True


        self.comp_symb_type = "ge"


        # 赠送的商品
        self.buygift_product = [{'ecode': 'ecode', 'amt_list': 123}]

        # 比较值
        self.value_num = value_num

        # if not type(obj['specific_activities'][0]['operation_set'][0]["buy_gifts"]["give_value"]) == int:
        # raise ProException("赠送数量非int")

        # 赠送数量
        self.gift_number = 1
        # 翻倍
        self.max_times = 2
        self.members_group = [1,2,3]

class UserInfoMock(object):
    def __init__(self):
        self.discount = 0.8
        self.id = 1
# 不存在买A赠A的商品
class NotProductMock(object):
    def __init__(self):
        self.qtty = 11
        self.productSeatList = []
        self.discountId = set()
        self.qttyCount = self.qtty
        self.ecode = "ecode"
        if self.qtty > 0:
            for i in range(self.qtty):
                self.productSeatList.append(SeatMock())
    def notOccupiedThree(self):
        sum = 0
        for bean in self.productSeatList:

            if bean.seat == False:
                sum = sum + 1

        return sum
    # 当前未占位商品的总吊牌价
    def getCountAmtList(self):
        sum = 0
        for bean in self.productSeatList:
            if bean.is_run_other_pro and bean.seat == False:
                sum += bean.amt_list
        return sum
    # 当前未占位商品的总零售价
    def getCountAmtRetail(self):
        sum = 0
        for bean in self.productSeatList:
            if bean.is_run_other_pro and bean.seat == False:
                sum += bean.amt_retail
        return sum
    # 当前未占位商品的总应收价
    def getCountAmtReceivable(self):
        sum = 0
        for bean in self.productSeatList:
            if bean.is_run_other_pro and bean.seat == False:
                sum += bean.amt_receivable
        return sum

# 测试梯度买A赠A
class Test_condition_qtty(unittest.TestCase):

    @classmethod
    def setUp(self):
        # 商品明细对象
        self.seatMock = SeatMock()
        # 商品活动对象
        self.productMock = ProductMock()
        # 当前活动详细
        self.beanMock = Bean_Mock(3)
        # 当前活动
        self.promotionMock = PromotionMock(3)

        self.userinfoMock = UserInfoMock()

        self.response = basics_bg.condition_qtty(self.beanMock,self.productMock,self.productMock,self.userinfoMock)

    def test_condition_qtty(self):
        print(self.response)
        self.assertIsNone(self.response)
class Test_condition_amt_list(unittest.TestCase):

    @classmethod
    def setUp(self):
        # 商品明细对象
        self.seatMock = SeatMock()
        # 商品活动对象
        self.productMock = ProductMock()
        # 当前活动详细
        self.beanMock = Bean_Mock(100)
        # 当前活动
        self.promotionMock = PromotionMock(100)

        self.userinfoMock = UserInfoMock()

        self.response = basics_bg.condition_amt_list(self.beanMock,self.productMock,self.promotionMock,self.userinfoMock)

    def test_condition_amt_list(self):
        print(self.response)
        self.assertEqual(self.response,1)

class Test_buy_a_give_a(unittest.TestCase):

    @classmethod
    def setUp(self):
        # 商品明细对象
        self.seatMock = SeatMock()
        # 商品活动对象
        self.productMock = ProductMock()
        self.productMock_list = [self.productMock]
        # 当前活动详细
        self.beanMock = Bean_Mock(100)
        # 当前活动
        self.promotionMock = PromotionMock(100)

        self.userinfoMock = UserInfoMock()
        self.response = basics_bg.buy_a_give_a(self.beanMock,self.promotionMock,self.userinfoMock,self.productMock_list)
    def test_buy_a_give_a(self):
        print(self.response)
        self.assertEqual(self.response,"-1")


# 测试入口
class Test_gradient_buygift(unittest.TestCase):

    @classmethod
    def setUp(self):
        # 商品明细对象
        self.seatMock = SeatMock()
        # 商品活动对象
        self.productMock = ProductMock()
        self.productMock_list = [self.productMock]
        # 当前活动详细
        self.beanMock = Bean_Mock(100)
        # 当前活动
        self.promotionMock = PromotionMock(100)

        self.userinfoMock = UserInfoMock()
        self.response = gradient_buygift.gradient_buygift(self.productMock_list,self.promotionMock,self.userinfoMock)

    def test_gradient_buygift(self):
        print(self.response)
        self.assertIsNotNone(self.response)





