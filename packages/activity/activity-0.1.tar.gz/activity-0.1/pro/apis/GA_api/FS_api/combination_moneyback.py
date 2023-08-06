# -*- coding:utf-8 -*-
# author:weiyanping
# datetime:2019/4/16 10:00
# software: PyCharm

import copy
from pro.apis.GA_api.FS_api.basics_mb import operation_combination_moenyback
from pro.apis.GA_api.SO_api.current_zeyou import current_zeyou
from pro.apis.GA_api.BG_api.buy_a_for_value import tongji

def preferential_com(product_object_list, com_moneyback_list, userInfo):
    """
    进入组合满减活动计算
    :param product_object_list:商品列表
    :param com_moneyback_list:组合满减活动列表
    :param userInfo: 会员信息
    :return:
    """
    # 首先按照发布时间降序排序，其实感觉没用（因为最终都会走一遍）
    com_moneyback_list = sorted(com_moneyback_list, key=lambda x: x.publish_date, reverse=True)
    productListMAX = []  # 存放计算的结果
    list1 = copy.deepcopy(product_object_list)

    index_cursor = 0
    for index in range(0, len(com_moneyback_list)):

        for bean in com_moneyback_list:
            # 返回每个方案计算后的商品集合
            list1 = combination_moneyback(list1, bean, userInfo)

        productListMAX.append(list1)
        # 游标加1
        index_cursor += 1

        # 将当前下标与这次循环下标交换
        if len(com_moneyback_list) > 1:
            if index_cursor != len(com_moneyback_list):
                com_moneyback_list[0], com_moneyback_list[index_cursor] = com_moneyback_list[index_cursor], \
                                                                          com_moneyback_list[0]
        list1 = copy.deepcopy(product_object_list)

    response = current_zeyou(productListMAX)
    # response = result_data(response, productListMAX)
    return response

# 具体的计算
def combination_moneyback(productList, bean, userInfo):
    """
     组合具体的计算逻辑，主要是条件比较以及翻倍的计算
    :param productList: 商品
    :param bean: 活动信息
    :param userInfo: 会员信息
    :return:
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

    # 当前商品信息是否可以参加此活动， 如果为False的话，表示原始商品满足条件，可以作为可以参加的活动，但是不在择优执行列表中
    is_can_executed = True
    productListA = []  # 参与条件的商品
    part_product_ecode = []  # 参与活动的商品的款号
    # bean.max_times
    max_double_times = 0  # 当前最大可以翻倍的次数

    has_is_discount_product = False  # 是否有可以参与促销计算的商品
    # 对每个组合条件进行循环
    for spec_item in bean.specific_activities:
        # 将该行的条件商品拎出来
        current_part_product = []
        for ecode in spec_item.product_list:
            for product in productList:
                if ecode.lower() == product.ecode.lower():
                    if product.productSeatList and product.productSeatList[0].is_discount == "y":
                        has_is_discount_product = True
                    current_part_product.append(product)
                    part_product_ecode.append(ecode.lower())

        # 如果没有符合条件的商品，说明不满足执行条件，不执行
        if not current_part_product:
            return productList

        # 计算当前商品中未占位的总数量，总价格（包括零售，吊牌，应收价）
        promotion_qtty_sum, promotion_amt_list_sum, promotion_amt_retail_sum, promotion_amt_receivable_sum, org_promotion_qtty_sum, org_promotion_amt_list_sum, org_promotion_amt_retail_sum, org_promotion_amt_receivable_sum = tongji(current_part_product)

        value_num = float(spec_item.value_num)  # 比较值
        # 如果是大于的话，比较值 加1
        if spec_item.comp_symb_type == "g":
            value_num = value_num + 1

        if str(spec_item.target_type).lower() == "qtty":
            # 以数量满足
            if not int(promotion_qtty_sum) >= int(value_num):
                # 未占位商品不满足条件
                if not int(org_promotion_qtty_sum) >= int(value_num):
                    # 原始商品也不满足条件
                    return productList
                is_can_executed = False  # 原始商品满足条件
            p = int(promotion_qtty_sum) // int(value_num)  # 当前可以翻的倍数
        elif str(spec_item.target_type).lower() == "amt_list":
            # 以吊牌价满足
            if not float(promotion_amt_list_sum) >= value_num:
                if not float(org_promotion_amt_list_sum) >= value_num:
                    return productList
                is_can_executed = False
            p = int(promotion_amt_list_sum) // int(value_num)
        elif str(spec_item.target_type).lower() == "amt_retail":
            # 以零售价满足
            if not float(promotion_amt_retail_sum) >= value_num:
                if not float(org_promotion_amt_retail_sum) >= value_num:
                    return productList
                is_can_executed = False
            p = int(promotion_amt_retail_sum) // int(value_num)
        elif str(spec_item.target_type).lower() == "amt_receivable":
            # 以应收价满足
            if not float(promotion_amt_receivable_sum) >= value_num:
                if not float(org_promotion_amt_receivable_sum) >= value_num:
                    return productList
                is_can_executed = False
            p = int(promotion_amt_receivable_sum) // int(value_num)
        # 和之前存储的翻倍进行比较，如果小于之前的翻倍，将翻倍次数修改
        if max_double_times == 0 or max_double_times > p:
            max_double_times = p
        continue
    # 可以参与此活动的商品款号
    part_product_ecode = list(set(part_product_ecode))

    # 找出总的符合该条件的商品
    for ecode in part_product_ecode:
        for product in productList:
            if ecode.lower() == product.ecode.lower():
                productListA.append(product)
    # 翻倍，比较活动的翻倍限制，再对翻倍次数进行修改
    if max_double_times > 1:
        if bean.max_times == 0 or bean.max_times == 1:
            max_double_times = 1
        elif bean.max_times > 1 and max_double_times > bean.max_times:
            max_double_times = bean.max_times

    if not is_can_executed:
        # 说明该促销可以保留到可以参与的促销中
        # 不符合计算，但使用原始数据符合可保留
        productList[0].discountId.add(bean.id)
        return productList
    else:
        # 符合活动条件，进行计算
        if has_is_discount_product:
            operation_combination_moenyback(bean, userInfo, productListA, max_double_times)
        else:
            # 说明没有可以参与促销计算的商品，直接返回
            productList[0].discountId.add(bean.id)
            return productList

    return productList