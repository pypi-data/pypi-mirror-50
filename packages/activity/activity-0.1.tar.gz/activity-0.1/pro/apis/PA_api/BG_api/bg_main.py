# -*- coding:utf-8 -*-
# author:李旭辉
# datetime:2018/10/23 9:36
'''
添加线上、线上排名买赠活动执行
20190716
'''
import copy
import pro.utils.util as util
from pro.apis.entitys.products_entitys.product import *
from pro.apis.entitys.PA_entitys.promotion_entity import *
import math

def executebuygifts(productList, buygifts, userInfo, nodis_products):
    '''
    全场活动买赠类的活动具体计算入口
    :param productList: 参与计算的商品
    :param buygifts: 全场买赠活动
    :param userInfo: 会员
    :return:
    '''
    newproduct = {}
    ifvipdis = True
    try:
        type_three = buygifts.prom_type_three.upper()
        if buygifts.target_item.lower()=="amt_receivable":
            productList = sorted(productList, key=lambda x: x.amt_receivable,reverse=True) #按照应收价格降序
        elif buygifts.target_item.lower()=="amt_list":
            productList = sorted(productList, key=lambda x: x.amt_list, reverse=True)  # 按照吊牌价格降序
        elif buygifts.target_item.lower() == "amt_retail":
            productList = sorted(productList, key=lambda x: x.amt_retail, reverse=True)  # 按照零售价格降序
        if type_three == "PA1301":
            # 统一买赠
            newproduct = unifybuygifts(productList, buygifts, nodis_products)
        elif type_three == "PA1302":
            # 梯度买赠
            newproduct = incrementalbg(productList, buygifts, nodis_products)
        elif type_three=="PA1602" or type_three=="PA1702":
            #线上、线上排名梯度买赠
            newproduct = incrementalbg_online(productList, buygifts)
        elif type_three == "PA1601" or type_three == "PA1701":
            #线上、线上排名统一买赠
            newproduct = unifybuygifts_online(productList, buygifts, nodis_products)
        # elif type_three == "PA1303":
        #     #统一送券
        #     newproduct=unifycoupon(productList,buygifts)
        # elif type_three == "PA1303":
        #     #梯度送券
        #     newproduct=incrementalcoupon(productList,buygifts)
        if newproduct and newproduct.get("disproductList"):
            #重新计算单据总金额
            new_total_amt_receivable=0
            for row in newproduct["disproductList"]:
                if buygifts.id not in row.fulldiscountID:
                    row.fulldiscountID.append(buygifts.id)
                for row1 in row.productSeatList:
                    new_total_amt_receivable=new_total_amt_receivable+float(row1.amt_receivable)
                    if row1.is_run_vip_discount:
                        ifvipdis = False
            newproduct["total_amt_receivable"]=new_total_amt_receivable
            newproduct["new_total_amt_receivable"]=new_total_amt_receivable
            newproduct["total_oldamt_receivable"] = new_total_amt_receivable
            # 执行VIP折上折
            isvipdis = False
            # 当用户数据不为空且
            if buygifts.is_run_vip_discount and userInfo is not None and ifvipdis and userInfo.id != -1 \
                    and userInfo.id is not None:
                if buygifts.members_only:
                    if userInfo.id in buygifts.members_group and userInfo.discount is not None:
                        newproduct["total_amt_receivable"] = util.CalculationPrice(util.mul(newproduct["total_amt_receivable"], userInfo.discount))
                        newproduct["new_total_amt_receivable"] = newproduct["total_amt_receivable"]
                        isvipdis = True
                else:
                    if userInfo.discount is not None:
                        newproduct["total_amt_receivable"] = util.CalculationPrice(util.mul(newproduct["total_amt_receivable"], userInfo.discount))
                        newproduct["new_total_amt_receivable"] = newproduct["total_amt_receivable"]
                        isvipdis = True
            if isvipdis:
                newproduct["isCalculation"] = "N"
                for row in newproduct["disproductList"]:
                    for row1 in row.productSeatList:
                        if row1.is_buy_gifts=='n':
                            row1.fulldiscounts.append(buygifts.id)
                        row1.is_run_vip_discount = True



    except Exception as e:
        newproduct = {}

    return newproduct


def unifybuygifts(productList, buygifts, nodis):
    '''
    全场活动统一买赠计算
    :param productList: 参与的商品信息
    :param buygifts: 全场活动信息
    :param gifts:赠品信息
    :return: 返回包含计算得到的新的总应收金额的结果
    '''
    try:
        give_max_pronum = 0  # 赠送商品总数量
        give_max_amtlist = 0  # 赠送商品总金额
        target_type = buygifts.target_type  # 获取比较条件
        operation_set = buygifts.operation_set[0]  # 获取比较整体列表
        comp_symb_type = operation_set.get("comp_symb_type", "ge").lower()  # 比较符
        value_num = operation_set.get("value_num", 1)  # 比较值
        buygifts_value = operation_set["buy_gifts"]
        newproduct = setproductlist(productList, target_type)
        v_comparison = newproduct["v_comparison"]
        isbg =checkdis(comp_symb_type, v_comparison, value_num, target_type)
        if isbg:
            bg = {}
            operations = []
            # gifts_ecodes, gifts, ecode_sum_not, ecode_sum, ecode_sum_not_one, ecode_sum_one = details(newproduct,
            #                                                                                           buygifts_value,
            #                                                                                           target_type)
            gifts_ecodes, gifts, ecode_sum_not, ecode_sum, ecode_sum_not_one, ecode_sum_one = \
                caculate_product_infos(newproduct, buygifts_value, target_type, nodis)

            give_value = buygifts_value['give_value']
            if comp_symb_type == "g":
                value_num = value_num + 1
            else:
                value_num = value_num
            # 计算不是交集的商品（包括是赠品但是不可参与计算的商品）现在的可翻倍数
            now_times = ecode_sum_not // value_num
            is_complate = False  # 是否已经计算完成
            current_give_value_num = now_times * give_value  # 当前赠品数
            give_max_pronum = 0  # 最大赠品数
            give_max_amtlist = 0  # 最大赠品金额
            if now_times > 0:  # 当当前倍数大于0时， 标记赠品。
                # 首先判断当前促销的翻倍次数限制
                if buygifts.max_times == 0 or buygifts.max_times is None:
                    now_times = 1
                    is_complate = True  # 说明当前已达到最大翻倍次数
                elif buygifts.max_times > 0 and now_times > buygifts.max_times:
                    now_times = buygifts.max_times
                    is_complate = True  # 说明当前已达到最大翻倍次数

                current_give_value_num = now_times * give_value
                # 占位当前赠品
                current_give_max_pronum, current_give_max_amtlist, gifts = gift_mark(current_give_value_num,
                                                                                     gifts, buygifts)
                give_max_pronum += current_give_max_pronum
                give_max_amtlist += current_give_max_amtlist
                if give_max_pronum < current_give_value_num or (not gifts):
                    # 说明当前赠品已经占完， 计算完成
                    is_complate = True
            if not is_complate and ecode_sum != 0 and gifts:
                # 如果当前还未计算完成且当前交集商品不为0的话， 说明可以继续计算
                new_ecode_sum_not = ecode_sum_not
                while not is_complate:
                    # 当所有计算已经完成， 退出循环
                    condition_gift_list = []  # 当前作为条件的商品
                    gifts = sorted(gifts, key=lambda x: x.amt_receivable, reverse=True)  # 按照应收价降序占位条件
                    for gift in gifts:
                        if not gift.no_pur_seat:
                            # 当赠品属于可以作为条件的商品时， 才参与条件计算
                            if target_type == "qtty":
                                new_ecode_sum_not += 1
                            elif target_type == "amt_list":
                                new_ecode_sum_not += gift.amt_list
                            elif target_type == "amt_retail":
                                new_ecode_sum_not += gift.amt_retail
                            else:
                                new_ecode_sum_not += gift.amt_receivable
                            condition_gift_list.append(gift)

                        if new_ecode_sum_not // value_num > now_times:
                            # 当当前条件已经达到一倍（大于上次计算出来的倍数）， 结束当前倍数计算
                            break
                    current_max_times = new_ecode_sum_not // value_num  # 当前的最大倍数
                    if current_max_times <= now_times:
                        # 如果当前计算出来的倍数不大于上次的倍数时， 说明已经达到最大翻倍次数，结束循环
                        break
                    for item in condition_gift_list:
                        # 将作为条件的三个品从赠品列表中剔除
                        gifts.remove(item)
                    # 促销翻倍次数限制
                    if buygifts.max_times == 0 or buygifts.max_times is None:
                        current_max_times = 1
                        is_complate = True
                    elif buygifts.max_times > 0 and current_max_times >= buygifts.max_times:
                        current_max_times = buygifts.max_times
                        is_complate = True
                    current_give_value_num = (current_max_times - now_times) * give_value
                    # 占位当前倍数的赠品
                    current_give_max_pronum, current_give_max_amtlist, gifts = gift_mark(current_give_value_num,
                                                                                         gifts, buygifts)
                    give_max_pronum += current_give_max_pronum
                    give_max_amtlist += current_give_max_amtlist
                    if give_max_pronum < current_max_times * give_value or (not gifts):
                        # 当赠品没有时，说明已经达到最大翻倍次数，
                        is_complate = True
                    now_times = current_max_times

            buygifts_value['give_value'] = now_times * give_value  # 当前可送赠品

            # 以前的方法，现在暂时不用
            # if ecode_sum == 0:
            #     buygifts_value['give_value'] = notAforA_times(buygifts, value_num, buygifts_value, newproduct,
            #                                                   target_type)
            #     if newproduct['total_' + target_type] >= value_num:
            #         give_max_pronum, give_max_amtlist =notAforA_mark(buygifts_value, nodis, gifts_ecodes, buygifts)
            # if ecode_sum != 0:
            #     # 当在赠品列表中的可参加活动商品数量-赠送值+不在赠品列表中的可参加活动商品数量>=比较值时，遍历可参加策略的商品明细，判断其是否为赠品，若为赠品则继续遍历，如不是则查询其是否在赠品编码列表里，如有则标记其为赠品
            #     num1 = 0
            #     if target_type == "qtty":
            #         num1, buygifts_value["give_value"] = isAforA_qtty(num1, value_num, buygifts, give_value,
            #                                                           buygifts_value, ecode_sum, ecode_sum_not)
            #         if ecode_sum + ecode_sum_not - num1 >= value_num:
            #             give_max_pronum, give_max_amtlist =isAforA_mark(num1, gifts, buygifts)
            #     else:
            #         num1, buygifts_value["give_value"] = isAforA_money(num1, buygifts, give_value, value_num,
            #                                                            buygifts_value, ecode_sum_not, ecode_sum_one,
            #                                                            ecode_sum, ecode_sum_not_one)
            #         if ecode_sum + ecode_sum_not - sum(ecode_sum_one[-int(num1):]) >= value_num:
            #             give_max_pronum, give_max_amtlist =isAforA_mark(num1, gifts, buygifts)
            if ecode_sum + ecode_sum_not >= value_num:
                operations.append(operation_set)

            # 添加活动id和赠送值以及满足条件的活动执行方案到返回字典中
            bg["id"] = buygifts.id
            bg["give_value"] = buygifts_value['give_value']
            bg["operations"] = operations
            newproduct["gifts_ecodes"]=gifts_ecodes
            # 标记其为可执行活动
            newproduct["keepdis"] = "Y"
            # 将bg返回
            newproduct["bg"] = bg
            # 标记其不能进行分摊
            newproduct["isCalculation"] = "Y"
            newproduct["buygift"] = "Y"
            newproduct["give_max_pronum"] = give_max_pronum  # 赠送商品总数量
            newproduct["give_max_amtlist"] = give_max_amtlist  # 赠送商品总金额
            return newproduct
        else:
            return {"keepdis": "N"}
    except Exception as e:
        return {}


