#!/usr/bin/env python
"""
    满减活动详细运算
   encoding: utf-8
   2018/12/18 4:42 PM
   
  
   by李博文
"""
from pro.apis.GA_utils import calculation_amt_receivable,calculation_amt_receivable_qtty
from pro.utils.util import CalculationPrice
from pro.utils.util import minus
import math
from pro.utils.linq import linq
from pro.apis.GA_api.DC_api.basics import splitDiffPrice
import pro.utils.util as util

def choice(bean, userInfo, productListA, promotion_qtty_sum, promotion_amt_list_sum,
           promotion_amt_retail_sum, promotion_amt_receivable_sum):
    """
    :param bean: 满减买赠的具体对象
    :param productListA:  所有可以参加活动的列表
    :param promotion_qtty_sum:  数量总数
    :param promotion_amt_list_sum:  amt_list:吊牌金额
    :param promotion_amt_retail_sum: amt_retail:零售金额
    :param promotion_amt_receivable_sum: amt_receivable:应收金额
    :return:
    """

    # 判断活动以什么满足qtty：数量  amt_list：吊牌金额  amt_retail：零售金额  amt_receivable：应收金额
    if bean.target_type == "qtty":
        return operation_qtty(bean, userInfo, productListA, promotion_qtty_sum)


    elif bean.target_type == "amt_list":
        condition = "amt_list"
        return operation_moeny(bean, userInfo, productListA, promotion_amt_list_sum, condition)


    elif bean.target_type == "amt_retail":
        condition = "amt_retail"
        return operation_moeny(bean, userInfo, productListA, promotion_amt_retail_sum, condition)

    elif bean.target_type == "amt_receivable":
        condition = "amt_receivable"
        return operation_moeny(bean, userInfo, productListA, promotion_amt_receivable_sum, condition)


