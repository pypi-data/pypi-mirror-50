# -*- coding:utf-8 -*-
"""
    折扣二类下所有活动进行择优运算
    2018/10/24
    by李博文
    edit by hexiaoxia 2019/04/26
    修改项：
    1.重组促销执行代码逻辑；
    2.添加“组合买赠”活动
"""
import copy

from pro.apis.GA_api.BG_api import unify_buygift, gradient_buygift,combination_buygift,unify_buygift_online, gradient_buygift_online,combination_buygift_online
from pro.apis.GA_utils import recovery_seat
from pro.apis.GA_api.BG_api import basics_bg


def get_BuyGift(product_object_list, promotion_objec_list, user_object, product_Original):

    # 先将所有商品站位复原
    product_object_list = recovery_seat(product_object_list)


    # 梯度买赠模板列表
    gradient_buygift_list = []

    # 统一买赠模板列表
    unify_buygift_list = []

    #组合买赠模板列表
    combination_buygift_list=[]

    # 排序
    promotion_objec_list = sorted(promotion_objec_list, key=lambda x: x.publish_date, reverse=True)

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
    can_part_promotion_id = []
    productlists = copy.deepcopy(product_object_list)

    # 记录一轮循环里第一次出现使用原始数据执行促销的上个促销的索引及执行后的商品结构
    isallpro_upproductlists = []
    isallpro_upindex = -1

    index_cursor = 0
    for index in range(0, len(promotion_objec_list)):

        for bean in promotion_objec_list:
            if bean.prom_type_three.lower() != "ga1405" and bean.prom_type_three.lower() != "ga1703" and bean.prom_type_three.lower() != "ga1803":
                if len(bean.product_list) < 1:
                    continue

            if isallpro_upindex == -1:
                isallpro_upproductlists = copy.deepcopy(productlists)

            # 统一买赠
            if bean.prom_type_three.lower() == "ga1401":
                list1 = unify_buygift.unify_buygift(productlists, bean, user_object, product_Original)

            # 梯度买赠
            elif bean.prom_type_three.lower() == "ga1402":
                list1 = gradient_buygift.gradient_buygift(productlists, bean, user_object,product_Original)

            # 组合买赠
            elif bean.prom_type_three.lower() == "ga1405":
                list1 = combination_buygift.combination_buygift(productlists, bean, user_object,product_Original)

            # 线上统一买赠、线上排名统一买赠
            elif bean.prom_type_three.lower() == "ga1701" or bean.prom_type_three.lower() == "ga1801":
                list1 = unify_buygift_online.unify_buygift_online(productlists, bean, user_object, product_Original)

            # 线上梯度买赠、线上排名梯度买赠
            elif bean.prom_type_three.lower() == "ga1702" or bean.prom_type_three.lower() == "ga1802":
                list1 = gradient_buygift_online.gradient_buygift_online(productlists, bean, user_object,product_Original)

            #线上组合买赠、线上排名组合买赠
            elif bean.prom_type_three.lower() == "ga1703" or bean.prom_type_three.lower() == "ga1803":
                list1 = combination_buygift_online.combination_buygift_online(productlists, bean, user_object,product_Original)
            if list1:
                can_part_promotion_id.append(bean.id)
            if list1 and type(list1) == dict:
                if list1["buygift"]:
                    if list1["dis_id"] not in give_id:
                        if bean.prom_type_three.lower() != "ga1701" and  bean.prom_type_three.lower() != "ga1801" and bean.prom_type_three.lower() != "ga1702" and bean.prom_type_three.lower() != "ga1802" and bean.prom_type_three.lower() != "ga1703" and bean.prom_type_three.lower() != "ga1803":
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
        if len(promotion_objec_list) > 1:
            if index_cursor != len(promotion_objec_list):
                promotion_objec_list[0], promotion_objec_list[index_cursor] = promotion_objec_list[index_cursor], \
                                                                              promotion_objec_list[0]

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
        n_productlists = basics_bg.get_optimalgroupdis(productListMAX)
        buygift_two_id = []
        for row in n_productlists:
            two_id.add(row["dis_id"])

        buygift_two_id.append(list(two_id))

        productlists = n_productlists[-1]["product"]

    response = {
        "product": productlists,
        "buygift": buygift_list if len(buygift_list) >= 1 else [],
        "buygift_two_id": buygift_two_id if len(buygift_two_id) >= 1 else [],
        "can_part_promotion_id": can_part_promotion_id
    }
    return response



    # for i in promotion_objec_list:
    #
    #     # 统一买赠模板列表
    #     if i.prom_type_three.lower() == "ga1401":
    #         unify_buygift_list.append(i)
    #
    #     # 梯度买赠模板列表
    #     elif i.prom_type_three.lower() == "ga1402":
    #         gradient_buygift_list.append(i)
    #
    #     #组合买赠模板列表
    #     elif i.prom_type_three.lower() == "ga1405":
    #         combination_buygift_list.append(i)
    #
    #     else:
    #         raise ProException("三类id出错")
    # unify_buygift_preferential = None
    # gradient_buygift_preferential_gd = None
    # # 按时间排序
    # gradient_buygift_list = sorted(gradient_buygift_list, key=lambda x: x.publish_date, reverse=True)
    # unify_buygift_list = sorted(unify_buygift_list, key=lambda x: x.publish_date, reverse=True)
    # combination_buygift_list = sorted(combination_buygift_list, key=lambda x: x.publish_date, reverse=True)
    #
    # sum_promotion=[]
    #
    # if unify_buygift_list:
    #     sum_promotion.append(unify_buygift_list)
    # if gradient_buygift_list:
    #     sum_promotion.append(gradient_buygift_list)
    # if combination_buygift_list:
    #     sum_promotion.append(combination_buygift_list)
    #
    #
    # r_product = copy.deepcopy(product_object_list)
    #
    # buygift_two_id = []
    # g_buygift_two_id=[]
    #
    # buygift = []
    # buygift_id=[]
    #
    # productListMAX = [] #记录三种买赠促销按照对应顺序执行后得到的最优的结果
    # product_max = [] #记录每种买赠促销执行后的结果
    #
    # #新的执行方法
    # for index1,promotion in enumerate(sum_promotion):
    #     product_max = []
    #     r_product = copy.deepcopy(product_object_list)
    #     #统一买赠
    #     if promotion[0].prom_type_three=="ga1401":
    #         list1 = unify_buygift.preferential_bg(r_product, unify_buygift_list,user_object, product_Original)
    #
    #     #梯度买赠
    #     elif promotion[0].prom_type_three=="ga1402":
    #         list1 = gradient_buygift.preferential_gd(r_product, gradient_buygift_list, user_object, product_Original)
    #
    #     #组合买赠
    #     elif promotion[0].prom_type_three == "ga1405":
    #         list1 = combination_buygift.preferential_cb(r_product, combination_buygift_list, user_object, product_Original)
    #
    #     if list1["buygift_two_id"] is not None:
    #         for i in list1["buygift_two_id"]:
    #             if len(list1["buygift"]) == 1 and list1["buygift"][0]["isallpro"] == True:
    #                 continue
    #
    #             for row_i in i:
    #                 if row_i not in buygift_two_id:
    #                     buygift_two_id.append(row_i)
    #
    #     for j in list1["buygift"]:
    #         if j["id"] not in buygift_id:
    #             buygift.append(j)
    #             buygift_id.append(j["id"])
    #
    #     # product_max.append(list1["n_productlists"])
    #
    #     if not checkisnoseatpro(list1["product"]):
    #         if list1["n_productlists"]:
    #             productListMAX.append(list1["n_productlists"])
    #         continue
    #
    #     r_product=list1["product"]
    #
    #     for index2,promotion2 in enumerate(sum_promotion):
    #         if index1==index2:
    #             continue
    #         # 统一买赠
    #         if promotion2[0].prom_type_three == "ga1401":
    #             list1 = unify_buygift.preferential_bg(r_product, unify_buygift_list,user_object, product_Original)
    #
    #         # 梯度买赠
    #         elif promotion2[0].prom_type_three == "ga1402":
    #             list1 = gradient_buygift.preferential_gd(r_product, gradient_buygift_list, user_object, product_Original)
    #
    #         # 组合买赠
    #         elif promotion2[0].prom_type_three == "ga1405":
    #             list1 = combination_buygift.preferential_cb(r_product, combination_buygift_list, user_object,
    #                                                      product_Original)
    #
    #         if list1["buygift_two_id"] is not None:
    #             for i in list1["buygift_two_id"]:
    #                 if len(list1["buygift"]) == 1 and list1["buygift"][0]["isallpro"] == True:
    #                     continue
    #
    #                 for row_i in i:
    #                     if row_i not in buygift_two_id:
    #                         buygift_two_id.append(row_i)
    #
    #         for j in list1["buygift"]:
    #             if j["id"] not in buygift_id:
    #                 buygift.append(j)
    #                 buygift_id.append(j["id"])
    #
    #         # product_max.append(list1["n_productlists"])
    #
    #         if not checkisnoseatpro(list1["product"]):
    #             # #从product_max里筛选最优的组存入productListMAX里
    #             # n_productlists = basics_bg.get_optimalgroupdis(product_max)
    #             # productListMAX.append(n_productlists)
    #             if list1["n_productlists"]:
    #                 productListMAX.append(list1["n_productlists"])
    #             continue
    #
    #         r_product = list1["product"]
    #
    #
    #     r_product = list1["product"]
    #
    #     # # 从product_max里筛选最优的组存入productListMAX里
    #     # n_productlists = basics_bg.get_optimalgroupdis(product_max)
    #     # productListMAX.append(n_productlists)
    #
    #     if list1["n_productlists"]:
    #         productListMAX.append(list1["n_productlists"])
    #
    #
    #     if buygift_two_id and len(buygift_two_id)>1 and buygift_two_id not in g_buygift_two_id:
    #         g_buygift_two_id.append(buygift_two_id)
    #
    #     buygift_two_id=[]
    #
    # n_productlists = basics_bg.get_optimalgroupdis(productListMAX)
    # r_product = n_productlists[-1]["product"]
    #
    # #返参中：
    # # buygift：当前单据中所有可执行的买赠活动；
    # # buygift_two_id：当前单据中可同组执行的买赠活动的分组列表；
    # return {
    #     "product": r_product, #current_promitions_id(product_max),
    #     "buygift": buygift if len(buygift) >= 1 else [],
    #     "buygift_two_id": g_buygift_two_id if len(g_buygift_two_id) >= 1 else []
    # }




