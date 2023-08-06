"""
    统一买免
    2018/11/15
    by李博文
"""
import copy


def current_zeyou(productList_zeyou):
    """
    判断应收价为0的商品数量
    :param productList:
    :return:
    """
    for productList in productList_zeyou:

        for product in productList:
            pro_sum = 0
            product.amt_receivable_sum = 0
            for set in product.productSeatList:
                if set.amt_receivable == 0:
                    pro_sum += set.discountPrice[-1]
                    product.amt_receivable_sum = pro_sum
    return max(productList_zeyou, key=lambda i: i[-1].amt_receivable_sum)


def result_data(productList, productListMAX):
    """
    整合数据 要达到所有可以参与活动的id
    :param productList: 择优完的最优数据
    :param productListMAX: 所有参加活动商品
    :return:
    """

    # 存放数据的列表
    current_list = []

    cur_set = set()

    productListMAX.insert(0, productList)
    # 第一组数据
    product_1 = productListMAX[0]

    # 遍历第二组数据将其取出
    for number_2 in productListMAX:

        if not current_list:
            for not_product in number_2:
                for i in not_product.discountId:
                    cur_set.add(i)
                current_list.append(cur_set)

        else:

            cursor_id = 0
            for product in number_2:
                for i in product.discountId:
                    current_list[cursor_id].add(i)
                cursor_id += 1

            cursor_id = 0


    # 定义第二个游标
    cursor_id_2 = 0
    # 拼接数据

    for product in product_1:
        for i in current_list[cursor_id_2]:
            product.discountId.add(i)
        cursor_id_2 += 1



    return product_1
