# -*- coding:utf-8 -*-
# author:weiyanping
# datetime:2019/7/11 11:00
# software: PyCharm

from pro.apis.GA_api.BG_api import basics_bg
from pro.apis.GA_api.BG_api.buy_a_for_value import tongji


def combination_buygift_online(productList, bean, userInfo, org_productlists):
    # 判断当前活动是否限制会员并且当前用户可否参与
    if bean.members_only:
        if userInfo is not None:
            # 当前用户会员级别不再此活动会员级别范围之内
            if userInfo.id not in bean.members_group:
                return None
        else:
            return None

    specific_productall = []
    holddis = -1
    holddis, specific_productall, max_double_times = conbination_compare_online(bean, productList,
                                                                                specific_productall, 0)

    if holddis == -1:
        specific_productall = []
        # 表示上面的情况不可执行，那么再使用原始数据结构判断该促销是否可执行
        holddis, specific_productall, max_double_times = conbination_compare_online(bean, productList, specific_productall, 1)
        if holddis == -1:
            return None
        else:
            return 1

    response = basics_bg.combination_unify_dis_online(bean, productList, org_productlists, holddis,
                                                      max_double_times)

    if type(response) == dict:
        return response
    else:
        return None


def conbination_compare_online(bean,productList,specific_productall,intype):
    '''
    检测该促销活动是否满足执行条件
    :param bean: 活动
    :param productList: 商品
    :param specific_productall: 可以参加活动的商品款号
    :param intype: 比较类型，0为参加过其他活动的商品，1为原始商品
    :return:
    '''
    max_double_times = 0
    for r_item in bean.specific_activities:
        holddis = -1
        # qtty:数量
        promotion_qtty_sum = 0

        # 原始商品总数量
        org_promotion_qtty_sum = 0

        specific_product = []

        # 遍历每一件商品合并encode相同的商品
        for ecode in r_item.product_list:
            for product in productList:
                if ecode in [product.ecode, product.sku]:
                    specific_productall.append(ecode)
                    specific_product.append(product)
        if not specific_product:
            # 如果没有符合条件的商品，则返回
            return -1, [], 0

        promotion_qtty_sum, promotion_amt_list_sum, promotion_amt_retail_sum, promotion_amt_receivable_sum, \
        org_promotion_qtty_sum, org_promotion_amt_list_sum, org_promotion_amt_retail_sum, org_promotion_amt_receivable_sum = \
            tongji(specific_product)

        # 如果比较条件为大于， 则+ 1
        value_num = r_item.value_num
        if r_item.comp_symb_type == "g":
            value_num += 1

        current_times = 0
        if intype == 0:
            if r_item.target_type == "qtty":
                current_times = int(promotion_qtty_sum / value_num)
            elif r_item.target_type == "amt_list":
                current_times = int(promotion_amt_list_sum / value_num)
            elif r_item.target_type == "amt_retail":
                current_times = int(promotion_amt_retail_sum / value_num)
            elif r_item.target_type == "amt_receivable":
                current_times = int(promotion_amt_receivable_sum / value_num)
        else:
            if r_item.target_type == "qtty":
                current_times = int(org_promotion_qtty_sum / value_num)
            elif r_item.target_type == "amt_list":
                current_times = int(org_promotion_amt_list_sum / value_num)
            elif r_item.target_type == "amt_retail":
                current_times = int(org_promotion_amt_retail_sum / value_num)
            elif r_item.target_type == "amt_receivable":
                current_times = int(org_promotion_amt_receivable_sum / value_num)
        if current_times <= 0:
            # 如果有不满足条件的行， 直接返回
            return -1, [], 0
        if current_times > 0:
            if max_double_times == 0:
                max_double_times = current_times
            else:
                max_double_times = current_times if current_times < max_double_times else max_double_times
            holddis = intype
        specific_productall = list(set(specific_productall))

    return holddis, specific_productall, max_double_times