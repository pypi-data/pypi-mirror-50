# -*- coding:utf-8 -*-
"""
    单元测试
    2018/11/3
    by李博文
"""

import unittest
import copy

from pro.apis.GA_api.BG_api import unify_buygift
from pro.apis.GA_api.BG_api import basics_bg



class Test_one_buy_product(unittest.TestCase):
    """
    测试更改赠品
    """
    @classmethod
    def setUp(self):
        class ProductMock(object):
            def __init__(self):
                self.qttyCount = 3
        class SeatMock(object):
            def __init__(self):
                self.is_buy_gifts = "n"

        self.productMock = ProductMock()
        self.seatMock = SeatMock()
        basics_bg.one_buy_product(self.seatMock,self.productMock)

    def test_qttyCount(self):
        # 测试总数量减1
        print(self.productMock.qttyCount)
        self.assertEqual(self.productMock.qttyCount,2)


    def test_qttyCount1(self):
        # 测试更改赠品属性值
        print(self.seatMock.is_buy_gifts)
        self.assertEqual(self.seatMock.is_buy_gifts,"y")



class Test_basics_one(unittest.TestCase):
    # 测试更改每一件商品属性
    @classmethod
    def setUp(self):
        # 商品明细
        class SeatMock(object):
            def __init__(self):
                self.is_buy_gifts = "n"
                # 不可以进行商品活动
                self.seat = False
                # 判断当前商品是否可以跟其他活动同时进行进行
                self.is_run_other_pro = True
                # 是否可以进行全场活动
                self.is_run_store_act = True

                # 是否参加个vip折中折
                self.is_run_vip_discount = False

                # 应收价
                self.amt_receivable = 78.2
                # 记录折扣
                self.discountPrice = []

        # 商品
        class ProductMock(object):
            def __init__(self):
                self.qttyCount = 3
                # 记录当前活动id
                self.discountId = set()


        class UserInfo(object):
            def __init__(self):
                self.discount = 0.8


        class Bean_Mock(object):
            def __init__(self):
                self.id = 1
                self.is_run_other_pro = True
                self.is_run_store_act = True
                self.target_item = "amt_receivable"
                # 当前活动是否可以参加vip
                self.is_run_vip_discount = True

        self.seatMock = SeatMock()

        self.productMock = ProductMock()

        self.userinfo = UserInfo()

        self.bean_Mock = Bean_Mock()

        basics_bg.basics_one(self.seatMock,self.productMock,self.bean_Mock,self.userinfo)
    def test_productmock(self):
        print(self.productMock.qttyCount)
        # 正确2
        self.assertEqual(self.productMock.qttyCount,2)

    def test_seatMock(self):

        # 判断是否站位
        print(self.seatMock.seat)
        self.assertEqual(self.seatMock.seat,True)

        # 是否记录当前活动id
        print(self.productMock.discountId)
        self.assertEqual(self.productMock.discountId,{1})

        # 判断是否记录当前折扣 78.2 * 0.8
        print(self.seatMock.discountPrice)
        self.assertEqual(self.seatMock.discountPrice,[15.64])

        # 更改当前应收价格
        print(self.seatMock.amt_receivable)
        self.assertEqual(self.seatMock.amt_receivable,62.56)


class Test_condition_qtty_buygift(unittest.TestCase):
    @classmethod
    def setUp(self):
        # 商品明细
        class SeatMock(object):
            def __init__(self):
                self.is_buy_gifts = "n"
                # 占位
                self.seat = False
                # 判断当前商品是否可以跟其他活动同时进行进行
                self.is_run_other_pro = True
                # 是否可以进行全场活动
                self.is_run_store_act = True
                # 记录当前活动id
                self.discountId = set()

                # 是否参加个vip折中折
                self.is_run_vip_discount = False

                # 应收价
                self.amt_receivable = 78.2
                # 记录折扣
                self.discountPrice = []
                self.amt_list = 78.2
        # 商品
        class ProductMock(object):
            def __init__(self):
                self.qtty = 11
                self.productSeatList = []
                self.discountId = set()
                self.qttyCount = self.qtty
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

        class UserInfo(object):
            def __init__(self):
                self.discount = 0.8


        class Bean_Mock(object):
            def __init__(self):
                self.id = 1
                self.is_run_other_pro = True
                self.is_run_store_act = True
                self.target_item = "amt_list"
                # 当前活动是否可以参加vip
                self.is_run_vip_discount = True

                # 比较值
                self.value_num = 3

                self.comp_symb_type = "ge"

                # 满足条件
                self.target_type = "qtty"

                # 翻倍
                self.max_times = 2

        self.seatMock = SeatMock()

        self.productMock = ProductMock()

        self.userinfo = UserInfo()

        self.bean_Mock = Bean_Mock()
        # self.response = basics_bg.condition_qtty_buygift(self.bean_Mock,self.productMock,self.userinfo)
        self.response = basics_bg.condition_amt_list_buygift(self.bean_Mock,self.productMock,self.userinfo)

    # def testbuy_a_give_a(self):
        # print(self.response)
        # self.assertEqual(self.response,1)

    def test_condition_amt_list_buygift(self):
        print(self.response)
        self.assertEqual(self.response,1)


