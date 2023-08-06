#!/usr/bin/env python
"""
   由于换购太复杂这个工具只针对换购
   encoding: utf-8
   2018/12/26 4:55 PM
   
  
   by李博文
"""
from pro.apis.GA_api.BG_api.buy_a_for_value import tongji


def pandun_one_or_two_cp(bean, productListA, pro=0, pro2=0, ):
    """

    :param bean:
    :param productListA:
    :return: response 0:满足条件如果是数量为空  最后一个下标是1or2 2就是组合
    """
    response = []
    # 先判断是组合还是统一
    if bean.prom_type_three.lower() == "ga1504" or bean.prom_type_three.lower() == "ga1506" or bean.prom_type_three.lower() == "ga1502":
        # 说明是组合 取出第一个组合的条件和第二个组合的条件
        cp1 = bean.specific_activities[0]
        cp2 = bean.specific_activities[1]

        # 获取商品所有条件属性
        promotion_qtty_sum, promotion_amt_list_sum, promotion_amt_retail_sum, promotion_amt_receivable_sum = tongji(
            productListA[0])
        # 获取条件2所有商品条件属性
        promotion_qtty_sum2, promotion_amt_list_sum2, promotion_amt_retail_sum2, promotion_amt_receivable_sum2 = tongji(
            productListA[1])

        if pro <= pro2:
            # 判断商品是否满足1
            if cp1.target_type.lower() == "qtty":
                if not promotion_qtty_sum >= bean.specific_activities[0].value_num:
                    return "off"
                response.append(None)
            elif cp1.target_type.lower() == "amt_list":
                if not promotion_amt_list_sum >= bean.specific_activities[0].value_num:
                    return "off"
                response.append("amt_list")
            elif cp1.target_type.lower() == "amt_retail":
                if not promotion_amt_retail_sum >= bean.specific_activities[0].value_num:
                    return "off"
                response.append("amt_retail")
            else:
                if not promotion_amt_receivable_sum >= bean.specific_activities[0].value_num:
                    return "off"
                response.append("amt_receivable")
        if pro2 <= pro:
            if cp2.target_type.lower() == "qtty":
                if not promotion_qtty_sum2 >= bean.specific_activities[1].value_num:
                    return "off"
                response.append(None)
            elif cp2.target_type.lower() == "amt_list":
                if not promotion_amt_list_sum2 >= bean.specific_activities[1].value_num:
                    return "off"
                response.append("amt_list")
            elif cp2.target_type.lower() == "amt_retail":
                if not promotion_amt_retail_sum2 >= bean.specific_activities[1].value_num:
                    return "off"
                response.append("amt_retail")
            else:
                if not promotion_amt_receivable_sum2 >= bean.specific_activities[1].value_num:
                    return "off"
                response.append("amt_receivable")
            response.append(2)
            return response
        return "ok"
    else:
        # 走到这说明是不是组合
        promotion_qtty_sum, promotion_amt_list_sum, promotion_amt_retail_sum, promotion_amt_receivable_sum = tongji(
            productListA)

        if bean.target_type.lower() == "qtty":
            if not promotion_qtty_sum >= bean.value_num:
                return
            response.append(None)
        elif bean.target_type.lower() == "amt_list":
            if not promotion_amt_list_sum >= bean.value_num:
                return
            response.append("amt_retail")
        elif bean.target_type.lower() == "amt_retail":
            if not promotion_amt_retail_sum >= bean.value_num:
                return
            response.append("amt_retail")
        else:
            if not promotion_amt_receivable_sum >= bean.value_num:
                return
            response.append("amt_receivable")
        response.append(1)
        return response


def contion(response, bean):
    """
    判断是单品还是组合and两者活动以什么满足是
    :param response:
    :return:
    """
    condition1 = None
    condition2 = None
    if response[-1] == 2:
        # 说明是组合
        # 先查看第一个满足条件是什么
        condition1 = None
        condition2 = None
        if response[0] != None:
            condition1 = response[0]
        if response[1] != "qtty" and response[1] != 2:
            condition2 = response[1]
    else:
        # 走到这就是单品
        condition1 = None
        if response[0] != None:
            condition1 = response[0]

        if bean.target_type.lower() == "amt_list":
            condition1 = "amt_list"
        elif bean.target_type.lower() == "amt_retail":
            condition1 = "amt_retail"
        elif bean.target_type.lower() == "amt_receivable":
            condition1 = "amt_receivable"

    return condition1, condition2


