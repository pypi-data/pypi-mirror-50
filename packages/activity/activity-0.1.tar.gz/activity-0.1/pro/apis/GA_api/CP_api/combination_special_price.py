
#!/usr/bin/env python
"""

   encoding: utf-8
   2018/12/26 3:30 PM
   
  
   by李博文
"""
from pro.apis.GA_api.CP_api.basics_cp import cp_basic

def combination_special_cp(product_List, cp, userInfo, productList_cp, kaiguan):
    """

    :param product_List:
    :param cp:
    :param userInfo:
    :param productList_cp:
    :return:
    """
    return com_special_cp(product_List, cp, userInfo, kaiguan)

def com_special_cp(productList, bean, userInfo, kaiguan):
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
                        "product_cp":[]}


        else:
            if kaiguan != False:
                return
                # 当前活动限制会员参加 且 当前用户不是会员
            return {"product": productList,
                    "buygift": [],
                    "buygift_two_id": [],
                    "product_cp":[]}

    # 将组合1和组合2的可以参与商品取出
    # 组合1
    productListA1 = []
    # 组合2
    productListA2 = []
    for ecode in bean.specific_activities[0].product_list:
        for product in productList:
            if ecode.lower() == product.ecode.lower():
                productListA1.append(product)

    for ecode in bean.specific_activities[1].product_list:
        for product in productList:
            if ecode.lower() == product.ecode.lower():
                productListA2.append(product)

    productListA1 = sorted(productListA1, key=lambda x: x.amt_receivable, reverse=True)
    productListA2 = sorted(productListA2, key=lambda x: x.amt_receivable, reverse=True)
    productListA = [productListA1, productListA2]

    response = cp_basic(bean, userInfo, productListA, productList, kaiguan)

    if hasattr(bean, "specific_activities"):
        # 将活动比较值恢复
        if bean.specific_activities[0].comp_symb_type.lower() == "g":
            bean.specific_activities[0].value_num -= 1
        if bean.specific_activities[1].comp_symb_type.lower() == "g":
            bean.specific_activities[1].value_num -= 1

    if kaiguan != False:
        return response

    buygift, product_cp = response

    if response == None:
        return {"product": productList,
                "buygift": [],
                "product_cp":[]}

    return {"product": productList,
            "buygift": buygift,
            "product_cp":product_cp}
