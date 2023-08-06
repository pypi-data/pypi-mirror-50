# -*- coding:utf-8 -*-
"""
    创建商品和活动模板类
    2018/10/24
    by李博文
"""

import copy

from pro.apis.entitys.products_entitys.product import Product
from pro.apis.entitys.GA_entitys.discount.unify_discount import UnifyDiscountEntity
from pro.apis.entitys.GA_entitys.discount.multiple_discounts import MultipleDiscountEntity
from pro.apis.entitys.GA_entitys.discount.Increasing_discounts import IncrementalDiscountEntity
from pro.apis.entitys.GA_entitys.discount.combination_discount import CombinationDiscountEntity
from pro.apis.entitys.GA_entitys.cp.unify_specialprice_cp import Unify_Specialprice_cp
from pro.apis.entitys.GA_entitys.buygift.gradient_buygift import Gradient_BuyGift
from pro.apis.entitys.GA_entitys.buygift.unify_buygift import Unify_BuyGift
from pro.apis.entitys.GA_entitys.buygift.combination_buygift import Combination_buygiftEntity
from pro.apis.entitys.GA_entitys.buygift.gradient_buygift_online import Gradient_BuyGift_Online
from pro.apis.entitys.GA_entitys.buygift.unify_buygift_online import Unify_BuyGift_Online
from pro.apis.entitys.GA_entitys.buygift.combination_buygift_online import Combination_buygift_Online
from pro.apis.entitys.GA_entitys.cp.unify_discount_cp import Unify_Cp
from pro.apis.entitys.GA_entitys.cp.combination_discount_cp import CombinationDiscountEntity_Cp
from pro.apis.entitys.GA_entitys.cp.combination_specialprice_cp import Combination_Specialprice_Cp
from pro.apis.entitys.GA_entitys.cp.unify_moneyback_cp import Unify_MoneyBack_Cp
from pro.apis.entitys.GA_entitys.cp.combination_moneyback_cp import Combination_Moneyback_Cp
from pro.apis.GA_api.DC_api.dc_main import getDiscount
from pro.apis.GA_api.BG_api.bg_main import get_BuyGift
from pro.utils.pro_exception import ProException
from pro.apis.entitys.GA_entitys.specialprice.gradient_Special_price import Gradient_Special_price
from pro.apis.entitys.GA_entitys.specialprice.unify_Special_price import Unify_Special_price
from pro.apis.entitys.GA_entitys.specialprice.combination_Special_price import Combination_Special_SpriceEntity
from pro.apis.entitys.GA_entitys.maimian.unify_maimian import Unify_Maimian
from pro.apis.entitys.GA_entitys.maimian.combination_maimian import CombinationMaimian
from pro.apis.GA_api.SO_api.so_main import get_special_price
from pro.apis.GA_api.PE_api.pe_main import get_maimian
from pro.apis.entitys.GA_entitys.moneyback.unify_moneyback import Unify_Moneyback
from pro.apis.entitys.GA_entitys.moneyback.gradient_moenyback import Gradient_Moneyback
from pro.apis.entitys.GA_entitys.moneyback.combination_moneyback import CombinationMoneyback
from pro.apis.GA_api.FS_api.fs_main import get_moenyback
from pro.apis.GA_api.CP_api.cp_main import get_cp
from pro.utils.linq import linq


def promotion_obj(productList, promotionJsonObj, userInfo):
    # 商品打折活动集合
    discount_list = []

    # 商品满减活动
    money_back_list = []
    # 商品买赠活动列表
    buy_giftList = []

    # 特价
    special_price_list = []

    # 买免
    maimian_list = []

    # 活动总列表
    promotion_sum = []

    # 换购集合
    cp = []
    # 取出商品活动集合
    product_activity_list = promotionJsonObj.get('product_activity_list')

    # 返回值
    response = {}

    productList_cp = copy.deepcopy(productList)
    product_List = copy.deepcopy(productList)

    #循环传入的所有商品活动，按照不同二类编码分组取出---2019-07-08
    group_list=[]
    for bean in product_activity_list:
        two_id=bean['prom_type_two']
        if bean.get('prom_type_two_code') and bean.get('prom_type_two_code') is not None:
            two_code = str(bean['prom_type_two_code']).lower()
        else:
            two_code =str(two_id)
        three_id=str(bean['prom_type_three']).lower()
        new_bean=setdisentitys(three_id,two_id,bean)
        if new_bean is None:
            raise ProException(bean['ename'] + "---二类【促销类型】或三类ID有误")
        if len(promotion_sum)==0:
            group_list.append(new_bean)
            promotion_sum.append(group_list)
        else:
            num=0
            for r_bean in promotion_sum:
                row_bean = linq(r_bean).where(lambda x: str(x.prom_type_two_code).lower() == two_code).tolist()
                if row_bean and len(row_bean)>0:
                    r_bean.append(new_bean)
                    break
                else:
                    num=num+1
            if num==len(promotion_sum):
                group_list = []
                group_list.append(new_bean)
                promotion_sum.append(group_list)

    # 定义商品的返回值
    current_response = None


    # 定义下表游标
    # cursor = 0
    buygift_two_id = []
    give_id = []
    product_cp = []
    # 排序优先级别
    promotion_sum = sorted(promotion_sum, key=lambda i: i[0].prom_type_two_c)
    # 循环遍历所有数据 分别进入每一个活动
    for promotion in promotion_sum:
        # 如果当前活动类别为1 打折
        if promotion[0].prom_type_two == 1:
            current_response = getDiscount(product_List, promotion, userInfo)
        # 2为满减
        elif promotion[0].prom_type_two == 2:
            current_response = get_moenyback(product_List, promotion, userInfo, productList_cp)
        # 3为特价
        elif promotion[0].prom_type_two == 3:
            current_response = get_special_price(product_List, promotion, userInfo, productList_cp)
        # 4为买赠
        elif promotion[0].prom_type_two == 4:
            current_response = get_BuyGift(product_List, promotion, userInfo, productList_cp)
        # 5为换购
        elif promotion[0].prom_type_two == 5:
            current_response = get_cp(product_List, promotion, userInfo, productList_cp)
        # 6为买免
        elif promotion[0].prom_type_two == 6:
            # 2019,4,26修改，增加了组合买免
            current_response = get_maimian(product_List, promotion, userInfo, productList_cp)

        # 如果返回为dict说明进入了买赠或换购
        if type(current_response) == dict:
            if current_response["product"]:
                product_List = current_response["product"]
            if current_response.get("can_part_promotion_id", []):
                for id in current_response["can_part_promotion_id"]:
                    product_List[0].discountId.add(id)
            if len(current_response["buygift"]) > 0:
                for i in current_response["buygift"]:
                    give_id.append(i)
            if len(current_response["buygift_two_id"]) > 0:
                for i in current_response["buygift_two_id"]:
                    buygift_two_id.append(i)
            if "product_cp" in current_response:
                if len(current_response["product_cp"]) > 0:
                    for i in current_response["product_cp"]:
                        product_cp.append(i)


        # 不确定如果打折不满足会不会返回None 所以就写了如果为None
        elif current_response == None:
            product_List = product_List
        else:
            product_List = current_response

    # #返参中：
    # # buygift：当前单据中所有可执行的买赠活动；
    # # buygift_two_id：当前单据中可同组执行的买赠活动的分组列表；
    response = {}
    response["product"] = product_List
    response["buygift"] = give_id
    response["buygift_two_id"] = buygift_two_id
    response["product_cp"] = product_cp
    # 返回值
    return response