def unifybuygifts_online(productList, buygifts, nodis):
    '''
    全场活动-线上统一买赠计算
    :param productList: 参与的商品信息
    :param buygifts: 全场活动信息
    :return: 返回包含计算得到的新的总应收金额的结果
    '''
    try:
        target_type = buygifts.target_type  # 获取比较条件
        operation_sets = buygifts.specific_activities[0].operation_set
        operation_set = operation_sets[0]  # 获取比较整体列表
        comp_symb_type = (buygifts.specific_activities[0].comp_symb_type).lower()  # 比较符
        value_num = buygifts.specific_activities[0].value_num  # 比较值
        bean_max_times = buygifts.max_times
        newproduct = setproductlist(productList, target_type)
        v_comparison = newproduct["v_comparison"]
        max_double_times = caculate_max_times(comp_symb_type, v_comparison, value_num, target_type,
                                              bean_max_times)
        if max_double_times > 0:
            # 说明可以执行促销
            # 根据最大翻倍次数，计算可以赠送的商品
            all_give_products, give_max_pronum, give_max_amtlist, all_give_infos = caculate_buygift_info_online(
                buygifts, operation_sets, max_double_times, nodis)
            disproductList = newproduct["disproductList"]
            for item in all_give_products:
                disproductList.append(item)
            newproduct["disproductList"] = disproductList
            newproduct["give_max_pronum"] = give_max_pronum  # 线上赠送商品总数量
            newproduct["give_max_amtlist"] = give_max_amtlist  # 线上赠送商品总金额
            newproduct["max_double_times"] = max_double_times
            newproduct["isCalculation"] = "Y"
            newproduct["keepdis"] = "Y"
            newproduct["buygift"] = "Y"
            return newproduct
        else:
            # 说明无法执行此促销
            return {"keepdis": "N"}
    except Exception as e:
        return {}

