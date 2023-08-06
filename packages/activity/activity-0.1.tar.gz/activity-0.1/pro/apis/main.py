# encoding=utf-8

import copy
import threading
import traceback
import time
import operator

from pro.apis.entitys.products_entitys.product import Product
from pro.settings.globle_params import global_data
from pro.utils.pro_exception import ProException
from pro.apis.entitys.user_info import UserInfo
from pro.apis.PA_api.main_api import executefullactivity
from pro.apis.PA_api.main_api import getgadis
from pro.apis.PA_api.main_api import getreturnprovalue
from pro.apis.PA_api.main_api import getreturnprodisvalue
from pro.apis.PA_api.main_api import getreturndisvalue
from pro.apis.PA_api.main_api import getreturnbgpro
from pro.apis.PA_api.main_api import getreturnbgtwo
from pro.apis.PA_api.main_api import getcpproducts

from pro.settings.logs import Log
from pro.settings import globle_params




from pro.apis.product_promotion_objcet import promotion_obj
import json
# 接收参数
def acceptParams(productJsonList, promotionJsonObj, userInfoJson, retail_carryway):
    '''
    促销执行的总入口
    :param productJsonList: 商品明细
    :param promotionJsonObj: 促销信息
    :param userInfoJson: VIP信息
    :param retail_carryway: 金额进位方式
    :return:
    '''
    # 所有商品对象集合
    productList = []
    # 商品打折活动集合
    discount_list = []
    # 全场打折活动集合
    pa11_list = []
    try:
        if retail_carryway == None:
            retail_carryway = 2
        # 把当前进位参数存放当前线程中
        globle_params.set_retail_carryway(retail_carryway)
        userInfo = check(productJsonList, promotionJsonObj, userInfoJson)
        # 所有商品放入商品对象集合
        i = 1
        for productJson in productJsonList:
            productList.append(Product(productJson, i))
            i = i + 1
        # 取出商品活动集合
        product_activity_list = promotionJsonObj.get('product_activity_list', [])

        # 取出全场活动集合
        fullcourt_activity_list = promotionJsonObj.get('fullcourt_activity_list', [])
        # 择优运算中类级别 预留
        productListGA = []
        r_returnvalue = {}
        product_cp=[]
        buygift_two_id=[]
        buy_gift=[]
        if product_activity_list:

        # 商品活动的最优计算list中会包含买赠和打折各种活动
            response = promotion_obj(productList,promotionJsonObj,userInfo)
            if response:
                if "buygift" in response:
                    buy_gift=response['buygift']
                if "buygift_two_id" in response:
                    buygift_two_id=response["buygift_two_id"]
                productListGA = response['product']
                if "product_cp" in response:
                    product_cp = response["product_cp"]




        if fullcourt_activity_list:
            # 商品进入全场活动折扣二类所有折扣活动择优运算
            fulldispro = productListGA if productListGA else copy.deepcopy(productList)
            for row in fulldispro:
                for row1 in row.productSeatList:
                    row1.seat = False
            try:
                r_returnvalue = executefullactivity(fulldispro, fullcourt_activity_list, userInfo, product_activity_list,productList,buy_gift,buygift_two_id,product_cp)
            except UnboundLocalError:
                r_returnvalue = executefullactivity(fulldispro, fullcourt_activity_list, userInfo,product_activity_list, productList)
            r_returnvalue['status'] = 0
            return r_returnvalue
        else:
            products = []
            alldis = []
            optimal_dis = []
            dis_proitems = []
            fullgit_dis=[]
            swap_products=[]
            if productListGA:
                getgadis(copy.deepcopy(productListGA), alldis, product_activity_list,buy_gift),
                products = getreturnprovalue(copy.deepcopy(productListGA), [])
                swap_products=getcpproducts(product_cp,[])
                for row in products:
                    row["amt_receivable"] = float("%.2f" % row["amt_receivable"])
                    # row["beforpadisamt_receivable"] = row["amt_receivable"]
                optimal_dis = getreturndisvalue(copy.deepcopy(productListGA), [], product_activity_list,
                                                fullcourt_activity_list)
                dis_proitems = getreturnprodisvalue(copy.deepcopy(productListGA), [], product_activity_list,
                                                    discount_list)
            else:
                products = getreturnprovalue(copy.deepcopy(productList), [])
            fullgit_dis=getreturnbgpro(copy.deepcopy(productListGA),[],product_activity_list,fullcourt_activity_list,optimal_dis,buy_gift)
            fullgit_disgroup=getreturnbgtwo(buygift_two_id)
            return {"status": 0, "products": products, "swap_products":swap_products,"optimal_dis": optimal_dis, "alldis": alldis,"dis_proitems": dis_proitems,"fullgit_dis":fullgit_dis,"fullgit_disgroup":fullgit_disgroup}
    except ProException as esc:
        logs = Log()
        logs.error("错误信息开始" + ("*" * 50))
        logs.error(str(esc))
        logs.error(traceback.print_exc())
        logs.error(traceback.format_exc())
        logs.error("错误信息结束" + ("*" * 50))
        return {"status": -1, "message": str(esc.arg)}


# 商品集合与活动集合的非空判断
def check(productJsonList, promotionJsonObj, userInfoJson):
    if len(productJsonList) < 1:
        raise ProException("商品为空")
    # 未添加key 为空判断
    if promotionJsonObj == None or (promotionJsonObj.get('product_activity_list', []) == None and promotionJsonObj.get(
            'fullcourt_activity_list', []) == None) or (
            len(promotionJsonObj.get('product_activity_list', [])) < 1 and len(
        promotionJsonObj.get('fullcourt_activity_list', [])) < 1):
        raise ProException("促销活动为空")
    userInfo = UserInfo(userInfoJson)
    return userInfo