def unify_gradient_cal(bean, userInfo, productListA, promotion_qtty_sum, promotion_amt_list_sum,
                       promotion_amt_retail_sum, promotion_amt_receivable_sum, org_promotion_qtty_sum,
                       org_promotion_amt_list_sum, org_promotion_amt_retail_sum,
                       org_promotion_amt_receivable_sum):
    """
    统一和梯度满减计算  20190802 By WeiYanPing
    :param bean: 满减买赠的具体对象
    :param productListA:  所有可以参加活动的列表
    :param promotion_qtty_sum:  数量总数
    :param promotion_amt_list_sum:  amt_list:吊牌金额
    :param promotion_amt_retail_sum: amt_retail:零售金额
    :param promotion_amt_receivable_sum: amt_receivable:应收金额
    :return:
    """

    # 判断活动以什么满足qtty：数量  amt_list：吊牌金额  amt_retail：零售金额  amt_receivable：应收金额
    value_num = bean.value_num
    if bean.comp_symb_type == "g":
        value_num += 1

    max_double_times = 0
    ori_product_compare_condition = 0
    if bean.target_type == "qtty":
        max_double_times = promotion_qtty_sum // value_num
        ori_product_compare_condition = org_promotion_qtty_sum
    elif bean.target_type == "amt_list":
        max_double_times = promotion_amt_list_sum // value_num
        ori_product_compare_condition = org_promotion_amt_list_sum
    elif bean.target_type == "amt_retail":
        max_double_times = promotion_amt_retail_sum // value_num
        ori_product_compare_condition = org_promotion_amt_retail_sum
    elif bean.target_type == "amt_receivable":
        max_double_times = promotion_amt_receivable_sum // value_num
        ori_product_compare_condition = org_promotion_amt_receivable_sum

    if max_double_times < 1:
        # 说明不能执行促销， 看原始商品能否执行
        if ori_product_compare_condition >= value_num:
            return 1
        return None
    else:
        if bean.max_times == 0 or bean.max_times == 1 or bean.max_times is None:
            max_double_times = 1
        elif bean.max_times > 1 and max_double_times > bean.max_times:
            max_double_times = bean.max_times

    # 参与商品
    seat_list = []  # 参与计算的商品
    seat_product_list = []  # 参与计算的明细与商品
    condition_seat_list = []  # 只能作为条件的商品明细（）
    condition_seat_product_list = []  # 只能作为条件的商品明细和对应商品
    current_sum = 0
    max_value_num_sum = max_double_times * value_num
    for i in range(2):
        # i 为0， 表示选择非特例品，i为1表示选择特例品
        if current_sum >= max_value_num_sum:
            break
        for product in productListA:
            if current_sum >= max_value_num_sum:
                break
            # 当前商品不在该行的判断条件中
            if product.ecode not in bean.product_list:
                continue
            if i == 0 and product.productSeatList and product.productSeatList[0].is_discount == "n":
                continue
            if i == 1 and product.productSeatList and product.productSeatList[0].is_discount == "y":
                continue
            if product.notOccupiedThree() <= 0:
                # 如果没有未占位的商品，进入下一个商品
                continue
            for seat in product.productSeatList:
                if current_sum >= max_value_num_sum:
                    break
                if (not seat.seat) and seat.is_run_other_pro:
                    if str(bean.target_type).lower() == "qtty":
                        current_sum += 1
                    elif str(bean.target_type).lower() == "amt_list":
                        current_sum += seat.amt_list
                    elif str(bean.target_type).lower() == "amt_retail":
                        current_sum += seat.amt_retail
                    elif str(bean.target_type).lower() == "amt_receivable":
                        current_sum += seat.amt_receivable
                    if seat.is_discount == "y":
                        if seat not in seat_list:
                            seat_list.append(seat)
                            seat_product_list.append({"seat": seat, "product": product})
                    else:
                        if seat not in condition_seat_list:
                            condition_seat_list.append(seat)
                            condition_seat_product_list.append({"seat": seat, "product": product})

    if not seat_list:
        # 说明没有可以参与促销计算的商品
        return 1

    # 首先将条件商品占位
    for item in condition_seat_product_list:
        seat = item.get("seat")
        product = item.get("product")
        # 标记剩余未参加商品数量
        product.qttyCount -= 1
        # 是否与其他商品活动同时执行
        seat.is_run_other_pro = bean.is_run_other_pro
        # 是否与全场活动同时执行
        seat.is_run_store_act = bean.is_run_store_act
        # 当前三类中占位
        seat.seat = True
        if bean.id not in product.discountId:
            product.discountId.append(bean.id)

    # 计算可参与的商品的总的应收价
    receivable_sum = 0
    for seat in seat_list:
        receivable_sum += seat.amt_receivable
    # 满减值
    moenyback_sum = bean.moenyback * max_double_times

    # 公式计算：
    if receivable_sum > moenyback_sum:  # 如果应收价大于满减值
        # 实际占位计算
        return calculation_moenyback(bean, userInfo, seat_product_list, moenyback_sum, receivable_sum, True)
    else:
        # 实际占位计算
        return calculation_moenyback(bean, userInfo, seat_product_list, moenyback_sum, receivable_sum, False)