def incrementalbg(productList, buygifts, nodis):
    '''
    全场活动梯度买赠计算
    :param productList: 参与的商品信息
    :param buygifts: 全场活动信息
    :return: 返回包含计算得到的新的总应收金额的结果
    '''

    try:
        give_max_pronum = 0  # 赠送商品总数量
        give_max_amtlist = 0  # 赠送商品总金额
        target_type = buygifts.target_type
        operation_set = buygifts.operation_set
        # 将各梯度以比较值降序排列
        operation_set = sorted(operation_set, key=lambda x: x.get('value_num'), reverse=True)
        newproduct = setproductlist(productList, target_type)
        v_comparison = newproduct["v_comparison"]
        maxoperation_set = {}
        for operation in operation_set:
            comp_symb_type = operation.get("comp_symb_type", "ge").lower()  # 比较符
            value_num = operation.get("value_num", 0)  # 比较值
            if comp_symb_type == "ge":
                if v_comparison >= float(value_num):
                    maxoperation_set = operation
            elif comp_symb_type == "g":
                if v_comparison > float(value_num):
                    maxoperation_set = operation
            elif comp_symb_type == "e":
                if value_num == 0 and target_type == "qtty":
                    maxoperation_set = None
                if v_comparison >= float(value_num):
                    maxoperation_set = operation
            if maxoperation_set:
                break
        if maxoperation_set:
            bg = {}
            operations = []
            operation = maxoperation_set
            if operation['comp_symb_type'].lower() == "g":
                value_num = operation['value_num'] + 1
                # maxvalue_num = operation_set[0]['value_num']+1
            else:
                value_num = operation['value_num']
                #maxvalue_num = operation_set[0]['value_num']
            buygifts_value = operation['buy_gifts']
            gifts_ecodes, gifts, ecode_sum_not, ecode_sum, ecode_sum_not_one, ecode_sum_one = \
                caculate_product_infos(newproduct, buygifts_value, target_type, nodis)

            give_value = buygifts_value['give_value']

            # 计算不是交集的商品（包括是赠品但是不可参与计算的商品）现在的可翻倍数
            now_times = ecode_sum_not // value_num
            is_complate = False  # 是否已经计算完成
            current_give_value_num = now_times * give_value  # 当前赠品数
            give_max_pronum = 0  # 最大赠品数
            give_max_amtlist = 0  # 最大赠品金额
            if now_times > 0:  # 当当前倍数大于0时， 标记赠品。
                # 首先判断当前促销的翻倍次数限制
                if buygifts.max_times == 0 or buygifts.max_times is None:
                    now_times = 1
                    is_complate = True  # 说明当前已达到最大翻倍次数
                elif buygifts.max_times > 0 and now_times > buygifts.max_times:
                    now_times = buygifts.max_times
                    is_complate = True  # 说明当前已达到最大翻倍次数
                current_give_value_num = now_times * give_value
                # 占位当前赠品
                current_give_max_pronum, current_give_max_amtlist, gifts = gift_mark(current_give_value_num,
                                                                                     gifts, buygifts)
                give_max_pronum += current_give_max_pronum
                give_max_amtlist += current_give_max_amtlist
                if give_max_pronum < current_give_value_num or (not gifts):
                    # 说明当前赠品已经占完， 计算完成
                    is_complate = True
            if not is_complate and ecode_sum != 0 and gifts:
                # 如果当前还未计算完成且当前交集商品不为0的话， 说明可以继续计算
                new_ecode_sum_not = ecode_sum_not
                while not is_complate:
                    # 当所有计算已经完成， 退出循环
                    condition_gift_list = []  # 当前作为条件的商品
                    gifts = sorted(gifts, key=lambda x: x.amt_receivable, reverse=True)  # 按照应收价降序占位条件
                    for gift in gifts:
                        if not gift.no_pur_seat:
                            # 当赠品属于可以作为条件的商品时， 才参与条件计算
                            if target_type == "qtty":
                                new_ecode_sum_not += 1
                            elif target_type == "amt_list":
                                new_ecode_sum_not += gift.amt_list
                            elif target_type == "amt_retail":
                                new_ecode_sum_not += gift.amt_retail
                            else:
                                new_ecode_sum_not += gift.amt_receivable
                            condition_gift_list.append(gift)

                        if new_ecode_sum_not // value_num > now_times:
                            # 当当前条件已经达到一倍（大于上次计算出来的倍数）， 结束当前倍数计算
                            break
                    current_max_times = new_ecode_sum_not // value_num  # 当前的最大倍数
                    if current_max_times <= now_times:
                        # 如果当前计算出来的倍数不大于上次的倍数时， 说明已经达到最大翻倍次数，结束循环
                        break
                    for item in condition_gift_list:
                        # 将作为条件的三个品从赠品列表中剔除
                        gifts.remove(item)
                    # 促销翻倍次数限制
                    if buygifts.max_times == 0 or buygifts.max_times is None:
                        current_max_times = 1
                        is_complate = True
                    elif buygifts.max_times > 0 and current_max_times >= buygifts.max_times:
                        current_max_times = buygifts.max_times
                        is_complate = True
                    current_give_value_num = (current_max_times - now_times) * give_value
                    # 占位当前倍数的赠品
                    current_give_max_pronum, current_give_max_amtlist, gifts = gift_mark(current_give_value_num,
                                                                                         gifts, buygifts)
                    give_max_pronum += current_give_max_pronum
                    give_max_amtlist += current_give_max_amtlist
                    if give_max_pronum < current_max_times * give_value or (not gifts):
                        # 当赠品没有时，说明已经达到最大翻倍次数，
                        is_complate = True
                    now_times = current_max_times

            buygifts_value['give_value'] = now_times * give_value  # 当前可送赠品
            newproduct["buygifts_value"] = buygifts_value
            newproduct["buygifts_value"]["list_sort"] = operation['promotion_lineno']

            # 原来的方法， 现不使用
            # operation=maxoperation_set
            # if operation['value_num'] != 0 and operation['comp_symb_type'].lower() == "g":
            #     value_num_now = operation['value_num'] + 1
            #     maxvalue_num = operation_set[0]['value_num']+1
            # else:
            #     value_num_now = operation['value_num']
            #     maxvalue_num = operation_set[0]['value_num']
            # buygifts_value = operation['buy_gifts']
            # give_value = buygifts_value['give_value']
            # gifts_ecodes, gifts, ecode_sum_not, ecode_sum, ecode_sum_not_one, ecode_sum_one = details(newproduct, buygifts_value, target_type)
            # if ecode_sum == 0:
            #     buygifts_value['give_value'] = tidu_notAforA_times(newproduct, target_type, maxvalue_num,
            #                                                                buygifts, buygifts_value, operation)
            #     newproduct["buygifts_value"] = buygifts_value
            #     newproduct["buygifts_value"]["list_sort"] = operation['promotion_lineno']
            #     if newproduct['total_' + target_type] >= value_num_now:
            #         give_max_pronum, give_max_amtlist =notAforA_mark(buygifts_value, nodis, gifts_ecodes, buygifts)
            # if ecode_sum != 0:
            #     num1 = 0
            #     if target_type == "qtty":
            #         if newproduct['total_' + target_type] >= maxvalue_num:
            #             num1, buygifts_value["give_value"] = isAforA_qtty(num1, maxvalue_num, buygifts,
            #                                                                       give_value, buygifts_value, ecode_sum,
            #                                                                       ecode_sum_not)
            #         elif newproduct['total_' + target_type] < maxvalue_num:
            #             num1 = give_value
            #             buygifts_value["give_value"] = give_value
            #         if ecode_sum + ecode_sum_not - num1 >= value_num_now:
            #             give_max_pronum, give_max_amtlist =isAforA_mark(num1, gifts, buygifts)
            #     else:
            #         if newproduct['total_' + target_type] >= maxvalue_num:
            #             num1, buygifts_value["give_value"] = isAforA_money(num1, buygifts, give_value,
            #                                                                        maxvalue_num, buygifts_value,
            #                                                                        ecode_sum_not, ecode_sum_one,
            #                                                                        ecode_sum, ecode_sum_not_one)
            #         elif newproduct['total_' + target_type] < maxvalue_num:
            #             num1 = give_value
            #             buygifts_value["give_value"] = buygifts_value['give_value']
            #         if ecode_sum + ecode_sum_not - sum(ecode_sum_one[-int(num1):]) >= value_num_now:
            #             give_max_pronum, give_max_amtlist =isAforA_mark(num1, gifts, buygifts)
            for operation in operation_set:
                if operation['value_num'] != 0 and operation['comp_symb_type'].lower() == "g":
                    value_num = operation['value_num'] + 1
                else:
                    value_num = operation['value_num']
                if ecode_sum + ecode_sum_not >= value_num:
                    operations.append(operation)
                    if "id" not in bg:
                        bg["id"] = buygifts.id
                        bg["give_value"] = buygifts_value['give_value']
            bg["operations"] = operations
            newproduct["bg"] = bg
            newproduct["gifts_ecodes"] = gifts_ecodes
            newproduct["isCalculation"] = "Y"
            newproduct["keepdis"] = "Y"
            newproduct["buygift"] = "Y"
            newproduct["give_max_pronum"] = give_max_pronum  # 赠送商品总数量
            newproduct["give_max_amtlist"] = give_max_amtlist  # 赠送商品总金额
            return newproduct
        else:
            return {"keepdis": "N"}
    except Exception as e:
        return {}


def setproductlist(productList, target_type):
    t_productl = {}
    v_comparison = 0
    total_amt_list = 0  # 当前参与策略的所有商品的总吊牌金额
    total_amt_retail = 0  # 当前参与策略的所有商品的总零售金额
    total_amt_receivable = 0  # 当前参与策略的所有商品的总应收金额
    total_qtty = 0  # 记录当前参与该策略的总商品数量
    t_productl["disproductList"] = copy.deepcopy(productList)
    for row in productList:
        if target_type == "qtty":
            v_comparison = v_comparison + int(row.qtty)
        elif target_type == "amt_list":
            # 吊牌金额
            v_comparison = v_comparison + float(row.total_amt_list)
        elif target_type == "amt_retail":
            # 零售金额
            v_comparison = v_comparison + float(row.total_amt_retail)
        elif target_type == "amt_receivable":
            # 应收金额
            v_comparison = v_comparison + float(row.total_amt_receivable)
        total_amt_list = total_amt_list + float(row.total_amt_list)
        total_amt_retail = total_amt_retail + float(row.total_amt_retail)
        total_amt_receivable = total_amt_receivable + float(row.total_amt_receivable)
        total_qtty = total_qtty + int(row.qtty)
    t_productl["v_comparison"] = v_comparison
    t_productl["total_amt_list"] = total_amt_list
    t_productl["total_amt_retail"] = total_amt_retail
    t_productl["total_amt_receivable"] = total_amt_receivable  # 参与策略的总应收金额
    t_productl["total_oldamt_receivable"] = total_amt_receivable
    t_productl["total_qtty"] = total_qtty
    return t_productl


