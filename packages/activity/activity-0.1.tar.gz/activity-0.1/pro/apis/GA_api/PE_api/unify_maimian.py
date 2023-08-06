# -*- coding:utf-8 -*-
"""
    统一买免
    2018/11/15
    by李博文
"""

import copy
from pro.apis.GA_api.PE_api.current_zeyou import current_zeyou

from pro.apis.GA_api.PE_api.basics_maimian import condition
from pro.apis.GA_utils import recovery_seat
from pro.apis.GA_api.BG_api.buy_a_for_value import tongji
from pro.apis.GA_api.PE_api.current_zeyou import result_data

def preferential_maimian(product_object_list, unify_buygift_list, userInfo , product_List):
    """

    :param product_object_list: 所有商品
    :param unify_buygift_list: 所有统一买免活动
    :param userInfo:  会员对象
    :return: 最优活动
    """
    recovery_seat(product_object_list)

    productListMAX = []


    list1 = copy.deepcopy(product_object_list)
    unify_buygift_list = sorted(unify_buygift_list, key=lambda x: x.publish_date, reverse=True)
    index_cursor = 0
    for index in range(0, len(unify_buygift_list)):

        for bean in unify_buygift_list:
            if len(bean.product_list) < 1:
                continue
            # 返回每个方案计算后的商品集合
            list1 = unify_maimian(list1, bean, userInfo)

        productListMAX.append(list1)



        # 游标加1
        index_cursor += 1

        # 将当前下标与这次循环下标交换
        if len(unify_buygift_list) > 1:
            if index_cursor != len(unify_buygift_list):
                unify_buygift_list[0], unify_buygift_list[index_cursor] = unify_buygift_list[index_cursor], \
                                                                          unify_buygift_list[0]
                list1 = copy.deepcopy(product_object_list)



    # 整合数据
    response = current_zeyou(productListMAX)
    response = result_data(response, productListMAX)


    # 用所有原始数据再来一次

    # 最后整合需要用的数据
    productList_or = []
    list1 = copy.deepcopy(product_List)

    index_cursor = 0
    for index in range(0, len(unify_buygift_list)):

        for bean in unify_buygift_list:
            if len(bean.product_list) < 1:
                continue
            # 返回每个方案计算后的商品集合
            list1 = unify_maimian(list1, bean, userInfo)

        productList_or.append(list1)



        # 游标加1
        index_cursor += 1

        # 将当前下标与这次循环下标交换
        if len(unify_buygift_list) > 1:
            if index_cursor != len(unify_buygift_list):
                unify_buygift_list[0], unify_buygift_list[index_cursor] = unify_buygift_list[index_cursor], \
                                                                          unify_buygift_list[0]
        list1 = copy.deepcopy(product_List)

    response = result_data(response, productList_or)
    return response



def unify_maimian(productList, bean, userInfo):
    """

    :param productList:  所有商品
    :param bean: 当前活动
    :param userInfo: 会员对象
    :return: 所有商品
    """
    # 判断当前活动是否限制会员并且当前用户可否参与
    if bean.members_only:
        if userInfo is not None:
            # 当前用户会员级别不再此活动会员级别范围之内
            if userInfo.id not in bean.members_group:
                return productList
        else:
            # 当前活动限制会员参加 且 当前用户不是会员
            return productList

    # 取出当前活动赠送品

    # qtty:数量
    promotion_qtty_sum = 0

    # 所有ecode相同对象
    productListA = []

    # 遍历每一件商品合并encode相同的商品
    for ecode in bean.product_list:

        for product in productList:
            if ecode.lower() == product.ecode.lower():
                productListA.append(product)

    # 计算可以参加活动的总数量
    if len(productListA) > 0:
        promotion_qtty_sum, _, _, _, _, _, _, _ = tongji(productListA)

        condition(bean, userInfo, productListA, promotion_qtty_sum)
        if bean.comp_symb_type == "g":
            bean.value_num -= 1
    return productList
