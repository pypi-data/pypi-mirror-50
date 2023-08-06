# -*- coding:utf-8 -*-
"""
    统一买免 活动详细运算
    2018/11/14
    by李博文
"""
import math
from pro.apis.GA_api.BG_api.basics_bg import get_product_sum
from pro.apis.GA_api.BG_api.buy_a_for_value import tongji
import math
from pro.utils.linq import linq
from pro.utils.util import CalculationPrice

def condition(bean, userInfo, productListA, promotion_qtty_sum):
    """
    此函数的功能只是为了更改对象的属性 不用返回值
    :param bean: 活动
    :param userInfo:  会员对象
    :param productListA: 所有可以参加买免的商品
    :param promotion_qtty_sum 所有可以参加活动商品的总数量
    :return:
    """

    if len(productListA) != 1:
        # 排序
        productListA = sorted(productListA, key=lambda i: i.productSeatList[0].amt_receivable, reverse=True)
    else:
        productListA[0].productSeatList = sorted(productListA[0].productSeatList, key=lambda i:i.amt_receivable, reverse=True)
    # 如果比较值为g大于 比较值加1
    if bean.comp_symb_type == "g":
        bean.value_num += 1

    # 如果比较值为0 或者 最大翻倍值为0 那么退出当前函数
    if bean.value_num == 0 or bean.max_times == 0:
        bean.max_times = 1

    # 定义翻倍游标
    cursor = 0
    # 如果不满足条件直接返回
    if not promotion_qtty_sum >= bean.value_num:
        return
    # 此时进入更改商品详细属性
    # 2019-07-11修改， 为了特例品这个条件。
    # 最大翻倍次数
    max_double_times = int(get_product_sum(productListA) / bean.value_num)
    if max_double_times > 1:
        if bean.max_times == 0:
            max_double_times = 1
        elif bean.max_times != -1:
            max_double_times = bean.max_times

    # 特例品数量
    special_product_qtty = 0

    # 计算可参与的商品中有多少特例品
    for product in productListA:
        for seat in product.productSeatList:
            if seat.seat == False and seat.is_run_other_pro != False and seat.is_discount == "n":
                special_product_qtty += seat.qtty

    times = int(math.ceil(special_product_qtty / (bean.value_num - bean.buy_from_value)))
    if times > max_double_times:
        times = max_double_times
    max_double_times = max_double_times - int(times)
    # is_order = False
    # if times > 0:
    #     is_order = True
    while times > 0:
        # 占位条件商品
        # # 将商品由高到低
        # if len(productListA) != 1:
        #     # 排序
        #     productListA = sorted(productListA, key=lambda i: i.productSeatList[0].amt_receivable, reverse=True)
        # else:
        #     productListA[0].productSeatList = sorted(productListA[0].productSeatList,
        #                                              key=lambda i: i.amt_receivable,
        #                                              reverse=True)
        for_pro = bean.value_num - bean.buy_from_value
        for product in productListA:
            for seat in product.productSeatList:
                if for_pro == 0:
                    break
                if seat.seat == False and seat.is_run_other_pro != False and seat.is_discount == "n":
                    one_product_seat(seat, product, bean, userInfo)
                    for_pro -= 1
        if for_pro != 0:
            for product in productListA:
                for seat in product.productSeatList:
                    if for_pro == 0:
                        break
                    if seat.seat == False and seat.is_run_other_pro != False:
                        one_product_seat(seat, product, bean, userInfo)
                        for_pro -= 1
        # 更改免去值商品
        # # 将商品由低到高排序
        # if len(productListA) != 1:
        #     # 排序
        #     productListA = sorted(productListA, key=lambda i: i.productSeatList[0].amt_receivable, reverse=False)
        # else:
        #     productListA[0].productSeatList = sorted(productListA[0].productSeatList,
        #                                              key=lambda i: i.amt_receivable,
        #                                              reverse=False)
        mian_pro(productListA, bean, userInfo, bean.buy_from_value)
        times -= 1

    # if is_order:
    #     # 将商品由高到低
    #     if len(productListA) != 1:
    #         # 排序
    #         productListA = sorted(productListA, key=lambda i: i.productSeatList[0].amt_receivable, reverse=True)
    #     else:
    #         productListA[0].productSeatList = sorted(productListA[0].productSeatList,
    #                                                  key=lambda i: i.amt_receivable,
    #                                                  reverse=True)
    while True:
        if max_double_times <= 0:
            # 如果已经达到最大翻倍次数， 则退出循环
            if bean.comp_symb_type == "g":
                bean.value_num -= 1
            return

        # 比较值减去买免值等于可以参加活动的商品
        for_pro = bean.value_num - bean.buy_from_value
        # 更改条件商品
        pro_number(productListA, bean, userInfo, for_pro)
        # 更改免去值商品
        mian_pro(productListA, bean, userInfo, bean.buy_from_value)
        cursor += 1
        max_double_times -= 1


