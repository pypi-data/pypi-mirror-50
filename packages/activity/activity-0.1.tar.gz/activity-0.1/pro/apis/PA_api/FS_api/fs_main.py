# -*- coding:utf-8 -*-
# author:李旭辉
# datetime:2018/10/23 9:36
import copy
from pro.apis.entitys.PA_entitys.promotion_entity import *
def executemoneyback(productList, moneyback, userInfo,r_disobj):
    '''
    全场活动满减类的活动具体计算入口
    :param productList: 参与计算的商品
    :param buygifts: 全场买赠活动
    :param userInfo: 会员
    :return:
    '''
    newproduct={}
    ifvipdis=True
    try:
        type_three = moneyback.prom_type_three.upper()
        if moneyback.target_item.lower()=="amt_receivable":
            productList = sorted(productList, key=lambda x: x.amt_receivable,reverse=True) #按照应收价格降序
        elif moneyback.target_item.lower()=="amt_list":
            productList = sorted(productList, key=lambda x: x.amt_list, reverse=True)  # 按照吊牌价格降序
        else:
            productList = sorted(productList, key=lambda x: x.amt_retail, reverse=True)  # 按照零售价格降序
        if type_three == "PA1201":
            # 统一满减
            newproduct = unifymoneyback(productList, moneyback)
        elif type_three == "PA1202":
            # 梯度满减
            newproduct = incrementalmb(productList, moneyback)
        if newproduct and newproduct.get("disproductList"):
            newproduct["disproductList"]=sorted(newproduct["disproductList"],key=lambda x:x.amt_receivable,reverse=True)
            for row in newproduct["disproductList"]:
                row.fulldiscountID.append(moneyback.id)
                for row1 in row.productSeatList:
                    if row1.is_discount == "n":
                        continue
                    row1.fulldiscounts.append(r_disobj["id"])
                    if row1.is_run_vip_discount:
                        ifvipdis = False
            #执行VIP折上折
            isvipdis = False
            if moneyback.is_run_vip_discount and userInfo is not None and ifvipdis:
                if moneyback.members_only:
                    if userInfo.id in moneyback.members_group:
                        newproduct["total_amt_receivable"]="%.2f" % float(util.mul(newproduct["total_amt_receivable"],userInfo.discount))
                        newproduct["new_total_amt_receivable"]=newproduct["total_amt_receivable"]
                        isvipdis = True
                else:
                    if userInfo.discount is not None:
                        newproduct["total_amt_receivable"] = "%.2f" % float(util.mul(newproduct["total_amt_receivable"], userInfo.discount))
                        newproduct["new_total_amt_receivable"] = newproduct["total_amt_receivable"]
                        isvipdis = True
            if isvipdis:
                for row in newproduct["disproductList"]:
                    for row1 in row.productSeatList:
                        row1.is_run_vip_discount=True
    except Exception as e:
        newproduct={}

    return newproduct


def unifymoneyback(productList, moneyback):
    '''
    全场活动统一满减计算
    :param productList: 参与的商品信息
    :param moneyback: 全场活动信息
    :return: 返回包含计算得到的新的总应收金额的结果
    '''
    try:
        target_type=moneyback.target_type#获取比较条件
        target_item=moneyback.target_item
        operation_set=moneyback.operation_set[0]#获取比较整体列表
        comp_symb_type=operation_set.get("comp_symb_type","ge").lower() #比较符
        value_num=operation_set.get("value_num",1) #比较值
        money_off_value=operation_set["money_off_value"]
        newproduct=setproductlist(productList,target_type)
        v_comparison = newproduct["v_comparison"]
        isfs=checkdis(comp_symb_type,v_comparison,value_num,target_type)
        if isfs:
            if float(newproduct["total_amt_receivable"] - newproduct.get("special_total_amt_receivable", 0)) == 0:
                return {"keepdis": "Y"}
            if comp_symb_type=="g" and value_num!=0:
                value_num = value_num + 1
            newproduct["money_off_value"]=money_off_value
            money_off_num=times(newproduct,target_type,value_num,moneyback,money_off_value)
            times_money_off_value=money_off_num*money_off_value
            if target_type=="qtty" and comp_symb_type=="e":
                times_value_num=money_off_num*value_num
                newproduct = setproductlist2(newproduct, times_value_num, target_item)
            # if (comp_symb_type=="ge" or comp_symb_type=="g") and target_type=="qtty" and moneyback.max_times>=0:
            #     times_value_num=times_money_off_value//money_off_value*value_num
            #     if newproduct["total_qtty"]>times_value_num:
            #         newproduct = setproductlist2(newproduct, times_value_num, target_item)
            #     else:
            #         newproduct=newproduct
            if newproduct["total_oldamt_receivable"] == 0:
                # 如果全都是特例品， 直接返回
                return {"keepdis": "N"}
            total_amt_receivable = util.minus(newproduct["total_amt_receivable"], newproduct.get(
                "special_total_amt_receivable", 0))
            new_total_amt_receivable = "%.2f" % float(util.minus(total_amt_receivable, times_money_off_value))

            if float(new_total_amt_receivable) < 0:
                new_total_amt_receivable = 0
            new_total_amt_receivable = util.add(new_total_amt_receivable, newproduct.get(
                "special_total_amt_receivable", 0))
            newproduct["new_total_amt_receivable"] = float(new_total_amt_receivable)
            newproduct["total_amt_receivable"] = float(new_total_amt_receivable)
            newproduct["keepdis"] = "Y"
            return newproduct
        else:
            return {"keepdis": "N"}
    except Exception as e:
        return {}

