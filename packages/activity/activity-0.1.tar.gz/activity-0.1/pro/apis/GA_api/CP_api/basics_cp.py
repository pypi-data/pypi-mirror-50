#!/usr/bin/env python
"""
   换购详细运算
   encoding: utf-8
   2018/12/26 4:27 PM
   by李博文

   edit by hexiaoxia 2019/06/26
   重写商品换购活动具体执行方法
"""
from pro.apis.GA_api.CP_api.cp_utils import pandun_one_or_two_cp
from pro.apis.GA_api.CP_api.cp_utils import contion
from pro.apis.GA_api.CP_api.cp_utils import pro_change_sum_intersection, pro_change_money_intersection, \
    calculation_current, change_pro_qtty, change_pro_money, result_max_ge_CurResult_combination, intersection_qtty
from pro.apis.GA_api.CP_api.cp_utils import calculate_fun, getNewPrice, result_max_ge_CurResult
from pro.apis.GA_api.CP_api.cp_utils import min_pro_pro2_max
from pro.apis.GA_api.CP_api.cp_utils import re_response
from pro.utils.linq import linq
import copy
import pro.utils.util as util


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
    统一打折换购、统一特价换购、统一优惠换购
    :param bean: 活动的具体对象
    :param productListA:  所有可以参加活动的列表
    :param not_product_ListA:  所有不可以参加的列表
    :param promotion_qtty_sum:  数量总数
    :param promotion_amt_list_sum:  amt_list:吊牌金额
    :param promotion_amt_retail_sum: amt_retail:零售金额
    :param promotion_amt_receivable_sum: amt_receivable:应收金额
    :param org_infos:未排除已占位商品的符合该促销的数量、吊牌价、零售价、应收价统计结果字典；
    :param give_product:交集的商品（即在条件商品列表里又在换购商品列表里）
    :return:
    """
    isallpro = False

    # 第一步判断活动是否符合执行条件
    if bean.operation_set[0].give_value == 0:
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
        # 说明可以作为可参与的活动，但不在择优列表中
        return 1
    # 判断是否有特例品
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

    newproductlist, max_times, max_pronum, redemption_productall = discomputefunction(
        bean, productList, 0, 0, 0, 0, 0, 0, give_product, [], 1, has_special_product)

    newproductlist, now_max_amt, swap_products=calculation_dis(newproductlist, redemption_productall, bean)

    response_1 = {}
    response_1["product"] = newproductlist
    response_1["buygift"] = {
        "id": bean.id,
        "qtty": max_pronum,
        "sum_amt": now_max_amt,
        "times":max_times,
        "bsc_qtty":bean.operation_set[0].give_value,
        "isallpro": isallpro}
    response_1["isallpro"] = isallpro
    response_1["dis_id"] = bean.id
    response_1["product_cp"]=swap_products
    return response_1

def discomputefunction(
        bean,
        productList,
        now_max_times,
        now_max_pro_numb,
        all_sum_amt_list,
        all_sum_amt_retail,
        all_sum_amt_receivable,
        all_sum_qtty,
        give_product,redemption_productall,groupnum, has_special_product):
    '''
    :param bean:当前促销活动
    :param productList:商品信息
    :param now_max_times:可翻倍次数
    :param now_max_pro_numb:可赠送商品数量
    :param give_product:交集的商品（即在条件商品列表里又在换购商品列表里）
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
        key=lambda i: i.amt_list,
        reverse=True)

    oldproductList = copy.deepcopy(productList)
    seat_list = []  # 参与的商品明细
    # 在统计一倍的调价商品占位时优先占位只是条件商品的商品，之后还有剩余，那么再占位既是条件商品又是换购的商品
    all_sum_amt_list, all_sum_amt_retail, all_sum_amt_receivable, all_sum_qtty, has_special_product = \
        getonepronumb(productList, bean, seatrownum, now_max_times, productListA, all_sum_amt_list,
                      all_sum_amt_retail, all_sum_amt_receivable, all_sum_qtty, isaddrow,
                      ishavedis, give_product, 1, has_special_product, seat_list)
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
                getonepronumb(productList, bean, seatrownum, now_max_times, productListA,
                              all_sum_amt_list, all_sum_amt_retail, all_sum_amt_receivable,
                              all_sum_qtty, isaddrow, ishavedis, give_product, 2, has_special_product, seat_list)

    if not productListA:
        return oldproductList, now_max_times, now_max_pro_numb, redemption_productall
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
            return oldproductList, now_max_times, now_max_pro_numb, redemption_productall
        if bean.max_times == -1:
            # 可无限翻倍
            max_pro_numb = bean.operation_set[0].give_value * (nownum - now_max_times)
        elif bean.max_times >= 0:
            if nownum - now_max_times > 1:
                if bean.max_times != 0:
                    if nownum > bean.max_times:
                        nownum = bean.max_times
                        max_pro_numb = bean.operation_set[0].give_value * (nownum - now_max_times)
                        # return oldproductList, now_max_times, now_max_pro_numb, redemption_productall
                    else:
                        max_pro_numb = bean.operation_set[0].give_value * \
                            (nownum - now_max_times)
                else:
                    nownum = 1
                    max_pro_numb = bean.operation_set[0].give_value
            else:
                if bean.max_times != 0:
                    if nownum > bean.max_times:
                        return oldproductList, now_max_times, now_max_pro_numb, redemption_productall
                else:
                    nownum = 1
                max_pro_numb = bean.operation_set[0].give_value

        now_max_times = nownum
        now_max_pro_numb = bean.operation_set[0].give_value * nownum
        # 将参与的明细占位
        for seat in seat_list:
            seat.seat = True
        # redemption_productall=[] #记录当前计算倍数里的参与商品对应换购优惠明细的记录
        redemption_product={}
        redemption_productlist=[]
        disproductList=[]
        t_amt_receivable=0
        t_qttys=0
        oldt_qttys=0
        # groupnum=1
        pric=0
        ifsameoperation=True
        operation_setall = []
        r_operation_set = {}
        r_disproductList=[]
        r_oldt_qttys=0
        three_id = str(bean.prom_type_three).lower()

        purchase_way = "T"
        if three_id == "ga1505":
            purchase_way = "J"
        elif three_id == "ga1503":
            purchase_way = "D"

        if three_id == "ga1505":
            bean.operation_set = sorted(bean.operation_set,
                                        key=lambda i: i.purchase_condition, reverse=False)
        else:
            bean.operation_set = sorted(bean.operation_set,
                             key=lambda i: i.purchase_condition,reverse=True)

        productList = sorted(productList, key=lambda i: i.amt_receivable)


        if max_pro_numb > 0:
            for s_row in bean.operation_set:
                operation_setall = []
                r_disproductList = []
                r_oldt_qttys = 0
                if max_pro_numb <= 0:
                    break
                #
                can_remove_product = []
                r_operation_set = {}
                if redemption_productall:
                    row_redemption_pro = linq(redemption_productall).where(
                        lambda x: x["pcond_id"] == s_row.pcond_id and x["t_qttys"] < s_row.give_value).tolist()
                    if row_redemption_pro:
                        red_index = redemption_productall.index(row_redemption_pro[0])

                        row_operation_set = linq(redemption_productall[red_index]["operation_setall"]).where(
                            lambda x: x["pcond_id"] == s_row.pcond_id).tolist()

                        if row_operation_set:
                            r_operation_set = row_operation_set[0]
                            operation_setall = redemption_productall[red_index]["operation_setall"]
                            operation_setall.remove(r_operation_set)

                        disproductList = row_redemption_pro[0]["disproductList"]
                        r_disproductList = copy.deepcopy(row_redemption_pro[0]["disproductList"])
                        redemption_productlist = []
                        t_qttys = row_redemption_pro[0]["t_qttys"]
                        oldt_qttys = t_qttys
                        t_amt_receivable = row_redemption_pro[0]["total_oldamt_receivable"]
                        groupnum = row_redemption_pro[0]["groupnum"]
                        # row_productSeatList = linq(disproductList).where(
                        #     lambda x: x.ecode.lower() == product1.ecode.lower()).tolist()
                        # if row_productSeatList:
                        #     redemption_productlist = row_productSeatList[0]
                        #     disproductList.remove(row_productSeatList[0])
                        # else:
                        t_qttys = 0
                        redemption_productall.remove(row_redemption_pro[0])
                for product1 in productList:
                    if max_pro_numb <= 0:
                        break

                    row_sku = linq(s_row.product_list).where(lambda x: x["ecode"].lower() == product1.ecode.lower()).tolist()
                    if row_sku:
                        if not r_operation_set:
                            r_operation_set["pcond_id"] = s_row.pcond_id
                            r_operation_set["give_value"] = s_row.give_value
                            r_operation_set["purchase_way"] = purchase_way
                            r_operation_set["purchase_condition"] = s_row.purchase_condition
                            if purchase_way == "T" or purchase_way == "J":
                                ceilprice = util.div(s_row.purchase_condition, s_row.give_value)
                            else:
                                ceilprice = s_row.purchase_condition
                            r_operation_set["ceilprice"] = ceilprice

                        new_pro=copy.deepcopy(product1)
                        can_seat_remove = []
                        for r_seat1 in product1.productSeatList:
                            if max_pro_numb > 0 and r_seat1.seat == False and r_seat1.is_discount == "y":
                                # 如果上一次计算达到了一倍换购数， r_operation_set将清空， 需要重新赋值
                                if not r_operation_set:
                                    r_operation_set["pcond_id"] = s_row.pcond_id
                                    r_operation_set["give_value"] = s_row.give_value
                                    r_operation_set["purchase_way"] = purchase_way
                                    r_operation_set["purchase_condition"] = s_row.purchase_condition
                                    if purchase_way == "T" or purchase_way == "J":
                                        ceilprice = util.div(s_row.purchase_condition, s_row.give_value)
                                    else:
                                        ceilprice = s_row.purchase_condition
                                    r_operation_set["ceilprice"] = ceilprice
                                r_seat1.seat = True
                                r_seat1.discountId.append(bean.id)
                                if bean.target_item == "amt_receivable":
                                    pric=r_seat1.amt_receivable
                                elif bean.target_item == 'amt_retail':
                                    pric = r_seat1.amt_retail
                                elif bean.target_item == 'amt_list':
                                    pric = r_seat1.amt_list
                                # r_seat1.is_run_other_pro = bean.is_run_other_pro
                                # r_seat1.is_run_store_act = bean.is_run_store_act
                                # r_seat1.is_buy_gifts = "y"
                                # r_seat1.pcond_id=s_row.pcond_id
                                # r_seat1.groupnum=groupnum
                                # r_seat1.purchase_way=purchase_way
                                r_seat1.upamt_receivable=pric
                                r_seat1.amt_receivable=pric
                                redemption_productlist.append(r_seat1)

                                # (product1.productSeatList).remove(r_seat1)
                                can_seat_remove.append(r_seat1)
                                product1.qtty=product1.qtty-1

                                t_amt_receivable=t_amt_receivable+pric
                                t_qttys=t_qttys+1
                                oldt_qttys=oldt_qttys+1
                                r_oldt_qttys=r_oldt_qttys+1
                                # now_max_amt = now_max_amt + r_seat1.amt_receivable
                                max_pro_numb = max_pro_numb - 1

                                if oldt_qttys==s_row.give_value:
                                    new_pro.qtty = t_qttys
                                    new_pro.productSeatList = redemption_productlist
                                    disproductList.append(new_pro)
                                    r_disproductList.append(new_pro)
                                    r_operation_set["t_qttys"] = r_oldt_qttys
                                    r_operation_set["disproductList"] = copy.deepcopy(r_disproductList)
                                    r_operation_set["total_oldamt_receivable"] = util.CalculationPrice(t_amt_receivable)
                                    r_operation_set["new_total_amt_receivable"] = util.CalculationPrice(t_amt_receivable)
                                    operation_setall.append(r_operation_set)

                                    groupnum, redemption_product, redemption_productlist, disproductList, t_amt_receivable, t_qttys,oldt_qttys=setnewdisitem(oldt_qttys, t_amt_receivable,
                                                  disproductList, s_row, groupnum, redemption_productall, redemption_product,)

                                    redemption_productall[-1]["operation_setall"]=operation_setall
                                    operation_setall = []
                                    r_operation_set = {}
                                    r_disproductList=[]
                                    r_oldt_qttys=0
                                    t_amt_receivable = 0
                                    redemption_productlist = []

                        for seat_item in can_seat_remove:
                            (product1.productSeatList).remove(seat_item)
                        if product1.qtty==0:
                            can_remove_product.append(product1)
                            # productList.remove(product1)

                        if t_qttys > 0 and oldt_qttys > 0:
                            new_pro.qtty = t_qttys
                            new_pro.productSeatList = redemption_productlist
                            disproductList.append(new_pro)
                            r_disproductList.append(new_pro)
                            r_operation_set["t_qttys"] = r_oldt_qttys
                            r_operation_set["disproductList"] = copy.deepcopy(r_disproductList)
                            r_operation_set["total_oldamt_receivable"] = util.CalculationPrice(t_amt_receivable)
                            r_operation_set["new_total_amt_receivable"] = util.CalculationPrice(t_amt_receivable)
                            # operation_setall.append(r_operation_set)
                            t_qttys=0
                            # t_amt_receivable=0
                            # r_oldt_qttys=0
                            redemption_productlist=[]
                            # r_disproductList=[]

                            if oldt_qttys == s_row.give_value:
                                groupnum, redemption_product, redemption_productlist, disproductList, t_amt_receivable, t_qttys, oldt_qttys = setnewdisitem(
                                    oldt_qttys, t_amt_receivable,
                                    disproductList, s_row,
                                    groupnum, redemption_productall, redemption_product)

                                redemption_productall[-1]["operation_setall"] = operation_setall
                                operation_setall = []
                                r_operation_set = {}
                                r_disproductList=[]
                # 删除
                for can_del_item in can_remove_product:
                    productList.remove(can_del_item)
                if oldt_qttys > 0 and oldt_qttys != s_row.give_value:
                    operation_setall.append(r_operation_set)
                    # t_amt_receivable=0
                    groupnum, redemption_product, redemption_productlist, disproductList, t_amt_receivable, t_qttys, oldt_qttys = setnewdisitem(
                        oldt_qttys, t_amt_receivable, disproductList, s_row,
                        groupnum, redemption_productall, redemption_product)

                    redemption_productall[-1]["operation_setall"] = operation_setall
                    operation_setall = []
                    r_operation_set = {}
                    r_disproductList = []
            # if oldt_qttys > 0:
            #     if t_qttys>0:
            #         new_pro.qtty = t_qttys
            #         new_pro.productSeatList = redemption_productlist
            #         disproductList.append(new_pro)
            #         r_disproductList.append(new_pro)
            #         r_operation_set["t_qttys"] = r_oldt_qttys
            #         r_operation_set["disproductList"] = copy.deepcopy(r_disproductList)
            #         r_operation_set["total_oldamt_receivable"] = util.CalculationPrice(t_amt_receivable)
            #         r_operation_set["new_total_amt_receivable"] = util.CalculationPrice(t_amt_receivable)
            #         operation_setall.append(r_operation_set)
            #
            #     if oldt_qttys == s_row.give_value:
            #         groupnum, redemption_product, redemption_productlist, disproductList, t_amt_receivable, t_qttys,oldt_qttys=setnewdisitem(oldt_qttys, t_amt_receivable, disproductList, s_row,
            #                       groupnum, redemption_productall, redemption_product)
            #
            #         redemption_productall[-1]["operation_setall"] = operation_setall
            #         operation_setall = []
            #         r_operation_set = {}
            #         r_disproductList=[]
            #     else:
            #         groupnum, redemption_product, redemption_productlist, disproductList, t_amt_receivable, t_qttys, oldt_qttys = setnewdisitem(
            #             oldt_qttys,  t_amt_receivable, disproductList, s_row,
            #             groupnum, redemption_productall, redemption_product)
            #         redemption_productall[-1]["operation_setall"] = operation_setall


        if bean.max_times > 1 and (now_max_times + 1) > bean.max_times:
            return productList, now_max_times, now_max_pro_numb, redemption_productall
        else:
            if bean.max_times == 0:
                return productList, now_max_times, now_max_pro_numb, redemption_productall
            return discomputefunction(
                bean,
                productList,
                now_max_times,
                now_max_pro_numb,
                all_sum_amt_list,
                all_sum_amt_retail,
                all_sum_amt_receivable,
                all_sum_qtty,
                give_product,redemption_productall,groupnum, has_special_product)

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
    :param give_product:交集的商品（即在条件商品列表里又在换购商品列表里）
    :param intype:1 表示当前从只在条件商品不在换购里的获取条件商品占位;2 表示从存在交集的商品里获取条件商品占位；
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

    if (not is_can_caculate) or current_caculate_sum >= bean.value_num:
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
                # 当前不是特例品的时候，结束当前循环，进入下一层循环
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
                        if current_caculate_sum >= bean.value_num:
                            # 当当前的计算总和大于比较值时，结束循环
                            break
                        if r_seat.seat:
                            seatrownum += 1
                            continue
                        if not ishavedis:
                            isaddrow = False
                            break
                        #if bean.max_times != 0:
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
        # 如果当前已经达到条件，结束循环
        return all_sum_amt_list, all_sum_amt_retail, all_sum_amt_receivable, all_sum_qtty, has_special_product
    if intype == 1:
        # 说明条件商品中没有特例品了
        has_special_product["condition_pro_flug"] = False
    if intype == 2:
        # 说明交集的商品中没有特例品了
        has_special_product["give_pro_flug"] = False

    for product in productList:
        if current_caculate_sum >= bean.value_num:
            # 当当前的计算总和大于比较值时，结束循环
            break
        if not isaddrow:
            break
        if product.productSeatList and product.productSeatList[0].is_discount == "n":
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
                    if current_caculate_sum >= bean.value_num:
                        # 当当前的计算总和大于比较值时，结束循环
                        break
                    if r_seat.seat:
                        seatrownum += 1
                        continue
                    if not ishavedis:
                        isaddrow = False
                        break
                    #if bean.max_times != 0:
                    if bean.target_type == "qtty":
                        # if all_sum_qtty >= bean.value_num:
                        #     break
                        current_caculate_sum += 1
                        # if newrow.qtty >= bean.value_num:
                        #     break
                        #
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
                        current_caculate_sum += r_seat.amt_list
                        # if newrow.sum_amt_list >= bean.value_num:
                        #     break
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
                        current_caculate_sum += r_seat.amt_retail
                        # if newrow.sum_amt_retail >= bean.value_num:
                        #     break
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
                            # current_caculate_sum += r_seat.amt_receivable
                            # if newrow.sum_amt_receivable >= bean.value_num:
                            #     break
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

def setnewdisitem(oldt_qttys,t_amt_receivable,disproductList,s_row,groupnum,redemption_productall,redemption_product):
    redemption_product["groupnum"]=groupnum
    redemption_product["t_qttys"] = oldt_qttys
    redemption_product["pcond_id"] = s_row.pcond_id
    redemption_product["total_oldamt_receivable"] = t_amt_receivable
    redemption_product["disproductList"] = disproductList

    redemption_productall.append(redemption_product)
    groupnum = groupnum + 1
    redemption_product = {}
    redemption_productlist = []
    disproductList = []
    t_amt_receivable = 0
    t_qttys = 0
    oldt_qttys=0
    return groupnum,redemption_product,redemption_productlist,disproductList,t_amt_receivable,t_qttys,oldt_qttys

def calculation_dis(newproductlist,redemption_productall,bean):
    '''
    当前促销换购活动执行结果的商品重新计算得到最终执行结果
    :param newproductlist: 原商品信息
    :param redemption_productall: 换购执行的标记的结果
    :param bean: 促销
    :return:
    '''
    swap_products = []
    now_max_amt = 0
    if redemption_productall:
        for rowitem in redemption_productall:
            ifdis=True
            operation_setall = rowitem["operation_setall"]
            groupnum = rowitem["groupnum"]
            for row_1 in operation_setall:
                pcond_id = row_1["pcond_id"]
                purchase_way = row_1["purchase_way"]
                if row_1["t_qttys"] == row_1["give_value"]:
                    if purchase_way == "T":
                        row_1["new_total_amt_receivable"] = util.CalculationPrice(row_1["purchase_condition"])
                    elif purchase_way == "J":
                        row_1["new_total_amt_receivable"] = util.CalculationPrice(
                            util.minus(row_1["new_total_amt_receivable"], row_1["purchase_condition"]))
                    else:
                        row_1["new_total_amt_receivable"] = util.CalculationPrice(
                            util.mul(row_1["new_total_amt_receivable"], row_1["purchase_condition"]))
                    if float(row_1["new_total_amt_receivable"]) < row_1["total_oldamt_receivable"]:
                        row_1 = util.calculation(row_1, "GA")
                    else:
                        for row1 in row_1["disproductList"]:
                            for row1 in row1.productSeatList:
                                row1.discountPrice.append(0)
                else:
                    if purchase_way == "T":
                        row_1["new_total_amt_receivable"] = util.CalculationPrice(
                            util.mul(row_1["ceilprice"], row_1["t_qttys"]))
                    elif purchase_way == "J":
                        t_jprice=util.mul(row_1["ceilprice"], row_1["t_qttys"])
                        row_1["new_total_amt_receivable"] = util.CalculationPrice(
                            util.minus(row_1["new_total_amt_receivable"],t_jprice))
                    else:
                        row_1["new_total_amt_receivable"] = util.CalculationPrice(
                            util.mul(row_1["ceilprice"], row_1["new_total_amt_receivable"]))
                    if float(row_1["new_total_amt_receivable"]) < row_1["total_oldamt_receivable"]:
                        row_1 = util.calculation(row_1, "GA")
                    else:
                        for row1 in row_1["disproductList"]:
                            for row1 in row1.productSeatList:
                                row1.discountPrice.append(0)

                disproductList = row_1["disproductList"]
                for row_2 in disproductList:
                    for row_3 in row_2.productSeatList:
                        upamt_receivable = row_3.upamt_receivable
                        row_3.upamt_receivable = row_3.amt_receivable
                        row_3.is_run_other_pro = bean.is_run_other_pro
                        row_3.is_run_store_act = bean.is_run_store_act
                        row_3.is_repurchase = "y"  # 是否是换购商品
                        row_3.pcond_id = pcond_id
                        row_3.groupnum = groupnum
                        row_3.purchase_way = purchase_way
                        if row_3.discountPrice:
                            now_max_amt = util.add(now_max_amt, row_3.discountPrice[-1])

                        row_swap_products = {}
                        row_swap_products = {}
                        row_swap_products["ecode"] = row_3.ecode
                        row_swap_products["sku"] = row_3.sku
                        row_swap_products["lineno"] = row_3.lineno
                        row_swap_products["amt_receivableb"] = upamt_receivable
                        row_swap_products["qtty"] = row_3.qtty
                        row_swap_products["pcond_id"] = pcond_id
                        row_swap_products["groupnum"] = groupnum
                        # 修改， 因为append方法执行后没有返回值（None）， 所以执行set会出错
                        # row_swap_products["ga_dis"] = list(set(row.discountId.append(id))) if len(row.discountId) > 0 else [id]
                        if type(row_3.discountId) == list:
                            row_swap_products["ga_dis"] = list(set(row_3.discountId))
                        else:
                            row_swap_products["ga_dis"] = [id]
                        row_swap_products["pa_dis"] = []
                        row_swap_products["amt_receivablea"] = row_3.amt_receivable
                        swap_products.append(row_swap_products)

                    newproductlist.append(row_2)

    return newproductlist,float(now_max_amt),swap_products

def combination_unify_dis(
        bean,
        productList,
        org_productlists,
        holddis,
        give_product):
    """
    组合打折换购、组合特价换购、组合优惠换购
    :param bean: 换购活动的具体对象
    :param productList: 执行过其它类型促销的商品集合
    :param org_productlists:最原始的商品集合
    :param holddis:是否是使用最原始的商品计算
    :param give_product:交集的商品（即在条件商品列表里又在换购商品列表里）
    :return:
    """
    isallpro = False

    if holddis == 1:
        isallpro = True
        productList = copy.deepcopy(org_productlists)

    newproductlist, max_times, max_pronum, redemption_productall = discomputefunction_cb(
        bean, productList, 0, 0, 0, 0, 0, 0, give_product,[],[],1)

    newproductlist, now_max_amt, swap_products = calculation_dis(newproductlist, redemption_productall, bean)

    response_1 = {}
    response_1["product"] = newproductlist
    response_1["buygift"] = {
        "id": bean.id,
        "qtty": max_pronum,
        "sum_amt": now_max_amt,
        "times": max_times,
        "bsc_qtty": bean.operation_set[0].give_value,
        "isallpro": isallpro}
    response_1["isallpro"] = isallpro
    response_1["dis_id"] = bean.id
    response_1["product_cp"] = swap_products
    return response_1

def discomputefunction_cb(
        bean,
        productList,
        now_max_times,
        now_max_pro_numb,
        all_sum_amt_list,
        all_sum_amt_retail,
        all_sum_amt_receivable,
        all_sum_qtty,
        give_product,
        specific_rowtotal,redemption_productall,groupnum):
    '''
    促销的具体计算方法
    :param bean:当前促销活动
    :param productList:商品信息
    :param now_max_times:可翻倍次数
    :param now_max_pro_numb:可换购商品数量
    :param all_sum_amt_list:
    :param all_sum_amt_retail:
    :param all_sum_amt_receivable:
    :param all_sum_qtty:
    :param give_product:交集的商品（即在条件商品列表里又在换购商品列表里）
    :param specific_rowtotal:记录组合条件每项参与计算的总的相关数据，供递归统计翻倍次数使用
    :return:
    '''
    # 先将商品按照吊牌价降序排序，优先将一倍的条件商品筛选出来
    nownum = 0  # 当前可翻多少倍（对于按金额计算，有可能会发生大于1的倍数，按数量的每次进来这个都是1）
    max_pro_numb = 0  # 当前翻的倍数换购的商品数
    ishavedis = True
    isaddrow = True

    seatrownum = 0
    productListA = []
    productList = sorted(
        productList,
        key=lambda i: i.productSeatList[0].amt_list,
        reverse=True)

    oldproductList = copy.deepcopy(productList)
    seat_list = []  # 参与的商品明细
    current_not_caculate = []
    bean_items = []
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
                all_sum_amt_list, all_sum_amt_retail, all_sum_amt_receivable, all_sum_qtty, \
                has_special_product = getonepronumb(productList, r_item, seatrownum, now_max_times,
                                                    productListA, all_sum_amt_list, all_sum_amt_retail,
                                                    all_sum_amt_receivable, all_sum_qtty, isaddrow,
                                                    ishavedis, give_product, 2, has_special_product, seat_list)

        isadd_specific_rowtotal=True
        if specific_rowtotal:
            if len(specific_rowtotal)>row_index:
                isadd_specific_rowtotal=False

        if isadd_specific_rowtotal:
            newrowitem = {}
            newrowitem["all_sum_amt_list"] = 0
            newrowitem["all_sum_amt_retail"] = 0
            newrowitem["all_sum_amt_receivable"] = 0
            newrowitem["all_sum_qtty"] = 0
            newrowitem["has_special_product"] = 0
            specific_rowtotal.append(newrowitem)
        else:
            # 先不将每行结果记录， 当每一行的结果都出来后，再根据筛选出来的商品计算每一行的最终比较价格
            # specific_rowtotal[row_index]["all_sum_amt_list"]=all_sum_amt_list
            # specific_rowtotal[row_index]["all_sum_amt_retail"] = all_sum_amt_retail
            # specific_rowtotal[row_index]["all_sum_amt_receivable"] = all_sum_amt_receivable
            # specific_rowtotal[row_index]["all_sum_qtty"] = all_sum_qtty
            specific_rowtotal[row_index]["has_special_product"] = has_special_product
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
            max_pro_numb = bean.operation_set[0].give_value * (nownum - now_max_times)
        elif r_item.max_times >= 0:
            # 不可翻倍或设置了固定翻倍次数
            if (nownum - now_max_times) > 1:
                if r_item.max_times != 0:
                    if nownum > r_item.max_times:
                        nownum = r_item.max_times
                        max_pro_numb = bean.operation_set[0].give_value * (nownum - now_max_times)
                    else:
                        max_pro_numb = bean.operation_set[0].give_value * \
                            (nownum - now_max_times)
                        # return
                        # productList,now_max_times,now_max_pro_numb,now_max_amt
                else:
                    nownum = 1
                    max_pro_numb = bean.operation_set[0].give_value
            else:
                if r_item.max_times != 0:
                    if nownum > r_item.max_times:
                        nownum = r_item.max_times
                else:
                    nownum = 1
                max_pro_numb = bean.operation_set[0].give_value

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

    # for seat in seat_list:
    #     seat.seat = True
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
        key=lambda i: i.amt_list)

    now_max_times = nownum
    now_max_pro_numb = bean.operation_set[0].give_value * nownum

    redemption_product = {}
    redemption_productlist = []
    disproductList = []
    t_amt_receivable = 0
    t_qttys = 0
    oldt_qttys = 0
    # groupnum=1
    pric = 0
    ifsameoperation = True
    operation_setall = []
    r_operation_set = {}
    r_disproductList = []
    r_oldt_qttys = 0
    three_id = str(bean.prom_type_three).lower()

    purchase_way = "T"
    if three_id == "ga1506":
        purchase_way = "J"
    elif three_id == "ga1504":
        purchase_way = "D"

    if three_id == "ga1506":
        bean.operation_set = sorted(bean.operation_set,
                                    key=lambda i: i.purchase_condition, reverse=False)
    else:
        bean.operation_set = sorted(bean.operation_set,
                                    key=lambda i: i.purchase_condition, reverse=True)

    productList = sorted(productList, key=lambda i: i.amt_receivable)

    if max_pro_numb > 0:
        for s_row in bean.operation_set:
            operation_setall = []
            r_disproductList = []
            r_oldt_qttys = 0
            can_remove_product = []
            if max_pro_numb <= 0:
                break

            r_operation_set = {}
            if redemption_productall:
                row_redemption_pro = linq(redemption_productall).where(
                    lambda x: x["pcond_id"] == s_row.pcond_id and x["t_qttys"] < s_row.give_value).tolist()
                if row_redemption_pro:
                    red_index = redemption_productall.index(row_redemption_pro[0])

                    row_operation_set = linq(redemption_productall[red_index]["operation_setall"]).where(
                        lambda x: x["pcond_id"] == s_row.pcond_id).tolist()

                    if row_operation_set:
                        r_operation_set = row_operation_set[0]
                        operation_setall = redemption_productall[red_index]["operation_setall"]
                        operation_setall.remove(r_operation_set)

                    disproductList = row_redemption_pro[0]["disproductList"]
                    r_disproductList = copy.deepcopy(row_redemption_pro[0]["disproductList"])
                    t_qttys = row_redemption_pro[0]["t_qttys"]
                    oldt_qttys = t_qttys
                    t_amt_receivable = row_redemption_pro[0]["total_oldamt_receivable"]
                    groupnum = row_redemption_pro[0]["groupnum"]
                    # row_productSeatList = linq(disproductList).where(
                    #     lambda x: x.ecode.lower() == product1.ecode.lower()).tolist()
                    # if row_productSeatList:
                    #     redemption_productlist = row_productSeatList[0]
                    #     disproductList.remove(row_productSeatList[0])
                    # else:
                    t_qttys = 0
                    redemption_productlist = []
                    redemption_productall.remove(row_redemption_pro[0])
            for product1 in productList:
                if max_pro_numb <= 0:
                    break

                row_sku = linq(s_row.product_list).where(
                    lambda x: x["ecode"].lower() == product1.ecode.lower()).tolist()
                if row_sku:
                    if not r_operation_set:
                        r_operation_set["pcond_id"] = s_row.pcond_id
                        r_operation_set["give_value"] = s_row.give_value
                        r_operation_set["purchase_way"] = purchase_way
                        r_operation_set["purchase_condition"] = s_row.purchase_condition
                        if purchase_way == "T" or purchase_way == "J":
                            ceilprice = util.div(s_row.purchase_condition, s_row.give_value)
                        else:
                            ceilprice = s_row.purchase_condition
                        r_operation_set["ceilprice"] = ceilprice
                    # if redemption_productall:
                    #     row_redemption_pro = linq(redemption_productall).where(
                    #         lambda x: x["pcond_id"] == s_row.pcond_id and x["t_qttys"] < s_row.give_value).tolist()
                    #     if row_redemption_pro:
                    #         red_index = redemption_productall.index(row_redemption_pro[0])
                    #
                    #         row_operation_set = linq(redemption_productall[red_index]["operation_setall"]).where(
                    #             lambda x: x["pcond_id"] == s_row.pcond_id).tolist()
                    #
                    #         if row_operation_set:
                    #             r_operation_set = row_operation_set[0]
                    #             operation_setall = redemption_productall[red_index]["operation_setall"]
                    #             operation_setall.remove(r_operation_set)
                    #
                    #         disproductList = row_redemption_pro[0]["disproductList"]
                    #         t_qttys = row_redemption_pro[0]["t_qttys"]
                    #         oldt_qttys = t_qttys
                    #         t_amt_receivable = row_redemption_pro[0]["total_oldamt_receivable"]
                    #         groupnum = row_redemption_pro[0]["groupnum"]
                    #         row_productSeatList = linq(disproductList).where(
                    #             lambda x: x.ecode.lower() == product1.ecode.lower()).tolist()
                    #         if row_productSeatList:
                    #             redemption_productlist = row_productSeatList[0]
                    #             disproductList.remove(row_productSeatList[0])
                    #         else:
                    #             t_qttys = 0
                    #         redemption_productall.remove(row_redemption_pro[0])

                    new_pro = copy.deepcopy(product1)
                    can_seat_remove = []
                    for r_seat1 in product1.productSeatList:
                        if max_pro_numb > 0 and r_seat1.seat == False and r_seat1.is_discount == "y":
                            # 如果上一次计算达到了一倍换购数， r_operation_set将清空， 需要重新赋值
                            if not r_operation_set:
                                r_operation_set["pcond_id"] = s_row.pcond_id
                                r_operation_set["give_value"] = s_row.give_value
                                r_operation_set["purchase_way"] = purchase_way
                                r_operation_set["purchase_condition"] = s_row.purchase_condition
                                if purchase_way == "T" or purchase_way == "J":
                                    ceilprice = util.div(s_row.purchase_condition, s_row.give_value)
                                else:
                                    ceilprice = s_row.purchase_condition
                                r_operation_set["ceilprice"] = ceilprice

                            r_seat1.seat = True
                            r_seat1.discountId.append(bean.id)
                            if bean.target_item == "amt_receivable":
                                pric = r_seat1.amt_receivable
                            elif bean.target_item == 'amt_retail':
                                pric = r_seat1.amt_retail
                            elif bean.target_item == 'amt_list':
                                pric = r_seat1.amt_list
                            # r_seat1.is_run_other_pro = bean.is_run_other_pro
                            # r_seat1.is_run_store_act = bean.is_run_store_act
                            # r_seat1.is_buy_gifts = "y"
                            # r_seat1.pcond_id=s_row.pcond_id
                            # r_seat1.groupnum=groupnum
                            # r_seat1.purchase_way=purchase_way
                            r_seat1.upamt_receivable = pric
                            r_seat1.amt_receivable = pric
                            redemption_productlist.append(r_seat1)

                            # (product1.productSeatList).remove(r_seat1)
                            can_seat_remove.append(r_seat1)
                            product1.qtty = product1.qtty - 1

                            t_amt_receivable = t_amt_receivable + pric
                            t_qttys = t_qttys + 1
                            oldt_qttys = oldt_qttys + 1
                            r_oldt_qttys = r_oldt_qttys + 1
                            # now_max_amt = now_max_amt + r_seat1.amt_receivable
                            max_pro_numb = max_pro_numb - 1

                            if oldt_qttys == s_row.give_value:
                                new_pro.qtty = t_qttys
                                new_pro.productSeatList = redemption_productlist
                                disproductList.append(new_pro)
                                r_disproductList.append(new_pro)
                                r_operation_set["t_qttys"] = r_oldt_qttys
                                r_operation_set["disproductList"] = copy.deepcopy(r_disproductList)
                                r_operation_set["total_oldamt_receivable"] = util.CalculationPrice(t_amt_receivable)
                                r_operation_set["new_total_amt_receivable"] = util.CalculationPrice(t_amt_receivable)
                                operation_setall.append(r_operation_set)

                                groupnum, redemption_product, redemption_productlist, disproductList, t_amt_receivable, t_qttys, oldt_qttys = setnewdisitem(
                                    oldt_qttys, t_amt_receivable,
                                    disproductList, s_row, groupnum, redemption_productall, redemption_product, )

                                redemption_productall[-1]["operation_setall"] = operation_setall
                                operation_setall = []
                                r_operation_set = {}
                                r_disproductList = []
                                r_oldt_qttys = 0
                                t_qttys = 0
                                t_amt_receivable = 0
                                redemption_productlist = []

                    if product1.qtty == 0:
                        can_remove_product.append(product1)
                        # productList.remove(product1)
                    for seat in can_seat_remove:
                        (product1.productSeatList).remove(seat)
                    if t_qttys > 0 and oldt_qttys > 0:
                        new_pro.qtty = t_qttys
                        new_pro.productSeatList = redemption_productlist
                        disproductList.append(new_pro)
                        r_disproductList.append(new_pro)
                        r_operation_set["t_qttys"] = r_oldt_qttys
                        r_operation_set["disproductList"] = copy.deepcopy(r_disproductList)
                        r_operation_set["total_oldamt_receivable"] = util.CalculationPrice(t_amt_receivable)
                        r_operation_set["new_total_amt_receivable"] = util.CalculationPrice(t_amt_receivable)
                        # operation_setall.append(r_operation_set)
                        t_qttys = 0
                        # t_amt_receivable = 0
                        # r_oldt_qttys = 0
                        redemption_productlist = []
                        # r_disproductList = []

                        if oldt_qttys == s_row.give_value:
                            groupnum, redemption_product, redemption_productlist, disproductList, t_amt_receivable, t_qttys, oldt_qttys = setnewdisitem(
                                oldt_qttys, t_amt_receivable,
                                disproductList, s_row,
                                groupnum, redemption_productall, redemption_product)

                            redemption_productall[-1]["operation_setall"] = operation_setall
                            operation_setall = []
                            r_operation_set = {}
                            r_disproductList = []
                            t_amt_receivable = 0
                            redemption_productlist = []
            # 删除
            for can_del_item in can_remove_product:
                productList.remove(can_del_item)
            if oldt_qttys > 0 and oldt_qttys != s_row.give_value:
                operation_setall.append(r_operation_set)
                # t_amt_receivable = 0
                groupnum, redemption_product, redemption_productlist, disproductList, t_amt_receivable, t_qttys, oldt_qttys = setnewdisitem(
                    oldt_qttys, t_amt_receivable, disproductList, s_row,
                    groupnum, redemption_productall, redemption_product)

                redemption_productall[-1]["operation_setall"] = operation_setall
                operation_setall = []
                r_operation_set = {}
                r_disproductList = []
        # if oldt_qttys > 0:
        #     if t_qttys > 0:
        #         new_pro.qtty = t_qttys
        #         new_pro.productSeatList = redemption_productlist
        #         disproductList.append(new_pro)
        #         r_disproductList.append(new_pro)
        #         r_operation_set["t_qttys"] = r_oldt_qttys
        #         r_operation_set["disproductList"] = copy.deepcopy(r_disproductList)
        #         r_operation_set["total_oldamt_receivable"] = util.CalculationPrice(t_amt_receivable)
        #         r_operation_set["new_total_amt_receivable"] = util.CalculationPrice(t_amt_receivable)
        #         operation_setall.append(r_operation_set)
        #
        #     if oldt_qttys == s_row.give_value:
        #         groupnum, redemption_product, redemption_productlist, disproductList, t_amt_receivable, t_qttys, oldt_qttys = setnewdisitem(
        #             oldt_qttys, t_amt_receivable, disproductList, s_row,
        #             groupnum, redemption_productall, redemption_product)
        #
        #         redemption_productall[-1]["operation_setall"] = operation_setall
        #         operation_setall = []
        #         r_operation_set = {}
        #         r_disproductList = []
        #     else:
        #         groupnum, redemption_product, redemption_productlist, disproductList, t_amt_receivable, t_qttys, oldt_qttys = setnewdisitem(
        #             oldt_qttys, t_amt_receivable, disproductList, s_row,
        #             groupnum, redemption_productall, redemption_product)
        #         redemption_productall[-1]["operation_setall"] = operation_setall
    else:
        return productList, now_max_times, now_max_pro_numb, redemption_productall

    if bean.max_times > 1 and (now_max_times + 1) > bean.max_times:
        return productList, now_max_times, now_max_pro_numb, redemption_productall
    else:
        # if not ishavedis:
        #     return productList, now_max_times, now_max_pro_numb, now_max_amt
        # else:
        if bean.max_times == 0:
            return productList, now_max_times, now_max_pro_numb, redemption_productall
        return discomputefunction_cb(
            bean,
            productList,
            now_max_times,
            now_max_pro_numb,
            all_sum_amt_list,
            all_sum_amt_retail,
            all_sum_amt_receivable,
            all_sum_qtty,
            give_product,specific_rowtotal, redemption_productall, groupnum)


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
        index_row = 0
        for row in productListMAX:
            row_sumamtpro = 0
            row_sumqttyoline=0
            row_sumamtoline=0
            row_sumamt = 0
            for row_item in row:
                row_sumamtpro += row_item["buygift"]["sum_amt"]

            for row_item1 in row[-1]["product"]:
                for row_item2 in row_item1.productSeatList:
                    row_sumamt += row_item2.amt_receivable

            if row_sumamtpro==0:
                continue

            if row_sumbuygiftpro_up>0:
                if row_sumbuygiftpro_up>row_sumamt:
                    row_sumbuygiftpro_up = row_sumamt
                    index_row = productListMAX.index(row)
                elif row_sumbuygiftpro_up==row_sumamt:
                    if row_sumamtpro>row_sumamtpro_up:
                        row_sumbuygiftpro_up = row_sumamt
                        index_row = productListMAX.index(row)
            else:
                row_sumbuygiftpro_up = row_sumamt
                index_row = productListMAX.index(row)

        n_productlists = productListMAX[index_row]
        for row1 in productListMAX[index_row]:
            buygift_list.append(row1["buygift"])
    else:
        n_productlists = productListMAX[0]
        for row1 in productListMAX[0]:
            buygift_list.append(row1["buygift"])
    return n_productlists


def cp_basic(bean, userInfo, productListA, productList, kaiguan):
    """
    原来的方法，废弃（只做保留记录）--hexiaoxia 2019-06-26
    :param bean:活动
    :param userInfo: 会员
    :param productListA: 可以参与活动的商品
    :param productList: 所有商品
    :return:
    """

    # 如果换购商品条件为空直接返回
    if not len(bean.operation_set) > 0:
        return

    # 判断bean的长度
    if hasattr(bean, "specific_activities"):
        # 说明是组合
        if bean.specific_activities[0].comp_symb_type.lower() == "g":
            if bean.specific_activities[0].value_num == 0:
                bean.max_times = 1
            bean.specific_activities[0].value_num += 1

        if bean.specific_activities[1].comp_symb_type.lower() == "g":
            if bean.specific_activities[1].value_num == 0:
                bean.max_times = 1
            bean.specific_activities[1].value_num += 1
    else:
        # 单品
        if bean.comp_symb_type.lower() == "g":
            if bean.value_num == 0:
                bean.max_times = 1
            bean.value_num += 1
    response = pandun_one_or_two_cp(bean, productListA)
    # 如果response 返回时空说明不满足活动
    if response == None or response == "off":
        return

    # 如果是判断可以参与的活动 就不用运行了
    if kaiguan != False:
        return {"id": bean.id}

    # 进入详细运算
    return cp_condition(bean, productListA, productList, response)


def cp_condition(bean, productListA, productList, response):
    """
    原来的方法，废弃（只做保留记录）--hexiaoxia 2019-06-26
    :param bean: 活动详细运算
    :param productListA: 可以参与活动的列表
    :param productList: 所有商品
    :return: 所有作为换购的商品明细
    """
    # 计算判断条件
    condition1, condition2 = contion(response, bean)

    if bean.max_times == 0:
        bean.max_times = 1

    # 记录总倍数
    max = 0
    # 组合商品的可以翻倍数
    pro = 0
    pro2 = 0

    response_cp = []
    result = None
    last_time_pro = 0
    last_time_pro2 = 0

    result_moeny = 0
    result_moeny2 = 0

    response1 = None
    # 记录是否还可以进入更改换购商品明细
    is_implement = True

    if response[-1] != 1:
        p = 0
        # 说明是组合. 先查看是否存在交集
        for product1 in productListA[0]:
            for product2 in productListA[1]:
                if product1.ecode.lower() == product2.ecode.lower():
                    p += 1

        while True:
            # 如果条件1是数量 本来一个函数可以判断两个比较值 但是不能太全面就又写了一个金额函数
            if pro <= pro2:
                if bean.specific_activities[0].target_type.lower() == "qtty":
                    response = intersection_qtty(bean.specific_activities[0].value_num, productListA[0])
                # 如果是金额
                else:
                    response = result_max_ge_CurResult_combination(bean.specific_activities[0].value_num, pro,
                                                                   productListA[0], result_moeny, condition1, 1)
            if pro2 <= pro:
                # 接下来是组合2条件的看是否满足
                if bean.specific_activities[1].target_type.lower() == "qtty":
                    response1 = intersection_qtty(bean.specific_activities[1].value_num, productListA[1])
                # 如果是金额
                else:
                    response1 = result_max_ge_CurResult_combination(bean.specific_activities[1].value_num, pro,
                                                                    productListA[1], result_moeny2, condition2, 2)
            if response == "off" or response1 == "off":
                # 如果不满足就返回
                # 返回id,当前可以换购的最大数量 基础件数 当前倍数 和 所有换购商品
                if len(response_cp) > 0:
                    response_cp = getNewPrice(bean, response_cp)
                return re_response(bean, response_cp, max)

            if bean.max_times != -1:
                if max == bean.max_times or max > bean.max_times:
                    if max > bean.max_times:
                        max = bean.max_times
                    if len(response_cp) > 0:
                        response_cp = getNewPrice(bean, response_cp)
                    return re_response(bean, response_cp, max)
            # 说明有交集
            if p != 0:
                # 当前条件1的倍数小于或者等于条件2的倍数方可执行
                if pro <= pro2:
                    # 然后判断第一个条件以什么满足 None为数量 不为None的用getter来获取满足条件
                    if condition1 == None:
                        # 更改数量条件商品
                        pro_change_sum_intersection(bean.specific_activities[0].value_num, productListA, 1, bean)
                        pro += 1
                    else:
                        result_moeny += pro_change_money_intersection(bean.specific_activities[0].value_num,
                                                                      productListA, 1,
                                                                      condition1, max, result_moeny, bean)
                        pro = calculation_current(result_moeny, bean.specific_activities[0].value_num)
                # 当前条件2的倍数小于或者等于条件1的倍数方可执行
                if pro2 <= pro:
                    # 更改第二组商品
                    if condition2 == None:
                        pro_change_sum_intersection(bean.specific_activities[1].value_num, productListA, 2, bean)
                        pro2 += 1
                    else:
                        result_moeny2 += pro_change_money_intersection(bean.specific_activities[1].value_num,
                                                                       productListA, 2,
                                                                       condition2, max, result_moeny2, bean)
                        pro2 = calculation_current(result_moeny2, bean.specific_activities[1].value_num)
                # 看组合1 和组合2 谁的倍数更小并且判断循环次数
                for_max = min_pro_pro2_max(pro, pro2, min(last_time_pro, last_time_pro2))

                # 如果当前倍数已经超过最大倍数就是只有5倍 7倍而没有6倍
                if bean.max_times != -1:
                    if min(pro, pro2) > bean.max_times:
                        for_max = min_pro_pro2_max(pro, pro2, (bean.max_times - min(last_time_pro, last_time_pro2)))

                if is_implement == True:
                    while True:
                        if is_implement == False:
                            break
                        if for_max == 0:
                            break
                        max += 1
                        productList = sorted(productList, key=lambda x: x.amt_receivable)
                        cur_response = calculate_fun(bean, productList, max, response_cp)
                        # 如果没执行完.
                        if cur_response == None:
                            is_implement = False
                            cur_response = []
                        else:
                            if cur_response[0]["one_multiple"] == False:
                                # 手动更改进入值
                                is_implement = False
                            response_cp = cur_response[0]["pro_list"]
                        for_max -= 1

                        if cur_response == None or cur_response[0]["one_multiple"] == False:
                            max += for_max

                else:
                    max += for_max
                    last_time_pro = pro
                    last_time_pro2 = pro2
            else:
                # 到这就是 无交集了
                response = pandun_one_or_two_cp(bean, productListA)
                if response == None:
                    return re_response(bean, response_cp, max)

                # 当前条件1的倍数小于或者等于条件2的倍数方可执行
                if pro <= pro2:
                    # 然后判断第一个条件以什么满足 None为数量 不为None的用getter来获取满足条件
                    if condition1 == None:
                        # 更改数量条件商品
                        change_pro_qtty(productListA[0], bean.specific_activities[0].value_num, bean)
                        pro += 1
                    else:
                        result_moeny = change_pro_money(productListA[0], bean.specific_activities[0].value_num,
                                                        condition1, max, result_moeny, bean)
                        last_time_pro = pro
                        pro = calculation_current(result_moeny, bean.specific_activities[0].value_num)
                # 当前条件2的倍数小于或者等于条件1的倍数方可执行
                if pro2 <= pro:
                    # 更改第二组商品
                    if condition2 == None:
                        change_pro_qtty(productListA[1], bean.specific_activities[1].value_num, bean)
                        pro2 += 1
                    else:
                        result_moeny = change_pro_money(productListA[1], bean.specific_activities[1].value_num,
                                                        condition2, max, result_moeny, bean)
                        last_time_pro2 = pro2
                        pro2 = calculation_current(result_moeny, bean.specific_activities[0].value_num)
                # 看组合1 和组合2 谁的倍数更小并且判断循环次数
                for_max = min_pro_pro2_max(pro, pro2, min(last_time_pro, last_time_pro2))
                # 如果当前倍数已经超过最大倍数就是只有5倍 7倍而没有6倍
                if bean.max_times != -1:
                    if min(pro, pro2) > bean.max_times:
                        for_max = min_pro_pro2_max(pro, pro2, (bean.max_times - min(last_time_pro, last_time_pro2)))

                if is_implement == True:
                    while True:
                        if is_implement == False:
                            break
                        if for_max == 0:
                            break
                        max += 1
                        productList = sorted(productList, key=lambda x: x.amt_receivable)
                        cur_response = calculate_fun(bean, productList, max, response_cp)
                        # 如果没执行完.
                        if cur_response == None:
                            is_implement = False
                            cur_response = []
                        else:
                            if cur_response[0]["one_multiple"] == False:
                                # 手动更改进入值
                                is_implement = False
                            response_cp = cur_response[0]["pro_list"]
                        for_max -= 1

                        if cur_response == None or cur_response[0]["one_multiple"] == False:
                            max += for_max
                else:
                    max += for_max
            last_time_pro = pro
            last_time_pro2 = pro2
    # 能走到这说明就是单品了
    while True:
        # 先查看是否已经达到最大倍数
        if bean.max_times != -1:
            if max == bean.max_times or max > bean.max_times:
                if max > bean.max_times:
                    max = bean.max_times
                if len(response_cp) > 0:
                    response_cp = getNewPrice(bean, response_cp)
                return re_response(bean, response_cp, max)

        # 判断当前条件是否满足
        if bean.target_type.lower() == "qtty":
            result = pandun_one_or_two_cp(bean, productListA)
        else:
            # 金额
            result = result_max_ge_CurResult(bean, max, productListA, result_moeny, condition1)
        if result == None:
            if len(response_cp) > 0:
                response_cp = getNewPrice(bean, response_cp)
            return re_response(bean, response_cp, max)
        # 判断以什么条件满足的 如果是数量那就None 不为数量是什么就是什么
        if result[0] == None:
            change_pro_qtty(productListA, bean.value_num, bean)
            pro += 1
        else:
            # 那就是金额了
            result_moeny = change_pro_money(productListA, bean.value_num,
                                            condition1, max, result_moeny, bean)

            pro = calculation_current(result_moeny, bean.value_num)

        # 看组合1 和组合2 谁的倍数更小并且判断循环次数
        for_max = pro - last_time_pro
        # 如果当前倍数已经超过最大倍数就是只有5倍 7倍而没有6倍
        if bean.max_times != -1:
            if pro > bean.max_times:
                for_max = bean.max_times - last_time_pro

        if is_implement == True:
            while True:
                if is_implement == False:
                    break
                if for_max == 0:
                    break
                max += 1
                productList = sorted(productList, key=lambda x: x.amt_receivable)
                cur_response = calculate_fun(bean, productList, max, response_cp)
                # 如果没执行完.
                if cur_response == None:
                    is_implement = False
                    cur_response = []
                else:
                    if cur_response[0]["one_multiple"] == False:
                        # 手动更改进入值
                        is_implement = False
                    response_cp = cur_response[0]["pro_list"]
                for_max -= 1

                if cur_response == None or cur_response[0]["one_multiple"] == False:
                    max += for_max

            last_time_pro = pro

        else:
            max += for_max
            last_time_pro = pro