# def combination_maimian_condition(bean, userInfo, productList, max_double_times, double_numb, special_all):
#     """
#     组合买免计算总方法
#     :param bean: 活动信息
#     :param userInfo: 会员信息
#     :param productList: 参与商品
#     :param max_double_times: 最大翻倍次数
#     :return:
#     """
#     # 首先根据应收价降序排序
#     productList = sorted(productList, key=lambda i: i.productSeatList[0].amt_receivable, reverse=True)
#     while True:
#         # 当翻倍次数减到0时，退出
#         if max_double_times <= 0:
#             return
#         # 统计当前有多少可参与计算的商品
#         promotion_qtty_sum = tongjiqtty(productList)
#         # 当没有未占位（且能参与计算）的商品时，返回
#         if promotion_qtty_sum <= 0:
#             return
#         # 每一倍参与的数量
#         one_double_numb = int(double_numb)
#         # 每一倍具体计算
#         for_pro = int(double_numb - bean.buy_from_value)
#         has_special_pro_flug = False  # 有无特例品
#         for special_item in special_all:
#             special_item["can_use_num"] = special_item["value_num"]  # 每一行可以参与的数量
#             if special_item["has_special_product"]:
#                 has_special_pro_flug = True
#
#         # 如果有特例品的话， 条件商品优先占位特例品
#         if has_special_pro_flug:
#             # 首先占位特例品
#             for product in productList:
#                 if for_pro <= 0:
#                     # 如果条件商品已经占完，结束循环
#                     break
#                 # 如果当前商品不是特例品，进入下一个商品判断
#                 if product.productSeatList[0].is_discount == "y":
#                     continue
#                 for special_item in special_all:
#                     if for_pro <= 0:
#                         break
#                     # 如果当前行
#                     if special_item["can_use_num"] <= 0:
#                         continue
#                     if product.ecode in special_item.get("ecode"):
#                         for seat in product.productSeatList:
#                             if for_pro <= 0:
#                                 break
#                             if special_item["can_use_num"] <= 0:
#                                 break
#                             if seat.seat == False and seat.is_run_other_pro:
#                                 # 条件商品占位
#                                 one_product_seat(seat, product, bean, userInfo)
#                                 special_item["can_use_num"] = special_item["can_use_num"] - 1
#                                 for_pro -= 1
#                                 one_double_numb -= 1
#         if for_pro > 0:
#             for special_item in special_all:
#                 if special_item["can_use_num"] != 0:
#                     if special_item["has_special_product"]:
#                         special_item["has_special_product"] = False
#
#         for product in productList:
#             if one_double_numb <= 0:
#                 break
#             for special_item in special_all:
#                 if one_double_numb <= 0:
#                     break
#                 if special_item["can_use_num"] <= 0:
#                     continue
#                 if product.ecode in special_item.get("ecode"):
#                     for seat in product.productSeatList:
#                         if one_double_numb <= 0:
#                             break
#                         if special_item["can_use_num"] <= 0:
#                             break
#                         if seat.seat == False and seat.is_run_other_pro:
#                             if for_pro <= 0:
#                                 # 免去商品占位
#                                 one_mianjian(seat, product, bean)
#                             else:
#                                 # 条件商品占位
#                                 one_product_seat(seat, product, bean, userInfo)
#                                 for_pro -= 1
#                                 one_double_numb -= 1
#                             special_item["can_use_num"] = special_item["can_use_num"] - 1
#         max_double_times -= 1