def details(newproduct, buygifts_value, target_type):
    gifts_ecodes = []
    gifts = []

    newproduct["buygifts_value"] = buygifts_value
    give_value = buygifts_value['give_value']
    # 遍历赠品列表，将赠品的商品编码放在一起，等待比较
    for gift in buygifts_value["product_list"]:
        gifts_ecodes.append(gift['ecode'])
    for gift in buygifts_value["product_list"]:
        for product1 in newproduct["disproductList"]:
            seat1 = product1.productSeatList
            for row1 in seat1:
                if row1.ecode == gift['ecode']:
                    gifts.append(row1)
    # 计算在赠品列表中的可参加活动商品数量和不在赠品列表中的可参加活动商品数量
    ecode_sum_not = 0
    ecode_sum = 0
    ecode_sum_not_one = []
    ecode_sum_one = []
    if target_type == "qtty":
        for product1 in newproduct["disproductList"]:
            seat1 = product1.productSeatList
            for row1 in seat1:
                if row1.ecode not in gifts_ecodes:
                    ecode_sum_not += row1.qtty
                    ecode_sum_not_one.append(row1.amt_receivable)
                if row1.ecode in gifts_ecodes:
                    if row1.is_discount == "y":
                        ecode_sum += row1.qtty
                        ecode_sum_one.append(row1.amt_receivable)
                    else:
                        ecode_sum_not += row1.qtty
                        ecode_sum_not_one.append(row1.amt_receivable)
    if target_type == "amt_list":
        for product1 in newproduct["disproductList"]:
            seat1 = product1.productSeatList
            for row1 in seat1:
                if row1.ecode not in gifts_ecodes:
                    ecode_sum_not += row1.amt_list
                    ecode_sum_not_one.append(row1.amt_list)
                if row1.ecode in gifts_ecodes:
                    if row1.is_discount == "y":
                        ecode_sum += row1.amt_list
                        ecode_sum_one.append(row1.amt_list)
                    else:
                        ecode_sum_not += row1.amt_list
                        ecode_sum_not_one.append(row1.amt_list)
    if target_type == "amt_retail":
        for product1 in newproduct["disproductList"]:
            seat1 = product1.productSeatList
            for row1 in seat1:
                if row1.ecode not in gifts_ecodes:
                    ecode_sum_not += row1.amt_retail
                    ecode_sum_not_one.append(row1.amt_retail)
                if row1.ecode in gifts_ecodes:
                    if row1.is_discount == "y":
                        ecode_sum += row1.amt_retail
                        ecode_sum_one.append(row1.amt_retail)
                    else:
                        ecode_sum_not += row1.amt_retail
                        ecode_sum_not_one.append(row1.amt_retail)
    if target_type == "amt_receivable":
        for product1 in newproduct["disproductList"]:
            seat1 = product1.productSeatList
            for row1 in seat1:
                if row1.ecode not in gifts_ecodes:
                    ecode_sum_not += row1.amt_receivable
                    ecode_sum_not_one.append(row1.amt_receivable)
                if row1.ecode in gifts_ecodes:
                    if row1.is_discount == "y":
                        ecode_sum += row1.amt_receivable
                        ecode_sum_one.append(row1.amt_receivable)
                    else:
                        ecode_sum_not += row1.amt_receivable
                        ecode_sum_not_one.append(row1.amt_receivable)
    return [gifts_ecodes, gifts, ecode_sum_not, ecode_sum, ecode_sum_not_one, ecode_sum_one]


def details_new(newproduct, buygifts_value, target_type, nodis_products):
    gifts_ecodes = []
    gifts = []

    newproduct["buygifts_value"] = buygifts_value
    give_value = buygifts_value['give_value']
    # 遍历赠品列表，将赠品的商品编码放在一起，等待比较
    for gift in buygifts_value["product_list"]:
        gifts_ecodes.append(gift['ecode'])
    current_gifts_ecodes = []

    for product1 in newproduct["disproductList"] + nodis_products:
        if product1.ecode not in gifts_ecodes:
            continue
        seat1 = product1.productSeatList
        if seat1 and seat1[0].is_discount == "n":
            continue
        if product1.ecode not in current_gifts_ecodes:
            current_gifts_ecodes.append(product1.ecode)
        for row1 in seat1:
            gifts.append(row1)
    # 计算在赠品列表中的可参加活动商品数量和不在赠品列表中的可参加活动商品数量
    for item in nodis_products:
        for row1 in item.productSeatList:
            row1.no_pur_seat = True
    all_product_list = newproduct["disproductList"] + nodis_products
    all_product_list = sorted(all_product_list, key=lambda i: i.productSeatList[0].amt_receivable, reverse=True)
    ecode_sum_not = 0
    ecode_sum = 0
    ecode_sum_not_one = []
    ecode_sum_one = []
    if target_type == "qtty":
        for product1 in all_product_list:
            seat1 = product1.productSeatList
            for row1 in seat1:
                if row1.no_pur_seat:
                    ecode_sum_one.append(0)
                else:
                    if row1.ecode not in gifts_ecodes:
                        ecode_sum_not += row1.qtty
                        ecode_sum_not_one.append(row1.amt_receivable)
                    if row1.ecode in gifts_ecodes:
                        ecode_sum += row1.qtty
                        ecode_sum_one.append(1)
    if target_type == "amt_list":
        for product1 in all_product_list:
            seat1 = product1.productSeatList
            for row1 in seat1:
                if row1.no_pur_seat:
                    ecode_sum_one.append(0)
                else:
                    if row1.ecode not in gifts_ecodes:
                        ecode_sum_not += row1.qtty
                        ecode_sum_not_one.append(row1.amt_list)
                    if row1.ecode in gifts_ecodes:
                        ecode_sum += row1.qtty
                        ecode_sum_one.append(row1.amt_list)
    if target_type == "amt_retail":
        for product1 in all_product_list:
            seat1 = product1.productSeatList
            for row1 in seat1:
                if row1.no_pur_seat:
                    ecode_sum_one.append(0)
                else:
                    if row1.ecode not in gifts_ecodes:
                        ecode_sum_not += row1.qtty
                        ecode_sum_not_one.append(row1.amt_retail)
                    if row1.ecode in gifts_ecodes:
                        ecode_sum += row1.qtty
                        ecode_sum_one.append(row1.amt_retail)
    if target_type == "amt_receivable":
        for product1 in all_product_list:
            seat1 = product1.productSeatList
            for row1 in seat1:
                if row1.no_pur_seat:
                    ecode_sum_one.append(0)
                else:
                    if row1.ecode not in gifts_ecodes:
                        ecode_sum_not += row1.qtty
                        ecode_sum_not_one.append(row1.amt_receivable)
                    if row1.ecode in gifts_ecodes:
                        ecode_sum += row1.qtty
                        ecode_sum_one.append(row1.amt_receivable)
    return [gifts_ecodes, gifts, ecode_sum_not, ecode_sum, ecode_sum_not_one, ecode_sum_one]