def pro_change_money_intersection(for_max, productListA, number, condition, max, result_moeny, bean):
    """"
    :param for_max: 最大循环次数
    :param productListA: 可以参与的商品
    :param number 控制是第一次进来还是第二次
    :param max 当前的倍数
    :param result_moeny 当前已经参与商品的金额
    :return:
    """
    result = result_moeny
    if number == 1:
        for product in productListA[0]:
            for seat in product.productSeatList:
                if result // for_max > max:
                    return result - result_moeny
                if hasattr(seat,"intersection2"):
                    seat.seat = True
                    # 是否与全场活动同时执行
                    seat.is_run_other_pro = bean.is_run_other_pro
                    # 是否与全场活动同时执行
                    seat.is_run_store_act = bean.is_run_store_act
                    result += getattr(seat, condition)
                    delattr(seat, "intersection2")

        pro_intersection = intersection(productListA)
        for product in pro_intersection:
            for seat in product.productSeatList:
                if result // for_max > max:
                    return result - result_moeny
                if seat.seat == False and seat.is_run_other_pro != False:
                    seat.seat = True
                    seat.intersection = 1
                    # 是否与全场活动同时执行
                    seat.is_run_other_pro = bean.is_run_other_pro
                    # 是否与全场活动同时执行
                    seat.is_run_store_act = bean.is_run_store_act
                    result += getattr(seat, condition)

        if not result // for_max > max:
            for product in productListA[0]:
                for seat in product.productSeatList:
                    if result // for_max > max:
                        return result - result_moeny
                    if seat.seat == False and seat.is_run_other_pro != False:
                        seat.seat = True
                        seat.intersection = 1

                        # 是否与全场活动同时执行
                        seat.is_run_other_pro = bean.is_run_other_pro
                        # 是否与全场活动同时执行
                        seat.is_run_store_act = bean.is_run_store_act
                        result += getattr(seat, condition)
    else:
        # 优先计算已经站位的商品
        for product in productListA[1]:
            for seat in product.productSeatList:
                if result // for_max > max:
                    return result - result_moeny
                if hasattr(seat, "intersection"):
                    result += getattr(seat, condition)

                    delattr(seat, "intersection")

        if not result // for_max > max:
            # 如果循环完还没有满足说明还要循环别的商品
            # 优先计算已经站位的商品
            for product in productListA[1]:
                for seat in product.productSeatList:
                    if result // for_max > max:
                        return result - result_moeny
                    if seat.is_run_other_pro != False and seat.seat == False:
                        result += getattr(seat, condition)
                        seat.is_run_other_pro = bean.is_run_other_pro
                        # 是否与全场活动同时执行
                        seat.is_run_store_act = bean.is_run_store_act
                        seat.seat = True
                        seat.intersection2 = 1
    return result - result_moeny


