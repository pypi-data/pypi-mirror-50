# -*- coding:utf-8 -*-
# author:李旭辉
# datetime:2018/10/23 9:36
import copy
from pro.apis.GA_api.DC_api.basics import splitDiffPrice
from pro.apis.entitys.PA_entitys.promotion_entity import *
import math


def executeredemption(productList, redemptions, userInfo, nodis_products):
    '''
    全场活动换购类的活动具体计算入口
    :param productList: 参与计算的商品
    :param buygifts: 全场换购活动
    :param userInfo: 会员
    :return:
    '''
    newproduct = {}
    ifvipdis = True
    try:
        #按照优惠价格基础进行可参加商品排序
        if redemptions.target_item.lower() == "amt_receivable":
            productList = sorted(productList, key=lambda x: x.amt_receivable, reverse=True)  # 按照应收价格降序
        elif redemptions.target_item.lower() == "amt_list":
            productList = sorted(productList, key=lambda x: x.amt_list, reverse=True)  # 按照吊牌价格降序
        elif redemptions.target_item.lower() == "amt_retail":
            productList = sorted(productList, key=lambda x: x.amt_retail, reverse=True)  # 按照零售价格降序
        if nodis_products:
            for row in nodis_products:
                for row1 in row.productSeatList:
                        row1.no_pur_seat = True
        newproduct = unify_redemption(productList, redemptions, nodis_products)
        if newproduct and newproduct.get("disproductList"):
            # 重新计算单据总金额
            new_total_amt_receivable = 0
            for row in newproduct["disproductList"]:
                row.fulldiscountID.append(redemptions.id)
                for row1 in row.productSeatList:
                    new_total_amt_receivable = new_total_amt_receivable + float(row1.amt_receivable)
                    if row1.is_run_vip_discount:
                        ifvipdis = False
            newproduct["total_amt_receivable"] = new_total_amt_receivable
            newproduct["new_total_amt_receivable"] = new_total_amt_receivable
            # 执行VIP折上折
            isvipdis = False
            # 当用户数据不为空且
            if redemptions.is_run_vip_discount and userInfo is not None and ifvipdis:
                if redemptions.members_only:
                    if userInfo.id in redemptions.members_group:
                        newproduct["total_amt_receivable"] = util.CalculationPrice(util.mul(newproduct["total_amt_receivable"], userInfo.discount))
                        newproduct["new_total_amt_receivable"] = newproduct["total_amt_receivable"]
                        isvipdis = True
                else:
                    if userInfo.discount is not None:
                        newproduct["total_amt_receivable"] = util.CalculationPrice(util.mul(newproduct["total_amt_receivable"], userInfo.discount))
                        newproduct["new_total_amt_receivable"] = newproduct["total_amt_receivable"]
                        isvipdis = True
            if isvipdis:
                for row in newproduct["disproductList"]:
                    for row1 in row.productSeatList:
                        if row1.is_repurchase=='n':
                            row1.fulldiscounts.append(redemptions.id)
                        row1.is_run_vip_discount = True



    except Exception as e:
        newproduct = {}

    return newproduct


