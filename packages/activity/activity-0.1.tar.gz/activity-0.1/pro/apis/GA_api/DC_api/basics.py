# -*- coding:utf-8 -*-
# author:尹晨
# datetime:2018/9/29 17:03
import copy

from pro.apis.GA_api.DC_api import get_count
from pro.utils.util import CalculationPrice
import pro.utils.util as util


# 优惠基础金额计算
def basics(seat, bean, userInfo, product, operation=None):
    # retail_carryway = globle_params.get_retail_carryway()

    if seat == None or bean == None:
        return None, None, None
    if operation == None:
        operation = bean
    # 因翻倍限制所不能参加的活动 - --活动ID
    if seat.notProId:
        for id in seat.notProId:
            if id == bean.id:
                return None, None, None

    if seat.is_run_other_pro == False:
        return  None, None, None # 不可以进行商品活动
    if seat.seat:
        return  None, None, None # 商品已占位
    # 如果当前商品不参与促销计算，直接返回
    if seat.is_discount == "n":
        return None, None, None
    # 标记剩余未参加商品数量
    product.qttyCount = product.qttyCount - 1
    # 应收金额优惠基础
    if bean.target_item == "amt_receivable":
        amt_receivable = seat.amt_receivable * operation.discount_value
        # 向下取整取出差额
        # seat.diffPrice = amt_receivable - int(amt_receivable)
        # pric = float(seat.amt_receivable - int(amt_receivable))
        # seat.amt_receivable = int(amt_receivable)
        seat.after_dis_amt_receivable.append(seat.amt_receivable)
        # seat.str_discount = seat.str_discount + '参加' + bean.ename + '活动优惠了' + str(pric) + '元\n'
        # 活动是否允许折上折
        if bean.is_run_vip_discount:
            if seat.is_run_vip_discount == False:
                if userInfo.discount != None:
                    # amt_receivable = CalculationPrice(seat.amt_receivable * userInfo.discount)
                    amt_receivable = amt_receivable * userInfo.discount
                    # vipPric = float(seat.amt_receivable - amt_receivable)
                    # seat.amt_receivable = amt_receivable
                    # 设置当前商品明细为已经折上折
                    seat.is_run_vip_discount = True
                    # seat.str_discount = seat.str_discount + "参加" + bean.ename + "活动允许VIP折上折,优惠了" + str(vipPric) + "元\n"
        seat.amt_receivable = CalculationPrice(amt_receivable)
        # 是否与其他商品活动同时执行
        seat.is_run_other_pro = bean.is_run_other_pro
        # 是否与全场活动同时执行
        seat.is_run_store_act = bean.is_run_store_act
        # 当前三类中占位
        seat.seat = True
        # 加入参加过的活动ID
        seat.discountId.append(bean.id)
        # 这次活动优惠的金额
        # seat.discountPrice.append(pric)
    # 零售金额优惠基础
    elif bean.target_item == 'amt_retail':
        # pric = seat.amt_retail - seat.amt_retail * operation.discount_value
        # amt_receivable = seat.amt_receivable - pric
        # seat.diffPrice = amt_receivable - int(amt_receivable)
        # pric = seat.amt_receivable - int(amt_receivable)
        # seat.amt_receivable = int(amt_receivable)
        amt_receivable = seat.amt_retail * operation.discount_value
        seat.after_dis_amt_receivable.append(seat.amt_receivable)
        # seat.str_discount = seat.str_discount + '参加' + bean.ename + '活动优惠了' + str(pric) + '元\n'
        # 活动是否允许折上折
        if bean.is_run_vip_discount:
            if seat.is_run_vip_discount == False:
                if userInfo.discount != None:
                    # vipPric = CalculationPrice((seat.amt_retail - seat.amt_retail * userInfo.discount),
                    #                            retail_carryway)
                    # seat.amt_receivable = seat.amt_receivable - vipPric
                    amt_receivable = amt_receivable * userInfo.discount
                    # 设置当前商品明细为已经折上折
                    seat.is_run_vip_discount = True
                    # seat.str_discount = seat.str_discount + "参加" + bean.ename + "活动允许VIP折上折,优惠了" + str(
                    #     vipPric) + "元\n"
        seat.amt_receivable = CalculationPrice(amt_receivable)
        # 是否与其他商品活动同时执行
        seat.is_run_other_pro = bean.is_run_other_pro
        # 是否与全场活动同时执行
        seat.is_run_store_act = bean.is_run_store_act
        # 当前中类占位
        seat.seat = True
        # 加入参加过的活动ID
        seat.discountId.append(bean.id)
        # 这次活动优惠的金额
        # seat.discountPrice.append(pric)
    # 吊牌金额优惠基础
    elif bean.target_item == 'amt_list':
        # pric = seat.amt_list - seat.amt_list * operation.discount_value
        # amt_receivable = seat.amt_receivable - pric
        # seat.diffPrice = amt_receivable - int(amt_receivable)
        # pric = seat.amt_receivable - int(amt_receivable)
        # seat.amt_receivable = int(amt_receivable)
        amt_receivable = seat.amt_list * operation.discount_value
        seat.after_dis_amt_receivable.append(seat.amt_receivable)
       #  seat.str_discount = seat.str_discount + '参加' + bean.ename + '活动优惠了' + str(pric) + '元\n'
        # 活动是否允许折上折
        if bean.is_run_vip_discount:
            if seat.is_run_vip_discount == False:
                if userInfo.discount != None:
                    # vipPric = CalculationPrice((seat.amt_list - seat.amt_list * userInfo.discount))
                    # seat.amt_receivable = seat.amt_receivable - vipPric
                    amt_receivable = amt_receivable * userInfo.discount
                    # 设置当前商品明细为已经折上折
                    seat.is_run_vip_discount = True
                    # seat.str_discount = seat.str_discount + "参加" + bean.ename + "活动允许VIP折上折,优惠了" + str(vipPric) + "元\n"
        seat.amt_receivable = CalculationPrice(amt_receivable)
        # 是否与其他商品活动同时执行
        seat.is_run_other_pro = bean.is_run_other_pro
        # 是否与全场活动同时执行
        seat.is_run_store_act = bean.is_run_store_act
        # 当前中类占位
        seat.seat = True
        # 加入参加过的活动ID
        seat.discountId.append(bean.id)
        # 这次活动优惠的金额
        # seat.discountPrice.append(pric)
    return seat, amt_receivable, CalculationPrice(amt_receivable)