class Test_buy_a_give_a_unify_buygift(unittest.TestCase):
    @classmethod
    def setUp(self):
        # 商品明细
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

                # 是否参加个vip折中折
                self.is_run_vip_discount = False

                # 应收价
                self.amt_receivable = 78.2
                # 记录折扣
                self.discountPrice = []
                self.amt_list = 78.2
        # 商品
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

        class UserInfo(object):
            def __init__(self):
                self.discount = 0.8


        class Bean_Mock(object):
            def __init__(self):
                self.id = 1
                self.is_run_other_pro = True
                self.is_run_store_act = True
                self.target_item = "amt_list"
                # 当前活动是否可以参加vip
                self.is_run_vip_discount = True


                self.buygift_product = [{'ecode': 'ecode', 'amt_list': 123}, {'ecode': 'as002', 'amt_list': 456}]
                # 比较值
                self.value_num = 100

                self.comp_symb_type = "ge"

                # 满足条件
                self.target_type = "qtty"

                # 翻倍
                self.max_times = 2

        self.seatMock = SeatMock()

        self.productMock = ProductMock()
        self.productMockListA = [self.productMock]
        self.userinfo = UserInfo()

        self.bean_Mock = Bean_Mock()

        self.response = basics_bg.buy_a_give_a_unify_buygift(self.bean_Mock,self.userinfo,self.productMockListA)


    def test_buy_a_give_a_unify_buygift(self):
        print(self.response)
        self.assertIsNone(self.response)


class Test_sum_number_qtty(unittest.TestCase):



    @classmethod
    def setUp(self):
        # 商品明细
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

                # 是否参加个vip折中折
                self.is_run_vip_discount = False

                # 应收价
                self.amt_receivable = 78.2
                # 记录折扣
                self.discountPrice = []
                self.amt_list = 78.2
        # 商品
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

        class UserInfo(object):
            def __init__(self):
                self.discount = 0.8


        class Bean_Mock(object):
            def __init__(self):
                self.id = 1
                self.is_run_other_pro = True
                self.is_run_store_act = True
                self.target_item = "amt_list"
                # 当前活动是否可以参加vip
                self.is_run_vip_discount = True


                self.buygift_product = [{'ecode': 'ecode', 'amt_list': 123}, {'ecode': 'as002', 'amt_list': 456}]
                # 比较值
                self.value_num = 3

                self.comp_symb_type = "ge"

                # 满足条件
                self.target_type = "qtty"

                # 翻倍
                self.max_times = 2


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
        self.seatMock = SeatMock()

        self.productMock = ProductMock()
        self.productMockListA = [self.productMock]
        self.notproductMockListA = NotProductMock()
        self.notproductMock_ListA = [self.notproductMockListA]
        self.userinfo = UserInfo()

        self.sum_qtty_Mock  = copy.deepcopy(self.productMock.qttyCount)
        self.bean_Mock = Bean_Mock()


        self.response = basics_bg.sum_number_qtty(self.bean_Mock,self.userinfo,self.productMockListA,self.notproductMock_ListA,self.sum_qtty_Mock)


    def test_sum_number_qtty(self):

        # 如果等于None 说明没问题 因为完整修改完商品了已经
        self.assertIsNone(self.response)


