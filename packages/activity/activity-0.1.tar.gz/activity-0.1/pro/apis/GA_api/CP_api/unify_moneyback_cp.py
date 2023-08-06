#!/usr/bin/env python
"""
   统一优惠换购
   encoding: utf-8
   2018/12/26 3:53 PM
   
  
   by李博文
"""

from pro.apis.GA_api.CP_api.basics_cp import cp_basic


def unify_moneyback_cp(product_List, cp, userInfo, productList_cp, kaiguan):
    """

    :param product_List:
    :param cp:
    :param userInfo:
    :param productList_cp:
    :return:
    """
    if kaiguan == True:
        return un_mb_cp(productList_cp, cp, userInfo, kaiguan)
    return un_mb_cp(product_List, cp, userInfo, kaiguan)


def un_mb_cp(productList, bean, userInfo, kaiguan):
    """

   :param productList: 所有商品
   :param bean: 活动
   :param userInfo: 会员
   :param kaiguan: 控制所有可以参加活动的id
   :return:
   """
    if bean.members_only:
        if userInfo is not None:
            # 当前用户会员级别不再此活动会员级别范围之内
            if userInfo.id not in bean.members_group:
                if kaiguan != False:
                    return
                return {"product": productList,
                        "buygift": [],
                        "buygift_two_id": [],
                        "product_cp": []}


        else:
            if kaiguan != False:
                return
                # 当前活动限制会员参加 且 当前用户不是会员
            return {"product": productList,
                    "buygift": [],
                    "buygift_two_id": [],
                    "product_cp": []}

    # 定义可以参与活动的列表
    productListA = []

    for ecode in bean.product_list:
        for product in productList:
            if ecode.lower() == product.ecode.lower():
                productListA.append(product)

    productListA = sorted(productListA, key=lambda x: x.amt_receivable, reverse=True)

    response = cp_basic(bean, userInfo, productListA, productList, kaiguan)
    if bean.comp_symb_type.lower() == "g":
        bean.value_num -= 1
    if kaiguan != False:
        return response

    if response == None:
        return {"product": productList,
                "buygift": [],
                "product_cp": []}
    buygift, product_cp = response
    return {"product": productList,
            "buygift": buygift,
            "product_cp": product_cp}