def combination_maimian_condition(bean, userInfo, productList, max_double_times, double_numb, special_all):
    """
    组合买免计算总方法
    :param bean: 活动信息
    :param userInfo: 会员信息
    :param productList: 参与商品
    :param max_double_times: 最大翻倍次数
    :return:
    """
    # 首先根据应收价降序排序
    productList = sorted(productList, key=lambda i: i.productSeatList[0].amt_receivable, reverse=True)
    while True:
        # 当翻倍次数减到0时，退出
        if max_double_times <= 0:
            return
        # 统计当前有多少可参与计算的商品
        promotion_qtty_sum = tongjiqtty(productList)
        # 当没有未占位（且能参与计算）的商品时，返回
        if promotion_qtty_sum <= 0:
            return
        seat_list = []
        seat_product_list = []
        has_normal_product = False
        for spec_item in special_all:
            # 比较值
            value_num = spec_item.get("value_num")
            buy_from_value = bean.buy_from_value
            if buy_from_value > value_num:
                buy_from_value = value_num
            new_special_seat_list = []
            new_special_pro_seat_list = []
            current_num = 0
            # 当前行条件值
            condition_num = value_num - bean.buy_from_value if value_num - bean.buy_from_value > 0 else 0
            # new_value_num = value_num
            if spec_item.get("has_special_product"):
                for product in productList:
                    if value_num <= 0:
                        # 如果条件商品已经占完，结束循环
                        break
                    # 如果当前商品不是特例品，进入下一个商品判断
                    if product.productSeatList[0].is_discount == "y":
                        continue
                    if product.ecode not in spec_item.get("ecode"):
                        continue
                    for seat in product.productSeatList:
                        if value_num <= 0:
                            break
                        if seat.seat == False and seat.is_run_other_pro:
                            # 条件商品占位
                            if condition_num > 0:
                                if seat not in seat_list:
                                    seat_list.append(seat)
                                    seat_product_item = {"seat": seat, "product": product}
                                    seat_product_list.append(seat_product_item)
                                condition_num -= 1
                                current_num += 1
                            else:
                                if seat not in new_special_seat_list:
                                    new_special_seat_list.append(seat)
                                    seat_product_item = {"seat": seat, "product": product}
                                    new_special_pro_seat_list.append(seat_product_item)

                            value_num -= 1

                if condition_num > 0:
                    spec_item["has_special_product"] = False

            value_num = value_num if value_num >= buy_from_value else buy_from_value
            for product in productList:
                if value_num <= 0:
                    # 如果当前已经占完， 结束循环
                    break
                # 如果当前商品不是特例品，进入下一个商品判断
                if product.productSeatList[0].is_discount == "n":
                    continue
                if product.ecode not in spec_item.get("ecode"):
                    continue
                for seat in product.productSeatList:
                    if value_num <= 0:
                        break
                    if seat.seat == False and seat.is_run_other_pro:
                        has_normal_product = True
                        if seat not in seat_list:
                            seat_list.append(seat)
                            seat_product_item = {"seat": seat, "product": product}
                            seat_product_list.append(seat_product_item)
                        value_num -= 1
                        current_num += 1

            if current_num < spec_item.get("value_num"):
                range_num = spec_item.get("value_num") - current_num
                if len(new_special_seat_list) < range_num:
                    range_num = len(new_special_seat_list)
                for i in range(int(range_num)):
                    if new_special_seat_list[i] not in seat_list:
                        seat_list.append(new_special_seat_list[i])
                        seat_product_list.append(new_special_pro_seat_list[i])

        if not has_normal_product:
            break
        buy_from_value = bean.buy_from_value
        seat_product_list = sorted(seat_product_list, key=lambda x: x.get("seat").amt_receivable)
        for seat_item in seat_product_list:
            seat = seat_item.get("seat")
            product = seat_item.get("product")
            if seat.is_discount == "n":
                one_product_seat(seat, product, bean, userInfo)
            else:
                if buy_from_value <= 0:
                    one_product_seat(seat, product, bean, userInfo)
                else:
                    # 免去商品占位
                    one_mianjian(seat, product, bean)
                    buy_from_value -= 1
        max_double_times -= 1