def incrementalmb(productList, moneyback):
    '''
    全场活动梯度满减计算
    :param productList: 参与的商品信息
    :param moneyback: 全场活动信息
    :return: 返回包含计算得到的新的总应收金额的结果
    '''
    try:
        target_type = moneyback.target_type
        target_item=moneyback.target_item
        operation_set = moneyback.operation_set
        operation_set = sorted(operation_set, key=lambda x: x.get('value_num'), reverse=True)
        newproduct=setproductlist(productList,target_type)
        maxoperation_set = tidu_checkdis(operation_set,newproduct)
        if maxoperation_set:
            if float(newproduct["total_amt_receivable"] - newproduct.get("special_total_amt_receivable", 0)) == 0:
                return {"keepdis": "Y"}
            operation=maxoperation_set
            if operation['value_num'] != 0 and operation['comp_symb_type'].lower() == "g":
                value_num = operation['value_num'] + 1
            else:
                value_num=operation['value_num']
            money_off_value = operation['money_off_value']
            money_off_num=times(newproduct,target_type,value_num,moneyback,money_off_value)
            times_money_off_value=money_off_num*money_off_value
            if target_type=="qtty" and operation['comp_symb_type'].lower()=="e":
                times_value_num=money_off_num*value_num
                newproduct = setproductlist2(newproduct, times_value_num, target_item)
            # if (operation['comp_symb_type'].lower()=="ge" or operation['comp_symb_type'].lower()=="g") and target_type=="qtty" and moneyback.max_times>=0:
            #     times_value_num=times_money_off_value//money_off_value*value_num
            #     if newproduct["total_qtty"]>times_value_num:
            #         newproduct = setproductlist2(newproduct, times_value_num, target_item)
            #     else:
            #         newproduct=newproduct
            if float(newproduct["total_amt_receivable"] - newproduct.get("special_total_amt_receivable", 0)) == 0:
                return {"keepdis": "Y"}
            total_amt_receivable = util.minus(newproduct["total_amt_receivable"], newproduct.get(
                "special_total_amt_receivable", 0))
            new_total_amt_receivable = "%.2f" % float(util.minus(total_amt_receivable, times_money_off_value))

            if float(new_total_amt_receivable) < 0:
                new_total_amt_receivable = 0
            new_total_amt_receivable = util.add(new_total_amt_receivable, newproduct.get(
                "special_total_amt_receivable", 0))
            newproduct["new_total_amt_receivable"] = float(new_total_amt_receivable)
            newproduct["total_amt_receivable"] = float(new_total_amt_receivable)
            newproduct["keepdis"] = "Y"
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
    special_total_amt_receivable = 0
    t_productl["disproductList"]=copy.deepcopy(productList)
    for row in productList:
        if target_type == "qtty":
            v_comparison = v_comparison + int(row.qtty)
        elif target_type == "amt_list":
            # 吊牌金额
            v_comparison = v_comparison + float(row.total_amt_list)
        elif target_type == "amt_retail":
            # 零售金额
            v_comparison = v_comparison + float(row.total_amt_retail)
        elif target_type == "amt_receivable":
            # 应收金额
            v_comparison = v_comparison + float(row.total_amt_receivable)
        if row.productSeatList[0].is_discount == "n":
            special_total_amt_receivable = special_total_amt_receivable + float(row.total_amt_receivable)

        total_amt_list=total_amt_list+float(row.total_amt_list)
        total_amt_retail=total_amt_retail+float(row.total_amt_retail)
        total_amt_receivable=total_amt_receivable+float(row.total_amt_receivable)
        total_qtty=total_qtty+int(row.qtty)
    t_productl["v_comparison"]=v_comparison
    t_productl["total_amt_list"]=total_amt_list
    t_productl["total_amt_retail"]=total_amt_retail
    t_productl["total_amt_receivable"]=total_amt_receivable #参与策略的总应收金额
    t_productl["special_total_amt_receivable"] = special_total_amt_receivable
    t_productl["total_oldamt_receivable"] = total_amt_receivable
    t_productl["total_qtty"]=total_qtty
    return t_productl
