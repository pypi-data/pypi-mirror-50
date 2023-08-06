# -*- coding:utf-8 -*-
# author:尹晨
# datetime:2018/9/29 13:00
import copy

from pro.apis.GA_api.DC_api.basics import basics, getNotOccupied,splitDiffPrice
from pro.apis.GA_api.DC_api import get_count
from pro.utils.util import CalculationPrice
import pro.utils.util as util

# 组合打折方案计算
def preferential(productList, discountList, userInfo):
    productLists = copy.deepcopy(productList)
    # 按照折扣值升序排列
    discountList = sorted(discountList, key=lambda x: x.specific_activities[-1].discount_value)
    for bean in discountList:
        for SpecificActivities in bean.specific_activities:
            if len(SpecificActivities.product_list) < 1:
                continue
        # 进入判断运算
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

    productListA=[] #记录【优惠商品】----20190411--hexiaoxia
    for ecode in bean.execute_product_list:
        for product in productList:
            if product.ecode == ecode:
                productListA.append(product)

    #组合活动具体的【购买商品】判断项是控制在1~5项的(云促销前端控制，引擎不做控制)，所以对于之前写死的2项做修改----20190411--hexiaoxia
    allproductOneCount=[]
    allproductOnesss=[]
    alldisproducts=[]
    isdis=True #是否符合执行
    is_enable_exec = True
    for r_item in bean.specific_activities:
        productOneCount = -1
        productOnesss = 0
        r_products=[]
        for ecode in r_item.product_list:
            for product in productList:
                if product.ecode == ecode:
                    r_products.append(product)
        if not r_products:
            isdis=False #【购买商品】项中的一项在传入的商品中没有找到，那么就表示该促销不符合执行了
            is_enable_exec = False  # 不满足可执行条件
            break
            # 第一行促销活动满足条件为数量
        if r_item.target_type == 'qtty':
            # 比较符"GE/大于等于/G大于/E等于"
            if r_item.comp_symb_type == 'ge':
                # 判断当前上行商品是否符合活动条件
                if get_count.getNotOccupiedAll(r_products) >= r_item.value_num:
                    productOneCount = -2
                # 记录可参加的活动
                if get_count.getCountQtty(r_products) >= r_item.value_num:
                    productOnesss = 1
            # 大于
            elif r_item.comp_symb_type == 'g':
                if get_count.getNotOccupiedAll(r_products) > r_item.value_num:
                    productOneCount = -2
                # 记录可参加的活动
                if get_count.getCountQtty(r_products) > r_item.value_num:
                    productOnesss = 1
            # E等于
            elif r_item.comp_symb_type == 'e':
                if r_item.value_num != 0 and get_count.getNotOccupiedAll(r_products) >= r_item.value_num:
                    productOneCount = r_item.value_num
                # 记录可参加的活动
                if get_count.getCountQtty(r_products) >= r_item.value_num and r_item.value_num != 0:
                    productOnesss = r_item.value_num
        # 第一行促销活动满足条件应收金额
        elif r_item.target_type == 'amt_receivable':
            # 比较符"GE/大于等于/G大于/E等于"
            if r_item.comp_symb_type == 'ge' or r_item.comp_symb_type == 'e':
                # 判断当前上行商品是否符合活动条件
                if get_count.getCountAmtReceivableOne(r_products) >= r_item.value_num:
                    productOneCount = -2
                # 记录可参加的活动
                if get_count.getCountAmtReceivableThree(r_products) >= r_item.value_num:
                    productOnesss = 1
            # 大于
            elif r_item.comp_symb_type == 'g':
                # 记录可参加的活动
                if get_count.getCountAmtReceivableThree(r_products) > r_item.value_num:
                    productOnesss = 1
                if get_count.getCountAmtReceivableOne(r_products) > r_item.value_num:
                    productOneCount = -2
        # 第一行促销活动满足条件为零售金额
        elif r_item.target_type == 'amt_retail':
            # 比较符"GE/大于等于/G大于/E等于"
            if r_item.comp_symb_type == 'ge' or r_item.comp_symb_type == 'e':
                # 记录可参加的活动
                if get_count.getCountAmtRetailTwo(r_products) >= r_item.value_num:
                    productOnesss = 1
                # 判断当前上行商品是否符合活动条件
                if get_count.getCountAmtRetailOne(r_products) >= r_item.value_num:
                    productOneCount = -2
            # 大于
            elif r_item.comp_symb_type == 'g':
                # 记录可参加的活动
                if get_count.getCountAmtRetailTwo(r_products) > r_item.value_num:
                    productOnesss = 1
                if get_count.getCountAmtRetailOne(r_products) > r_item.value_num:
                    productOneCount = -2
        # 第一行促销活动满足条件为吊牌金额
        elif r_item.target_type == 'amt_list':
            # 比较符"GE/大于等于/G大于/E等于"
            if r_item.comp_symb_type == 'ge' or r_item.comp_symb_type == 'e':
                # 记录可参加的活动
                if get_count.getCountAmtListTwo(r_products) >= r_item.value_num:
                    productOnesss = 1
                # 判断当前上行商品是否符合活动条件
                if get_count.getCountAmtListOne(r_products) >= r_item.value_num:
                    productOneCount = -2
            # 大于
            elif r_item.comp_symb_type == 'g':
                # 记录可参加的活动
                if get_count.getCountAmtListTwo(r_products) > r_item.value_num:
                    productOnesss = 1
                if get_count.getCountAmtListOne(r_products) > r_item.value_num:
                    productOneCount = -2

        if productOnesss == 0:
            # 不满足执行条件，直接结束循环
            isdis = False
            is_enable_exec = False  # 说明不满足条件（所有商品）
            break


        if not bean.execute_product_list:
            # 如果优惠商品为空的话（说明参与所有商品都可优惠），需要根据未占位商品去判断能否执行此促销
            if productOneCount == -1:
                # 说明不满足择优条件
                isdis = False
                # break

        alldisproducts.append(r_products)
        allproductOneCount.append(productOneCount)
        allproductOnesss.append(productOnesss)

    if is_enable_exec:
        # 如果可以参加此活动，则记录可参加的活动ID
        for r_products in alldisproducts:
            for r_product in r_products:
                r_product.discountId.add(bean.id)

    if not isdis:
        # 如果不符合执行条件，直接返回
        return None



    if not bean.execute_product_list:
        # 没有设置优惠商品
        for r_index,row in enumerate(alldisproducts):
            seatlist = []
            new_total_amt_receivable = 0  # 参与的每个商品计算后的金额总和（不进位）
            new_total_amt_receivable1 = 0  # 每个商品计算后进位所得的金额总和
            productOneCount=allproductOneCount[r_index]
            if productOneCount == -2:
                for productOne in row:
                    for seat in productOne.productSeatList:
                        new_seat, new_amt_receivable, new_amt_receivable1 = basics(seat, bean, userInfo, productOne,
                                                                                   bean.specific_activities[0])
                        if new_seat != None:
                            new_total_amt_receivable = new_total_amt_receivable + new_amt_receivable
                            new_total_amt_receivable1 = new_total_amt_receivable1 + float(new_amt_receivable1)
                            seatlist.append(new_seat)
                        # seatlist.append(basics(seat, bean, userInfo, productOne, bean.specific_activities[0]))
                # splitDiffPrice(seatlist, bean)
            else:
                for i in range(0, productOneCount):
                    seat, productOne = get_count.getNotOccupiedOne(row)
                    new_seat, new_amt_receivable, new_amt_receivable1 = basics(seat, bean, userInfo, productOne,
                                                                               bean.specific_activities[0])
                    if new_seat != None:
                        new_total_amt_receivable = new_total_amt_receivable + new_amt_receivable
                        new_total_amt_receivable1 = new_total_amt_receivable1 + float(new_amt_receivable1)
                        seatlist.append(new_seat)
                    # seatlist.append(basics(seat, bean, userInfo, productOne, bean.specific_activities[0]))
                # splitDiffPrice(copy.deepcopy(seatlist), bean)
            # 计算误差
            new_total_amt_receivable = CalculationPrice(new_total_amt_receivable)
            diffPrice = CalculationPrice(
                util.minus(new_total_amt_receivable, new_total_amt_receivable1))

            splitdiff_and_caculate_discount(seatlist, bean, diffPrice)
    else:
        seatlist = []
        new_total_amt_receivable = 0  # 参与的每个商品计算后的金额总和（不进位）
        new_total_amt_receivable1 = 0  # 每个商品计算后进位所得的金额总和
        for productOne in productListA:
            for seat in productOne.productSeatList:
                new_seat, new_amt_receivable, new_amt_receivable1 = basics(seat, bean, userInfo, productOne, bean.specific_activities[0])
                if new_seat != None:
                    new_total_amt_receivable = new_total_amt_receivable + new_amt_receivable
                    new_total_amt_receivable1 = new_total_amt_receivable1 + float(new_amt_receivable1)
                    seatlist.append(new_seat)
                # seatlist.append(basics(seat, bean, userInfo, productOne, bean.specific_activities[0]))
        # splitDiffPrice(seatlist, bean)
        # 计算误差
        new_total_amt_receivable = CalculationPrice(new_total_amt_receivable)
        diffPrice = CalculationPrice(
            util.minus(new_total_amt_receivable, new_total_amt_receivable1))

        splitdiff_and_caculate_discount(seatlist, bean, diffPrice)