def operation_moeny(bean, userInfo, productListA, promotion_money_sum, condition):
    """"
    :param bean: 满减活动
    :param userInfo: 活动对象
    :param productListA: 可以参与活动的商品
    :param promotion_money_sum:  可以参与活动的总商品
    :param condition:
    :return:
    """
    p = False
    # 若比较符为大于 比较值加1
    if bean.comp_symb_type == "g":

        p = True
        bean.value_num += 1


    # 若不满足比较值直接返回
    if not promotion_money_sum >= bean.value_num:
        return
    productListA = sorted(productListA, key=lambda i: i.productSeatList[0].amt_receivable, reverse=True)
    for_max_value = 0  # 最大循环次数
    moenyback_sum = 0  # 最大翻倍满减值

    # 将满减值四舍五入
    bean.moenyback = CalculationPrice(bean.moenyback)
    # 计算翻倍值
    if bean.max_times == -1:
        # 如果翻倍值为无限翻
        # 用总数量 / 数量
        i = promotion_money_sum // bean.value_num
        for_max_value = bean.value_num * i
        # 计算满减翻倍之后的总价钱
        moenyback_sum = CalculationPrice(i * bean.moenyback)

    elif bean.max_times == 0 or bean.max_times == 1:
        # 如果为不翻倍
        for_max_value = bean.value_num
        moenyback_sum = bean.moenyback
    else:
        # 走到这肯定就不为无限翻倍,不为不翻倍
        # 先看目前最大倍数
        i = promotion_money_sum // bean.value_num
        if i >= bean.max_times:  # 当前倍数大于等于最大翻倍值取最大翻倍值
            for_max_value = bean.max_times * bean.value_num  # 最大循环次数
            moenyback_sum = CalculationPrice(bean.max_times * bean.moenyback)  # 最大翻倍之后的满减值
        else:
            # 此时就是不满足最大翻倍次数
            for_max_value = bean.value_num * i
            moenyback_sum = CalculationPrice(i * bean.moenyback)
    # 被迫加的
    if bean.comp_symb_type == "g":
        if p == True:
            value = bean.value_num - 1
            if value == 0:
                # 如果为不翻倍
                for_max_value = bean.value_num
                moenyback_sum = bean.moenyback
    # 如果能走到这正好循环值为0就加一 因为肯定满足了 但是不包括测试10 和10 之间的乱测
    if for_max_value == 0:
        for_max_value = 1
    if moenyback_sum == 0:
        moenyback_sum = bean.moenyback
    # 计算最大商品的总应收价
    receivable_sum = calculation_amt_receivable(productListA, for_max_value, condition)

    # 怎么进来你给我怎么出去 若总价钱小于满减值
    judge = False
    # 判断应收价大还是满减值大
    if receivable_sum > moenyback_sum:  # 如果应收价大于满减值
        return operation_moeny_for(bean, userInfo, productListA, moenyback_sum, for_max_value, receivable_sum,judge , condition)
    else:
        judge = True
        # 此时就是总金额小于满减值
        return operation_moeny_for(bean, userInfo, productListA, moenyback_sum, for_max_value, receivable_sum, judge , condition)