def getfsbyoriginalpro(moneyback,originalproductlist):
    type_three = str(moneyback.prom_type_three).upper()
    target_type = moneyback.target_type
    target_item = moneyback.target_item
    operation_set = moneyback.operation_set
    operation_set = sorted(operation_set, key=lambda x: x["value_num"], reverse=True)
    newproduct = setproductlist(originalproductlist, target_type)
    v_comparison = newproduct["v_comparison"]
    if type_three == "PA1201":
        # 统一减现
        operation_set = moneyback.operation_set[0]
        comp_symb_type = str(operation_set.get("comp_symb_type", "ge")).lower()  # 比较符
        value_num = operation_set.get("value_num", 0)  # 比较值v_comparison = newproduct["v_comparison"]
        iskeepbg = checkdis(comp_symb_type, v_comparison, value_num, target_type)
        if iskeepbg:
            return True
        else:
            return False
    elif type_three == "PA1202":
        # 梯度减现
        maxoperation_set=tidu_checkdis(operation_set,newproduct)
        if maxoperation_set:
            return True
        else:
            return False
def checkdis(comp_symb_type,v_comparison,value_num,target_type):
    isfs = False  # 是否可以执行优惠
    if comp_symb_type == "ge":
        if v_comparison >= float(value_num):
            isfs = True
    elif comp_symb_type == "g":
        if v_comparison > float(value_num):
            isfs= True
    elif comp_symb_type == "e":
        if value_num == 0 and target_type == "qtty":
            isfs = False
        if v_comparison >= float(value_num):
            isfs = True
    return isfs
def tidu_checkdis(operation_set,newproduct):
    maxoperation_set={}
    for row in operation_set:
        comp_symb_type = str(row.get("comp_symb_type", "ge")).lower()  # 比较符
        value_num = row.get("value_num", 0)  # 比较值
        v_comparison = newproduct["v_comparison"]
        if comp_symb_type == "ge":
            if v_comparison >= float(value_num):
                maxoperation_set = row
        elif comp_symb_type == "g":
            if v_comparison > float(value_num):
                maxoperation_set = row
        elif comp_symb_type == "e":
            if v_comparison >= float(value_num):
                maxoperation_set = row
        if maxoperation_set:
            break
    return maxoperation_set
def times(newproduct,target_type,value_num,moneyback,money_off_value):
    if newproduct["v_comparison"] >= value_num:
        money_off_num = newproduct["v_comparison"] // value_num
        if moneyback.max_times == 0 or moneyback.max_times is None or value_num == 0:
            money_off_num = 1
        elif moneyback.max_times > 0:
            if money_off_num > moneyback.max_times:
                money_off_num = moneyback.max_times
    return money_off_num
