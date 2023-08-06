# -*- coding:utf-8 -*-
"""
    特价二类下所有活动进行择优运算
    2018/11/13
    by李博文
    edit by hexiaoxia 2019/04/15
    修改项：
    1.重组促销执行代码逻辑；
    2.添加“组合特价”活动
"""
import copy

from pro.utils.pro_exception import ProException
from pro.apis.GA_api.SO_api.gradient_special_price import preferential_gr
from pro.apis.GA_api.SO_api.unify_special_price import preferential_un
from pro.apis.GA_api.SO_api.combination_special_price import preferential_cb
from pro.apis.GA_api.SO_api.current_zeyou import current_zeyou
from pro.apis.GA_utils import recovery_seat
from pro.apis.GA_utils import checkisnoseatpro

def get_special_price(product_object_list, promotion_objec_list, user_object, productList_cp):


    # 梯度特价模板列表
    gradient_special_price = []

    # 统一特价模板列表
    unify_bpecial_price = []

    # 组合特价模板列表
    combination_special_price = []

    # 特价活动总列表
    promotion_sum = []

    for i in promotion_objec_list:

        # 统一特价模板列表
        if i.prom_type_three.lower() == "ga1301":
            unify_bpecial_price.append(i)

        # 梯度特价模板列表
        elif i.prom_type_three.lower() == "ga1302":
            gradient_special_price.append(i)

        # 组合特价模板列表
        elif i.prom_type_three.lower() == "ga1303":
            combination_special_price.append(i)
        else:
            raise ProException("三类id出错")

    if unify_bpecial_price:
        promotion_sum.append(unify_bpecial_price)
    if gradient_special_price:
        promotion_sum.append(gradient_special_price)
    if combination_special_price:
        promotion_sum.append(combination_special_price)

    #恢复商品占位
    recovery_seat(product_object_list)

    #新执行方式--edit by hexiaoxia 2019/04/15
    product_un = None
    product_gr = None
    product_all = []
    for index1,promotion in enumerate(promotion_sum):
        product_un = None
        productlistdis=copy.deepcopy(product_object_list)
        #统一特价
        if promotion[0].prom_type_three=="ga1301":
            product_un = preferential_un(productlistdis, unify_bpecial_price, user_object,productList_cp)

        #梯度特价
        elif promotion[0].prom_type_three=="ga1302":
            product_un = preferential_gr(productlistdis, gradient_special_price, user_object, productList_cp)

        #组合特价
        elif promotion[0].prom_type_three == "ga1303":
            product_un = preferential_cb(productlistdis, combination_special_price, user_object)

        if not checkisnoseatpro(product_un):
            product_all.append(product_un)
            continue

        for index2,promotion2 in enumerate(promotion_sum):
            if index1==index2:
                continue
            # 统一特价
            if promotion2[0].prom_type_three == "ga1301":
                product_un = preferential_un(product_un, unify_bpecial_price, user_object,productList_cp)

            # 梯度特价
            elif promotion2[0].prom_type_three == "ga1302":
                product_un = preferential_gr(product_un, gradient_special_price,user_object, productList_cp)

            # 组合特价
            elif promotion2[0].prom_type_three == "ga1303":
                product_un = preferential_cb(product_un, combination_special_price, user_object)


            if not checkisnoseatpro(product_un):
                product_all.append(product_un)
                continue

        product_all.append(product_un)

    # 最后进入择优
    return current_zeyou(product_all)

    #end 新执行方式





    # #老的执行方法
    # product_gr = None
    # product_un = None
    # # 如果梯度特价不为空
    #
    # recovery_seat(product_object_list)
    #
    # # 如果两者都不为空
    # if len(gradient_special_price) > 0 and len(unify_bpecial_price) > 0:
    #     product_all = []
    #
    #
    #     # 在进入统一特价
    #     product_un = preferential_un(copy.deepcopy(product_object_list), unify_bpecial_price, user_object, productList_cp)
    #     # 先进入梯度特价
    #     product_gr = preferential_gr(product_un, gradient_special_price, user_object, productList_cp)
    #     # 这是顺序统一梯度
    #     product_all.append(product_gr)
    #
    #
    #     # 现在执行梯度统一
    #     product_tidu = preferential_gr(copy.deepcopy(product_object_list), gradient_special_price, user_object, productList_cp)
    #     product_tongyi = preferential_un(product_tidu, unify_bpecial_price, user_object, productList_cp)
    #
    #     product_all.append(product_tongyi)
    #     # 最后进入择优
    #     return current_zeyou(product_all)
    #
    #
    #
    #
    # # 进入梯度特价
    # if len(gradient_special_price) > 0:
    #     return preferential_gr(copy.deepcopy(product_object_list), gradient_special_price, user_object, productList_cp)
    #
    # # 进入统一特价
    # if len(unify_bpecial_price) > 0:
    #     return preferential_un(copy.deepcopy(product_object_list), unify_bpecial_price, user_object, productList_cp)

