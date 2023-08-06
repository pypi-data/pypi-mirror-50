# -*- coding:utf-8 -*-
"""
    梯度买赠
    2018/10/24
    by李博文
"""

import copy

from pro.apis.GA_api.BG_api import basics_bg
from pro.apis.GA_api.BG_api.buy_a_for_value import tongji
from pro.utils.util import CalculationPrice

def preferential_gd(productList, discountList, userInfo, productList_CP):
    # 1循环活动总长度
    # 2循环进入每一个活动
    # 3做到 54321 45321这种遍历
    give_id = []
    buygift = []
    productListMAX = []
    buygift_list = []

    two_id = set()
    buygift_two_id = []
    can_part_promotion_id = []  # 可以参与的活动ID
    # 深拷贝商品数据
    productlists = copy.deepcopy(productList)

    # 记录一轮循环里第一次出现使用原始数据执行促销的上个促销的索引及执行后的商品结构
    isallpro_upproductlists = []
    isallpro_upindex = -1

    # 定义游标
    index_cursor = 0

    for index in range(0, len(discountList)):

        for bean in discountList:
            n_bean=copy.deepcopy(bean)
            if len(n_bean.product_list) < 1:
                continue

            if isallpro_upindex==-1:
                isallpro_upproductlists=copy.deepcopy(productlists)

            # 返回每个方案计算后的商品集合
            list1 = gradient_buygift(productlists, n_bean, userInfo, copy.deepcopy(productList))
            if list1:
                can_part_promotion_id.append(bean.id)
            if list1 and type(list1) == dict:
                if list1["buygift"]:
                    if list1["dis_id"] not in give_id:
                        give_id.append(list1["dis_id"])
                        buygift_list.append(list1["buygift"])
                    if list1["isallpro"]:
                        # 记录前面执行的组的数据
                        if len(list(two_id)) > 1  and list(two_id) not in buygift_two_id:
                            buygift_two_id.append(list(two_id))
                        if buygift:
                            productListMAX.append(buygift)

                        two_id = set()
                        buygift = []

                        if isallpro_upindex==-1:
                            isallpro_upindex=len(buygift_two_id)-1

                        if isallpro_upindex > -1:
                            productlists = copy.deepcopy(isallpro_upproductlists)

                        # buygift.append(list1)
                        # productListMAX.append(buygift)
                        two_id = set()
                        buygift = []
                    else:
                        if isallpro_upindex==-1:
                            two_id.add(bean.id)
                            buygift.append(list1)
                        else:
                            set(buygift_two_id[isallpro_upindex]).add(bean.id)
                            productListMAX[isallpro_upindex].append(list1)

                    isallpro_upproductlists = copy.deepcopy(productlists)

            # 将当前下标与这次循环下标交换
        index_cursor += 1

        if len(discountList) > 1:
            if index_cursor != len(discountList):
                discountList[0], discountList[index_cursor] = discountList[index_cursor], \
                                                              discountList[0]


        productlists = copy.deepcopy(productList)
        isallpro_upproductlists = []
        isallpro_upindex = -1

        # 将第一轮里可以在一组同时执行的同三类买赠活动筛选组织成需要的结构
        if len(list(two_id)) >= 1  and list(two_id) not in buygift_two_id:
            buygift_two_id.append(list(two_id))
        if buygift:
            productListMAX.append(buygift)
        two_id = set()
        buygift = []

    # 从所有执行的顺序中取出最优的一组
    n_productlists = []
    if productListMAX:
        n_productlists = basics_bg.get_optimalgroupdis(productListMAX)
        buygift_two_id = []
        two_id=set()
        for row in n_productlists:
            two_id.add(row["dis_id"])

        buygift_two_id.append(list(two_id))

        productlists = n_productlists[-1]["product"]

    response = {
        "n_productlists":n_productlists, #最优组促销执行情况，供后面再择优使用
        "product": productlists,
        "buygift": buygift_list if len(buygift_list) >= 1 else [],
        "buygift_two_id": buygift_two_id if len(buygift_two_id) >= 1 else [],
        "can_part_promotion_id": can_part_promotion_id
    }
    return response