def pro_change_sum_intersection(for_max, productListA, number, bean):
    """
    如果number 值为1 就只更改商品站位信息
    如果number 不为1 就先找有属性为intersection 删除
    如果还不满足就找没站位的商品继续站位
    :param for_max: 最大循环次数
    :param productListA: 可以参与的商品
    :param number 控制是第一次进来还是第二次
    :return: 因为是数量不需要返回值
    """

    if number == 1:
        for product in productListA[0]:
            for seat in product.productSeatList:
                if for_max == 0:
                    return
                if hasattr(seat, "intersection2"):
                    for_max -= 1
                    delattr(seat, "intersection2")

        if for_max != 0:
            pro_intersection = intersection(productListA)
            for product in pro_intersection:
                for seat in product.productSeatList:
                    if for_max == 0:
                        break
                    if seat.seat == False and seat.is_run_other_pro != False:
                        seat.seat = True
                        seat.is_run_other_pro = bean.is_run_other_pro
                        # 是否与全场活动同时执行
                        seat.is_run_store_act = bean.is_run_store_act
                        seat.intersection = 1
                        for_max -= 1
        if for_max != 0:
            for product in productListA[0]:
                for seat in product.productSeatList:
                    if for_max == 0:
                        break
                    if seat.seat == False and seat.is_run_other_pro != False:
                        seat.seat = True
                        # 是否与其他商品活动同时执行
                        seat.is_run_other_pro = bean.is_run_other_pro
                        # 是否与全场活动同时执行
                        seat.is_run_store_act = bean.is_run_store_act
                        seat.intersection = 1
                        for_max -= 1
    else:
        # 优先计算已经站位的商品
        for product in productListA[1]:
            for seat in product.productSeatList:
                if for_max == 0:
                    break
                if hasattr(seat, "intersection"):
                    for_max -= 1
                    delattr(seat, "intersection")

        if for_max != 0:
            # 如果循环完还没有满足说明还要循环别的商品
            # 优先计算已经站位的商品
            for product in productListA[1]:
                for seat in product.productSeatList:
                    if for_max == 0:
                        break
                    if seat.is_run_other_pro != False and seat.seat == False:
                        for_max -= 1
                        seat.is_run_other_pro = bean.is_run_other_pro
                        # 是否与全场活动同时执行
                        seat.is_run_store_act = bean.is_run_store_act
                        seat.seat = True
                        seat.intersection2 = 1

def intersection(productListA):
    """
    找到组合1和组合2的交集商品
    :param productListA: 所有商品
    :return: 所有交集商品
    """
    response = []
    for product in productListA[0]:
        if product in productListA[1]:
            response.append(product)
    return response


def calculation_current(money, value_num):
    """

    :param money: 当前最大金额
    :param value_num:
    :return:
    """
    return money // value_num


def change_pro_qtty(productListA, for_max, bean):
    """
    更改商品站位信息(数量)
    :param productListA: 可以参与活动的商品
    :param for_max:  数量的最大循环次数
    :return:
    """

    for product in productListA:
        for seat in product.productSeatList:
            if for_max == 0:
                break
            if seat.seat == False and seat.is_run_other_pro != False:
                seat.is_run_other_pro = bean.is_run_other_pro
                # 是否与全场活动同时执行
                seat.is_run_store_act = bean.is_run_store_act
                seat.seat = True
                for_max -= 1


def change_pro_money(productListA, for_max, condition, max, result_moeny, bean):
    """
    更改商品站位信息(金额)
    :param productListA: 可以参与活动的商品
    :param for_max: 最大金额
    :param condition: 满足条件
    :param max: 当前倍数
    :param result_moeny
    :return:
    """
    result = result_moeny
    for product in productListA:
        for seat in product.productSeatList:
            if result // for_max > max:
                return result
            if seat.seat == False and seat.is_run_other_pro != False:
                seat.seat = True
                result += getattr(seat, condition)
                seat.is_run_other_pro = bean.is_run_other_pro
                # 是否与全场活动同时执行
                seat.is_run_store_act = bean.is_run_store_act
    return result


def repurchase(bean, for_max, productList):
    """
    宗旨每次进入更改一次最小倍数的站位信息
    :param bean: 活动
    :param for_max 最大循环次数
    :param productList: 所有商品
    :return: 返回所以换购条件的商品明细 并告诉是否完整执行完
    """
    response = []
    while True:
        if for_max == 0:
            break
        cur_response = calculate_fun(bean, productList)
        for i in cur_response:
            response.append(i)
        # 调用小霞姐写的函数
        for_max -= 1

    return response


