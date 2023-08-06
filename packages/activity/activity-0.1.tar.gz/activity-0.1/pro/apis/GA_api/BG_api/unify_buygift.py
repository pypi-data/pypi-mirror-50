# -*- coding:utf-8 -*-
"""
    统一买赠
    2018/10/24
    by李博文
    edit by hexiaoxia 2019/04/28
    修改项：
    1.整体促销实现方式做了修改
"""

import copy

from pro.apis.GA_api.BG_api import basics_bg
from pro.apis.GA_api.BG_api.buy_a_for_value import fuwei,tongji
from pro.utils.util import CalculationPrice
from pro.apis.GA_utils import recovery_seat

# 统一买赠入口
def preferential_bg(product_object_list, unify_buygift_list, userInfo, productList_CP):
    # 1循环活动总长度
    # 2循环进入每一个活动
    # 3做到 54321 45321这种遍历
    give_id = []

    productListMAX = []

    # 暂时记录 id
    two_id = set()

    # 最终返回的成双id
    buygift_two_id = []
    buygift=[]
    buygift_list = []

    productlists = copy.deepcopy(product_object_list)
    can_part_promotion_id = []
    #记录一轮循环里第一次出现使用原始数据执行促销的上个促销的索引及执行后的商品结构
    isallpro_upproductlists=[]
    isallpro_upindex=-1

    index_cursor = 0
    for index in range(0, len(unify_buygift_list)):

        for bean in unify_buygift_list:
            if len(bean.product_list) < 1:
                continue

            if isallpro_upindex==-1:
                isallpro_upproductlists=copy.deepcopy(productlists)

            # 返回每个方案计算后的商品集合
            list1 = unify_buygift(productlists, bean, userInfo, copy.deepcopy(product_object_list))
            if list1:
                can_part_promotion_id.append(bean.id)
            if list1 and type(list1) == dict:
                if list1["buygift"]:
                    if list1["dis_id"] not in give_id:
                        give_id.append(list1["dis_id"])
                        buygift_list.append(list1["buygift"])
                    if list1["isallpro"]:
                        # 记录前面执行的组的数据
                        if len(list(two_id)) >= 1  and list(two_id) not in buygift_two_id:
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
        # 游标加1
        index_cursor += 1

        # 将当前下标与这次循环下标交换
        if len(unify_buygift_list) > 1:
            if index_cursor != len(unify_buygift_list):
                unify_buygift_list[0], unify_buygift_list[index_cursor] = unify_buygift_list[index_cursor], \
                                                                          unify_buygift_list[0]


        productlists = copy.deepcopy(product_object_list)
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
    n_productlists=[]
    if productListMAX:
        n_productlists = basics_bg.get_optimalgroupdis(productListMAX)
        buygift_two_id = []
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
def unify_buygift(productList, bean, userInfo,org_productlists):
    # 判断当前活动是否限制会员并且当前用户可否参与
    if bean.members_only:
        if userInfo is not None:
            # 当前用户会员级别不再此活动会员级别范围之内
            if userInfo.id not in bean.members_group:
                return None
        else:
            return None



    # 取出当前活动赠送品

    # qtty:数量
    promotion_qtty_sum = 0

    # amt_list:吊牌金额
    promotion_amt_list_sum = 0

    # amt_retail:零售金额
    promotion_amt_retail_sum = 0

    # amt_receivable:应收金额是否满足
    promotion_amt_receivable_sum = 0

    #没有排除占位信息统计值
    org_promotion_qtty_sum = 0
    org_promotion_amt_list_sum = 0
    org_promotion_amt_retail_sum = 0
    org_promotion_amt_receivable_sum = 0

    # 不可以参加当前活动的ecode 全场要用
    not_product_ListA = []

    # 即在条件商品又在赠送商品列表里的商品集合（只存款号，为之后占位方便），在条件占位时优先占用只是条件商品
    give_product = []

    condition_product=[] #记录条件商品（只存款号）



    # 所有ecode相同对象
    productListA = []


    response = None

    # 遍历每一件商品合并encode相同的商品
    for ecode in bean.product_list:
        for product in productList:
            if ecode.lower() == product.ecode.lower():
                productListA.append(product)
                condition_product.append(ecode)


    # 交集的商品（即在条件商品列表里又在赠品商品列表里）
    for ecode in bean.buygift_product:
        for product in productList:
            if product.ecode.lower() == ecode["ecode"].lower():
                if product.ecode in condition_product:
                    give_product.append(product.ecode)

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
        org_infos={"org_promotion_qtty_sum":org_promotion_qtty_sum,"org_promotion_amt_list_sum":org_promotion_amt_list_sum,"org_promotion_amt_retail_sum":org_promotion_amt_retail_sum,"org_promotion_amt_receivable_sum":org_promotion_amt_receivable_sum}

        if bean.comp_symb_type == "g":
            bean.value_num += 1
        # 为了梯度用同一个函数
        response = basics_bg.not_buy_a_give_a_unify(bean, userInfo, productList,promotion_qtty_sum,
                                                    promotion_amt_list_sum, promotion_amt_retail_sum,
                                                    promotion_amt_receivable_sum,org_infos,org_productlists,give_product)
        if bean.comp_symb_type == "g":
            bean.value_num -= 1
    if type(response) == dict:
        return response
    elif response == 1:
        return 1
    else:
        return None



    if type(response) == str or response == None:
        return None
    return response
