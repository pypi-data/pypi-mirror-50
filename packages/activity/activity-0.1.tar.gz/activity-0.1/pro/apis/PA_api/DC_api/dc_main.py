# -*- coding:utf-8 -*-
# author:何小霞
# datetime:2018/9/28 10:28
import copy
import pro.utils.util as util




def executediscount(productList, discount, userInfo,r_disobj):
    '''
    全场活动折扣类的活动具体计算入口
    :param productList: 参与计算的商品
    :param discount: 全场活动
    :param userInfo: 会员
    :return:
    '''
    newproduct={}
    ifvipdis=True
    isvipdis=False
    try:
        type_three = str(discount.prom_type_three).upper()
        if discount.target_item=="amt_receivable":
            productList = sorted(productList, key=lambda x: x.amt_receivable,reverse=True) #按照应收价格降序
        elif discount.target_item=="amt_list":
            productList = sorted(productList, key=lambda x: x.amt_list, reverse=True)  # 按照吊牌价格降序
        else:
            productList = sorted(productList, key=lambda x: x.amt_retail, reverse=True)  # 按照零售价格降序
        if type_three == "PA1101":
            # 统一折扣
            newproduct=unifydis(productList,discount)
        elif type_three == "PA1102":
            #多种折扣
            newproduct=multipledis(productList,discount)
        elif type_three == "PA1103":
            #递增折扣
            newproduct=incrementaldis(productList,discount,r_disobj)


        if newproduct and newproduct.get("disproductList"):
            for row in newproduct["disproductList"]:
                row.fulldiscountID.append(discount.id)
                for row1 in row.productSeatList:
                    if type_three!="PA1103" and row1.is_discount == "y":
                        row1.fulldiscounts.append(r_disobj["id"])
                    if row1.is_run_vip_discount:
                        ifvipdis=False

            #执行VIP折上折
            if discount.is_run_vip_discount and userInfo is not None and ifvipdis:
                if discount.members_only:
                    if userInfo.id in discount.members_group and userInfo.discount is not None:
                        newproduct["total_amt_receivable"]=util.CalculationPrice(util.mul(newproduct["total_amt_receivable"],userInfo.discount))
                        newproduct["new_total_amt_receivable"]=newproduct["total_amt_receivable"]
                        if type_three=="PA1103":
                            newproduct["isCalculation"] = "N"
                        isvipdis=True
                else:
                    if userInfo.discount is not None:
                        newproduct["total_amt_receivable"] = util.CalculationPrice(util.mul(newproduct["total_amt_receivable"], userInfo.discount))
                        newproduct["new_total_amt_receivable"]=newproduct["total_amt_receivable"]
                        if type_three=="PA1103":
                            newproduct["isCalculation"] = "N"
                        isvipdis=True
            if isvipdis:
                for row in newproduct["disproductList"]:
                    for row1 in row.productSeatList:
                        row1.is_run_vip_discount=True


    except Exception as e:
        newproduct={}

    return newproduct

def checkdis(comp_symb_type,v_comparison,value_num):
    isdis = False  # 是否可以执行优惠
    if comp_symb_type == "ge":
        if v_comparison >= float(value_num):
            isdis = True
    elif comp_symb_type == "g":
        if v_comparison > float(value_num):
            isdis = True
    elif comp_symb_type == "e":
        if v_comparison == float(value_num):
            isdis = True
        elif v_comparison > float(value_num):
            isdis = True
    return isdis