def calculate_fun(bean, productList, groupnum=1, oldpro_list=[]):
    '''
    换购促销的计算方法 hexiaoxia
    :param bean: 一个换购促销对象
    :param productList: 录入所有商品列表对象
    :param groupnum: 当前是哪个倍数进来的倍数，从1开始（例如：某促销可以翻3倍，那么第一次进来传入1，第二次进来传入2，第三进来传入3，……
    :return:
    '''
    from pro.utils.linq import linq
    import pro.utils.util as util
    import copy

    n_productList = copy.deepcopy(productList)

    operation_set = bean.operation_set
    three_id = str(bean.prom_type_three).lower()
    target_item = bean.target_item
    purchase_way = "T"
    if three_id == "ga1505" or three_id == "ga1506":
        purchase_way = "J"
        operation_set = sorted(operation_set, key=lambda x: x.purchase_condition)  # 统一换购优惠或组合换购优惠执行顺序按照执行值升序排序
    else:
        if three_id == "ga1503" or three_id == "ga1504":
            purchase_way = "D"
        operation_set = sorted(operation_set, key=lambda x: x.purchase_condition, reverse=True)  # 其它换购活动执行顺序按照执行值降序排序
        # 李博文修改 在外排序

    calculate_list = []  # 换购商品计算后的，里面的pro_list是product 的class 对象
    swap_products = []  # 换购商品计算后列表,json格式
    operation_set_list = []  # 存放每个执行列表里一倍的商品明细列表
    # groupnum = 0
    pronum = 0
    give_value = operation_set[0].give_value
    one_item = {}
    one_item["one_multiple"] = False  # True 表示一倍计算完成；False 表示一倍没有计算完成
    for row in operation_set:
        old_pronum = 0
        if pronum >= int(give_value):
            break
        # groupnum += 1
        isnew = True
        oneprice = 0
        tamt_receivable = 0
        t_qtty = 0
        rownum = 0
        pro_list = []
        r_item = {}
        r_item["pcond_id"] = row.pcond_id
        if oldpro_list:
            for index, row3 in enumerate(oldpro_list):
                if row3["pcond_id"] == row.pcond_id and len(row3["pro_list"]) < give_value:
                    old_pronum = len(row3["pro_list"])
                    pro_list = row3["pro_list"]
                    isnew = False
                    break

        for row1_index, row1 in enumerate(n_productList):
            if pronum >= int(give_value):
                break
            row1pro = linq(row.product_list).where(lambda x: x["ECODE"] == row1.ecode).tolist().copy()
            if not row1pro:
                continue
            row1pro1 = linq(row1.productSeatList).where(
                lambda x: x.seat == False and x.is_run_other_pro == True).tolist().copy()
            if not row1pro1:
                continue
            for row2_index, row2 in enumerate(row1.productSeatList):
                if pronum < int(give_value):
                    if row2.seat == True or row2.is_run_other_pro == False:
                        continue
                    if target_item == "amt_retail":
                        tamt_receivable = tamt_receivable + row2.amt_retail
                        new_amtreceivable = row2.amt_retail
                    elif target_item == "amt_list":
                        tamt_receivable = tamt_receivable + row2.amt_list
                        new_amtreceivable = row2.amt_list
                    else:
                        tamt_receivable = tamt_receivable + row2.amt_receivable
                        new_amtreceivable = row2.amt_receivable
                    t_qtty = t_qtty + row2.qtty
                    row2.amt_receivable = new_amtreceivable
                    # row2_index = row1.productSeatList.index(row2)
                    if old_pronum >= int(give_value):
                        isnew = True
                        pro_list = []
                        old_pronum = 0
                    pro_list.append(row2)
                    row2.seat = True
                    productList[row1_index].productSeatList[row2_index].seat = True
                    productList[row1_index].productSeatList[row2_index].is_run_other_pro = False
                    productList[row1_index].productSeatList[row2_index].is_run_store_act = False
                    pronum += 1
                    old_pronum += 1
                else:
                    # TODO 站位有问题.. 当row2是True时候直接break了.
                    break
        if not pro_list:
            continue
        r_item["pro_list"] = pro_list
        if oldpro_list:
            if isnew:
                oldpro_list.append(r_item)
        else:
            operation_set_list.append(r_item)

    if pronum == int(give_value):
        one_item["one_multiple"] = True
    else:
        one_item["one_multiple"] = False

    one_item["pro_list"] = operation_set_list if not oldpro_list else oldpro_list
    calculate_list.append(one_item)

    if not calculate_list:
        return None
    else:
        # return {"calculate_list":calculate_list,"swap_products":swap_products}
        return calculate_list


