#!/usr/bin/env python
"""
   encoding: utf-8
   2019/06/28
   add by hexiaoxia
   商品换购---统一打折换购、统一特价换购、统一优惠换购 执行入口
"""
from pro.apis.GA_api.CP_api.basics_cp import not_buy_a_give_a_unify
from pro.utils.linq import linq
import pro.utils.util as util
from pro.apis.GA_api.BG_api.buy_a_for_value import tongji


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

    condition_product = []  # 记录条件商品（只存款号）

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
    for row in bean.operation_set:
        for product in productList:
            rowecode = linq(row.product_list).where(lambda x: x["ecode"].lower() == product.ecode.lower()).tolist()
            if rowecode:
                if product.ecode in condition_product:
                    give_product.append(product.ecode)

    # 循环添加各种满足条件
    if len(productListA) > 0:

        promotion_qtty_sum,promotion_amt_list_sum,promotion_amt_retail_sum,promotion_amt_receivable_sum,org_promotion_qtty_sum,org_promotion_amt_list_sum,org_promotion_amt_retail_sum,org_promotion_amt_receivable_sum = tongji(productListA)

        # 保留两位小数点
        promotion_amt_list_sum = float(util.Keeptwodecplaces(promotion_amt_list_sum))
        promotion_amt_retail_sum = float(util.Keeptwodecplaces(promotion_amt_retail_sum))
        promotion_amt_receivable_sum = float(util.Keeptwodecplaces(promotion_amt_receivable_sum))
        org_promotion_amt_list_sum = float(util.Keeptwodecplaces(org_promotion_amt_list_sum))
        org_promotion_amt_retail_sum = float(util.Keeptwodecplaces(org_promotion_amt_retail_sum))
        org_promotion_amt_receivable_sum = float(util.Keeptwodecplaces(org_promotion_amt_receivable_sum))
        org_infos = {"org_promotion_qtty_sum": org_promotion_qtty_sum,
                     "org_promotion_amt_list_sum": org_promotion_amt_list_sum,
                     "org_promotion_amt_retail_sum": org_promotion_amt_retail_sum,
                     "org_promotion_amt_receivable_sum": org_promotion_amt_receivable_sum}
        # 如果比较条件为大于，则比较值+1
        if bean.comp_symb_type == "g":
            bean.value_num += 1

        # 为了梯度用同一个函数
        response = not_buy_a_give_a_unify(bean, userInfo, productList, promotion_qtty_sum,
                                          promotion_amt_list_sum, promotion_amt_retail_sum,
                                          promotion_amt_receivable_sum, org_infos,
                                          org_productlists, give_product)
        # 执行完后，如果比较条件为大于，则比较值 -1
        if bean.comp_symb_type == "g":
            bean.value_num -= 1

    if type(response) == dict:
        return response
    elif response == 1:
        return 1
    else:
        return None