def unifydis(productList, discount):
    '''
    全场活动统一折扣计算
    :param productList: 参与的商品信息
    :param discount: 全场活动信息
    :return: 返回包含计算得到的新的总应收金额的结果
    '''
    try:
        target_type=discount.target_type
        target_item=discount.target_item
        operation_set=discount.operation_set[0]
        comp_symb_type = str(operation_set.get("comp_symb_type", "ge")).lower() #比较符
        value_num=operation_set.get("value_num",0) #比较值
        discount_value=operation_set.get("discount_value",1) #折扣值
        newproduct=setproductlist(productList,target_type)
        v_comparison = newproduct["v_comparison"]
        new_total_amt_receivable=0 #记录优惠后的所有参与商品的总应收金额
        isdis=False #是否可以执行优惠
        if comp_symb_type=="ge":
            if v_comparison>=float(value_num):
                isdis=True
        elif comp_symb_type=="g":
            if v_comparison>float(value_num):
                isdis=True
        elif comp_symb_type=="e":
            if v_comparison==float(value_num):
                isdis=True
            elif v_comparison>float(value_num):
                isdis=True
                if target_type == "qtty":
                    newproduct=setproductlist2(newproduct,value_num,target_item)
                    if newproduct["total_amt_receivable"] == 0:
                        return {"keepdis": "N"}

        if isdis:
            if float(newproduct["total_amt_receivable"] - newproduct.get("special_total_amt_receivable", 0)) == 0:
                return {"keepdis": "Y"}
            # 总的应收价减去特例品的价格，才是可以参与促销的总价格
            new_total_amt_receivable = util.CalculationPrice(util.mul(newproduct["total_amt_receivable"] - newproduct.get("special_total_amt_receivable", 0), discount_value))
            # 最后的价格要加上特例品的价格
            new_total_amt_receivable = new_total_amt_receivable + newproduct.get("special_total_amt_receivable", 0)
            newproduct["new_total_amt_receivable"]=float(new_total_amt_receivable)
            newproduct["total_amt_receivable"] = float(new_total_amt_receivable)
            newproduct["keepdis"]="Y"
            return newproduct
        else:
            return {"keepdis": "N"}
    except Exception as e:
        return {}


def multipledis(productList, discount):
    '''
    全场活动多种折扣计算
    :param productList: 参与的商品信息
    :param discount: 全场活动信息
    :return: 返回包含计算得到的新的总应收金额的结果
    '''
    try:
        target_type=discount.target_type
        target_item=discount.target_item
        operation_set=discount.operation_set
        # operation_set = sorted(operation_set, key=lambda x: x["value_num"],reverse=True)
        noperation_set=[]
        operationlen=len(operation_set)
        if operationlen>0:
            for i in range(operationlen):
                noperation_set.append(operation_set[operationlen-1-i])
        newproduct=setproductlist(productList,target_type)
        new_total_amt_receivable=0 #记录优惠后的所有参与商品的总应收金额
        maxoperation_set={}
        for row in noperation_set:
            comp_symb_type=str(row.get("comp_symb_type","ge")).lower() #比较符
            value_num=row.get("value_num",0) #比较值
            v_comparison = newproduct["v_comparison"]
            if comp_symb_type=="ge":
                if v_comparison>=float(value_num):
                    maxoperation_set=row
            elif comp_symb_type=="g":
                if v_comparison>float(value_num):
                    maxoperation_set=row
            elif comp_symb_type=="e":
                if v_comparison==float(value_num):
                    maxoperation_set=row
                elif v_comparison>float(value_num):
                    if target_type == "qtty":
                        newproduct = setproductlist2(newproduct, value_num,target_item)
                    maxoperation_set=row
            if maxoperation_set:
                break
        if maxoperation_set:
            if float(newproduct["total_amt_receivable"] - newproduct.get("special_total_amt_receivable", 0)) == 0:
                return {"keepdis": "Y"}
            discount_value = maxoperation_set.get("discount_value",1)  # 折扣值
            new_total_amt_receivable = util.CalculationPrice(
                util.mul(newproduct["total_amt_receivable"] - newproduct.get("special_total_amt_receivable", 0),
                         discount_value))
            new_total_amt_receivable = new_total_amt_receivable + newproduct.get("special_total_amt_receivable", 0)

            newproduct["new_total_amt_receivable"]=float(new_total_amt_receivable)
            newproduct["total_amt_receivable"] = float(new_total_amt_receivable)
            newproduct["keepdis"]="Y"
            return newproduct
        else:
            return {"keepdis": "N"}
    except Exception as e:
        return {}

