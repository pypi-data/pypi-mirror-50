#-*- coding:utf-8 _*-
"""
@author:尹晨
@file: count_basic.py
@time: 2018/10/18
"""
import copy

from pro.apis.GA_api.DC_api import incremental_discount_api
from pro.apis.GA_api.DC_api import multiple_discount_api
from pro.apis.GA_api.DC_api import unify_discount_api
from pro.apis.GA_api.DC_api.basics import pickProduct


# 统一打折后进行递增打折、多种打折活动判断
def unifyPreferential(productList, MultipleDiscountList, IncrementalDiscountList,userInfo):
    productListMax = []
    for i in range(0, 2):
        listMD = []
        if i == 0:
            listMD = multiple_discount_api.preferential(copy.copy(productList), MultipleDiscountList,userInfo)
            listMD = incremental_discount_api.preferential(copy.copy(productList), IncrementalDiscountList,userInfo)
        else:
            listMD = incremental_discount_api.preferential(copy.copy(productList), IncrementalDiscountList,userInfo)
            listMD = multiple_discount_api.preferential(copy.copy(productList), MultipleDiscountList,userInfo)
        productListMax.append(listMD)
    return pickProduct(productList, productListMax)


# 多种打折后进行统一打折、递增打折活动判断
def multiplePreferential(productList, UnifyDiscountList, IncrementalDiscountList,userInfo):
    productListMax = []
    for i in range(0, 2):
        listMD = []
        if i == 0:
            listMD = unify_discount_api.preferential(copy.copy(productList), UnifyDiscountList,userInfo)
            listMD = incremental_discount_api.preferential(copy.copy(productList), IncrementalDiscountList,userInfo)
        else:
            listMD = incremental_discount_api.preferential(copy.copy(productList), IncrementalDiscountList,userInfo)
            listMD = unify_discount_api.preferential(copy.copy(productList), UnifyDiscountList,userInfo)
        productListMax.append(listMD)
    return pickProduct(productList, productListMax)


# 递增打折后进行统一打折、多种打折活动判断
def incrementalPreferential(productList, UnifyDiscountList, MultipleDiscountList,userInfo):
    productListMax = []
    for i in range(0, 2):
        listMD = []
        if i == 0:
            listMD = unify_discount_api.preferential(copy.copy(productList), UnifyDiscountList,userInfo)
            listMD = multiple_discount_api.preferential(copy.copy(productList), MultipleDiscountList,userInfo)
        else:
            listMD = multiple_discount_api.preferential(copy.copy(productList), MultipleDiscountList,userInfo)
            listMD = unify_discount_api.preferential(copy.copy(productList), UnifyDiscountList,userInfo)
        productListMax.append(listMD)
    return pickProduct(productList, productListMax)


