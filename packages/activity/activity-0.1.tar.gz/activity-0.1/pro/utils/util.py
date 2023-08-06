# coding=utf-8
import json
import socket
import copy
import sys
import importlib
from decimal import Decimal
from pro.settings import globle_params


# 殷海翔写的
def equalsIgnoreCase(str1, str2):
    return str1.lower() == str2.lower()



def product_give(not_product):
    "计算赠送列表中未站位商品"
    n = 0
    for giv in not_product:
        for give_seat in giv.productSeatList:
            if give_seat.is_buy_gifts == "n":
                n+=1
    return n


def sort_ab_a_number(productlistA, not_product_ListA):
    """
    AB A 数量
    商品排序
    :param productlistA:
    :param not_product_ListA:
    :return:
    """
    # 重组所有列表
    productListA = []
    for product in productlistA:
        # 取出当前不存在当前赠送列表中的商品
        if product.ecode.lower() != not_product_ListA[0].ecode.lower():
            productListA.append(product)
            # 将原有列表删除
            productlistA.pop(productlistA.index(product))

    # 升序降序
    productListA = sorted(productListA, key=lambda i: i.productSeatList[0].amt_list, reverse=True)

    # 将原有列表降序排序
    productlistA = sorted(productlistA, key=lambda i: i.productSeatList[0].amt_list)

    for i in productlistA:
        productListA.append(i)

    return productListA





