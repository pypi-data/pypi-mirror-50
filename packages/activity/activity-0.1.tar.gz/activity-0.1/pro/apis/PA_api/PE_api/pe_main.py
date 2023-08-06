# -*- coding:utf-8 -*-
# author:李旭辉
# datetime:2018/11/14 19:22
import copy
import pro.utils.util as util
from pro.apis.entitys.products_entitys.product import *
from pro.apis.entitys.products_entitys.product_seat import *
from pro.apis.entitys.PA_entitys.promotion_entity import *
from pro.apis.entitys.user_info import *
def executemaimian(productList, maimians, userInfo):
    '''
    全场活动买免类的活动具体计算入口
    :param productList: 参与计算的商品
    :param buygifts: 全场买赠活动
    :param userInfo: 会员
    :return:
    '''
    newproduct={}
    ifvipdis=True
    try:
        type_three = maimians.prom_type_three.upper()
        if maimians.target_item.lower()=="amt_receivable":
            productList = sorted(productList, key=lambda x: x.amt_receivable,reverse=True) #按照应收价格降序
        elif maimians.target_item.lower()=="amt_list":
            productList = sorted(productList, key=lambda x: x.amt_list, reverse=True)  # 按照吊牌价格降序
        else:
            productList = sorted(productList, key=lambda x: x.amt_retail, reverse=True)  # 按照零售价格降序
        if type_three == "PA1501":
            # 买免
            newproduct = maimian(productList, maimians)
        if newproduct and newproduct.get("disproductList"):
            #重新计算单据总金额
            new_total_amt_receivable=0
            for row in newproduct["disproductList"]:
                row.fulldiscountID.append(maimians.id)
                for row1 in row.productSeatList:
                    new_total_amt_receivable = new_total_amt_receivable + float(row1.amt_receivable)
                    if row1.is_run_vip_discount:
                        ifvipdis = False
            newproduct["total_amt_receivable"] = new_total_amt_receivable
            newproduct["new_total_amt_receivable"] = new_total_amt_receivable
            newproduct["total_oldamt_receivable"] = new_total_amt_receivable
            #执行VIP折上折
            isvipdis = False
            if maimians.is_run_vip_discount and userInfo is not None and ifvipdis:
                if maimians.members_only:
                    if userInfo.id in maimians.members_group:
                        newproduct["total_amt_receivable"]=util.CalculationPrice(util.mul(newproduct["total_amt_receivable"],userInfo.discount))
                        newproduct["new_total_amt_receivable"]=newproduct["total_amt_receivable"]
                        isvipdis = True
                else:
                    if userInfo.discount is not None:
                        newproduct["total_amt_receivable"] = util.CalculationPrice(util.mul(newproduct["total_amt_receivable"], userInfo.discount))
                        newproduct["new_total_amt_receivable"] = newproduct["total_amt_receivable"]
                        isvipdis = True
            if isvipdis:
                newproduct["isCalculation"] = "N"
                for row in newproduct["disproductList"]:
                    for row1 in row.productSeatList:
                        if row1.is_taken_off==False:
                            row1.fulldiscounts.append(maimians.id)
                        row1.is_run_vip_discount=True
    except Exception as e:
        newproduct={}

    return newproduct
def maimian(productList, maimians):
    '''
    全场活动买免计算
    :param productList: 参与的商品信息
    :param buygifts: 全场活动信息
    :return: 返回包含计算得到的新的总应收金额的结果
    '''
    try:
        operation_set=maimians.operation_set[0]#获取比较整体列表
        value_num=operation_set.get("value_num",0) #比较值
        comp_symb_type = operation_set.get("comp_symb_type", "ge").lower()  # 比较符
        buy_from=operation_set["buy_from"]
        newproduct=setproductlist(productList,"qtty")
        new_total_amt_receivable = 0  # 记录优惠后的所有参与商品的总应收金额
        v_comparison = newproduct["v_comparison"]
        isfe=checkpe(v_comparison,value_num,comp_symb_type,buy_from)
        if isfe:
            newproduct["buy_from"]=buy_from
            num=buy_from
            if comp_symb_type=="g" and value_num!=0:
                value_num=value_num+1
            if newproduct["total_qtty"]>=value_num:
                buy_from=buy_from_times(maimians,newproduct,buy_from,value_num)
            #使用两个变量记录买免数量，用来控制标记数量
            nownum = buy_from
            newnum=buy_from
            #将所有的商品明细添加到一个列表中
            productlist=[]
            pro_num = 0  # 计算可以参加计算的商品的数量
            for disproduct in newproduct["disproductList"]:
                seat = disproduct.productSeatList
                for row in seat:
                    if row.is_discount == "n":
                        continue
                    pro_num += 1
                    productlist.append(row)
            # 将可参加活动商品明细按应收价升序排列
            if not productlist:
                return {"keepdis": "Y"}
            nownum = min(nownum, pro_num)  # 取免去值和可以参与计算的商品的数量中较小的一个
            productlist = sorted(productlist, key=lambda x: x.amt_receivable)
            # 按照比较值划分商品明细列表
            for i in range(0, nownum):
                # if len(productlist)-i<value_num or nownum==0:
                #     break
                # small_list=productlist[i:i+value_num]
                # #反转划分后的列表，使其应收价为升序排列，应收价改为0，参加活动为本活动，优惠金额为吊牌价
                # for product in productlist:
                productlist[i].fulldiscounts.append(maimians.id)
                productlist[i].fulldiscountPrice.append(util.CalculationPrice(productlist[i].amt_receivable))
                productlist[i].is_taken_off = True
                productlist[i].is_run_store_act = False
                productlist[i].upamt_receivable = productlist[i].amt_receivable
                productlist[i].amt_receivable = 0.0
                # nownum-=1
                # #当翻倍后的买免数量减去循环递减后的翻倍后的买免数量等于原买免数量时，newnum递减原买免值，跳出循环
                # if newnum-nownum==num:
                #     newnum-=num
                #     break
            for row in newproduct["disproductList"]:
                for row1 in row.productSeatList:
                    new_total_amt_receivable+=row1.amt_receivable
            newproduct["new_total_amt_receivable"] = float(new_total_amt_receivable)
            newproduct["total_amt_receivable"] = float(new_total_amt_receivable)
            newproduct["keepdis"] = "Y"
            newproduct["isCalculation"] = "Y"
            return newproduct
        else:
            return {"keepdis": "N"}
    except Exception as e:
        return {}