def unify_redemption(productList, redemptions, nodis):
    '''
    全场活动统一特价换购计算
    :param productList: 参与的商品信息
    :param redemptions: 全场活动信息
    :param nodis:不能参与活动的商品信息
    :return: 返回包含计算得到的新的总应收金额的结果
    '''
    try:
        target_type = redemptions.target_type  # 获取比较条件
        operation_set = redemptions.operation_set
        operation = redemptions.operation_set[0]  # 获取比较整体列表
        comp_symb_type = operation.get("comp_symb_type", "ge").lower()  # 比较符
        value_num = operation.get("value_num", 1)  # 比较值
        newproduct = setproductlist(productList, target_type)
        v_comparison = newproduct["v_comparison"]
        isrp = checkdis(comp_symb_type, v_comparison, value_num, target_type)
        if isrp:
            cp = {}
            operations = []
            # after_give_times = 0
            give_value = operation["redemption"]["give_value"]  # 获取元换购数量
            # 当比较符为大于且比较值不为0的时候，将比较值+1
            if comp_symb_type == "g":
                value_num = value_num + 1
            else:
                value_num = value_num
            for operation_item in operation_set:
                rdmp = operation_item["redemption"]
                # 将每个梯度的换购列表按吊牌价升序排序，保证先换购便宜的商品
                product_list = rdmp["product_list"]
                product_list_ecode = list(map(lambda x: x["ecode"], product_list))
                rdmp["product_list_ecode"] = product_list_ecode
                operation_item["redemption"] = rdmp

            # 计算交集和非交集的商品的总数量，金额以及筛选换购商品列表
            # purchase_ecodes：换购商品编码， purchase： 换购商品列表
            # ecode_sum_not：不在换购商品范围内的总数量/金额 ecode_sum：在换购商品范围内的总数量/金额
            purchase_ecodes, purchase, ecode_sum_not, ecode_sum = caculate_product_infos(newproduct,
                                                                                         operation_set,
                                                                                         target_type,
                                                                                         nodis,
                                                                                         redemptions)

            # 计算不是交集的商品（包括是换购品但是不可参与计算的商品）现在的可翻倍数
            now_times = ecode_sum_not // value_num
            is_complate = False  # 是否已经计算完成
            current_give_value_num = now_times * give_value  # 当前换购品数
            give_max_pronum = 0  # 最大换购数
            give_max_amtlist = 0  # 最大换购金额金额
            redemp_seat_list = []
            groupnum = 1
            if now_times > 0:  # 当当前倍数大于0时， 标记赠品。
                # 首先判断当前促销的翻倍次数限制
                if redemptions.max_times == 0 or redemptions.max_times is None:
                    now_times = 1
                    is_complate = True  # 说明当前已达到最大翻倍次数
                elif redemptions.max_times > 0 and now_times >= redemptions.max_times:
                    now_times = redemptions.max_times
                    is_complate = True  # 说明当前已达到最大翻倍次数
                current_give_value_num = now_times * give_value
                redemp_seat_list = []
                # 占位当前赠品
                purchase, redemp_seat_list, groupnum = redemptions_mark(current_give_value_num, purchase,
                                                                        redemptions, operation_set, give_value,
                                                                        1, redemp_seat_list)

                if not purchase:
                    # 说明当前换购品已经占完， 计算完成
                    is_complate = True
            if not is_complate and ecode_sum != 0 and purchase:
                # 如果当前还未计算完成且当前交集商品不为0的话， 说明可以继续计算
                new_ecode_sum_not = ecode_sum_not
                while not is_complate:
                    # 当所有计算已经完成， 退出循环
                    condition_pur_list = []  # 当前作为条件的商品
                    purchase = sorted(purchase, key=lambda x: x.amt_receivable, reverse=True)  # 按照应收价降序占位条件
                    for purchase_item in purchase:
                        if not purchase_item.no_pur_seat:
                            # 当赠品属于可以作为条件的商品时， 才参与条件计算
                            if target_type == "qtty":
                                new_ecode_sum_not += 1
                            elif target_type == "amt_list":
                                new_ecode_sum_not += purchase_item.amt_list
                            elif target_type == "amt_retail":
                                new_ecode_sum_not += purchase_item.amt_retail
                            else:
                                new_ecode_sum_not += purchase_item.amt_receivable
                            condition_pur_list.append(purchase_item)

                        if new_ecode_sum_not // value_num > now_times:
                            # 当当前条件已经达到一倍（大于上次计算出来的倍数）， 结束当前倍数计算
                            break
                    current_max_times = new_ecode_sum_not // value_num  # 当前的最大倍数
                    if current_max_times <= now_times:
                        # 如果当前计算出来的倍数不大于上次的倍数时， 说明已经达到最大翻倍次数，结束循环
                        break
                    for item in condition_pur_list:
                        # 将作为条件的三个品从赠品列表中剔除
                        purchase.remove(item)
                    # 促销翻倍次数限制
                    if redemptions.max_times == 0 or redemptions.max_times is None:
                        current_max_times = 1
                        is_complate = True
                    elif redemptions.max_times > 0 and current_max_times >= redemptions.max_times:
                        current_max_times = redemptions.max_times
                        is_complate = True
                    current_give_value_num = (current_max_times - now_times) * give_value
                    # 占位当前倍数的赠品
                    purchase, redemp_seat_list, groupnum = redemptions_mark(current_give_value_num, purchase,
                                                                            redemptions, operation_set,
                                                                            give_value, 1, redemp_seat_list)

                    if not purchase:
                        # 当赠品没有时，说明已经达到最大翻倍次数，
                        is_complate = True
                    now_times = current_max_times

            ishavepurchaselist = False
            if redemp_seat_list:
                ishavepurchaselist = True
                cal(operation_set, redemp_seat_list, [], [], give_value, redemptions)

            # #进入可参加活动商品详细统计（换购商品编码列表，在换购商品范围内的换购商品列表，不在换购列表范围的商品的总金额或总数量，在换购列表范围的商品的总金额或总数量，不在换购列表范围的商品单价列表，在换购列表范围的商品单价列表）
            # purchase_ecodes, purchase, nodis_purchase,ecode_sum_not, ecode_sum, ecode_sum_one,total_nodis_purchase = details(
            #     newproduct, operation_set, target_type,nodis,redemptions)
            # give_value = operation["redemption"]["give_value"] #获取元换购数量
            # #当比较符为大于且比较值不为0的时候，将比较值+1
            # if comp_symb_type == "g" and value_num != 0:
            #     value_num = value_num + 1
            # else:
            #     value_num = value_num
            # #当可参加活动的商品中没有在换购列表范围里的商品时，进入没有交集计算
            # if ecode_sum == 0:
            #     #计算翻倍后的换购值
            #     after_give_times = notAforA_times(give_value, value_num, redemptions, newproduct,
            #                                       target_type)
            #     #当可参加活动商品的总数量或总金额满足比较值，从不可参加当前活动的商品中标记赠品
            #     if newproduct['total_' + target_type] >= value_num:
            #         notAforA_mark(after_give_times, nodis_purchase,  redemptions, operation_set, give_value)
            # # 当可参加活动的商品中没有在换购列表范围里的商品时，进入有交集计算
            # if ecode_sum != 0:
            #     num1 = 0
            #     #当满足条件时，进入翻倍计算，得到换购品标记数量num1和翻倍后换购数量after_give_times
            #     num1, after_give_times = isAforA(num1, redemptions, give_value, value_num,
            #                                          ecode_sum_not, ecode_sum_one,
            #                                          ecode_sum)
            #     if nodis_purchase and purchase:
            #         if target_type=="qtty":
            #             num1,purchase=when_purchase_both_have_qtty(after_give_times,ecode_sum_not,give_value,value_num,purchase)
            #         else:
            #             num1, purchase =when_purchase_both_have_money(after_give_times,ecode_sum_not,give_value,value_num,purchase,target_type)
            #         #当除去换购品后的总金额仍满足比较值，进行标记
            #     isAforA_mark(num1, purchase, redemptions, operation_set, give_value,nodis_purchase)
            # #将换购品放在一个列表中，按应收价降序进行分摊运算
            # purchaselist = []
            # ishavepurchaselist = False
            # for row in purchase+nodis_purchase:
            #     if row.is_repurchase == "y":
            #         purchaselist.append(row)
            # purchaselist=sorted(purchaselist,key=lambda x:x.pcond_id,reverse=False)
            # if purchaselist:
            #     ishavepurchaselist = True
            #     cal(operation_set,purchaselist,[],[],give_value,redemptions)
            #返回所有梯度的换购列表
            for operation in operation_set:
                operations.append(operation)
            # 打包活动id、翻倍后换购数量、满足的翻倍次数、元换购值、换购列表返回用于出参
            cp["id"] = redemptions.id
            cp["qtty"] = now_times * give_value
            cp["times"] = now_times
            cp["bsc_qtty"] = give_value
            cp["operations"] = operations
            cp["type_three"]=redemptions.prom_type_three
            # 标记其为可执行活动
            newproduct["keepdis"] = "Y"
            #标记其不进入分摊方法
            newproduct["isCalculation"] = "N"
            #标记其执行过全场换购
            newproduct["purchase"] = "Y"
            newproduct["gifts_ecodes"]=purchase_ecodes
            # 将cp返回
            newproduct["bg"] = cp
            newproduct["ishavepurchaselist"]=ishavepurchaselist  #记录当前换购促销是否录入换购商品
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


