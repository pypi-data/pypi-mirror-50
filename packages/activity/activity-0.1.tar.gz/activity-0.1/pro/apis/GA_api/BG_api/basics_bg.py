# -*- coding:utf-8 -*-
"""
    基础运算买赠
    2018/10/24
    by李博文
    edit by hexiaoxia 2019/05/14
    修改项：
    1.重新整理原来统一买赠、梯度买赠具体执行方法；
    2.添加组合买赠具体执行方法
"""
import copy
from pro.utils.util import CalculationPrice
from pro.utils.pro_exception import ProException
from pro.utils.util import get_product_sum, get_money_sum, result_number
from pro.utils.util import  sort_pro, sort_ab_a_number
from pro.apis.entitys.products_entitys.product import Product


# 更改每一件可以赠送的商品
def one_buy_product(seat, product, bean):
    if not seat.is_run_other_pro:
        return  # 不可以进行商品活动
    # 如果该商品不参与促销计算，直接返回
    if seat.is_discount == "n":
        return
    # 标记剩余未参加商品数量

    seat.is_buy_gifts = "y"
    seat.discountId.append(bean.id)
    seat.seat = True

    # 判断当前商品是否可以跟其他活动同时进行进行
    seat.is_run_other_pro = False
    # 判断是否可以进行全场活动
    seat.is_run_store_act = False


# 更改商品明细
def basics_one(seat, product, bean, userInfo, ):
    """

    :param seat: 商品明细
    :param product: 商品对象
    :param bean: 活动对象
    :param userInfo: 会员对象
    :return:

    """

    if not seat.is_run_other_pro:
        return  # 不可以进行商品活动

    if seat.seat:
        return  # 商品已占位

    # 标记剩余未参加商品数量

    product.qttyCount -= 1

    # 更改商品站位信息
    seat.seat = True
    # 判断当前商品是否可以跟其他活动同时进行进行
    seat.is_run_other_pro = bean.is_run_other_pro
    # 判断是否可以进行全场活动
    seat.is_run_store_act = bean.is_run_store_act
    # 记录当前活动id
    product.discountId.add(bean.id)

    # 判断以什么价格进行优惠 吊牌价 或 零售 或 应收
    # 以应收金额为基础
    if bean.target_item == "amt_receivable":
        # 判断是否可以参加vip折中折
        if bean.is_run_vip_discount:
            # 当前商品没有参加过vip折中折
            if not seat.is_run_vip_discount:
                if userInfo.discount:
                    # 设置当前商品已经参加过vip折中折
                    seat.is_run_vip_discount = True

                    vipPric = float(seat.amt_receivable * userInfo.discount)
                    vipPric = round(vipPric, 2)

                    # 计算vip 折中折优惠金额
                    vipMoney = seat.amt_receivable - vipPric
                    vipMoney = round(vipMoney, 2)

                    # 记录vip 优惠折扣
                    seat.discountPrice.append(vipMoney)

                    # 当前价格设置为已参加过vip折中折
                    seat.amt_receivable = vipPric

    # 以零售金额为基础
    elif bean.target_item == "amt_retail":
        # 判断是否可以参参加vip折中折
        if bean.is_run_vip_discount:
            # 当前商品没有参加过vip折中折
            if not seat.is_run_vip_discount:
                if userInfo.discount:
                    # 设置当前商品已经参加过vip折中折
                    seat.is_run_vip_discount = True

                    vipPric = float(seat.amt_retail * userInfo.discount)
                    vipPric = round(vipPric, 2)

                    # 计算vip 折中折优惠金额
                    vipMoney = seat.amt_retail - vipPric

                    # 记录vip 优惠折扣
                    seat.discountPrice.append(vipMoney)

                    # 当前价格设置为已参加过vip折中折
                    seat.amt_receivable = vipPric
    # 吊牌金额优惠基础
    elif bean.target_item == "amt_list":
        # 判断是否可以参参加vip折中折
        if bean.is_run_vip_discount:
            # 当前商品没有参加过vip折中折
            if not seat.is_run_vip_discount:
                if userInfo.discount:
                    # 设置当前商品已经参加过vip折中折
                    seat.is_run_vip_discount = True

                    vipPric = float(seat.amt_list * userInfo.discount)
                    vipPric = round(vipPric, 2)

                    # 计算vip 折中折优惠金额
                    vipMoney = seat.amt_list - vipPric

                    # 记录vip 优惠折扣
                    seat.discountPrice.append(vipMoney)

                    # 当前价格设置为已参加过vip折中折
                    seat.amt_receivable = vipPric

    else:
        raise ProException("优惠价格基础参数错误")


def not_buy_a_give_a_unify(
        bean,
        userInfo,
        productList,
        promotion_qtty_sum,
        promotion_amt_list_sum,
        promotion_amt_retail_sum,
        promotion_amt_receivable_sum,
        org_infos,
        org_productlists,
        give_product):
    """
    :param bean: 统一买赠、梯度买赠的具体对象
    :param productListA:  所有可以参加活动的列表
    :param not_product_ListA:  所有不可以参加的列表
    :param promotion_qtty_sum:  数量总数
    :param promotion_amt_list_sum:  amt_list:吊牌金额
    :param promotion_amt_retail_sum: amt_retail:零售金额
    :param promotion_amt_receivable_sum: amt_receivable:应收金额
    :param org_infos:未排除已占位商品的符合该促销的数量、吊牌价、零售价、应收价统计结果字典；
    :param give_product:交集的商品（即在条件商品列表里又在赠品商品列表里）
    :return:
    """
    isallpro = False

    # 第一步判断活动是否符合执行条件
    if bean.give_value == 0:
        return str(-1)

    if bean.comp_symb_type == "e" and bean.value_num == 0:
        return str(-1)

    # if bean.comp_symb_type == "g":
    #     bean.value_num += 1

    if bean.target_type == "qtty":
        if not promotion_qtty_sum >= bean.value_num:
            if org_infos.get("org_promotion_qtty_sum", 0) >= bean.value_num:
                productList = copy.deepcopy(org_productlists)
                isallpro = True
            else:
                return str(-1)
    elif bean.target_type == "amt_list":
        if not promotion_amt_list_sum >= bean.value_num:
            if org_infos.get(
                "org_promotion_amt_list_sum",
                    0) >= bean.value_num:
                productList = copy.deepcopy(org_productlists)
                isallpro = True
            else:
                return str(-1)
    elif bean.target_type == "amt_retail":
        if not promotion_amt_retail_sum >= bean.value_num:
            if org_infos.get(
                "org_promotion_amt_retail_sum",
                    0) >= bean.value_num:
                productList = copy.deepcopy(org_productlists)
                isallpro = True
            else:
                return str(-1)
    elif bean.target_type == "amt_receivable":
        if not promotion_amt_receivable_sum >= bean.value_num:
            if org_infos.get(
                "org_promotion_amt_receivable_sum",
                    0) >= bean.value_num:
                productList = copy.deepcopy(org_productlists)
                isallpro = True
            else:
                return str(-1)
    if isallpro:
        return 1

    has_special_product_flug = False
    has_special_product_give_flug = False
    for product_item in productList:
        if has_special_product_flug and has_special_product_give_flug:
            break
        if product_item.ecode in bean.product_list:
            if product_item.productSeatList[0].is_discount == "n":
                for seat in product_item.productSeatList:
                    if seat.seat == False and seat.is_run_other_pro:
                        if product_item.ecode in give_product:
                            has_special_product_give_flug = True
                        else:
                            has_special_product_flug = True
                        break
    has_special_product = {"condition_pro_flug": has_special_product_flug,
                           "give_pro_flug": has_special_product_give_flug}
    newproductlist, max_times, max_pronum, now_max_amt = discomputefunction(
        bean, productList, 0, 0, 0, 0, 0, 0, 0, give_product, has_special_product)

    # promotion_lineno:梯度买赠进入，记录当前执行的到底是哪个梯度的，这样返回前端时，只返回该梯度前所有的商品
    promotion_lineno = 0
    if bean.prom_type_three == "ga1402":
        promotion_lineno = bean.promotion_lineno
    response_1 = {}
    response_1["product"] = newproductlist
    response_1["buygift"] = {
        "id": bean.id,
        "qtty": max_pronum,
        "sum_amt": now_max_amt,
        "online_qtty": 0,
        "online_amtlist": 0,
        "max_double_times": 0,
        "all_give_infos": [],
        "promotion_lineno": promotion_lineno,
        "isallpro": isallpro}
    response_1["isallpro"] = isallpro
    response_1["dis_id"] = bean.id
    return response_1