def setproductlist(productList,target_type):
    t_productl={}
    v_comparison = 0
    total_amt_list=0 #当前参与策略的所有商品的总吊牌金额
    total_amt_retail=0 #当前参与策略的所有商品的总零售金额
    total_amt_receivable=0 #当前参与策略的所有商品的总应收金额
    total_qtty=0 #记录当前参与该策略的总商品数量
    t_productl["disproductList"]=copy.deepcopy(productList)
    for row in productList:
        if target_type == "qtty":
            v_comparison = v_comparison + int(row.qtty)
        total_amt_list=total_amt_list+float(row.total_amt_list)
        total_amt_retail=total_amt_retail+float(row.total_amt_retail)
        total_amt_receivable=total_amt_receivable+float(row.total_amt_receivable)
        total_qtty=total_qtty+int(row.qtty)
    t_productl["v_comparison"]=v_comparison
    t_productl["total_amt_list"]=total_amt_list
    t_productl["total_amt_retail"]=total_amt_retail
    t_productl["total_amt_receivable"]=total_amt_receivable #参与策略的总应收金额
    t_productl["total_oldamt_receivable"] = total_amt_receivable
    t_productl["total_qtty"]=total_qtty
    return t_productl
def checkpe(v_comparison,value_num,comp_symb_type,buy_from):
    isfe = False  # 是否可以执行优惠
    if comp_symb_type == "ge":
        if v_comparison >= float(value_num):
            isfe = True
    elif comp_symb_type == "g":
        if v_comparison > float(value_num):
            isfe = True
    elif comp_symb_type == "e":
        if value_num == 0:
            isfe = False
        if v_comparison >= float(value_num):
            isfe = True
    if value_num<=buy_from:
        isfe=False
    return isfe
def buy_from_times(maimians,newproduct,buy_from,value_num):
    # 当翻倍次数为-1时，买免数量为录入商品总数量或总金额*买免值//比较值
    if maimians.max_times == -1:
        buy_from = newproduct['total_qtty']// value_num * buy_from
    # 当翻倍次数为0或空时，买免值为原买免值
    elif maimians.max_times == 0 or maimians.max_times is None or value_num == 0:
        buy_from = buy_from
    # 当翻倍次数大于0时，分为3种情况：1、当商品总数量<翻倍次数*比较值，买免数量为录入商品总数量或总金额*买免值//比较值
    # 2、当商品总数量或总金额>=翻倍次数*比较值，买免数量为原买免数量*翻倍次数
    # 3、当商品总数量或总金额<比较值，买免值为原买免值
    elif maimians.max_times > 0:
        if newproduct['total_qtty'] < maimians.max_times * value_num:
            buy_from = newproduct['total_qtty'] // value_num* buy_from
        elif newproduct['total_qtty'] >= maimians.max_times * value_num:
            buy_from = buy_from * maimians.max_times
    return buy_from
def getpebyoriginalpro(maimian,originalproductlist):
    target_type = maimian.target_type
    newproduct = setproductlist(originalproductlist, target_type)
    v_comparison = newproduct["v_comparison"]
    # 统一买免
    operation_set = maimian.operation_set[0]
    comp_symb_type = str(operation_set.get("comp_symb_type", "ge")).lower()  # 比较符
    value_num = operation_set.get("value_num", 0)  # 比较值v_comparison = newproduct["v_comparison"]
    buy_from =  operation_set.get("buy_from", 0)
    iskeeppe = checkpe(v_comparison, value_num,comp_symb_type,buy_from)
    if iskeeppe:
        return True
    else:
        return False