def details(newproduct, operation_set, target_type,nodis,redemptions):
    purchase_ecodes = []
    purchase = []
    nodis_purchase=[]
    nodis_ecodes=[]
    #记录换购列表商品编码
    operation_set = sorted(operation_set, key=lambda x: x["redemption"]["purchase_condition"], reverse=True)
    if redemptions.prom_type_three == "PA1403":
        operation_set = sorted(operation_set, key=lambda x: x["redemption"]["purchase_condition"], reverse=False)
    for operation in operation_set:
        rdmp = operation["redemption"]
        # 将每个梯度的换购列表按吊牌价升序排序，保证先换购便宜的商品
        product_list = rdmp["product_list"]
        new_product_list = []
        product = {}
        for row_p1 in product_list:
            for product1 in newproduct["disproductList"]+nodis:
                seat1 = product1.productSeatList
                if seat1 and seat1[0].is_discount == "n":
                    continue
                for row_p2 in seat1:
                    if row_p1["ecode"] == row_p2.ecode:
                        if product != {}:
                            if product["ecode"] == row_p2.ecode:
                                continue
                        product = {"amt_receivable": row_p2.amt_receivable, "ecode": row_p2.ecode}
                        new_product_list.append(product)

        new_product_list = sorted(new_product_list, key=lambda x: x["amt_receivable"])
        for cp in new_product_list:
            purchase_ecodes.append(cp['ecode'])
    #遍历可参加活动商品列表，取出可换购商品列表
    for pur in purchase_ecodes:
        for product1 in newproduct["disproductList"]:
            seat1 = product1.productSeatList
            if seat1 and seat1[0].is_discount == "n":
                continue
            for row1 in seat1:
                if row1.ecode == pur:
                    if row1.pur:
                        continue
                    purchase.append(row1)
                    row1.pur = True
    # 根据传入的比较条件和换购品商品编码列表记录在换购品列表中的可参加活动商品的信息和不在换购品列表中的可参加活动商品信息，包括其总数量/总金额及每件的单价
    ecode_sum_not = 0
    ecode_sum = 0
    total_nodis_purchase=0
    ecode_sum_one = []
    if target_type == "qtty":
        for product1 in newproduct["disproductList"]:
            seat1 = product1.productSeatList
            for row1 in seat1:
                if row1.ecode not in purchase_ecodes:
                    ecode_sum_not += row1.qtty
                if row1.ecode in purchase_ecodes:
                    ecode_sum += row1.qtty

        for ecode in purchase_ecodes:
            for product1 in nodis:
                seat1 = product1.productSeatList
                if seat1 and seat1[0].is_discount == "n":
                    continue
                for row1 in seat1:
                    if row1.ecode == ecode:
                        nodis_purchase.append(row1)
                        nodis_ecodes.append(row1.ecode)
                        total_nodis_purchase += row1.qtty
        for ecode in purchase_ecodes:
            for product1 in newproduct["disproductList"] + nodis:
                if product1.productSeatList and product1.productSeatList[0].is_discount == "n":
                    continue
                for row1 in product1.productSeatList:
                    if row1.ecode == ecode:
                        if row1.pur_seat:
                            continue
                        if row1.no_pur_seat:
                            ecode_sum_one.append(0)
                        else:
                            ecode_sum_one.append(1)
                        row1.pur_seat=True
    if target_type == "amt_list":
        for product1 in newproduct["disproductList"]:
            seat1 = product1.productSeatList
            for row1 in seat1:
                if row1.ecode not in purchase_ecodes:
                    ecode_sum_not += row1.amt_list
                if row1.ecode in purchase_ecodes:
                    ecode_sum += row1.amt_list
        for ecode in purchase_ecodes:
            for product1 in nodis:
                seat1 = product1.productSeatList
                for row1 in seat1:
                    if row1.ecode == ecode:
                        nodis_purchase.append(row1)
                        nodis_ecodes.append(row1.ecode)
                        total_nodis_purchase += row1.amt_list
        for ecode in purchase_ecodes:
            for product1 in newproduct["disproductList"]+nodis:
                seat1 = product1.productSeatList
                for row1 in seat1:
                    if row1.ecode == ecode:
                        if row1.pur_seat:
                            continue
                        if row1.no_pur_seat:
                            ecode_sum_one.append(0)
                        else:
                            ecode_sum_one.append(row1.amt_list)
                        row1.pur_seat=True
    if target_type == "amt_retail":
        for product1 in newproduct["disproductList"]:
            seat1 = product1.productSeatList
            for row1 in seat1:
                if row1.ecode not in purchase_ecodes:
                    ecode_sum_not += row1.amt_retail
                if row1.ecode in purchase_ecodes:
                    ecode_sum += row1.amt_retail
        for ecode in purchase_ecodes:
            for product1 in nodis:
                seat1 = product1.productSeatList
                for row1 in seat1:
                    if row1.ecode == ecode:
                        nodis_purchase.append(row1)
                        nodis_ecodes.append(row1.ecode)
                        total_nodis_purchase += row1.amt_retail
        for ecode in purchase_ecodes:
            for product1 in newproduct["disproductList"]+nodis:
                seat1 = product1.productSeatList
                for row1 in seat1:
                    if row1.ecode == ecode:
                        if row1.pur_seat:
                            continue
                        if row1.no_pur_seat:
                            ecode_sum_one.append(0)
                        else:
                            ecode_sum_one.append(row1.amt_retail)
                        row1.pur_seat = True
    if target_type == "amt_receivable":
        for product1 in newproduct["disproductList"]:
            seat1 = product1.productSeatList
            for row1 in seat1:
                if row1.ecode not in purchase_ecodes:
                    ecode_sum_not += row1.amt_receivable
                if row1.ecode in purchase_ecodes:
                    ecode_sum += row1.amt_receivable
        for ecode in purchase_ecodes:
            for product1 in nodis:
                seat1 = product1.productSeatList
                for row1 in seat1:
                    if row1.ecode == ecode:
                        nodis_purchase.append(row1)
                        nodis_ecodes.append(row1.ecode)
                        total_nodis_purchase += row1.amt_receivable
        for ecode in purchase_ecodes:
            for product1 in newproduct["disproductList"]+nodis:
                seat1 = product1.productSeatList
                for row1 in seat1:
                    if row1.ecode == ecode:
                        if row1.pur_seat:
                            continue
                        if row1.no_pur_seat:
                            ecode_sum_one.append(0)
                        else:
                            ecode_sum_one.append(row1.amt_receivable)
                        row1.pur_seat=True
    return [purchase_ecodes, purchase,nodis_purchase, ecode_sum_not, ecode_sum, ecode_sum_one[::-1],total_nodis_purchase]