# 具体运算
def gradient_buygift(productList, bean, userInfo ,org_productlists):
    # 判断当前活动是否限制会员并且当前用户可否参与
    if bean.members_only:
        if userInfo is not None:
            # 当前用户会员级别不再此活动会员级别范围之内
            if userInfo.id not in bean.members_group:
                return None

        else:
                # 当前活动限制会员参加 且 当前用户不是会员
            return None

    # qtty:数量
    promotion_qtty_sum = 0

    # amt_list:吊牌金额
    promotion_amt_list_sum = 0

    # amt_retail:零售金额
    promotion_amt_retail_sum = 0

    # amt_receivable:应收金额是否满足
    promotion_amt_receivable_sum = 0


    condition_product = []  # 记录条件商品（只存款号）

    # 所有ecode相同对象
    productListA = []


    # 遍历每一件商品合并encode相同的商品
    for ecode in bean.product_list:

        for product in productList:
            if ecode == product.ecode:
                productListA.append(product)
                condition_product.append(ecode)

    is_can_part_activity = False  # 是否满足活动条件

    # 循环添加各种满足条件
    if len(productListA) > 0:
        promotion_qtty_sum,promotion_amt_list_sum,promotion_amt_retail_sum,promotion_amt_receivable_sum,org_promotion_qtty_sum,org_promotion_amt_list_sum,org_promotion_amt_retail_sum,org_promotion_amt_receivable_sum = tongji(productListA)

        # 保留两位小数点
        promotion_amt_list_sum = CalculationPrice(promotion_amt_list_sum)
        promotion_amt_retail_sum = CalculationPrice(promotion_amt_retail_sum)
        promotion_amt_receivable_sum = CalculationPrice(promotion_amt_receivable_sum)
        org_promotion_amt_list_sum = CalculationPrice(org_promotion_amt_list_sum)
        org_promotion_amt_retail_sum = CalculationPrice(org_promotion_amt_retail_sum)
        org_promotion_amt_receivable_sum = CalculationPrice(org_promotion_amt_receivable_sum)
        org_infos = {"org_promotion_qtty_sum": org_promotion_qtty_sum,
                     "org_promotion_amt_list_sum": org_promotion_amt_list_sum,
                     "org_promotion_amt_retail_sum": org_promotion_amt_retail_sum,
                     "org_promotion_amt_receivable_sum": org_promotion_amt_receivable_sum}


        response=None
        # 循环进入函数 从大往下遍历每一个条件
        for promotion in reversed(bean.operation_set):

            # 即在条件商品又在赠送商品列表里的商品集合（只存款号，为之后占位方便），在条件占位时优先占用只是条件商品
            give_product = []

            for ecode in promotion.buygift_product:
                for product in productList:
                    if product.ecode.lower() == ecode["ecode"].lower():
                        if product.ecode in condition_product:
                            give_product.append(product.ecode)

            bean.buygift_product = promotion.buygift_product
            bean.value_num = promotion.value_num
            bean.give_value = promotion.give_value
            bean.comp_symb_type = promotion.comp_symb_type
            bean.promotion_lineno=promotion.promotion_lineno
            if bean.comp_symb_type == "g":
                bean.value_num += 1
            response = basics_bg.not_buy_a_give_a_unify(bean, userInfo, productList,promotion_qtty_sum,
                                                    promotion_amt_list_sum, promotion_amt_retail_sum,
                                                    promotion_amt_receivable_sum,org_infos,org_productlists,give_product)
            if bean.comp_symb_type == "g":
                bean.value_num -= 1

            if type(response) == dict:
                is_can_part_activity = True
                return response
            elif response == 1:
                is_can_part_activity = True

    # response_1 = {}
    # response_1["product"] = productList
    # response_1["buygift"] = []
    if is_can_part_activity:
        return 1
    else:
        return None
    # return response_1
