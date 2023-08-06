#!/usr/bin/env python
"""
   换购详细运算
   encoding: utf-8
   2018/12/26 5:59 PM
   
  
   by李博文
"""


# 预留文件.以后可能新增功能会在这里写... 防止循环导入

def condition_for_pro(for_max, productListA, condition):

    # 更改商品站位信息金额
    result = 0
    for product in productListA:
        for seat in product.productSeatList:
            if result >= for_max:
                return result
            if seat.seat == False and seat.is_run_other_pro != False:
                result += 1
                basics(seat)
                result += getattr(seat, condition)

    return result


def condition_for_pro_qtty(for_max, productListA):
    # 更改商品站位信息 数量
    for product in productListA:
        for seat in product.productSeatList:
            if for_max == 0:
                return
            if seat.seat == False and seat.is_run_other_pro != False:
                basics(seat)
                for_max -= 1