def incrementaldis(productList, discount,r_disobj):
    '''
    全场活动递增折扣计算
    :param productList: 参与的商品信息
    :param discount: 全场活动信息
    :return: 返回包含计算得到的新的总应收金额的结果
    '''
    try:
        target_type=discount.target_type
        target_item=discount.target_item
        operation_set = discount.operation_set
        operation_set = sorted(operation_set, key=lambda x: x["value_num"], reverse=True)
        newproduct=setproductlist(productList,target_type)
        v_comparison = newproduct["v_comparison"]
        new_total_amt_receivable=0 #记录优惠后的所有参与商品的总应收金额
        # maxoperation_set={}
        isdis = False
        comp_symb_type = str(operation_set[0].get("comp_symb_type", "ge")).lower()  # 比较符
        value_num = operation_set[0].get("value_num",0)  # 比较值
        if comp_symb_type == "ge":
            if v_comparison >= float(value_num):
                isdis = True
        elif comp_symb_type == "g":
            if v_comparison > float(value_num):
                isdis = True
        elif comp_symb_type == "e":
            if v_comparison == float(value_num):
                isdis = True
            elif v_comparison > float(value_num):
                if target_type == "qtty":
                    newproduct = setproductlist2(newproduct, value_num,target_item)
                    if newproduct["total_amt_receivable"] == 0:
                        return {"keepdis": "N"}
                isdis = True

        if isdis:
            if float(newproduct["total_amt_receivable"] - newproduct.get("special_total_amt_receivable", 0)) == 0:
                # 说明全部都是特例品， 不能参与计算
                return {"keepdis": "Y"}
            new_amt_receivable = 0
            new_amt_receivable_carry = 0
            ifdis=False
            disqty=0
            seat_list = []
            for row in discount.operation_set:
                ifdis = False
                discount_value = row.get("discount_value",1)  # 折扣值
                for row1 in newproduct["disproductList"]:
                    if ifdis and disqty<len(operation_set):
                        break
                    productSeatList = row1.productSeatList
                    if productSeatList:
                        for row2 in productSeatList:
                            if ifdis and disqty<len(operation_set):
                                break
                            if row2.is_discount == "n":
                                continue
                            if not row2.seat:
                                row1.total_amt_receivable=util.CalculationPrice(row1.total_amt_receivable-float(row2.amt_receivable))
                                amt_receivable = float(util.mul(row2.amt_receivable, discount_value))
                                new_amt_receivable += amt_receivable
                                new_amt_receivable_carry += util.CalculationPrice(amt_receivable)
                                row2.amt_receivable = util.CalculationPrice(amt_receivable)
                                row2.seat=True
                                row1.total_amt_receivable = row1.total_amt_receivable + float(row2.amt_receivable)
                                disqty=disqty+1
                                ifdis=True
                                row2.fulldiscounts.append(r_disobj["id"])
                                seat_list.append(row2)
                                # row2.fulldiscountPrice.append(util.CalculationPrice(util.minus(row2.upamt_receivable, row2.amt_receivable)))
                                # row2.upamt_receivable = row2.amt_receivable

                    # new_amt_receivable = new_amt_receivable + float(row1.total_amt_receivable)
            diff = util.CalculationPrice(new_amt_receivable) - new_amt_receivable_carry
            if abs(diff) > 0:
                util.splitDiffPrice(seat_list, diff)
            for seat in seat_list:
                seat.fulldiscountPrice.append(util.minus(seat.upamt_receivable, seat.amt_receivable))
                seat.upamt_receivable = seat.amt_receivable

            new_amt_receivable = 0
            for row3 in newproduct["disproductList"]:
                row_new_amt_receivable = 0
                for seat in row3.productSeatList:
                    row_new_amt_receivable = row_new_amt_receivable + seat.amt_receivable
                row3.total_amt_receivable = row_new_amt_receivable
                new_amt_receivable += row_new_amt_receivable

            newproduct["new_total_amt_receivable"] = util.CalculationPrice(new_amt_receivable)
            newproduct["total_amt_receivable"] = util.CalculationPrice(new_amt_receivable)
            newproduct["total_oldamt_receivable"]=util.CalculationPrice(new_amt_receivable)
            newproduct["isCalculation"]="Y"
            newproduct["keepdis"]="Y"
            return newproduct
        else:
            return {"keepdis": "N"}
    except Exception as e:
        return {}


