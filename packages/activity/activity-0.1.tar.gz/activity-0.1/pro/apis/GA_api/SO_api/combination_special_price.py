# -*- coding:utf-8 -*-
"""
    组合特价
    2019/04/16
    add by hexiaoxia
"""
import copy

from pro.apis.GA_api.SO_api.current_zeyou import current_zeyou
from pro.apis.GA_api.BG_api.buy_a_for_value import tongji
from pro.apis.GA_utils import checkisnoseatpro
from pro.apis.GA_api.SO_api.basics_fs import condition_qtty_combination


def preferential_cb(product_object_list, combination_buygift_list, userInfo):
    '''
    组合特价方法入口
    :param product_object_list: 前端促销执行后的商品集合或原始商品集合
    :param combination_buygift_list: 所有符合的商品特价---组合特价 活动列表
    :param userInfo: 但前录入的VIP信息
    :return:
    '''
    productListMAX = []
    list1 = copy.deepcopy(product_object_list)

    index_cursor = 0
    for index in range(0, len(combination_buygift_list)):

        for bean in combination_buygift_list:
            # 返回每个方案计算后的商品集合
            list1 = combination_special_pirce(list1, bean, userInfo)
            if not checkisnoseatpro(list1):
                break

        productListMAX.append(list1)

        # 游标加1
        index_cursor += 1

        # 将当前下标与这次循环下标交换
        if len(combination_buygift_list) > 1:
            if index_cursor != len(combination_buygift_list):
                combination_buygift_list[0], combination_buygift_list[index_cursor] = combination_buygift_list[index_cursor], \
                                                                                      combination_buygift_list[0]
        list1 = copy.deepcopy(product_object_list)

    response = current_zeyou(productListMAX)


    return response


# 具体运算
def combination_special_pirce(productList, bean, userInfo):
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



    specific_productall=[]
    holddis = -1
    candouble = False
    # 记录是否可翻倍，在本身可翻倍的情况下，只有当组合的所有条件设置的比较形式都是 = 的时候才可以翻倍
    double_numb = 0  # 记录翻倍基数

    # 使用执行前面其它的买赠促销的数据结构判断该促销是否可执行
    holddis, candouble, double_numb, \
    specific_productall, max_double_times, specific_product_list = conbination_compare(bean, productList, 0)

    if holddis == -1:
        # 表示上面的情况不可执行，那么再使用原始数据结构判断该促销是否可执行
        holddis, candouble, double_numb, specific_productall, \
        max_double_times, specific_product_list = conbination_compare(bean, productList, 1)

        if holddis == -1:
            return productList

    if holddis == 1:
        #不符合计算，但使用原始数据符合可保留
        productList[0].discountId.add(bean.id)
        return productList
    else:
        # 当前可计算
        for i in specific_productall:
            for product in productList:
                if i.lower() == product.ecode.lower():
                    productListA.append(product)

        productListA = sorted(productListA, key=lambda x: x.productSeatList[0].amt_receivable, reverse=True)  # 按照应收价格降序

        condition_qtty_combination(productListA, candouble, bean, double_numb,
                                   max_double_times, specific_product_list, userInfo)

        return productList


def conbination_compare(bean, productList, intype):
    '''
    检测组合项是否都满足条件
    :param bean: 促销活动
    :param productList: 商品集合
    :param intype: 0 表示基于前面执行过促销的数据上执行； 1 表示基于原始的数据上执行；
    :return:
    '''
    specific_productall = []
    double_numb = 0
    candouble = True  # 记录是否能翻倍
    max_double_times = 0  # 记录翻倍次数
    specific_product_list = []
    for r_item in bean.specific_activities:
        holddis = -1
        # qtty:数量
        promotion_qtty_sum = 0

        # 原始商品总数量
        org_promotion_qtty_sum = 0

        specific_product = []
        current_specific_product_ecode = []

        # 遍历每一件商品合并encode相同的商品
        for ecode in r_item.product_list:
            for product in productList:
                if ecode.lower() == product.ecode.lower():
                    specific_productall.append(ecode)
                    specific_product.append(product)
                    current_specific_product_ecode.append(ecode)
        if not specific_product:
            return -1, False, 0, [], 0, []

        promotion_qtty_sum, _, _, _, org_promotion_qtty_sum, _, _, _ = tongji(specific_product)

        # 如果总数不满足条件那么返回
        if r_item.comp_symb_type == "g":
            r_item.value_num += 1

        if intype==0:
            times = int(promotion_qtty_sum / r_item.value_num)
            if times < 1:
                return -1, False, 0, [], 0, []
            else:
                max_double_times = min(times, max_double_times) if max_double_times > 0 else times
                holddis=0
        else:
            if not org_promotion_qtty_sum >= r_item.value_num:
                return -1, False, 0, [], 0, []
            else:
                holddis=1

        specific_productall = list(set(specific_productall))

        if r_item.comp_symb_type != "e":
            # 如果有不是等于的条件， 则不能翻倍
            candouble = False
        double_numb += r_item.value_num
        specific_product_list.append({"pro_ecode_list": current_specific_product_ecode, "value_num": r_item.value_num})

    if max_double_times > 1:
        if bean.max_times == 0 or bean.max_times == 1:
            max_double_times = 1
        elif bean.max_times > 1 and max_double_times > bean.max_times:
            max_double_times = bean.max_times
    return holddis, candouble, double_numb, specific_productall, max_double_times, specific_product_list
