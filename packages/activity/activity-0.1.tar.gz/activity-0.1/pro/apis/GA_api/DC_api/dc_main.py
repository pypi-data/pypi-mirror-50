# -*- coding:utf-8 -*-
# author:尹晨
# datetime:2018/9/28 10:28
import copy

from pro.apis.GA_api.DC_api.basics import pickProduct
from pro.apis.GA_api.DC_api import unify_discount_api
from pro.apis.GA_api.DC_api import multiple_discount_api
from pro.apis.GA_api.DC_api import incremental_discount_api
from pro.apis.GA_api.DC_api import combination_discount_api
from pro.apis.GA_api.DC_api import count_basic


# 折扣二类下所有活动进行择优运算
def getDiscount(productListDiscount, discount_list, userInfo):
    # 创建4个方案模板列表
    UnifyDiscountList = []  # 统一打折
    MultipleDiscountList = []  # 多种打折
    IncrementalDiscountList = []  # 递增打折
    CombinationDiscountList = []  # 组合打折

    # 遍历每个活动放入对应的模板
    discount_list = sorted(discount_list, key=lambda x: x.publish_date)
    for bean in discount_list:

        if 'ga1101' == bean.prom_type_three:
            UnifyDiscountList.append(bean)  # 统一折扣
        elif 'ga1102' == bean.prom_type_three:
            MultipleDiscountList.append(bean)  # 多种折扣
        elif 'ga1103' == bean.prom_type_three:
            IncrementalDiscountList.append(bean)  # 递增折扣
        elif 'ga1104' == bean.prom_type_three:
            CombinationDiscountList.append(bean)  # 组合折扣

    # 进入统一打折三类,多种打折三类,递增打折三类方案--活动择优
    productList = singleDiscounts(copy.deepcopy(productListDiscount), UnifyDiscountList, MultipleDiscountList,
                                  IncrementalDiscountList,
                                  userInfo)
    # 对未占位商品进行再次单品活动判断
    productList = forSingleDiscounts(productList, UnifyDiscountList, MultipleDiscountList, IncrementalDiscountList,
                                     userInfo)
    # 对未占位商品进行组合活动判断
    productList = forGroupDiscounts(productList, CombinationDiscountList, userInfo)

    # 进入组合打折三类方案--活动择优
    productCDList = groupDiscounts(copy.deepcopy(productListDiscount), CombinationDiscountList, userInfo)
    # 对未占位商品进行再次组合活动判断
    productCDList = forGroupDiscounts(productCDList, CombinationDiscountList, userInfo)
    # 对未占位商品进行单品活动判断
    productCDList = forSingleDiscounts(productCDList, UnifyDiscountList, MultipleDiscountList, IncrementalDiscountList,
                                       userInfo)
    for i in range(0, len(productCDList)):
        productList[i].discountId = productList[i].discountId | productCDList[i].discountId
        productCDList[i].discountId = productList[i].discountId | productCDList[i].discountId

    singleSum = 0
    for p in productList:
        singleSum += p.getCountPric()
    groupSum = 0
    for p in productCDList:
        groupSum += p.getCountPric()
    # 重置所有的占位为flase
    for a, b in enumerate(productList):
        for c, d in enumerate(b.productSeatList):
            if d.is_run_other_pro:
                d.seat = False
            if productCDList[a].productSeatList[c].is_run_other_pro:
                productCDList[a].productSeatList[c].seat = False

    if singleSum <= groupSum:
        return productList
    else:
        return productCDList


# 进入单品择优方案
def singleDiscounts(productList, UnifyDiscountList, MultipleDiscountList, IncrementalDiscountList, userInfo):
    productUDLists = []
    productMDLists = []
    productIDLists = []
    if len(UnifyDiscountList) > 0:  # 进入统一打折三类方案--活动择优
        productUDLists = unify_discount_api.preferential(productList, UnifyDiscountList, userInfo)
        productUDLists = count_basic.unifyPreferential(productUDLists, MultipleDiscountList, IncrementalDiscountList,
                                                       userInfo)
    if len(MultipleDiscountList) > 0:  # 进入多种打折三类方案--活动择优
        productMDLists = multiple_discount_api.preferential(productList, MultipleDiscountList,
                                                            userInfo)
        productMDLists = count_basic.multiplePreferential(productMDLists, UnifyDiscountList, IncrementalDiscountList,
                                                          userInfo)
    if len(IncrementalDiscountList) > 0:  # 进入递增打折三类方案--活动择优
        productIDLists = incremental_discount_api.preferential(productList,
                                                               IncrementalDiscountList, userInfo)
        productIDLists = count_basic.incrementalPreferential(productIDLists, UnifyDiscountList, MultipleDiscountList,
                                                             userInfo)
        # 单品活动种最优活动
    productListMax = []
    if productUDLists is not None:
        if len(productUDLists) > 0:
            productListMax.append(productUDLists)

    if productMDLists is not None:
        if len(productMDLists) > 0:
            productListMax.append(productMDLists)

    if productIDLists is not None:
        if len(productIDLists) > 0:
            productListMax.append(productIDLists)

    if productListMax is not None:
        if len(productListMax) > 0:
            productList = pickProduct(productList, productListMax)
            return productList
    return productList


# 进入组合择优方案
def groupDiscounts(productList, CombinationDiscountList, userInfo):
    if len(CombinationDiscountList) > 0:
        productCDList = combination_discount_api.preferential(productList,
                                                              CombinationDiscountList, userInfo)
        return productCDList
    return productList


# 循环判断是否还有能参加单品活动的商品
def forSingleDiscounts(productList, UnifyDiscountList, MultipleDiscountList, IncrementalDiscountList,
                       userInfo):
    # 健壮性
    sumA = 0
    sumB = 0
    for product in productList:
        sumA += product.qttyCount
        sumB += product.qtty
    if sumA == 0 or sumA == sumB:
        return productList
    productListA = singleDiscounts(productList, UnifyDiscountList, MultipleDiscountList, IncrementalDiscountList,
                                   userInfo)
    if productListA == None:
        return productList
    sumA = 0
    sumB = 0
    for i, j in enumerate(productList):
        sumA += j.qttyCount
        sumB += productListA[i].qttyCount
    if sumA == sumB:
        return productListA
    else:
        productListB = singleDiscounts(productList, UnifyDiscountList, MultipleDiscountList, IncrementalDiscountList,
                                       userInfo)
        return productListB


# 循环判断是否还有能参加组合活动的商品
def forGroupDiscounts(productList, CombinationDiscountList, userInfo):
    # 健壮性
    sumA = 0
    sumB = 0
    for product in productList:
        sumA += product.qttyCount
        sumB += product.qtty
    if sumA == 0 or sumA == sumB:
        return productList

    productListA = groupDiscounts(productList, CombinationDiscountList, userInfo)
    sumA = 0
    sumB = 0
    if productListA == None:
        return productList
    for i, j in enumerate(productList):
        sumA += j.qttyCount
        sumB += productListA[i].qttyCount
    if sumA == sumB:
        return productListA
    else:
        productListB = forGroupDiscounts(productListA, CombinationDiscountList, userInfo)
        return productListB