def splitdiff_and_caculate_discount(seatlist, bean, diffPrice):
    """
    误差分摊以及优惠金额计算
    :param seatlist:
    :param bean:
    :param diffPrice:
    :return:
    """
    # 误差分摊
    if float(diffPrice) != 0:
        splitDiffPrice(seatlist, bean, diffPrice=diffPrice)

    # 计算优惠金额
    for seat1 in seatlist:
        # pric = float("%.2f" % float(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
        pric = float(util.Keeptwodecplaces(util.minus(seat1.upamt_receivable, seat1.amt_receivable)))
        seat1.upamt_receivable = seat1.amt_receivable
        seat1.discountPrice.append(pric)




    # #之前的老方法
    # # one为第一行促销活动
    # one = bean.specific_activities[0]
    # # 进入具体运算 遍历每个商品
    # productListA = []
    # for ecode in one.product_list:
    #     for product in productList:
    #         if product.ecode == ecode:
    #             productListA.append(product)
    # # 订单中有此ecode的商品
    # if len(productListA) > 0:
    #     productOneCount = -1
    #     productOnesss = 0
    #     # 第一行促销活动满足条件为数量
    #     if one.target_type == 'qtty':
    #         # 比较符"GE/大于等于/G大于/E等于"
    #         if one.comp_symb_type == 'ge':
    #             # 判断当前上行商品是否符合活动条件
    #             if get_count.getNotOccupiedAll(productListA) >= one.value_num:
    #                 productOneCount = -2
    #             # 记录可参加的活动
    #             if get_count.getCountQtty(productListA) >= one.value_num:
    #                 productOnesss = 1
    #         # 大于
    #         elif one.comp_symb_type == 'g':
    #             if get_count.getNotOccupiedAll(productListA) > one.value_num:
    #                 productOneCount = -2
    #             # 记录可参加的活动
    #             if get_count.getCountQtty(productListA) > one.value_num :
    #                 productOnesss = 1
    #         # E等于
    #         elif one.comp_symb_type == 'e':
    #             if one.value_num != 0 and get_count.getNotOccupiedAll(productListA) >= one.value_num :
    #                 productOneCount = one.value_num
    #             # 记录可参加的活动
    #             if get_count.getCountQtty(productListA) >= one.value_num and one.value_num != 0:
    #                 productOnesss = 1
    #     # 第一行促销活动满足条件应收金额
    #     elif one.target_type == 'amt_receivable':
    #         # 比较符"GE/大于等于/G大于/E等于"
    #         if one.comp_symb_type == 'ge' or one.comp_symb_type == 'e':
    #             # 判断当前上行商品是否符合活动条件
    #             if get_count.getCountAmtReceivableOne(productListA) >= one.value_num:
    #                 productOneCount = -2
    #             # 记录可参加的活动
    #             if get_count.getCountAmtReceivableThree(productListA) >= one.value_num:
    #                 productOnesss = 1
    #         # 大于
    #         elif one.comp_symb_type == 'g':
    #             # 记录可参加的活动
    #             if get_count.getCountAmtReceivableThree(productListA) > one.value_num:
    #                 productOnesss = 1
    #             if get_count.getCountAmtReceivableOne(productListA) > one.value_num:
    #                 productOneCount = -2
    #     # 第一行促销活动满足条件为零售金额
    #     elif one.target_type == 'amt_retail':
    #         # 比较符"GE/大于等于/G大于/E等于"
    #         if one.comp_symb_type == 'ge' or one.comp_symb_type == 'e':
    #             # 记录可参加的活动
    #             if get_count.getCountAmtRetailTwo(productListA) >= one.value_num:
    #                 productOnesss = 1
    #             # 判断当前上行商品是否符合活动条件
    #             if get_count.getCountAmtRetailOne(productListA) >= one.value_num:
    #                 productOneCount = -2
    #         # 大于
    #         elif one.comp_symb_type == 'g':
    #             # 记录可参加的活动
    #             if get_count.getCountAmtRetailTwo(productListA) > one.value_num:
    #                 productOnesss = 1
    #             if get_count.getCountAmtRetailOne(productListA) > one.value_num:
    #                 productOneCount = -2
    #     # 第一行促销活动满足条件为吊牌金额
    #     elif one.target_type == 'amt_list':
    #         # 比较符"GE/大于等于/G大于/E等于"
    #         if one.comp_symb_type == 'ge' or one.comp_symb_type == 'e':
    #             # 记录可参加的活动
    #             if get_count.getCountAmtListTwo(productListA) >= one.value_num:
    #                 productOnesss = 1
    #             # 判断当前上行商品是否符合活动条件
    #             if get_count.getCountAmtListOne(productListA) >= one.value_num:
    #                 productOneCount = -2
    #         # 大于
    #         elif one.comp_symb_type == 'g':
    #             # 记录可参加的活动
    #             if get_count.getCountAmtListTwo(productListA) > one.value_num:
    #                 productOnesss = 1
    #             if get_count.getCountAmtListOne(productListA) > one.value_num:
    #                 productOneCount = -2
    #
    #     # 判断是否是单组合
    #     if len(bean.specific_activities) > 1:
    #         # two为第二行促销活动
    #         two = bean.specific_activities[1]
    #         productListB = []
    #         for ecodeB in two.product_list:
    #             for productB in productList:
    #                 # if (productB.ecode == ecodeB) and (ecodeB not in one.product_list):
    #                 if productB.ecode == ecodeB:
    #                     productListB.append(productB)
    #         productTwoCount = -1
    #         productTwosss = 0
    #         # 订单中有此ecode的商品
    #         if len(productListB) > 0:
    #             # 找到组合商品 判断第二行促销活动商品
    #             # 第二行促销活动满足条件为数量
    #             if two.target_type == 'qtty':
    #                 # 比较符"GE/大于等于/G大于/E等于"
    #                 if two.comp_symb_type == 'ge':
    #                     # 记录可参加的活动
    #                     if get_count.getCountQtty(productListB) >= two.value_num:
    #                         productTwosss = 1
    #                     # 判断当前商品是否符合活动条件
    #                     if get_count.getNotOccupiedAll(productListB) >= two.value_num:
    #                         productTwoCount = -2
    #                 # 大于
    #                 elif two.comp_symb_type == 'g':
    #                     # 记录可参加的活动
    #                     if get_count.getCountQtty(productListB) > two.value_num:
    #                         productTwosss = 1
    #                     if get_count.getNotOccupiedAll(productListB) > two.value_num:
    #                         productTwoCount = -2
    #                 # E等于
    #                 elif two.comp_symb_type == 'e':
    #                     # 记录可参加的活动
    #                     if two.value_num != 0 and get_count.getCountQtty(productListB) >= two.value_num:
    #                         productTwosss = 1
    #                     if two.value_num != 0 and get_count.getNotOccupiedAll(productListB) >= two.value_num:
    #                         productTwoCount = two.value_num
    #             # 第二行促销活动满足条件应收金额
    #             elif two.target_type == 'amt_receivable':
    #                 # 比较符"GE/大于等于/G大于/E等于"
    #                 if two.comp_symb_type == 'ge' or two.comp_symb_type == 'e':
    #                     # 记录可参加的活动
    #                     if get_count.getCountAmtReceivableThree(productListB) >= two.value_num:
    #                         productTwosss = 1
    #                     # 判断当前上行商品是否符合活动条件
    #                     if get_count.getCountAmtReceivableOne(productListB) >= two.value_num:
    #                         productTwoCount = -2
    #                 # 大于
    #                 elif two.comp_symb_type == 'g':
    #                     # 记录可参加的活动
    #                     if get_count.getCountAmtReceivableThree(productListB) > two.value_num:
    #                         productTwosss = 1
    #                     if get_count.getCountAmtReceivableOne(productListB) > two.value_num:
    #                         productTwoCount = -2
    #             # 第二行促销活动满足条件为零售金额
    #             elif two.target_type == 'amt_retail':
    #                 # 比较符"GE/大于等于/G大于/E等于"
    #                 if two.comp_symb_type == 'ge' or two.comp_symb_type == 'e':
    #                     # 记录可参加的活动
    #                     if get_count.getCountAmtRetailTwo(productListB) >= two.value_num:
    #                         productTwosss = 1
    #                     # 判断当前上行商品是否符合活动条件
    #                     if get_count.getCountAmtRetailOne(productListB) >= two.value_num:
    #                         productTwoCount = -2
    #                 # 大于
    #                 elif two.comp_symb_type == 'g':
    #                     # 记录可参加的活动
    #                     if get_count.getCountAmtRetailTwo(productListB) > two.value_num:
    #                         productTwosss = 1
    #                     if get_count.getCountAmtRetailOne(productListB) > two.value_num:
    #                         productTwoCount = -2
    #             # 第二行促销活动满足条件为吊牌金额
    #             elif two.target_type == 'amt_list':
    #                 # 比较符"GE/大于等于/G大于/E等于"
    #                 if two.comp_symb_type == 'ge' or two.comp_symb_type == 'e':
    #                     # 记录可参加的活动
    #                     if get_count.getCountAmtListTwo(productListB) >= two.value_num:
    #                         productTwosss = 1
    #                     # 判断当前上行商品是否符合活动条件
    #                     if get_count.getCountAmtListOne(productListB) >= two.value_num:
    #                         productTwoCount = -2
    #                 # 大于
    #                 elif two.comp_symb_type == 'g':
    #                     # 记录可参加的活动
    #                     if get_count.getCountAmtListTwo(productListB) > two.value_num:
    #                         productTwosss = 1
    #                     if get_count.getCountAmtListOne(productListB) > two.value_num:
    #                         productTwoCount = -2
    #
    #             if productOnesss != 0 and productTwosss != 0:
    #                 for pd in productListA:
    #                     pd.discountId.add(bean.id)
    #                 for pd in productListB:
    #                     pd.discountId.add(bean.id)
    #             if productTwoCount == -1 or productOneCount == -1:
    #                 return
    #
    #             # 组合商品进行赋值占位
    #             groupBasics(productListA, productOneCount, productListB, productTwoCount, bean, userInfo)
    #     # 单 组合
    #     else:
    #         seatlist=[]
    #         for i in range(0, productOneCount):
    #             seat, productOne = get_count.getNotOccupiedOne(productListA)
    #             seatlist.append(basics(seat, bean, userInfo, productOne, bean.specific_activities[0]))
    #         splitDiffPrice(seatlist,bean)