def caculate_product_infos(newproduct, buygifts_value, target_type, nodis_products):
    '''

    :param newproduct: 可以参与当前促销的商品列表
    :param buygifts_value: 当前促销可赠送的商品列表
    :param target_type: 当前促销活动条件类型（数量/吊牌价/零售价/应收价）
    :param nodis_products: 不可以参与当前促销的商品列表
    :return:
    '''
    gifts_ecodes = [] #促销活动里所有可赠送商品的列表
    gifts = [] #从newproduct和nodis_products里筛选出所有可赠送的商品列表【以商品模板的最小单位类对象作为列表的一项】
    newproduct["buygifts_value"] = buygifts_value
    give_value = buygifts_value['give_value']
    # 遍历赠品列表，将赠品的商品编码放在一起，等待比较
    for gift in buygifts_value["product_list"]:
        gifts_ecodes.append(gift['ecode'])
    current_gifts_ecodes = []
    # 计算在赠品列表中的可参加活动商品数量和不在赠品列表中的可参加活动商品数量
    for item in nodis_products:
        for row1 in item.productSeatList:
            row1.no_pur_seat = True #值为true表示是在不能参与该促销的商品列表里的
    for product1 in newproduct["disproductList"] + nodis_products:
        if product1.ecode not in gifts_ecodes:
            continue
        seat1 = product1.productSeatList
        if seat1 and seat1[0].is_discount == "n":
            continue
        if product1.ecode not in current_gifts_ecodes:
            current_gifts_ecodes.append(product1.ecode)
        for row1 in seat1:
            gifts.append(row1)

    all_product_list = newproduct["disproductList"] + nodis_products
    all_product_list = sorted(all_product_list, key=lambda i: i.productSeatList[0].amt_receivable, reverse=True)
    ecode_sum_not = 0 #不在赠送商品里的数量
    ecode_sum = 0 #在赠送商品里的数量
    ecode_sum_not_one = []
    ecode_sum_one = []
    if target_type == "qtty":
        for product1 in all_product_list:
            seat1 = product1.productSeatList
            for row1 in seat1:
                if row1.no_pur_seat:
                    ecode_sum_one.append(0)
                else:
                    if row1.ecode not in current_gifts_ecodes:
                        ecode_sum_not += row1.qtty
                        ecode_sum_not_one.append(1)
                    if row1.ecode in current_gifts_ecodes:
                        ecode_sum += row1.qtty
                        ecode_sum_one.append(1)
    if target_type == "amt_list":
        for product1 in all_product_list:
            seat1 = product1.productSeatList
            for row1 in seat1:
                if row1.no_pur_seat:
                    ecode_sum_one.append(0)
                else:
                    if row1.ecode not in current_gifts_ecodes:
                        ecode_sum_not += row1.amt_list
                        ecode_sum_not_one.append(row1.amt_list)
                    if row1.ecode in current_gifts_ecodes:
                        ecode_sum += row1.amt_list
                        ecode_sum_one.append(row1.amt_list)
    if target_type == "amt_retail":
        for product1 in all_product_list:
            seat1 = product1.productSeatList
            for row1 in seat1:
                if row1.no_pur_seat:
                    ecode_sum_one.append(0)
                else:
                    if row1.ecode not in current_gifts_ecodes:
                        ecode_sum_not += row1.amt_retail
                        ecode_sum_not_one.append(row1.amt_retail)
                    if row1.ecode in current_gifts_ecodes:
                        ecode_sum += row1.amt_retail
                        ecode_sum_one.append(row1.amt_retail)
    if target_type == "amt_receivable":
        for product1 in all_product_list:
            seat1 = product1.productSeatList
            for row1 in seat1:
                if row1.no_pur_seat:
                    ecode_sum_one.append(0)
                else:
                    if row1.ecode not in current_gifts_ecodes:
                        ecode_sum_not += row1.amt_receivable
                        ecode_sum_not_one.append(row1.amt_receivable)
                    if row1.ecode in current_gifts_ecodes:
                        ecode_sum += row1.amt_receivable
                        ecode_sum_one.append(row1.amt_receivable)
    return [gifts_ecodes, gifts, ecode_sum_not, ecode_sum, ecode_sum_not_one, ecode_sum_one]

def notAforA_times(buygifts, value_num, buygifts_value, newproduct, target_type):
    if newproduct['total_' + target_type] >= value_num:
        # 当翻倍次数为0或空时，赠品数量为原赠品数量
        if buygifts.max_times == 0 or buygifts.max_times is None or value_num == 0:
            buygifts_value['give_value'] = buygifts_value['give_value']
            # 当翻倍次数为-1时，赠品数量为录入商品总数量或总金额*赠送商品数量//比较值
        elif buygifts.max_times == -1:
            buygifts_value['give_value'] = newproduct['total_' + target_type] // value_num * buygifts_value[
                'give_value']
        # 当翻倍次数大于0时，分为3种情况：1、当商品总数量或总金额<翻倍次数*比较值，赠品数量总金额*赠送商品数量//比较值
        # 2、当商品总数量或总金额>=翻倍次数*比较值，赠品数量为原赠品数量*翻倍次数
        # 3、当商品总数量或总金额<比较值，赠品数量为原赠品数量
        elif buygifts.max_times > 0:
            if newproduct['total_' + target_type] < buygifts.max_times * value_num:
                buygifts_value['give_value'] = newproduct['total_' + target_type] // value_num * buygifts_value[
                    'give_value']
            elif newproduct['total_' + target_type] >= buygifts.max_times * value_num:
                buygifts_value['give_value'] = buygifts_value['give_value'] * buygifts.max_times
    return buygifts_value['give_value']


def tidu_notAforA_times(newproduct, target_type, maxvalue_num, buygifts, buygifts_value, operation):
    if newproduct['total_' + target_type] >= maxvalue_num:
        if buygifts.max_times == -1:
            buygifts_value['give_value'] = newproduct['total_' + target_type] // maxvalue_num* buygifts_value[
                'give_value']
        elif buygifts.max_times == 0 or buygifts.max_times is None or operation['value_num'] == 0:
            buygifts_value['give_value'] = buygifts_value['give_value']
        elif buygifts.max_times > 0:
            if newproduct['total_' + target_type] < buygifts.max_times * maxvalue_num:
                buygifts_value['give_value'] = newproduct['total_' + target_type] // maxvalue_num* buygifts_value[
                    'give_value']
            elif newproduct['total_' + target_type] >= buygifts.max_times * maxvalue_num:
                buygifts_value['give_value'] = buygifts.max_times * buygifts_value['give_value']
    elif newproduct['total_' + target_type] < maxvalue_num:
        buygifts_value['give_value'] = buygifts_value['give_value']
    return buygifts_value['give_value']


def notAforA_mark(buygifts_value, nodis, gifts_ecodes, buygifts):
    target_item = buygifts.target_item
    give_max_pronum = 0  # 赠送商品总数量
    give_max_amtlist = 0  # 赠送商品总金额
    num = buygifts_value['give_value']
    if nodis != [] and num != 0:
        for product in nodis:
            seat = product.productSeatList
            seat = sorted(seat, key=lambda x: x.amt_list, reverse=False)  # 按照吊牌价格升序
            for row in seat:
                if num == 0:
                    break
                if row.is_discount == "n":
                    continue
                if row.is_buy_gifts == 'y'or row.is_taken_off:
                    continue
                elif row.ecode in gifts_ecodes:
                    row.is_buy_gifts = 'y'
                    row.fulldiscounts.append(buygifts.id)
                    row.fulldiscountPrice.append(util.CalculationPrice(row.amt_receivable))
                    row.is_run_store_act=buygifts.is_run_store_act
                    row.upamt_receivable=row.amt_receivable
                    row.amt_receivable=0
                    give_max_pronum = give_max_pronum + 1
                    if target_item == "amt_list":
                        give_max_amtlist = give_max_amtlist + float(row.amt_list)
                    elif target_item == "amt_retail":
                        give_max_amtlist = give_max_amtlist + float(row.amt_retail)
                    else:
                        give_max_amtlist = give_max_amtlist + float(row.amt_receivable)
                    num -= 1

    return give_max_pronum, give_max_amtlist


def isAforA_mark(num1, gifts, buygifts):
    target_item = buygifts.target_item
    give_max_pronum = 0  # 赠送商品总数量
    give_max_amtlist = 0  # 赠送商品总金额
    gifts = sorted(gifts, key=lambda x: x.amt_receivable, reverse=False)  # 按照应收价升序
    for product1 in gifts:
        if product1.is_buy_gifts == 'y' or product1.is_repurchase == "y" or product1.is_taken_off:
            continue
        if num1 == 0:
            break
        if product1.is_discount == "n":
            continue
        product1.is_buy_gifts = 'y'
        product1.fulldiscounts.append(buygifts.id)
        product1.fulldiscountPrice.append(util.CalculationPrice(product1.amt_receivable))
        product1.is_run_store_act = buygifts.is_run_store_act
        product1.upamt_receivable=product1.amt_receivable
        product1.amt_receivable=0
        give_max_pronum = give_max_pronum + 1
        if target_item == "amt_list":
            give_max_amtlist = give_max_amtlist + float(product1.amt_list)
        elif target_item == "amt_retail":
            give_max_amtlist = give_max_amtlist + float(product1.amt_retail)
        else:
            give_max_amtlist = give_max_amtlist + float(product1.amt_receivable)
        num1 -= 1
    return give_max_pronum, give_max_amtlist

def gift_mark(num1, gifts, buygifts):
    target_item = buygifts.target_item
    give_max_pronum = 0  # 赠送商品总数量
    give_max_amtlist = 0  # 赠送商品总金额
    gifts = sorted(gifts, key=lambda x: x.amt_receivable, reverse=False)  # 按照应收价升序
    mark_gift_list = []
    for product1 in gifts:
        if product1.is_buy_gifts == 'y' or product1.is_repurchase == "y" or product1.is_taken_off:
            continue
        if num1 == 0:
            break
        if product1.is_discount == "n":
            continue
        product1.is_buy_gifts = 'y'
        product1.fulldiscounts.append(buygifts.id)
        product1.fulldiscountPrice.append(util.CalculationPrice(product1.amt_receivable))
        product1.is_run_store_act = buygifts.is_run_store_act
        product1.upamt_receivable=product1.amt_receivable
        product1.amt_receivable=0
        give_max_pronum = give_max_pronum + 1
        if target_item == "amt_list":
            give_max_amtlist = give_max_amtlist + float(product1.amt_list)
        elif target_item == "amt_retail":
            give_max_amtlist = give_max_amtlist + float(product1.amt_retail)
        else:
            give_max_amtlist = give_max_amtlist + float(product1.amt_receivable)
        num1 -= 1
        mark_gift_list.append(product1)
    for item in mark_gift_list:
        gifts.remove(item)
    return give_max_pronum, give_max_amtlist, gifts

