#!/usr/bin/env python
"""

   encoding: utf-8
   2018/11/24 4:22 PM
   
   计算循环值
   by李博文
"""


def buy_a_for_value(product_listA, give_product, bean):
    """

    :param product_listA: 所有买A赠A的商品列表
    :param bean 活动
    :return: [商品循环值,赠品循环值 ,最大赠数]

    """

    # 总数量
    sum_pro = 0

    give_pro_sum = 0

    # 游标值
    cursor_max_times = 0

    # 商品最大循环值
    for_pro = 0

    # 赠品最大循环值
    for_give_pro = 0

    # 最大赠送数
    give_pro_number = 0

    value_num = 0
    if bean.value_num == 0:
        value_num = 1
    if bean.max_times == 0:
        bean.max_times = 1

    value_num = bean.value_num

    # 先算出当前商品的未站位数量
    for product in product_listA:
        sum_pro += product.notOccupiedThree()

    # 进入死循环 查出当前最大商品循环值 与 赠品循环值

    while True:
        # 若当前游标值等于当前最大翻倍数 终止函数
        if cursor_max_times == bean.max_times:
            return for_pro, for_give_pro, give_pro_number

        # 若当前商品最大数减去比较值大于0 说明可以执行相反则终止函数运行
        if not sum_pro - value_num >= 0:
            return for_pro, for_give_pro, give_pro_number
        # 此时循环值加
        sum_pro -= value_num
        # 商品最大循环值加上比较值
        for_pro += value_num

        # 此时在判断当前最大数量减去赠品数量是否大于等于0
        if not sum_pro - bean.give_value >= 0:
            # 若不大于0说明没了此时赠品最大循环值加上 当前sum_pro 所剩余的数量
            for_give_pro += sum_pro
            # 最大赠送数加赠送数
            give_pro_number += bean.give_value

            return for_pro, for_give_pro, give_pro_number
        # 否则则减去
        sum_pro -= bean.give_value
        # 循环值加上赠送数量
        for_give_pro += bean.give_value
        # 最大赠送数加 赠送数
        give_pro_number += bean.give_value

        # 最后让游标加1
        cursor_max_times += 1


def tidu_give_pro(bean, productList, index, off):
    """

    :param bean: 活动
    :param productList: 所有商品
    :param index: 下标志
    :return: 赠送列表
    """
    give_product = []
    T = False
    cursor = 0
    list1 = []
    # 遍历从当前最大的条件到赠送最小商品
    for i in range(0, len(bean.operation_set)):
        # 遍历 所有条款存在赠送列表中
        if not off == True:
            if bean.operation_set[i] == bean.operation_set[index]:
                break


        # 先将当前所有档位的增添

        for eocde in bean.operation_set[i].buygift_product:
            list1.append(eocde["ECODE"])

        # for eocde in bean.operation_set[i].buygift_product:
        #     if T == True:
        #         if eocde["ECODE"] == bean.operation_set[cursor].buygift_product["ECODE"]:
        #             continue
        #     for product in productList:
        #
        #         if product.ecode == eocde["ECODE"]:
        #             give_product.append(product)
        # T = True
        # cursor += 1
    list1 = list(set(list1))
    for i in list1:
        for product in productList:
            if product.ecode.lower() == i.lower():
                # 匹配ecode
                give_product.append(product)
    return give_product

def fuwei(productList):
    for product in productList:
        for seat in product.productSeatList:
            seat.seat = False
            seat.is_run_other_pro = True
    return productList

def tongji(productList):
    promotion_qtty_sum = 0
    promotion_amt_list_sum = 0
    promotion_amt_retail_sum = 0
    promotion_amt_receivable_sum = 0

    #没有限制条件商品的统计结果，为做任何其它活动未执行时，判断当前促销是否可执行使用而记录 --- add by hexiaoxia 2019/04/15
    org_promotion_qtty_sum = 0
    org_promotion_amt_list_sum = 0
    org_promotion_amt_retail_sum = 0
    org_promotion_amt_receivable_sum = 0

    for product in productList:
        for seat in product.productSeatList:
            if seat.seat == False and seat.is_run_other_pro == True:
                promotion_qtty_sum += 1
                promotion_amt_list_sum += seat.amt_list
                promotion_amt_retail_sum += seat.amt_retail
                promotion_amt_receivable_sum += seat.amt_receivable

            org_promotion_qtty_sum += 1
            org_promotion_amt_list_sum += seat.amt_list
            org_promotion_amt_retail_sum += seat.amt_retail
            org_promotion_amt_receivable_sum += seat.amt_receivable


    return promotion_qtty_sum,promotion_amt_list_sum,promotion_amt_retail_sum,promotion_amt_receivable_sum,org_promotion_qtty_sum,org_promotion_amt_list_sum,org_promotion_amt_retail_sum,org_promotion_amt_receivable_sum