# 组合商品进行赋值占位

def groupBasics(productListA, productOneCount, productListB, productTwoCount, bean, userInfo):
    seatlist = []
    if productOneCount == -2:  # 第一种商品占位
        for productOne in productListA:
            for seat in productOne.productSeatList:
                seatlist.append(basics(seat, bean, userInfo, productOne, bean.specific_activities[0]))
        splitDiffPrice(seatlist, bean)
    else:
        for i in range(0, productOneCount):
            seat, productOne = get_count.getNotOccupiedOne(productListA)
            seatlist.append(basics(seat, bean, userInfo, productOne, bean.specific_activities[0]))
        splitDiffPrice(copy.deepcopy(seatlist), bean)

    # 第二种商品占位
    if productTwoCount == -2:
        for productTwo in productListB:
            for seat in productTwo.productSeatList:
                seatlist.append(basics(seat, bean, userInfo, productTwo, bean.specific_activities[0]))
        splitDiffPrice(copy.deepcopy(seatlist), bean)
    else:
        for i in range(0, productTwoCount):
            seat, productTwo = get_count.getNotOccupiedOne(productListB)
            seatlist.append(basics(seat, bean, userInfo, productTwo, bean.specific_activities[0]))
        splitDiffPrice(seatlist, bean)
    # 同类商品其他件数不能在参加此活动
    if productOneCount != -2 and productTwoCount != -2:
        for productOne in productListA:
            for seat in productOne.productSeatList:
                seat.notProId.append(bean.id)
        for productOne in productListB:
            for seat in productOne.productSeatList:
                seat.notProId.append(bean.id)