def isAforA_qtty_new(num1, maxvalue_num, buygifts, give_value, buygifts_value, ecode_sum, ecode_sum_not, ecode_sum_one):
    '''

    :param num1: 标记赠品数量
    :param maxvalue_num: 最大比较值
    :param buygifts: 买赠活动对象
    :param give_value: 元赠送值
    :param buygifts_value: 赠送商品+赠送数量的字典
    :param ecode_sum: 可参加活动商品列表中在赠品列表中的商品总数量
    :param ecode_sum_not: 可参加活动商品列表中不在赠品列表中的商品总数量
    :return:
    '''
    # 当可参加商品总数量大于比较值时，进入此逻辑。对于梯度买赠，这里的比较值为最大比较值，没有大于最大比较值时，标记赠品数量和赠送值均为元赠送值。
    # 当最大比较值为0时，+1，否则不加。用新的变量接收值，防止覆盖
    if maxvalue_num == 0:
        new_maxvalue_num = maxvalue_num + 1
    else:
        new_maxvalue_num = maxvalue_num
    if buygifts.max_times == 0 or buygifts.max_times is None or maxvalue_num == 0:
        num1 = give_value
        buygifts_value["give_value"] = give_value
        return [num1, buygifts_value["give_value"]]

    not_times = ecode_sum_not // new_maxvalue_num * give_value
    current_max_times = ecode_sum_not // new_maxvalue_num
    if not_times >= len(ecode_sum_one):
        num1 = len(ecode_sum_one)
    else:
        new_ecode_sum_not = ecode_sum_not
        if not_times > 0:
            new_ecode_sum_one = copy.deepcopy(ecode_sum_one[:-not_times])
        else:
            new_ecode_sum_one = copy.deepcopy(ecode_sum_one)
        tims = current_max_times
        num1 = not_times
        while new_ecode_sum_one and sum(ecode_sum_one) > 0:
            new_list = []
            for i in new_ecode_sum_one:
                if i > 0:
                    new_ecode_sum_not += i
                    current_times = new_ecode_sum_not // new_maxvalue_num - tims
                    if current_times > 0:
                        tims = new_ecode_sum_not // new_maxvalue_num
                        if i >= len(new_ecode_sum_one) - 1:
                            remain_list = []
                        else:
                             remain_list = new_ecode_sum_one[i+1:]
                        if len(remain_list) > give_value * current_times:
                            num1 += give_value * current_times
                            new_list += remain_list[:-(give_value * current_times)]
                            new_ecode_sum_one = new_list
                            break
                        else:
                            num1 += (give_value if len(remain_list) + len(new_list) >= give_value * current_times else len(remain_list) + len(new_list))
                            new_ecode_sum_one = []
                            break
                else:
                    new_list.append(i)
        # 循环结束， 将当前最大翻倍次数
        current_max_times = tims



    if buygifts.max_times > 0 and current_max_times > buygifts.max_times:
        current_max_times = buygifts.max_times
        num1 = num1 if num1 <= current_max_times * give_value else current_max_times * give_value
    buygifts_value["give_value"] = current_max_times * give_value
    return [num1, buygifts_value["give_value"]]




    # # 当可翻倍次数为0或为空或最大比较值为0时，标记赠品数量和赠送值均为元赠送值。
    # if buygifts.max_times == 0 or buygifts.max_times is None or maxvalue_num == 0:
    #     num1 = give_value
    #     buygifts_value["give_value"] = give_value
    # # 当可翻倍次数为无限时
    # elif buygifts.max_times == -1:
    #     if new_maxvalue_num<give_value:
    #         num =math.ceil ((ecode_sum + ecode_sum_not) / (new_maxvalue_num + give_value)) * new_maxvalue_num
    #         num1 =ecode_sum+ecode_sum_not- num
    #     else:
    #         num1=int((ecode_sum + ecode_sum_not) / (new_maxvalue_num + give_value)+0.5)*give_value
    #         num=int((ecode_sum + ecode_sum_not) / (new_maxvalue_num + give_value)+0.5)*new_maxvalue_num
    #         if num1>ecode_sum+ecode_sum_not-num:
    #             num1=ecode_sum+ecode_sum_not-num
    #         if ecode_sum_not+ecode_sum<new_maxvalue_num + give_value:
    #             num1=(ecode_sum + ecode_sum_not)%new_maxvalue_num
    #
    #     if ecode_sum_not>new_maxvalue_num:
    #         if num1>ecode_sum:
    #             num1=ecode_sum
    #     else:
    #         if num1>ecode_sum-num+ecode_sum_not:
    #             num1=ecode_sum-num+ecode_sum_not
    #     # 赠送值为可参加商品总数量减去标记赠品数量整除比较值乘以赠送值。
    #     buygifts_value["give_value"] = (ecode_sum_not+ecode_sum-num1)//new_maxvalue_num*give_value
    # # 当翻倍次数有限时
    # elif buygifts.max_times > 0:
    #     # 如果可参加活动商品列表中不在赠品列表中的商品总数量大于等于翻倍值乘以比较值，标记商品数量和赠送值为元赠送值
    #     if ecode_sum_not >= buygifts.max_times * new_maxvalue_num:
    #         num1 = give_value * buygifts.max_times
    #         if num1>ecode_sum:
    #             num1=ecode_sum
    #         buygifts_value["give_value"] = give_value * buygifts.max_times
    #     # 如果可参加活动商品列表中不在赠品列表中的商品总数量小于翻倍值乘以比较值
    #     if ecode_sum_not< buygifts.max_times * new_maxvalue_num:
    #         # 标记商品数量为可参加商品总数量整除比较值与赠送值的和乘以赠送值，赠送值为可参加商品总数量减去标记赠品数量整除比较值乘以赠送值。
    #         if new_maxvalue_num < give_value:
    #             num = math.ceil((ecode_sum + ecode_sum_not) / (new_maxvalue_num + give_value)) * new_maxvalue_num
    #             num1 = ecode_sum + ecode_sum_not - num
    #         else:
    #             num1 = int((ecode_sum + ecode_sum_not) / (new_maxvalue_num + give_value) + 0.5) * give_value
    #             num = int((ecode_sum + ecode_sum_not) / (new_maxvalue_num + give_value) + 0.5) * new_maxvalue_num
    #             if num1 > ecode_sum + ecode_sum_not - num:
    #                 num1 = ecode_sum + ecode_sum_not - num
    #             if ecode_sum_not + ecode_sum < new_maxvalue_num + give_value:
    #                 num1 = (ecode_sum + ecode_sum_not) % new_maxvalue_num
    #
    #         if ecode_sum_not > new_maxvalue_num:
    #             if num1 > ecode_sum:
    #                 num1 = ecode_sum
    #         else:
    #             if num1 > ecode_sum - num + ecode_sum_not:
    #                 num1 = ecode_sum - num + ecode_sum_not
    #         buygifts_value["give_value"] = (ecode_sum_not+ecode_sum-num1)//new_maxvalue_num*give_value
    #         # 如果可参加商品总数量减去标记商品数量大于翻倍值乘以比较值，赠送值和标记商品数量为元赠送值乘以翻倍次数
    #         if ecode_sum + ecode_sum_not - num1 > buygifts.max_times * new_maxvalue_num:
    #             num1 = give_value * buygifts.max_times
    #             if num1 > ecode_sum:
    #                 num1 = ecode_sum
    #             buygifts_value["give_value"] = give_value * buygifts.max_times
    # # 返回标记商品数量和赠送值
    # return [num1, buygifts_value["give_value"]]