def operation_moeny_for(bean, userInfo, productListA, moenyback_sum, for_max_value, receivable_sum, judge , condition
                        ):
    """
    :param bean:  活动
    :param userInfo:  会员
    :param productListA:  可以参与活动的商品
    :param moenyback_sum: 满减值(可能是翻倍后的)
    :param for_max_value: 最大价钱参与活动
    :param receivable_sum: 总应收价
    :return:
    """
    # 参与活动列表
    seat_list = []
    result = 0
    result_off = 0
    result_recevable_sum = 0
    receivable_sum = 0
    if judge != False:
        for product in productListA:
            for seat in product.productSeatList:
                if result_off >= for_max_value:
                    break
                if seat.seat == False and seat.is_run_other_pro != False and seat.is_discount == "y":
                    result_off += getattr(seat, condition)
                    basics_one_p(seat,product,bean, userInfo)
        return "ok"
    for product in productListA:
        for seat in product.productSeatList:
            if result_off >= for_max_value:
                break
            if seat.seat == False and seat.is_run_other_pro != False and seat.is_discount == "y":
                receivable_sum += seat.amt_receivable
                result_off += getattr(seat, condition)

    result_off = 0
    for product in productListA:
        for seat in product.productSeatList:
            if result_off >= for_max_value:
                break
            if seat.seat == False and seat.is_run_other_pro != False and seat.is_discount == "y":
                result_off += getattr(seat, condition)
                result_recevable_sum += seat.amt_receivable
                result += basics_one(seat, product, bean, userInfo, moenyback_sum, receivable_sum)
                seat_list.append(seat)
    # 计算满减值之后的差价
    moenyback_money_sum = CalculationPrice(result_recevable_sum - moenyback_sum)

    # 有误差，误差分摊按照参数的进位方式处理
    pingtan_value = CalculationPrice(minus(moenyback_money_sum, result))

    # 误差分摊
    if pingtan_value != 0:
        splitDiffPrice(seat_list, bean, diffPrice=pingtan_value)

    # 计算优惠金额
    for seat1 in seat_list:
        pric = float("%.2f" % float(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
        seat1.upamt_receivable = seat1.amt_receivable
        seat1.discountPrice.append(pric)

    return "ok"


def operation_qtty(bean, userInfo, productListA, promotion_qtty_sum):
    """

    :param bean: 活动
    :param userInfo: 会员对象
    :param productListA: 可以参加活动的列表
    :param promotion_qtty_sum: 数量总数
    :return:
    """
    # 临时变量控制翻倍用的
    p = False
    # 若比较符为大于 比较值加1
    if bean.comp_symb_type == "g":

        bean.value_num += 1
        p = True

    # 若不满足比较值直接返回
    if not promotion_qtty_sum >= bean.value_num:
        return
    productListA = sorted(productListA, key=lambda i: i.productSeatList[0].amt_receivable, reverse=True)
    for_max_value = 0  # 最大循环次数
    moenyback_sum = 0  # 最大翻倍满减值

    # get_re = int(get_retail_carryway())
    # # 如果进位参数不为 四舍五入取整或者 2 那么return
    # if not get_re != None or get_re != 2:
    #     return

    # 四舍五入计算
    bean.moenyback = CalculationPrice(bean.moenyback)
    # 将满减值四舍五入
    # 计算翻倍值
    if bean.max_times == -1:
        # 如果翻倍值为无限翻
        # 用总数量 / 数量
        i = promotion_qtty_sum // bean.value_num
        for_max_value = bean.value_num * i
        # 计算满减翻倍之后的总价钱
        moenyback_sum = CalculationPrice(i * bean.moenyback)

    elif bean.max_times == 0 or bean.max_times == 1:
        # 如果为不翻倍
        for_max_value = bean.value_num
        moenyback_sum = CalculationPrice(bean.moenyback)
    else:
        # 走到这肯定就不为无限翻倍,不为不翻倍
        # 先看目前最大倍数
        i = promotion_qtty_sum // bean.value_num
        if i >= bean.max_times:  # 当前倍数大于等于最大翻倍值取最大翻倍值
            for_max_value = bean.max_times * bean.value_num  # 最大循环次数
            moenyback_sum = CalculationPrice(bean.max_times * bean.moenyback)  # 最大翻倍之后的满减值
        else:
            # 此时就是不满足最大翻倍次数
            for_max_value = bean.value_num * i
            moenyback_sum = CalculationPrice(i * bean.moenyback)
    # 被迫加的
    if bean.comp_symb_type == "g":
        if p == True:
            value = bean.value_num - 1
            if value == 0:
                # 如果为不翻倍
                for_max_value = bean.value_num
                moenyback_sum = bean.moenyback
    # 计算最大商品的总应收价
    receivable_sum = calculation_amt_receivable_qtty(productListA, for_max_value)


    # 控制是否可以参与满减的属性
    judge = False
    # 判断应收价大还是满减值大
    if receivable_sum > moenyback_sum:  # 如果应收价大于满减值
        return operation_qtty_for(bean, userInfo, productListA, moenyback_sum, for_max_value, receivable_sum,judge)
    else:
        judge = True
        # 此时就是总金额小于满减值
        return operation_qtty_for(bean, userInfo, productListA, moenyback_sum, for_max_value, receivable_sum, judge)


def basics_one_p(seat, product, bean, userInfo):
    """
    # 此函数只更改站位信息不记录任何优惠
    :param bean:
    :param userInfo:
    :param productListA:
    :return:
    """

    if seat.notProId:
        for id in seat.notProId:
            if id == bean.id:
                return

    if seat.is_run_other_pro == False:
        return  # 不可以进行商品活动

    if seat.seat:
        return  # 商品已占位

    # 如果该商品不参与促销计算
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

    seat.upamt_receivable = seat.amt_receivable
    # 这次活动优惠的金额
    seat.discountPrice.append(seat.amt_receivable)
    # 更改应收价
    seat.amt_receivable = 0
    # 加入参加过的活动ID
    seat.discountId.append(bean.id)

    # 商品记录活动id
    product.discountId.add(bean.id)


def operation_qtty_for(bean, userInfo, productListA, moenyback_sum, for_max_value, receivable_sum,judge):

    """
    :param bean: 活动
    :param userInfo: 会员
    :param productListA: 可以参与活动的商品
    :param moenyback_sum: 翻倍或不翻倍的满减值
    :param for_max_value: 最大循环次数
    :param receivable_sum: 应收价总值
    :param judge: 如果为F说明需要公式计算
    :return:
    """
    if not judge:
        result = 0
        # 先统计可以参与活动所有的应收价
        seat_list = []
        for product in productListA:
            for seat in product.productSeatList:
                if for_max_value == 0:
                    break
                if seat.seat == False and seat.is_run_other_pro != False and seat.is_discount == "y":
                    result += basics_one(seat, product, bean, userInfo, moenyback_sum, receivable_sum)
                    for_max_value -= 1
                    seat_list.append(seat)
        # 计算新的应收价总额
        moenyback_money_sum = CalculationPrice(receivable_sum - moenyback_sum)

        # 有误差，误差分摊按照参数的进位方式处理
        pingtan_value = CalculationPrice(minus(moenyback_money_sum, result))
        # 误差分摊
        if pingtan_value != 0:
            splitDiffPrice(seat_list, bean, diffPrice=pingtan_value)

        # 计算优惠金额
        for seat1 in seat_list:
            pric = float("%.2f" % float(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
            seat1.upamt_receivable = seat1.amt_receivable
            seat1.discountPrice.append(pric)

    for product in productListA:
        for seat in product.productSeatList:
            if for_max_value == 0:
                break
            if seat.seat == False and seat.is_run_other_pro != False and seat.is_discount == "y":
                basics_one_p(seat, product, bean, userInfo)
                for_max_value -= 1

    return "ok"


def basics_one(seat, product, bean, userInfo, moenyback_sum, receivable_sum):
    """

    :param seat: 商品明细
    :param product: 商品
    :param bean: 活动
    :param userInfo: 会员
    :param moenyback_sum: 满减总值
    :param receivable_sum: 商品总价
    :return:
    """
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

    # 计算平摊值
    # 应收价减去 应收价除以商品所有应收价乘以满减总值
    value = CalculationPrice(seat.amt_receivable - ((seat.amt_receivable / receivable_sum) * moenyback_sum))

    # 记录优惠金额
    dc = seat.amt_receivable - value
    # 更改应收价
    seat.amt_receivable = value
    # 加入参加过的活动ID
    seat.discountId.append(bean.id)
    # 这次活动优惠的金额
    # seat.discountPrice.append(dc)
    # 商品记录活动id
    product.discountId.add(bean.id)
    return value


def operation_combination(bean, userInfo, productList, max_double_time):
    """
    组合满减计算-原来写的， 现不使用
    :param bean:
    :param userInfo:
    :param productList:
    :param max_double_time:
    :return:
    """
    # 商品应收价降序排序
    productList = sorted(productList, key=lambda i: i.productSeatList[0].amt_receivable, reverse=True)

    # partProductList = []
    part_product_ecode = []  # 参与商品款号列表
    part_product_ecode_sum = {}  # 每个款号，参与计算的数量
    # current_part_product_ecode_sum = {}
    for spec_item in bean.specific_activities:
        current_part_product_ecode_sum = {}  # 当前行参与计算的每个款的数量
        # 比较值
        value_num = spec_item.value_num
        if spec_item.comp_symb_type == "g":
            value_num = value_num + 1

        current_sum = 0  # 当前参与计算的总数（可以是数量，金额）
        max_value_num_sum = max_double_time * value_num  # 当前行最大的计算值，达到这个值后，后面的商品就不再计算了
        for product in productList:
            if current_sum >= max_value_num_sum:
                break
            # 当前商品不在该行的判断条件中
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

        if current_part_product_ecode_sum:
            # 将参与活动的所有商品所需数量与当前行中个款号所需数量进行对比，没有则加上，小于也加上
            for key, value in current_part_product_ecode_sum.items():
                if part_product_ecode_sum.get(key, 0) < value:
                    part_product_ecode_sum[key] = value

    # for i in max_double_time:
    #     pass
    # 计算可参与的商品的总的应收价
    receivable_sum = 0
    for key, value in part_product_ecode_sum.items():
        sum_qtty = 0
        for product in productList:
            if sum_qtty >= value:
                break
            if key == product.ecode.lower():
                for seat in product.productSeatList:
                    if sum_qtty >= value:
                        break
                    if seat.seat == False and seat.is_run_other_pro != False and seat.is_discount == "y":
                        receivable_sum = receivable_sum + seat.amt_receivable
                        sum_qtty += 1
                # if product.notOccupiedThree() <= value - sum_qtty:
                #     receivable_sum = receivable_sum + (product.notOccupiedThree() * product.amt_receivable)
                #     sum_qtty += product.notOccupiedThree()
                # else:
                #     receivable_sum = receivable_sum + ((value - sum_qtty) * product.amt_receivable)
                #     sum_qtty = value

    # 满减值
    moenyback_sum = bean.moenyback * max_double_time

    # 公式计算：
    if receivable_sum > moenyback_sum:  # 如果应收价大于满减值
        # 实际占位计算
        return calculation_combination_moenyback(bean, userInfo, productList, moenyback_sum,part_product_ecode_sum, receivable_sum,True)
        # return operation_qtty_for(bean, userInfo, productListA, moenyback_sum, for_max_value, receivable_sum,judge)
    else:
        # 实际占位计算
        return calculation_combination_moenyback(bean, userInfo, productList, moenyback_sum, part_product_ecode_sum,
                                          receivable_sum, False)


def operation_combination_moenyback(bean, userInfo, productList, max_double_time):
    """
    组合满减计算-选择参与商品：2019-08-01 By WeiYanPing
    :param bean:
    :param userInfo:
    :param productList:
    :param max_double_time:
    :return:
    """
    # 商品应收价降序排序
    productList = sorted(productList, key=lambda i: i.productSeatList[0].amt_receivable, reverse=True)

    seat_list = []  # 参与计算的商品
    seat_product_list = []  # 参与计算的明细与商品
    condition_seat_list = []  # 只能作为条件的商品明细（）
    condition_seat_product_list = []  # 只能作为条件的商品明细和对应商品
    for spec_item in bean.specific_activities:
        # 比较值
        value_num = spec_item.value_num
        if spec_item.comp_symb_type == "g":
            value_num = value_num + 1

        current_sum = 0  # 当前参与计算的总数（可以是数量，金额）
        # 当前行最大的计算值，达到这个值后，后面的商品就不再计算了
        max_value_num_sum = max_double_time * value_num
        for i in range(2):
            # i 为0， 表示选择非特例品，i为1表示选择特例品
            if current_sum >= max_value_num_sum:
                break
            for product in productList:
                if current_sum >= max_value_num_sum:
                    break
                # 当前商品不在该行的判断条件中
                if product.ecode not in spec_item.product_list:
                    continue
                if i == 0 and product.productSeatList and product.productSeatList[0].is_discount == "n":
                    continue
                if i == 1 and product.productSeatList and product.productSeatList[0].is_discount == "y":
                    continue
                if product.notOccupiedThree() <= 0:
                    # 如果没有未占位的商品，进入下一个商品
                    continue
                for seat in product.productSeatList:
                    if current_sum >= max_value_num_sum:
                        break
                    if (not seat.seat) and seat.is_run_other_pro:
                        if str(spec_item.target_type).lower() == "qtty":
                            current_sum += 1
                        elif str(spec_item.target_type).lower() == "amt_list":
                            current_sum += seat.amt_list
                        elif str(spec_item.target_type).lower() == "amt_retail":
                            current_sum += seat.amt_retail
                        elif str(spec_item.target_type).lower() == "amt_receivable":
                            current_sum += seat.amt_receivable
                        if seat.is_discount == "y":
                            if seat not in seat_list:
                                seat_list.append(seat)
                                seat_product_list.append({"seat": seat, "product": product})
                        else:
                            if seat not in condition_seat_list:
                                condition_seat_list.append(seat)
                                condition_seat_product_list.append({"seat": seat, "product": product})

    if not seat_list:
        # 说明没有可以进行促销计算的商品明细
        return 1

    # 首先将条件商品占位
    for item in condition_seat_product_list:
        seat = item.get("seat")
        product = item.get("product")
        # 标记剩余未参加商品数量
        product.qttyCount -= 1
        # 是否与其他商品活动同时执行
        seat.is_run_other_pro = bean.is_run_other_pro
        # 是否与全场活动同时执行
        seat.is_run_store_act = bean.is_run_store_act
        # 当前三类中占位
        seat.seat = True
        if bean.id not in product.discountId:
            product.discountId.append(bean.id)

    # 计算可参与的商品的总的应收价
    receivable_sum = 0
    for seat in seat_list:
        receivable_sum += seat.amt_receivable
    # 满减值
    moenyback_sum = bean.moenyback * max_double_time

    # 公式计算：
    if receivable_sum > moenyback_sum:  # 如果应收价大于满减值
        # 实际占位计算
        return calculation_moenyback(bean, userInfo, seat_product_list, moenyback_sum, receivable_sum, True)
    else:
        # 实际占位计算
        return calculation_moenyback(bean, userInfo, seat_product_list, moenyback_sum, receivable_sum, False)


def calculation_combination_moenyback(bean, userInfo, productListA, moenyback_sum, part_prosuct_num, receivable_sum,judge):
    """
    组合满减占位计算
    :param bean: 活动
    :param userInfo: 会员信息
    :param productListA: 参与活动商品
    :param moenyback_sum: 优惠总额
    :param part_prosuct_num: 参与商品每个款号所需数量
    :param receivable_sum: 参与商品总应收价
    :param judge: True则计算，False则直接将应收价改为0并占位
    :return:
    """
    if judge:
        result = 0
        seat_list = []
        for key, value in part_prosuct_num.items():
            for product in productListA:
                if value == 0:
                    break
                if key == product.ecode.lower():
                    for seat in product.productSeatList:
                        if value == 0:
                            break
                        if seat.seat == False and seat.is_run_other_pro != False and seat.is_discount == "y":
                            result += basics_one(seat, product, bean, userInfo, moenyback_sum, receivable_sum)
                            seat_list.append(seat)
                            value -= 1

        # 计算满减之后的总的应收价
        moenyback_money_sum = CalculationPrice(receivable_sum - moenyback_sum)
        # if result == moenyback_money_sum:
        #     return "ok"

        # 有误差，误差分摊按照参数的进位方式处理
        pingtan_value = CalculationPrice(minus(moenyback_money_sum, result))
        # 误差分摊
        # flattenDiffPirce(pingtan_value, productListA, bean.id)
        if pingtan_value != 0:
            splitDiffPrice(seat_list, bean, diffPrice=pingtan_value)

        # 计算优惠金额
        for seat1 in seat_list:
            pric = float("%.2f" % float(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
            seat1.upamt_receivable = seat1.amt_receivable
            seat1.discountPrice.append(pric)
        return "ok"
    else:
        for key, value in part_prosuct_num.items():
            for product in productListA:
                for seat in product.productSeatList:
                    if value == 0:
                        break
                    if seat.seat == False and seat.is_run_other_pro != False:
                        basics_one_p(seat, product, bean, userInfo)
                        value -= 1
        return "ok"


def calculation_moenyback(bean, userInfo, seatProductList, moenyback_sum, receivable_sum, judge):
    """
    满减占位计算-20190802 By WeiYanPing
    :param bean: 活动
    :param userInfo: 会员信息
    :param seatProductList: 参与计算商品
    :param moenyback_sum: 优惠总额
    :param receivable_sum: 参与商品总应收价
    :param judge: True则计算，False则直接将应收价改为0并占位
    :return:
    """
    if judge:
        result = 0
        seat_list = []
        for item in seatProductList:
            result += basics_one(item.get("seat"), item.get("product"), bean, userInfo, moenyback_sum, receivable_sum)
            seat_list.append(item.get("seat"))

        # 计算满减之后的总的应收价
        moenyback_money_sum = CalculationPrice(receivable_sum - moenyback_sum)

        # 有误差，误差分摊按照参数的进位方式处理
        pingtan_value = CalculationPrice(minus(moenyback_money_sum, result))
        # 误差分摊
        if pingtan_value != 0:
            splitDiffPrice(seat_list, bean, diffPrice=pingtan_value)

        # 计算优惠金额
        for seat1 in seat_list:
            pric = float("%.2f" % float(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
            seat1.upamt_receivable = seat1.amt_receivable
            seat1.discountPrice.append(pric)
        return "ok"
    else:
        for item in seatProductList:
            basics_one_p(item.get("seat"), item.get("product"), bean, userInfo)
        return "ok"