def setdisentitys(three_id,two_id,bean):
    new_bean=None
    three_id = str(bean['prom_type_three']).lower()
    # print(two_id)
    if two_id == 1:
        if 'ga1101' == three_id:
            new_bean=UnifyDiscountEntity(bean)  # 统一折扣
        elif 'ga1102' == three_id:
            new_bean =MultipleDiscountEntity(bean)  # 多种折扣
        elif 'ga1103' == three_id:
            new_bean =IncrementalDiscountEntity(bean)  # 递增折扣
        elif 'ga1104' == three_id:
            new_bean =CombinationDiscountEntity(bean)  # 组合折扣

    elif two_id == 2:
        if 'ga1201' == three_id:
            new_bean =Unify_Moneyback(bean)  # 统一满减
        elif 'ga1202' == three_id:
            new_bean =Gradient_Moneyback(bean)  # 梯度满减
        elif 'ga1203' == three_id:
            new_bean =CombinationMoneyback(bean)

    elif two_id == 3:
        if "ga1301" == three_id:
            new_bean =Unify_Special_price(bean)  # 统一特价
        elif "ga1302" == three_id:
            new_bean =Gradient_Special_price(bean)  # 梯度特价
        elif "ga1303" == three_id:
            new_bean =Combination_Special_SpriceEntity(bean)  # 组合特价--hexiaoxia 2019/04/15

    elif two_id == 4:
        if "ga1401" == three_id:
            new_bean =Unify_BuyGift(bean)  # 统一买赠
        elif "ga1402" == three_id:
            new_bean =Gradient_BuyGift(bean)  # 梯度买赠
        elif "ga1405" == three_id:
            new_bean =Combination_buygiftEntity(bean)  # 组合买赠--hexiaoxia 2019/04/26
        elif "ga1701" == three_id or "ga1801" == three_id:
            new_bean =Unify_BuyGift_Online(bean)  # 线上统一买赠、线上排名统一买赠-- 2019/07/11
        elif "ga1702" == three_id or "ga1802" == three_id:
            new_bean =Gradient_BuyGift_Online(bean)  # 线上梯度买赠、线上排名梯度买赠-- 2019/07/11
        elif "ga1703" == three_id or "ga1803" == three_id:
            new_bean =Combination_buygift_Online(bean)  # 线上组合买赠、线上排名组合买赠--2019/07/11

    elif two_id == 5:
        if "ga1503" == three_id:  # 统一打折换购:GA1503
            new_bean =Unify_Cp(bean)
        elif "ga1504" == three_id:  # 组合打折换购:GA1504
            new_bean =CombinationDiscountEntity_Cp(bean)
        elif "ga1501" == three_id:  # GA1501", "统一特价换购
            new_bean =Unify_Specialprice_cp(bean)
        elif "ga1502" == three_id:  # "GA1502", "组合特价换购"
            new_bean =Combination_Specialprice_Cp(bean)
        elif "ga1505" == three_id:  # GA1505", "统一优惠换购
            new_bean =Unify_MoneyBack_Cp(bean)
        elif "ga1506" == three_id:  # GA1506", "组合优惠换购
            new_bean =Combination_Moneyback_Cp(bean)

    elif two_id == 6:
        if "ga1601" == three_id:  # "GA1601, 统一买免"
            new_bean =Unify_Maimian(bean)
        elif "ga1602" == three_id:  # "GA1602, 组合买免"
            new_bean =CombinationMaimian(bean)

    return new_bean



