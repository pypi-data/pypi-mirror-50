# -*- coding:utf-8 -*-
"""
    梯度特价
    2018/11/13
    by李博文
"""
import copy

from pro.apis.GA_api.SO_api.basics_fs import condition_qtty
from pro.apis.GA_api.SO_api.current_zeyou import current_zeyou
from pro.apis.GA_api.BG_api.buy_a_for_value import tongji
from pro.apis.GA_utils import checkisnoseatpro

def preferential_gr(product_object_list, unify_buygift_list, userInfo, productList_cp):

    productListMAX = []


    list1 = copy.deepcopy(product_object_list)

    index_cursor = 0
    for index in range(0, len(unify_buygift_list)):

        for bean in unify_buygift_list:
            if len(bean.product_list) < 1:
                continue
            # 返回每个方案计算后的商品集合
            list1 = gradient_special_pirce(list1, bean, userInfo)
            if not checkisnoseatpro(list1):
                break

        productListMAX.append(list1)



        # 游标加1
        index_cursor += 1

        # 将当前下标与这次循环下标交换
        if len(unify_buygift_list) > 1:
            if index_cursor != len(unify_buygift_list):
                unify_buygift_list[0], unify_buygift_list[index_cursor] = unify_buygift_list[index_cursor], \
                                                                          unify_buygift_list[0]
        list1 = copy.deepcopy(product_object_list)


    response =  current_zeyou(productListMAX)

    # start 对于判断只有该促销活动时该单据是否符合执行条件完全没有必要将活动执行一遍，因为这个只需要记录该活动符合该单据返回给前端就可以了，所以下面这个都可以不需要了，edit by hexiaoxia 2019/04/15
    # response = result_data(response,productListMAX)
    #
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
    #         list1 = gradient_special_pirce(list1, bean, userInfo)
    #
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
    # end edit by hexiaoxia 2019/04/15

    return response

# 具体运算
def gradient_special_pirce(productList, bean, userInfo):
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

    # 原始商品总数量
    org_promotion_qtty_sum = 0

    # 遍历每一件商品合并encode相同的商品
    for ecode in bean.product_list:
        for product in productList:
            if ecode.lower() == product.ecode.lower():
                productListA.append(product)

    # 循环添加各种满足条件
    if len(productListA) > 0:
        promotion_qtty_sum, _, _, _,org_promotion_qtty_sum, _, _, _ = tongji(productListA)



        for promotion in reversed(bean.operation_set):
            # 将所有promotion需要的数据动态赋值给bean以达到函数复用
            # 比较符
            bean.comp_symb_type = promotion.comp_symb_type

            # 比较值
            bean.value_num = promotion.value_num
            # 特价值
            bean.special_price = promotion.special_price

            response = condition_qtty(bean, userInfo, productListA, promotion_qtty_sum,org_promotion_qtty_sum)
            if type(response) == str:
                return productList

    return productList