def caculate_product_infos(newproduct, operation_set, target_type, nodis, redemptions):
    purchase_ecodes = []
    purchase = []
    #记录换购列表商品编码
    operation_set = sorted(operation_set, key=lambda x: x["redemption"]["purchase_condition"], reverse=True)
    for item in nodis:
        for row1 in item.productSeatList:
            row1.no_pur_seat = True
    if redemptions.prom_type_three == "PA1403":
        operation_set = sorted(operation_set, key=lambda x: x["redemption"]["purchase_condition"], reverse=False)

    for operation in operation_set:
        rdmp = operation["redemption"]
        # 将每个梯度的换购列表按吊牌价升序排序，保证先换购便宜的商品
        product_list = rdmp["product_list"]
        product_list_ecode = rdmp["product_list_ecode"]
        for product1 in newproduct["disproductList"] + nodis:
            if product1.ecode not in product_list_ecode:
                continue
            seat1 = product1.productSeatList
            if seat1 and seat1[0].is_discount == "n":
                continue
            if product1.ecode not in purchase_ecodes:
                purchase_ecodes.append(product1.ecode)
            for row_p2 in seat1:
                purchase.append(row_p2)

    # 根据传入的比较条件和换购品商品编码列表计算不在交集中的商品和交集的商品的数量/总金额
    ecode_sum_not = 0
    ecode_sum = 0
    if target_type == "qtty":
        for product1 in newproduct["disproductList"]:
            seat1 = product1.productSeatList
            for row1 in seat1:
                if row1.ecode not in purchase_ecodes:
                    ecode_sum_not += row1.qtty
                if row1.ecode in purchase_ecodes:
                    ecode_sum += row1.qtty
    if target_type == "amt_list":
        for product1 in newproduct["disproductList"]:
            seat1 = product1.productSeatList
            for row1 in seat1:
                if row1.ecode not in purchase_ecodes:
                    ecode_sum_not += row1.amt_list
                if row1.ecode in purchase_ecodes:
                    ecode_sum += row1.amt_list
    if target_type == "amt_retail":
        for product1 in newproduct["disproductList"]:
            seat1 = product1.productSeatList
            for row1 in seat1:
                if row1.ecode not in purchase_ecodes:
                    ecode_sum_not += row1.amt_retail
                if row1.ecode in purchase_ecodes:
                    ecode_sum += row1.amt_retail
    if target_type == "amt_receivable":
        for product1 in newproduct["disproductList"]:
            seat1 = product1.productSeatList
            for row1 in seat1:
                if row1.ecode not in purchase_ecodes:
                    ecode_sum_not += row1.amt_receivable
                if row1.ecode in purchase_ecodes:
                    ecode_sum += row1.amt_receivable
    return [purchase_ecodes, purchase, ecode_sum_not, ecode_sum]

