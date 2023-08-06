# -*- coding:utf-8 _*-
"""
@author:尹晨
@file: get_count.py
@time: 2018/10/24
"""



# 获取当前商品集合所有未占位的商品数量
def getNotOccupiedAll(productList):
    if len(productList) < 1:
        return 0
    sum = 0
    for products in productList:
        sum += products.notOccupiedThree()
    return sum


# 获取当前商品集合总数量
def getCountQtty(productList):
    sum = 0
    if len(productList) > 0:
        for products in productList:
            sum += products.qtty
    return sum


# 查找出一个未占位的且进行可以进行这次活动的一件商品
def getNotOccupiedOne(productList):
    if len(productList) > 0:
        productlist = []
        for products in productList:
            seat=products.productSeatList
            for row in seat:
                productlist.append(row)
        seat = getNotOccupied(productlist)
        for products in productList:
            if seat != None:
                if seat.sku==products.sku:
                    return seat, products
        return None, None

# 当前未占位商品的总吊牌价
def getCountAmtListOne(productList):
    sum = 0
    if len(productList) > 0:
        for products in productList:
            sum += products.getCountAmtList()
    return sum

# 当前商品的总吊牌价
def getCountAmtListTwo(productList):
    sum = 0
    if len(productList) > 0:
        for products in productList:
            sum += products.qtty * products.amt_list
    return sum

# 当前未占位商品的总零售价
def getCountAmtRetailOne(productList):
    sum = 0
    if len(productList) > 0:
        for products in productList:
            sum += products.getCountAmtRetail()
    return sum

# 当前商品的总零售价
def getCountAmtRetailTwo(productList):
    sum = 0
    if len(productList) > 0:
        for products in productList:
            sum += products.qtty * products.amt_retail
    return sum

# 当前未占位商品的总应收价
def getCountAmtReceivableOne(productList):
    sum = 0
    if len(productList) > 0:
        for products in productList:
            sum += products.getCountAmtReceivable()
    return sum

# 当前商品的总应收价
def getCountAmtReceivableTwo(productList):
    sum = 0
    if len(productList) > 0:
        for products in productList:
            sum += products.getCountPric()
    return sum

#当前商品的初始总应收价
def getCountAmtReceivableThree(productList):
    sum = 0
    if len(productList) > 0:
        for products in productList:
            sum += products.qtty*products.amt_receivable
    return sum


# 查找出一个未占位的且进行可以进行这次活动的一件商品
def getNotOccupied(list):
    tmpPlist = [i for i in list if i.seat is False and i.is_run_other_pro is True and i.is_discount == "y"]
    return min(tmpPlist, key=lambda x: x.amt_receivable) if len(tmpPlist) > 0 else None