def combination_maimian_operation(bean, userInfo, productList):
    """
    组合买免每一倍计算
    :param bean:
    :param userInfo:
    :param productList:
    :return:
    """
    # 商品应收价降序排序
    productList = sorted(productList, key=lambda i: i.productSeatList[0].amt_receivable, reverse=True)

    part_product_ecode = []  # 参与商品款号列表
    part_product_ecode_sum = {}  # 每个款号，参与计算的数量
    for spec_item in bean.specific_activities:
        current_part_product_ecode_sum = {}  # 当前行参与计算的每个款的数量
        # 比较值
        value_num = spec_item.value_num
        if spec_item.comp_symb_type == "g":
            value_num = value_num + 1

        current_sum = 0  # 当前参与计算的总数
        max_value_num_sum = value_num  # 当前行计算值（比较值），达到这个值后，后面的商品就不再计算了
        for product in productList:
            if current_sum >= max_value_num_sum:
                break
            if linq(spec_item.product_list).where(lambda x: str(x).lower() == product.ecode.lower()).count() < 1:
                continue

            if product.notOccupiedThree() <= 0:
                # 如果没有未占位的商品，进入下一个商品
                continue
            if product.ecode.lower() not in part_product_ecode:
                part_product_ecode.append(product.ecode.lower())
            # 计算条件所需要的数量
            if str(spec_item.target_type).lower() == "qtty":
                request_qty = max_value_num_sum - current_sum
            elif str(spec_item.target_type).lower() == "amt_list":
                request_qty = math.ceil((max_value_num_sum - current_sum) / product.amt_list)
            elif str(spec_item.target_type).lower() == "amt_retail":
                request_qty = math.ceil((max_value_num_sum - current_sum) / product.amt_retail)
            elif str(spec_item.target_type).lower() == "amt_receivable":
                request_qty = 0
                for seat in product.productSeatList:
                    if current_sum >= max_value_num_sum:
                        break
                    if seat.seat == False and seat.is_run_other_pro == True:
                        current_sum += seat.amt_receivable
                        request_qty += 1
                if current_sum < max_value_num_sum:
                    request_qty += 1

            if product.notOccupiedThree() >= request_qty:
                # 如果当前未占位商品大于所需要的数量，则直接改数量之后，将当前计算值改为最大计算值
                current_part_product_ecode_sum[product.ecode.lower()] = current_part_product_ecode_sum.get(
                        product.ecode.lower(), 0) + request_qty
                current_sum = max_value_num_sum
            else:
                # 如果当前行未展位商品没有达到要求，将数量加到current_part_product_ecode_sum中
                current_part_product_ecode_sum[product.ecode.lower()] = current_part_product_ecode_sum.get(
                        product.ecode.lower(), 0) + product.notOccupiedThree()
                # 将当前行的总和（数量或者金额）加入到当前计算值
                if str(spec_item.target_type).lower() == "qtty":
                    current_sum += product.notOccupiedThree()
                if str(spec_item.target_type).lower() == "amt_list":
                    current_sum += product.amt_list * product.notOccupiedThree()
                elif str(spec_item.target_type).lower() == "amt_retail":
                    current_sum += product.amt_retail * product.notOccupiedThree()
        # 这个传值顺序不同，计算结果会不同，现不使用
        # for ecode in spec_item.product_list:
        #     # 数量已经达到最大值，则退出当前循环
        #     if current_sum >= max_value_num_sum:
        #         break
        #     for product in productList:
        #         if current_sum >= max_value_num_sum:
        #             break
        #         if ecode.lower() == product.ecode.lower():
        #             if product.notOccupiedThree() <= 0:
        #                 # 如果没有未占位的商品，进入下一个商品
        #                 continue
        #
        #             if ecode.lower() not in part_product_ecode:
        #                 part_product_ecode.append(ecode.lower())
        #
        #             # 计算条件所需要的数量
        #             if str(spec_item.target_type).lower() == "qtty":
        #                 request_qty = max_value_num_sum - current_sum
        #             elif str(spec_item.target_type).lower() == "amt_list":
        #                 request_qty = math.ceil((max_value_num_sum - current_sum) / product.amt_list)
        #             elif str(spec_item.target_type).lower() == "amt_retail":
        #                 request_qty = math.ceil((max_value_num_sum - current_sum) / product.amt_retail)
        #             elif str(spec_item.target_type).lower() == "amt_receivable":
        #                 request_qty = 0
        #                 for seat in product.productSeatList:
        #                     if current_sum >= max_value_num_sum:
        #                         break
        #                     if seat.seat == False and seat.is_run_other_pro == True:
        #                         current_sum += seat.amt_receivable
        #                         request_qty += 1
        #                 if current_sum < max_value_num_sum:
        #                     request_qty += 1
        #
        #             if product.notOccupiedThree() >= request_qty:
        #                 # 如果当前未占位商品大于所需要的数量，则直接改数量之后，将当前计算值改为最大计算值
        #                 current_part_product_ecode_sum[ecode.lower()] = current_part_product_ecode_sum.get(
        #                     ecode.lower(), 0) + request_qty
        #                 current_sum = max_value_num_sum
        #             else:
        #                 # 如果当前行未展位商品没有达到要求，将数量加到current_part_product_ecode_sum中
        #                 current_part_product_ecode_sum[ecode.lower()] = current_part_product_ecode_sum.get(
        #                     ecode.lower(), 0) + product.notOccupiedThree()
        #                 # 将当前行的总和（数量或者金额）加入到当前计算值
        #                 if str(spec_item.target_type).lower() == "qtty":
        #                     current_sum += product.notOccupiedThree()
        #                 if str(spec_item.target_type).lower() == "amt_list":
        #                     current_sum += product.amt_list * product.notOccupiedThree()
        #                 elif str(spec_item.target_type).lower() == "amt_retail":
        #                     current_sum += product.amt_retail * product.notOccupiedThree()

        if current_part_product_ecode_sum:
            # 将参与活动的所有商品所需数量与当前行中个款号所需数量进行对比，没有则加上，小于也加上
            for key, value in current_part_product_ecode_sum.items():
                if part_product_ecode_sum.get(key, 0) < value:
                    part_product_ecode_sum[key] = value

    # 计算可参与的商品的总的数量：
    part_qtty_sum = 0
    for key, value in part_product_ecode_sum.items():
        part_qtty_sum += value

    # 买免值
    # 比较值减去买免值等于可以参加活动的商品
    for_pro = part_qtty_sum - bean.buy_from_value

    # 具体占位计算
    calculation_maimian_combination(bean, userInfo, productList, for_pro, part_product_ecode_sum)

