# -*- coding:utf-8 -*-
"""
    组合买赠
    2019/04/26
    add by hexiaoxia
"""

import copy

from pro.apis.GA_api.BG_api import basics_bg
from pro.apis.GA_api.BG_api.current_promotions_preferential import current_promitions_id
from pro.apis.GA_api.BG_api.buy_a_for_value import fuwei,tongji
from pro.apis.GA_utils import recovery_seat

# 组合买赠入口
def preferential_cb(product_object_list, combination_buygift_list, userInfo, productList_CP):
    productListMAX = []
    give_id = []

    # 暂时记录 id
    two_id = set()

    # 最终返回的成双id
    buygift_two_id = []
    buygift = []
    buygift_list = []

    productlists = copy.deepcopy(product_object_list)
    can_part_promotion_id = []  # 可以参与的活动ID
    # 记录一轮循环里第一次出现使用原始数据执行促销的上个促销的索引及执行后的商品结构
    isallpro_upproductlists = []
    isallpro_upindex = -1

    index_cursor = 0
    for index in range(0, len(combination_buygift_list)):

        for bean in combination_buygift_list:

            if isallpro_upindex==-1:
                isallpro_upproductlists=copy.deepcopy(productlists)

            # 返回每个方案计算后的商品集合
            list1 = combination_buygift(productlists, bean, userInfo, copy.deepcopy(productList_CP))

            list1 = unify_buygift(productlists, bean, userInfo, copy.deepcopy(productList_CP))
            if list1:
                can_part_promotion_id.append(bean.id)
            if list1 and type(list1) == dict:
                if list1["buygift"]:
                    if list1["dis_id"] not in give_id:
                        give_id.append(list1["dis_id"])
                        buygift_list.append(list1["buygift"])
                    if list1["isallpro"]:
                        # 记录前面执行的组的数据
                        if len(list(two_id)) >= 1 and list(two_id) not in buygift_two_id:
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
        if len(combination_buygift_list) > 1:
            if index_cursor != len(combination_buygift_list):
                combination_buygift_list[0], combination_buygift_list[index_cursor] = combination_buygift_list[index_cursor], \
                                                                                      combination_buygift_list[0]



        productlists = copy.deepcopy(product_object_list)
        isallpro_upproductlists = []
        isallpro_upindex = -1

        # 将第一轮里可以在一组同时执行的同三类买赠活动筛选组织成需要的结构
        if len(list(two_id)) >= 1 and list(two_id) not in buygift_two_id:
            buygift_two_id.append(list(two_id))
        if buygift:
            productListMAX.append(buygift)
        two_id = set()
        buygift = []

    # 从所有执行的顺序中取出最优的一组
    n_productlists = []
    if productListMAX:
        n_productlists=basics_bg.get_optimalgroupdis(productListMAX)
        buygift_two_id=[]
        for row in n_productlists:
            two_id.add(row["dis_id"])

        buygift_two_id.append(list(two_id))

        productlists=n_productlists[-1]["product"]


    response = {
        "n_productlists":n_productlists, #最优组促销执行情况，供后面再择优使用
        "product": productlists,
        "buygift": buygift_list if len(buygift_list) >= 1 else [],
        "buygift_two_id": buygift_two_id if len(buygift_two_id) >= 1 else [],
        "can_part_promotion_id": can_part_promotion_id
    }
    return response


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
        else:
            return 1


    # 即在条件商品又在赠送商品列表里的商品集合（只存款号，为之后占位方便），在条件占位时优先占用只是条件商品
    give_product = []

    # 找出赠品商品
    for ecode in bean.buygift_product:
        for product in productList:
            if product.ecode.lower() == ecode["ecode"].lower():
                if product.ecode in specific_productall:
                    give_product.append(product.ecode)
    for r_item in bean.specific_activities:
        if r_item.comp_symb_type == "g":
            r_item.value_num += 1
    response = basics_bg.combination_unify_dis(bean, productList, org_productlists,holddis,give_product)
    for r_item in bean.specific_activities:
        if r_item.comp_symb_type == "g":
            r_item.value_num -= 1
    if type(response) == dict:
        return response
    else:
        return 1



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
            return -1, []

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
    return holddis,specific_productall
