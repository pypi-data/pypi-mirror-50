# -*- coding:utf-8 -*-
# author:尹晨
# datetime:2018/9/29 12:57
import copy

from pro.apis.GA_api.DC_api.basics import basics, pickProduct,splitDiffPrice
from pro.apis.GA_api.DC_api import get_count
from pro.utils.util import CalculationPrice
import pro.utils.util as util

# 递增打折方案计算
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
    productList_execute = []  # 存放优惠商品
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
            operations = bean.operation_set  # 递增比较明细集合
            meet_condition_flug = False  # 满足条件标志
            if operations[0].comp_symb_type == 'ge' or operations[0].comp_symb_type == 'e':
                # 满足方式为数量
                if bean.target_type == 'qtty':
                    if get_count.getCountQtty(productListA) >= operations[0].value_num:
                        meet_condition_flug = True
                elif bean.target_type == 'amt_receivable':
                    if get_count.getCountAmtReceivableThree(productListA) >= operations[0].value_num:
                        meet_condition_flug = True
                elif bean.target_type == 'amt_retail':
                    if get_count.getCountAmtRetailTwo(productListA) >= operations[0].value_num:
                        meet_condition_flug = True
                elif bean.target_type == 'amt_list':
                    if get_count.getCountAmtListTwo(productListA) >= operations[0].value_num:
                        meet_condition_flug = True
            elif operations[0].comp_symb_type == 'g':
                # 大于
                if bean.target_type == 'qtty':
                    if get_count.getCountQtty(productListA) > operations[0].value_num:
                        meet_condition_flug = True
                elif bean.target_type == 'amt_receivable':
                    if get_count.getCountAmtReceivableThree(productListA) > operations[0].value_num:
                        meet_condition_flug = True
                elif bean.target_type == 'amt_retail':
                    if get_count.getCountAmtRetailTwo(productListA) > operations[0].value_num:
                        meet_condition_flug = True
                elif bean.target_type == 'amt_list':
                    if get_count.getCountAmtListTwo(productListA) > operations[0].value_num:
                        meet_condition_flug = True
            if meet_condition_flug:
                # 说明该活动可以执行，记录到可以参加的活动
                for product in productListA:
                    product.discountId.add(bean.id)
                # 当优惠商品未占位数量大于0的话，执行此促销
                if get_count.getNotOccupiedAll(productList_execute) > 0:
                    if not (bean.target_type == 'qtty' and operations[0].comp_symb_type == 'e'):
                        # 不满足的话
                        getCount(operations, productList_execute, bean, userInfo)
                    else:
                        new_total_amt_receivable = 0  # 参与的每个商品计算后的金额总和（不进位）
                        new_total_amt_receivable1 = 0  # 每个商品计算后进位所得的金额总和
                        for i in range(0, operations[0].value_num):
                            # 选择执行哪一行
                            if i >= (len(operations) - 1):
                                select_operation = operations[-1]
                            else:
                                select_operation = operations[i]
                            # 查找出一个未占位的且进行可以进行这次活动的一件商品
                            seat, product = get_count.getNotOccupiedOne(productList_execute)
                            new_seat, new_amt_receivable, new_amt_receivable1 = basics(seat, bean, userInfo,
                                                                                       product, select_operation)
                            if new_seat != None:
                                new_total_amt_receivable = new_total_amt_receivable + new_amt_receivable
                                new_total_amt_receivable1 = new_total_amt_receivable1 + float(
                                    new_amt_receivable1)
                                seatList.append(new_seat)
                            # seatList.append(basics(seat, bean, userInfo, product, select_operation))
                        # 计算误差
                        new_total_amt_receivable = CalculationPrice(new_total_amt_receivable)
                        diffPrice = CalculationPrice(
                            util.minus(new_total_amt_receivable, new_total_amt_receivable1))

                        # 误差分摊
                        if float(diffPrice) != 0:
                            splitDiffPrice(seatList, bean, diffPrice=diffPrice)

                        # 计算优惠金额
                        for seat1 in seatList:
                            # pric = float("%.2f" % float(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
                            pric = float(
                                util.Keeptwodecplaces(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
                            seat1.upamt_receivable = seat1.amt_receivable
                            seat1.discountPrice.append(pric)

                        # 同类商品其他件数不能在参加此活动
                        for product in productList_execute:
                            for seat in product.productSeatList:
                                seat.notProId.append(bean.id)
        else:
            # 以前写的方法，现在进行优化
            # # 满足方式为数量
            # if bean.target_type == 'qtty':
            #     # 递增比较明细集合
            #     operations = bean.operation_set
            #     # GE：大于等于，E：等于
            #     if operations[0].comp_symb_type == 'ge':
            #         # 记录可参加的活动
            #         if get_count.getCountQtty(productListA) >= operations[0].value_num:
            #             for product in productListA:
            #                 product.discountId.add(bean.id)
            #         # 计算优惠
            #         if get_count.getNotOccupiedAll(productListA) >= operations[0].value_num:
            #             getCount(operations, productListA, bean, userInfo)
            #     # 大于
            #     elif operations[0].comp_symb_type == 'g':
            #         # 记录可参加的活动
            #         if get_count.getCountQtty(productListA) > operations[0].value_num:
            #             for product in productListA:
            #                 product.discountId.add(bean.id)
            #         # 计算优惠
            #         if get_count.getNotOccupiedAll(productListA) > operations[0].value_num:
            #             getCount(operations, productListA, bean, userInfo)
            #     # 等于
            #     elif operations[0].comp_symb_type == 'e':
            #         # 记录可参加的活动
            #         if get_count.getCountQtty(productListA) >= operations[0].value_num and operations[0].value_num != 0:
            #             for product in productListA:
            #                 product.discountId.add(bean.id)
            #         # 计算优惠
            #         if get_count.getNotOccupiedAll(productListA) >= operations[0].value_num and operations[
            #             0].value_num != 0:
            #             if len(operations) >= operations[0].value_num:
            #                 for operation in operations:
            #                     # 查找出一个未占位的且进行可以进行这次活动的一件商品
            #                     seat, product = get_count.getNotOccupiedOne(productListA)
            #                     seatList.append(basics(seat, bean, userInfo, product, operation))
            #                 splitDiffPrice(seatList, bean)
            #             elif len(operations) < operations[0].value_num:
            #                 for operation in operations:
            #                     if (len(operations) - 1) == operations.index(operation):
            #                         num = operations[0].value_num - len(operations)
            #                         # 加1为当前循环的商品加上
            #                         for i in range(0, num + 1):
            #                             # 查找出一个未占位的且进行可以进行这次活动的一件商品
            #                             seat, product = get_count.getNotOccupiedOne(productListA)
            #                             if seat != None:
            #                                 seatList.append(basics(seat, bean, userInfo, product, operation))
            #                     else:
            #                         # 查找出一个未占位的且进行可以进行这次活动的一件商品
            #                         seat, product = get_count.getNotOccupiedOne(productListA)
            #                         if seat != None:
            #                             seatList.append(basics(seat, bean, userInfo, product, operation))
            #                 splitDiffPrice(seatList, bean)
            #             elif len(operations) > operations[0].value_num:
            #                 for i in range(0, operations[0].value_num):
            #                     # 查找出一个未占位的且进行可以进行这次活动的一件商品
            #                     seat, product = get_count.getNotOccupiedOne(productListA)
            #                     seatList.append(basics(seat, bean, userInfo, product, operations[i]))
            #                 splitDiffPrice(seatList, bean)
            #             # 同类商品其他件数不能在参加此活动
            #             for product in productListA:
            #                 for seat in product.productSeatList:
            #                     seat.notProId.append(bean.id)
            # # 满足方式为应收金额
            # elif bean.target_type == 'amt_receivable':
            #     # 递增比较明细集合
            #     operations = bean.operation_set
            #     # GE：大于等于，E：等于
            #     if operations[0].comp_symb_type == 'ge' or operations[0].comp_symb_type == 'e':
            #         # 记录可参加的活动
            #         if get_count.getCountAmtReceivableThree(productListA) >= operations[0].value_num:
            #             for product in productListA:
            #                 product.discountId.add(bean.id)
            #         # 计算优惠
            #         if get_count.getCountAmtReceivableOne(productListA) >= operations[0].value_num:
            #             getCount(operations, productListA, bean, userInfo)
            #     # 大于
            #     elif operations[0].comp_symb_type == 'g':
            #         # 记录可参加的活动
            #         if get_count.getCountAmtReceivableThree(productListA) > operations[0].value_num:
            #             for product in productListA:
            #                 product.discountId.add(bean.id)
            #         # 计算优惠
            #         if get_count.getCountAmtReceivableOne(productListA) > operations[0].value_num:
            #             getCount(operations, productListA, bean, userInfo)
            # # 满足方式为零售金额
            # elif bean.target_type == 'amt_retail':
            #     # 递增比较明细集合
            #     operations = bean.operation_set
            #     # GE：大于等于，E：等于
            #     if operations[0].comp_symb_type == 'ge' or operations[0].comp_symb_type == 'e':
            #         # 记录可参加的活动
            #         if get_count.getCountAmtRetailTwo(productListA) >= operations[0].value_num:
            #             for product in productListA:
            #                 product.discountId.add(bean.id)
            #         # 计算优惠
            #         if get_count.getCountAmtRetailOne(productListA) >= operations[0].value_num:
            #             getCount(operations, productListA, bean, userInfo)
            #     # g 大于
            #     elif operations[0].comp_symb_type == 'g':
            #         # 记录可参加的活动
            #         if get_count.getCountAmtRetailTwo(productListA) > operations[0].value_num:
            #             for product in productListA:
            #                 product.discountId.add(bean.id)
            #         # 计算优惠
            #         if get_count.getCountAmtRetailOne(productListA) > operations[0].value_num:
            #             getCount(operations, productListA, bean, userInfo)
            # # 满足方式为吊牌金额
            # elif bean.target_type == 'amt_list':
            #     # 获得递增比较明细集合
            #     operations = bean.operation_set
            #     # GE：大于等于，E：等于
            #     if operations[0].comp_symb_type == 'ge' or operations[0].comp_symb_type == 'e':
            #         # 记录可参加的活动
            #         if get_count.getCountAmtListTwo(productListA) >= operations[0].value_num:
            #             for product in productListA:
            #                 product.discountId.add(bean.id)
            #         # 计算优惠
            #         if get_count.getCountAmtListOne(productListA) >= operations[0].value_num:
            #             getCount(operations, productListA, bean, userInfo)
            #     # g 大于
            #     elif operations[0].comp_symb_type == 'g':
            #         # 记录可参加的活动
            #         if get_count.getCountAmtListTwo(productListA) > operations[0].value_num:
            #             for product in productListA:
            #                 product.discountId.add(bean.id)
            #         # 计算优惠
            #         if get_count.getCountAmtListOne(productListA) > operations[0].value_num:
            #             getCount(operations, productListA, bean, userInfo)
            operations = bean.operation_set  # 递增比较明细集合
            meet_condition_flug = False  # 满足条件标志
            can_enable_execute = False  # 是否可以参加活动
            if operations[0].comp_symb_type == 'ge' or operations[0].comp_symb_type == 'e':
                # 满足方式为数量
                if bean.target_type == 'qtty':
                    if get_count.getNotOccupiedAll(productListA) >= operations[0].value_num:
                        meet_condition_flug = True
                    else:
                        if get_count.getCountQtty(productListA) >= operations[0].value_num:
                            can_enable_execute = True
                elif bean.target_type == 'amt_receivable':
                    if get_count.getCountAmtReceivableOne(productListA) >= operations[0].value_num:
                        meet_condition_flug = True
                    else:
                        if get_count.getCountAmtReceivableThree(productListA) >= operations[0].value_num:
                            can_enable_execute = True
                elif bean.target_type == 'amt_retail':
                    if get_count.getCountAmtRetailOne(productListA) >= operations[0].value_num:
                        meet_condition_flug = True
                    else:
                        if get_count.getCountAmtRetailTwo(productListA) >= operations[0].value_num:
                            can_enable_execute = True
                elif bean.target_type == 'amt_list':
                    if get_count.getCountAmtListOne(productListA) >= operations[0].value_num:
                        meet_condition_flug = True
                    else:
                        if get_count.getCountAmtListTwo(productListA) >= operations[0].value_num:
                            can_enable_execute = True
            elif operations[0].comp_symb_type == 'g':
                # 大于
                if bean.target_type == 'qtty':
                    if get_count.getNotOccupiedAll(productListA) > operations[0].value_num:
                        meet_condition_flug = True
                    else:
                        if get_count.getCountQtty(productListA) > operations[0].value_num:
                            can_enable_execute = True
                elif bean.target_type == 'amt_receivable':
                    if get_count.getCountAmtReceivableOne(productListA) > operations[0].value_num:
                        meet_condition_flug = True
                    else:
                        if get_count.getCountAmtReceivableThree(productListA) > operations[0].value_num:
                            can_enable_execute = True
                elif bean.target_type == 'amt_retail':
                    if get_count.getCountAmtRetailOne(productListA) > operations[0].value_num:
                        meet_condition_flug = True
                    else:
                        if get_count.getCountAmtRetailTwo(productListA) > operations[0].value_num:
                            meet_condition_flug = True
                elif bean.target_type == 'amt_list':
                    if get_count.getCountAmtListOne(productListA) > operations[0].value_num:
                        meet_condition_flug = True
                    else:
                        if get_count.getCountAmtListTwo(productListA) > operations[0].value_num:
                            can_enable_execute = True

            if meet_condition_flug or can_enable_execute:
                # 说明该活动可以执行，记录到可以参加的活动
                for product in productListA:
                    product.discountId.add(bean.id)

            if meet_condition_flug:
                if not (bean.target_type == 'qtty' and operations[0].comp_symb_type == 'e'):
                    # 不满足的话
                    getCount(operations, productListA, bean, userInfo)
                else:
                    new_total_amt_receivable = 0  # 参与的每个商品计算后的金额总和（不进位）
                    new_total_amt_receivable1 = 0  # 每个商品计算后进位所得的金额总和
                    for i in range(0, operations[0].value_num):
                        # 选择执行哪一行
                        if i >= (len(operations) - 1):
                            select_operation = operations[-1]
                        else:
                            select_operation = operations[i]
                        # 查找出一个未占位的且进行可以进行这次活动的一件商品
                        seat, product = get_count.getNotOccupiedOne(productListA)
                        new_seat, new_amt_receivable, new_amt_receivable1 = basics(seat, bean, userInfo,
                                                                                   product, select_operation)
                        if new_seat != None:
                            new_total_amt_receivable = new_total_amt_receivable + new_amt_receivable
                            new_total_amt_receivable1 = new_total_amt_receivable1 + float(
                                new_amt_receivable1)
                            seatList.append(new_seat)
                        # seatList.append(basics(seat, bean, userInfo, product, select_operation))
                    # 计算误差
                    new_total_amt_receivable = CalculationPrice(new_total_amt_receivable)
                    diffPrice = CalculationPrice(
                        util.minus(new_total_amt_receivable, new_total_amt_receivable1))

                    # 误差分摊
                    if float(diffPrice) != 0:
                        splitDiffPrice(seatList, bean, diffPrice=diffPrice)

                    # 计算优惠金额
                    for seat1 in seatList:
                        # pric = float("%.2f" % float(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
                        pric = float(util.Keeptwodecplaces(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
                        seat1.upamt_receivable = seat1.amt_receivable
                        seat1.discountPrice.append(pric)

                    # 同类商品其他件数不能在参加此活动
                    for product in productListA:
                        for seat in product.productSeatList:
                            seat.notProId.append(bean.id)


# 循环遍历递增条件计算
def getCount(operations, productListA, bean, userInfo):
    seatList=[]
    new_total_amt_receivable = 0  # 参与的每个商品计算后的金额总和（不进位）
    new_total_amt_receivable1 = 0  # 每个商品计算后进位所得的金额总和
    for operation in operations:
        if (len(operations) - 1) == operations.index(operation):
            for product in productListA:
                for seat in product.productSeatList:
                    new_seat, new_amt_receivable, new_amt_receivable1 = basics(seat, bean, userInfo, product, operation)
                    if new_seat != None:
                        new_total_amt_receivable = new_total_amt_receivable + new_amt_receivable
                        new_total_amt_receivable1 = new_total_amt_receivable1 + float(new_amt_receivable1)
                        seatList.append(new_seat)
                    # seatList.append(basics(seat, bean, userInfo, product, operation))
        else:
            # 获取一个应收价最高的商品
            seat,product = get_count.getNotOccupiedOne(productListA)
            new_seat, new_amt_receivable, new_amt_receivable1 = basics(seat, bean, userInfo, product, operation)
            if new_seat != None:
                new_total_amt_receivable = new_total_amt_receivable + new_amt_receivable
                new_total_amt_receivable1 = new_total_amt_receivable1 + float(new_amt_receivable1)
                seatList.append(new_seat)
            # seatList.append(basics(seat, bean, userInfo, product, operation))
    # splitDiffPrice(seatList, bean)
    # 计算误差
    new_total_amt_receivable = CalculationPrice(new_total_amt_receivable)
    diffPrice = CalculationPrice(
        util.minus(new_total_amt_receivable, new_total_amt_receivable1))

    # 误差分摊
    if float(diffPrice) != 0:
        splitDiffPrice(seatList, bean, diffPrice=diffPrice)

    # 计算优惠金额
    for seat1 in seatList:
        # pric = float("%.2f" % float(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
        pric = float(util.Keeptwodecplaces(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
        seat1.upamt_receivable = seat1.amt_receivable
        seat1.discountPrice.append(pric)