# 查找出一个未占位的且进行可以进行这次活动的一件商品
def getNotOccupied(list):
    tmpPlist = [i for i in list if i.seat is False and i.is_run_other_pro is True]
    return max(tmpPlist, key=lambda x: x.amt_receivable) if len(tmpPlist) > 0 else None


# 同一个促销方案下择优商品
def pickProduct(productList, productListMax):
    # 健壮性
    if len(productListMax) == 1:
        return productListMax[0]
    # 找到所有ecode存入sets
    sets = set()
    productPick = copy.deepcopy(productList)
    for product in productList:
        sets.add(product.ecode)
    for ecode in sets:
        # 第一个同ecode商品集合
        productCountA = []
        productB = None
        for pds in productPick:
            if pds.ecode == ecode:
                productCountA.append(pds)
        for productPro in productListMax:
            # 第二个同ecode商品集合
            productCountB = []
            for pdPro in productPro:
                if pdPro.ecode == ecode:
                    productCountB.append(copy.deepcopy(pdPro))
                    productB = productPro
            # 所有可参加的活动合并
            for i, pd in enumerate(productPick):
                productPick[i].discountId = productB[i].discountId | productPick[i].discountId
                productB[i].discountId = productPick[i].discountId | productPick[i].discountId
            # 比较当前活动此ecode的商品是否比上一个优惠
            if get_count.getCountAmtReceivableTwo(productCountB) <= get_count.getCountAmtReceivableTwo(productCountA):
                for i, pd in enumerate(productPick):
                    if ecode == pd.ecode:
                        productPick[i] = copy.deepcopy(productB[i])
                        productCountA = productCountB
    return productPick