def isAforA_qtty(num1, maxvalue_num, buygifts, give_value, buygifts_value, ecode_sum, ecode_sum_not):
    '''

    :param num1: 标记赠品数量
    :param maxvalue_num: 最大比较值
    :param buygifts: 买赠活动对象
    :param give_value: 元赠送值
    :param buygifts_value: 赠送商品+赠送数量的字典
    :param ecode_sum: 可参加活动商品列表中在赠品列表中的商品总数量
    :param ecode_sum_not: 可参加活动商品列表中不在赠品列表中的商品总数量
    :return:
    '''
    # 当可参加商品总数量大于比较值时，进入此逻辑。对于梯度买赠，这里的比较值为最大比较值，没有大于最大比较值时，标记赠品数量和赠送值均为元赠送值。
    # 当最大比较值为0时，+1，否则不加。用新的变量接收值，防止覆盖
    if maxvalue_num == 0:
        new_maxvalue_num = maxvalue_num + 1
    else:
        new_maxvalue_num = maxvalue_num
    if buygifts.max_times == 0 or buygifts.max_times is None or maxvalue_num == 0:
        num1 = give_value
        buygifts_value["give_value"] = give_value
        return [num1, buygifts_value["give_value"]]
    # 首先计算没有重合的商品可翻倍的次数
    ecode_sum_not_times = int(ecode_sum_not / new_maxvalue_num)
    ecode_sum_not_remain = ecode_sum_not - ecode_sum_not_times * new_maxvalue_num
    # now_can_give_num = ecode_sum_not_times * give_value
    ecode_sum_remain = ecode_sum - ecode_sum_not_times * give_value
    if ecode_sum_remain < 0:
        ecode_sum_remain = 0
    ecode_sum_times = int(int(ecode_sum_not_remain + ecode_sum_remain) / (new_maxvalue_num + give_value))
    remaining = int(ecode_sum_not_remain + ecode_sum_remain) % (new_maxvalue_num + give_value)
    if remaining >= new_maxvalue_num:
        max_double_times = ecode_sum_not_times + ecode_sum_times + 1
    else:
        max_double_times = ecode_sum_not_times + ecode_sum_times

    # max_double_times = ecode_sum_not_times + ecode_sum_times + remaining // new_maxvalue_num
    # 判断当前可翻多少倍
    if buygifts.max_times >= 1 and max_double_times > buygifts.max_times:
        max_double_times = buygifts.max_times
    give_num = max_double_times * give_value
    current_give_num = ecode_sum + ecode_sum_not - max_double_times * new_maxvalue_num
    num1 = give_num if give_num <= current_give_num else current_give_num
    buygifts_value["give_value"] = max_double_times * give_value
    return [num1, buygifts_value["give_value"]]


