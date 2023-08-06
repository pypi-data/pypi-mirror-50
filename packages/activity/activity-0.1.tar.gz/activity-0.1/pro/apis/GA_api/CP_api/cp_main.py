#!/usr/bin/env python
"""
    换购主入口
   encoding: utf-8
   2018/12/26 2:43 PM
   by李博文

   edit by hexiaoxia
   2019-06-28
   执行方式重新
"""

from pro.utils.pro_exception import ProException
from pro.apis.GA_utils import recovery_seat
from pro.apis.GA_api.CP_api import basics_cp
from pro.apis.GA_api.CP_api import unify_redemption
from pro.apis.GA_api.CP_api import combination_redemption

import copy


def get_cp(product_List, cp, userInfo, productList_cp):
    """

    :param product_List:
    :param buy_giftList:
    :param userInfo:
    :param productList_cp:
    :return:
    """
    kaiguan = False
    give_id = []
    buygift_two_id = []
    productcp = []
    buygift_two_id = []
    two_id = set()
    # 先将所有商品站位复原
    product_object_list = recovery_seat(product_List)

    # 排序
    cp = sorted(cp, key=lambda x: x.publish_date, reverse=True)

    # 1循环活动总长度
    # 2循环进入每一个活动
    # 3做到 54321 45321这种遍历
    give_id = []

    productListMAX = []

    # 暂时记录 id
    two_id = set()

    # 最终返回的成双id
    buygift_two_id = []
    buygift = []
    buygift_list = []
    can_part_promotion_id = []  # 满足条件的促销活动ID
    product_cp=[]

    productlists = copy.deepcopy(product_object_list)

    # 记录一轮循环里第一次出现使用原始数据执行促销的上个促销的索引及执行后的商品结构
    isallpro_upproductlists = []
    isallpro_upindex = -1

    index_cursor = 0
    for index in range(0, len(cp)):

        for bean in cp:

            if bean.prom_type_three.lower() == "ga1501" or bean.prom_type_three.lower() == "ga1503" or bean.prom_type_three.lower() == "ga1505":
                if len(bean.product_list) < 1:
                    continue

            if isallpro_upindex == -1:
                isallpro_upproductlists = copy.deepcopy(productlists)

            # 返回每个方案计算后的商品集合
            if bean.prom_type_three.lower() == "ga1501" or bean.prom_type_three.lower() == "ga1503" or bean.prom_type_three.lower() == "ga1505":
                #统一特价换购、统一打折换购、统一优惠换购
                list1 = unify_redemption.unify_buygift(productlists, bean, userInfo, copy.deepcopy(product_object_list))
            elif bean.prom_type_three.lower() == "ga1502" or bean.prom_type_three.lower() == "ga1504" or bean.prom_type_three.lower() == "ga1506":
                #组合特价换购、组合打折换购、组合优惠换购
                list1 = combination_redemption.combination_buygift(productlists, bean, userInfo, copy.deepcopy(product_object_list))
            else:
                ProException("三类id有错")
            if list1:
                can_part_promotion_id.append(bean.id)
            if list1 and type(list1) == dict:
                if list1["buygift"]:
                    if list1["product_cp"]:
                        for row_1 in list1["product_cp"]:
                            product_cp.append(row_1)
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

                        if isallpro_upindex == -1:
                            isallpro_upindex = len(buygift_two_id) - 1

                        if isallpro_upindex > -1:
                            productlists = copy.deepcopy(isallpro_upproductlists)

                        # buygift.append(list1)
                        # productListMAX.append(buygift)
                        two_id = set()
                        buygift = []
                    else:
                        if isallpro_upindex == -1:
                            two_id.add(bean.id)
                            buygift.append(list1)
                        else:
                            set(buygift_two_id[isallpro_upindex]).add(bean.id)
                            productListMAX[isallpro_upindex].append(list1)

                    isallpro_upproductlists = copy.deepcopy(productlists)

                productlists = list1["product"]

        # 游标加1
        index_cursor += 1

        # 将当前下标与这次循环下标交换
        if len(cp) > 1:
            if index_cursor != len(cp):
                cp[0], cp[index_cursor] = cp[index_cursor], \
                                          cp[0]

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
        n_productlists = basics_cp.get_optimalgroupdis(productListMAX)
        buygift_two_id = []
        for row in n_productlists:
            two_id.add(row["dis_id"])

        buygift_two_id.append(list(two_id))

        productlists = n_productlists[-1]["product"]

    response = {
        "product": productlists,
        "buygift": buygift_list if len(buygift_list) >= 1 else [],
        "buygift_two_id": buygift_two_id if len(buygift_two_id) >= 1 else [],
        "product_cp":product_cp,
        "can_part_promotion_id": can_part_promotion_id
    }
    return response

