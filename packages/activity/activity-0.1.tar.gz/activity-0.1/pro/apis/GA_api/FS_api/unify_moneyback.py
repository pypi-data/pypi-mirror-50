#!/usr/bin/env python
"""
    循环活动计算满减
   encoding: utf-8
   2018/12/18 4:03 PM
   
  
   by李博文
"""

import copy


from pro.apis.GA_api.FS_api.basics_mb import choice, unify_gradient_cal
from pro.apis.GA_api.PE_api.current_zeyou import result_data
from pro.apis.GA_api.SO_api.current_zeyou import current_zeyou
from pro.apis.GA_api.BG_api.buy_a_for_value import tongji


def preferential_un(product_object_list, unify_buygift_list, userInfo, productList_cp):
    # 先排序
    unify_buygift_list = sorted(unify_buygift_list, key=lambda x: x.publish_date, reverse=True)
    productListMAX = []


    list1 = copy.deepcopy(product_object_list)

    index_cursor = 0
    for index in range(0, len(unify_buygift_list)):

        for bean in unify_buygift_list:
            if len(bean.product_list) < 1:
                continue
            # 返回每个方案计算后的商品集合
            list1 = unify_moneyback(list1, bean, userInfo)
            # if bean.comp_symb_type == "g":
            #     bean.value_num -= 1
        productListMAX.append(list1)



        # 游标加1
        index_cursor += 1

        # 将当前下标与这次循环下标交换
        if len(unify_buygift_list) > 1:
            if index_cursor != len(unify_buygift_list):
                unify_buygift_list[0], unify_buygift_list[index_cursor] = unify_buygift_list[index_cursor], \
                                                                          unify_buygift_list[0]
        list1 = copy.deepcopy(product_object_list)



    response = current_zeyou(productListMAX)
    response = result_data(response, productListMAX)

    # # 用所有原始数据再来一次
    # # 最后整合需要用的数据
    # productList_or = []
    # list1 = copy.deepcopy(productList_cp)
    #
    # index_cursor = 0
    # for index in range(0, len(unify_buygift_list)):
    #
    #     for bean in unify_buygift_list:
    #         if len(bean.product_list) < 1:
    #             continue
    #         # 返回每个方案计算后的商品集合
    #         list1 = unify_moneyback(list1, bean, userInfo)
    #         if bean.comp_symb_type == "g":
    #             bean.value_num -= 1
    #     productList_or.append(list1)
    #
    #     # 游标加1
    #     index_cursor += 1
    #
    #     # 将当前下标与这次循环下标交换
    #     if len(unify_buygift_list) > 1:
    #         if index_cursor != len(unify_buygift_list):
    #             unify_buygift_list[0], unify_buygift_list[index_cursor] = unify_buygift_list[index_cursor], \
    #                                                                       unify_buygift_list[0]
    #     list1 = copy.deepcopy(productList_cp)
    #
    # response = result_data(response, productList_or)
    return response


# 具体运算
def unify_moneyback(productList, bean, userInfo):
    # 判断当前活动是否限制会员并且当前用户可否参与
    if bean.members_only:
        if userInfo is not None:
            # 当前用户会员级别不再此活动会员级别范围之内
            if userInfo.id not in bean.members_group:
                return productList
        else:
            # 当前活动限制会员参加 且 当前用户不是会员
            return productList

    # 所有可以参加活动的商品列表
    productListA = []

    # qtty:数量
    promotion_qtty_sum = 0

    # amt_list:吊牌金额
    promotion_amt_list_sum = 0

    # amt_retail:零售金额
    promotion_amt_retail_sum = 0

    # amt_receivable:应收金额是否满足
    promotion_amt_receivable_sum = 0

    # 遍历每一件商品合并encode相同的商品
    for ecode in bean.product_list:
        for product in productList:
            if ecode.lower() == product.ecode.lower():
                productListA.append(product)

    # 循环添加各种满足条件
    if len(productListA) > 0:

        # promotion_qtty_sum, promotion_amt_list_sum, promotion_amt_retail_sum, promotion_amt_receivable_sum,_,_,_,_ = tongji(productListA)
        promotion_qtty_sum, promotion_amt_list_sum, promotion_amt_retail_sum, promotion_amt_receivable_sum, \
        org_promotion_qtty_sum, org_promotion_amt_list_sum, org_promotion_amt_retail_sum, \
        org_promotion_amt_receivable_sum = tongji(productListA)

        response = unify_gradient_cal(bean, userInfo, productListA, promotion_qtty_sum, promotion_amt_list_sum,
                                      promotion_amt_retail_sum, promotion_amt_receivable_sum,
                                      org_promotion_qtty_sum, org_promotion_amt_list_sum,
                                      org_promotion_amt_retail_sum, org_promotion_amt_receivable_sum)

        if response == 1:
            # 说明该促销满足条件，但不是最优的
            productListA[0].discountId.add(bean.id)

    return productList