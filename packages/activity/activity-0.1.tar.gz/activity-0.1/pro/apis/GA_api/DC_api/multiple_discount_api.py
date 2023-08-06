# -*- coding:utf-8 -*-
# author:尹晨
# datetime:2018/9/29 12:53
import copy

from pro.apis.GA_api.DC_api.basics import basics, pickProduct,splitDiffPrice
from pro.apis.GA_api.DC_api import get_count
from pro.utils.util import CalculationPrice
import pro.utils.util as util

# 多种打折方案计算
def preferential(productList, discountList, userInfo):
    productLists = copy.deepcopy(productList)
    # 按照折扣值升序排列
    discountList = sorted(discountList, key=lambda x: x.operation_set[-1].discount_value)
    for bean in discountList:
        if len(bean.product_list) < 1:
            continue
        # 返回每个方案计算后的商品集合
        countOne(productLists, bean, userInfo)
    return productLists


def countOne(productList, bean, userInfo):
    # 判断当前活动是否限制会员并且当前用户可否参与
    if bean.members_only:
        if userInfo is not None:
            # 当前用户会员级别不再此活动会员级别范围之内
            if userInfo.id not in bean.members_group:
                return None
        # 当前活动限制会员参加 且 当前用户不是会员
        else:
            return None
    # 进入具体运算 遍历每个商品
    productListA = []
    productList_execute = []   # 存放优惠商品
    for ecode in bean.product_list:
        for product in productList:
            if product.ecode == ecode:
                productListA.append(product)
    # 优惠商品列表
    for ecode in bean.execute_product_list:
        for product in productList:
            if product.ecode == ecode:
                productList_execute.append(product)

    #占位后的商品明细列表
    seatList=[]
    # 订单中有此ecode的商品
    if len(productListA) > 0:
        if bean.execute_product_list:
            select_operation = None  # 执行的哪个优惠
            meet_condition_flug = False  # 满足条件标志
            for operation in reversed(bean.operation_set):
                # 首先判断是否满足执行条件
                if operation.comp_symb_type == 'ge' or operation.comp_symb_type == 'e':
                    if bean.target_type == 'qtty':
                        if get_count.getCountQtty(productListA) >= operation.value_num:
                            meet_condition_flug = True
                    elif bean.target_type == 'amt_list':
                        if get_count.getCountAmtListTwo(productListA) >= operation.value_num:
                            meet_condition_flug = True
                    elif bean.target_type == 'amt_retail':
                        if get_count.getCountAmtRetailTwo(productListA) >= operation.value_num:
                            meet_condition_flug = True
                    elif bean.target_type == 'amt_receivable':
                        if get_count.getCountAmtReceivableThree(productListA) >= operation.value_num:
                            meet_condition_flug = True
                elif operation.comp_symb_type == 'g':
                    if bean.target_type == 'qtty':
                        if get_count.getCountQtty(productListA) > operation.value_num:
                            meet_condition_flug = True
                    elif bean.target_type == 'amt_list':
                        if get_count.getCountAmtListTwo(productListA) > operation.value_num:
                            meet_condition_flug = True
                    elif bean.target_type == 'amt_retail':
                        if get_count.getCountAmtRetailTwo(productListA) > operation.value_num:
                            meet_condition_flug = True
                    elif bean.target_type == 'amt_receivable':
                        if get_count.getCountAmtReceivableThree(productListA) > operation.value_num:
                            meet_condition_flug = True
                if meet_condition_flug:
                    select_operation = operation
                    break
            if meet_condition_flug:
                for product in productListA:
                    product.discountId.add(bean.id)
                # 当优惠商品未占位数量大于0的话，执行此促销
                if get_count.getNotOccupiedAll(productList_execute) > 0:
                    # 判断优惠商品和条件商品是否重合，以及满足方式为数量及对比条件为等于
                    if not (bean.target_type == 'qtty' and select_operation.comp_symb_type == 'e'):
                        # 不满足的话, 所有商品都参与计算
                        new_total_amt_receivable = 0  # 参与的每个商品计算后的金额总和（不进位）
                        new_total_amt_receivable1 = 0  # 每个商品计算后进位所得的金额总和
                        for product in productList_execute:
                            for seat in product.productSeatList:
                                new_seat, new_amt_receivable, new_amt_receivable1 = basics(seat, bean, userInfo,
                                                                                           product,select_operation)
                                if new_seat != None:
                                    # 计算总的应收价
                                    new_total_amt_receivable = new_total_amt_receivable + new_amt_receivable
                                    new_total_amt_receivable1 = new_total_amt_receivable1 + float(new_amt_receivable1)
                                    seatList.append(new_seat)
                                # seatList.append(basics(seat, bean, userInfo, product, select_operation))
                        # 计算误差
                        new_total_amt_receivable = CalculationPrice(new_total_amt_receivable)
                        diffPrice = CalculationPrice(
                            util.minus(new_total_amt_receivable, new_total_amt_receivable1))
                        if float(diffPrice) != 0:
                            splitDiffPrice(seatList, bean, diffPrice=diffPrice)
                        # 计算优惠金额
                        for seat1 in seatList:
                            # pric = float("%.2f" % float(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
                            pric = float(
                                util.Keeptwodecplaces(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
                            seat1.upamt_receivable = seat1.amt_receivable
                            seat1.discountPrice.append(pric)
                    else:
                        # 满足的话，
                        new_total_amt_receivable = 0  # 参与的每个商品计算后的金额总和（不进位）
                        new_total_amt_receivable1 = 0  # 每个商品计算后进位所得的金额总和
                        if select_operation.value_num > 0:
                            for i in range(0, select_operation.value_num):
                                # 查找出一个未占位的且进行可以进行这次活动的一件商品
                                seat, product = get_count.getNotOccupiedOne(productList_execute)
                                if seat is not None:
                                    new_seat, new_amt_receivable, new_amt_receivable1 = basics(seat, bean, userInfo, product, select_operation)
                                    if new_seat != None:
                                        # 计算总的应收价
                                        new_total_amt_receivable = new_total_amt_receivable + new_amt_receivable
                                        new_total_amt_receivable1 = new_total_amt_receivable1 + float(
                                            new_amt_receivable1)
                                        seatList.append(new_seat)
                                    # seatList.append(basics(seat, bean, userInfo, product, select_operation))
                            # 计算误差
                            new_total_amt_receivable = CalculationPrice(new_total_amt_receivable)
                            diffPrice = CalculationPrice(
                                util.minus(new_total_amt_receivable, new_total_amt_receivable1))
                            if float(diffPrice) != 0:
                                splitDiffPrice(seatList, bean, diffPrice=diffPrice)
                            # 计算优惠金额
                            for seat1 in seatList:
                                # pric = float("%.2f" % float(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
                                pric = float(
                                    util.Keeptwodecplaces(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
                                seat1.upamt_receivable = seat1.amt_receivable
                                seat1.discountPrice.append(pric)
                            for products in productList_execute:
                                for seat in products.productSeatList:
                                    seat.notProId.append(bean.id)
        else:
            # # 满足方式为数量
            # if bean.target_type == 'qtty':
            #     # 倒序循环取出判断
            #     for operation in reversed(bean.operation_set):
            #         # GE：大于等于，E：等于
            #         if operation.comp_symb_type == 'ge':
            #             # 记录可参加的活动
            #             if get_count.getCountQtty(productListA) >= operation.value_num:
            #                 for product in productListA:
            #                     product.discountId.add(bean.id)
            #             # 计算优惠
            #             if get_count.getNotOccupiedAll(productListA) >= operation.value_num:
            #                 for product in productListA:
            #                     for seat in product.productSeatList:
            #                         seatList.append(basics(seat, bean, userInfo, product, operation))
            #                 splitDiffPrice(seatList, bean)
            #                 break
            #
            #         elif operation.comp_symb_type == 'g':
            #             # 记录可参加的活动
            #             if get_count.getCountQtty(productListA) > operation.value_num:
            #                 for product in productListA:
            #                     product.discountId.add(bean.id)
            #             # 计算优惠
            #             if get_count.getNotOccupiedAll(productListA) > operation.value_num:
            #                 for product in productListA:
            #                     for seat in product.productSeatList:
            #                         seatList.append(basics(seat, bean, userInfo, product, operation))
            #                 splitDiffPrice(seatList, bean)
            #                 break
            #         elif operation.comp_symb_type == 'e':
            #             # 记录可参加的活动
            #             if get_count.getCountQtty(productListA) >= operation.value_num and operation.value_num != 0:
            #                 for product in productListA:
            #                     product.discountId.add(bean.id)
            #             # 计算优惠
            #             if get_count.getNotOccupiedAll(
            #                     productListA) >= operation.value_num and operation.value_num != 0:
            #                 for i in range(0, operation.value_num):
            #                     # 查找出一个未占位的且进行可以进行这次活动的一件商品
            #                     seat, product = get_count.getNotOccupiedOne(productListA)
            #                     if seat is not None:
            #                         seatList.append(basics(seat, bean, userInfo, product, operation))
            #                 splitDiffPrice(seatList, bean)
            #                 for product in productListA:
            #                     for seat in product.productSeatList:
            #                         seat.notProId.append(bean.id)
            #                 break
            # # 满足方式为应收金额
            # elif bean.target_type == 'amt_receivable':
            #     # 倒序循环取出判断
            #     for operation in reversed(bean.operation_set):
            #         # GE：大于等于，E：等于
            #         if operation.comp_symb_type == 'ge' or operation.comp_symb_type == 'e':
            #             # 记录可参加的活动
            #             if get_count.getCountAmtReceivableThree(productListA) >= operation.value_num:
            #                 for product in productListA:
            #                     product.discountId.add(bean.id)
            #             # 计算优惠
            #             if get_count.getCountAmtReceivableOne(productListA) >= operation.value_num:
            #                 for product in productListA:
            #                     for seat in product.productSeatList:
            #                         seatList.append(basics(seat, bean, userInfo, product, operation))
            #                 splitDiffPrice(seatList, bean)
            #                 break
            #         elif operation.comp_symb_type == 'g':
            #             # 记录可参加的活动
            #             if get_count.getCountAmtReceivableThree(productListA) > operation.value_num:
            #                 for product in productListA:
            #                     product.discountId.add(bean.id)
            #             # 计算优惠
            #             if get_count.getCountAmtReceivableOne(productListA) > operation.value_num:
            #                 for product in productListA:
            #                     for seat in product.productSeatList:
            #                         seatList.append(basics(seat, bean, userInfo, product, operation))
            #                 splitDiffPrice(seatList, bean)
            #                 break
            # # 满足方式为零售金额
            # elif bean.target_type == 'amt_retail':
            #     # 倒序循环取出判断
            #     for operation in reversed(bean.operation_set):
            #         # GE：大于等于，E：等于
            #         if operation.comp_symb_type == 'ge' or operation.comp_symb_type == 'e':
            #             # 记录可参加的活动
            #             if get_count.getCountAmtRetailTwo(productListA) >= operation.value_num:
            #                 for product in productListA:
            #                     product.discountId.add(bean.id)
            #             # 计算优惠
            #             if get_count.getCountAmtRetailOne(productListA) >= operation.value_num:
            #                 for product in productListA:
            #                     for seat in product.productSeatList:
            #                         seatList.append(basics(seat, bean, userInfo, product, operation))
            #                 splitDiffPrice(seatList, bean)
            #                 break
            #         elif operation.comp_symb_type == 'g':
            #             # 记录可参加的活动
            #             if get_count.getCountAmtRetailTwo(productListA) > operation.value_num:
            #                 for product in productListA:
            #                     product.discountId.add(bean.id)
            #             # 计算优惠
            #             if get_count.getCountAmtRetailOne(productListA) > operation.value_num:
            #                 for product in productListA:
            #                     for seat in product.productSeatList:
            #                         seatList.append(basics(seat, bean, userInfo, product, operation))
            #                 splitDiffPrice(seatList, bean)
            #                 break
            # # 满足方式为吊牌金额
            # elif bean.target_type == 'amt_list':
            #     # 倒序循环取出判断
            #     for operation in reversed(bean.operation_set):
            #         # GE：大于等于，E：等于
            #         if operation.comp_symb_type == 'ge' or operation.comp_symb_type == 'e':
            #             # 记录可参加的活动
            #             if get_count.getCountAmtListTwo(productListA) >= operation.value_num:
            #                 for product in productListA:
            #                     product.discountId.add(bean.id)
            #             # 计算优惠
            #             if get_count.getCountAmtListOne(productListA) >= operation.value_num:
            #                 for product in productListA:
            #                     for seat in product.productSeatList:
            #                         seatList.append(basics(seat, bean, userInfo, product, operation))
            #                 splitDiffPrice(seatList, bean)
            #                 break
            #         elif operation.comp_symb_type == 'g':
            #             # 记录可参加的活动
            #             if get_count.getCountAmtListTwo(productListA) > operation.value_num:
            #                 for product in productListA:
            #                     product.discountId.add(bean.id)
            #             # 计算优惠
            #             if get_count.getCountAmtListOne(productListA) > operation.value_num:
            #                 for product in productListA:
            #                     for seat in product.productSeatList:
            #                         seatList.append(basics(seat, bean, userInfo, product, operation))
            #                 splitDiffPrice(seatList, bean)
            #                 break
            select_operation = None  # 执行的哪个优惠
            meet_condition_flug = False  # 满足条件标志
            can_enable_execute = False  # 可以参加活动标志
            for operation in reversed(bean.operation_set):
                # 首先判断是否满足执行条件
                if operation.comp_symb_type == 'ge' or operation.comp_symb_type == 'e':
                    if bean.target_type == 'qtty':
                        if get_count.getNotOccupiedAll(productListA) >= operation.value_num:
                            meet_condition_flug = True
                        else:
                            if get_count.getCountQtty(productListA) >= operation.value_num:
                                can_enable_execute = True
                    elif bean.target_type == 'amt_list':
                        if get_count.getCountAmtListOne(productListA) >= operation.value_num:
                            meet_condition_flug = True
                        else:
                            if get_count.getCountAmtListTwo(productListA) >= operation.value_num:
                                can_enable_execute = True
                    elif bean.target_type == 'amt_retail':
                        if get_count.getCountAmtRetailOne(productListA) >= operation.value_num:
                            meet_condition_flug = True
                        else:
                            if get_count.getCountAmtRetailTwo(productListA) >= operation.value_num:
                                can_enable_execute = True
                    elif bean.target_type == 'amt_receivable':
                        if get_count.getCountAmtReceivableOne(productListA) >= operation.value_num:
                            meet_condition_flug = True
                        else:
                            if get_count.getCountAmtReceivableThree(productListA) >= operation.value_num:
                                can_enable_execute = True
                elif operation.comp_symb_type == 'g':
                    if bean.target_type == 'qtty':
                        if get_count.getNotOccupiedAll(productListA) > operation.value_num:
                            meet_condition_flug = True
                        else:
                            if get_count.getCountQtty(productListA) > operation.value_num:
                                can_enable_execute = True
                    elif bean.target_type == 'amt_list':
                        if get_count.getCountAmtListOne(productListA) > operation.value_num:
                            meet_condition_flug = True
                        else:
                            if get_count.getCountAmtListTwo(productListA) > operation.value_num:
                                can_enable_execute = True
                    elif bean.target_type == 'amt_retail':
                        if get_count.getCountAmtRetailOne(productListA) > operation.value_num:
                            meet_condition_flug = True
                        else:
                            if get_count.getCountAmtRetailTwo(productListA) > operation.value_num:
                                can_enable_execute = True
                    elif bean.target_type == 'amt_receivable':
                        if get_count.getCountAmtReceivableOne(productListA) > operation.value_num:
                            meet_condition_flug = True
                        else:
                            if get_count.getCountAmtReceivableThree(productListA) > operation.value_num:
                                can_enable_execute = True
                if meet_condition_flug:
                    select_operation = operation
                    break
            if meet_condition_flug or can_enable_execute:
                # 记录可执行的促销
                for product in productListA:
                    product.discountId.add(bean.id)
            if meet_condition_flug:
                # 判断优惠商品和条件商品是否重合，以及满足方式为数量及对比条件为等于
                if not (bean.target_type == 'qtty' and select_operation.comp_symb_type == 'e'):
                    # 不满足的话, 所有商品都参与计算
                    new_total_amt_receivable = 0  # 参与的每个商品计算后的金额总和（不进位）
                    new_total_amt_receivable1 = 0  # 每个商品计算后进位所得的金额总和
                    for product in productListA:
                        for seat in product.productSeatList:
                            new_seat, new_amt_receivable, new_amt_receivable1 = basics(seat, bean, userInfo,
                                                                                       product, select_operation)
                            if new_seat != None:
                                # 计算总的应收价
                                new_total_amt_receivable = new_total_amt_receivable + new_amt_receivable
                                new_total_amt_receivable1 = new_total_amt_receivable1 + float(
                                    new_amt_receivable1)
                                seatList.append(new_seat)
                            # seatList.append(basics(seat, bean, userInfo, product, select_operation))
                    # 计算误差
                    new_total_amt_receivable = CalculationPrice(new_total_amt_receivable)
                    diffPrice = CalculationPrice(
                        util.minus(new_total_amt_receivable, new_total_amt_receivable1))
                    if float(diffPrice) != 0:
                        splitDiffPrice(seatList, bean, diffPrice=diffPrice)
                    # 计算优惠金额
                    for seat1 in seatList:
                        # pric = float("%.2f" % float(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
                        pric = float(util.Keeptwodecplaces(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
                        seat1.upamt_receivable = seat1.amt_receivable
                        seat1.discountPrice.append(pric)
                else:
                    # 满足的话，
                    new_total_amt_receivable = 0  # 参与的每个商品计算后的金额总和（不进位）
                    new_total_amt_receivable1 = 0  # 每个商品计算后进位所得的金额总和
                    if select_operation.value_num > 0:
                        for i in range(0, select_operation.value_num):
                            # 查找出一个未占位的且进行可以进行这次活动的一件商品
                            seat, product = get_count.getNotOccupiedOne(productListA)
                            if seat is not None:
                                new_seat, new_amt_receivable, new_amt_receivable1 = basics(seat, bean, userInfo,
                                                                                           product,
                                                                                           select_operation)
                                if new_seat != None:
                                    # 计算总的应收价
                                    new_total_amt_receivable = new_total_amt_receivable + new_amt_receivable
                                    new_total_amt_receivable1 = new_total_amt_receivable1 + float(
                                        new_amt_receivable1)
                                    seatList.append(new_seat)
                                # seatList.append(basics(seat, bean, userInfo, product, select_operation))
                        # 计算误差
                        new_total_amt_receivable = CalculationPrice(new_total_amt_receivable)
                        diffPrice = CalculationPrice(
                            util.minus(new_total_amt_receivable, new_total_amt_receivable1))
                        if float(diffPrice) != 0:
                            splitDiffPrice(seatList, bean, diffPrice=diffPrice)
                        # 计算优惠金额
                        for seat1 in seatList:
                            # pric = float("%.2f" % str(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
                            pric = float(
                                util.Keeptwodecplaces(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
                            seat1.upamt_receivable = seat1.amt_receivable
                            seat1.discountPrice.append(pric)
                        for products in productListA:
                            for seat in products.productSeatList:
                                seat.notProId.append(bean.id)