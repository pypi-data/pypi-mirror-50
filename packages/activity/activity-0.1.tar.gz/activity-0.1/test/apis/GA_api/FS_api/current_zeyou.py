"""
    特价商品择优计算单元测试
    2018/11/14
    by李博文
"""

from pro.apis.GA_api.SO_api.current_zeyou import current_zeyou

import unittest


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


class ProductMock1(object):
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
        self.amt_receivable = 80

        # 数量
        self.qtty = 5

        # 循环判断优惠数量是否变化--值
        self.qttyCount = self.qtty

        self.productSeatList = []
        if self.qtty > 0:
            for i in range(self.qtty):
                self.productSeatList.append(SeatMock1())
        # 当前三类中未占位的数量


class BeanMock(object):

    def __init__(self):
        self.notProId = None

        self.is_run_other_pro = True

        self.target_item = "amt_list"

        self.is_run_vip_discount = None

        self.is_run_other_pro = True

        self.is_run_store_act = True

        self.special_price = 80

        self.ename = "刘志洋"

        self.id = 1

        self.max_times = 2

        self.value_num = 300

        self.comp_symb_type = "ge"


class SeatMock1(object):
    def __init__(self) -> None:
        # 商品编码
        self.ecode = "ecode"
        # 吊牌价
        self.amt_list = 120
        # 零售价
        self.amt_retail = 90
        # 应收价
        self.amt_receivable = 80
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


class UsefInfoMock(object):
    def __init__(self):
        self.id = 1
        self.discount = 0.8


class Test_cureent_zeyou(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.productMock = ProductMock()
        self.productMock1 = ProductMock1()

    def test_zeyou(self):
        product_list = [[self.productMock, self.productMock], [self.productMock1, self.productMock1]]
        response = current_zeyou(product_list)


        self.assertEqual(response[0].productSeatList[0].amt_receivable, 80)