def calculation_maimian_combination(bean, userInfo, productListA, for_pro, part_prosuct_num):
    """
    组合买免具体占位
    :param bean: 活动信息
    :param userInfo: 会员信息
    :param productListA: 商品
    :param for_pro: 条件商品数量
    :param part_prosuct_num: 参与的各个商品的数量
    :return:
    """
    # 循环参与活动的商品
    for product in productListA:
        # 判断当前商品是否参与计算
        if part_prosuct_num.get(product.ecode.lower(), 0) <= 0:
            break
        # 循环
        for seat in product.productSeatList:
            # 当前商品参与计算的数量小于等于0是，结束当前循环
            if part_prosuct_num.get(product.ecode.lower(), 0) <= 0:
                break
            if seat.seat == False and seat.is_run_other_pro != False:
                # 当条件商品还未计算完成时，先更改条件商品
                if for_pro > 0:
                    # 更改条件商品
                    one_product_seat(seat, product, bean, userInfo)
                    # 条件值减1
                    for_pro -= 1
                else:
                    # 更改买免值
                    one_mianjian(seat, product, bean)
                # 当前商品参与数量减一
                part_prosuct_num[product.ecode.lower()] = part_prosuct_num.get(product.ecode.lower(), 0) - 1


def mian_pro(productListA, bean, userInfo, mian_pro):
    """
    :param productListA:
    :param bean:
    :param userInfo:
    :param mian_pro: 免去商品数量
    :return:
    """
    for product in productListA:
        for mian_seat in product.productSeatList:
            if mian_pro == 0:
                break
            if mian_seat.seat == False and mian_seat.is_run_other_pro != False and mian_seat.is_discount == "y":
                one_mianjian(mian_seat, product, bean)
                mian_pro -= 1