def getNewPrice(bean, oldpro_list=[]):
    from pro.utils.linq import linq
    import pro.utils.util as util
    import copy

    swap_products = []
    operation_set = bean.operation_set
    give_value = operation_set[0].give_value
    three_id = str(bean.prom_type_three).lower()
    target_item = bean.target_item
    # TODO 全局变量
    swap_products_setrow = []
    purchase_way = "T"
    if three_id == "ga1505" or three_id == "ga1506":
        purchase_way = "J"
    else:
        if three_id == "ga1503" or three_id == "ga1504":
            purchase_way = "D"
    for row in operation_set:
        groupnum = 0
        purchase_condition = row.purchase_condition
        for index, row1 in enumerate(oldpro_list):
            if row1["pcond_id"] == row.pcond_id:

                groupnum += 1
                pro_list = row1["pro_list"]
                tamt_receivable = 0
                for row2 in row1["pro_list"]:
                    if target_item == "amt_retail":
                        tamt_receivable = tamt_receivable + row2.amt_retail
                        new_amtreceivable = row2.amt_retail
                    elif target_item == "amt_list":
                        tamt_receivable = tamt_receivable + row2.amt_list
                        new_amtreceivable = row2.amt_list
                    else:
                        tamt_receivable = tamt_receivable + row2.amt_receivable
                        new_amtreceivable = row2.amt_receivable
                if len(pro_list) > 1 and len(pro_list) <= give_value:
                    if len(pro_list) == give_value:
                        if purchase_way == "T":
                            newtamtreceivable = float(util.CalculationPrice(
                                tamt_receivable if float(purchase_condition) >= tamt_receivable else float(
                                    purchase_condition)))
                        elif purchase_way == "J":
                            new_price = float(util.CalculationPrice(util.minus(tamt_receivable, purchase_condition)))
                            newtamtreceivable = new_price if new_price >= 0 else 0
                        else:
                            newtamtreceivable = util.CalculationPrice(util.mul(tamt_receivable, purchase_condition))
                    else:
                        if purchase_way == "T":
                            newpurchase_condition = util.mul(
                                util.div(float(purchase_condition), give_value), len(pro_list))

                            newtamtreceivable = float(util.CalculationPrice(
                                tamt_receivable if float(
                                    newpurchase_condition) >= tamt_receivable else newpurchase_condition))
                        elif purchase_way == "J":
                            newpurchase_condition = util.mul(util.div(purchase_condition, give_value), len(pro_list))
                            new_price = float(util.CalculationPrice(util.minus(tamt_receivable, newpurchase_condition)))
                            newtamtreceivable = new_price if new_price >= 0 else 0
                        else:
                            newtamtreceivable = util.CalculationPrice(util.mul(tamt_receivable, purchase_condition))
                    if newtamtreceivable != tamt_receivable:
                        newdis = float(util.div(newtamtreceivable, tamt_receivable))
                        row_total_amt_receivable = 0
                        for index3, row3 in enumerate(pro_list):
                            row_swap_products = {}
                            row_swap_products = getRowitem(row3, row.pcond_id, groupnum, bean.id)
                            ReceivablePrice = float(util.mul(float(row3.amt_receivable), float(newdis)))  # 实收价
                            row3.amt_receivable = util.CalculationPrice(ReceivablePrice)
                            row_swap_products["amt_receivablea"] = row3.amt_receivable
                            swap_products_setrow.append(row_swap_products)
                            row_total_amt_receivable = row_total_amt_receivable + row3.amt_receivable
                        diff = util.CalculationPrice(
                            util.minus(newtamtreceivable,
                                       row_total_amt_receivable))  # ("%.2f" % (new_price-new_disprice)))
                        if abs(diff) > 0:
                            # 存在误差，误差分摊方法
                            ceil = 0.01  # 最小分摊单位目前写死按照保留两位小数的最小单位进位
                            old_diff = diff
                            while abs(float(diff)) > 0:
                                ceil = 0.01
                                if float(old_diff) < 0:
                                    ceil = -0.01
                                if (abs(diff) < abs(ceil)):
                                    diff = 0
                                    break
                                if abs(diff) >= abs(ceil):
                                    for i in range(len(pro_list)):
                                        if float(old_diff) < 0:
                                            if float(diff) > 0:
                                                diff = 0
                                        else:
                                            if float(diff) < 0:
                                                diff = 0
                                        if diff == 0:
                                            break

                                        if abs(diff) >= 10:
                                            ceil = 10
                                            if float(old_diff) < 0:
                                                ceil = -10
                                        elif 10 > abs(diff) >= 1:
                                            ceil = 1
                                            if float(old_diff) < 0:
                                                ceil = -1
                                        elif 0.1 <= abs(diff) < 1:
                                            ceil = 0.1
                                            if float(old_diff) < 0:
                                                ceil = -0.1
                                        if abs(diff) > 0 and float(pro_list[i].amt_receivable) / float(
                                                pro_list[i].amt_list) >= 1:
                                            continue
                                        oldqty = int(pro_list[i].qtty)
                                        oldprice = float(
                                            "%.2f" % float(util.mul(pro_list[i].amt_receivable, pro_list[i].qtty)))
                                        if diff < 0:
                                            if len(pro_list) == 1:
                                                if oldprice <= 0:
                                                    diff = 0
                                                    break
                                                else:
                                                    if ceil < 0 and oldprice < abs(ceil):
                                                        diff = 0
                                                        break
                                            else:
                                                if oldprice <= 0:
                                                    continue
                                                else:
                                                    if ceil < 0 and oldprice < abs(ceil):
                                                        continue
                                        ReceivablePrice = float(util.add(float(pro_list[i].amt_receivable), ceil))
                                        diff = float("%.2f" % float(util.minus(diff, util.mul(ceil, oldqty))))
                                        pro_list[i].amt_receivable = util.CalculationPrice(ReceivablePrice)
                                        if diff == 0:
                                            break
                                else:
                                    diff = 0

                            # 误差分摊结束，重新设置存放计算后商品列表里的商品应收价
                            for index4, row4 in enumerate(pro_list):
                                row4_index = pro_list.index(row4)
                                swap_products_setrow[row4_index]["amt_receivablea"] = row4.amt_receivable
                    # TODO 李博文增加当应收价小于特价值时直接返回product_list
                    else:
                        for index3, row3 in enumerate(pro_list):
                            row_swap_products = {}
                            row_swap_products = getRowitem(row3, row.pcond_id, groupnum, bean.id)
                            row_swap_products["amt_receivablea"] = row3.amt_receivable
                            swap_products_setrow.append(row_swap_products)

                else:
                    row_swap_products = {}
                    row_swap_products = getRowitem(pro_list[0], row.pcond_id, groupnum, bean.id)
                    if purchase_way == "T" or purchase_way == "J":  # 特价 或 优惠
                        oneprice = float(util.CalculationPrice(util.div(purchase_condition, give_value)))
                        if purchase_way == "T":
                            pro_list[0].amt_receivable = oneprice if oneprice < float(pro_list[0].amt_receivable) else \
                                pro_list[
                                    0].amt_receivable
                        else:
                            new_price = float(util.CalculationPrice(util.minus(pro_list[0].amt_receivable, oneprice)))
                            pro_list[0].amt_receivable = new_price if new_price >= 0 else 0
                    else:  # 打折
                        pro_list[0].amt_receivable = float(
                            util.CalculationPrice(util.mul(purchase_condition, pro_list[0].amt_receivable)))
                    row_swap_products["amt_receivablea"] = pro_list[0].amt_receivable
                    swap_products_setrow.append(row_swap_products)
            # TODO 李博文改的
            if swap_products_setrow:
                for row4 in swap_products_setrow:
                    # if row4 not in swap_products:
                    swap_products.append(row4)
                swap_products_setrow = []
    return swap_products