def isAforA_money(num1, buygifts, give_value, value_num, buygifts_value, ecode_sum_not, ecode_sum_one, ecode_sum,
                  ecode_sum_not_one):
    '''

    :param num1: 标记商品数量
    :param buygifts: 买赠活动对象
    :param give_value: 元赠送值
    :param value_num: 比较值
    :param buygifts_value:赠品列表+赠送数量
    :param ecode_sum_not:可参加活动商品中不在赠品列表中的商品总金额
    :param ecode_sum_one:可参加活动商品中在赠品列表中的商品单价
    :param ecode_sum:可参加活动商品中在赠品列表中的商品总金额
    :param ecode_sum_not_one:可参加活动商品中不在赠品列表中的商品单价
    :return:
    '''
    # 可参加商品总金额整除可参加活动商品中在赠品列表中的商品单价得出当前总金额可满足的赠品数量
    one_time=0
    # 当可翻倍次数为0或为空或最大比较值为0时，标记赠品数量和赠送值均为元赠送值。
    if buygifts.max_times == 0 or buygifts.max_times is None or value_num == 0:
        num1 = give_value
        buygifts_value["give_value"] = give_value
    # 当可翻倍次数为无限时
    elif buygifts.max_times == -1:
        new_ecode_sum_not = ecode_sum_not
        times=0
        for i in range(0, int((ecode_sum + ecode_sum_not) // 1)):
            if ecode_sum_not < value_num:
                new_ecode_sum_not += ecode_sum_one[i]
                new_total_times = new_ecode_sum_not // value_num*give_value
                if new_total_times >= len(ecode_sum_one) - i - 1:
                    num1 = new_total_times
                    if num1>len(ecode_sum_one) - i - 1:
                        num1=len(ecode_sum_one) - i - 1
                    break
            else:
                not_times = new_ecode_sum_not // value_num*give_value
                if not_times>=len(ecode_sum_one):
                    num1=len(ecode_sum_one)
                else:
                    new_ecode_sum_not+=ecode_sum_one[i]
                    times=new_ecode_sum_not//value_num*give_value
                    if times>=len(ecode_sum_one)-i-1:
                        num1=times
                        if num1 > len(ecode_sum_one) - i - 1:
                            num1 = len(ecode_sum_one) - i - 1
                        break

        # 赠送值为总金额减去标记赠品的总金额整除比较值乘以元赠送值
        buygifts_value["give_value"] =(sum(ecode_sum_one[0:int(len(ecode_sum_one)-num1)])+ecode_sum_not)//value_num*give_value
    # 当翻倍次数有限时
    elif buygifts.max_times > 0:
        # 当可参加活动商品中不在赠品列表中的商品总金额大于等于翻倍值乘以比较值，标记赠品数量为元赠送值
        if ecode_sum_not >= buygifts.max_times * value_num:
            num1 = give_value * buygifts.max_times
            if num1 >= len(ecode_sum_one):
                num1 = len(ecode_sum_one)
            buygifts_value["give_value"] = give_value * buygifts.max_times
        # 当可参加活动商品中不在赠品列表中的商品总金额小于翻倍值乘以比较值，逻辑与翻倍无限大致相同
        if ecode_sum_not < buygifts.max_times * value_num:
            new_ecode_sum_not = ecode_sum_not
            odd_money = 0
            times = 0
            for i in range(0, int((ecode_sum + ecode_sum_not) // 1)):
                if ecode_sum_not < value_num:
                    new_ecode_sum_not += ecode_sum_one[i]
                    new_total_times = new_ecode_sum_not // value_num * give_value
                    if new_total_times >= len(ecode_sum_one) - i - 1:
                        num1 = new_total_times
                        if num1 > len(ecode_sum_one) - i - 1:
                            num1 = len(ecode_sum_one) - i - 1
                        buygifts_value["give_value"] = (sum(
                            ecode_sum_one[0:int(len(ecode_sum_one) - num1)]) + ecode_sum_not) // value_num * give_value
                        if num1>buygifts.max_times * give_value:
                            num1=buygifts.max_times * give_value
                            buygifts_value["give_value"] =buygifts.max_times * give_value
                        if buygifts_value["give_value"]>buygifts.max_times * give_value:
                            buygifts_value["give_value"] = buygifts.max_times * give_value
                        break
                else:
                    not_times = new_ecode_sum_not // value_num * give_value
                    if not_times >= len(ecode_sum_one):
                        num1 = len(ecode_sum_one)
                        buygifts_value["give_value"] = (sum(
                            ecode_sum_one[0:int(len(ecode_sum_one) - num1)]) + ecode_sum_not) // value_num * give_value
                        if num1 > buygifts.max_times * give_value:
                            num1 = buygifts.max_times * give_value
                            buygifts_value["give_value"] = buygifts.max_times * give_value
                        if buygifts_value["give_value"]>buygifts.max_times * give_value:
                            buygifts_value["give_value"] = buygifts.max_times * give_value
                    else:
                        new_ecode_sum_not += ecode_sum_one[i]
                        times = new_ecode_sum_not // value_num * give_value
                        if times >= len(ecode_sum_one) - i - 1:
                            num1 = times
                            if num1 > len(ecode_sum_one) - i - 1:
                                num1 = len(ecode_sum_one) - i - 1
                            buygifts_value["give_value"] = (sum(
                                ecode_sum_one[
                                0:int(len(ecode_sum_one) - num1)]) + ecode_sum_not) // value_num * give_value
                            if num1 > buygifts.max_times * give_value:
                                num1 = buygifts.max_times * give_value
                                buygifts_value["give_value"] = buygifts.max_times * give_value
                            if buygifts_value["give_value"] > buygifts.max_times * give_value:
                                buygifts_value["give_value"] = buygifts.max_times * give_value
                            break

            # 赠送值为总金额减去标记赠品的总金额整除比较值乘以元赠送值

    # 返回标记赠品数量与赠送值
    return [num1, buygifts_value["give_value"]]
def getbgbyoriginalpro(buygifts,originalproductlist):
    type_three = str(buygifts.prom_type_three).upper()
    target_type = buygifts.target_type
    operation_set = buygifts.operation_set
    operation_set = sorted(operation_set, key=lambda x: x["value_num"], reverse=True)
    newproduct = setproductlist(originalproductlist, target_type)
    v_comparison = newproduct["v_comparison"]
    maxoperation_set = {}
    if type_three == "PA1301" or "PA1303":
        # 统一买赠
        operation_set = buygifts.operation_set[0]
        comp_symb_type = str(operation_set.get("comp_symb_type", "ge")).lower()  # 比较符
        value_num = operation_set.get("value_num", 0)  # 比较值v_comparison = newproduct["v_comparison"]
        iskeepbg = checkdis(comp_symb_type, v_comparison, value_num,target_type)
        if iskeepbg:
            return True
        else:
            return False
    elif type_three == "PA1302" or "PA1304":
        # 多种折扣
        for row in operation_set:
            comp_symb_type=str(row.get("comp_symb_type","ge")).lower() #比较符
            value_num=row.get("value_num",0) #比较值
            v_comparison = newproduct["v_comparison"]
            if comp_symb_type=="ge":
                if v_comparison>=float(value_num):
                    maxoperation_set=row
            elif comp_symb_type=="g":
                if v_comparison>float(value_num):
                    maxoperation_set=row
            elif comp_symb_type=="e":
                if v_comparison>=float(value_num):
                    maxoperation_set=row
            if maxoperation_set:
                break
        if maxoperation_set:
            return True
        else:
            return False
def checkdis(comp_symb_type,v_comparison,value_num,target_type):
    isbg = False  # 是否可以执行优惠
    if comp_symb_type == "ge":
        if v_comparison >= float(value_num):
            isbg = True
    elif comp_symb_type == "g":
        if v_comparison > float(value_num):
            isbg= True
    elif comp_symb_type == "e":
        if value_num == 0 and target_type == "qtty":
            isbg = False
        if v_comparison >= float(value_num):
            isbg = True
    return isbg


def caculate_max_times(comp_symb_type, v_comparison, value_num, target_type, bean_max_times):
    max_doubles_times = 0  # 最大翻倍次数
    if comp_symb_type == "g":
        value_num += 1
    # 计算最大翻倍次数
    if value_num != 0:
        max_doubles_times = int(v_comparison // value_num)
    else:
        if target_type != "qtty" and v_comparison >= float(value_num):
            max_doubles_times = 1
    if max_doubles_times > 1:
        if bean_max_times == 0 or bean_max_times == 1:
            max_doubles_times = 1
        elif bean_max_times > 1 and bean_max_times < max_doubles_times:
            max_doubles_times = bean_max_times
    return max_doubles_times

def caculate_buygift_info_online(bean, operation_set, max_double_times, org_productlists):
    """
    计算线上买赠的赠品信息
    :param bean:
    :param max_double_times:
    :param org_productlists:
    :return:
    """
    give_max_pronum = 0  # 最大赠送数量
    give_max_amtlist = 0  # 最大赠送金额
    all_give_infos = []  # 赠品信息（送了哪些赠品以及相应的数量）
    give_product_list = []

    # 计算可送赠品的总数量及金额
    for operation_item in operation_set:
        current_qtty = int(util.mul(max_double_times, operation_item.give_value))  # 此行可送数量
        give_max_pronum += current_qtty
        current_buygift_product = operation_item.buygift_product
        if current_buygift_product:
            # 此行可送总金额
            current_amt = float(util.mul(current_qtty, current_buygift_product[0].get("amt_list", 0)))
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
            give_product_info["amt_list"] = current_buygift_product[0].get("amt_list", 0)
            give_product_info["amt_retail"] = current_buygift_product[0].get("amt_list", 0)
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
        give_product.fulldiscountID.append(bean.id)
        give_product.qttyCount = 0
        for seat in give_product.productSeatList:
            seat.seat = True
            seat.is_run_other_pro = False
            seat.is_run_store_act = False
            seat.fulldiscounts.append(bean.id)
            seat.fulldiscountPrice.append(give_product.amt_list)
            seat.is_buy_gifts = "y"
            seat.pcond_id = give_item.get("pcond_id")
        all_give_product.append(give_product)
        # max_line_no += 1

    return all_give_product, give_max_pronum, give_max_amtlist, all_give_infos

def incrementalbg_online(productList, buygifts):
    '''
    全场活动线上、线上排名梯度买赠计算--2019-07-16
    :param productList: 参与的商品信息
    :param buygifts: 全场活动信息
    :return: 返回包含计算得到的新的总应收金额的结果
    '''

    try:
        target_type = buygifts.target_type
        # operation_set = buygifts.operation_set
        # 将各梯度以比较值降序排列
        # operation_set = sorted(operation_set, key=lambda x: x.get('value_num'), reverse=True)
        newproduct = setproductlist(productList, target_type)
        v_comparison = newproduct["v_comparison"]
        maxoperation_set = None
        buygifts.specific_activities=sorted(buygifts.specific_activities, key=lambda x: x.value_num)
        for row_spec in reversed(buygifts.specific_activities):
            comp_symb_type = (row_spec.comp_symb_type).lower()  # 比较符
            value_num = row_spec.value_num  # 比较值
            if comp_symb_type == "ge":
                if v_comparison >= float(value_num):
                    maxoperation_set = row_spec
            elif comp_symb_type == "g":
                if v_comparison > float(value_num):
                    maxoperation_set = row_spec
            elif comp_symb_type == "e":
                if v_comparison >= float(value_num):
                    maxoperation_set = row_spec
            if maxoperation_set:
                break

        if maxoperation_set:
            value_num = maxoperation_set.value_num
            if (maxoperation_set.comp_symb_type).lower() == "g":
                value_num += 1
            now_max_times = int(v_comparison // value_num)
            if now_max_times > 1:
                if buygifts.max_times == 0 or buygifts.max_times == 1 or buygifts.max_times is None:
                    now_max_times = 1
                elif buygifts.max_times > 1 and now_max_times > buygifts.max_times:
                    now_max_times = buygifts.max_times
            give_max_pronum = 0  # 最大赠送数量
            give_max_amtlist = 0  # 最大赠送金额
            give_product_list = []
            for row_oper in maxoperation_set.operation_set:
                current_qtty = now_max_times * row_oper.give_value  # 此行可送数量
                give_max_pronum += current_qtty
                current_buygift_product = row_oper.buygift_product
                if current_buygift_product:
                    # 此行可送总金额
                    current_amt = current_qtty * current_buygift_product[0].get("amt_list", 0)
                    give_max_amtlist += current_amt
                    # 可送赠品信息
                    give_product_info = {}
                    give_product_info["lineno"] = ""
                    give_product_info["ecode"] = current_buygift_product[0].get("ecode")
                    give_product_info["sku"] = current_buygift_product[0].get("sku", "")
                    give_product_info["qtty"] = current_qtty
                    give_product_info["amt_list"] = current_buygift_product[0].get("amt_list", 0)
                    give_product_info["amt_retail"] = current_buygift_product[0].get("amt_list", 0)
                    give_product_info["amt_receivable"] = 0
                    give_product_info["is_buy_gifts"] = "y"
                    give_product_info["pcond_id"] = row_oper.pcond_id
                    give_product_info["pitem_id"] = maxoperation_set.pitem_id
                    give_product_list.append(give_product_info)


            for give_item in give_product_list:
                give_product = Product(give_item, -1)
                give_product.fulldiscountID.append(buygifts.id)
                give_product.qttyCount = 0
                for seat in give_product.productSeatList:
                    seat.seat = True
                    seat.is_run_other_pro = False
                    seat.is_run_store_act = False
                    seat.fulldiscounts.append(buygifts.id)
                    seat.fulldiscountPrice.append(give_product.amt_list)
                    seat.is_buy_gifts = "y"
                    seat.pcond_id = give_item.get("pcond_id")
                newproduct["disproductList"].append(give_product)


            newproduct["isCalculation"] = "Y"
            newproduct["keepdis"] = "Y"
            newproduct["buygift"] = "Y"
            newproduct["give_max_pronum"] = give_max_pronum
            newproduct["give_max_amtlist"] = give_max_amtlist
            newproduct["max_double_times"] = now_max_times
            return newproduct
        else:
            return {"keepdis": "N"}
    except Exception as e:
        return {}