#分摊差价
def splitDiffPrice(seatList, discount,give_value=None,diffPrice=None):
    '''
    :param seatList: 商品明细列表/换购商品明细列表
    :param discount: 当前活动
    :param give_value: 换购值
    :return:
    '''
    diffPrice_sum = 0
    #清除商品明细列表中的None值
    while None in seatList:
        seatList.remove(None)
    #商品打折分摊差价入口
    # if discount.prom_type_three.upper() == "GA1101" or discount.prom_type_three.upper() == "GA1102" or discount.prom_type_three.upper() == "GA1103" or discount.prom_type_three.upper() == "GA1104":
    #     # 计算总差价
    #     if diffPrice == None:
    #         for seat in seatList:
    #             diffPrice_sum += seat.diffPrice
    #         # 将总差价四舍五入计算，当总差价为0时，结束方法
    #         diffPrice_sum = CalculationPrice(diffPrice_sum)
    #     else:
    #         diffPrice_sum = diffPrice
    #     if diffPrice_sum == 0:
    #         return
    #     # 将商品明细列表按应收价降序排序，进入差价分摊
    #     seatList = sorted(seatList, key=lambda x: x.amt_receivable, reverse=True)
    #     for seat in seatList:
    #         # 取出当前活动ID的下标值，该条明细应收价+1，该活动优惠金额-1
    #         i = seat.discountId.index(discount.id)
    #         seat.amt_receivable = seat.amt_receivable + 1
    #         seat.discountPrice[i] = seat.discountPrice[i] - 1
    #         # 总差价递减1，控制循环次数，当总差价分摊完后，跳出分摊循环，
    #         diffPrice_sum -= 1
    #         if diffPrice_sum == 0:
    #             break
    #     # #计算总差价
    #     # for seat in seatList:
    #     #     diffPrice_sum += seat.diffPrice
    #     # #将总差价四舍五入计算，当总差价为0时，结束方法
    #     # diffPrice_sum = CalculationPrice(diffPrice_sum)
    #     # if diffPrice_sum == 0:
    #     #     return
    #     # #将商品明细列表按应收价降序排序，进入差价分摊
    #     # seatList = sorted(seatList, key=lambda x: x.amt_receivable, reverse=True)
    #     #
    #     # while abs(diffPrice_sum)>0:
    #     #     ceil=0.01
    #     #     if abs(diffPrice_sum)>=1:
    #     #         ceil=1
    #     #     elif 0.1<=abs(diffPrice_sum) and abs(diffPrice_sum)<1:
    #     #         ceil=0.1
    #     #     if diffPrice_sum<0:
    #     #         ceil=-ceil
    #     #     seatnum=0
    #     #     seatnum1 = 0
    #     #     for seat in seatList:
    #     #         if (seat.amt_receivable + ceil)<0:
    #     #             seatnum1=seatnum1+1
    #     #             continue
    #     #         if float(util.div(seat.amt_receivable,seat.amt_list))>=1:
    #     #             seatnum=seatnum+1
    #     #             continue
    #     #         #取出当前活动ID的下标值，该条明细应收价+1，该活动优惠金额-1
    #     #         i = seat.discountId.index(discount.id)
    #     #         seat.amt_receivable = CalculationPrice(seat.amt_receivable + ceil)
    #     #         seat.discountPrice[i] = CalculationPrice(seat.discountPrice[i] - ceil)
    #     #         #总差价递减1，控制循环次数，当总差价分摊完后，跳出分摊循环，
    #     #         diffPrice_sum -= ceil
    #     #         diffPrice_sum=CalculationPrice(diffPrice_sum)
    #     #         if diffPrice_sum == 0:
    #     #             break
    #     #     if diffPrice_sum == 0:
    #     #         break
    #     #     if seatnum==len(seatList):
    #     #         break
    #     #     if seatnum1==len(seatList):
    #     #         break
    #全场换购分摊差价入口
    # if discount.prom_type_three.upper()=="PA1401" or discount.prom_type_three.upper()=="PA1402" or discount.prom_type_three.upper()=="PA1403":
    if diffPrice == None:
        # 计算总差价
        for seat in seatList:
            diffPrice_sum += seat.diffPrice
        # 将总差价四舍五入计算，当总差价为0时，结束方法
        diffPrice_sum = CalculationPrice(diffPrice_sum)
        if diffPrice_sum == 0:
            return
    else:
        diffPrice_sum = diffPrice
    # 将商品明细列表按应收价降序排序，进入差价分摊
    seatList = sorted(seatList, key=lambda x: x.amt_receivable, reverse=False)
    while abs(diffPrice_sum) > 0:
        ceil = 0.01
        if abs(diffPrice_sum) >= 1:
            ceil = 1
        elif 0.1 <= abs(diffPrice_sum) and diffPrice_sum < 1:
            ceil = 0.1
        if float(diffPrice_sum) < 0:
            ceil = -ceil
        seatnum = 0
        seatnum1 = 0
        for seat in seatList:
            if (seat.amt_receivable + ceil) < 0:
                seatnum1 = seatnum1 + 1
                continue
            if float(util.div(seat.amt_receivable + ceil, seat.amt_list)) > 1:
                seatnum = seatnum + 1
                continue
            # 取出当前活动ID的下标值，该条明细应收价+1，该活动优惠金额-1
            # i = seat.fulldiscounts.index(discount.id)
            seat.amt_receivable = seat.amt_receivable + ceil
            # seat.fulldiscountPrice[i] = seat.fulldiscountPrice[i] - ceil
            # 总差价递减1，控制循环次数，当总差价分摊完后，跳出分摊循环，
            diffPrice_sum -= ceil
            diffPrice_sum = CalculationPrice(diffPrice_sum)
            if diffPrice_sum == 0:
                break
        if diffPrice_sum == 0:
            break

        if seatnum == len(seatList):
            break
        if seatnum1 == len(seatList):
            break


