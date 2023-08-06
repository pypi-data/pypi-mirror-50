#!/usr/bin/env python
"""
    满减入口函数
   encoding: utf-8
   2018/12/18 2:04 PM
   
  
   by李博文
"""
import copy


from pro.utils.pro_exception import ProException
from pro.apis.GA_utils import recovery_seat
from pro.apis.GA_api.FS_api.unify_moneyback import preferential_un
from pro.apis.GA_api.FS_api.gradient_moneyback import preferential_gr
from pro.apis.GA_api.FS_api.combination_moneyback import preferential_com
from pro.apis.GA_api.PE_api.current_zeyou import result_data
from pro.apis.GA_api.SO_api.current_zeyou import current_zeyou
from pro.apis.GA_utils import checkisnoseatpro

def get_moenyback(product_object_list, promotion_objec_list, user_object, productList_cp):
    """

    :param product_object_list: 商品对象集合
    :param promotion_objec_list: 活动对象集合
    :param user_object: 会员对象集合
    :return:
    """

    # 先将所有商品站位复原
    product_object_list = recovery_seat(product_object_list)
    # 梯度满减模板列表
    gradient_moenyback = []

    # 统一满减模板列表
    unify_moenyback = []

    # 组合满减模板列表
    combination_moneyback = []

    for i in promotion_objec_list:

        # 统一满减模板列表
        if i.prom_type_three.lower() == "ga1201":
            unify_moenyback.append(i)

        # 梯度满减模板列表
        elif i.prom_type_three.lower() == "ga1202":
            gradient_moenyback.append(i)

        # 组合满减列表
        elif i.prom_type_three.lower() == "ga1203":
            combination_moneyback.append(i)
        else:
            raise ProException("三类id出错")

    moneyback_list = []  # 满减活动列表
    if unify_moenyback:
        moneyback_list.append(unify_moenyback)
    if gradient_moenyback:
        moneyback_list.append(gradient_moenyback)
    if combination_moneyback:
        moneyback_list.append(combination_moneyback)


    product_gr = None
    product_un = None
    # 如果梯度特价不为空

    recovery_seat(product_object_list)  # 恢复商品占位信息
    product_list = copy.deepcopy(product_object_list)
    productListMAX = []  # 择优列表
    index_cursor = 0
    # 循环计算满减活动
    for index1 in range(0, max((len(moneyback_list) * (len(moneyback_list)-1)), 1)):
        for promotion in moneyback_list:
            # 统一满减
            if promotion[0].prom_type_three == "ga1201":
                product_list = preferential_un(product_list, promotion, user_object, productList_cp)
            # 梯度满减
            elif promotion[0].prom_type_three == "ga1202":
                product_list = preferential_gr(product_list, promotion, user_object, productList_cp)
            # 组合满减
            elif promotion[0].prom_type_three == "ga1203":
                product_list = preferential_com(product_list, promotion, user_object)
            # 判断还有没有未占位的商品，如果没有未占位的商品，直接结束本次循环。
            if not checkisnoseatpro(product_list):
                continue
        productListMAX.append(product_list)
        # 游标加1
        index_cursor += 1

        # 将当前下标与这次循环下标交换
        if len(moneyback_list) > 1:
            if index_cursor >= len(moneyback_list):
                index_cursor = 1
            moneyback_list[0], moneyback_list[index_cursor] = moneyback_list[index_cursor], \
                                                                          moneyback_list[0]
        product_list = copy.deepcopy(product_object_list)
    response = current_zeyou(productListMAX)
    return response
    # 原来的方法，现在不使用
    # # 如果两者都不为空
    # if len(gradient_moenyback) > 0 and len(unify_moenyback) > 0:
    #     product_all = []
    #
    #
    #     # 在进入统一满减
    #     product_un = preferential_un(copy.deepcopy(product_object_list), unify_moenyback, user_object, productList_cp)
    #     # 先进入梯度满减
    #     product_gr = preferential_gr(product_un, gradient_moenyback, user_object, productList_cp)
    #     # 这是顺序统一梯度
    #     product_all.append(product_gr)
    #
    #
    #     # 现在执行梯度统一
    #     product_tidu = preferential_gr(copy.deepcopy(product_object_list), gradient_moenyback, user_object, productList_cp)
    #     product_tongyi = preferential_un(product_tidu, unify_moenyback, user_object, productList_cp)
    #
    #     product_all.append(product_tongyi)
    #
    #     response = current_zeyou(product_all)
    #     response = result_data(response, product_all)
    #     return response





    # # 进入梯度特价
    # if len(gradient_moenyback) > 0:
    #     return preferential_gr(copy.deepcopy(product_object_list), gradient_moenyback, user_object, productList_cp)
    #
    # # 进入统一特价
    # if len(unify_moenyback) > 0:
    #     return preferential_un(copy.deepcopy(product_object_list), unify_moenyback, user_object, productList_cp)
    #
    # if len(combination_moneyback) > 0:
    #     return preferential_com(copy.deepcopy(product_object_list), combination_moneyback, user_object, productList_cp)