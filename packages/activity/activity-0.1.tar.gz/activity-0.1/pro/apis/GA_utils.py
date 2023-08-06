#!/usr/bin/env python
"""
   商品活动公用方法
   encoding: utf-8
   2018/12/5 4:51 PM
   
  
   by李博文
"""
import math



def calculation_amt_receivable(productListA, for_value, condition):
    """
    计算应收总价格 控制循环值
    :param productListA: 商品价钱
    :param for_value
    :return: 所有商品的应收价的总值
    """
    result = 0
    result_re = 0
    for product in productListA:
        for seat in product.productSeatList:
            if seat.is_discount == "n":
                continue
            if result >= for_value:
                break
            if seat.seat == False and seat.is_run_other_pro != False:
                result += getattr(seat, condition)
                result_re += seat.amt_receivable
    return result_re

def calculation_amt_receivable_qtty(productListA, for_value):
    """
    计算应收总价格 控制循环值
    :param productListA: 商品价钱
    :param for_value
    :return: 所有商品的应收价的总值
    """
    result = 0
    for product in productListA:
        for seat in product.productSeatList:
            if seat.is_discount == "n":
                continue
            if for_value == 0:
                break
            if seat.seat == False and seat.is_run_other_pro != False:
                result += seat.amt_receivable
                for_value -= 1
    return result

def recovery_seat(productList):
    """
    恢复所有商品站位信息
    :param productList:
    :return:
    """
    for product in productList:
        for seat in product.productSeatList:
            if seat.seat == True:
                seat.seat = False
    return productList


def GA_retail_carryway(retail_carryway, moeny):
    """

    :param retail_carryway: 进位符
    :param moeny: 需要进位的金额
    :return: 进位后的金额
    """
    # 1(保留小数位);2(四舍五入取整);3(直接取整);4(进位取整);5(四舍五入到角);6(取整到角);

    # 1(保留小数位)
    if retail_carryway == 1:
        return float('%.2f' % moeny)
    # 2(四舍五入取整)
    elif retail_carryway == 2:
        if int(moeny) % 2 == 0:
            return round(moeny + 0.1)
        return round(moeny)
    # 3(直接取整)
    elif retail_carryway == 3:
        return math.floor(moeny)
    # 4 (进位取整)
    elif retail_carryway == 4:
        return math.ceil(moeny)
    # 5(四舍五入到角)
    elif retail_carryway == 5:
        return round(moeny, 1)
    else:
        return float('%.1f' % moeny)


def result_max_pro(productList, for_value):
    """
    计算当前商品的总应收价
    :param productList:
    :param for_value: 循环次数
    :return:
    """
    result = 0
    can_execute_special_amt_price = 0
    can_execute_special_qtty = 0
    for product in productList:
        for seat in product.productSeatList:
            if for_value == 0:
                break
            if seat.seat == False and seat.is_run_other_pro != False and seat.is_discount == "y":
                result += seat.amt_receivable
                for_value -= 1
                can_execute_special_qtty += seat.qtty
    can_execute_special_amt_price = result
    if for_value != 0:
        for product in productList:
            for seat in product.productSeatList:
                if for_value == 0:
                    break
                if seat.seat == False and seat.is_run_other_pro != False and seat.is_discount == "n":
                    result += seat.amt_receivable
                    for_value -= 1
    return result, can_execute_special_amt_price, can_execute_special_qtty


def checkisnoseatpro(productlist):
    '''
    检测传入的商品列表中是否还存在未占位商品
    add by hexiaoxia 2019/04/16
    :param productlist: 商品列表
    :return:
    '''
    for product in productlist:
        for seat in product.productSeatList:
            if seat.seat == False:
                return True
    return False