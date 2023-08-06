# -*- coding:utf-8 -*-
"""
    当前活动的择优
    2018/10/29
    by李博文
"""
import copy

def current_promitions_preferential(productListMax):
    """
    :param productListMax: 参加过的活动的商品列表
    :return: 以赠品的价格来择优
    """

    for product_ListA in productListMax:
        give_sum = 0
        for product in product_ListA["product"]:

            for seat in product.productSeatList:

                if str(seat.is_buy_gifts).lower() == "y":
                    give_sum += seat.amt_list
            product.give_sum = give_sum

    return max(productListMax, key=lambda i: i["product"][-1].give_sum)


def current_promitions_id(product_id_notNone):
    """

    :param product_id_notNone: 所有未完结的商品信息
    :return: 整合完的数据
    """

    # 存放数据的列表
    current_list = []

    # 存在product记录id的
    current_set = []

    # 第一组数据
    product_1 = product_id_notNone[0]

    # 遍历第二组数据将其取出
    for number_2 in product_id_notNone:

        if not current_list:
            for not_product in number_2:
                current_set.append(copy.deepcopy(not_product.discountId))
                # 循环遍历所有商品明细 将所有id 与 是否赠品取出
                for not_seat in not_product.productSeatList:
                    current_list.append(copy.deepcopy([not_seat.discountId, not_seat.is_buy_gifts]))
        else:
            # 此时存放数据列表已经有了第一组商品的所有数据

            # 游标 id
            cursor_id = 0

            for product in number_2:
                current_set.append(product.discountId)
                for seat in product.productSeatList:
                    if len(seat.discountId) >= 1:


                        for i in seat.discountId:
                            current_list[cursor_id][0].append(copy.deepcopy(i))

                    if not seat.is_buy_gifts == "n":
                        current_list[cursor_id][1] = seat.is_buy_gifts

                    # 游标加1
                    cursor_id += 1

    # 定义第二个游标
    cursor_id_2 = 0
    # 拼接数据
    for product in product_1:

        for seat in product.productSeatList:
            for i in current_list[cursor_id_2][0]:
                if i not in seat.discountId:
                    seat.discountId.append(i)
            seat.is_buy_gifts = current_list[cursor_id_2][1]

            cursor_id_2 += 1

    for product in product_1:
        for seat in product.productSeatList:
            if len(seat.discountId) > 0:
                for i in seat.discountId:
                    product.discountId.add(i)


    return product_1