def notAforA_times(give_value, value_num, redemptions, newproduct, target_type):
    if newproduct['total_' + target_type] >= value_num:
        # 当翻倍次数为0或空时，换购数量为原换购数量
        if redemptions.max_times == 0 or redemptions.max_times is None or value_num == 0:
            give_value = give_value
            # 当翻倍次数为-1时，换购数量为可参加活动商品总数量或总金额//比较值*元换购数量
        elif redemptions.max_times == -1:
            give_value = newproduct['total_' + target_type] // value_num * give_value
        # 当翻倍次数大于0时，分为2种情况：1、当商品总数量或总金额<翻倍次数*比较值，可参加商品总数量总金额//比较值*元换购数量
        # 2、当商品总数量或总金额>=翻倍次数*比较值，换购数量为元换购数量*翻倍次数
        elif redemptions.max_times > 0:
            if newproduct['total_' + target_type] < redemptions.max_times * value_num:
                give_value = newproduct['total_' + target_type] // value_num * give_value
            elif newproduct['total_' + target_type] >= redemptions.max_times * value_num:
                give_value = give_value * redemptions.max_times
    return give_value


def notAforA_mark(after_give_times, nodis_purchase, redemptions, operation_set, give_value):
    #num控制循环次数
    num = after_give_times
    #将活动换购梯度按换购值降序排序，统一优惠换购按换购值升序排序
    operation_set = sorted(operation_set, key=lambda x: x["redemption"]["purchase_condition"], reverse=True)
    if redemptions.prom_type_three == "PA1403":
        operation_set = sorted(operation_set, key=lambda x: x["redemption"]["purchase_condition"], reverse=False)
    if nodis_purchase != [] and num != 0:
        mark_purchase(operation_set,nodis_purchase,num,redemptions,give_value)



def isAforA_mark(num1, purchase, redemptions, operation_set, give_value,nodis_purchase):
    purchase = sorted(purchase, key=lambda x: x.amt_receivable, reverse=False)  # 按照应收价格升序
    # 将活动换购梯度按换购值降序排序，统一优惠换购按换购值升序排序
    operation_set = sorted(operation_set, key=lambda x: x["redemption"]["purchase_condition"], reverse=True)
    if redemptions.prom_type_three == "PA1403":
        operation_set = sorted(operation_set, key=lambda x: x["redemption"]["purchase_condition"], reverse=False)

    # 遍历换购梯度，从换购列表匹配录入商品
    if nodis_purchase != []:
        for row in nodis_purchase:
            purchase.append(row)
    mark_purchase(operation_set,purchase,num1,redemptions,give_value)


def redemptions_mark(current_give_num, purchase, redemptions, operation_set, give_value, groupnum,
                     redemp_seat_list):
    purchase = sorted(purchase, key=lambda x: x.amt_receivable, reverse=False)  # 按照应收价格升序
    # 将活动换购梯度按换购值降序排序，统一优惠换购按换购值升序排序
    operation_set = sorted(operation_set, key=lambda x: x["redemption"]["purchase_condition"], reverse=True)
    if redemptions.prom_type_three == "PA1403":
        operation_set = sorted(operation_set, key=lambda x: x["redemption"]["purchase_condition"], reverse=False)

    # 获取元换购值用于复位
    new_give_value = give_value
    # 组别原始值设为1
    # groupnum = 1
    # 遍历换购梯度，从换购列表匹配录入商品
    new_select_list = []
    for operation in operation_set:
        # 获取元换购值用于复位
        give_value = new_give_value
        rdmp = operation["redemption"]
        # 将每个梯度的换购列表按吊牌价升序排序，保证先换购便宜的商品
        product_list_ecode = rdmp["product_list_ecode"]
        for row in purchase:
            if current_give_num == 0:
                break
            if row.ecode not in product_list_ecode:
                continue
            if row.is_discount == "n":
                continue
            if row.is_repurchase == 'y' or row.is_buy_gifts == "y" or row.is_taken_off:
                continue
            # 当匹配到商品时，改变商品明细，是否为换购品设为y，记录活动ID，记录换购梯度，记录换购组别
            row.is_repurchase = 'y'
            row.fulldiscounts.append(redemptions.id)
            row.is_run_store_act = False
            row.pcond_id = operation["pcond_id"]
            row.groupnum = groupnum
            redemp_seat_list.append(row)
            new_select_list.append(row)
            # 元换购值递减以控制组别，当元换购值为0时，复位元换购值，换购组别+1
            give_value -= 1
            if give_value == 0:
                give_value = new_give_value
                groupnum += 1
                # 控制循环次数，当翻倍后的换购数量为0时，跳出循环
            current_give_num -= 1

    for row in new_select_list:
        purchase.remove(row)
    return purchase, redemp_seat_list, groupnum

