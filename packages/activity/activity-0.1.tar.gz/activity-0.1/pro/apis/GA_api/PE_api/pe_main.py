#!/usr/bin/env python
"""
    商品买免入口函数
   encoding: utf-8
   2019/4/26

   by 魏艳萍
"""
import copy
from pro.utils.pro_exception import ProException
from pro.apis.GA_utils import recovery_seat
from pro.apis.GA_api.PE_api.unify_maimian import preferential_maimian
from pro.apis.GA_api.PE_api.combination_maimian import preferential_com_maimian
from pro.apis.GA_api.SO_api.current_zeyou import current_zeyou
from pro.apis.GA_utils import checkisnoseatpro


def get_maimian(product_object_list, promotion_objec_list, user_object, productList_cp):
    """

    :param product_object_list: 商品对象集合
    :param promotion_objec_list: 活动对象集合
    :param user_object: 会员对象集合
    :return:
    """

    # 先将所有商品站位复原
    product_object_list = recovery_seat(product_object_list)

    # 统一买免模板列表
    unify_maimian = []

    # 组合买免模板列表
    combination_maimian = []

    for i in promotion_objec_list:

        # 统一买免模板列表
        if i.prom_type_three.lower() == "ga1601":
            unify_maimian.append(i)

        # 组合买免列表
        elif i.prom_type_three.lower() == "ga1602":
            combination_maimian.append(i)
        else:
            raise ProException("三类id出错")

    maimian_list = []  # 买免活动列表
    if unify_maimian:
        maimian_list.append(unify_maimian)
    if combination_maimian:
        maimian_list.append(combination_maimian)


    product_list = copy.deepcopy(product_object_list)
    productListMAX = []  # 择优列表
    index_cursor = 0
    # 循环计算买免活动
    for index1 in range(0, len(maimian_list)):
        for promotion in maimian_list:
            # 统一买免
            if promotion[0].prom_type_three == "ga1601":
                product_list = preferential_maimian(product_list, promotion, user_object, productList_cp)
            # 组合买免
            elif promotion[0].prom_type_three == "ga1602":
                product_list = preferential_com_maimian(product_list, promotion, user_object, productList_cp)
            # 判断还有没有未占位的商品，如果没有未占位的商品，直接结束本次循环。
            if not checkisnoseatpro(product_list):
                continue
        productListMAX.append(product_list)
        # 游标加1
        index_cursor += 1

        # 将当前下标与这次循环下标交换
        if len(maimian_list) > 1:
            if index_cursor >= len(maimian_list):
                index_cursor = 1
            maimian_list[0], maimian_list[index_cursor] = maimian_list[index_cursor], \
                                                          maimian_list[0]
        product_list = copy.deepcopy(product_object_list)
    response = current_zeyou(productListMAX)
    return response
