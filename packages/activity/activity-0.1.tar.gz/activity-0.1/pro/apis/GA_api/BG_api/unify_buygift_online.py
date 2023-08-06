# -*- coding:utf-8 -*-
# author:weiyanping
# datetime:2019/7/10 09:40
# software: PyCharm

import copy

from pro.apis.GA_api.BG_api import basics_bg
from pro.apis.GA_api.BG_api.buy_a_for_value import tongji
from pro.utils.util import Keeptwodecplaces


def unify_buygift_online(productList, bean, userInfo, org_productlists):
    """
    线上统一买赠计算
    :param productList:
    :param bean:
    :param userInfo:
    :param org_productlists:
    :return:
    """
    # 判断当前活动是否限制会员并且当前用户可否参与
    if bean.members_only:
        if userInfo is not None:
            # 当前用户会员级别不再此活动会员级别范围之内
            if userInfo.id not in bean.members_group:
                return None
        else:
            return None

    # qtty:数量
    promotion_qtty_sum = 0

    # amt_list:吊牌金额
    promotion_amt_list_sum = 0

    # amt_retail:零售金额
    promotion_amt_retail_sum = 0

    # amt_receivable:应收金额是否满足
    promotion_amt_receivable_sum = 0

    # 没有排除占位信息统计值
    org_promotion_qtty_sum = 0
    org_promotion_amt_list_sum = 0
    org_promotion_amt_retail_sum = 0
    org_promotion_amt_receivable_sum = 0

    condition_product = []  # 记录条件商品（只存款号）

    # 所有ecode相同对象
    productListA = []

    response = None

    # 遍历每一件商品, 合并encode相同的商品
    for ecode in bean.product_list:
        for product in productList:
            if ecode.lower() in [product.ecode.lower(), product.sku.lower()]:
                productListA.append(product)
                condition_product.append(ecode)

    # 循环添加各种满足条件
    if len(productListA) > 0:

        promotion_qtty_sum, promotion_amt_list_sum, promotion_amt_retail_sum, promotion_amt_receivable_sum, org_promotion_qtty_sum, org_promotion_amt_list_sum, org_promotion_amt_retail_sum, org_promotion_amt_receivable_sum = tongji(productListA)

        # 保留两位小数点
        promotion_amt_list_sum = float(Keeptwodecplaces(promotion_amt_list_sum))
        promotion_amt_retail_sum = float(Keeptwodecplaces(promotion_amt_retail_sum))
        promotion_amt_receivable_sum = float(Keeptwodecplaces(promotion_amt_receivable_sum))
        org_promotion_amt_list_sum = float(Keeptwodecplaces(org_promotion_amt_list_sum))
        org_promotion_amt_retail_sum = float(Keeptwodecplaces(org_promotion_amt_retail_sum))
        org_promotion_amt_receivable_sum = float(Keeptwodecplaces(org_promotion_amt_receivable_sum))
        org_infos = {"org_promotion_qtty_sum": org_promotion_qtty_sum,
                     "org_promotion_amt_list_sum": org_promotion_amt_list_sum,
                     "org_promotion_amt_retail_sum": org_promotion_amt_retail_sum,
                     "org_promotion_amt_receivable_sum": org_promotion_amt_receivable_sum}

        # 如果比较符为大于的话，则将比较值加1
        if bean.comp_symb_type == "g":
            bean.value_num += 1

        # 为了梯度用同一个函数
        response = basics_bg.not_buy_a_give_a_unify_online(bean, userInfo, productList, promotion_qtty_sum,
                                                           promotion_amt_list_sum, promotion_amt_retail_sum,
                                                           promotion_amt_receivable_sum, org_infos,
                                                           org_productlists)
        # 如果比较符为大于的话，使用过后将比较值-1
        if bean.comp_symb_type == "g":
            bean.value_num -= 1

    if type(response) == dict:
        return response
    elif response == 1:
        return 1
    else:
        return None