def getRowitem(row, pcond_id, groupnum, id):
    row_swap_products = {}
    row_swap_products["ecode"] = row.ecode
    row_swap_products["sku"] = row.sku
    row_swap_products["lineno"] = row.lineno
    row_swap_products["amt_receivableb"] = row.amt_receivable
    row_swap_products["qtty"] = row.qtty
    row_swap_products["pcond_id"] = pcond_id
    row_swap_products["groupnum"] = groupnum
    # 修改， 因为append方法执行后没有返回值（None）， 所以执行set会出错
    # row_swap_products["ga_dis"] = list(set(row.discountId.append(id))) if len(row.discountId) > 0 else [id]
    if type(row.discountId) == list:
        row.discountId.append(id)
        row_swap_products["ga_dis"] = list(set(row.discountId))
    else:
        row_swap_products["ga_dis"] = [id]
    row_swap_products["pa_dis"] = []
    row_swap_products["amt_receivablea"] = row.amt_receivable
    return row_swap_products


def getCp_number(bean, productList):
    """
    统计换购商品的数量
    :param bean: 活动
    :param productList: 所有商品
    :return: 换购商品未站位的数量
    """
    result = 0
    for product in productList:
        for promotion in bean.operation_set:
            if product.ecode.lower() == promotion.product_list['ECODE']:
                for seat in product.productSeatList:
                    if seat.seat == False and seat.is_run_other_pro == True:
                        result += 1
    return result


