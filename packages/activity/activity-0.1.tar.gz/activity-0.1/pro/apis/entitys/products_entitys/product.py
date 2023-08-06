#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:尹晨
# datetime:2018/9/26 12:23

from pro.apis.entitys.products_entitys.product_seat import ProductSeat
from pro.utils.pro_exception import ProException


class Product():
    def __init__(self, obj, i):
        if obj['ecode'] is None:
            raise ProException('商品编码为空')
        # 商品编码
        self.ecode = obj['ecode']

        self.sku = obj['sku']

        if obj['amt_list'] is None:
            raise ProException('商品' + self.ecode + '吊牌金额为空')
        # 吊牌金额
        self.amt_list = float(obj['amt_list'])

        if obj['amt_retail'] is None:
            raise ProException('商品' + self.ecode + '零售金额为空')
        # 零售金额
        self.amt_retail = float(obj['amt_retail'])

        if obj['amt_receivable'] is None:
            raise ProException('商品' + self.ecode + '应收金额为空')
        # 应收金额
        self.amt_receivable = float(obj['amt_receivable'])

        #
        if obj['qtty'] is None or int(obj['qtty']) <= 0:
            raise ProException('商品' + self.ecode + '数量不正确')
        # 数量
        self.qtty = int(obj['qtty'])

        # 循环判断优惠数量是否变化--值
        self.qttyCount = self.qtty
        # pos端行号标记符
        if obj.get("lineno"):
            self.lineno = int(obj.get("lineno"))
        else:
            self.lineno = i

        # 标记最开始入参传入的商品顺序行，确定唯一的，全场活动计算需要，字典行数据是无序的，经过不同传值会乱的
        self.rownum = i

        # 可参加的活动
        self.discountId = set()
        #可参加的全场活动
        self.fulldiscountID = []
        # 明细
        self.productSeatList = []

        if self.qtty > 0:
            for i in range(self.qtty):
                self.productSeatList.append(ProductSeat(obj))

    def __hash__(self) -> int:
        return self.ecode.__hash__()

    def __eq__(self, o: object) -> bool:
        return self.ecode == o.ecode

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

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
            if bean.seat == False and bean.is_run_other_pro==True:
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

    # 取出一个当前商品中应收价最高的一件(未占位和可以参加商品活动)
    def getMaxAmtReceivable(self):
        tmpPlist = [i for i in self.productSeatList if i.seat is False and i.is_run_other_pro is True]
        return max(tmpPlist, key=lambda x: x.amt_receivable) if len(tmpPlist) > 0 else None

    # 当前商品的应收价总和
    def getCountPric(self):
        sum = 0
        for seat in self.productSeatList:
            sum += seat.amt_receivable
        return sum


tt = {"t1": ""}
if tt.get("t1"):
    print(1)