def isAforA(num1, redemptions, give_value, value_num, ecode_sum_not, ecode_sum_one, ecode_sum):
    '''

    :param num1: 标记商品数量
    :param buygifts: 换购活动对象
    :param give_value: 元换购值
    :param value_num: 比较值
    :param buygifts_value:换购列表+元换购数量
    :param ecode_sum_not:可参加活动商品中不在换购品列表中的商品总金额
    :param ecode_sum_one:可参加活动商品中在换购品列表中的商品单价
    :param ecode_sum:可参加活动商品中在换购品列表中的商品总金额
    :param ecode_sum_not_one:可参加活动商品中不在换购品列表中的商品单价
    :return:
    '''
    one_time = 0
    after_give_value=0
    # 当可翻倍次数为0或为空或最大比较值为0时，标记换购品数量和换购值均为元换购值。
    if redemptions.max_times == 0 or redemptions.max_times is None or value_num == 0:
        num1 = give_value
        after_give_value = give_value
    # 当可翻倍次数为无限时
    elif redemptions.max_times == -1:
        #用新的变量接收，防止覆盖
        new_ecode_sum_not = ecode_sum_not
        times = 0
        #遍历可参加活动商品中在换购品列表中的商品单价列表
        for i in range(0,len(ecode_sum_one) ):
            if ecode_sum_not < value_num:
                #当可参加活动商品中不在换购品列表中的商品总金额<比较值，将可参加活动商品中在换购品列表中的商品单价依次加在该总金额上
                new_ecode_sum_not += ecode_sum_one[i]
                #计算标记换购数量
                new_total_times = new_ecode_sum_not // value_num * give_value
                #控制当标记数量多于剩余商品数量时.,返回标记数量，跳出循环
                if new_total_times >= len(ecode_sum_one) - i - 1:
                    num1 = new_total_times
                    if num1 > len(ecode_sum_one) - i - 1:
                        num1 = len(ecode_sum_one) - i - 1
                    break
            else:
                # 当可参加活动商品中不在换购品列表中的商品总金额》=比较值，先排除不在换购品列表中的商品总金额可以换购的商品数量
                not_times = ecode_sum_not // value_num * give_value
                #如果不在换购品列表中的商品总金额可以换购的商品数量大于等于可参加活动商品中在换购品列表中的商品数量，返回标记数量
                if not_times >= len(ecode_sum_one):
                    num1 = len(ecode_sum_one)
                else:
                    #将可参加活动商品中在换购品列表中的商品单价依次加在该总金额上
                    new_ecode_sum_not += ecode_sum_one[i]
                    times = new_ecode_sum_not // value_num * give_value
                    if times >= len(ecode_sum_one) - i - 1:
                        num1 = times
                        if num1 > len(ecode_sum_one) - i - 1:
                            num1 = len(ecode_sum_one) - i - 1
                        break

        # 赠送值为总金额减去标记赠品的总金额整除比较值乘以元赠送值
        after_give_value = (sum(
            ecode_sum_one[0:int(len(ecode_sum_one) - num1)]) + ecode_sum_not) // value_num * give_value
    # 当翻倍次数有限时
    elif redemptions.max_times > 0:
        # 当可参加活动商品中不在赠品列表中的商品总金额大于等于翻倍值乘以比较值，标记赠品数量为元赠送值
        if ecode_sum_not >= redemptions.max_times * value_num:
            num1 = give_value * redemptions.max_times
            if num1 >= len(ecode_sum_one):
                num1 = len(ecode_sum_one)
            after_give_value = give_value * redemptions.max_times
        # 当可参加活动商品中不在赠品列表中的商品总金额小于翻倍值乘以比较值，逻辑与翻倍无限大致相同
        if ecode_sum_not < redemptions.max_times * value_num:
            new_ecode_sum_not = ecode_sum_not
            odd_money = 0
            times = 0
            for i in range(0, len(ecode_sum_one)):
                if ecode_sum_not < value_num:
                    new_ecode_sum_not += ecode_sum_one[i]
                    new_total_times = new_ecode_sum_not // value_num * give_value
                    if new_total_times >= len(ecode_sum_one) - i - 1:
                        num1 = new_total_times
                        if num1 > len(ecode_sum_one) - i - 1:
                            num1 = len(ecode_sum_one) - i - 1
                        after_give_value = (sum(
                            ecode_sum_one[0:int(len(ecode_sum_one) - num1)]) + ecode_sum_not) // value_num * give_value
                        if num1 > redemptions.max_times * give_value:
                            num1 = redemptions.max_times * give_value
                            after_give_value = redemptions.max_times * give_value
                        if after_give_value > redemptions.max_times * give_value:
                            after_give_value = redemptions.max_times * give_value
                        break
                else:
                    not_times = new_ecode_sum_not // value_num * give_value
                    if not_times >= len(ecode_sum_one):
                        num1 = len(ecode_sum_one)
                        after_give_value = (sum(
                            ecode_sum_one[0:int(len(ecode_sum_one) - num1)]) + ecode_sum_not) // value_num * give_value
                        if num1 > redemptions.max_times * give_value:
                            num1 = redemptions.max_times * give_value
                            after_give_value = redemptions.max_times * give_value
                        if after_give_value > redemptions.max_times * give_value:
                            after_give_value = redemptions.max_times * give_value
                    else:
                        new_ecode_sum_not += ecode_sum_one[i]
                        times = new_ecode_sum_not // value_num * give_value
                        if times >= len(ecode_sum_one) - i - 1:
                            num1 = times
                            if num1 > len(ecode_sum_one) - i - 1:
                                num1 = len(ecode_sum_one) - i - 1
                            after_give_value = (sum(
                                ecode_sum_one[
                                0:int(len(ecode_sum_one) - num1)]) + ecode_sum_not) // value_num * give_value
                            if num1 > redemptions.max_times * give_value:
                                num1 = redemptions.max_times * give_value
                                after_give_value = redemptions.max_times * give_value
                            if after_give_value > redemptions.max_times * give_value:
                                after_give_value = redemptions.max_times * give_value
                            break

            # 赠送值为总金额减去标记赠品的总金额整除比较值乘以元赠送值

    # 返回标记赠品数量与赠送值
    return [num1, after_give_value]