def discomputefunction(
        bean,
        productList,
        now_max_times,
        now_max_pro_numb,
        now_max_amt,
        all_sum_amt_list,
        all_sum_amt_retail,
        all_sum_amt_receivable,
        all_sum_qtty,
        give_product,
        has_special_product):
    '''
    买赠促销的具体计算方法（统一买赠、梯度买赠）
    :param bean:当前促销活动
    :param productList:商品信息
    :param now_max_times:可翻倍次数
    :param now_max_pro_numb:可赠送商品数量
    :param now_max_amt:优惠的总金额
    :param give_product:交集的商品（即在条件商品列表里又在赠品商品列表里）
    :return:
    '''
    # 先将商品按照吊牌价降序排序，优先将一倍的条件商品筛选出来
    nownum = 0  # 当前可翻多少倍（对于按金额计算，有可能会发生大于1的倍数，按数量的每次进来这个都是1）
    max_pro_numb = 0  # 当前翻的倍数赠送的商品数
    ishavedis = True
    isaddrow = True

    # if bean.comp_symb_type == "g":
    #     bean.value_num += 1

    seatrownum = 0
    productListA = []
    productList = sorted(
        productList,
        key=lambda i: i.productSeatList[0].amt_list,
        reverse=True)

    oldproductList = copy.deepcopy(productList)
    seat_list = []  # 参与的商品明细

    # 在统计一倍的调价商品占位时优先占位只是条件商品的商品，之后还有剩余，那么再占位既是条件商品又是赠品的商品
    all_sum_amt_list, all_sum_amt_retail, all_sum_amt_receivable, all_sum_qtty, has_special_product = \
        getonepronumb(productList, bean, seatrownum, now_max_times, productListA,
                      all_sum_amt_list, all_sum_amt_retail, all_sum_amt_receivable,
                      all_sum_qtty, isaddrow, ishavedis, give_product, 1, has_special_product, seat_list)
    if give_product:
        if bean.target_type == "qtty":
            nownum = int(all_sum_qtty // bean.value_num)
        elif bean.target_type == "amt_list":
            nownum = int(all_sum_amt_list // bean.value_num)
        elif bean.target_type == "amt_retail":
            nownum = int(all_sum_amt_retail // bean.value_num)
        elif bean.target_type == "amt_receivable":
            nownum = int(all_sum_amt_receivable // bean.value_num)

        if nownum < 1 or nownum <= now_max_times:
            all_sum_amt_list, all_sum_amt_retail, all_sum_amt_receivable, all_sum_qtty, has_special_product = \
                getonepronumb(productList, bean, seatrownum, now_max_times, productListA, all_sum_amt_list,
                              all_sum_amt_retail, all_sum_amt_receivable, all_sum_qtty, isaddrow,
                              ishavedis, give_product, 2, has_special_product, seat_list)

    if not productListA:
        return oldproductList, now_max_times, now_max_pro_numb, now_max_amt
    else:

        if bean.target_type == "qtty":
            nownum = int(all_sum_qtty // bean.value_num)
        elif bean.target_type == "amt_list":
            nownum = int(all_sum_amt_list // bean.value_num)
        elif bean.target_type == "amt_retail":
            nownum = int(all_sum_amt_retail // bean.value_num)
        elif bean.target_type == "amt_receivable":
            nownum = int(all_sum_amt_receivable // bean.value_num)

        if nownum < 1 or nownum <= now_max_times:
            return oldproductList, now_max_times, now_max_pro_numb, now_max_amt
        if bean.max_times == -1:
            # 可无限翻倍
            max_pro_numb = bean.give_value * (nownum - now_max_times)
        elif bean.max_times >= 0:
            if nownum - now_max_times > 1:
                if bean.max_times != 0:
                    if nownum > bean.max_times:
                        nownum = bean.max_times
                        max_pro_numb = bean.give_value * (nownum - now_max_times)
                        # return oldproductList, now_max_times, now_max_pro_numb, now_max_amt
                    else:
                        max_pro_numb = bean.give_value * \
                            (nownum - now_max_times)
                else:
                    nownum = 1
                    max_pro_numb = bean.give_value
            else:
                if bean.max_times != 0:
                    if nownum > bean.max_times:
                        nownum = bean.max_times
                else:
                    nownum = 1
                max_pro_numb = bean.give_value

        # 将商品按照吊牌价升序排序，进行赠品占位
        productList = sorted(productList,
                             key=lambda i: i.productSeatList[0].amt_list)

        now_max_times = nownum
        now_max_pro_numb = bean.give_value * nownum
        # 将参与的明细占位
        for seat in seat_list:
            seat.seat = True

        for product1 in productList:
            if max_pro_numb <= 0:
                break
            for ecode1 in bean.buygift_product:
                if max_pro_numb <= 0:
                    break
                if ecode1["ecode"].lower(
                ) == product1.ecode.lower() and max_pro_numb > 0:
                    for r_seat1 in product1.productSeatList:
                        if max_pro_numb <= 0:
                            break
                        if r_seat1.seat == False and r_seat1.is_discount == "y":
                            pric=0
                            r_seat1.seat = True
                            r_seat1.discountId.append(bean.id)
                            if bean.target_item == "amt_receivable":
                                r_seat1.discountPrice.append(r_seat1.amt_receivable)
                                pric=r_seat1.amt_receivable
                            elif bean.target_item == 'amt_retail':
                                r_seat1.discountPrice.append(r_seat1.amt_retail)
                                pric = r_seat1.amt_retail
                            elif bean.target_item == 'amt_list':
                                r_seat1.discountPrice.append(r_seat1.amt_list)
                                pric = r_seat1.amt_list
                            r_seat1.str_discount = r_seat1.str_discount + '参加' + bean.ename + '活动优惠了' + str(pric) + '元\n'
                            r_seat1.amt_receivable = 0
                            r_seat1.is_run_other_pro = bean.is_run_other_pro
                            r_seat1.is_run_store_act = bean.is_run_store_act
                            r_seat1.is_buy_gifts = "y"
                            now_max_amt = now_max_amt + float(pric)
                            max_pro_numb = max_pro_numb - 1

        if bean.max_times > 1 and (now_max_times + 1) > bean.max_times:
            return productList, now_max_times, now_max_pro_numb, now_max_amt
        else:
            # if not ishavedis:
            #     return productList, now_max_times, now_max_pro_numb, now_max_amt
            # else:
            if bean.max_times == 0:
                return productList, now_max_times, now_max_pro_numb, now_max_amt
            return discomputefunction(
                bean,
                productList,
                now_max_times,
                now_max_pro_numb,
                now_max_amt,
                all_sum_amt_list,
                all_sum_amt_retail,
                all_sum_amt_receivable,
                all_sum_qtty,
                give_product,
                has_special_product)


def combination_unify_dis(
        bean,
        productList,
        org_productlists,
        holddis,
        give_product):
    """
    :param bean: 组合买赠的具体对象
    :param productList: 执行过其它类型促销的商品集合
    :param org_productlists:最原始的商品集合
    :param holddis:是否是使用最原始的商品计算
    :param give_product:交集的商品（即在条件商品列表里又在赠品商品列表里）
    :return:
    """
    isallpro = False

    if holddis == 1:
        isallpro = True
        productList = copy.deepcopy(org_productlists)

    newproductlist, max_times, max_pronum, now_max_amt = discomputefunction_cb(
        bean, productList, 0, 0, 0, 0, 0, 0, 0, give_product, [])

    # promotion_lineno:梯度买赠进入，记录当前执行的到底是哪个梯度的，这样返回前端时，只返回该梯度前所有的商品
    promotion_lineno = 0
    if bean.prom_type_three == "ga1402":
        promotion_lineno = bean.promotion_lineno
    response_1 = {}
    response_1["product"] = newproductlist
    response_1["buygift"] = {
        "id": bean.id,
        "qtty": max_pronum,
        "sum_amt": now_max_amt,
        "online_qtty": 0,
        "online_amtlist": 0,
        "max_double_times": 0,
        "all_give_infos": [],
        "promotion_lineno": promotion_lineno,
        "isallpro": isallpro}
    response_1["isallpro"] = isallpro
    response_1["dis_id"] = bean.id
    return response_1


def discomputefunction_cb(
        bean,
        productList,
        now_max_times,
        now_max_pro_numb,
        now_max_amt,
        all_sum_amt_list,
        all_sum_amt_retail,
        all_sum_amt_receivable,
        all_sum_qtty,
        give_product,
        specific_rowtotal):
    '''
    组合买赠促销的具体计算方法
    :param bean:当前促销活动
    :param productList:商品信息
    :param now_max_times:可翻倍次数
    :param now_max_pro_numb:可赠送商品数量
    :param now_max_amt:优惠的总金额
    :param all_sum_amt_list:
    :param all_sum_amt_retail:
    :param all_sum_amt_receivable:
    :param all_sum_qtty:
    :param give_product:交集的商品（即在条件商品列表里又在赠品商品列表里）
    :param specific_rowtotal:记录组合条件每项参与计算的总的相关数据，供递归统计翻倍次数使用
    :return:
    '''
    # 先将商品按照吊牌价降序排序，优先将一倍的条件商品筛选出来
    nownum = 0  # 当前可翻多少倍（对于按金额计算，有可能会发生大于1的倍数，按数量的每次进来这个都是1）
    max_pro_numb = 0  # 当前翻的倍数赠送的商品数
    ishavedis = True
    isaddrow = True

    seatrownum = 0
    productListA = []
    productList = sorted(
        productList,
        key=lambda i: i.productSeatList[0].amt_list,
        reverse=True)

    oldproductList = copy.deepcopy(productList)
    # seat_all_list = []
    bean_items = []
    seat_list = []  # 参与的商品明细
    current_not_caculate = []
    for row_index,r_item in enumerate(bean.specific_activities):
        if specific_rowtotal and len(specific_rowtotal)>row_index:
            all_sum_amt_list = specific_rowtotal[row_index]["all_sum_amt_list"]
            all_sum_amt_retail = specific_rowtotal[row_index]["all_sum_amt_retail"]
            all_sum_amt_receivable = specific_rowtotal[row_index]["all_sum_amt_receivable"]
            all_sum_qtty = specific_rowtotal[row_index]["all_sum_qtty"]
            has_special_product = specific_rowtotal[row_index]["has_special_product"]
        else:
            all_sum_amt_list = 0
            all_sum_amt_retail = 0
            all_sum_amt_receivable = 0
            all_sum_qtty = 0
            has_special_product_flug = False
            has_special_product_give_flug = False
            for product_item in productList:
                if has_special_product_flug and has_special_product_give_flug:
                    break
                if product_item.ecode in r_item.product_list:
                    if product_item.productSeatList[0].is_discount == "n":
                        for seat in product_item.productSeatList:
                            if seat.seat == False and seat.is_run_other_pro:
                                if product_item.ecode in give_product:
                                    has_special_product_give_flug = True
                                else:
                                    has_special_product_flug = True
                                break
            has_special_product = {"condition_pro_flug": has_special_product_flug,
                                   "give_pro_flug": has_special_product_give_flug}
        productListA = []

        # if r_item.comp_symb_type == "g":
        #     r_item.value_num += 1
        # seat_list = []
        all_sum_amt_list, all_sum_amt_retail, all_sum_amt_receivable, all_sum_qtty, has_special_product = \
            getonepronumb(productList, r_item, seatrownum, now_max_times, productListA,
                          all_sum_amt_list, all_sum_amt_retail, all_sum_amt_receivable,
                          all_sum_qtty, isaddrow, ishavedis, give_product, 1, has_special_product, seat_list)

        if give_product:
            if r_item.target_type == "qtty":
                nownum = int(all_sum_qtty // r_item.value_num)
            elif r_item.target_type == "amt_list":
                nownum = int(all_sum_amt_list // r_item.value_num)
            elif r_item.target_type == "amt_retail":
                nownum = int(all_sum_amt_retail // r_item.value_num)
            elif r_item.target_type == "amt_receivable":
                nownum = int(all_sum_amt_receivable // r_item.value_num)

            if nownum < 1 or nownum <= now_max_times:
                all_sum_amt_list, all_sum_amt_retail, all_sum_amt_receivable, all_sum_qtty,\
                has_special_product = getonepronumb(productList, r_item, seatrownum, now_max_times,
                                                    productListA, all_sum_amt_list, all_sum_amt_retail,
                                                    all_sum_amt_receivable, all_sum_qtty,
                                                    isaddrow, ishavedis, give_product, 2,
                                                    has_special_product, seat_list)

        isadd_specific_rowtotal=True
        if specific_rowtotal:
            if len(specific_rowtotal)>row_index:
                isadd_specific_rowtotal=False

        if isadd_specific_rowtotal:
            newrowitem={}
            newrowitem["all_sum_amt_list"] = 0
            newrowitem["all_sum_amt_retail"] = 0
            newrowitem["all_sum_amt_receivable"] = 0
            newrowitem["all_sum_qtty"] = 0
            newrowitem["has_special_product"] = has_special_product
            specific_rowtotal.append(newrowitem)
        else:
            # 先不将每行结果记录， 当每一行的结果都出来后，再根据筛选出来的商品计算每一行的最终比较价格
            # specific_rowtotal[row_index]["all_sum_amt_list"]=all_sum_amt_list
            # specific_rowtotal[row_index]["all_sum_amt_retail"] = all_sum_amt_retail
            # specific_rowtotal[row_index]["all_sum_amt_receivable"] = all_sum_amt_receivable
            # specific_rowtotal[row_index]["all_sum_qtty"] = all_sum_qtty
            specific_rowtotal[row_index]["has_special_product"] = has_special_product

        # if not productListA:
        #     # return oldproductList, now_max_times, now_max_pro_numb, now_max_amt
        #     break
        if not productListA:
            # 说明这一行已经达到当前倍数， 没有进行计算
            current_not_caculate.append(row_index)
        if r_item.target_type == "qtty":
            nownum = int(all_sum_qtty // r_item.value_num)
        elif r_item.target_type == "amt_list":
            nownum = int(all_sum_amt_list // r_item.value_num)
        elif r_item.target_type == "amt_retail":
            nownum = int(all_sum_amt_retail // r_item.value_num)
        elif r_item.target_type == "amt_receivable":
            nownum = int(all_sum_amt_receivable // r_item.value_num)

        if nownum < 1 or nownum <= now_max_times:
            # return oldproductList, now_max_times, now_max_pro_numb, now_max_amt
            break

        if r_item.max_times == -1:
            # 可无限翻倍
            max_pro_numb = bean.give_value * (nownum - now_max_times)
        elif r_item.max_times >= 0:
            # 不可翻倍或设置了固定翻倍次数
            if (nownum - now_max_times) > 1:
                if r_item.max_times != 0:
                    if nownum > r_item.max_times:
                        nownum = r_item.max_times
                        max_pro_numb = bean.give_value * (nownum - now_max_times)
                        # return oldproductList, now_max_times, now_max_pro_numb, now_max_amt
                    else:
                        max_pro_numb = bean.give_value * \
                            (nownum - now_max_times)
                        # return
                        # productList,now_max_times,now_max_pro_numb,now_max_amt
                else:
                    nownum = 1
                    max_pro_numb = bean.give_value
            else:
                if r_item.max_times != 0:
                    if nownum > r_item.max_times:
                        nownum = r_item.max_times
                else:
                    nownum = 1
                max_pro_numb = bean.give_value

        bean_item = {}
        bean_item["nownum"] = nownum
        bean_item["max_pro_numb"] = max_pro_numb
        bean_item["ishavedis"] = ishavedis
        bean_items.append(bean_item)

    for seat in seat_list:
        # 根据筛选出来的商品，计算每个比较行中的总金额，总数量
        seat.seat = True
        for row_index, r_item in enumerate(bean.specific_activities):
            product_list = r_item.product_list
            if seat.ecode in product_list:
                all_sum_amt_list = specific_rowtotal[row_index]["all_sum_amt_list"]
                all_sum_amt_retail = specific_rowtotal[row_index]["all_sum_amt_retail"]
                all_sum_amt_receivable = specific_rowtotal[row_index]["all_sum_amt_receivable"]
                all_sum_qtty = specific_rowtotal[row_index]["all_sum_qtty"]
                all_sum_amt_list += seat.amt_list
                all_sum_amt_retail += seat.amt_retail
                all_sum_amt_receivable += seat.amt_receivable
                all_sum_qtty += seat.qtty
                specific_rowtotal[row_index]["all_sum_amt_list"] = all_sum_amt_list
                specific_rowtotal[row_index]["all_sum_amt_retail"] = all_sum_amt_retail
                specific_rowtotal[row_index]["all_sum_amt_receivable"] = all_sum_amt_receivable
                specific_rowtotal[row_index]["all_sum_qtty"] = all_sum_qtty
    # if current_not_caculate:
    #     # 对于这一倍没有进行计算的， 需要将其他行筛选出来的商品在本行，明细中的金额，数量加上去， 不然会有问题。
    #     for seat in seat_list:
    #         for current_item in current_not_caculate:
    #             product_list = bean.specific_activities[current_item].product_list
    #             if seat.ecode in product_list:
    #                 all_sum_amt_list = specific_rowtotal[current_item]["all_sum_amt_list"]
    #                 all_sum_amt_retail = specific_rowtotal[current_item]["all_sum_amt_retail"]
    #                 all_sum_amt_receivable = specific_rowtotal[current_item]["all_sum_amt_receivable"]
    #                 all_sum_qtty = specific_rowtotal[current_item]["all_sum_qtty"]
    #                 all_sum_amt_list += seat.amt_list
    #                 all_sum_amt_retail += seat.amt_retail
    #                 all_sum_amt_receivable += seat.amt_receivable
    #                 all_sum_qtty += seat.qtty
    #                 specific_rowtotal[current_item]["all_sum_amt_list"] = all_sum_amt_list
    #                 specific_rowtotal[current_item]["all_sum_amt_retail"] = all_sum_amt_retail
    #                 specific_rowtotal[current_item]["all_sum_amt_receivable"] = all_sum_amt_receivable
    #                 specific_rowtotal[current_item]["all_sum_qtty"] = all_sum_qtty

    # for seat_all_item in seat_all_list:
    #     for seat in seat_all_item:
    #         seat.seat = True
    # for seat in seat_list:
    #     seat.seat = True
    # print("=======================" + str(len(seat_list)))
    # for item in specific_rowtotal:
    #     print("********************" + str(item))
    if len(bean_items) < len(bean.specific_activities):
        max_pro_numb=0
        nownum=now_max_times
    else:
        for index, r in enumerate(bean_items):
            if index == 0:
                nownum = r["nownum"] if r["ishavedis"] else 0
                max_pro_numb = r["max_pro_numb"] if r["ishavedis"] else 0
            else:
                max_pro_numb = r["max_pro_numb"] if nownum > r["nownum"] else max_pro_numb
                nownum = r["nownum"] if nownum > r["nownum"] else nownum

    # 将商品按照吊牌价升序排序，进行赠品占位
    productList = sorted(
        productList,
        key=lambda i: i.productSeatList[0].amt_list)

    now_max_times = nownum
    now_max_pro_numb = bean.give_value * nownum

    if max_pro_numb>0:
        for product1 in productList:
            if max_pro_numb <= 0:
                break
            for ecode1 in bean.buygift_product:
                if max_pro_numb <= 0:
                    break
                if ecode1["ecode"].lower(
                ) == product1.ecode.lower() and max_pro_numb > 0:
                    for r_seat1 in product1.productSeatList:
                        if max_pro_numb <= 0:
                            break
                        if r_seat1.seat == False and r_seat1.is_discount == "y":
                            pric = 0
                            r_seat1.seat = True
                            r_seat1.discountId.append(bean.id)
                            if bean.target_item == "amt_receivable":
                                r_seat1.discountPrice.append(r_seat1.amt_receivable)
                                pric = r_seat1.amt_receivable
                            elif bean.target_item == 'amt_retail':
                                r_seat1.discountPrice.append(r_seat1.amt_retail)
                                pric = r_seat1.amt_retail
                            elif bean.target_item == 'amt_list':
                                r_seat1.discountPrice.append(r_seat1.amt_list)
                                pric = r_seat1.amt_list
                            r_seat1.str_discount = r_seat1.str_discount + '参加' + bean.ename + '活动优惠了' + str(pric) + '元\n'
                            r_seat1.amt_receivable=0
                            r_seat1.is_run_other_pro = bean.is_run_other_pro
                            r_seat1.is_run_store_act = bean.is_run_store_act
                            r_seat1.is_buy_gifts = "y"
                            now_max_amt = now_max_amt + r_seat1.amt_receivable
                            max_pro_numb = max_pro_numb - 1
    else:
        return productList, now_max_times, now_max_pro_numb, now_max_amt

    if bean.max_times > 1 and (now_max_times + 1) > bean.max_times:
        return productList, now_max_times, now_max_pro_numb, now_max_amt
    else:
        if bean.max_times == 0:
            return productList, now_max_times, now_max_pro_numb, now_max_amt
        return discomputefunction_cb(
            bean,
            productList,
            now_max_times,
            now_max_pro_numb,
            now_max_amt,
            all_sum_amt_list,
            all_sum_amt_retail,
            all_sum_amt_receivable,
            all_sum_qtty, give_product,specific_rowtotal)


def getonepronumb(
        productList,
        bean,
        seatrownum,
        now_max_times,
        productListA,
        all_sum_amt_list,
        all_sum_amt_retail,
        all_sum_amt_receivable,
        all_sum_qtty,
        isaddrow,
        ishavedis,
        give_product,
        intype,
        has_special_product,
        seat_list):
    '''
    获取每个组合项的比较情况
    :param productList:
    :param bean:
    :param seatrownum:
    :param now_max_times:
    :param productListA:
    :param all_sum_amt_list:
    :param all_sum_amt_retail:
    :param all_sum_amt_receivable:
    :param all_sum_qtty:
    :param isaddrow:
    :param ishavedis:
    :param give_product:交集的商品（即在条件商品列表里又在赠品商品列表里）
    :param intype:1 表示当前从只在条件商品不在赠品里的获取条件商品占位;2 表示从存在交集的商品里获取条件商品占位；
    :return:
    '''
    current_caculate_sum = 0  # 当前条件商品的
    is_can_caculate = True
    if bean.target_type == "qtty":
        if bean.max_times > 0 and int(all_sum_qtty // bean.value_num) >= bean.max_times:
            is_can_caculate = False
        current_caculate_sum = all_sum_qtty - (now_max_times * bean.value_num)
    elif bean.target_type == "amt_list":
        if bean.max_times > 0 and int(all_sum_amt_list // bean.value_num) >= bean.max_times:
            is_can_caculate = False
        current_caculate_sum = all_sum_amt_list - (now_max_times * bean.value_num)
    elif bean.target_type == "amt_retail":
        if bean.max_times > 0 and int(all_sum_amt_retail // bean.value_num) >= bean.max_times:
            is_can_caculate = False
        current_caculate_sum = all_sum_amt_retail - (now_max_times * bean.value_num)
    elif bean.target_type == "amt_receivable":
        if bean.max_times > 0 and int(all_sum_amt_receivable // bean.value_num) >= bean.max_times:
            is_can_caculate = False
        current_caculate_sum = all_sum_amt_receivable - (now_max_times * bean.value_num)

    if not is_can_caculate:
        return all_sum_amt_list, all_sum_amt_retail, all_sum_amt_receivable, all_sum_qtty, has_special_product
    if current_caculate_sum >= bean.value_num:
        return all_sum_amt_list, all_sum_amt_retail, all_sum_amt_receivable, all_sum_qtty, has_special_product
    condition_pro_flug = has_special_product.get("condition_pro_flug", False)
    give_pro_flug = has_special_product.get("give_pro_flug", False)
    if (intype == 1 and condition_pro_flug) or (intype == 2 and give_pro_flug):
        for product in productList:
            if current_caculate_sum >= bean.value_num:
                # 当当前的计算总和大于比较值时，结束循环
                break
            if not isaddrow:
                break
            if intype == 1 and product.ecode in give_product:
                continue
            if intype == 2 and (product.ecode not in give_product):
                continue
            if product.productSeatList[0].is_discount == "y":
                if intype == 1 and condition_pro_flug:
                    continue
                if intype == 2 and give_pro_flug:
                    continue
            for ecode in bean.product_list:
                if current_caculate_sum >= bean.value_num:
                    # 当当前的计算总和大于比较值时，结束循环
                    break
                if not isaddrow:
                    break
                if ecode.lower() == product.ecode.lower():
                    seatrownum = 0
                    newrow = copy.deepcopy(product)
                    newrow.productSeatList = []
                    newrow.sum_amt_list = 0
                    newrow.sum_amt_retail = 0
                    newrow.sum_amt_receivable = 0
                    newrow.qtty = 0
                    product.productSeatList = sorted(
                        product.productSeatList, key=lambda i: i.amt_list, reverse=True)
                    for r_seat in product.productSeatList:
                        if r_seat.seat:
                            seatrownum += 1
                            continue
                        if not ishavedis:
                            isaddrow = False
                            break
                        if current_caculate_sum >= bean.value_num:
                            # 当当前的计算总和大于比较值时，结束循环
                            break
                        # if bean.max_times != 0:
                        if bean.target_type == "qtty":
                            current_caculate_sum += 1
                        elif bean.target_type == "amt_list":
                            current_caculate_sum += r_seat.amt_list
                        elif bean.target_type == "amt_retail":
                            current_caculate_sum += r_seat.amt_retail
                        elif bean.target_type == "amt_receivable":
                            # if bean.max_times == -1 or bean.max_times > 0:
                            current_caculate_sum += r_seat.amt_receivable

                        newrow.productSeatList.append(r_seat)
                        newrow.qtty = newrow.qtty + 1
                        newrow.sum_amt_list = newrow.sum_amt_list + r_seat.amt_list
                        newrow.sum_amt_retail = newrow.sum_amt_retail + r_seat.amt_retail
                        newrow.sum_amt_receivable = newrow.sum_amt_receivable + r_seat.amt_receivable
                        # r_seat.seat = True
                        if r_seat not in seat_list:
                            seat_list.append(r_seat)
                    if isaddrow and seatrownum < len(product.productSeatList):
                        all_sum_amt_list = all_sum_amt_list + newrow.sum_amt_list
                        all_sum_amt_retail = all_sum_amt_retail + newrow.sum_amt_retail
                        all_sum_amt_receivable = all_sum_amt_receivable + newrow.sum_amt_receivable
                        all_sum_qtty = all_sum_qtty + newrow.qtty
                        productListA.append(newrow)
                    break
    if current_caculate_sum >= bean.value_num:
        return all_sum_amt_list, all_sum_amt_retail, all_sum_amt_receivable, all_sum_qtty, has_special_product
    if intype == 1:
        has_special_product["condition_pro_flug"] = False
    if intype == 2:
        has_special_product["give_pro_flug"] = False
    for product in productList:
        if current_caculate_sum >= bean.value_num:
            # 当当前的计算总和大于比较值时，结束循环
            break
        if not isaddrow:
            break
        if product.productSeatList[0].is_discount == "n":
            continue
        if intype == 1 and product.ecode in give_product:
            continue
        if intype == 2 and (product.ecode not in give_product):
            continue
        for ecode in bean.product_list:
            if current_caculate_sum >= bean.value_num:
                # 当当前的计算总和大于比较值时，结束循环
                break
            if not isaddrow:
                break
            if ecode.lower() == product.ecode.lower():
                seatrownum = 0
                newrow = copy.deepcopy(product)
                newrow.productSeatList = []
                newrow.sum_amt_list = 0
                newrow.sum_amt_retail = 0
                newrow.sum_amt_receivable = 0
                newrow.qtty = 0
                product.productSeatList = sorted(
                    product.productSeatList, key=lambda i: i.amt_list, reverse=True)
                for r_seat in product.productSeatList:
                    if r_seat.seat:
                        seatrownum += 1
                        continue
                    if not ishavedis:
                        isaddrow = False
                        break
                    if current_caculate_sum >= bean.value_num:
                        # 当当前的计算总和大于比较值时，结束循环
                        break
                    # if bean.max_times != 0:
                    if bean.target_type == "qtty":
                        # if all_sum_qtty >= bean.value_num:
                        #     break
                        # if newrow.qtty >= bean.value_num:
                        #     break
                        current_caculate_sum += 1
                        # if bean.max_times >= 1:
                        #     nownum = int(
                        #         (all_sum_qtty +
                        #          newrow.qtty +
                        #          1) //
                        #         bean.value_num)
                        #     if nownum >= 1 and now_max_times > 0:
                        #         if nownum > bean.max_times:
                        #             ishavedis = False
                        #             isaddrow = False
                        #             break

                    elif bean.target_type == "amt_list":
                        # if all_sum_amt_list >= bean.value_num:
                        #     break
                        # if newrow.sum_amt_list >= bean.value_num:
                        #     break
                        current_caculate_sum += r_seat.amt_list
                        # if bean.max_times >= 1:
                        #     nownum = int(
                        #         (all_sum_amt_list +
                        #          newrow.sum_amt_list +
                        #          r_seat.amt_list) //
                        #         bean.value_num)
                        #     if nownum >= 1 and now_max_times > 0:
                        #         if nownum > bean.max_times:
                        #             ishavedis = False
                        #             isaddrow = False
                        #             break
                    elif bean.target_type == "amt_retail":
                        # if all_sum_amt_retail >= bean.value_num:
                        #     break
                        # if newrow.sum_amt_retail >= bean.value_num:
                        #     break
                        current_caculate_sum += r_seat.amt_retail
                        # if bean.max_times >= 1:
                        #     nownum = int(
                        #         (all_sum_amt_retail +
                        #          newrow.sum_amt_retail +
                        #          r_seat.amt_retail) //
                        #         bean.value_num)
                        #     if nownum >= 1 and now_max_times > 0:
                        #         if nownum > bean.max_times:
                        #             ishavedis = False
                        #             isaddrow = False
                        #             break
                    elif bean.target_type == "amt_receivable":
                        current_caculate_sum += r_seat.amt_receivable
                        # if bean.max_times == -1 or bean.max_times > 0:
                            # if all_sum_amt_receivable >= bean.value_num:
                            #     break
                            # if newrow.sum_amt_receivable >= bean.value_num:
                            #     break
                            # current_caculate_sum += r_seat.amt_receivable
                            # if bean.max_times >= 1:
                            #     nownum = int(
                            #         (all_sum_amt_receivable +
                            #          newrow.sum_amt_receivable +
                            #          r_seat.amt_receivable) //
                            #         bean.value_num)
                            #     if nownum >= 1 and now_max_times > 0:
                            #         if nownum > bean.max_times:
                            #             ishavedis = False
                            #             isaddrow = False
                            #             break

                    newrow.productSeatList.append(r_seat)
                    newrow.qtty = newrow.qtty + 1
                    newrow.sum_amt_list = newrow.sum_amt_list + r_seat.amt_list
                    newrow.sum_amt_retail = newrow.sum_amt_retail + r_seat.amt_retail
                    newrow.sum_amt_receivable = newrow.sum_amt_receivable + r_seat.amt_receivable
                    # r_seat.seat = True
                    if r_seat not in seat_list:
                        seat_list.append(r_seat)
                if isaddrow and seatrownum < len(product.productSeatList):
                    all_sum_amt_list = all_sum_amt_list + newrow.sum_amt_list
                    all_sum_amt_retail = all_sum_amt_retail + newrow.sum_amt_retail
                    all_sum_amt_receivable = all_sum_amt_receivable + newrow.sum_amt_receivable
                    all_sum_qtty = all_sum_qtty + newrow.qtty
                    productListA.append(newrow)
                break

    return all_sum_amt_list, all_sum_amt_retail, all_sum_amt_receivable, all_sum_qtty, has_special_product


def get_optimalgroupdis(productListMAX):
    '''
    筛选出最优的某个组合的执行情况
    :param productListMAX: 前面不同排序执行的结果集
    :return:n_productlists（最优组的商品标记明细）
    '''
    buygift_list = []
    if len(productListMAX) > 1:
        row_sumbuygiftpro_up = 0 #上个执行顺序中已优惠后的总金额（包含已录入赠送商品的促销，和新的 线上买赠、线上排名买赠 的促销）
        row_sumamtpro_up = 0 #上个执行顺序中录入的赠品的总金额（也就是总优惠的金额）
        row_sumqttyoline_up= 0   #上个执行顺序中线上买赠、线上排名买赠可赠送的商品总数量
        row_sumamtoline_up = 0  # 上个执行顺序中线上买赠、线上排名买赠可赠送的商品总吊牌价
        index_row = 0
        for row in productListMAX:
            row_sumamtpro = 0
            row_sumqttyoline=0
            row_sumamtoline=0
            row_sumamt = 0
            for row_item in row:
                row_sumamtpro += row_item["buygift"]["sum_amt"]
                row_sumqttyoline +=row_item["buygift"]["online_qtty"]
                row_sumamtoline +=row_item["buygift"]["online_amtlist"]

            for row_item1 in row[-1]["product"]:
                for row_item2 in row_item1.productSeatList:
                    row_sumamt += row_item2.amt_receivable

            if row_sumamtpro==0 and row_sumqttyoline==0 and row_sumamtoline==0:
                continue

            if row_sumbuygiftpro_up>0:
                if row_sumbuygiftpro_up>row_sumamt:
                    row_sumbuygiftpro_up = row_sumamt
                    row_sumamtpro_up = row_sumamtpro
                    row_sumqttyoline_up = row_sumqttyoline
                    row_sumamtoline_up = row_sumamtoline
                    index_row = productListMAX.index(row)
                elif row_sumbuygiftpro_up==row_sumamt:
                    if row_sumamtpro>row_sumamtpro_up or row_sumamtoline>row_sumamtoline_up or row_sumqttyoline>row_sumqttyoline_up:
                        row_sumbuygiftpro_up = row_sumamt
                        row_sumamtpro_up = row_sumamtpro
                        row_sumqttyoline_up = row_sumqttyoline
                        row_sumamtoline_up = row_sumamtoline
                        index_row = productListMAX.index(row)
            else:
                row_sumbuygiftpro_up = row_sumamt
                row_sumamtpro_up = row_sumamtpro
                row_sumqttyoline_up = row_sumqttyoline
                row_sumamtoline_up = row_sumamtoline
                index_row = productListMAX.index(row)

        n_productlists = productListMAX[index_row]
        for row1 in productListMAX[index_row]:
            buygift_list.append(row1["buygift"])
    else:
        n_productlists = productListMAX[0]
        for row1 in productListMAX[0]:
            buygift_list.append(row1["buygift"])
    return n_productlists


def sum_number_qtty(
        bean,
        userInfo,
        productListA,
        not_product_ListA,
        promotion_qtty_sum,
        number,
        kaiguan):
    '''
    之前其它开发人员写的方法，目前暂时没有使用
    :param bean:
    :param userInfo:
    :param productListA:
    :param not_product_ListA:
    :param promotion_qtty_sum:
    :param number:
    :param kaiguan:
    :return:
    '''
    not_product_ListA = sorted(not_product_ListA,
                               key=lambda i: i.productSeatList[0].amt_list)
    productListA = sorted(
        productListA,
        key=lambda i: i.productSeatList[0].amt_list)
    if bean.comp_symb_type == "ge" or bean.comp_symb_type == "e":

        if bean.give_value == 0:
            return str(-1)

        if bean.comp_symb_type == "e" and bean.value_num == 0:
            return str(-1)

        if not promotion_qtty_sum >= bean.value_num:

            return str(-1)

        if kaiguan:
            return {"id": bean.id}

        sum_give_pro = 0

        # 计算可参与商品的总数量
        for product in productListA:
            for i in product.productSeatList:
                if i.seat == False and i.is_run_other_pro != False:
                    sum_give_pro += 1

        # 计算赠品未站位的数量
        give_sum = get_product_sum(not_product_ListA)

        give_number = 0
        # 计算赠送值

        if number == 1:
            if bean.value_num != 0:
                if bean.max_times == -1:
                    give_number += int(promotion_qtty_sum //
                                       bean.value_num * bean.give_value)
                elif bean.max_times == 0 or bean.max_times == 1:
                    give_number += bean.give_value
                else:
                    # 1 先算出当前最多能翻多少倍
                    # 2 在看看当前最大翻倍数量是否超过 当前倍数
                    # 2.1 如果超过了 用总数除以条件
                    max_fan = int(promotion_qtty_sum // bean.value_num)
                    if max_fan == 0:
                        max_fan = 1
                    if max_fan <= bean.max_times:
                        give_number = bean.give_value * max_fan
                    else:
                        give_number = bean.max_times * bean.give_value

            else:
                give_number = bean.give_value
                bean.max_times = 1

        else:
            bean.max_times = 1
            give_number = bean.give_value
        # 判断值
        panduan_value = 0

        cur_index_off = -1
        # 判断是否是买A赠A
        for product in productListA:
            if product in not_product_ListA:
                cur_index_off -= 1

        # 完整执行完的买赠赠送数量
        end_qtty = copy.deepcopy(give_number)

        # 赠送商品未站位数量
        give_product_qtty = 0

        for_value = 0

        # 计算赠送值
        give_pro_sum = 0
        if cur_index_off != -1:
            if bean.value_num == 0:
                bean.value_num = 1

            pro_ecode_num = list(set(productListA))
            give_pro_ecode_num = list(set(not_product_ListA))

            # 用来标记赠品数量
            if bean.value_num != 0 and bean.max_times == -1:
                # 若是买A赠A进入
                if len(pro_ecode_num) > len(give_pro_ecode_num):
                    return ab_a_wuxian(
                        productListA, not_product_ListA, bean, userInfo)
                return a_ab(productListA, not_product_ListA, bean, userInfo)
            # 当为翻倍值不为0and1
            if bean.max_times > 1:
                # 若是买A赠A进入
                if len(pro_ecode_num) > len(give_pro_ecode_num):
                    return ab_a_wuxian(
                        productListA, not_product_ListA, bean, userInfo)
                return a_ab(productListA, not_product_ListA, bean, userInfo)
            if bean.value_num == 1 or bean.max_times == 0 or bean.max_times == 1:
                if len(pro_ecode_num) > len(give_pro_ecode_num):
                    return ab_a_wuxian(
                        productListA, not_product_ListA, bean, userInfo)
                return a_ab(productListA, not_product_ListA, bean, userInfo)
        else:
            if not promotion_qtty_sum >= bean.value_num:
                return str(-1)
            # 总数 / 条件  等于倍数
            if bean.value_num == 0:
                bean.value_num += 1
            can_promotion_product = int(promotion_qtty_sum / bean.value_num)
            # 最大循环次数
            for_number = int(can_promotion_product * bean.value_num)
            for product in productListA:
                for seat in product.productSeatList:
                    if for_number == 0:
                        break
                    if seat.seat == False and seat.is_run_other_pro != False:
                        basics_one(seat, product, bean, userInfo)
                        for_number -= 1

            # 循环赠送列表中商品所有未站位的信息
            if not not_product_ListA:
                return {"id": bean.id, "qtty": give_number}
            give_product_qtty = get_product_sum(not_product_ListA)

            if give_product_qtty >= give_number:

                # 赠送数量
                for not_product in not_product_ListA:

                    for give_seat in not_product.productSeatList:
                        if give_number == 0:
                            break
                        if give_seat.seat == False and give_seat.is_run_other_pro != False and give_seat.is_discount == "y":
                            one_buy_product(give_seat, not_product, bean)
                            give_number -= 1
            else:
                for not_product in not_product_ListA:
                    if give_product_qtty == 0:
                        return {"id": bean.id, "qtty": give_number}

                    for give_seat in not_product.productSeatList:

                        if give_seat.seat == False and give_seat.is_run_other_pro != False and give_seat.is_discount == "y":
                            one_buy_product(give_seat, not_product, bean)
                            give_product_qtty -= 1

            return {"id": bean.id, "qtty": end_qtty}

    if bean.comp_symb_type == "g":

        if bean.give_value == 0:
            return str(-1)

        if not promotion_qtty_sum > bean.value_num:
            return str(-1)

        if kaiguan:
            return {"id": bean.id}
        sum_give_pro = 0

        # 计算可参与商品的总数量
        for product in productListA:
            for i in product.productSeatList:
                if i.seat == False and i.is_run_other_pro != False:
                    sum_give_pro += 1

        give_number = 0

        # 计算赠送值
        # 计算赠品未站位的数量
        give_sum = get_product_sum(not_product_ListA)

        # 计算赠送值

        if number == 1:

            if bean.value_num != 0:
                bean.value_num += 1

                if bean.max_times == -1:
                    give_number += int(promotion_qtty_sum //
                                       bean.value_num * bean.give_value)
                elif bean.max_times == 0 or bean.max_times == 1:
                    give_number += bean.give_value
                else:
                    max_fan = int(promotion_qtty_sum // (bean.value_num))
                    if max_fan == 0:
                        max_fan = 1
                    if max_fan < bean.max_times:
                        give_number = bean.give_value * max_fan
                    else:
                        give_number = give_number = bean.max_times * bean.give_value

            else:
                bean.value_num += 1
                bean.max_times = 1
                give_number = bean.give_value

        else:
            bean.max_times = 1
            give_number = bean.give_value
        # 判断值
        panduan_value = 0

        cur_index_off = -1
        # 判断是否是买A赠A
        # 判断是否是买A赠A
        for product in productListA:
            if product in not_product_ListA:
                cur_index_off -= 1

        # 完整执行完的买赠赠送数量
        end_qtty = copy.deepcopy(give_number)

        # 赠送商品未站位数量
        give_product_qtty = 0

        # 计算赠送值
        give_pro_sum = 0

        for_value = 0

        # 证明是买A赠A
        if cur_index_off != -1:

            pro_ecode_num = list(set(productListA))
            give_pro_ecode_num = list(set(not_product_ListA))

            if bean.value_num != 0 and bean.max_times == -1:
                # 若是买A赠A进入
                if len(pro_ecode_num) > len(give_pro_ecode_num):
                    return ab_a_wuxian(
                        productListA, not_product_ListA, bean, userInfo)
                return a_ab(productListA, not_product_ListA, bean, userInfo)
            # 当为翻倍值不为0and1
            if bean.max_times > 1:
                # 若是买A赠A进入
                if len(pro_ecode_num) > len(give_pro_ecode_num):
                    return ab_a_wuxian(
                        productListA, not_product_ListA, bean, userInfo)
                return a_ab(productListA, not_product_ListA, bean, userInfo)
            if bean.value_num == 1 or bean.max_times == 0 or bean.max_times == 1:
                if len(pro_ecode_num) > len(give_pro_ecode_num):
                    return ab_a_wuxian(
                        productListA, not_product_ListA, bean, userInfo)
                return a_ab(productListA, not_product_ListA, bean, userInfo)
        else:

            # 总数 / 条件  等于倍数
            if bean.value_num == 0:
                for_number = 1

            else:
                can_promotion_product = int(
                    promotion_qtty_sum / bean.value_num)
                # 最大循环次数
                for_number = int(can_promotion_product * bean.value_num)

            for product in productListA:
                for seat in product.productSeatList:
                    if for_number == 0:
                        break
                    if seat.seat == False and seat.is_run_other_pro != False:
                        basics_one(seat, product, bean, userInfo)
                        for_number -= 1

            # 循环赠送列表中商品所有未站位的信息
            if not not_product_ListA:
                return {"id": bean.id, "qtty": give_number}
            give_product_qtty = get_product_sum(not_product_ListA)

            if give_product_qtty >= give_number:

                # 赠送数量
                for not_product in not_product_ListA:

                    for give_seat in not_product.productSeatList:
                        if give_number == 0:
                            break
                        if give_seat.seat == False and give_seat.is_run_other_pro != False and give_seat.is_discount == "y":
                            one_buy_product(give_seat, not_product, bean)
                            give_number -= 1
            else:
                for not_product in not_product_ListA:
                    if give_product_qtty == 0:
                        return {"id": bean.id, "qtty": give_number}

                    for give_seat in not_product.productSeatList:

                        if give_seat.seat == False and give_seat.is_run_other_pro != False and give_seat.is_discount == "y":
                            one_buy_product(give_seat, not_product, bean)
                            give_product_qtty -= 1

            return {"id": bean.id, "qtty": end_qtty}


def sum_number_money(
        bean,
        userInfo,
        productListA,
        not_product_ListA,
        promotion_money_sum,
        condition,
        number,
        kaiguan):
    # 将赠品列表降序排序
    productListA = sorted(
        productListA,
        key=lambda i: getattr(
            i.productSeatList[0],
            condition),
        reverse=True)
    not_product_ListA = sorted(
        not_product_ListA,
        key=lambda i: getattr(
            i.productSeatList[0],
            condition))
    if bean.comp_symb_type == "ge" or bean.comp_symb_type == "e":

        if not promotion_money_sum >= bean.value_num:
            return str(-1)

        if bean.give_value == 0:
            return str(-1)
        if kaiguan:
            return {"id": bean.id}

        give_number = 0

        # 判断值
        panduan_value = 0

        cur_index_off = -1

        # 判断是否是买A赠A
        for product in productListA:
            if product in not_product_ListA:
                cur_index_off -= 1

        # 赠送商品未站位数量
        give_product_qtty = 0

        # 金额的最大循环次数
        # for_number = 0
        if number == 1:
            if bean.value_num != 0:
                if bean.max_times == -1:
                    give_number += int(promotion_money_sum //
                                       bean.value_num * bean.give_value)
                    # 算出当前最大多少倍
                    max_fan = int(promotion_money_sum // bean.value_num)
                    # 可参与商品的循环次数
                    for_number = max_fan * bean.value_num
                    # 如果比较值为0 或者不翻倍
                elif bean.value_num == 0 or bean.max_times == 0 or bean.max_times == 1:
                    for_number = bean.value_num
                    give_number += bean.give_value

                else:

                    # 如果翻倍
                    # 先计算当前翻倍值是多少
                    max_fan = int(promotion_money_sum // bean.value_num)
                    if max_fan == 0:
                        max_fan = 1
                    # 如果小于翻倍值
                    if max_fan <= bean.max_times:
                        # 赠送数量
                        give_number = bean.give_value * max_fan
                        for_number = bean.value_num * max_fan

                    else:
                        # 赠送数量与控制循环次数
                        give_number = bean.value_num * bean.give_value
                        for_number = bean.value_num * bean.max_times
            else:
                for_number = bean.value_num
                give_number += bean.give_value
                bean.max_times = 1
        else:
            bean.max_times = 1
            for_number = bean.value_num
            give_number += bean.give_value
        # 完整执行完的买赠赠送数量
        end_qtty = copy.deepcopy(give_number)

        if cur_index_off != -1:

            pro_ecode_num = list(set(productListA))
            give_pro_ecode_num = list(set(not_product_ListA))

            # # 先判断交集是否等于 2
            # if len(pro_ecode_num) + len(give_pro_ecode_num) >= 4:
            # return intersection(productListA, not_product_ListA, bean,
            # userInfo, condition)

            # 如果判断值为0 循环次数为1 赠送数量就是赠送数量
            if bean.value_num == 0 or bean.max_times == 0 or bean.max_times == 1:
                if len(give_pro_ecode_num) > len(pro_ecode_num):
                    return tow_give_one(
                        productListA, not_product_ListA, bean, userInfo, condition)
                return intersection_one(
                    productListA, not_product_ListA, bean, userInfo, condition)

            # 如果为无限翻倍
            if bean.max_times == -1:
                if len(give_pro_ecode_num) > len(pro_ecode_num):
                    return tow_give_max(
                        productListA, not_product_ListA, bean, userInfo, condition)
                return intersection_noe(
                    productListA, not_product_ListA, bean, userInfo, condition)

            # 若不为无限翻倍
            if bean.max_times > 1:
                if len(give_pro_ecode_num) > len(pro_ecode_num):
                    return tow_give_max(
                        productListA, not_product_ListA, bean, userInfo, condition)
                return intersection_noe(
                    productListA, not_product_ListA, bean, userInfo, condition)

        else:

            if bean.value_num == 0:
                for_number = getattr(
                    productListA[0].productSeatList[0], condition)
                bean.max_times = 1

            # 如果翻倍大于1
            if bean.max_times > 1:
                # 先计算当前翻倍数等于多少
                max_fan = int(promotion_money_sum // bean.value_num)
                if max_fan == 0:
                    max_fan = 1
                if max_fan <= bean.max_times:
                    # 若最大翻倍数小于当前翻倍之后的数量
                    give_number = bean.give_value * max_fan
                    # 如果小于那就翻倍数X比较值得出最大循环次数
                    for_number = max_fan * bean.value_num

                else:
                    # 若超过比较值 那么就按照当前最大倍数来算
                    give_number = bean.max_times * bean.give_value
                    for_number = bean.max_times * bean.value_num
                # 定义比较值
                max_pro = 0
                for product in productListA:
                    for seat in product.productSeatList:
                        if max_pro >= for_number:
                            break
                        if seat.seat == False and seat.is_run_other_pro != False:
                            basics_one(seat, product, bean, userInfo)
                            max_pro += getattr(seat, condition)
                # 循环赠送列表中商品所有未站位的信息
                if not not_product_ListA:
                    return {"id": bean.id, "qtty": give_number}
                give_product_qtty = get_product_sum(not_product_ListA)

                if give_product_qtty >= give_number:
                    pp = give_number

                    # 赠送数量
                    for not_product in not_product_ListA:

                        for give_seat in not_product.productSeatList:

                            if pp == 0:
                                break
                            if give_seat.seat == False and give_seat.is_run_other_pro != False and give_seat.is_discount == "y":
                                one_buy_product(give_seat, not_product, bean)
                                pp -= 1
                else:

                    for not_product in not_product_ListA:

                        for give_seat in not_product.productSeatList:

                            if give_seat.seat == False and give_seat.is_run_other_pro != False and give_seat.is_discount == "y":
                                one_buy_product(give_seat, not_product, bean)

                return {"id": bean.id, "qtty": give_number}

            max_pro = 0
            for product in productListA:
                for seat in product.productSeatList:
                    if max_pro >= for_number:
                        break
                    if seat.seat == False and seat.is_run_other_pro != False:
                        basics_one(seat, product, bean, userInfo)
                        max_pro += getattr(seat, condition)
            # 循环赠送列表中商品所有未站位的信息
            if not not_product_ListA:
                return {"id": bean.id, "qtty": give_number}

            give_product_qtty = get_product_sum(not_product_ListA)

            if give_product_qtty >= give_number:

                # 赠送数量
                for not_product in not_product_ListA:

                    for give_seat in not_product.productSeatList:

                        if give_number == 0:
                            break
                        if give_seat.seat == False and give_seat.is_run_other_pro != False and give_seat.is_discount == "y":
                            one_buy_product(give_seat, not_product, bean)
                            give_number -= 1
            else:

                for not_product in not_product_ListA:
                    if give_product_qtty == 0:
                        return {"id": bean.id, "qtty": give_number}

                    for give_seat in not_product.productSeatList:

                        if give_seat.seat == False and give_seat.is_run_other_pro != False and give_seat.is_discount == "y":
                            one_buy_product(give_seat, not_product, bean)
                            give_product_qtty -= 1

            return {"id": bean.id, "qtty": end_qtty}

    if bean.comp_symb_type == "g":
        if not promotion_money_sum > bean.value_num:
            return str(-1)

        if bean.give_value == 0:
            return str(-1)
        if kaiguan:
            return {"id": bean.id}
        give_number = 0

        # 判断值
        panduan_value = 0

        cur_index_off = -1
        # 判断是否是买A赠A
        for product in productListA:
            if product in not_product_ListA:
                cur_index_off -= 1
        for_number = 0
        # 赠送商品未站位数量
        give_product_qtty = 0

        if bean.give_value == 0:
            return
        # 金额的最大循环次数
        # for_number = 0
        if number == 1:
            if bean.value_num != 0:
                bean.value_num += 1
                if bean.max_times == -1:
                    give_number += int(promotion_money_sum //
                                       bean.value_num * bean.give_value)
                    # 算出当前最大多少倍
                    max_fan = int(promotion_money_sum // bean.value_num)
                    if max_fan == 0:
                        max_fan = 1
                    # 可参与赠品总金额
                    for_number = max_fan * bean.value_num

                elif bean.value_num == 0 or bean.max_times == 0 or bean.max_times == 1:
                    for_number = bean.value_num
                    give_number += bean.give_value

                else:

                    # 先计算当前翻倍数等于多少
                    max_fan = int(promotion_money_sum // bean.value_num)
                    if max_fan == 0:
                        max_fan = 1
                    if max_fan <= bean.max_times:
                        # 若最大翻倍数小于当前翻倍之后的数量
                        give_number = bean.give_value * max_fan
                        # 如果小于那就翻倍数X比较值得出最大循环次数
                        for_number = max_fan * bean.value_num

                    else:
                        # 若超过比较值 那么就按照当前最大倍数来算
                        give_number = bean.max_times * bean.give_value
                        for_number = bean.max_times * bean.value_num
            else:
                for_number = getattr(
                    productListA[0].productSeatList[0], condition)
                give_number += bean.give_value
                bean.max_times = 1

        else:
            bean.max_times = 1
            for_number = bean.value_num
            give_number += bean.give_value
        # 完整执行完的买赠赠送数量
        end_qtty = copy.deepcopy(give_number)

        if cur_index_off != -1:

            pro_ecode_num = list(set(productListA))
            give_pro_ecode_num = list(set(not_product_ListA))
            # # 先判断交集是否等于 2
            # if len(pro_ecode_num) + len(give_pro_ecode_num) >= 4:
            # return intersection(productListA, not_product_ListA, bean,
            # userInfo, condition)

            # 如果判断值为0 循环次数为1 赠送数量就是赠送数量
            if bean.value_num == 0 or bean.max_times == 0 or bean.max_times == 1:
                if len(give_pro_ecode_num) > len(pro_ecode_num):
                    return tow_give_one(
                        productListA, not_product_ListA, bean, userInfo, condition)
                return intersection_one(
                    productListA, not_product_ListA, bean, userInfo, condition)

            # 如果为无限翻倍
            if bean.max_times == -1:
                if len(give_pro_ecode_num) > len(pro_ecode_num):
                    return tow_give_max(
                        productListA, not_product_ListA, bean, userInfo, condition)
                return intersection_noe(
                    productListA, not_product_ListA, bean, userInfo, condition)

            # 若不为无限翻倍
            if bean.max_times > 1:
                if len(give_pro_ecode_num) > len(pro_ecode_num):
                    return tow_give_max(
                        productListA, not_product_ListA, bean, userInfo, condition)
                return intersection_noe(
                    productListA, not_product_ListA, bean, userInfo, condition)

        else:
            max_pro = 0
            for product in productListA:
                for seat in product.productSeatList:
                    if max_pro >= for_number:
                        break
                    if seat.seat == False and seat.is_run_other_pro != False:
                        basics_one(seat, product, bean, userInfo)
                        max_pro += getattr(seat, condition)
            # 循环赠送列表中商品所有未站位的信息
            if not not_product_ListA:
                return {"id": bean.id, "qtty": give_number}
            give_product_qtty = get_product_sum(not_product_ListA)

            if give_product_qtty >= give_number:

                # 赠送数量
                for not_product in not_product_ListA:

                    for give_seat in not_product.productSeatList:

                        if give_number == 0:
                            break
                        if give_seat.seat == False and give_seat.is_run_other_pro != False and give_seat.is_discount == "y":
                            one_buy_product(give_seat, not_product, bean)
                            give_number -= 1
            else:
                for not_product in not_product_ListA:
                    if give_product_qtty == 0:
                        return {"id": bean.id, "qtty": give_number}

                    for give_seat in not_product.productSeatList:

                        if give_seat.seat == False and give_seat.is_run_other_pro != False and give_seat.is_discount == "y":
                            one_buy_product(give_seat, not_product, bean)
                            give_product_qtty -= 1

            return {"id": bean.id, "qtty": end_qtty}


def ab_ba(productListA, not_product_ListA, bean, userInfo):
    if bean.value_num == 0:
        value_num = 1

    if bean.max_times == 0:
        bean.max_times = 1

    cour_max = 0
    # 获取可以参加商品的总数

    give_number = 0
    panduanzhi_pro = -1
    for product in productListA:
        for give in not_product_ListA:

            # 获取当前可以参加活动的总数

            if product.ecode.lower() == give.ecode.lower():
                if hasattr(product, 'T'):
                    continue
                productListA[productListA.index(product)], productListA[panduanzhi_pro] = productListA[panduanzhi_pro], \
                    productListA[
                    productListA.index(
                        product)]
                # 表示已经交换过下标 所以不需要再次交换
                product.T = True
                panduanzhi_pro -= 1
    # 判断值
    panduanzhi_give = -1
    for product in productListA:
        for give in not_product_ListA:

            # 获取当前可以参加活动的总数

            if product.ecode.lower() == give.ecode.lower():
                if hasattr(give, 'F'):
                    continue
                not_product_ListA[not_product_ListA.index(give)], not_product_ListA[panduanzhi_give] = \
                    not_product_ListA[panduanzhi_give], not_product_ListA[not_product_ListA.index(give)]
                panduanzhi_give -= 1
                give.F = True

    while True:
        if cour_max == bean.max_times:
            return {"id": bean.id, "qtty": give_number}

        # 先判断最大商品数量是否满足
        cur_pro_sum = get_product_sum(productListA)
        # 如果当前活动剩余商品可以参加活动
        if not cur_pro_sum >= bean.value_num:
            return {"id": bean.id, "qtty": give_number}
        # 循环比较值
        p = bean.value_num

        # 循环更改当前商品站位信息(比较值)
        for product in productListA:
            for seat in product.productSeatList:
                if p == 0:
                    break
                if seat.seat == False and seat.is_run_other_pro != False:
                    basics_one(seat, product, bean, userInfo)
                    p -= 1

        # 获取当前赠品所剩数量
        cur_give_pro_sum = get_product_sum(not_product_ListA)

        # 如果当前赠品所剩数量不满足则返回
        if cur_give_pro_sum == 0:
            give_number += bean.give_value
            return {"id": bean.id, "qtty": give_number}

        if not cur_give_pro_sum >= bean.give_value:
            # 循环增改剩余赠品
            for give_product in not_product_ListA:
                for give in give_product.productSeatList:

                    if give.seat == False and give.is_run_other_pro != False and give.is_discount == "y":
                        one_buy_product(give, give_product, bean)

            give_number += bean.give_value

        b = bean.give_value
        # 获取当前赠品的剩余数量
        for give_product in not_product_ListA:
            # 循环增改剩余赠品
            for give in give_product.productSeatList:
                if b == 0:
                    break
                if give.seat == False and give.is_run_other_pro != False and give.is_discount == "y":
                    one_buy_product(give, give_product, bean)
                    b -= 1
        give_number += bean.give_value

        cour_max += 1


def ab_a_wuxian(productListA, not_product_ListA, bean, userInfo):
    """
    买AB 送A 算法
    :param productListA:
    :param not_product_ListA:
    :param bean:
    :param userInfo:
    :return:
    """

    if bean.value_num == 0:
        value_num = 1

    if bean.max_times == 0:
        bean.max_times = 1

    # 取出不在赠送列表的商品
    pro_one = []

    # 赠送总数量
    give_number = 0
    if len(productListA) > 1:
        for product in productListA:
            if product not in not_product_ListA:
                pro_one.append(product)

    # 获取不在赠送列表的总数
    result = get_product_sum(pro_one)

    # 如果商品和赠品相同那么值为0
    if productListA == not_product_ListA:
        result = 0
    pro_one = sorted(
        pro_one,
        key=lambda i: i.productSeatList[0].amt_list,
        reverse=True)
    result_number = 0
    # 定义游标
    cursor = 0
    # 赠送总量
    give_number = 0

    give_sum = 0
    # 排序
    productListA = sort_ab_a_number(productListA, not_product_ListA)
    not_product_ListA = sorted(not_product_ListA,
                               key=lambda i: i.productSeatList[0].amt_list)
    productListA = sorted(
        productListA,
        key=lambda i: i.productSeatList[0].amt_list,
        reverse=True)

    # 如果不为无限翻倍
    if bean.max_times != -1:

        # 先看当前数量是否满足最小条件
        if not result >= bean.value_num:
            # 若小于比较值从赠品列表中抽取
            n = change_pro_number(pro_one, result, bean, userInfo)
            # 让总数量加上当前金额
            result_number += n
            # 此时从赠品列表抽取满足最小条件数量
            number = bean.value_num - result_number
            # 再次进入更改商品站位信息
            not_product_ListA = sorted(
                not_product_ListA,
                key=lambda i: i.productSeatList[0].amt_list,
                reverse=True)

            n = change_pro_number(not_product_ListA, number, bean, userInfo)
            result_number += n
            # 此时已经满足比较值计算赠送数量
            # 获取赠品总数量
            result_numb_giv = get_product_sum(not_product_ListA)
            # 看赠品数量是否满足当前最小条件
            if not result_numb_giv >= bean.give_value:
                give_sum = 0
                change_give_product(not_product_ListA, bean, give_sum)
                give_number = bean.give_value
                return {"id": bean.id, "qtty": give_number}
            # 如果最大赠送值已经超过那就只改最大赠送值
            give_sum = bean.give_value
            not_product_ListA = sorted(
                not_product_ListA,
                key=lambda i: i.productSeatList[0].amt_list)

            change_give_product(not_product_ListA, bean, give_sum)
            # 控制翻倍游标加1
            cursor += 1
            # 此时进入死循环控制所有商品
            while True:
                if cursor == bean.max_times:
                    # 如果当前倍数已经达到最大限度
                    give_number = int(cursor * bean.give_value)
                    return {"id": bean.id, "qtty": give_number}
                # 获取有交集数量
                result_numb_giv = get_product_sum(not_product_ListA)
                # 如果交集数量小于最小翻倍值
                if not result_numb_giv >= bean.value_num:
                    # 如果当前倍数已经达到最大限度
                    give_number = int(cursor * bean.give_value)
                    return {"id": bean.id, "qtty": give_number}
                not_product_ListA = sorted(
                    not_product_ListA,
                    key=lambda i: i.productSeatList[0].amt_list,
                    reverse=True)

                # 此时就是满足 更改商品信息
                change_pro_number(productListA, bean.value_num, bean, userInfo)
                # 再次获取有交集剩余商品
                result_numb_giv = get_product_sum(not_product_ListA)
                # 看看是否还满足当前赠送值
                if not result_numb_giv >= bean.give_value:
                    give_sum = 0
                    change_give_product(not_product_ListA, bean, give_sum)
                    give_number = bean.give_value * (cursor + 1)
                    return {"id": bean.id, "qtty": give_number}

                # 如果最大赠送值已经超过那就只改最大赠送值
                give_sum = bean.give_value
                not_product_ListA = sorted(
                    not_product_ListA,
                    key=lambda i: i.productSeatList[0].amt_list)

                change_give_product(not_product_ListA, bean, give_sum)
                # 控制翻倍游标加1
                cursor += 1

        # 若此时不满足最大翻倍次数
        if not result >= bean.value_num * bean.max_times:
            # 先看看当前商品可以翻几倍
            while True:
                # 更改最小比较值的数量
                change_pro_number(pro_one, bean.value_num, bean, userInfo)
                result_numb_giv = get_product_sum(not_product_ListA)
                # 看赠品数量是否满足当前最小条件
                if not result_numb_giv >= bean.give_value:
                    # 游标加1
                    cursor += 1

                    give_sum = 0
                    change_give_product(not_product_ListA, bean, give_sum)
                    # 如果此时赠品已经识别完看还剩几件可以参与活动
                    while True:
                        result_pro = get_product_sum(productListA)
                        # 若剩余商品不满足就退出
                        # 如果商品最大翻倍值已经满足也退出该循环
                        if cursor == bean.max_times:
                            break
                        if not result_pro >= bean.value_num:
                            break
                        # 更改商品站位信息
                        change_pro_number(
                            pro_one, bean.value_num, bean, userInfo)
                        # 游标加1
                        cursor += 1

                    if cursor != 0:
                        give_number = bean.give_value * cursor
                    else:
                        give_number = bean.give_value
                    return {"id": bean.id, "qtty": give_number}

                # 如果最大赠送值已经超过那就只改最大赠送值
                give_sum = bean.give_value
                not_product_ListA = sorted(
                    not_product_ListA,
                    key=lambda i: i.productSeatList[0].amt_list)
                change_give_product(not_product_ListA, bean, give_sum)
                # 控制翻倍游标加1
                cursor += 1

                if not get_product_sum(pro_one) >= bean.value_num:
                    # 若小于比较值从赠品列表中抽取
                    n = change_pro_number(pro_one, result, bean, userInfo)
                    # 让总数量加上当前金额
                    result_number += n
                    # 此时从赠品列表抽取满足最小条件数量
                    number = bean.value_num - result_number
                    # 获取有交集数量
                    result_numb_giv = get_product_sum(not_product_ListA)
                    # 如果交集数量小于最小翻倍值
                    if not result_numb_giv >= bean.value_num:
                        # 如果当前倍数已经达到最大限度
                        give_number = int(cursor * bean.give_value)
                        return {"id": bean.id, "qtty": give_number}

                    not_product_ListA = sorted(
                        not_product_ListA,
                        key=lambda i: i.productSeatList[0].amt_list,
                        reverse=True)
                    # 再次进入更改商品站位信息
                    n = change_pro_number(
                        not_product_ListA, number, bean, userInfo)
                    result_number += n
                    # 此时已经满足比较值计算赠送数量
                    # 获取赠品总数量
                    result_numb_giv = get_product_sum(not_product_ListA)
                    # 看赠品数量是否满足当前最小条件
                    if not result_numb_giv > bean.give_value:
                        give_sum = 0
                        change_give_product(not_product_ListA, bean, give_sum)
                        give_number = bean.give_value * (cursor + 1)
                        return {"id": bean.id, "qtty": give_number}
                    # 如果最大赠送值已经超过那就只改最大赠送值
                    give_sum = bean.give_value
                    not_product_ListA = sorted(
                        not_product_ListA, key=lambda i: i.productSeatList[0].amt_list)

                    change_give_product(not_product_ListA, bean, give_sum)
                    # 控制翻倍游标加1
                    cursor += 1
                    # 此时进入死循环控制所有商品
                    while True:
                        if cursor == bean.max_times:
                            # 如果当前倍数已经达到最大限度
                            give_number = int(cursor * bean.give_value)
                            return {"id": bean.id, "qtty": give_number}
                        # 获取有交集数量
                        result_numb_giv = get_product_sum(not_product_ListA)
                        # 如果交集数量小于最小翻倍值
                        if not result_numb_giv >= bean.value_num:
                            # 如果当前倍数已经达到最大限度
                            give_number = int(cursor * bean.give_value)
                            return {"id": bean.id, "qtty": give_number}
                        # 此时就是满足 更改商品信息
                        not_product_ListA = sorted(
                            not_product_ListA, key=lambda i: i.productSeatList[0].amt_list, reverse=True)
                        change_pro_number(
                            productListA, bean.value_num, bean, userInfo)
                        # 再次获取有交集剩余商品
                        result_numb_giv = get_product_sum(not_product_ListA)
                        # 看看是否还满足当前赠送值
                        if not result_numb_giv > bean.give_value:
                            give_sum = 0
                            change_give_product(
                                not_product_ListA, bean, give_sum)
                            give_number = bean.give_value * (cursor + 1)
                            return {"id": bean.id, "qtty": give_number}

                        # 如果最大赠送值已经超过那就只改最大赠送值
                        give_sum = bean.give_value
                        not_product_ListA = sorted(
                            not_product_ListA, key=lambda i: i.productSeatList[0].amt_list)
                        change_give_product(not_product_ListA, bean, give_sum)
                        # 控制翻倍游标加1
                        cursor += 1

        # 可以走到这说明已经满足了.直接改就好
        change_pro_number(
            pro_one,
            bean.value_num *
            bean.max_times,
            bean,
            userInfo)

        # 看下剩余赠品是否满足
        result_numb_giv = get_product_sum(not_product_ListA)
        # 看赠品数量是否满足当前最小条件
        if not result_numb_giv > bean.give_value:
            give_sum = 0
            change_give_product(not_product_ListA, bean, give_sum)
            give_number = bean.give_value * bean.max_times
            return {"id": bean.id, "qtty": give_number}

        give_number = bean.give_value * bean.max_times
        change_give_product(not_product_ListA, bean, give_number)
        return {"id": bean.id, "qtty": give_number}

    # 现在就是无限翻倍了
    # 先看当前数量是否满足最小条件
    if not result >= bean.value_num:
        # 若小于比较值从赠品列表中抽取
        n = change_pro_number(pro_one, result, bean, userInfo)
        # 让总数量加上当前金额
        result_number += n
        # 此时从赠品列表抽取满足最小条件数量
        number = bean.value_num - result_number
        # 若有交集不大于当前需要值也返回
        result_numb_giv = get_product_sum(not_product_ListA)
        if not result_numb_giv >= number:
            if cursor != 0:
                give_number = bean.give_value * (cursor + 1)
            else:
                give_number = bean.give_value
            return {"id": bean.id, "qtty": give_number}
        # 再次进入更改商品站位信息
        not_product_ListA = sorted(
            not_product_ListA,
            key=lambda i: i.productSeatList[0].amt_list,
            reverse=True)

        n = change_pro_number(not_product_ListA, number, bean, userInfo)
        result_number += n
        # 此时已经满足比较值计算赠送数量
        # 获取赠品总数量
        result_numb_giv = get_product_sum(not_product_ListA)
        # 看赠品数量是否满足当前最小条件
        if not result_numb_giv > bean.give_value:
            give_sum = 0
            change_give_product(not_product_ListA, bean, give_sum)
            give_number = bean.give_value
            return {"id": bean.id, "qtty": give_number}
        # 如果最大赠送值已经超过那就只改最大赠送值
        give_sum = bean.give_value
        not_product_ListA = sorted(
            not_product_ListA,
            key=lambda i: i.productSeatList[0].amt_list)

        change_give_product(not_product_ListA, bean, give_sum)
        # 控制翻倍游标加1
        cursor += 1
        # 此时进入死循环控制所有商品
        while True:

            # 获取有交集数量
            result_numb_giv = get_product_sum(not_product_ListA)
            # 如果交集数量小于最小翻倍值
            if not result_numb_giv >= bean.value_num:
                # 如果当前倍数已经达到最大限度
                give_number = int(cursor * bean.give_value)
                return {"id": bean.id, "qtty": give_number}
            not_product_ListA = sorted(
                not_product_ListA,
                key=lambda i: i.productSeatList[0].amt_list,
                reverse=True)

            # 此时就是满足 更改商品信息
            change_pro_number(productListA, bean.value_num, bean, userInfo)
            # 再次获取有交集剩余商品
            result_numb_giv = get_product_sum(not_product_ListA)
            # 看看是否还满足当前赠送值
            if not result_numb_giv >= bean.give_value:
                give_sum = 0
                change_give_product(not_product_ListA, bean, give_sum)
                give_number = bean.give_value * (cursor + 1)
                return {"id": bean.id, "qtty": give_number}

            # 如果最大赠送值已经超过那就只改最大赠送值
            give_sum = bean.give_value
            not_product_ListA = sorted(
                not_product_ListA,
                key=lambda i: i.productSeatList[0].amt_list)

            change_give_product(not_product_ListA, bean, give_sum)
            # 控制翻倍游标加1
            cursor += 1

    while True:

        # 更改最小比较值的数量
        change_pro_number(pro_one, bean.value_num, bean, userInfo)
        result_numb_giv = get_product_sum(not_product_ListA)
        # 看赠品数量是否满足当前最小条件
        if not result_numb_giv >= bean.give_value:
            # 游标加1
            cursor += 1

            give_sum = 0
            change_give_product(not_product_ListA, bean, give_sum)
            # 如果此时赠品已经识别完看还剩几件可以参与活动
            while True:
                result_pro = get_product_sum(productListA)
                # 若剩余商品不满足就退出
                if not result_pro >= bean.value_num:
                    break
                # 更改商品站位信息
                change_pro_number(pro_one, bean.value_num, bean, userInfo)
                # 游标加1
                cursor += 1

            if cursor != 0:
                give_number = bean.give_value * cursor
            else:
                give_number = bean.give_value
            return {"id": bean.id, "qtty": give_number}
        # 如果最大赠送值已经超过那就只改最大赠送值
        give_sum = bean.give_value
        not_product_ListA = sorted(
            not_product_ListA,
            key=lambda i: i.productSeatList[0].amt_list)
        change_give_product(not_product_ListA, bean, give_sum)
        cursor += 1
        if not get_product_sum(pro_one) >= bean.value_num:
            # 若小于比较值从赠品列表中抽取
            n = change_pro_number(pro_one, result, bean, userInfo)
            # 让总数量加上当前金额
            result_number += n
            # 此时从赠品列表抽取满足最小条件数量
            number = bean.value_num - result_number
            # 计算商品数量如果不足直接返回
            result_numb_giv = get_product_sum(not_product_ListA)
            if not result_numb_giv >= number:
                if cursor != 0:
                    give_number = bean.give_value * cursor
                else:
                    give_number = bean.give_value
                return {"id": bean.id, "qtty": give_number}

            not_product_ListA = sorted(
                not_product_ListA,
                key=lambda i: i.productSeatList[0].amt_list,
                reverse=True)

            # 再次进入更改商品站位信息
            n = change_pro_number(not_product_ListA, number, bean, userInfo)
            result_number += n
            # 此时已经满足比较值计算赠送数量
            # 获取赠品总数量
            result_numb_giv = get_product_sum(not_product_ListA)
            # 看赠品数量是否满足当前最小条件
            if not result_numb_giv > bean.give_value:
                give_sum = 0
                change_give_product(not_product_ListA, bean, give_sum)
                if cursor != 0:
                    give_number = bean.give_value * (cursor + 1)
                else:
                    give_number = bean.give_value
                return {"id": bean.id, "qtty": give_number}
            # 如果最大赠送值已经超过那就只改最大赠送值
            give_sum = bean.give_value
            not_product_ListA = sorted(
                not_product_ListA,
                key=lambda i: i.productSeatList[0].amt_list)

            change_give_product(not_product_ListA, bean, give_sum)
            # 控制翻倍游标加1
            cursor += 1
            # 此时进入死循环控制所有商品
            while True:

                # 获取有交集数量
                result_numb_giv = get_product_sum(not_product_ListA)
                # 如果交集数量小于最小翻倍值
                if not result_numb_giv >= bean.value_num:
                    # 如果当前倍数已经达到最大限度
                    give_number = int(cursor * bean.give_value)
                    return {"id": bean.id, "qtty": give_number}
                # 此时就是满足 更改商品信息
                not_product_ListA = sorted(
                    not_product_ListA,
                    key=lambda i: i.productSeatList[0].amt_list,
                    reverse=True)
                change_pro_number(productListA, bean.value_num, bean, userInfo)
                # 再次获取有交集剩余商品
                result_numb_giv = get_product_sum(not_product_ListA)
                # 看看是否还满足当前赠送值
                if not result_numb_giv > bean.give_value:
                    give_sum = 0
                    change_give_product(not_product_ListA, bean, give_sum)
                    give_number = bean.give_value * (cursor + 1)
                    return {"id": bean.id, "qtty": give_number}

                # 如果最大赠送值已经超过那就只改最大赠送值
                give_sum = bean.give_value
                not_product_ListA = sorted(
                    not_product_ListA,
                    key=lambda i: i.productSeatList[0].amt_list)
                change_give_product(not_product_ListA, bean, give_sum)
                # 控制翻倍游标加1
                cursor += 1


def a_ab(productListA, not_product_ListA, bean, userInfo):
    """
    买A送AB算法
    :param productListA:
    :param not_product_ListA:
    :param bean:
    :param userInfo:
    :return:
    """

    if bean.value_num == 0:
        value_num = 1

    if bean.max_times == 0:
        bean.max_times = 1

    # 定义游标
    cursor = 0
    # 赠送总量
    give_number = 0

    while True:
        # 如果当前不是无限翻倍
        if bean.max_times != -1:
            # 如果下表 与翻倍相等返回结果
            if cursor == bean.max_times:
                return {"id": bean.id, "qtty": give_number}
        # 获取可以参加活动的总数
        productListA = sorted(
            productListA,
            key=lambda i: i.productSeatList[0].amt_list,
            reverse=True)
        result = get_product_sum(productListA)
        # 看是否满足当前活动
        if result >= bean.value_num:
            # 循环更改站位信息
            for_pro = bean.value_num
            # 若满足就更改商品站位信息
            # 循环更改当前商品站位信息(比较值)
            for product in productListA:
                for seat in product.productSeatList:
                    if for_pro == 0:
                        break
                    if seat.seat == False and seat.is_run_other_pro != False:
                        basics_one(seat, product, bean, userInfo)
                        for_pro -= 1
            # 查看当前赠品是否满足
            # 赠送总数加上当前赠送数量
            give_number += bean.give_value

            # 计算赠品信息
            result_give = get_product_sum(not_product_ListA)
            # 若赠送数量为0 就直接返回

            if result_give == 0:
                return {"id": bean.id, "qtty": give_number}
            not_product_ListA = sorted(
                not_product_ListA,
                key=lambda i: i.productSeatList[0].amt_list)
            # 如果剩余数量满足赠送数量更改赠品信息
            if result_give >= bean.give_value:
                result_give_pro = bean.give_value
                # 循环更改赠品信息
                for give_product in not_product_ListA:
                    # 循环增改剩余赠品
                    for give in give_product.productSeatList:
                        if result_give_pro == 0:
                            break
                        if give.seat == False and give.is_run_other_pro != False and give.is_discount == "y":
                            one_buy_product(give, give_product, bean)
                            result_give_pro -= 1
                # 翻倍比较值 += 1
                cursor += 1
            else:
                # 否则就是不满足全部更改然后返回即可

                for give_product in not_product_ListA:
                    # 循环增改剩余赠品
                    for give in give_product.productSeatList:

                        if give.seat == False and give.is_run_other_pro != False and give.is_discount == "y":
                            one_buy_product(give, give_product, bean)

                return {"id": bean.id, "qtty": give_number}

        else:
            return {"id": bean.id, "qtty": give_number}


def ab_ab(productListA, not_product_ListA, bean, userInfo):
    """
    交集大于2的算法
    :param productListA:
    :param not_product_ListA:
    :param bean:
    :param userInfo:
    :return:
    """
    # 首先交集大于2的时候就不翻倍了.
    # 排序优先更改价格贵的信息

    bean.max_times = 1

    if bean.value_num == 0:
        value_num = 1

    give_number = 0

    # 排序可以参加活动的列表
    productListA = sorted(
        productListA,
        key=lambda i: i.productSeatList.amt_list)

    # 取出当前的比较值
    result_value = bean.value_num

    # 循环更改商品信息
    for product in productListA:
        for seat in product.productSeatList:
            if result_value == 0:
                break
            if seat.seat == False and seat.is_run_other_pro != False:
                basics_one(seat, product, bean, userInfo)
    # 更改赠品信息
    give_number += bean.give_value

    # 计算赠品信息
    result_give = get_product_sum(not_product_ListA)
    # 若赠送数量为0 就直接返回

    if result_give == 0:
        return {"id": bean.id, "qtty": give_number}

    # 如果剩余数量满足赠送数量更改赠品信息
    if result_give >= bean.give_value:
        result_give_pro = bean.give_value
        # 循环更改赠品信息
        for give_product in not_product_ListA:
            # 循环增改剩余赠品
            for give in give_product.productSeatList:
                if result_give_pro == 0:
                    break
                if give.seat == False and give.is_run_other_pro != False and give.is_discount == "y":
                    one_buy_product(give, give_product, bean)
                    result_give_pro -= 1

    else:
        # 否则就是不满足全部更改然后返回即可

        for give_product in not_product_ListA:
            # 循环增改剩余赠品
            for give in give_product.productSeatList:

                if give.seat == False and give.is_run_other_pro != False and give.is_discount == "y":
                    one_buy_product(give, give_product, bean)

        return {"id": bean.id, "qtty": give_number}


def intersection(productListA, not_product_ListA, bean, userInfo, condition):
    """

    :param productListA: 可参加活动列表
    :param not_product_ListA:  赠送列表
    :param bean: 活动
    :param userInfo: 会员
    :param condition 判断值
    :return:
    """
    if bean.value_num == 0:
        bean.value_num = 1

    # 1 将翻倍设置为 1
    bean.max_times = 1
    # 2 先排序降序
    productListA = sorted(
        productListA,
        key=lambda x: x.productSeatList[0].amt_list,
        reverse=True)

    # 循环更改站位信息
    # 定义容器
    result = 0
    for product in productListA:
        if result >= bean.value_num:
            break
        for seat in product.productSeatList:
            if seat.seat == False and seat.is_run_other_pro != False:
                basics_one(seat, product, bean, userInfo)
                result += getattr(seat, condition)
    # 最终赠送数量
    give_number = 0
    give_number = bean.give_value
    # 查看当前赠送列表当中可还满足数量
    result_give = get_product_sum(not_product_ListA)
    # 如果剩余数量大于赠送商品
    if result_give >= bean.give_value:
        result_give = bean.give_value

        for not_product in not_product_ListA:
            for not_seat in not_product.productSeatList:
                if result_give == 0:
                    return {"id": bean.id, "qtty": give_number}
                if not_seat.seat == False and not_seat.is_run_other_pro != False and not_seat.is_discount == "y":
                    one_buy_product(not_seat, not_product, bean)
    else:

        for not_product in not_product_ListA:
            for not_seat in not_product.productSeatList:

                if not_seat.seat == False and not_seat.is_run_other_pro != False and not_seat.is_discount == "y":
                    one_buy_product(not_seat, not_product, bean)
        return {"id": bean.id, "qtty": give_number}


def intersection_noe(
        productListA,
        not_product_ListA,
        bean,
        userInfo,
        condition):
    """

    :param productListA:  可参与活动商品
    :param not_product_ListA:  赠品列表
    :param bean: 活动
    :param userInfo: 会员
    :param condition: 条件
    :return:
    """
    money_linshi = 0
    if bean.value_num == 0:
        bean.value_num = 1

    pro_one = []

    # 赠送总数量
    give_number = 0

    give_sum = 0

    cursor_give_sum = 0

    if len(productListA) > 1:
        for product in productListA:
            if product not in not_product_ListA:
                pro_one.append(product)

    else:
        pro_one = productListA

    # 重新排序假如现在是买AB送 A  那就是BBBAAA
    productListA = sort_pro(condition, productListA, not_product_ListA)

    result_moeny = 0
    # 获取当前不是赠品的总金额
    result_pro = get_money_sum(pro_one, condition)

    kaiguan = False

    # 定义游标
    crs_max = 0
    if productListA == not_product_ListA:
        result_pro = 0

    # 计算最大翻倍金额
    if bean.max_times != -1:
        # 计算最大翻倍数量
        max_money = bean.max_times * bean.value_num
        # 若当前不在赠品的商品的金额已经超过最大翻倍值

        if result_pro > max_money:
            # 此时更改站位信息
            change_product(productListA, bean, userInfo, condition, max_money)

            # 获取赠品总数量
            result_numb_giv = get_product_sum(not_product_ListA)

            not_product_ListA = sorted(
                not_product_ListA, key=lambda i: getattr(
                    i.productSeatList[0], condition))
            # 判断赠品数量是否满足
            if not result_numb_giv >= (bean.give_value * bean.max_times):
                give_sum = 0
                change_give_product(not_product_ListA, bean, give_sum)
                give_number = bean.give_value * bean.max_times
                return {"id": bean.id, "qtty": give_number}
            # 如果最大赠送值已经超过那就只改最大赠送值
            give_sum = bean.give_value * bean.max_times
            give_number = int(bean.give_value * bean.max_times)
            change_give_product(not_product_ListA, bean, give_sum)
            return {"id": bean.id, "qtty": give_number}

        # 如果当前总金额不大于最小倍数
        if not result_pro > bean.value_num:

            while True:
                # 如果大于就终止循环
                if result_moeny >= max_money:
                    give_number = int(
                        max_money // bean.value_num * bean.give_value)
                    return {"id": bean.id, "qtty": give_number}

                if result_pro != 0 and productListA != not_product_ListA:
                    # 先更改不在赠品中的未满足站位信息
                    result_pro = change_product(
                        pro_one, bean, userInfo, condition, result_pro)
                    if result_pro == 0:
                        kaiguan = True
                    result_moeny += result_pro
                else:
                    result_pro = 0
                # 若不在赠品列表中的商品不满足 那就从赠品列表当中抽取

                not_product_ListA = sorted(
                    not_product_ListA, key=lambda i: getattr(
                        i.productSeatList[0], condition), reverse=True)
                result_cr = result_moeny

                for give in not_product_ListA:
                    for give_seat in give.productSeatList:
                        # 如果当前金额已经大于最大翻倍金额
                        if result_cr >= max_money:
                            break
                        if result_cr // bean.value_num > result_moeny // bean.value_num:
                            break
                        if not give_seat.seat:
                            result_pro += getattr(give_seat, condition)
                            result_cr += getattr(give_seat, condition)
                # 如果全部加完还没增加一倍那就返回吧.  多余的也没用
                if not ((result_moeny + result_pro) //
                        bean.value_num) > result_moeny // bean.value_num:
                    give_number = int(
                        result_moeny // bean.value_num * bean.give_value)
                    return {"id": bean.id, "qtty": give_number}

                if productListA == not_product_ListA:
                    result_int = result_pro

                else:
                    if not kaiguan:
                        result_int = result_pro - result_moeny
                    else:
                        result_int = result_pro

                b = change_product(
                    not_product_ListA,
                    bean,
                    userInfo,
                    condition,
                    result_int)

                result_moeny += b
                # 获取赠品总数量
                result_numb_giv = get_product_sum(not_product_ListA)
                not_product_ListA = sorted(
                    not_product_ListA, key=lambda i: getattr(
                        i.productSeatList[0], condition))
                # 此时计算赠送数量和更改商品站位信息
                # 如果赠送数量不大于当前剩余数量
                if not result_numb_giv >= (
                        result_moeny // bean.value_num * bean.give_value) - cursor_give_sum:

                    # 价钱从小到大排序
                    if result_moeny // bean.value_num * \
                            bean.give_value > max_money // bean.value_num * bean.give_value:

                        give_sum = int(
                            max_money // bean.value_num * bean.give_value)
                        change_give_product(not_product_ListA, bean, give_sum)

                        give_number = int(
                            max_money // bean.value_num * bean.give_value)
                        return {"id": bean.id, "qtty": give_number}
                    else:
                        give_sum = 0
                        change_give_product(not_product_ListA, bean, give_sum)

                        give_number = int(
                            result_moeny // bean.value_num * bean.give_value)
                        return {"id": bean.id, "qtty": give_number}

                # 如果当前赠送数量已经超过最大赠送数量
                if cursor_give_sum >= (bean.max_times * bean.give_value):
                    give_number = int(bean.max_times * bean.give_value)
                    change_give_product(not_product_ListA, bean, give_number)
                    return {"id": bean.id, "qtty": give_number}

                if result_moeny // bean.value_num * \
                        bean.give_value > max_money // bean.value_num * bean.give_value:

                    give_sum = int(
                        max_money // bean.value_num * bean.give_value)
                else:
                    give_sum = int(
                        result_moeny //
                        bean.value_num *
                        bean.give_value)

                # 若第一次循环进来
                give_sum -= cursor_give_sum
                # 更改站位信息
                change_give_product(not_product_ListA, bean, give_sum)
                # 此时在用游标加上此次赠送数量
                cursor_give_sum += give_sum

        # 能走到这说明当前金额满足条件但不满足最大翻倍次数
        # 先更改此时不在赠品的站位信息
        p = change_product(pro_one, bean, userInfo, condition, max_money)
        # 在用总金额加上
        result_moeny += p

        # 此时看赠送数量又是多少
        # 获取赠品总数量
        result_numb_giv = get_product_sum(not_product_ListA)

        # 排序
        not_product_ListA = sorted(
            not_product_ListA, key=lambda i: getattr(
                i.productSeatList[0], condition))

        # 判断赠品数量是否满足
        if not result_numb_giv >= (
                result_moeny //
                bean.value_num *
                bean.give_value):
            give_sum = 0
            change_give_product(not_product_ListA, bean, give_sum)
            give_number = bean.give_value * bean.max_times
            return {"id": bean.id, "qtty": give_number}

        # 更改这次最大的循环次数
        give_number = int(result_moeny // bean.value_num * bean.give_value)
        change_give_product(not_product_ListA, bean, give_number)
        cursor_give_sum += give_number

        # 进入死循环抽取商品
        while True:
            # 如果大于就终止循环
            if result_moeny >= max_money:
                give_number = int(
                    max_money //
                    bean.value_num *
                    bean.give_value)
                return {"id": bean.id, "qtty": give_number}

            if result_pro != 0 and productListA != not_product_ListA:
                # 先更改不在赠品中的未满足站位信息
                result_pro = change_product(
                    pro_one, bean, userInfo, condition, result_pro)
                if result_pro == 0:
                    kaiguan = True
                result_moeny += result_pro
            else:
                result_pro = 0
                # 若不在赠品列表中的商品不满足 那就从赠品列表当中抽取

            not_product_ListA = sorted(
                not_product_ListA, key=lambda i: getattr(
                    i.productSeatList[0], condition), reverse=True)
            cur_result_money = result_moeny
            for give in not_product_ListA:
                for give_seat in give.productSeatList:
                    # 如果当前金额已经大于最大翻倍金额
                    if cur_result_money // bean.value_num > result_moeny // bean.value_num:
                        break
                    if cur_result_money >= max_money:
                        break
                    if not give_seat.seat:
                        cur_result_money += getattr(give_seat, condition)
                        result_pro += getattr(give_seat, condition)
            # 如果全部加完还没增加一倍那就返回吧.  多余的也没用
            if cur_result_money // bean.value_num <= result_moeny // bean.value_num:
                give_number = int(
                    result_moeny //
                    bean.value_num *
                    bean.give_value)
                return {"id": bean.id, "qtty": give_number}

            if productListA == not_product_ListA:
                result_int = result_pro

            else:
                if not kaiguan:
                    result_int = result_pro - result_moeny
                else:
                    result_int = result_pro

            b = change_product(
                not_product_ListA,
                bean,
                userInfo,
                condition,
                result_int)

            result_moeny += b
            # 获取赠品总数量
            result_numb_giv = get_product_sum(not_product_ListA)
            not_product_ListA = sorted(
                not_product_ListA, key=lambda i: getattr(
                    i.productSeatList[0], condition))
            # 此时计算赠送数量和更改商品站位信息
            # 如果赠送数量不大于当前剩余数量
            if not result_numb_giv > (
                    result_moeny // bean.value_num * bean.give_value) - cursor_give_sum:
                # 全改了
                give_sum = 0
                # 价钱从小到大排序
                if result_moeny // bean.value_num * \
                        bean.give_value >= max_money // bean.value_num * bean.give_value:
                    give_sum = max_money // bean.value_num * bean.give_value
                    give_sum = give_sum - cursor_give_sum
                    change_give_product(not_product_ListA, bean, give_sum)
                    give_number = int(
                        max_money // bean.value_num * bean.give_value)
                    return {"id": bean.id, "qtty": give_number}

                change_give_product(not_product_ListA, bean, give_sum)

                give_number = int(
                    result_moeny //
                    bean.value_num *
                    bean.give_value)
                return {"id": bean.id, "qtty": give_number}

            # 如果当前赠送数量已经超过最大赠送数量
            if cursor_give_sum >= (bean.max_times * bean.give_value):
                give_number = int(bean.max_times * bean.give_value)
                change_give_product(not_product_ListA, bean, give_number)
                return {"id": bean.id, "qtty": give_number}

            # 如果满足
            give_sum = int(result_moeny // bean.value_num * bean.give_value)
            # 若第一次循环进来
            give_sum -= cursor_give_sum
            # 更改站位信息
            change_give_product(not_product_ListA, bean, give_sum)
            # 此时在用游标加上此次赠送数量
            cursor_give_sum += give_sum

    # 第一步看不是赠品列表的条件是否满足当前活动条件
    if result_pro >= bean.value_num:
        # 此时计算赠品数量是否满足

        # 获取赠品总数量
        result_numb_giv = get_product_sum(not_product_ListA)
        # 若当前数量少于赠送数量
        if not result_numb_giv >= (
                result_pro //
                bean.value_num *
                bean.give_value):
            give_sum = 0
            # 价钱从小到大排序
            not_product_ListA = sorted(
                not_product_ListA, key=lambda i: getattr(
                    i.productSeatList[0], condition))
            change_give_product(not_product_ListA, bean, give_sum)
            # 全部更改后计算应该赠送多少数量
            give_number = int(result_pro // bean.value_num * bean.give_value)

            # 更改商品站位数量
            give_sum = result_pro

            change_product(productListA, bean, userInfo, condition, give_sum)

            return {"id": bean.id, "qtty": give_number}

        # 若满足
        give_sum = int(result_pro // bean.value_num * bean.give_value)
        # 排序赠送商品从小到大
        not_product_ListA = sorted(
            not_product_ListA, key=lambda i: getattr(
                i.productSeatList[0], condition))
        change_give_product(not_product_ListA, bean, give_sum)

        # 此时循环次更改商品的金额
        give_sum = result_pro
        cur_money = change_product(
            productListA, bean, userInfo, condition, give_sum)

        # 当前参与商品总金额加上总值
        result_moeny += cur_money

        while True:
            # 查看当前赠品列表未站位数量
            result_numb_giv = get_product_sum(not_product_ListA)

            if result_numb_giv < 0 or result_numb_giv == 0:
                # 全部更改后计算应该赠送多少数量
                give_number = int(
                    result_moeny //
                    bean.value_num *
                    bean.give_value)
                return {"id": bean.id, "qtty": give_number}

            shao = result_numb_giv // 2
            cur_give = result_numb_giv - shao
            # 定义当前需要比对的金额值
            cur_reulst_money = result_moeny
            # 定义加上抽离赠品价钱的赠送金额
            cur_money = pull_give_product(
                not_product_ListA, cur_give, condition)

            cur_reulst_money += cur_money
            # 让总数也加上当前值
            if not (
                    cur_reulst_money //
                    bean.value_num) > (
                    result_moeny //
                    bean.value_num):
                # 若二分之后还是不满足那么就把另外一半也循环抽离
                money_linshi = give_change_pro_two(
                    not_product_ListA, shao, condition, cur_reulst_money, result_moeny, bean)
                cur_money += money_linshi
                cur_reulst_money += money_linshi

            # 如果抽离完还是不大于翻倍那么返回
            if not (
                    cur_reulst_money //
                    bean.value_num) > (
                    result_moeny //
                    bean.value_num):
                # 若不大于就返回
                give_number = int(
                    result_moeny //
                    bean.value_num *
                    bean.give_value)
                return {"id": bean.id, "qtty": give_number}

            # 价钱从大到小排序
            productListA = sorted(
                productListA,
                key=lambda i: getattr(
                    i.productSeatList[0],
                    condition),
                reverse=True)
            # 若大于倍数就用总价钱去执行当前函数
            change_product(productListA, bean, userInfo, condition, cur_money)
            # 在判断当前循环数是多少
            if not get_product_sum(not_product_ListA) >= (
                    cur_money // bean.value_num * bean.give_value):
                give_sum = 0

            else:
                give_sum = (cur_reulst_money // bean.value_num -
                            result_moeny // bean.value_num) * bean.give_value

            change_give_product(not_product_ListA, bean, give_sum)
            result_moeny += cur_money
            result_moeny += money_linshi
            money_linshi = 0
            # 此时计算最大赠送数量
            give_number = int(
                cur_reulst_money //
                bean.value_num *
                bean.give_value)
    else:

        while True:

            if result_pro != 0 and productListA != not_product_ListA:
                # 先更改不在赠品中的未满足站位信息
                result_pro = change_product(
                    pro_one, bean, userInfo, condition, result_pro)
                if result_pro == 0:
                    kaiguan = True
                result_moeny += result_pro
            else:
                result_pro = 0
            # 若不在赠品列表中的商品不满足 那就从赠品列表当中抽取

            not_product_ListA = sorted(
                not_product_ListA, key=lambda i: getattr(
                    i.productSeatList[0], condition), reverse=True)
            result_cr = result_moeny

            for give in not_product_ListA:
                for give_seat in give.productSeatList:
                    # 如果当前金额已经大于最大翻倍金额
                    if result_pro >= bean.value_num:
                        break
                    if result_cr // bean.value_num > result_moeny // bean.value_num:
                        break
                    if not give_seat.seat:
                        result_pro += getattr(give_seat, condition)
                        result_cr += getattr(give_seat, condition)
            # 如果全部加完还没增加一倍那就返回吧.  多余的也没用
            if not ((result_moeny + result_pro) //
                    bean.value_num) > result_moeny // bean.value_num:
                give_number = int(
                    result_moeny //
                    bean.value_num *
                    bean.give_value)
                return {"id": bean.id, "qtty": give_number}

            if productListA == not_product_ListA:
                result_int = result_pro

            else:
                if not kaiguan:
                    result_int = result_pro - result_moeny
                else:
                    result_int = result_pro

            b = change_product(
                not_product_ListA,
                bean,
                userInfo,
                condition,
                result_int)

            result_moeny += b
            # 获取赠品总数量
            result_numb_giv = get_product_sum(not_product_ListA)
            not_product_ListA = sorted(
                not_product_ListA, key=lambda i: getattr(
                    i.productSeatList[0], condition))
            # 此时计算赠送数量和更改商品站位信息
            # 如果赠送数量不大于当前剩余数量
            if not result_numb_giv >= (
                    result_moeny // bean.value_num * bean.give_value) - cursor_give_sum:
                # 全改了
                give_sum = 0
                # 价钱从小到大排序

                change_give_product(not_product_ListA, bean, give_sum)

                give_number = int(
                    result_moeny //
                    bean.value_num *
                    bean.give_value)
                return {"id": bean.id, "qtty": give_number}

            # 如果满足
            give_sum = int(result_moeny // bean.value_num * bean.give_value)
            # 若第一次循环进来
            give_sum -= cursor_give_sum
            # 更改站位信息
            change_give_product(not_product_ListA, bean, give_sum)
            # 此时在用游标加上此次赠送数量
            cursor_give_sum += give_sum


def change_product(productListA, bean, userInfo, condition, give_sum):
    """
    更改当前循环商品的值
    :param productListA:
    :param bean:
    :param userInfo:
    :param condition:
    :return: 返回所有参与活动商品的价钱
    """

    result_money = 0
    for product in productListA:
        for seat in product.productSeatList:
            if result_money >= give_sum:
                break
            if seat.seat == False and seat.is_run_other_pro != False:
                basics_one(seat, product, bean, userInfo)
                result_money += getattr(seat, condition)

    return result_money


def pull_give_product(not_product_ListA, number, condition):
    """
    二分法抽离赠品函数
    :param not_product_ListA:
    :param number: 抽离数量
    :param condition 条件
    :return: 抽离完金额
    """
    result = 0

    for give_pro in not_product_ListA:
        for give_seat in give_pro.productSeatList:
            if give_seat.seat == False and give_seat.is_run_other_pro != False:
                if number == 0:
                    break
                result += getattr(give_seat, condition)

                number -= 1

    return result


def pull_give_product1(not_product_ListA, number, condition):
    """
    二分法抽离赠品函数
    :param not_product_ListA:
    :param number: 抽离数量
    :param condition 条件
    :return: 抽离完金额
    """
    result = 0

    for give_pro in not_product_ListA:
        for give_seat in give_pro.productSeatList:
            if give_seat.seat == False and not hasattr(give_seat, 'b'):
                if number == 0:
                    break
                result += getattr(give_seat, condition)
                give_seat.b = 1
                number -= 1

    return result


def change_give_product(not_product_ListA, bean, give_sum):
    """
    更改活动没一件作为赠品
    :param not_product_ListA:
    :param bean:
    :param give_sum:
    :return:
    """

    # 若满足执行
    if give_sum > 0:
        for give_pro in not_product_ListA:
            for give in give_pro.productSeatList:
                if give.seat == False and give.is_run_other_pro != False and give.is_discount == "y":
                    if give_sum == 0:
                        break
                    one_buy_product(give, give_pro, bean)
                    give_sum -= 1
    else:
        # 不满足执行
        for give_pro in not_product_ListA:
            for give in give_pro.productSeatList:
                if give.seat == False and give.is_run_other_pro != False and give.is_discount == "y":
                    one_buy_product(give, give_pro, bean)


def intersection_max(
        productListA,
        not_product_ListA,
        bean,
        userInfo,
        condition):
    """

    :param productListA:  可参与活动商品
    :param not_product_ListA:  赠品列表
    :param bean: 活动
    :param userInfo: 会员
    :param condition: 条件
    :return:
    """

    if bean.comp_symb_type == "e":
        bean.max_times += 1

    # 赠送总数量
    give_number = 0
    pro_one = [i for i in productListA if i not in not_product_ListA]
    # 1 先取出AB中的 A
    if bean.comp_symb_type == "e":
        bean.max_times += 1

    # 获取当前不是赠品的总金额
    result_pro = get_money_sum(pro_one, condition)
    # 获取赠品总数量
    result_numb_giv = get_product_sum(not_product_ListA)

    # 如果当前总金额大于等于比较值
    if result_pro >= bean.value_num:
        break_value = 0
        for product in productListA:
            for seat in product.productSeatList:
                if break_value >= bean.value_num:
                    break
                if seat.seat == False and seat.is_run_other_pro != False:
                    basics_one(seat, product, bean, userInfo)
                    break_value += getattr(seat, condition)
        break_value = 0

        # 计算赠品是否满足
        result_numb_giv = get_product_sum(not_product_ListA)

        # 赠送数量
        give_number += bean.give_value
        for_give = bean.give_value

        # 如果当前赠送数量大于赠送数量
        if result_numb_giv >= bean.give_value:
            for give in not_product_ListA:

                for give_seat in give.productSeatList:
                    if for_give == 0:
                        break

                    if give_seat.seat == False and give_seat.is_run_other_pro != False and give_seat.is_discount == "y":
                        one_buy_product(give_seat, give, bean)
                        for_give -= 1

        else:
            # 否则就全改了
            for give in not_product_ListA:

                for give_seat in give.productSeatList:
                    if give_seat.seat == False and give_seat.is_run_other_pro != False and give_seat.is_discount == "y":
                        one_buy_product(give_seat, give, bean)

            return {"id": bean.id, "qtty": give_number}

    # 当不大于比较值时就从赠品列表中抽取
    else:
        for give in not_product_ListA:
            for give_seat in give.productSeatList:

                # 如果当前总价大于比较值终止当前循环肯定能大于比较值  之后看还是否可以大于金额
                if result_pro >= bean.value_num:
                    break
                # 若站位就继续循环
                if give_seat.seat:
                    continue
                # 若不大于就继续加而赠品数量随之也减少
                result_pro += getattr(give_seat, condition)
                # 赠品总数量 -=1
                result_numb_giv -= 1
        # 当全部抽取完了还不满足的话就翻倍
        if result_pro >= bean.value_num:
            return {"id": bean.id, "qtty": give_number}

        # 赠送数量
        give_number += bean.give_value
        for_give = bean.give_value
        # 如果当前赠送数量大于赠送数量
        if result_numb_giv >= bean.give_value:
            for give in not_product_ListA:

                for give_seat in give.productSeatList:
                    if for_give == 0:
                        break

                    if give_seat.seat == False and give_seat.is_run_other_pro != False and give_seat.is_discount == "y":
                        one_buy_product(give_seat, give, bean)
                        for_give -= 1

        else:
            # 否则就全改了
            for give in not_product_ListA:

                for give_seat in give.productSeatList:
                    if give_seat.seat == False and give_seat.is_run_other_pro != False and give_seat.is_discount == "y":
                        one_buy_product(give_seat, give, bean)

            return {"id": bean.id, "qtty": give_number}


def intersection_one(
        productListA,
        not_product_ListA,
        bean,
        userInfo,
        condition):
    """
    :param productListA:  可参与活动商品
    :param not_product_ListA:  赠品列表
    :param bean: 活动
    :param userInfo: 会员
    :param condition: 条件
    :return:
    """
    bean.max_times = 1
    # 2 先排序降序

    if bean.value_num == 0:
        bean.value_num = 1

    # 循环更改站位信息
    # 定义容器
    result = 0
    result_moneg = 0
    pro_one = []

    if len(productListA) > 1:
        for product in productListA:
            if product not in not_product_ListA:
                pro_one.append(product)

    else:
        pro_one = productListA

    result = 0

    result_money = 0

    result_pro = get_money_sum(pro_one, condition)
    # 如果当前不是赠品的商品总价不大于比较值
    if not result_pro >= bean.value_num:
        b = change_product(pro_one, bean, userInfo, condition, result_pro)
        # 总价加上未满足的商品金额
        result_money += b

        # 开始抽离有交集商品
        for give in not_product_ListA:
            for seat_give in give.productSeatList:
                if result_money >= bean.value_num:
                    break
                if seat_give.seat == False and seat_give.is_run_other_pro != False:
                    result_money += getattr(seat_give, condition)
                    basics_one(seat_give, give, bean, userInfo)

        result_give = get_product_sum(not_product_ListA)
        not_product_ListA = sorted(
            not_product_ListA, key=lambda i: getattr(
                i.productSeatList[0], condition))

        if result_give >= bean.give_value:
            result_give = bean.give_value

            for not_product in not_product_ListA:
                for not_seat in not_product.productSeatList:
                    if result_give == 0:
                        break
                    if not_seat.seat == False and not_seat.is_run_other_pro != False and not_seat.is_discount == "y":
                        one_buy_product(not_seat, not_product, bean)
                        result_give -= 1
            give_number = bean.give_value
            return {"id": bean.id, "qtty": give_number}
        else:

            for not_product in not_product_ListA:
                for not_seat in not_product.productSeatList:

                    if not_seat.seat == False and not_seat.is_run_other_pro != False and not_seat.is_discount == "y":
                        one_buy_product(not_seat, not_product, bean)
            give_number = bean.give_value
            return {"id": bean.id, "qtty": give_number}

    # 否则的话就是满足
    change_product(pro_one, bean, userInfo, condition, bean.value_num)

    result_give = get_product_sum(not_product_ListA)
    not_product_ListA = sorted(
        not_product_ListA,
        key=lambda i: getattr(
            i.productSeatList[0],
            condition))

    if result_give >= bean.give_value:
        result_give = bean.give_value

        for not_product in not_product_ListA:
            for not_seat in not_product.productSeatList:
                if result_give == 0:
                    break
                if not_seat.seat == False and not_seat.is_run_other_pro != False and not_seat.is_discount == "y":
                    one_buy_product(not_seat, not_product, bean)
                    result_give -= 1
        give_number = bean.give_value
        return {"id": bean.id, "qtty": give_number}
    else:

        for not_product in not_product_ListA:
            for not_seat in not_product.productSeatList:

                if not_seat.seat == False and not_seat.is_run_other_pro != False and not_seat.is_discount == "y":
                    one_buy_product(not_seat, not_product, bean)
        give_number = bean.give_value
        return {"id": bean.id, "qtty": give_number}


def tow_give_one(productListA, not_product_ListA, bean, userInfo, condition):
    if bean.value_num == 0:
        bean.value_num = 1

    # 不翻倍的 A AB
    bean.max_times = 1
    # 循环更改站位信息
    # 定义容器
    result = 0

    result_money = 0

    for product in productListA:

        for seat in product.productSeatList:

            if result >= bean.value_num:
                break
            if seat.seat == False and seat.is_run_other_pro != False:
                basics_one(seat, product, bean, userInfo)
                result += getattr(seat, condition)
                result_money += getattr(seat, condition)

    give_number = 0
    # 查看当前赠送列表当中可还满足数量
    result_give = get_product_sum(not_product_ListA)
    # 如果剩余数量大于赠送商品
    not_product_ListA = sorted(
        not_product_ListA,
        key=lambda i: getattr(
            i.productSeatList[0],
            condition))
    if result_give >= bean.give_value:
        result_give = bean.give_value

        for not_product in not_product_ListA:
            for not_seat in not_product.productSeatList:
                if result_give == 0:
                    break
                if not_seat.seat == False and not_seat.is_run_other_pro != False and not_seat.is_discount == "y":
                    one_buy_product(not_seat, not_product, bean)
                    result_give -= 1
        give_number = result_number(result_money, bean)
        return {"id": bean.id, "qtty": give_number}
    else:

        for not_product in not_product_ListA:
            for not_seat in not_product.productSeatList:

                if not_seat.seat == False and not_seat.is_run_other_pro != False and not_seat.is_discount == "y":
                    one_buy_product(not_seat, not_product, bean)
        give_number = result_number(result_money, bean)
        return {"id": bean.id, "qtty": give_number}


def tow_give_max(productListA, not_product_ListA, bean, userInfo, condition):
    # 若为无线翻倍
    # 先获取A的总金额

    if bean.value_num == 0:
        bean.value_num = 1
    # 赠送总数量
    give_number = 0
    pro_one = []
    # 1 先取出AB中的 A

    cursor_give = 0

    # 获取当前不是赠品的总金额
    result_pro = get_money_sum(productListA, condition)

    result_money = 0

    give_sum = 0

    # 将赠品列表降序排序
    not_product_ListA = sorted(
        not_product_ListA,
        key=lambda i: getattr(
            i.productSeatList[0],
            condition))
    productListA = sorted(
        productListA,
        key=lambda i: getattr(
            i.productSeatList[0],
            condition),
        reverse=True)
    if bean.max_times != -1:
        # 取出最大翻倍金额
        max_money = bean.value_num * bean.max_times
        # 查看现在最大的金额是否大于商品
        two_pro = result_pro / 2
        # 若二分之后连最小条件都不满足的话
        if not two_pro >= bean.value_num:

            # 说明不可二分 此时优先满足 参与商品
            result_pro = get_money_sum(productListA, condition)

            # 既然能进入这里说明肯定满足活动
            cur_money = change_product(
                productListA, bean, userInfo, condition, bean.value_num)

            result_money += cur_money

            result_numb_giv = get_product_sum(not_product_ListA)

            # 计算当前最大赠送商品的数量
            if not result_numb_giv > (
                    cur_money // bean.value_num * bean.give_value):
                give_sum = 0

                change_give_product(not_product_ListA, bean, give_sum)
                # 此时赠送商品的最大数量
                give_number = int(
                    cur_money //
                    bean.value_num *
                    bean.give_value)
                return {"id": bean.id, "qtty": give_number}

            # 此时是满足的 当前最大的循环次数
            give_sum = cur_money // bean.value_num * bean.give_value

            # 进入更改赠品商品
            change_give_product(not_product_ListA, bean, give_sum)
            cursor_give += give_sum
            # 此时看看是否还能满足其余活动
            while True:
                # 查看当前商品剩余价钱
                result_pro = get_money_sum(productListA, condition)

                # 看看剩余价钱是否还满足当前活动
                if not result_pro >= bean.value_num:
                    give_number = result_money // bean.value_num * bean.give_value
                    return {"id": bean.id, "qtty": give_number}
                # 计算当前价钱
                cur_money = change_product(
                    productListA, bean, userInfo, condition, bean.value_num)
                # 总金额加上这次的金额
                result_money += cur_money

                result_numb_giv = get_product_sum(not_product_ListA)

                # 计算当前最大赠送商品的数量
                if not result_numb_giv > (
                        result_money // bean.value_num * bean.give_value) - cursor_give:
                    give_sum = 0

                    change_give_product(not_product_ListA, bean, give_sum)
                    # 此时赠送商品的最大数量
                    give_number = cur_money // bean.value_num * bean.give_value
                    return {"id": bean.id, "qtty": give_number}

                # 那就是可以执行
                # 此时是满足的 当前最大的循环次数
                give_sum = cur_money // (result_money //
                                         bean.value_num * bean.give_value) - cursor_give
                # 总赠送商品游标加上 此次赠送值

                # 进入更改赠品商品
                change_give_product(not_product_ListA, bean, give_sum)
                cursor_give += give_sum

        # 如果当前金额二分之后不大于最大金额
        if not two_pro >= max_money:
            # 首先更改当前一半价钱的金额
            cur_money = change_product(
                productListA, bean, userInfo, condition, two_pro)
            result_money += cur_money
            # 获取当前赠品的数量
            result_numb_giv = get_product_sum(not_product_ListA)
            # 计算当前最大赠送商品的数量
            if not result_numb_giv > (
                    cur_money // bean.value_num * bean.give_value):
                give_sum = 0

                change_give_product(not_product_ListA, bean, give_sum)
                # 此时赠送商品的最大数量
                give_number = int(
                    cur_money //
                    bean.value_num *
                    bean.give_value)
                return {"id": bean.id, "qtty": give_number}

            # 此时是满足的 当前最大的循环次数
            give_sum = cur_money // bean.value_num * bean.give_value
            change_give_product(not_product_ListA, bean, give_sum)

            # 此时赠送商品的最大数量
            give_number = int(cur_money // bean.value_num * bean.give_value)
            # 此时再看当前金额是否满足
            result_pro = get_money_sum(productListA, condition)
            # 赠品总数量
            cursor_give += give_number

            # 此时执行进入死循环看看是否还满足其余商品
            while True:
                # 若此时参与商品的价钱已经大于最大翻倍值
                if result_money >= max_money:
                    give_number = int(
                        max_money // bean.value_num * bean.give_value)
                    return {"id": bean.id, "qtty": give_number}
                # 不然的话继续进入更改商品信息
                # 查看当前商品剩余价钱
                result_pro = get_money_sum(productListA, condition)

                # 看看剩余价钱是否还满足当前活动
                if not result_pro >= bean.value_num:
                    # 若当前商品还有剩余金额 看当前金额加上总金额是否大于当前倍数但又小于总倍数
                    if get_money_sum(productListA, condition) > 0:
                        if (result_money + get_money_sum(productListA,
                                                         condition)) // bean.value_num > result_money // bean.value_num and (
                                result_money + get_money_sum(productListA,
                                                             condition)) < max_money:
                            # 更改商品站位信息
                            cursor = change_product(
                                productListA, bean, userInfo, condition, result_pro)

                            j = ((result_money + cursor) // bean.value_num * bean.give_value) - \
                                result_money // bean.value_num * bean.give_value
                            change_give_product(not_product_ListA, bean, j)
                            result_money += cursor
                            give_number = result_money // bean.value_num * bean.give_value

                            return {"id": bean.id, "qtty": give_number}

                    give_number = result_money // bean.value_num * bean.give_value
                    return {"id": bean.id, "qtty": give_number}
                # 计算当前价钱
                result_cr = result_money
                pro = 0
                for product in productListA:
                    for seat in product.productSeatList:
                        # 如果当前金额已经大于最大翻倍金额
                        if result_cr >= max_money:
                            break
                        if result_cr // bean.value_num > result_money // bean.value_num:
                            break
                        if not seat.seat:
                            pro += getattr(seat, condition)
                            result_cr += getattr(seat, condition)
                # 如果全部加完还没增加一倍那就返回吧.  多余的也没用
                if not ((result_money + result_pro) //
                        bean.value_num) > result_money // bean.value_num:
                    give_number = int(
                        result_money // bean.value_num * bean.give_value)
                    return {"id": bean.id, "qtty": give_number}
                cur_money = change_product(
                    productListA, bean, userInfo, condition, pro)
                # 总金额加上这次的金额
                result_money += cur_money

                result_numb_giv = get_product_sum(not_product_ListA)

                # 计算当前最大赠送商品的数量
                if not result_numb_giv > (
                        result_money // bean.value_num * bean.give_value) - cursor_give:
                    give_sum = 0

                    change_give_product(not_product_ListA, bean, give_sum)
                    # 此时赠送商品的最大数量
                    give_number = result_money // bean.value_num * bean.give_value
                    return {"id": bean.id, "qtty": give_number}

                # 那就是可以执行
                # 此时是满足的 当前最大的循环次数
                give_sum = (result_money // bean.value_num *
                            bean.give_value) - cursor_give
                # 总赠送商品游标加上 此次赠送值

                # 进入更改赠品商品
                change_give_product(not_product_ListA, bean, give_sum)
                cursor_give += give_sum

        # 走到这说明啥都满足了.二分之后的金额也满足了.
        # 更改商品信息

        change_product(productListA, bean, userInfo, condition, max_money)

        # 获取当前赠品数量
        result_numb_giv = get_product_sum(not_product_ListA)

        # 计算最大赠送值
        give_number = bean.give_value * bean.max_times

        if result_numb_giv >= give_number:
            give_sum = give_number

        else:
            give_sum = 0
        change_give_product(not_product_ListA, bean, give_sum)

        return {"id": bean.id, "qtty": give_number}

    # 那就是无线翻倍
    two_pro = result_pro / 2
    # 若二分之后连最小条件都不满足的话
    if not two_pro >= bean.value_num:

        # 说明不可二分 此时优先满足 参与商品
        result_pro = get_money_sum(productListA, condition)

        # 既然能进入这里说明肯定满足活动
        cur_money = change_product(
            productListA,
            bean,
            userInfo,
            condition,
            bean.value_num)

        result_money += cur_money

        result_numb_giv = get_product_sum(not_product_ListA)

        # 计算当前最大赠送商品的数量
        if not result_numb_giv > (
                cur_money //
                bean.value_num *
                bean.give_value):
            give_sum = 0

            change_give_product(not_product_ListA, bean, give_sum)
            # 此时赠送商品的最大数量
            give_number = int(cur_money // bean.value_num * bean.give_value)
            return {"id": bean.id, "qtty": give_number}

        # 此时是满足的 当前最大的循环次数
        give_sum = cur_money // bean.value_num * bean.give_value

        # 进入更改赠品商品
        change_give_product(not_product_ListA, bean, give_sum)
        cursor_give += give_sum
        # 此时看看是否还能满足其余活动
        while True:
            # 查看当前商品剩余价钱
            result_pro = get_money_sum(productListA, condition)

            # 看看剩余价钱是否还满足当前活动
            if not result_pro >= bean.value_num:
                give_number = result_money // bean.value_num * bean.give_value
                return {"id": bean.id, "qtty": give_number}
            # 计算当前价钱
            cur_money = change_product(
                productListA, bean, userInfo, condition, bean.value_num)
            # 总金额加上这次的金额
            result_money += cur_money

            result_numb_giv = get_product_sum(not_product_ListA)

            # 计算当前最大赠送商品的数量
            if not result_numb_giv > (
                    result_money // bean.value_num * bean.give_value) - cursor_give:
                give_sum = 0

                change_give_product(not_product_ListA, bean, give_sum)
                # 此时赠送商品的最大数量
                give_number = cur_money // bean.value_num * bean.give_value
                return {"id": bean.id, "qtty": give_number}

            # 那就是可以执行
            # 此时是满足的 当前最大的循环次数
            give_sum = cur_money // (result_money //
                                     bean.value_num * bean.give_value) - cursor_give
            # 总赠送商品游标加上 此次赠送值

            # 进入更改赠品商品
            change_give_product(not_product_ListA, bean, give_sum)
            cursor_give += give_sum

    # 说明现在得二分法满足当前最小条件
    # 先将二分的价钱标记为参与商品
    cur_money = change_product(
        productListA,
        bean,
        userInfo,
        condition,
        two_pro)
    # 总价钱加上
    result_money += cur_money

    # 计算赠送商品
    # 获取当前赠品数量
    result_numb_giv = get_product_sum(not_product_ListA)

    # 如果不满足最大赠送数量
    if not result_numb_giv > cur_money // bean.value_num * bean.give_value:
        give_sum = 0
        give_number = int(cur_money // bean.value_num * bean.give_value)
        change_give_product(not_product_ListA, bean, give_sum)
        return {"id": bean.id, "qtty": give_number}
    give_number = int(cur_money // bean.value_num * bean.give_value)
    give_sum = give_number
    change_give_product(not_product_ListA, bean, give_sum)
    # 赠送总数加上当前赠送的商品
    cursor_give += give_number

    # 进入死循环 更改每一件商品
    while True:
        # 查看当前商品剩余价钱
        result_pro = get_money_sum(productListA, condition)

        # 若当前商品的价钱已经不满足条件
        if not result_pro >= bean.value_num:
            # 若当前商品还有剩余金额 看当前金额加上总金额是否大于当前倍数但又小于总倍数
            if get_money_sum(productListA, condition) > 0:
                if (result_money + get_money_sum(productListA, condition)
                    ) // bean.value_num > result_money // bean.value_num:
                    # 更改商品站位信息
                    cursor = change_product(
                        productListA, bean, userInfo, condition, result_pro)

                    j = ((result_money + cursor) // bean.value_num * bean.give_value) - \
                        result_money // bean.value_num * bean.give_value
                    change_give_product(not_product_ListA, bean, j)
                    result_money += cursor
                    give_number = result_money // bean.value_num * bean.give_value

                    return {"id": bean.id, "qtty": give_number}
            give_number = int(result_money // bean.value_num * bean.give_value)
            return {"id": bean.id, "qtty": give_number}
        result_cr = result_money
        pro = 0
        for product in productListA:
            for seat in product.productSeatList:
                # 如果当前金额已经大于最大翻倍金额

                if result_cr // bean.value_num > result_money // bean.value_num:
                    break
                if not seat.seat:
                    pro += getattr(seat, condition)
                    result_cr += getattr(seat, condition)
        # 如果全部加完还没增加一倍那就返回吧.  多余的也没用
        if not ((result_money + result_pro) //
                bean.value_num) > result_money // bean.value_num:
            give_number = int(result_money // bean.value_num * bean.give_value)
            return {"id": bean.id, "qtty": give_number}

        # 计算当前价钱
        cur_money = change_product(
            productListA, bean, userInfo, condition, pro)
        # 总金额加上这次的金额
        result_money += cur_money

        result_numb_giv = get_product_sum(not_product_ListA)

        # 计算当前最大赠送商品的数量
        if not result_numb_giv > (
                result_money // bean.value_num * bean.give_value) - cursor_give:
            give_sum = 0

            change_give_product(not_product_ListA, bean, give_sum)
            # 此时赠送商品的最大数量
            give_number = int(result_money // bean.value_num * bean.give_value)
            return {"id": bean.id, "qtty": give_number}

        # 那就是可以执行
        # 此时是满足的 当前最大的循环次数
        give_sum = (result_money // bean.value_num *
                    bean.give_value) - cursor_give
        # 总赠送商品游标加上 此次赠送值

        # 进入更改赠品商品
        change_give_product(not_product_ListA, bean, give_sum)
        cursor_give += give_sum


def change_pro_number(productlist, number, bean, userInfo):
    """

    :param productlist: 需要更改商品的列表
    :param number: 循环次数
    :return: 循环次数
    """
    n = 0
    for product in productlist:
        for seat in product.productSeatList:
            if number == 0:
                break
            if seat.seat == False and seat.is_run_other_pro != False:
                basics_one(seat, product, bean, userInfo)
                number -= 1
                n += 1
    return n


def give_change_pro_two(
        not_product_ListA,
        shao,
        condition,
        cur_reulst_money,
        result_moeny,
        bean):
    """

    :param not_product_ListA: 抽离列表
    :param shao: 二分法的作为赠品的数量
    :param condition:  条件
    :param cur_reulst_money: 当前金额
    :param result_moeny: 总金额
    :param bean: 活动
    :return:
    """
    result = 0
    for product in not_product_ListA:
        for seat in product.productSeatList:
            if shao == 0:
                break
            if (cur_reulst_money //
                bean.value_num) > (result_moeny //
                                   bean.value_num):
                break
            if seat.seat == False and seat.is_run_other_pro != False:
                cur_reulst_money += getattr(seat, condition)
                result += getattr(seat, condition)

    return result


def not_buy_a_give_a_unify_online(
        bean,
        userInfo,
        productList,
        promotion_qtty_sum,
        promotion_amt_list_sum,
        promotion_amt_retail_sum,
        promotion_amt_receivable_sum,
        org_infos,
        org_productlists):
    """
    :param bean: 线上统一买赠、梯度买赠的具体对象
    :param productListA:  所有可以参加活动的列表
    :param not_product_ListA:  所有不可以参加的列表
    :param promotion_qtty_sum:  数量总数
    :param promotion_amt_list_sum:  amt_list:吊牌金额
    :param promotion_amt_retail_sum: amt_retail:零售金额
    :param promotion_amt_receivable_sum: amt_receivable:应收金额
    :param org_infos:未排除已占位商品的符合该促销的数量、吊牌价、零售价、应收价统计结果字典；
    :return:
    """
    isallpro = False
    # 第一步判断活动是否符合执行条件
    if bean.comp_symb_type == "e" and bean.value_num == 0:
        return str(-1)
    # 判断每行的买赠数量是不是为0
    for operation_item in bean.operation_set:
        if operation_item.give_value == 0:
            return str(-1)

    max_double_times = 0
    if bean.target_type == "qtty":
        max_double_times = int(promotion_qtty_sum / bean.value_num)
        if max_double_times < 1:
            if org_infos.get("org_promotion_qtty_sum", 0) >= bean.value_num:
                # productList = copy.deepcopy(org_productlists)
                isallpro = True
            else:
                return str(-1)
    elif bean.target_type == "amt_list":
        max_double_times = int(promotion_amt_list_sum / bean.value_num)
        if max_double_times < 1:
            if org_infos.get(
                "org_promotion_amt_list_sum",
                    0) >= bean.value_num:
                # productList = copy.deepcopy(org_productlists)
                isallpro = True
            else:
                return str(-1)
    elif bean.target_type == "amt_retail":
        max_double_times = int(promotion_amt_retail_sum / bean.value_num)
        if max_double_times < 1:
            if org_infos.get(
                "org_promotion_amt_retail_sum",
                    0) >= bean.value_num:
                # productList = copy.deepcopy(org_productlists)
                isallpro = True
            else:
                return str(-1)
    elif bean.target_type == "amt_receivable":
        max_double_times = int(promotion_amt_receivable_sum / bean.value_num)
        if max_double_times < 1:
            if org_infos.get(
                "org_promotion_amt_receivable_sum",
                    0) >= bean.value_num:
                # productList = copy.deepcopy(org_productlists)
                isallpro = True
            else:
                return str(-1)

    if isallpro:
        return 1

    # 翻倍，比较活动的翻倍限制，再对翻倍次数进行修改
    if max_double_times > 1:
        if bean.max_times == 0 or bean.max_times == 1 or bean.max_times is None:
            max_double_times = 1
        elif bean.max_times > 1 and max_double_times > bean.max_times:
            max_double_times = bean.max_times
    # 说明可以参加此活动， 计算可送赠品数量。
    all_give_products, give_max_pronum, give_max_amtlist, all_give_infos = \
        caculate_buygift_info_online(bean, max_double_times, org_productlists)
    # 进行占位处理
    current_value_num = 0  # 当前已占位条件的总数量（金额）
    for product in productList:
        if current_value_num >= bean.value_num * max_double_times:
            # 已经达到最大翻倍次数所要求的条件，结束循环
            break
        if (product.ecode not in bean.product_list) and (product.sku not in bean.product_list):
            continue
        for seat in product.productSeatList:
            if current_value_num >= bean.value_num * max_double_times:
                # 已经达到最大翻倍次数所要求的条件，结束循环
                break
            if (not seat.seat) and seat.is_run_other_pro:
                # 进行条件占位
                seat.seat = True
                seat.is_run_other_pro = bean.is_run_other_pro  # 能否与其他商品活动同时执行
                seat.is_run_store_act = bean.is_run_store_act  # 能否与全场活动同时执行

                if bean.target_type == "qtty":
                    current_value_num += seat.qtty
                elif bean.target_type == "amt_list":
                    current_value_num += seat.amt_list
                elif bean.target_type == "amt_retail":
                    current_value_num += seat.amt_retail
                elif bean.target_type == "amt_receivable":
                    current_value_num += seat.amt_receivable
    # 将赠品添加到商品列表中
    for item in all_give_products:
        productList.append(item)
    # promotion_lineno:梯度买赠进入，记录当前执行的到底是哪个梯度的，这样返回前端时，只返回该梯度前所有的商品
    promotion_lineno = 0
    if bean.prom_type_three == "ga1402":
        promotion_lineno = bean.promotion_lineno
    # 组织返回值结构
    response_1 = {}
    response_1["product"] = productList
    response_1["buygift"] = {
        "id": bean.id,
        "qtty": 0,
        "sum_amt": 0,
        "online_qtty": give_max_pronum,
        "online_amtlist": give_max_amtlist,
        "max_double_times": max_double_times,
        "all_give_infos": all_give_infos,
        "promotion_lineno": promotion_lineno,
        "isallpro": isallpro}
    response_1["isallpro"] = isallpro
    response_1["dis_id"] = bean.id
    return response_1

def combination_unify_dis_online(
        bean,
        productList,
        org_productlists,
        holddis,
        max_double_times):
    """
    :param bean: 组合买赠的具体对象
    :param productList: 执行过其它类型促销的商品集合
    :param org_productlists:最原始的商品集合
    :param holddis:是否是使用最原始的商品计算
    :param max_double_times: 翻倍次数
    :return:
    """
    isallpro = False

    if holddis == 1:
        isallpro = True
        productList = copy.deepcopy(org_productlists)

    # 翻倍，比较活动的翻倍限制，再对翻倍次数进行修改
    if max_double_times > 1:
        if bean.max_times == 0 or bean.max_times == 1 or bean.max_times is None:
            max_double_times = 1
        elif bean.max_times > 1 and max_double_times > bean.max_times:
            max_double_times = bean.max_times
    # 计算可送赠品的数量金额
    all_give_products, give_max_pronum, give_max_amtlist, all_give_infos = caculate_buygift_info_online(bean,
                                                                                                  max_double_times,
                                                                                                  org_productlists)

    # 条件商品占位
    seat_list = []  # 参与的商品明细
    # 取出参与的商品
    for specific_item in bean.specific_activities:
        # 如果比较条件为大于的话，则比较条件+1
        if specific_item.comp_symb_type == "g":
            value_num = specific_item.value_num + 1
        else:
            value_num = specific_item.value_num
        # 对每一个比较行进行条件占位
        current_max_sum = max_double_times * value_num
        current_sum = 0
        for product in productList:
            if (product.ecode in specific_item.product_list) or (product.sku in specific_item.product_list):
                if current_sum >= current_max_sum:
                    break
                for seat in product.productSeatList:
                    if current_sum >= current_max_sum:
                        break
                    if seat.seat == False and seat.is_run_other_pro:
                        if seat not in seat_list:
                            seat_list.append(seat)
                        # seat.seat = True  # 进行占位
                        # seat.is_run_other_pro = bean.is_run_other_pro
                        # seat.is_run_store_act = bean.is_run_store_act
                        if specific_item.target_type == "qtty":
                            current_sum += seat.qtty
                        elif specific_item.target_type == "amt_list":
                            current_sum += seat.amt_list
                        elif specific_item.target_type == "amt_retail":
                            current_sum += seat.amt_retail
                        elif specific_item.target_type == "amt_receivable":
                            current_sum += seat.amt_receivable
    # 进行占位
    for seat in seat_list:
        seat.seat = True  # 进行占位
        seat.is_run_other_pro = bean.is_run_other_pro
        seat.is_run_store_act = bean.is_run_store_act

    # 将赠品添加到商品列表中
    for item in all_give_products:
        productList.append(item)

    # promotion_lineno:梯度买赠进入，记录当前执行的到底是哪个梯度的，这样返回前端时，只返回该梯度前所有的商品
    promotion_lineno = 0
    if bean.prom_type_three == "ga1402":
        promotion_lineno = bean.promotion_lineno
    # 组织返回值结构
    response_1 = {}
    response_1["product"] = productList
    response_1["buygift"] = {
        "id": bean.id,
        "qtty": 0,
        "sum_amt": 0,
        "online_qtty": give_max_pronum,
        "online_amtlist": give_max_amtlist,
        "max_double_times": max_double_times,
        "all_give_infos": all_give_infos,
        "promotion_lineno": promotion_lineno,
        "isallpro": isallpro}
    response_1["isallpro"] = isallpro
    response_1["dis_id"] = bean.id
    return response_1


def caculate_buygift_info_online(bean, max_double_times, org_productlists):
    """
    计算线上买赠的赠品信息
    :param bean:
    :param max_double_times:
    :param org_productlists:
    :return:
    """
    # # 翻倍，比较活动的翻倍限制，再对翻倍次数进行修改
    # if max_double_times > 1:
    #     if bean.max_times == 0 or bean.max_times == 1:
    #         max_double_times = 1
    #     elif bean.max_times > 1 and max_double_times > bean.max_times:
    #         max_double_times = bean.max_times

    give_max_pronum = 0  # 最大赠送数量
    give_max_amtlist = 0  # 最大赠送金额
    all_give_infos = []  # 赠品信息（送了哪些赠品以及相应的数量）
    give_product_list = []

    # 计算可送赠品的总数量及金额
    for operation_item in bean.operation_set:
        current_qtty = max_double_times * operation_item.give_value  # 此行可送数量
        give_max_pronum += current_qtty
        current_buygift_product = operation_item.buygift_product
        if current_buygift_product:
            # 此行可送总金额
            current_amt = current_qtty * CalculationPrice(current_buygift_product[0].get("amt_list", 0))
            give_max_amtlist += current_amt
            # 可送赠品信息
            give_info = current_buygift_product[0]
            give_info["qtty"] = current_qtty
            all_give_infos.append(give_info)
            give_product_info = {}
            give_product_info["lineno"] = ""
            give_product_info["ecode"] = current_buygift_product[0].get("ecode", "")
            give_product_info["sku"] = current_buygift_product[0].get("sku", "")
            give_product_info["qtty"] = current_qtty
            give_product_info["amt_list"] = CalculationPrice(current_buygift_product[0].get("amt_list", 0))
            give_product_info["amt_retail"] = CalculationPrice(current_buygift_product[0].get("amt_list", 0))
            give_product_info["amt_receivable"] = 0
            give_product_info["is_buy_gifts"] = "y"
            give_product_info["pcond_id"] = operation_item.pcond_id
            give_product_info["pitem_id"] = bean.pitem_id
            give_product_list.append(give_product_info)

    # max_line_no = 0
    # for ori_product in org_productlists:
    #     if ori_product.lineno > max_line_no:
    #         max_line_no = ori_product.lineno

    all_give_product = []
    # max_line_no += 1
    for give_item in give_product_list:
        give_product = Product(give_item, -1)
        give_product.discountId.add(bean.id)
        give_product.qttyCount = 0
        for seat in give_product.productSeatList:
            seat.seat = True
            seat.is_run_other_pro = False
            seat.is_run_store_act = False
            seat.discountId.append(bean.id)
            seat.discountPrice.append(give_product.amt_list)
            seat.is_buy_gifts = "y"
            seat.pcond_id = give_item.get("pcond_id")
        all_give_product.append(give_product)
        # max_line_no += 1

    return all_give_product, give_max_pronum, give_max_amtlist, all_give_infos