# -*- coding:utf-8 -*-
"""
    基础运算买赠
    2018/11/13
    by李博文
"""
from pro.utils.util import CalculationPrice
from pro.utils.util import flattenDiffPirce
from pro.utils.util import minus
from pro.apis.GA_utils import result_max_pro
from pro.apis.GA_api.BG_api.buy_a_for_value import tongji
from pro.apis.GA_api.DC_api.basics import splitDiffPrice
import pro.utils.util as util

def condition_qtty(bean, userInfo, productListA, condition_sum,org_condition_sum):
    """
    以数量满足
    2018/11/23
    by李博文
    edit by hexiaoxia 2019/04/15
    当占位商品不满足该促销时，那么判断原始数据商品是否满足该活动，满足则该活动对于该单据是可以单独执行的，供前端单独选择促销使用
    :param bean: 活动对象
    :param userInfo: 会员对象
    :param productListA: 可以参加活动的商品
    :param condition_sum: 条件总数（可参与该活动并且未占位且可参与同时与该活动叠加执行）
    :param org_condition_sum: 条件总数（原始可参与该活动的商品数据）
    :return:
    """

    # 如果总数不满足条件那么返回
    if bean.comp_symb_type == "g":
        bean.value_num += 1

    if not condition_sum >= bean.value_num:
        #add by hexiaoxia 2019/04/15
        if org_condition_sum>=bean.value_num:
            productListA[0].discountId.add(bean.id)

        return int(-1)

    # get_re = int(get_retail_carryway())
    #     # 如果进位参数不为 四舍五入取整或者 2 那么return
    # if not get_re != None or get_re != 2:
    #     return


    for row in productListA:
        if bean.target_item.lower() == 'amt_list':
            row.amt_receivable=row.amt_list
        elif bean.target_item.lower() == 'amt_retail':
            row.amt_receivable = row.amt_retail
        for r_seat in row.productSeatList:
            if bean.target_item.lower() == 'amt_list':
                r_seat.amt_receivable = r_seat.amt_list
            elif bean.target_item.lower() == 'amt_retail':
                r_seat.amt_receivable = r_seat.amt_retail

    # 先将可以参与活动的列表排序
    productListA = sorted(productListA, key=lambda i: i.productSeatList[0].amt_receivable, reverse=True)

    isvipdis = True

    if bean.is_run_vip_discount:
        if userInfo.discount != None:
            num=0
            for r_row in productListA:
                for r1 in r_row.productSeatList:
                    if r1.is_run_vip_discount:
                        isvipdis=False
                        break
    else:
        isvipdis = False


    # 转换条件类型
    try:
        bean.max_times = int(bean.max_times)
        bean.value_num = int(bean.value_num)
        bean.comp_symb_type = str(bean.comp_symb_type).lower()
        bean.special_price = float(bean.special_price)
    except Exception as e:
        raise e

    # 计算所有商品的总应收价
    amt_receivable_sum, can_part_qtty_sum = calculation_amt_receivable(productListA)

    if can_part_qtty_sum == 0:
        # 说明可参与促销优惠的商品数量为0，直接返回
        return -1

    # 定义最终结果 用于后面计算
    result = 0

    # 用与区分是大于等于还是等于
    judge = False

    # 特价是如果是大于等于 或者大于 都不考虑翻倍
    if bean.comp_symb_type == "ge" or bean.comp_symb_type == "g":
        # 特价 / 条件 * 当前总数量 取整 计算当前特价值
        # condition_sum = can_part_qtty_sum
        # if isvipdis:
        #     formula_value = CalculationPrice((bean.special_price / bean.value_num * condition_sum)*userInfo.discount)
        # else:
        formula_value = CalculationPrice(bean.special_price / bean.value_num * condition_sum)

        # 先看公式值是否大于
        if formula_value > amt_receivable_sum:
            # 看原价与特价值那个更便宜 取更小的
            if amt_receivable_sum > bean.special_price:
                # 当特价值比较小的时候，在根据商品价格算一遍。
                special_price = calculation_special_again(productListA, bean.special_price, bean.value_num)
                if isvipdis:
                    special_price = CalculationPrice(special_price*userInfo.discount)
                else:
                    special_price=CalculationPrice(special_price)
                # 看有无特例品
                has_special_product_flug = True  # 有特例品
                if condition_sum == can_part_qtty_sum:
                    has_special_product_flug = False
                return calculate_offer_price(productListA, bean, has_special_product_flug, judge, special_price,
                                             amt_receivable_sum, 0, isvipdis)
            else:
                if isvipdis:
                    special_price = CalculationPrice(amt_receivable_sum * userInfo.discount)
                    # 需要看有无特例品
                    has_special_product_flug = True
                    if condition_sum == can_part_qtty_sum:
                        has_special_product_flug = False
                    return calculate_offer_price(productListA, bean, has_special_product_flug, judge,
                                                 special_price, amt_receivable_sum, 0, isvipdis)
                else:
                    return amt_receivable_pro(productListA, bean, judge, 0)
        elif formula_value < amt_receivable_sum:
            if isvipdis:
                formula_value = CalculationPrice(bean.special_price / bean.value_num * condition_sum)

            has_special_product_flug = True
            if condition_sum == can_part_qtty_sum:
                has_special_product_flug = False
            return calculate_offer_price(productListA, bean, has_special_product_flug, judge, formula_value,
                                         amt_receivable_sum, 0, isvipdis)
        else:
            if isvipdis:
                special_price = CalculationPrice(amt_receivable_sum * userInfo.discount)
                # 需要看有无特例品
                has_special_product_flug = True
                if condition_sum == can_part_qtty_sum:
                    has_special_product_flug = False
                return calculate_offer_price(productListA, bean, has_special_product_flug, judge,
                                             special_price, amt_receivable_sum, 0, isvipdis)
            else:
                return amt_receivable_pro(productListA, bean, judge, 0)

    # 如果满足是等于
    if bean.comp_symb_type == "e":

        p = 0
        judge = True

        # 总循环次数
        max_pro_numb = 0

        # 第一步计算翻倍
        if bean.max_times == 0 or bean.max_times == 1:
            bean.max_times = 1
            max_pro_numb = bean.value_num
            p = 1
        elif bean.max_times > 1:
            # 先看看目前商品最多能翻多少倍
            p = condition_sum // bean.value_num
            # 如果当前倍数 >= 最大翻倍数 取最大翻倍数
            if p >= bean.max_times:
                max_pro_numb = bean.value_num * bean.max_times
                p = bean.max_times
            else:
                # 否则的话取当前最大倍数
                max_pro_numb = p * bean.value_num
        else:
            # 到这是无限翻倍了
            p = condition_sum // bean.value_num
            max_pro_numb = bean.value_num * p
        # 计算当前倍数的总价格
        formula_value, can_part_amt_sum, can_part_qtty_sum = result_max_pro(productListA, max_pro_numb)
        if formula_value == 0:
            return -1
        if can_part_qtty_sum == 0:
            return -1

        # 计算倍数之后的优惠价格
        # if isvipdis:
        #     special_price = CalculationPrice(bean.special_price * p * userInfo.discount)
        # else:
        special_price = CalculationPrice(bean.special_price * p)

        # 看原价与特价值那个更便宜 取更小的
        if formula_value > special_price:
            if can_part_qtty_sum != max_pro_numb:
                # 如果有特例品的话， 特价值需要减去特例品的金额
                if isvipdis:
                    special_price = CalculationPrice(bean.special_price * p * userInfo.discount)
                special_price = CalculationPrice(special_price - (formula_value - can_part_amt_sum))
                if special_price < 0:
                    special_price = 0
            return calculation_special_price(productListA, bean, judge, special_price, can_part_amt_sum,
                                             can_part_qtty_sum, isvipdis)
        else:
            if isvipdis:
                special_price = CalculationPrice(formula_value*userInfo.discount)
                if can_part_qtty_sum != max_pro_numb:
                    # 如果有特例品的话， 特价值需要减去特例品的金额
                    special_price = CalculationPrice(special_price - (formula_value - can_part_amt_sum))
                    if special_price < 0:
                        special_price = 0
                return calculation_special_price(productListA, bean, judge, special_price, can_part_amt_sum,
                                                 can_part_qtty_sum, isvipdis)
            else:
                return amt_receivable_pro(productListA, bean, judge, max_pro_numb)



