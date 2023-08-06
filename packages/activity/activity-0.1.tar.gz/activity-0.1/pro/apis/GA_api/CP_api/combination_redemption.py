
#!/usr/bin/env python
"""
   encoding: utf-8
   2019/06/28
   add by hexiaoxia
   商品换购---组合打折换购、组合特价换购、组合优惠换购 执行入口
"""
from pro.apis.GA_api.CP_api import basics_cp
from pro.apis.GA_api.BG_api.buy_a_for_value import tongji
from pro.utils.linq import linq


# 具体运算
def combination_buygift(productList, bean, userInfo,org_productlists):
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

    holddis, specific_productall=conbination_compare(bean,productList,specific_productall,0)

    if holddis==-1:
        specific_productall=[]
        #表示上面的情况不可执行，那么再使用原始数据结构判断该促销是否可执行
        holddis, specific_productall = conbination_compare(bean, productList,specific_productall, 1)

        if holddis==-1:
            return None
        return 1

    # 即在条件商品又在换购商品列表里的商品集合（只存款号，为之后占位方便），在条件占位时优先占用只是条件商品
    give_product = []

    # 交集的商品（即在条件商品列表里又在赠品商品列表里）
    for row in bean.operation_set:
        for product in productList:
            rowecode = linq(row.product_list).where(lambda x: x["ecode"].lower() == product.ecode.lower()).tolist()
            if rowecode:
                if product.ecode in specific_productall:
                    give_product.append(product.ecode)

    for r_item in bean.specific_activities:
        if r_item.comp_symb_type == "g":
            r_item.value_num += 1

    response = basics_cp.combination_unify_dis(bean, productList, org_productlists, holddis, give_product)
    for r_item in bean.specific_activities:
        if r_item.comp_symb_type == "g":
            r_item.value_num -= 1

    if type(response) == dict:
        return response
    elif response == 1:
        return 1
    else:
        return None


def conbination_compare(bean,productList,specific_productall,intype):
    '''
    检测该促销活动是否满足执行条件
    :param bean:
    :param productList:
    :param specific_productall:
    :param intype:
    :return:
    '''
    for r_item in bean.specific_activities:
        holddis=-1
        # qtty:数量
        promotion_qtty_sum = 0

        # 原始商品总数量
        org_promotion_qtty_sum = 0

        specific_product = []

        # 遍历每一件商品合并encode相同的商品
        for ecode in r_item.product_list:
            for product in productList:
                if ecode.lower() == product.ecode.lower():
                    specific_productall.append(ecode)
                    specific_product.append(product)
        if not specific_product:
            return holddis,[]

        promotion_qtty_sum, promotion_amt_list_sum, promotion_amt_retail_sum, promotion_amt_receivable_sum, org_promotion_qtty_sum, org_promotion_amt_list_sum, org_promotion_amt_retail_sum, org_promotion_amt_receivable_sum = tongji(specific_product)

        # 如果总数不满足条件那么返回
        value_num = r_item.value_num
        if r_item.comp_symb_type == "g":
            value_num += 1

        if intype == 0:
            if r_item.target_type == "qtty":
                if promotion_qtty_sum >= value_num:
                    holddis = 0
                else:
                    break
            elif r_item.target_type == "amt_list":
                if promotion_amt_list_sum >= value_num:
                    holddis = 0
                else:
                    break
            elif r_item.target_type == "amt_retail":
                if promotion_amt_retail_sum >= value_num:
                    holddis = 0
                else:
                    break
            elif r_item.target_type == "amt_receivable":
                if promotion_amt_receivable_sum >= value_num:
                    holddis = 0
                else:
                    break

        else:
            if r_item.target_type == "qtty":
                if org_promotion_qtty_sum >= value_num:
                    holddis = 1
                else:
                    break
            elif r_item.target_type == "amt_list":
                if org_promotion_amt_list_sum >= value_num:
                    holddis = 1
                else:
                    break
            elif r_item.target_type == "amt_retail":
                if org_promotion_amt_retail_sum >= value_num:
                    holddis = 1
                else:
                    break
            elif r_item.target_type == "amt_receivable":
                if org_promotion_amt_receivable_sum >= value_num:
                    holddis = 1
                else:
                    break

        specific_productall = list(set(specific_productall))

    return holddis, specific_productall