def pro_number(productListA, bean, userInfo, for_pro):
    """
    只更改条件商品的循环次数
    :param productListA: 活动列表
    :param bean: 活动
    :param userInfo: 会员
    :return: 不返回
    for_pro 循环次数
    """
    for product in productListA:
        for seat in product.productSeatList:
            if for_pro == 0:
                break
            if seat.seat == False and seat.is_run_other_pro != False:
                one_product_seat(seat, product, bean, userInfo)
                for_pro -= 1


def one_mianjian(seat, product, bean):
    """
    用来标记免件数量 并把应收价更改为0
    :param seat: 当前商品明细
    :param product: 当前商品
    :return:
    """
    # 1 将此商品标记成已站位
    # 2 将商品总数量减一
    # 3 将当前商品的应收金额更改为0
    if seat.is_run_other_pro == False:
        return  # 不可以进行商品活动
    # 因翻倍限制所不能参加的活动 - --活动ID
    if seat.notProId:
        for id in seat.notProId:
            if id == bean.id:
                return

    seat.seat = True

    product.qttyCount -= 1

    seat.discountPrice.append(seat.amt_receivable)

    seat.amt_receivable = 0

    seat.discountId.append(bean.id)

    # 增加标记让全场标记识别属性
    seat.is_taken_off = True

    product.discountId.add(bean.id)
    # 是否与其他商品活动同时执行
    seat.is_run_other_pro = False
    # 是否与全场活动同时执行
    seat.is_run_store_act = False


def one_product_seat(seat, product, bean, userInfo):
    """
    :param seat: 商品明细
    :param product: 商品
    :param bean: 活动
    :return:
    """

    # 1 更改当前商品站位信息
    # 2 记录当前活动id
    # 3 判断是否可以参加vip
    # 4 是否允许与其他商品活动允许一起执行
    if seat == None or bean == None:
        return

    # 因翻倍限制所不能参加的活动 - --活动ID
    if seat.notProId:
        for id in seat.notProId:
            if id == bean.id:
                return

    if seat.is_run_other_pro == False:
        return  # 不可以进行商品活动

    if seat.seat:
        return  # 商品已占位
    # 标记剩余未参加商品数量
    product.qttyCount -= 1

    # 将以什么优惠基础的取出
    discount_value = bean.target_item
    # 活动是否允许折上折
    if bean.is_run_vip_discount:
        if seat.is_run_vip_discount == False:
            if userInfo.discount != None:
                # 设置当前商品已经参加过vip折中折
                seat.is_run_vip_discount = True

                vipPric = float(seat.amt_receivable * userInfo.discount)
                # vipPric = round(vipPric, 2)
                vipPric = CalculationPrice(vipPric)  # 根据进位参数计算金额

                # 计算vip 折中折优惠金额
                vipMoney = seat.amt_receivable - vipPric
                # vipMoney = round(vipMoney, 2)
                vipMoney = CalculationPrice(vipMoney)

                # 记录vip 优惠折扣
                seat.discountPrice.append(vipMoney)

                # 当前价格设置为已参加过vip折中折
                seat.amt_receivable = vipPric

    # 是否与其他商品活动同时执行
    seat.is_run_other_pro = bean.is_run_other_pro
    # 是否与全场活动同时执行
    seat.is_run_store_act = bean.is_run_store_act
    # 当前三类中占位
    seat.seat = True
    # 加入参加过的活动ID
    product.discountId.add(bean.id)


def tongjiqtty(productList):
    """
    计算当前有多少可参与计算的商品
    :param productList:
    :return:
    """
    promotion_qtty_sum = 0
    promotion_qtty_no_discount = 0
    for product in productList:
        for seat in product.productSeatList:
            if seat.seat == False and seat.is_run_other_pro == True:
                if seat.is_discount == "y":
                    promotion_qtty_sum += 1
                else:
                    promotion_qtty_no_discount += 1

    return promotion_qtty_sum