def amt_receivable_pro(productListA, bean, judge, for_value):
    """
    只更改站位什么都不管
    :param productListA:
    :param bean:
    :param judge: 控制循环次数
    :param special_price:
    :param discount_sum:
    :return:
    """
    oldsum_amt_receivable=0
    newsum_amt_receivable=0
    if not judge:
        for product in productListA:
            for seat in product.productSeatList:
                if seat.seat == False and seat.is_run_other_pro != False and seat.is_discount == "y":
                    amt_receivable_basics_one(seat, product, bean)

    else:
        for product in productListA:
            for seat in product.productSeatList:
                if for_value == 0:
                    break
                if seat.seat == False and seat.is_run_other_pro != False  and seat.is_discount == "y":
                    amt_receivable_basics_one(seat, product, bean)
                    for_value -= 1
    return "ok"

def calculation_special_price(productListA, bean, judge, special_price, discount_sum, for_value,isvipdis):
    """
    # 控制更改商品次数
    :param productListA: 商品
    :param judge: 用与控制大于等于还是 等于
    :return:
    """
    # 记录这次更改完之后的商品的金额用于最后平摊
    result = 0
    seat_list = []
    if not judge:
        for product in productListA:
            for seat in product.productSeatList:
                if seat.seat == False and seat.is_run_other_pro != False and seat.is_discount == "y":
                    result += basics_one(seat, product, bean, special_price, discount_sum, isvipdis)
                    seat_list.append(seat)

    else:
        for product in productListA:
            for seat in product.productSeatList:
                if for_value == 0:
                    break
                if seat.seat == False and seat.is_run_other_pro != False and seat.is_discount == "y":
                    result += basics_one(seat, product, bean, special_price, discount_sum, isvipdis)
                    for_value -= 1
                    seat_list.append(seat)

    # 计算总差额平摊算法
    # 如果没有差价
    # if special_price == result:
    #     return "ok"

    #有误差，误差分摊按照参数的进位方式处理
    pingtan_value = CalculationPrice(minus(special_price, result))

    # flattenDiffPirce(pingtan_value, productListA, bean.id)
    if pingtan_value != 0:
        splitDiffPrice(seat_list, bean, diffPrice=pingtan_value)

    # 计算优惠金额
    for seat1 in seat_list:
        pric = float("%.2f" % float(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
        seat1.upamt_receivable = seat1.amt_receivable
        seat1.discountPrice.append(pric)
    # # 先比较谁比较大 如果结果四舍五入之后比较大
    # if special_price > result:
    #     pingtan_value = CalculationPrice(special_price - result)
    #
    #     for product in productListA:
    #         for seat in product.productSeatList:
    #             if pingtan_value == 0:
    #                 break
    #             if bean.id not in seat.discountId:
    #                 continue
    #
    #             seat.amt_receivable = seat.amt_receivable + 1
    #             seat.discountPrice[-1] = seat.discountPrice[-1] - 1
    #             pingtan_value -= 1
    # else:
    #     # 反过来就是多了
    #     pingtan_value = CalculationPrice(result - special_price)
    #     for product in productListA:
    #         for seat in product.productSeatList:
    #             if pingtan_value == 0:
    #                 break
    #             if bean.id not in seat.discountId:
    #                 continue
    #
    #             seat.amt_receivable = seat.amt_receivable - 1
    #             seat.discountPrice[-1] = seat.discountPrice[-1] + 1
    #             pingtan_value -= 1
    return "ok"

def condition_calculation_for_double(seat_product_list, bean, special_price, amt_receivable, is_caculate, isvipdis):
    seat_list = []
    result = 0
    if is_caculate:
        for seat_item in seat_product_list:
            result += basics_one(seat_item.get("seat"), seat_item.get("product"), bean, special_price, amt_receivable,
                                 isvipdis)
            seat_list.append(seat_item.get("seat"))

        # 有误差，误差分摊按照参数的进位方式处理
        pingtan_value = CalculationPrice(minus(special_price, result))

        if pingtan_value != 0:
            splitDiffPrice(seat_list, bean, diffPrice=pingtan_value)

        # 计算优惠金额
        for seat1 in seat_list:
            pric = float("%.2f" % float(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
            seat1.upamt_receivable = seat1.amt_receivable
            seat1.discountPrice.append(pric)
    else:
        for seat_item in seat_product_list:
            amt_receivable_basics_one(seat_item.get("seat"), seat_item.get("product"), bean)

    return "ok"

def amt_receivable_basics_one(seat, product, bean):
    # 因翻倍限制所不能参加的活动 - --活动ID
    if seat.notProId:
        for id in seat.notProId:
            if id == bean.id:
                return

    if seat.is_run_other_pro == False:
        return  # 不可以进行商品活动

    if seat.seat:
        return  # 商品已占位
    if seat.is_discount == "n":
        return
    # 标记剩余未参加商品数量
    product.qttyCount -= 1
    # 是否与其他商品活动同时执行
    seat.is_run_other_pro = bean.is_run_other_pro
    # 是否与全场活动同时执行
    seat.is_run_store_act = bean.is_run_store_act
    # 当前三类中占位
    seat.seat = True

    # # 更改以什么金额计算的
    # if bean.target_item.lower() == 'amt_list':
    #     seat.amt_list = seat.amt_receivable
    # elif bean.target_item.lower() == "amt_receivable":
    #
    #     seat.amt_receivable = seat.amt_receivable
    # else:
    #     seat.amt_retail = seat.amt_receivable

    # 加入参加过的活动ID
    seat.discountId.append(bean.id)
    # 这次活动优惠的金额
    seat.discountPrice.append(0)
    # 商品记录活动id
    product.discountId.add(bean.id)


def basics_one(seat, product, bean, special_price, discount_sum,isvipdis):
    # 因翻倍限制所不能参加的活动 - --活动ID
    if seat.notProId:
        for id in seat.notProId:
            if id == bean.id:
                return

    if seat.is_run_other_pro == False:
        return  # 不可以进行商品活动

    if seat.seat:
        return  # 商品已占位
    # 如果商品不能参与促销计算，直接返回
    if seat.is_discount == "n":
        return
    # 标记剩余未参加商品数量
    product.qttyCount -= 1

    # 将以什么优惠基础的取出
    discount_value = bean.target_item

    # 优惠金额
    dc = 0

    # 公式计算
    value = CalculationPrice(seat.amt_receivable / discount_sum * special_price)

    # 活动是否允许折上折
    if isvipdis:
        seat.is_run_vip_discount=True

    dc = seat.amt_receivable - value
    seat.amt_receivable = value

    # # 更改以什么金额计算的，这个是之前写的，理解错误，
    # if bean.target_item.lower() == 'amt_list':
    #     dc = seat.amt_list - value
    #     seat.amt_list = value
    # elif bean.target_item.lower() == "amt_receivable":
    #     dc = seat.amt_receivable - value
    #     seat.amt_receivable = value
    # else:
    #     dc = bean.amt_retail - value
    #     seat.amt_retail = value

    # 更改应收价格
    seat.amt_receivable = value
    # 是否与其他商品活动同时执行
    seat.is_run_other_pro = bean.is_run_other_pro
    # 是否与全场活动同时执行
    seat.is_run_store_act = bean.is_run_store_act
    # 当前三类中占位
    seat.seat = True

    # 加入参加过的活动ID
    seat.discountId.append(bean.id)
    # 这次活动优惠的金额
    # seat.discountPrice.append(dc)
    # 商品记录活动id
    product.discountId.add(bean.id)
    return value


def condition_moeny_sum(productListA, condition):
    """
    :param productListA: 参与活动商品
    :param condition: 条件
    :return: 总价格
    """

    result = 0
    for product in productListA:
        for seat in product.productSeatList:
            if seat.seat == False and seat.is_run_other_pro != False:
                result += getattr(seat, condition)
    return result


def calculation_amt_receivable(productListA):
    """
    计算应收总价格
    :param productListA: 商品价钱
    :return: 所有商品的应收价的总值
    """
    result = 0
    sum_qtty = 0
    for product in productListA:
        for seat in product.productSeatList:
            if seat.seat == False and seat.is_run_other_pro != False:
                result += seat.amt_receivable
                if seat.is_discount == "y":
                    sum_qtty += seat.qtty
    return result, sum_qtty


def calculate_offer_price(productListA, bean, has_special_product, judge, special_price, discount_sum, for_value, isvipdis):
    if has_special_product:
        # 首先计算特例品的总价格
        special_product_amt = calculation_amt_special_product(productListA)
        new_formula_value = special_price - special_product_amt
        if new_formula_value < 0:
            new_formula_value = 0
        return calculation_special_price(productListA, bean, judge, new_formula_value,
                                         discount_sum - special_product_amt, for_value, isvipdis)
    else:
        return calculation_special_price(productListA, bean, judge, special_price, discount_sum, for_value, isvipdis)

def calculation_amt_special_product(productListA):
    sum = 0
    for product in productListA:
        for seat in product.productSeatList:
            if seat.seat == False and seat.is_run_other_pro != False and seat.is_discount == "n":
                sum += seat.amt_receivable
    return sum


def calculation_special_again(productListA, special_price, value_num):
    """
    用大于等于特价值/数量值的商品(非特例品) 计算公式值。 返回新的特价价格
    :param productListA:
    :param special_price:
    :param value_num:
    :return:
    """
    ge_specialvalue_qtty_sum = 0
    ge_specialvalue_amt_sum = 0
    small_specialvalue_amt_sum = 0
    for product in productListA:
        for seat in product.productSeatList:
            if seat.seat == False and seat.is_run_other_pro != False:
                if seat.is_discount == "y":
                    if seat.amt_receivable >= special_price / value_num:
                        ge_specialvalue_amt_sum += seat.amt_receivable
                        ge_specialvalue_qtty_sum += seat.qtty
                    else:
                        small_specialvalue_amt_sum += seat.amt_receivable
                else:
                    small_specialvalue_amt_sum += seat.amt_receivable
    if ge_specialvalue_qtty_sum > 0:
        return special_price / value_num * ge_specialvalue_qtty_sum + small_specialvalue_amt_sum
    else:
        return special_price

def condition_qtty_combination(productListA, candouble, bean, double_numb, max_double_times, specific_product_list, userInfo):
    '''
    组合特价计算方法
    add by hexiaoxia 2019/04/15
    :param productListA:参与计算的商品
    :param candouble:是否可翻倍
    :param bean:当前促销对象
    :param double_numb:最多参与计算的商品数量
    :param max_double_times: 最大翻倍次数
    :param specific_product_list: 参与商品款号列表
    :return:
    '''
    for row in productListA:
        if bean.target_item.lower() == 'amt_list':
            row.amt_receivable=row.amt_list
        elif bean.target_item.lower() == 'amt_retail':
            row.amt_receivable = row.amt_retail
        for r_seat in row.productSeatList:
            if bean.target_item.lower() == 'amt_list':
                r_seat.amt_receivable = r_seat.amt_list
            elif bean.target_item.lower() == 'amt_retail':
                r_seat.amt_receivable = r_seat.amt_retail

    productListA = sorted(productListA, key=lambda x: x.productSeatList[0].amt_receivable, reverse=True)  # 按照应收价格降序

    isvipdis = True

    if bean.is_run_vip_discount:
        if userInfo.discount != None:
            num = 0
            for r_row in productListA:
                for r1 in r_row.productSeatList:
                    if r1.is_run_vip_discount:
                        isvipdis = False
                        break
    else:
        isvipdis = False

    promotion_qtty_sum, _, _, _, org_promotion_qtty_sum, _, _, _ = tongji(productListA)

    if candouble:
        # # 第一步计算翻倍
        # if bean.max_times == 0 or bean.max_times == 1:
        #     bean.max_times = 1
        #     max_pro_numb = double_numb
        #     p = 1
        # elif bean.max_times > 1:
        #     # 先看看目前商品最多能翻多少倍
        #     p = promotion_qtty_sum // double_numb
        #     # 如果当前倍数 >= 最大翻倍数 取最大翻倍数
        #     if p >= bean.max_times:
        #         max_pro_numb = double_numb * bean.max_times
        #         p = bean.max_times
        #     else:
        #         # 否则的话取当前最大倍数
        #         max_pro_numb = p * double_numb
        # else:
        #     # 到这是无限翻倍了
        #     p = promotion_qtty_sum // double_numb
        #     max_pro_numb = double_numb * p

        seat_product_list = []
        formula_value = 0  # 总价格
        can_part_amt_sum = 0  # 能参加活动的商品价格
        can_part_qtty_sum = 0  # 能参加活动的商品数量
        has_special_product_flug = False
        special_product_amt = 0
        for r_item in specific_product_list:
            r_item["value_num"] = max_double_times * int(r_item["value_num"])

        max_search_times = max_double_times * double_numb
        # 首先查找非特例品（可以参与促销计算的）
        for product in productListA:
            if max_double_times < 1:
                break
            for seat in product.productSeatList:
                if max_double_times < 1:
                    break
                if seat.seat == False and seat.is_run_other_pro and seat.is_discount == "y":
                    for spec_pro_item in specific_product_list:
                        if spec_pro_item["value_num"] > 0:
                            if product.ecode in spec_pro_item["pro_ecode_list"]:
                                seat_product_list.append({"seat": seat, "product": product})
                                spec_pro_item["value_num"] -= 1
                                max_search_times -= 1
                                can_part_qtty_sum += 1
                                can_part_amt_sum += seat.amt_receivable
                                formula_value += seat.amt_receivable
                                break

        #
        if max_double_times > 0:
            for product in productListA:
                if max_double_times < 1:
                    break
                for seat in product.productSeatList:
                    if max_double_times < 1:
                        break
                    if seat.seat == False and seat.is_run_other_pro and seat.is_discount == "n":
                        for spec_pro_item in specific_product_list:
                            if spec_pro_item["value_num"] > 0:
                                if product.ecode in spec_pro_item["pro_ecode_list"]:
                                    # seat_product_list.append({"seat": seat, "product": product})
                                    spec_pro_item["value_num"] -= 1
                                    max_search_times -= 1
                                    formula_value += seat.amt_receivable
                                    special_product_amt += seat.amt_receivable
                                    has_special_product_flug = True
                                    break
        # 计算当前倍数的总价格
        # formula_value, can_part_amt_sum, can_part_qtty_sum = result_max_pro(productListA, max_pro_numb)
        if formula_value == 0:
            return -1
        if can_part_qtty_sum == 0:
            return -1
        # 计算倍数之后的优惠价格
        # if isvipdis:
        #     special_price = CalculationPrice(bean.special_price * max_double_times * userInfo.discount)
        # else:
        special_price = bean.special_price * max_double_times

        # 看原价与特价值那个更便宜 取更小的
        if formula_value > special_price:
            if has_special_product_flug:
                # 如果有特例品的话， 特价值需要减去特例品的金额
                if isvipdis:
                    special_price = CalculationPrice(bean.special_price * max_double_times * userInfo.discount)
                special_price = CalculationPrice(special_price - special_product_amt)
                if special_price < 0:
                    special_price = 0
            return condition_calculation_for_double(seat_product_list, bean, special_price, can_part_amt_sum,
                                                    True, isvipdis)
            # return calculation_special_price(productListA, bean, candouble, special_price, can_part_amt_sum,
            #                                  can_part_qtty_sum, isvipdis)
        else:
            if isvipdis:
                special_price=CalculationPrice(formula_value*userInfo.discount)
                if has_special_product_flug:
                    # 如果有特例品的话， 特价值需要减去特例品的金额
                    special_price = CalculationPrice(special_price - special_product_amt)
                    if special_price < 0:
                        special_price = 0
                return condition_calculation_for_double(seat_product_list, bean, special_price, can_part_amt_sum,
                                                        True, isvipdis)
            else:
                return condition_calculation_for_double(seat_product_list, bean, special_price, can_part_amt_sum,
                                                        False, isvipdis)
    else:
        # 计算所有商品的总应收价
        amt_receivable_sum, can_part_qtty_sum = calculation_amt_receivable(productListA)
        if can_part_qtty_sum == 0:
            return -1
        # 特价 / 条件 * 当前总数量 取整 计算当前特价值
        # if isvipdis:
        #     formula_value = CalculationPrice((bean.special_price / double_numb * promotion_qtty_sum)*userInfo.discount)
        # else:
        formula_value = CalculationPrice(bean.special_price / double_numb * promotion_qtty_sum)

        # 先看公式值是否大于
        if formula_value > amt_receivable_sum:
            # 看原价与特价值那个更便宜 取更小的
            if amt_receivable_sum > bean.special_price:
                # 当特价值比较小的时候，在根据商品价格算一遍。
                special_price = calculation_special_again(productListA, bean.special_price, double_numb)
                if isvipdis:
                    special_price = CalculationPrice(special_price * userInfo.discount)
                has_special_product_flug = True
                if promotion_qtty_sum == can_part_qtty_sum:
                    has_special_product_flug = False
                return calculate_offer_price(productListA, bean, has_special_product_flug, candouble, special_price,
                                             amt_receivable_sum, 0, isvipdis)
            else:
                if isvipdis:
                    special_price = CalculationPrice(amt_receivable_sum * userInfo.discount)
                    # 需要看有无特例品
                    has_special_product_flug = True
                    if promotion_qtty_sum == can_part_qtty_sum:
                        has_special_product_flug = False
                    return calculate_offer_price(productListA, bean, has_special_product_flug, candouble,
                                                 special_price, amt_receivable_sum, 0, isvipdis)
                else:
                    return amt_receivable_pro(productListA, bean, candouble, 0)
        elif formula_value < amt_receivable_sum:
            if isvipdis:
                formula_value = CalculationPrice((bean.special_price / double_numb *
                                                  promotion_qtty_sum) * userInfo.discount)
            has_special_product_flug = True
            if promotion_qtty_sum == can_part_qtty_sum:
                has_special_product_flug = False
            return calculate_offer_price(productListA, bean, has_special_product_flug, candouble, formula_value,
                                         amt_receivable_sum, 0, isvipdis)
        else:
            if isvipdis:
                special_price = CalculationPrice(amt_receivable_sum * userInfo.discount)
                # 需要看有无特例品
                has_special_product_flug = True
                if promotion_qtty_sum == can_part_qtty_sum:
                    has_special_product_flug = False
                return calculate_offer_price(productListA, bean, has_special_product_flug, candouble,
                                             special_price, amt_receivable_sum, 0, isvipdis)
            else:
                return amt_receivable_pro(productListA, bean, candouble, 0)