def min_pro_pro2_max(pro, pro2, last_time):
    """
    判断当前倍数谁的最小 并且减去上次最大倍数计算出当前可以循环更改几次换购商品站位
    :param pro: 组合1的倍数
    :param pro2: 组合2的倍数
    :param last_time: 上次循环的最大倍数
    :return: 可以进入几次循环更改换购详细信息
    """

    cur_max = min(pro, pro2)

    return cur_max - last_time


def re_response(bean, response_cp, max):
    """
    单品和组合的返回方式不一样所以要单独构造单品的返回值
    :param bean:  活动
    :param response_cp: 换购商品明细
    :param max: 倍数
    :return:
    """
    if hasattr(bean, "specific_activities"):
        return {"id": bean.id, "qtty": max * bean.operation_set[0].give_value, "times": max,
                "bsc_qtty": bean.operation_set[0].give_value}, response_cp
    else:
        return {"id": bean.id, "qtty": max * bean.operation_set[0].give_value, "times": max,
                "bsc_qtty": bean.operation_set[0].give_value}, response_cp


def findIndexBySku(productList, product):
    for idx, value in enumerate(productList):
        if value.sku == product.sku:
            return idx
    return -1


def result_max_ge_CurResult(bean, max, productListA, result_moeny, condition):
    """
    计算当前倍数是否大于上次循环倍数
    :param bean:
    :param max:
    :param productListA:
    :param result_moeny:
    :return:
    """

    for product in productListA:
        for seat in product.productSeatList:
            if result_moeny // bean.value_num > max:
                return "ok"
            if seat.seat == False and seat.is_run_other_pro == True:
                result_moeny += getattr(seat, condition)
    if result_moeny // bean.value_num > max:
        return "ok"
    else:
        return None


def result_max_ge_CurResult_combination(condition_money, max, productListA, result_moeny, condition, number):
    """
    判断组合商品金额是否大于当前倍数
    :param condition_money: 满足条件的金额
    :param max: 倍数
    :param productListA:可以参与活动的商品
    :param result_moeny: 当前金额
    :param condition: 满足条件
    :param number: 控制是组合2还是组合1用于判断
    :return:
    """

    for product in productListA:
        for seat in product.productSeatList:
            if result_moeny // condition_money > max:
                return "ok"
            if seat.seat == False and seat.is_run_other_pro == True:
                result_moeny += getattr(seat, condition)
            if number == 1:
                if hasattr(seat, "intersection2"):
                    result_moeny += getattr(seat, condition)

    if result_moeny // condition_money > max:
        return "ok"
    else:
        return "off"


def intersection_qtty(value_num, productListA):
    """
    只针对有交集组合
    判断商品是否满足当前活动
    :param value_num: 比较值(数量)
    :param productListA: 可以参与的商品
    :return: 满足ok 不满足off
    """

    promotion_qtty_sum, _, _, _ = tongji(
        productListA)
    if promotion_qtty_sum >= value_num:
        return "ok"
    else:
        return "off"