def setproductlist2(disproobj,value_num,target_item):
    '''
    对于执行条件设置的是等于N件满足执行的情况下，参与的商品总数量大于N件，重新筛选出等于N件数量的商品行参与促销，其它多余的商品不参与促销
    :param disproobj: 原参与促销整个对象
    :param value_num: 策略比较值
    :return:
    '''
    t_productl={}
    dis_products = []  # 参与计算的商品明细
    nodis_products = []  # 不参与计算的商品明细
    total_amt_list=0 #当前参与策略的所有商品的总吊牌金额
    total_amt_retail=0 #当前参与策略的所有商品的总零售金额
    total_amt_receivable=0 #当前参与策略的所有商品的总应收金额
    total_qtty=0 #记录当前参与该策略的总商品数量
    productList=copy.deepcopy(disproobj["disproductList"])
    t_pronum=0
    for row in productList:
        productSeatList = row.productSeatList
        if target_item=="amt_receivable":
            productSeatList = sorted(productSeatList, key=lambda x: x.amt_receivable,reverse=True) #按照应收价格降序
        elif target_item=="amt_list":
            productSeatList = sorted(productSeatList, key=lambda x: x.amt_list, reverse=True)  # 按照吊牌价格降序
        else:
            productSeatList = sorted(productSeatList, key=lambda x: x.amt_retail, reverse=True)  # 按照零售价格降序
        new_disrowpro = {}
        new_nodisrowpro = {}
        total_amt_listdis = 0
        total_amt_retaildis = 0
        total_amt_receivabledis = 0
        total_amt_listnodis = 0
        total_amt_retailnodis = 0
        total_amt_receivablenodis = 0
        if productSeatList:
            new_disrowpro = copy.deepcopy(row)
            new_nodisrowpro = copy.deepcopy(row)
            new_disrowpro.productSeatList = []
            new_disrowpro.qtty = 0
            new_nodisrowpro.productSeatList = []
            new_nodisrowpro.qtty = 0
            for row1 in productSeatList:
                if t_pronum<value_num and row1.is_discount == "y":
                    t_pronum=t_pronum+row1.qtty
                    if target_item == "amt_retail":
                        row1.amt_receivable = row1.amt_retail
                    elif target_item == "amt_list":
                        row1.amt_receivable = row1.amt_list
                    new_disrowpro.productSeatList.append(row1)
                    new_disrowpro.qtty = new_disrowpro.qtty + 1
                    total_amt_listdis = total_amt_listdis + float(row1.amt_list)
                    total_amt_retaildis = total_amt_retaildis + float(row1.amt_retail)
                    total_amt_receivabledis = total_amt_receivabledis + float(row1.amt_receivable)
                else:
                    new_nodisrowpro.productSeatList.append(row1)
                    new_nodisrowpro.qtty = new_nodisrowpro.qtty + 1
                    total_amt_listnodis = total_amt_listnodis + float(row1.amt_list)
                    total_amt_retailnodis = total_amt_retailnodis + float(row1.amt_retail)
                    total_amt_receivablenodis = total_amt_receivablenodis + float(row1.amt_receivable)
            if new_disrowpro.productSeatList:
                # 吊牌金额
                new_disrowpro.total_amt_list = total_amt_listdis
                # 零售金额
                new_disrowpro.total_amt_retail = total_amt_retaildis
                # 应收金额
                new_disrowpro.total_amt_receivable = total_amt_receivabledis
                dis_products.append(new_disrowpro)
                total_amt_list = total_amt_list + total_amt_listdis
                total_amt_retail = total_amt_retail + total_amt_retaildis
                total_amt_receivable = total_amt_receivable + total_amt_receivabledis
                total_qtty=total_qtty+int(new_disrowpro.qtty)
            if new_nodisrowpro.productSeatList:
                # 吊牌金额
                new_nodisrowpro.total_amt_list = total_amt_listnodis
                # 零售金额
                new_nodisrowpro.total_amt_retail = total_amt_retailnodis
                # 应收金额
                new_nodisrowpro.total_amt_receivable = total_amt_receivablenodis
                nodis_products.append(new_nodisrowpro)
    t_productl["disproductList"] =dis_products
    t_productl["nodisproductList"] =nodis_products
    t_productl["v_comparison"]=disproobj["v_comparison"]
    t_productl["total_amt_list"]=total_amt_list
    t_productl["total_amt_retail"]=total_amt_retail
    t_productl["total_amt_receivable"]=total_amt_receivable
    t_productl["total_oldamt_receivable"] = total_amt_receivable
    t_productl["total_qtty"]=total_qtty
    return t_productl