def getdisbyoriginalpro(discount,originalproductlist):
    type_three = str(discount.prom_type_three).upper()
    target_type = discount.target_type
    target_item = discount.target_item
    operation_set = discount.operation_set
    operation_set = sorted(operation_set, key=lambda x: x["value_num"], reverse=True)
    newproduct = setproductlist1(originalproductlist, target_type)
    v_comparison = newproduct["v_comparison"]
    maxoperation_set = {}
    if type_three == "PA1101":
        # 统一折扣
        operation_set = discount.operation_set[0]
        comp_symb_type = str(operation_set.get("comp_symb_type", "ge")).lower()  # 比较符
        value_num = operation_set.get("value_num", 0)  # 比较值v_comparison = newproduct["v_comparison"]
        iskeepdis = checkdis(comp_symb_type, v_comparison, value_num)
        if iskeepdis:
            return True
        else:
            return False
    elif type_three == "PA1102":
        # 多种折扣
        for row in operation_set:
            comp_symb_type=str(row.get("comp_symb_type","ge")).lower() #比较符
            value_num=row.get("value_num",0) #比较值
            v_comparison = newproduct["v_comparison"]
            if comp_symb_type=="ge":
                if v_comparison>=float(value_num):
                    maxoperation_set=row
            elif comp_symb_type=="g":
                if v_comparison>float(value_num):
                    maxoperation_set=row
            elif comp_symb_type=="e":
                if v_comparison==float(value_num):
                    maxoperation_set=row
                elif v_comparison>float(value_num):
                    maxoperation_set=row
            if maxoperation_set:
                break
        if maxoperation_set:
            return True
        else:
            return False
    elif type_three == "PA1103":
        maxoperation_set = {}
        # 递增折扣
        comp_symb_type = str(operation_set[0].get("comp_symb_type", "ge")).lower()  # 比较符
        value_num = operation_set[0].get("value_num", 0)  # 比较值
        if comp_symb_type == "ge":
            if v_comparison >= float(value_num):
                maxoperation_set = operation_set[:-1]
        elif comp_symb_type == "g":
            if v_comparison > float(value_num):
                maxoperation_set = operation_set[:-1]
        elif comp_symb_type == "e":
            if v_comparison == float(value_num):
                maxoperation_set = operation_set[:-1]
            elif v_comparison > float(value_num):
                maxoperation_set = operation_set[:-1]
        if maxoperation_set:
            return True
        else:
            return False

def setproductlist1(productList,target_type):
    '''
    用原始商品数据判断全场活动是否可保留使用
    :param productList:
    :param target_type:
    :return:
    '''
    t_productl={}
    v_comparison = 0
    total_qtty=0 #记录当前参与该策略的总商品数量
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
    t_productl["v_comparison"]=v_comparison
    return t_productl

def setproductlist(productList,target_type):
    '''
    全场活动执行使用
    :param productList:
    :param target_type:
    :return:
    '''
    t_productl={}
    v_comparison = 0
    total_amt_list=0 #当前参与策略的所有商品的总吊牌金额
    total_amt_retail=0 #当前参与策略的所有商品的总零售金额
    total_amt_receivable=0 #当前参与策略的所有商品的总应收金额
    total_qtty=0 #记录当前参与该策略的总商品数量
    special_total_amt_receivable = 0  # 特例品的总价格
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
        total_amt_list = total_amt_list + float(row.total_amt_list)
        total_amt_retail = total_amt_retail + float(row.total_amt_retail)
        total_amt_receivable = total_amt_receivable + float(row.total_amt_receivable)
        total_qtty = total_qtty + int(row.qtty)
        if row.productSeatList[0].is_discount == "n":
            special_total_amt_receivable = special_total_amt_receivable+float(row.total_amt_receivable)
    t_productl["v_comparison"]=v_comparison
    t_productl["total_amt_list"]=total_amt_list
    t_productl["total_amt_retail"]=total_amt_retail
    t_productl["total_amt_receivable"]=total_amt_receivable #参与策略的总应收金额
    t_productl["special_total_amt_receivable"] = special_total_amt_receivable
    t_productl["total_oldamt_receivable"] = total_amt_receivable
    t_productl["total_qtty"]=total_qtty
    return t_productl

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