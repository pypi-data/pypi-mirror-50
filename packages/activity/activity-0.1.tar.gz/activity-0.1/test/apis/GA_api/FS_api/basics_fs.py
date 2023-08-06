"""
    基础运算买赠单元测试
    2018/11/13
    by李博文
"""
import unittest

from pro.apis.GA_api.SO_api.basics_fs import basics_one
from pro.apis.GA_api.SO_api.basics_fs import condition_moeny, condition_qtty


class ProductMock(object):
    """
    模拟类
    """

    def __init__(self) -> None:
        # 可参加的活动
        self.discountId = set()

        self.ecode = 'ecode'

        # 吊牌金额
        self.amt_list = 120

        # 零售金额
        self.amt_retail = 90

        # 应收金额
        self.amt_receivable = 90

        # 数量
        self.qtty = 5

        # 循环判断优惠数量是否变化--值
        self.qttyCount = self.qtty

        self.productSeatList = []

        if self.qtty > 0:
            for i in range(self.qtty):
                self.productSeatList.append(SeatMock())
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


class SeatMock(object):
    def __init__(self) -> None:
        # 商品编码
        self.ecode = "ecode"
        # 吊牌价
        self.amt_list = 120
        # 零售价
        self.amt_retail = 90
        # 应收价
        self.amt_receivable = 90
        # 最原始的应收价，用于计算商品活动优惠金额使用
        self.upamt_receivable = 90

        self.qtty = 1
        # 是否占位
        self.seat = False
        # 是否可以进行下次商品活动
        self.is_run_other_pro = True
        # 是否可以进行全场活动
        self.is_run_store_act = True
        # 记录优惠过程
        self.str_discount = '商品' + self.ecode
        # 参加商品的活动id集合
        self.discountId = []
        # 参加商品活动优惠的金额
        self.discountPrice = []
        # 是否参加过VIP折上折  true为参加过
        self.is_run_vip_discount = False

        self.discountPrice = []

        self.discountId = []

        self.notProId = False


class BeanMock(object):

    def __init__(self, tiaojian, bijiaozhi):
        self.notProId = None

        self.is_run_other_pro = True

        self.target_item = tiaojian

        self.is_run_vip_discount = None

        self.is_run_other_pro = True

        self.is_run_store_act = True

        self.special_price = 80

        self.ename = "刘志洋"

        self.id = 1

        self.max_times = 2

        self.value_num = bijiaozhi

        self.comp_symb_type = "ge"


class UsefInfoMock(object):
    def __init__(self):
        self.id = 1
        self.discount = 0.8


class Test_basics(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.productMock = ProductMock()
        self.userinfo = UsefInfoMock()
        self.seatMock = SeatMock()
        self.beanMock = BeanMock("amt_list", 300)
        # self.response = basics_one(seatMock, productMock, beanMock, userinfo)

    def test_amt_receivadiscountPriceble(self):
        # self.assertEqual(seatMock.amt_receivable,80)
        # self.assertIsNotNone(self.seatMock.str_discount)
        # print(self.seatMock.str_discount)
        basics_one(self.seatMock, self.productMock, self.beanMock, self.userinfo)
        # 应收价
        self.assertEqual(self.seatMock.amt_receivable, 80)

        # 是否全场进行
        self.assertEqual(self.seatMock.is_run_other_pro, True)

        # 商品已站位
        self.assertEqual(self.seatMock.seat, True)

        # 记录活动id
        self.assertEqual(self.seatMock.discountId, [1])

        # 记录优惠金额
        self.assertEqual(self.seatMock.discountPrice, [40])


class Test_condition_moeny(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.productMock = ProductMock()
        self.userinfo = UsefInfoMock()
        self.seatMock = SeatMock()
        self.beanMock = BeanMock("amt_list", 300)

    def test_condition_moeny(self):
        condition = "amt_list"
        promotion = 1200
        productListA = [self.productMock, self.productMock]
        response = condition_moeny(self.beanMock, self.userinfo, productListA, promotion, condition)
        self.assertIsNone(response)


class Test_condition_qtty(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.productMock = ProductMock()
        self.userinfo = UsefInfoMock()
        self.seatMock = SeatMock()
        self.beanMock = BeanMock("qtty",4)

    def test_condition_qtty(self):
        productListA = [self.productMock, self.productMock]
        response = condition_qtty(self.beanMock, self.userinfo, productListA, 10)
        self.assertIsNone(response)