def getcpbyoriginalpro(redemptions, originalproductlist):
    target_type = redemptions.target_type
    operation_set = redemptions.operation_set
    operation_set = sorted(operation_set, key=lambda x: x["value_num"], reverse=True)
    newproduct = setproductlist(originalproductlist, target_type)
    v_comparison = newproduct["v_comparison"]
    operation_set = operation_set[0]
    comp_symb_type = str(operation_set.get("comp_symb_type", "ge")).lower()  # 比较符
    value_num = operation_set.get("value_num", 0)  # 比较值v_comparison = newproduct["v_comparison"]
    iskeepcp = checkdis(comp_symb_type, v_comparison, value_num, target_type)
    if iskeepcp:
        return True
    else:
        return False


def checkdis(comp_symb_type, v_comparison, value_num, target_type):
    iscp = False  # 是否可以执行优惠
    if comp_symb_type == "ge":
        if v_comparison >= float(value_num):
            iscp = True
    elif comp_symb_type == "g":
        if v_comparison > float(value_num):
            iscp = True
    elif comp_symb_type == "e":
        if value_num == 0 and target_type == "qtty":
            iscp = False
        if v_comparison >= float(value_num):
            iscp = True
    return iscp

def mark_purchase(operation_set,seatlist,num,redemptions,give_value):
    # 获取元换购值用于复位
    new_give_value = give_value
    # 组别原始值设为1
    groupnum = 1
    # 遍历换购梯度，从换购列表匹配录入商品
    for operation in operation_set:
        # 获取元换购值用于复位
        give_value = new_give_value
        rdmp = operation["redemption"]
        # 将每个梯度的换购列表按吊牌价升序排序，保证先换购便宜的商品
        product_list = rdmp["product_list"]
        new_product_list = []
        product = {}
        for row_p1 in product_list:
            for row_p2 in seatlist:
                if row_p1["ecode"] == row_p2.ecode:
                    if product != {}:
                        if product["ecode"] == row_p2.ecode:
                            continue
                    product = {"amt_receivable": row_p2.amt_receivable, "ecode": row_p2.ecode}
                    new_product_list.append(product)
        new_product_list = sorted(new_product_list, key=lambda x: x["amt_receivable"])
        for pro in new_product_list:
            for row in seatlist:
                if pro["ecode"] == row.ecode:
                    if num == 0:
                        break
                    if row.is_discount == "n":
                        continue
                    if row.is_repurchase == 'y' or row.is_buy_gifts == "y" or row.is_taken_off:
                        continue
                    # 当匹配到商品时，改变商品明细，是否为换购品设为y，记录活动ID，记录换购梯度，记录换购组别
                    row.is_repurchase = 'y'
                    row.fulldiscounts.append(redemptions.id)
                    row.is_run_store_act = False
                    row.pcond_id = operation["pcond_id"]
                    row.groupnum = groupnum
                    # 元换购值递减以控制组别，当元换购值为0时，复位元换购值，换购组别+1
                    give_value -= 1
                    if give_value == 0:
                        give_value = new_give_value
                        groupnum += 1
                        # 控制循环次数，当翻倍后的换购数量为0时，跳出循环
                    num -= 1

def when_purchase_both_have_qtty(after_give_times,ecode_sum_not,give_value,value_num,purchase):
    num1 = after_give_times
    total_qtty = ecode_sum_not
    purchase = purchase[::-1]
    while True:
        if total_qtty >= after_give_times // give_value * value_num:
            purchase = purchase
            break
        else:
            total_qtty += 1
            purchase.pop(0)
            if total_qtty >= after_give_times // give_value * value_num:
                break
    return [num1,purchase]
def when_purchase_both_have_money(after_give_times,ecode_sum_not,give_value,value_num,purchase,target_type):
    num1 = after_give_times
    purchase=purchase[::-1]
    total_money = ecode_sum_not
    while True:
        if total_money >= after_give_times // give_value * value_num:
            purchase = purchase
            break
        else:
            if target_type == "amt_list":
                total_money += purchase[0].amt_list
            if target_type == "amt_receivable":
                total_money += purchase[0].amt_receivable
            if target_type == "amt_retail":
                total_money += purchase[0].amt_retail
            purchase.pop(0)
            if total_money >= after_give_times // give_value * value_num:
                break
    return [num1, purchase]
