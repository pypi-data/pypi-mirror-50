"""
    特价商品择优计算
    2018/11/14
    by李博文
"""


def current_zeyou(productList_zeyou):


    """
    取所有应收价最低的
    :param productList:
    :return:
    """

    for productList in productList_zeyou:
        pro_sum = 0
        for product in productList:
            for set in product.productSeatList:

                pro_sum += set.amt_receivable
                product.amt_receivable_sum = pro_sum
    return min(productList_zeyou, key=lambda i: i[-1].amt_receivable_sum)