def max_give(bean, sum_moeny):
    """
    计算最大翻倍数
    :param bean:
    :param sum_moeny:
    :return:
    """
    # 计算出倍数最大金额

    result = bean.value_num * bean.max_times

    if sum_moeny >= result:
        return  bean.max_times * bean.give_value


    return int(sum_moeny // bean.value_num * bean.give_value)


def sort_pro_two(condition, productlistA, not_product_ListA):
    """
    a ab 排序
    :param condition:
    :param productlistA:
    :param not_product_ListA:
    :return:
    """
    notproductList = []
    for give in not_product_ListA:
        if give.ecode.lower() != productlistA[0].ecode.lower():
            notproductList.append(give)
            not_product_ListA.pop(not_product_ListA.index(give))

    notproductList = sorted(notproductList, key=lambda i: getattr(i.productSeatList[0], condition))

    not_product_ListA = sorted(not_product_ListA, key=lambda i: getattr(i.productSeatList[0], condition))

    for i in not_product_ListA:
        notproductList.append(i)

    return notproductList


def sort_pro(condition, productlistA, not_product_ListA):
    """
    AB A 排序
    :param condition:
    :param productlistA:
    :param not_product_ListA:
    :return:
    """
    # 重组所有列表
    productListA = []


    for product in productlistA:
        # 取出当前不存在当前赠送列表中的商品
        if product.ecode.lower() != not_product_ListA[0].ecode.lower():
            productListA.append(product)



    # 升序降序
    productListA = sorted(productListA, key=lambda i: getattr(i.productSeatList[0], condition), reverse=True)

    # 将原有列表降序排序
    productlistA = sorted(productlistA, key=lambda i: getattr(i.productSeatList[0], condition))

    for i in not_product_ListA:
        productListA.append(i)

    return productListA


def check_ecode_number(productList):
    """
    取相同Ecode
    :param productList:
    :return:
    """
    result = [productList[0]]
    for product in productList:

        for i in result:
            if product.ecode.lower() != i.ecode.lower():
                result.append(product)

    return len(result)


def result_number(result_money, bean):
    """
    计算最大赠送件数
    :param result_money:
    :param bean:
    :return:
    """
    if bean.value_num == 1:
        return 1
    number = result_money // bean.value_num
    result = int(number * bean.give_value)

    return result


def get_product_sum(productList):
    """
    用于计算未站位商品总数
    :param productList: 商品列表
    :return: 数量
    """

    n = 0
    if not productList:
        return n
    for i in productList:
        for seat in i.productSeatList:
            if seat.seat == False and seat.is_run_other_pro != False:
                n += 1
    return n

def get_money_sum(productList, condition):
    """
    计算条件的价钱
    :param productList:
    :return:
    """
    result = 0
    if not productList:
        return 0
    if len(productList) == 1:
        for product in productList:

            for seat in product.productSeatList:
                if seat.seat == False and seat.is_run_other_pro != False:
                    result += getattr(seat, condition)
    else:
        for product in productList:
            for seat in product.productSeatList:
                if seat.seat == False and seat.is_run_other_pro != False:
                    result += getattr(seat, condition)
    return result


def checkproduct(productJsonList):
    """
    校验订单商品集合
    Date 2018/9/29
    by 李博文
    :param productJsonList:
    :return:
    """

    if not productJsonList:
        raise NameError("商品列表为空")

    # 价钱和数量强转
    try:
        float(productJsonList["amt_list"])
        float(productJsonList["amt_retail"])
        float(productJsonList["amt_receivable"])
        int(productJsonList["qtty"])
    except Exception as e:
        raise e
    return productJsonList


def checkpromotion(promotionJsonObj):
    """
     校验商品活动集合
     date 2018/9/29
     by 李博文
    :param promotionJsonObj:
    :return:
    """
    # 定义比较值 Interval
    interval_value = (1, 3)

    if not promotionJsonObj:
        raise NameError('商品活动集合非法')

    # 校验二类是否合法
    if not 1 <= int(promotionJsonObj["promotion_list"]["product_activity_list"][0].get("prom_type_two")) <= 6:
        raise NameError('二类非法')

    # 不能为空字段
    if not all([
        # 对应内容代表含义在三类明细
        (promotionJsonObj["promotion_list"]["product_activity_list"][0].get("prom_type_three")),
        # 活动名称
        (promotionJsonObj["promotion_list"]["product_activity_list"][0].get("ename")),
        # 二类活动级别
        (promotionJsonObj["promotion_list"]["product_activity_list"][0].get("prom_type_two_c")),
        # 活动发布时间(毫秒值)
        (promotionJsonObj["promotion_list"]["product_activity_list"][0].get("publish_date")),
        # 是/否(仅限会员参加)
        (promotionJsonObj["promotion_list"]["product_activity_list"][0].get("members_only")),
        # 是否与其他商品活动同时执行
        (promotionJsonObj["promotion_list"]["product_activity_list"][0].get("is_run_other_pro")),
        # 是否与全场活动同时执行
        (promotionJsonObj["promotion_list"]["product_activity_list"][0].get("is_run_store_act")),
        # 是否享受vip折上折
        (promotionJsonObj["promotion_list"]["product_activity_list"][0].get("is_run_vip_discount")),
        # 最大翻倍条件
        (promotionJsonObj["promotion_list"]["product_activity_list"][0].get("max_times")),
        # 组合打折换购等上下组合条件 默认并且
        (promotionJsonObj["promotion_list"]["product_activity_list"][0].get("rela_symb_type")),
        # 活动具体方案

    ]):
        raise NameError
    # 仅限同吊牌价 类型数字  换购条件
    if not int(
            promotionJsonObj["promotion_list"]["product_activity_list"][0].get("exchange_condition")) in interval_value:
        raise NameError

    # 买赠条件
    if not int(promotionJsonObj["promotion_list"]["product_activity_list"][0].get("gift_condition")) in interval_value:
        raise NameError

    # 校验具体活动方案

    #  校验所有参加活动的商品集合

    if not promotionJsonObj["promotion_list"]["product_activity_list"][0].get("specific_activities")[0].get(
            'product_list'):
        raise NameError

    # 校验比较集合

    # 校验比较符
    if not \
    promotionJsonObj["promotion_list"]["product_activity_list"][0].get("specific_activities")[0].get('operation_set')[
        0].get("comp_symb_type"):
        raise NameError
    # 比较值
    if not \
    promotionJsonObj["promotion_list"]["product_activity_list"][0].get("specific_activities")[0].get('operation_set')[
        0].get("value_num"):
        raise NameError
    # 优惠价格基础
    if not \
    promotionJsonObj["promotion_list"]["product_activity_list"][0].get("specific_activities")[0].get('operation_set')[
        0].get("target_item"):
        raise NameError

    # 转换折扣值 加非空
    if not float(promotionJsonObj["promotion_list"]["product_activity_list"][0].get("specific_activities")[0].get(
            'operation_set')[0].get("discount_value")):
        raise NameError
    # 转换满减值 加非空
    if not float(promotionJsonObj["promotion_list"]["product_activity_list"][0].get("specific_activities")[0].get(
            'operation_set')[0].get("money_off_value")):
        raise NameError
    # 特价值
    if not float(promotionJsonObj["promotion_list"]["product_activity_list"][0].get("specific_activities")[0].get(
            'operation_set')[0].get("money_off_value")):
        raise NameError
    # 吊牌价
    if not \
    promotionJsonObj["promotion_list"]["product_activity_list"][0].get("specific_activities")[0].get('operation_set')[
        0].get("buy_gifts").get('product_list')[0].get("amt_list"):
        raise NameError
    # ecode
    if not \
    promotionJsonObj["promotion_list"]["product_activity_list"][0].get("specific_activities")[0].get('operation_set')[
        0].get("buy_gifts").get('product_list')[0].get("ecode"):
        raise NameError
    # 赠送 ID
    if not int(promotionJsonObj["promotion_list"]["product_activity_list"][0].get("specific_activities")[0].get(
            'operation_set')[0].get("buy_gifts").get('ticket_list')[0].get("id")):
        raise NameError
    # 优惠券名
    if not \
    promotionJsonObj["promotion_list"]["product_activity_list"][0].get("specific_activities")[0].get('operation_set')[
        0].get("buy_gifts").get('ticket_list')[0].get("name"):
        raise NameError
    # 赠品数量
    if not \
    promotionJsonObj["promotion_list"]["product_activity_list"][0].get("specific_activities")[0].get('operation_set')[
        0].get("buy_gifts").get('ticket_list')[0].get("name"):
        raise NameError
    # 换购享受值 引擎根据三类id判断是否是打折/特价/优惠  是否是组合/统一
    if not int(promotionJsonObj["promotion_list"]["product_activity_list"][0].get("specific_activities")[0].get(
            'operation_set')[0].get("redemption")["purchase_condition"]):
        raise NameError
    # 换购商品ecode
    if not \
    promotionJsonObj["promotion_list"]["product_activity_list"][0].get("specific_activities")[0].get('operation_set')[
        0].get("redemption")["product_list"][0].get("ecode"):
        raise NameError
    # 换购商品吊牌价
    if not \
    promotionJsonObj["promotion_list"]["product_activity_list"][0].get("specific_activities")[0].get('operation_set')[
        0].get("redemption")["product_list"][0].get("amt_list"):
        raise NameError
    # 换购商品数量
    if not int(promotionJsonObj["promotion_list"]["product_activity_list"][0].get("specific_activities")[0].get(
            'operation_set')[0].get("redemption")["give_value"]):
        raise NameError
    # 买免值
    if not float(promotionJsonObj["promotion_list"]["product_activity_list"][0].get("specific_activities")[0].get(
            'operation_set')[0].get("buy_from")):
        raise NameError
    return promotionJsonObj


def checkuser(userJsonObje):
    """
    校验user数据
    如果是会员就属性都存在 如果不是会员就是None

    :param userJsonObje:
    :return:
    """
    try:
        if float(userJsonObje['user']['discount']) and int(userJsonObje['user']['id']):
            return userJsonObje
        return None
    except Exception as e:
        raise e


def add(num1, num2):
    '''
    两个数字相加精度处理
    :param num1:
    :param num2:
    :return:
    '''
    return str(Decimal(str(num1)) + Decimal(str(num2)))


def minus(num1, num2):
    '''
    两个数字相减精度处理
    :param num1:
    :param num2:
    :return:
    '''
    return str(Decimal(str(num1)) - Decimal(str(num2)))


def mul(num1, num2):
    '''
    两个数字相乘精度处理
    :param num1:
    :param num2:
    :return:
    '''
    return str(Decimal(str(num1)) * Decimal(str(num2)))


def div(num1, num2):
    '''
    两个数字相除精度处理
    :param num1:
    :param num2:
    :return:
    '''
    if float(num2) == 0:
        return "0"
    return str(Decimal(str(num1)) / Decimal(str(num2)))


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:

        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def CalculationPrice(price):
    '''
    根据进位方式系统参数来计算金额
    outhor：何小霞 2018/10/31
    :param price: 要计算的金额
    :return:
    '''
    try:
        # (保留小数位)1;(四舍五入取整)2;(直接取整)3;(进位取整)4;(四舍五入到角)5;(取整到角)6;
        retail_carryway = str(globle_params.get_retail_carryway())  # 进位方式系统参数值
        new_price = price
        new_price1 = ""
        new_price2 = "00"
        new_price3 = "0"
        new_price = str(price)
        price1 = new_price.split(".")
        if price1 and len(price1) > 1:
            new_price1 = price1[0]
            new_price2 = price1[1][:2]
            new_price3 = price1[1][:1]
        else:
            new_price1 = new_price
        if retail_carryway == "1":
            # 由于python中没有保留两位小数（不四舍五入）的方法，所以只能变相分割截取字符串
            new_price = Keeptwodecplaces(new_price)
        elif retail_carryway == "2":
            new_price = ("%.2f" % round(float(add(price, 0.001))))  # "%.2f" % round(Decimal(price)) #
        elif retail_carryway == "3":
            if new_price1:
                new_price = ("%.2f" % float(new_price1))
        elif retail_carryway == "4":
            if new_price1 and new_price2 != "00" and new_price2 != "0":
                if float(new_price1) < 0:
                    new_price = ("%.2f" % (float(new_price1) + (-1)))
                else:
                    new_price = ("%.2f" % (float(new_price1) + 1))
            else:
                new_price = ("%.2f" % float(new_price1))
        elif retail_carryway == "5":
            new_price = ("%.2f" % round(float(add(price, 0.0001)), 1))  # ("%.2f" % round(Decimal(price),1))
        elif retail_carryway == "6":
            if new_price1 and new_price3:
                new_price = ("%.2f" % float(new_price1 + "." + new_price3))
        else:
            new_price = ("%.2f" % round(float(add(price, 0.001))))  # ("%.2f" % float(Decimal(str(round(float(price))))))
        return float(new_price)
    except Exception as e:
        return float("%.2f" % round(float(price)))


def Keeptwodecplaces(price):
    '''
    将金额保留两位小数方法（不四舍五入）
    outhor:何小霞 2018/10/31
    :param price:
    :return:
    '''
    try:
        price = add(price, 0.00001)
        new_price1 = ""
        new_price2 = "00"
        new_price3 = "0"
        new_price = str(price)
        price1 = new_price.split(".")
        if price1 and len(price1) > 1:
            new_price1 = price1[0]
            new_price2 = price1[1][:2]
            new_price3 = price1[1][:1]
        else:
            new_price1 = price1[0]
            if price1[1] and len(price1[1]) > 1:
                new_price2 = price1[1][:2]
            else:
                new_price3 = price1[1][:1]
                new_price2 = new_price3 + "0"
        if new_price2 == "0":
            new_price2 = "00"
        return ("%.2f" % float(new_price1 + "." + new_price2))
    except Exception as e:
        return ("%.2f" % (float(price)))


def calculation(productsobj,dis_onetype="PA"):
    '''
    根据优惠重新计算参与商品的价格、金额
    author:何小霞
    :param productsobj:要参与计算的数据信息
    :param dis_onetype:标记是那种大类促销活动进入，默认是全场活动（PA），传入（GA）表示是商品活动  --2019-06-28
    :return:
    '''
    new_disprice = 0
    products = productsobj["disproductList"]
    # 计算的时候，要减去特例品的价格
    new_total_amt_receivable = float(minus(productsobj.get("new_total_amt_receivable", 0), productsobj.get("special_total_amt_receivable", 0)))
    if new_total_amt_receivable < 0:
        new_total_amt_receivable = 0
    total_oldamt_receivable = float(minus(productsobj.get("total_oldamt_receivable", 0), productsobj.get("special_total_amt_receivable", 0)))
    if total_oldamt_receivable == 0:
        total_oldamt_receivable = 1
    newdis = float(new_total_amt_receivable) / float(
        total_oldamt_receivable)
    a = len(products)
    seat_list = []  # 参与的商品列表
    for i in range(a):
        itemproduct = products[i]
        row_total_amt_receivable = 0
        if itemproduct.productSeatList[0].is_discount == "y":
            for row in itemproduct.productSeatList:
                ReceivablePrice = float(mul(float(row.amt_receivable), float(
                    newdis)))  # "%.2f" % round(float(itemproduct["PriceList"])*float(newdis)))  # 实收价
                row.amt_receivable = CalculationPrice(ReceivablePrice)
                row_total_amt_receivable = row_total_amt_receivable + row.amt_receivable
                seat_list.append(row)
            itemproduct.total_amt_receivable = row_total_amt_receivable
            products[i] = itemproduct
            new_disprice = float(add(new_disprice, float(itemproduct.total_amt_receivable)))
    diff = CalculationPrice(
        minus(new_total_amt_receivable, new_disprice))  # ("%.2f" % (new_price-new_disprice)))
    if abs(diff) > 0:
        # 如果有误差的话进行分摊
        # products = flattenDiffPirce(diff, products)
        splitDiffPrice(seat_list, diffPrice=diff)
    for row in products:
        pro_seat = row.productSeatList
        for row1 in pro_seat:
            if row1.fulldiscounts or row1.discountId:
                if row1.is_buy_gifts == 'y' or row1.is_taken_off==True or row1.is_repurchase=='y' or row1.is_discount == "n":
                    continue
                if dis_onetype=="GA":
                    row1.discountPrice.append(CalculationPrice(minus(row1.upamt_receivable, row1.amt_receivable)))
                else:
                    row1.fulldiscountPrice.append(CalculationPrice(minus(row1.upamt_receivable, row1.amt_receivable)))
                    row1.upamt_receivable = row1.amt_receivable

    productsobj["disproductList"] = []
    productsobj["disproductList"] = products
    return productsobj

def all_for_one(disproductList,buygifts,gifts_ecodes,productList=None):
    if buygifts != []:
        discountslist = []
        buygiftslists = []
        if productList!=None:
            for row in productList:
                for row1 in row.productSeatList:
                    if row1.ecode in gifts_ecodes:
                        discountslist.append(row1)
        for row in disproductList:
            for row1 in row.productSeatList:
                if row1.ecode in gifts_ecodes:
                    discountslist.append(row1)
        for row in buygifts:
            buygiftslist = []
            if "purchase" in row.keys():
                # operations=row["bg"]["operations"]
                # # num控制循环次数
                # num = row["bg"]["qtty"]
                # # 将活动换购梯度按换购值降序排序，统一优惠换购按换购值升序排序
                # operation_set = sorted(operations, key=lambda x: x["redemption"]["purchase_condition"], reverse=True)
                # if row["bg"]["type_three"] == "PA1403":
                #     operation_set = sorted(operation_set, key=lambda x: x["redemption"]["purchase_condition"],
                #                            reverse=False)
                # if row != [] and num != 0:
                #     # 遍历换购梯度，从换购列表匹配录入商品
                #     for operation in operation_set:
                #         rdmp = operation["redemption"]
                #         # 将每个梯度的换购列表按吊牌价升序排序，保证先换购便宜的商品
                #         product_list = sorted(rdmp["product_list"], key=lambda x: x["AMT_LIST"], reverse=False)
                #         for pro in product_list:
                #             discountslist = sorted(discountslist, key=lambda x: x.amt_receivable, reverse=False)  # 按照应收价格升序
                #             for product in discountslist:
                #                 if pro["ECODE"] == product.ecode:
                #                     if num == 0:
                #                         break
                #                     if product.is_repurchase == 'y':
                #                         continue
                #                     elif product.ecode in gifts_ecodes:
                #                         # 当匹配到商品时，改变商品明细，是否为换购品设为y，记录活动ID，记录换购梯度，记录换购组别
                #                         product.is_repurchase = 'y'
                #                         num -= 1
                continue
            for row1 in row["disproductList"]:
                for row2 in row1.productSeatList:
                    if row2.is_buy_gifts=="y" and row2.fulldiscounts!=[]:
                        buygiftslist.append(row2)
            for row3 in row["productList"]:
                for row4 in row3.productSeatList:
                    if row4.is_buy_gifts=="y" and row4.fulldiscounts!=[]:
                        buygiftslist.append(row4)
            buygiftslists.append(buygiftslist)
        for i in range(0,len(buygiftslists)):
            buygiftslists[i]=sorted(buygiftslists[i],key=lambda x:x.amt_list,reverse=False)
            discountslist=sorted(discountslist,key=lambda x:x.amt_list and len(x.fulldiscounts),reverse=False)
            for row_b, row_d in zip(buygiftslists[i], discountslist):
                if row_b.ecode == row_d.ecode:
                    if row_b.is_buy_gifts == "y":
                        if row_d.is_buy_gifts == "y":
                            continue
                        row_d.is_buy_gifts = "y"
                        for pro_id in row_b.fulldiscounts:
                            if pro_id not in row_d.fulldiscounts:
                                row_d.fulldiscounts.append(pro_id)
                        for pro_dis in row_b.fulldiscountPrice:
                            if pro_dis not in row_d.fulldiscountPrice:
                                row_d.fulldiscountPrice.append(pro_dis)
                    else:
                        for pro_id in row_b.fulldiscounts:
                            if pro_id not in row_d.fulldiscounts:
                                row_d.fulldiscounts.append(pro_id)
                        for pro_dis in row_b.fulldiscountPrice:
                            if pro_dis not in row_d.fulldiscountPrice:
                                row_d.fulldiscountPrice.append(pro_dis)






def flattenDiffPirce(diff, products,distid=-1):
    '''
    误差分摊拆分
    author:何小霞
    edit by hexiaoxia 2019/04/16 添加入参 distid
    :param diff: 误差
    :param products: 参与的商品
    :param distid: 促销ID，当传入值，表示商品活动处理误差进入，例如：商品特价等
    :return:
    '''
    if distid==-1:
        products = sorted(products, key=lambda x: x.total_amt_receivable)
    ceil = 0.01  # 最小分摊单位目前写死按照保留两位小数的最小单位进位
    newskus = []
    old_diff = diff
    while abs(float(diff)) > 0:
        ceil = 0.01
        if float(old_diff) < 0:
            ceil = -0.01
        if (abs(diff) < abs(ceil)):
            diff = 0
            break
        ab = int(diff / ceil)
        if abs(diff) >= abs(ceil):
            for i in range(len(products)):
                newskus = []
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
                    ab = int(diff / ceil)
                elif 10 > abs(diff) >= 1:
                    ceil = 1
                    if float(old_diff) < 0:
                        ceil = -1
                    ab = int(diff / ceil)
                elif 0.1 <= abs(diff) < 1:
                    ceil = 0.1
                    if float(old_diff) < 0:
                        ceil = -0.1
                    ab = int(diff / ceil)
                else:
                    ab = int(diff / ceil)
                row_item = products[i]
                productSeatList = row_item.productSeatList
                for item in productSeatList:
                    if item.is_buy_gifts=='y' or item.is_taken_off==True or item.is_repurchase=='y' or item.is_discount == "n":
                        continue
                    if distid!=-1 and distid not in item.discountId:
                        continue

                    if abs(diff) > 0 and float(item.amt_receivable) / float(item.amt_list) > 1:
                        continue
                    oldqty = int(item.qtty)
                    oldprice = float("%.2f" % float(mul(item.amt_receivable, item.qtty)))
                    if diff < 0:
                        if len(products) == 1:
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
                    ReceivablePrice = float(add(float(item.amt_receivable), ceil))
                    if distid !=-1:
                        discountPrice = float(add(float(item.discountPrice[-1]), ceil))
                        item.discountPrice[-1] = CalculationPrice(discountPrice)
                    diff = CalculationPrice(float("%.2f" % float(minus(diff, mul(ceil, oldqty)))))
                    item.amt_receivable = CalculationPrice(ReceivablePrice)# 应收价格
                    if diff == 0:
                        break
                products[i].productSeatList = productSeatList
                if diff == 0:
                    break
        else:
            diff = 0

    products = sorted(products, key=lambda x: x.lineno)
    return products




def get_settings():
    """
    处理动态加载配置文件
    date /2018/10/16
    by 李博文
    :param :
    :return:
    """
    # if sys.argv[1] == "pro":
    if sys.argv[1] == "dev":
        return importlib.import_module('pro.settings.development')
    elif sys.argv[1] == "pre":
        return importlib.import_module('pro.settings.preissue')
    elif sys.argv[1] == "pro":
        return importlib.import_module('pro.settings.production')

def get_distypeename(type_key,type_flag):
    '''
    促销各类编码对应中文说明
    :param type_key:
    :param type_flag:
    :return:
    '''
    # 一些字符表示对应的中文
    #促销大类编码、中文说明对应字典
    promotion_type_one = {"GA": "商品活动",
                          "PA": "全场活动"}
    # 促销中类编码、中文说明对应字典
    promotion_type_two = {"1": "打折",
                          "2": "满减",
                          "3": "特价",
                          "4": "买赠",
                          "5": "换购",
                          "6": "买免"}
    # 促销三类编码、中文说明对应字典
    promotion_type_three = {"GA1101": "统一折扣",
                            "GA1102": "多种折扣",
                            "GA1103": "递增折扣",
                            "GA1104": "组合折扣",
                            "PA1101": "统一折扣",
                            "PA1102": "多种折扣",
                            "PA1103": "递增折扣",
                            "GA1401": "统一送赠品",
                            "GA1402": "梯度送赠品",
                            "GA1403": "统一送券",
                            "GA1404": "梯度送券",
                            "GA1405": "组合送赠品",
                            "PA1301": "统一送赠品",
                            "PA1302": "梯度送赠品",
                            "PA1303": "统一送券",
                            "PA1304": "梯度送券",
                            "GA1701": "统一送赠品",
                            "GA1702": "梯度送赠品",
                            "GA1703": "组合送赠品",
                            "PA1601": "统一送赠品",
                            "PA1602": "梯度送赠品",
                            "GA1801": "统一送赠品",
                            "GA1802": "梯度送赠品",
                            "GA1803": "组合送赠品",
                            "PA1701": "统一送赠品",
                            "PA1702": "梯度送赠品",
                            "GA1201": "统一减现",
                            "GA1202": "梯度减现",
                            "GA1203": "组合减现",
                            "GA1301": "统一特价",
                            "GA1302": "梯度特价",
                            "GA1303": "组合特价",
                            "GA1501": "统一特价换购",
                            "GA1502": "组合特价换购",
                            "GA1503": "统一打折换购",
                            "GA1504": "组合打折换购",
                            "GA1505": "统一优惠换购",
                            "GA1506": "组合优惠换购",
                            "GA1601": "统一买免",
                            "GA1602": "组合买免",
                            "PA1201": "统一减现",
                            "PA1202": "梯度减现",
                            "PA1401": "统一特价换购",
                            "PA1402": "统一打折换购",
                            "PA1403": "统一优惠换购",
                            "PA1501": "买免"
                            }
    distypeename="-"
    if type_flag==1:
        distypeename=promotion_type_one.get(type_key,"-")
    elif type_flag==2:
        distypeename = promotion_type_two.get(type_key, "-")
    elif type_flag==3:
        distypeename = promotion_type_three.get(type_key, "-")

    return distypeename

def splitDiffPrice(seatList, diffPrice=0):
    """
    :param seatList: 商品明细列表
    :param diffPrice: 误差值
    :return:
    """
    diffPrice_sum = diffPrice
    # 清除商品明细列表中的None值
    while None in seatList:
        seatList.remove(None)
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
            if float(div(seat.amt_receivable + ceil, seat.amt_list)) > 1:
                seatnum = seatnum + 1
                continue
            # 该条明细应收价+1，该活动优惠金额-1
            seat.amt_receivable = seat.amt_receivable + ceil
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
