# -*- coding:utf-8 -*-
# author:weiyanping
# datetime:2019/4/23 20:00
# software: PyCharm

import copy
from pro.apis.GA_api.PE_api.current_zeyou import current_zeyou
from pro.apis.GA_api.BG_api.buy_a_for_value import tongji
from pro.apis.GA_api.PE_api.current_zeyou import result_data
from pro.apis.GA_api.PE_api.basics_maimian import combination_maimian_condition

def preferential_com_maimian(product_object_list, combination_buygift_list, userInfo , product_List):
    """

    :param product_object_list: 所有商品
    :param combination_buygift_list: 所有组合买免活动
    :param userInfo:  会员对象
    :return: 最优活动
    """

    productListMAX = []
    list1 = copy.deepcopy(product_object_list)
    combination_buygift_list = sorted(combination_buygift_list, key=lambda x: x.publish_date, reverse=True)
    index_cursor = 0
    for index in range(0, len(combination_buygift_list)):

        for bean in combination_buygift_list:
            # 返回每个方案计算后的商品集合
            list1 = combination_maimian(list1, bean, userInfo)

        productListMAX.append(list1)

        # 游标加1
        index_cursor += 1

        # 将当前下标与这次循环下标交换
        if len(combination_buygift_list) > 1:
            if index_cursor != len(combination_buygift_list):
                combination_buygift_list[0], combination_buygift_list[index_cursor] = combination_buygift_list[index_cursor], \
                                                                                      combination_buygift_list[0]
                list1 = copy.deepcopy(product_object_list)

    # 整合数据
    response = current_zeyou(productListMAX)
    # response = result_data(response, productListMAX)
    return response



def combination_maimian(productList, bean, userInfo):
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

    # 当前商品信息是否可以参加此活动， 如果为-1的话，表示原始商品满足条件，可以作为可以参加的活动，但是不在择优执行列表中
    is_can_executed = 1
    productListA = []  # 参与条件的商品
    part_product_ecode = []  # 参与活动的商品的款号
    max_double_times = 0  # 当前最大可以翻倍的次数
    special_all = []
    double_numb = 0
    # 对每个组合条件进行循环
    for spec_item in bean.specific_activities:
        # 将该行的条件商品拎出来
        current_part_product = []
        has_special_product = False  # 是否有特例品
        for ecode in spec_item.product_list:
            for product in productList:
                if ecode.lower() == product.ecode.lower():
                    current_part_product.append(product)
                    part_product_ecode.append(ecode.lower())
                    if product.productSeatList[0].is_discount == "n":
                        has_special_product = True

        # 如果没有符合条件的商品，说明不满足执行条件，不执行
        if not current_part_product:
            return productList

        # 计算当前商品中未占位的总数量，总价格（包括零售，吊牌，应收价）
        promotion_qtty_sum, _, _, _, org_promotion_qtty_sum, _, _, _ = tongji(
            current_part_product)

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
                is_can_executed = -1  # 原始商品满足条件
            p = int(promotion_qtty_sum) // int(value_num)  # 当前可以翻的倍数

        # 和之前存储的翻倍进行比较，如果小于之前的翻倍，将翻倍次数修改
        if max_double_times == 0 or max_double_times > p:
            max_double_times = p
        double_numb += value_num
        special_all.append({"ecode": spec_item.product_list, "has_special_product": has_special_product,
                            "value_num": spec_item.value_num})

    # 可以参与此活动的商品款号
    part_product_ecode = list(set(part_product_ecode))
    has_can_caculate_pro = False
    # 找出总的符合该条件的商品
    for ecode in part_product_ecode:
        for product in productList:
            if ecode.lower() == product.ecode.lower():
                productListA.append(product)
                if product.productSeatList[0].is_discount == "y":
                    has_can_caculate_pro = True

    if is_can_executed == -1:
        # 说明该促销可以保留到可以参与的促销中
        # 不符合计算，但使用原始数据符合可保留
        productList[0].discountId.add(bean.id)
        return productList
    else:
        if not has_can_caculate_pro:
            # 说明没有可以参与促销运算的商品， 直接返回
            # productList[0].discountId.add(bean.id)  # 但符合条件，可以保留
            return productList
        # 翻倍，比较活动的翻倍限制，再对翻倍次数进行修改
        if max_double_times > 1:
            if bean.max_times == 0 or bean.max_times == 1:
                max_double_times = 1
            elif bean.max_times > 1 and max_double_times > bean.max_times:
                max_double_times = bean.max_times

        # 符合活动条件，进行计算
        combination_maimian_condition(bean, userInfo, productList, max_double_times, double_numb, special_all)

    return productList