def cal(operation_set,purchaselist,tidu_purchaselist,split_purchaselist,give_value,redemptions):
    for i in range(0, len(operation_set)):
        for row2 in purchaselist:
            if operation_set[i]['pcond_id'] == row2.pcond_id:
                tidu_purchaselist.append(row2)
        if tidu_purchaselist:
            split_purchaselist.append(tidu_purchaselist)
        tidu_purchaselist = []
    for i in range(0, len(split_purchaselist)):
        # 遍历换购商品列表，以每组的商品件数，即元换购数量为步长，保证切片时没有重复明细
        new_tidu_purchaselist = sorted(split_purchaselist[i], key=lambda x: x.groupnum, reverse=False)
        pcond_id = new_tidu_purchaselist[0].pcond_id
        for i in range(0, len(new_tidu_purchaselist), int(give_value)):
            diffprice=0
            # 通过切片将每组换购品单独取出
            small_list = new_tidu_purchaselist[i:i + int(give_value)]
            if len(new_tidu_purchaselist) - i < give_value:
                small_list = new_tidu_purchaselist[i:len(new_tidu_purchaselist)]
            condition_operation = operation_set[pcond_id - 1]
            if redemptions.prom_type_three.upper() == "PA1401":
                purchase_condition = condition_operation["redemption"]["purchase_condition"]
                cal_purchase_condition = util.CalculationPrice(util.div(purchase_condition,give_value) )
                total_amt_receivable = util.CalculationPrice(sum(j.amt_receivable for j in small_list))
                if len(small_list)==give_value:
                    if total_amt_receivable>purchase_condition:
                        new_total_amt_receivable=purchase_condition
                        new_total_amt_receivable1=0
                        newdis=util.div(new_total_amt_receivable,total_amt_receivable)
                        for row_p in small_list:
                            row_p.upamt_receivable=row_p.amt_receivable
                            row_p.amt_receivable = util.CalculationPrice(util.mul(row_p.amt_receivable,newdis))
                            new_total_amt_receivable1=new_total_amt_receivable1+row_p.amt_receivable
                        diffprice=util.CalculationPrice(util.minus(new_total_amt_receivable,new_total_amt_receivable1))
                    else:
                        diffprice=0
                else:
                    new_total_amt_receivable=0
                    for row_1 in small_list:
                        row_1.upamt_receivable = row_1.amt_receivable
                        if row_1.amt_receivable>cal_purchase_condition:
                            row_1.amt_receivable=cal_purchase_condition
                        new_total_amt_receivable=new_total_amt_receivable+row_1.amt_receivable
                    new_total_amt_receivable1 = 0
                    newdis = util.div(new_total_amt_receivable, total_amt_receivable)
                    for row_p in small_list:
                        row_p.upamt_receivable = row_p.amt_receivable
                        row_p.amt_receivable = util.CalculationPrice(util.mul(row_p.amt_receivable, newdis))
                        new_total_amt_receivable1 = new_total_amt_receivable1 + row_p.amt_receivable
                    diffprice = util.CalculationPrice(util.minus(new_total_amt_receivable, new_total_amt_receivable1))
            if redemptions.prom_type_three.upper() == "PA1402":
                purchase_condition = condition_operation["redemption"]["purchase_condition"]
                cal_purchase_condition = purchase_condition
                total_amt_receivable = util.CalculationPrice(sum(j.amt_receivable for j in small_list))
                new_total_amt_receivable=util.CalculationPrice(util.mul(total_amt_receivable,purchase_condition))
                new_total_amt_receivable1=0
                newdis=util.div(new_total_amt_receivable,total_amt_receivable)
                for row_p in small_list:
                    row_p.upamt_receivable=row_p.amt_receivable
                    row_p.amt_receivable = util.CalculationPrice(util.mul(row_p.amt_receivable,newdis))
                    new_total_amt_receivable1=new_total_amt_receivable1+row_p.amt_receivable
                diffprice=util.CalculationPrice(util.minus(new_total_amt_receivable,new_total_amt_receivable1))
            if redemptions.prom_type_three.upper() == "PA1403":
                purchase_condition = condition_operation["redemption"]["purchase_condition"]
                cal_purchase_condition = util.CalculationPrice(util.div(purchase_condition, give_value))
                total_amt_receivable = util.CalculationPrice(sum(j.amt_receivable for j in small_list))
                if len(small_list) == give_value:
                    if total_amt_receivable > purchase_condition:
                        new_total_amt_receivable = util.minus(total_amt_receivable,purchase_condition)
                        new_total_amt_receivable1 = 0
                        newdis = util.div(new_total_amt_receivable, total_amt_receivable)
                        for row_p in small_list:
                            row_p.upamt_receivable = row_p.amt_receivable
                            row_p.amt_receivable = util.CalculationPrice(util.mul(row_p.amt_receivable, newdis))
                            new_total_amt_receivable1 = new_total_amt_receivable1 + row_p.amt_receivable
                        diffprice = util.CalculationPrice(
                            util.minus(new_total_amt_receivable, new_total_amt_receivable1))
                    else:
                        diffprice = 0
                else:
                    new_total_amt_receivable = 0
                    for row_1 in small_list:
                        row_1.upamt_receivable = row_1.amt_receivable
                        if row_1.amt_receivable > cal_purchase_condition:
                            row_1.amt_receivable = util.minus(row_1.amt_receivable,cal_purchase_condition)
                        new_total_amt_receivable = new_total_amt_receivable + row_1.amt_receivable
                    new_total_amt_receivable1 = 0
                    newdis = util.div(new_total_amt_receivable, total_amt_receivable)
                    for row_p in small_list:
                        row_p.upamt_receivable = row_p.amt_receivable
                        row_p.amt_receivable = util.CalculationPrice(util.mul(row_p.amt_receivable, newdis))
                        new_total_amt_receivable1 = new_total_amt_receivable1 + row_p.amt_receivable
                    diffprice = util.CalculationPrice(util.minus(new_total_amt_receivable, new_total_amt_receivable1))
            # 进入差价分摊方法
            if abs(diffprice)>0:
                splitDiffPrice(small_list, redemptions,None,diffprice)

            for row_p1 in small_list:
                row_p1.fulldiscountPrice.append(util.CalculationPrice(util.minus(row_p1.upamt_receivable,row_p.amt_receivable)))
                # row_p1.upamt_receivable = row_p1.amt_receivable