class Test_sum_number_money(unittest.TestCase):
    @classmethod
    def setUp(self):
        # 商品明细
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

                # 是否参加个vip折中折
                self.is_run_vip_discount = False

                # 应收价
                self.amt_receivable = 78.2
                # 记录折扣
                self.discountPrice = []
                self.amt_list = 78.2
        # 商品
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

        class UserInfo(object):
            def __init__(self):
                self.discount = 0.8


        class Bean_Mock(object):
            def __init__(self):
                self.id = 1
                self.is_run_other_pro = True
                self.is_run_store_act = True
                self.target_item = "amt_list"
                # 当前活动是否可以参加vip
                self.is_run_vip_discount = True


                self.buygift_product = [{'ecode': 'ecode', 'amt_list': 123}, {'ecode': 'as002', 'amt_list': 456}]
                # 比较值
                self.value_num = 200

                self.comp_symb_type = "ge"

                # 满足条件
                self.target_type = "qtty"

                # 翻倍
                self.max_times = 2


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
        self.seatMock = SeatMock()

        self.productMock = ProductMock()
        self.productMockListA = [self.productMock]
        self.notproductMockListA = NotProductMock()
        self.notproductMock_ListA = [self.notproductMockListA]
        self.userinfo = UserInfo()

        self.sum_qtty_Mock  = copy.deepcopy(self.productMock.qttyCount)
        self.bean_Mock = Bean_Mock()
        self.amt_sum = copy.deepcopy(self.productMock.getCountAmtList())
        self.condition = "amt_list"
        self.response = basics_bg.sum_number_money(self.bean_Mock,self.userinfo,self.productMockListA,self.notproductMock_ListA,self.amt_sum,self.condition)


    def test_sum_number_money(self):
        # print(self.response)
        self.assertIsNone(self.response)


class Test_not_buy_a_give_a_unify(unittest.TestCase):
    @classmethod
    def setUp(self):
        # 商品明细
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

                # 是否参加个vip折中折
                self.is_run_vip_discount = False

                # 应收价
                self.amt_receivable = 78.2
                # 记录折扣
                self.discountPrice = []
                self.amt_list = 78.2
        # 商品
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

        class UserInfo(object):
            def __init__(self):
                self.discount = 0.8


        class Bean_Mock(object):
            def __init__(self):
                self.id = 1
                self.is_run_other_pro = True
                self.is_run_store_act = True
                self.target_item = "amt_list"
                # 当前活动是否可以参加vip
                self.is_run_vip_discount = True


                self.buygift_product = [{'ecode': 'ecode', 'amt_list': 123}, {'ecode': 'as002', 'amt_list': 456}]
                # 比较值
                self.value_num = 200

                self.comp_symb_type = "ge"

                # 满足条件
                self.target_type = "qtty"

                # 翻倍
                self.max_times = 2


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
        self.seatMock = SeatMock()

        self.productMock = ProductMock()
        self.productMockListA = [self.productMock]
        self.notproductMockListA = NotProductMock()
        self.notproductMock_ListA = [self.notproductMockListA]
        self.userinfo = UserInfo()

        self.sum_qtty_Mock  = copy.deepcopy(self.productMock.qttyCount)
        self.bean_Mock = Bean_Mock()
        self.amt_sum = copy.deepcopy(self.productMock.getCountAmtList())
        self.relice = 0
        self.ratail = 0


        self.response = basics_bg.not_buy_a_give_a_unify(self.bean_Mock,self.userinfo,self.productMockListA,self.notproductMock_ListA,self.sum_qtty_Mock,self.amt_sum,self.relice,self.ratail)

    def test_not_buy_a_give_a_unify(self):
        print(self.response)
        self.assertIsNone(self.response)

class Test_unify_buygift(unittest.TestCase):
    @classmethod
    def setUp(self):
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
        # 商品
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


        class Bean_Mock(object):
            def __init__(self):
                self.id = 1
                self.is_run_other_pro = True
                self.is_run_store_act = True
                self.target_item = "amt_list"
                # 当前活动是否可以参加vip
                self.is_run_vip_discount = True

                self.members_only = True

                self.buygift_product = [{'ecode': 'ecode', 'amt_list': 123}, {'ecode': 'as002', 'amt_list': 456}]
                # 比较值
                self.value_num = 200

                self.comp_symb_type = "ge"

                # 满足条件
                self.target_type = "qtty"
                self.product_list = ["ecode"]
                # 翻倍
                self.max_times = 2
                self.members_group = [1,2,3]


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
        self.seatMock = SeatMock()

        self.productMock = ProductMock()

        self.notproductMockListA = NotProductMock()

        self.userinfo = UserInfo()

        self.sum_qtty_Mock  = copy.deepcopy(self.productMock.qttyCount)
        self.bean_Mock = Bean_Mock()
        self.amt_sum = copy.deepcopy(self.productMock.getCountAmtList())
        self.relice = 0
        self.ratail = 0
        self.productMockListA = [self.productMock,self.notproductMockListA]
        self.response = unify_buygift.unify_buygift(self.productMockListA,self.bean_Mock,self.userinfo,)
    # 里面有两个对象的的地址
    def test_buy_a_give_a_unify_buygift(self):
        print(self.response)
        self.assertIsNotNone(self.response)

