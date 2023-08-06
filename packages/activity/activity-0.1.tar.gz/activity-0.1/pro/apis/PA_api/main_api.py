# -*- coding:utf-8 -*-
# author:何小霞
# datetime:2018/9/28 10:28

from pro.apis.entitys.PA_entitys.promotion_entity import PromotionEntity
import copy
import pro.utils.util as util
from pro.apis.PA_api.DC_api.dc_main import executediscount
from pro.apis.PA_api.DC_api.dc_main import getdisbyoriginalpro
from pro.utils.linq import linq
from pro.apis.PA_api.BG_api.bg_main import *
from pro.utils.util import all_for_one
from pro.utils.util import CalculationPrice
from pro.apis.PA_api.PE_api.pe_main import *
from pro.apis.PA_api.FS_api.fs_main import *
from pro.apis.PA_api.CP_api.cp_main import *


def executefullactivity(productListDiscount, discount_list, userInfo, product_activity_list, originalproductlist,
                        gabg=None, fullgit_disgroup=None, product_cp=None):
    '''
    全场活动执行总入口
    :param productListDiscount: 经过执行商品活动后的的商品集合
    :param discount_list: 全场活动集合
    :param userInfo:VIP信息
    :param product_activity_list:商品活动
    :return:
    '''
    alldis = []  # 可保留的所有全场活动
    products = []  # 反参需要的商品明细结构
    optimal_dis = []
    swap_products = []
    buygifts = []  # 保留所有执行过的全场买赠活动
    dis_proitems = []  # 记录商品参与促销情况
    rownum = 0
    discount_id=[]
    after_alldis_pro = []  # 记录所有参与策略后的对象集合
    # 创建折扣的模板
    DiscountList = []
    productListDiscount = sorted(productListDiscount, key=lambda x: x.rownum)

    for bean in discount_list:
        DiscountList.append(PromotionEntity(bean))

    # 将策略按照二类执行顺序进行升序排序(执行顺序值越小，优先级越高)
    DiscountList = sorted(DiscountList, key=lambda x: (x.prom_type_two_c, -x.publish_date))
    for row in DiscountList:
        discount_id.append(row.id)
    # 将可返回的商品活动筛选到alldis对象中
    getgadis(productListDiscount, alldis, product_activity_list, gabg)
    # 第一步筛选：将商品进行参与策略和不参与策略分组
    new_products = getproductlists(productListDiscount)

    if not new_products.get("dis_products"):
        # 将商品活动执行后传入的商品结果重组成返回给前端的结构
        products = getreturnprovalue(copy.deepcopy(productListDiscount), [])
        optimal_dis = getreturndisvalue(copy.deepcopy(productListDiscount), [], product_activity_list, discount_list)
        dis_proitems = getreturnprodisvalue(copy.deepcopy(productListDiscount), [], product_activity_list,
                                            discount_list)
        swap_products = getcpproducts(product_cp, [])
        fullgit_dis = getreturnbgpro(copy.deepcopy(productListDiscount), [], product_activity_list, discount_list,
                                     optimal_dis, gabg)
        fullgit_disgroup = getreturnbgtwo(fullgit_disgroup)
        # 用原始数据再筛选一次
        getpadis(copy.deepcopy(originalproductlist), alldis, copy.deepcopy(DiscountList), userInfo)
        return {"products": products, "swap_products": swap_products, "optimal_dis": optimal_dis, "alldis": alldis,
                "dis_proitems": dis_proitems, "fullgit_dis": fullgit_dis,
                "fullgit_disgroup": fullgit_disgroup}  # 表示没有可参与全场活动的商品

    dis_products = []  # 参与计算的商品明细
    nodis_products = []  # 不参与计算的商品明细
    new_nodis_pro = []
    updis_products = []  # 记录本次策略可以与下个策略叠加执行时本次策略的执行后的商品明细
    up_after_dis_pro = {}  # 记录上个策略执行后的商品信息

    dis_products = new_products.get("dis_products")  # 可参与策略的商品明细
    nodis_products = new_products.get("nodis_products")  # 不可参与策略的商品明细
    pabg = []
    gifts_ecodes = []
    for row_item in DiscountList:
        rownum=DiscountList.index(row_item)
        # 判断当前活动是否限制会员并且当前用户可否参与
        if row_item.members_only:
            if userInfo.id is not None and userInfo.discount is not None:
                # 当前用户会员级别不再此活动会员级别范围之内
                if userInfo.id not in row_item.members_group:
                    continue
            # 当前活动限制会员参加 且 当前用户不是会员
            else:
                continue

        # 第二步筛选：将可参与策略的商品进行策略条件的筛选
        r_dis_products = copy.deepcopy(dis_products)
        if updis_products:
            r_dis_products = copy.deepcopy(updis_products)
            # updis_products = []

        new_dis_products = getproductliststwo(r_dis_products, row_item)
        new_dis_pro = new_dis_products.get("dis_products", [])
        new_nodis_pro = new_dis_products.get("nodis_products", [])
        after_dis_pro = {}  # 接收经过计算后的商品信息

        r_disobj = {"id": row_item.id, "ename": row_item.ename, "type_one": "PA", "type_two": row_item.prom_type_two,
                    "type_three": row_item.prom_type_three, "publish_date": row_item.publish_date}

        nowaddprodis = True  # 标记本次执行结果是否添加到最后执行结果集里
        if not new_dis_pro:
            if not new_dis_pro:
                # 用原始数据再筛选一次
                getpadis(copy.deepcopy(originalproductlist), alldis, copy.deepcopy(DiscountList), userInfo, row_item)
                if after_alldis_pro != []:
                    after_alldis_pro = sorted(after_alldis_pro, key=lambda x: x['total_amt_receivable'], reverse=False)
                    if row_item.prom_type_two == 6:
                        disrow = copy.deepcopy(copy.deepcopy(after_alldis_pro[0]))
                    else:
                        disrow = copy.deepcopy(util.calculation(copy.deepcopy(after_alldis_pro[0])))
                    for r_row in disrow["productList"]:
                        disrow["disproductList"].append(r_row)
                    updis_products = disrow["disproductList"]
                # if row_item.prom_type_two == 5 and buygifts:
                #     if len(buygifts) == 1 and "buygift" in buygifts[0].keys():
                #         disrow = copy.deepcopy(copy.deepcopy(buygifts[0]))
                #         for r_row in disrow["productList"]:
                #             disrow["disproductList"].append(r_row)
                #         updis_products = disrow["disproductList"]
                #     else:
                #         if "buygift" in buygifts[-1].keys():
                #             disrow = copy.deepcopy(copy.deepcopy(buygifts[-1]))
                #             for r_row in disrow["productList"]:
                #                 disrow["disproductList"].append(r_row)
                #             updis_products = disrow["disproductList"]
                #         else:
                #             for i in range(0, len(buygifts)):
                #                 if "buygift" in buygifts[i].keys() and "purchase" in buygifts[i + 1].keys():
                #                     disrow = copy.deepcopy(copy.deepcopy(buygifts[i]))
                #                     for r_row in disrow["productList"]:
                #                         disrow["disproductList"].append(r_row)
                #                     updis_products = disrow["disproductList"]
                #                     break
                continue

        # 对于当前全场活动不能与其它全场活动同时执行并且上一个全场或也不能与其它全场活动同时执行，那么当前活动不执行
        if rownum > 0 and rownum <= len(DiscountList) - 1:
            ids = []
            for row_dis in r_dis_products:
                if len(row_dis.fulldiscountID)>len(ids):
                    ids=row_dis.fulldiscountID
            if ids:
                id = ids[-1]
                num = discount_id.index(id)
                if (row_item.prom_type_two_code != DiscountList[num].prom_type_two_code):
                    if (DiscountList[num].is_run_store_act).upper() != "Y":
                        getpadis(copy.deepcopy(originalproductlist), alldis, copy.deepcopy(DiscountList), userInfo,
                                 row_item)
                        updis_products=r_dis_products
                        continue


        #修改上一次优惠后的金额
        for row1 in new_dis_pro:
            row1.upamt_receivable = row1.amt_receivable

        type_three = str(row_item.prom_type_three).upper()
        if type_three == "PA1101" or type_three == "PA1102" or type_three == "PA1103":
            # 统一折扣、多种折扣、递增折扣
            after_dis_pro = executediscount(copy.deepcopy(new_dis_pro), row_item, userInfo, r_disobj)
        elif type_three == "PA1201" or type_three == "PA1202":
            # 统一减现、梯度减现
            after_dis_pro = executemoneyback(copy.deepcopy(new_dis_pro), row_item, userInfo, r_disobj)
        elif type_three == "PA1301" or type_three == "PA1302" or type_three == "PA1303" or type_three == "PA1304" or type_three == "PA1601" or type_three == "PA1701" or type_three == "PA1602" or type_three == "PA1702":
            # 统一买赠、梯度买赠、统一送券、梯度送券、线上/线上排名统一买赠、线上/线上排名梯度买赠
            after_dis_pro = executebuygifts(copy.deepcopy(new_dis_pro), row_item, userInfo, new_nodis_pro)
        elif type_three == "PA1401" or type_three == "PA1402" or type_three == "PA1403":
            # 统一特价换购、统一打折换购，统一优惠换购
            after_dis_pro = executeredemption(copy.deepcopy(new_dis_pro), row_item, userInfo, new_nodis_pro)
        elif type_three == "PA1501":
            # 买免
            after_dis_pro = executemaimian(copy.deepcopy(new_dis_pro), row_item, userInfo)

        if after_dis_pro.get("keepdis", "Y") == "Y":
            alldis.append(r_disobj)
        else:
            # 用原始数据再筛选一次
            getpadis(copy.deepcopy(originalproductlist), alldis, copy.deepcopy(DiscountList), userInfo, row_item)
        if "bg" in after_dis_pro:
            pabg.append(after_dis_pro["bg"])
        if "gifts_ecodes" in after_dis_pro and "buygift" in after_dis_pro:
            gifts_ecodes = after_dis_pro["gifts_ecodes"]
        if after_dis_pro and after_dis_pro.get("disproductList"):
            after_dis_pro = mergepro(after_dis_pro, new_nodis_pro)
            if type_three == "PA1301" or type_three == "PA1302" or type_three == "PA1303" or type_three == "PA1304":
                if after_dis_pro.get("keepdis", "Y") == "Y":
                    buygifts.append(after_dis_pro)
            if type_three == "PA1401" or type_three == "PA1402" or type_three == "PA1403":
                if after_dis_pro.get("keepdis", "Y") == "Y":
                    buygifts.append(after_dis_pro)
            # if not up_after_dis_pro:
            #     up_after_dis_pro = copy.deepcopy(after_dis_pro)
            # else:
            if rownum > 0 and up_after_dis_pro:
                if row_item.prom_type_two_code == DiscountList[rownum - 1].prom_type_two_code :
                    total_amt_receivable = float(after_dis_pro["total_amt_receivable"])
                    up_total_amt_receivable = float(up_after_dis_pro["total_amt_receivable"])
                    give_max_pronum =0
                    give_max_amtlist =0
                    up_give_max_pronum = 0
                    up_give_max_amtlist = 0
                    give_max_pronum = after_dis_pro.get("give_max_pronum",0)
                    give_max_amtlist = after_dis_pro.get("give_max_amtlist",0)
                    up_give_max_pronum = up_after_dis_pro.get("give_max_pronum",0)
                    up_give_max_amtlist = up_after_dis_pro.get("give_max_amtlist",0)
                    if total_amt_receivable < up_total_amt_receivable:
                        #对于没有录入任何赠送商品的赠品活动是当没有执行了，那么不需要进入择优里
                        if (str(row_item.prom_type_two) == "4" and give_max_pronum==0 and give_max_amtlist==0) or (str(row_item.prom_type_two) == "5" and after_dis_pro.get("ishavepurchaselist",False)==False):
                            nowaddprodis = False
                        else:
                            if up_after_dis_pro in after_alldis_pro:
                                after_alldis_pro.remove(up_after_dis_pro)
                            # up_after_dis_pro = copy.deepcopy(after_dis_pro)
                    elif total_amt_receivable > up_total_amt_receivable:
                        nowaddprodis = False
                    else:
                        #对于没有录入任何赠送商品的赠品活动是当没有执行了，那么不需要进入择优里
                        if (str(row_item.prom_type_two) == "4" and give_max_pronum==0 and give_max_amtlist==0) or (str(row_item.prom_type_two) == "5" and after_dis_pro.get("ishavepurchaselist",False)==False):
                            nowaddprodis = False
                        else:
                            if str(row_item.prom_type_two) == "4" and (give_max_pronum>up_give_max_pronum or give_max_amtlist > up_give_max_amtlist):
                                if up_after_dis_pro in after_alldis_pro:
                                    after_alldis_pro.remove(up_after_dis_pro)
                                # up_after_dis_pro = copy.deepcopy(after_dis_pro)
                            else:
                                # 比较促销的发布时间，发布时间靠前的则取该促销执行结果
                                if int(row_item.publish_date) > int(DiscountList[rownum - 1].publish_date):
                                    if up_after_dis_pro in after_alldis_pro:
                                        after_alldis_pro.remove(up_after_dis_pro)
                                    # up_after_dis_pro = copy.deepcopy(after_dis_pro)
                                else:
                                    nowaddprodis = False
            else:
                give_max_pronum = 0
                give_max_amtlist = 0
                give_max_pronum = after_dis_pro.get("give_max_pronum", 0)
                give_max_amtlist = after_dis_pro.get("give_max_amtlist", 0)
                #对于没有录入任何赠送商品的赠品活动是当没有执行了，那么不需要进入择优里
                if (str(row_item.prom_type_two) == "4" and give_max_pronum == 0 and give_max_amtlist == 0)  or (str(row_item.prom_type_two) == "5" and after_dis_pro.get("ishavepurchaselist",False)==False):
                    nowaddprodis = False
            if rownum==0 or (not up_after_dis_pro):
                up_after_dis_pro = copy.deepcopy(after_dis_pro)
            else:
                if nowaddprodis:
                    up_after_dis_pro = copy.deepcopy(after_dis_pro)
            if rownum < len(DiscountList) - 1:
                if (row_item.is_run_store_act).upper() == "Y" or (
                        DiscountList[rownum + 1].is_run_store_act).upper() == "Y":
                    if row_item.prom_type_two_code != DiscountList[rownum + 1].prom_type_two_code:
                        after_alldis_pro.append(copy.deepcopy(after_dis_pro))
                        if after_alldis_pro:
                            after_alldis_pro = sorted(after_alldis_pro, key=lambda x: x['total_amt_receivable'],
                                                      reverse=False)
                            # 本次策略是可以与其它全场活动同时执行，并且下个全场活动和本次活动不属于同二类，所以可以叠加执行
                            # 将本次的执行结果首先进行分摊等计算处理，然后使用本次执行后的结果来作为后面策略的原始数据 (本次版本中只做折扣，所以暂不会存在不会存在)
                            if after_alldis_pro[0].get("isCalculation", "N") == "N":
                                disrow = copy.deepcopy(util.calculation(copy.deepcopy(after_dis_pro)))
                            else:
                                disrow = copy.deepcopy(copy.deepcopy(after_dis_pro))
                            for r_row in disrow["productList"]:
                                disrow["disproductList"].append(r_row)
                            updis_products = disrow["disproductList"]
                    else:
                        if nowaddprodis:
                            after_alldis_pro.append(copy.deepcopy(after_dis_pro))

                else:
                    if nowaddprodis:
                        after_alldis_pro.append(copy.deepcopy(after_dis_pro))
                    if row_item.prom_type_two_code != DiscountList[rownum + 1].prom_type_two_code:
                        if after_alldis_pro[-1].get("isCalculation", "N") == "N":
                            disrow = copy.deepcopy(util.calculation(copy.deepcopy(after_alldis_pro[-1])))
                        else:
                            disrow = copy.deepcopy(copy.deepcopy(after_alldis_pro[-1]))
                        for r_row in disrow["productList"]:
                            disrow["disproductList"].append(r_row)
                        updis_products = disrow["disproductList"]
            else:
                if nowaddprodis:
                    after_alldis_pro.append(copy.deepcopy(after_dis_pro))
        rownum = rownum + 1

    # 筛选出最优惠的那个执行对象
    if after_alldis_pro:
        minamt = 0
        give_max_pronum=0
        give_max_amtlist=0
        mindisrow = {}
        len1 = len(after_alldis_pro)
        for i in range(len1):
            if i == 0:
                minamt = float(after_alldis_pro[i]["total_amt_receivable"])
                give_max_pronum=after_alldis_pro[i].get("give_max_pronum",0)
                give_max_amtlist=after_alldis_pro[i].get("give_max_amtlist",0)
                mindisrow = after_alldis_pro[i]
            else:
                if minamt > float(after_alldis_pro[i]["total_amt_receivable"]):
                    minamt = float(after_alldis_pro[i]["total_amt_receivable"])
                    give_max_pronum=after_alldis_pro[i].get("give_max_pronum",0)
                    give_max_amtlist=after_alldis_pro[i].get("give_max_amtlist",0)
                    mindisrow = after_alldis_pro[i]
                else:
                    if give_max_pronum<after_alldis_pro[i].get("give_max_pronum",0) or give_max_amtlist<after_alldis_pro[i].get("give_max_amtlist",0):
                        minamt = float(after_alldis_pro[i]["total_amt_receivable"])
                        give_max_pronum = after_alldis_pro[i].get("give_max_pronum", 0)
                        give_max_amtlist = after_alldis_pro[i].get("give_max_amtlist", 0)
                        mindisrow = after_alldis_pro[i]


        if mindisrow:
            if mindisrow.get("isCalculation", "N") == "N":
                # 将mindisrow结果里的商品明细进行分摊计算
                mindisrow = util.calculation(copy.deepcopy(mindisrow))
            # if buygifts != []:
            #     all_for_one(mindisrow["disproductList"], buygifts, gifts_ecodes, mindisrow["productList"])
            # 将mindisrow结果重组成返回给前端的结构
            products = getreturnprovalue(copy.deepcopy(mindisrow["disproductList"]), [])
            swap_products = getcpproducts(product_cp, buygifts)
            optimal_dis = getreturndisvalue(copy.deepcopy(mindisrow["disproductList"]), [], product_activity_list,
                                            discount_list)
            dis_proitems = getreturnprodisvalue(copy.deepcopy(mindisrow["disproductList"]), [], product_activity_list,
                                                discount_list)
            products = getreturnprovalue(copy.deepcopy(mindisrow["productList"]), products)
            optimal_dis = getreturndisvalue(copy.deepcopy(mindisrow["productList"]), optimal_dis,
                                            product_activity_list,
                                            discount_list)
            dis_proitems = getreturnprodisvalue(copy.deepcopy(mindisrow["productList"]), dis_proitems,
                                                product_activity_list, discount_list)
            products = getreturnprovalue(copy.deepcopy(nodis_products), products)
            optimal_dis = getreturndisvalue(copy.deepcopy(nodis_products), optimal_dis,
                                            product_activity_list,
                                            discount_list)
            dis_proitems = getreturnprodisvalue(copy.deepcopy(nodis_products), dis_proitems,
                                                product_activity_list, discount_list)

        else:
            if buygifts != []:
                all_for_one(productListDiscount, buygifts, gifts_ecodes)
            # 将商品活动执行后传入的商品结果重组成返回给前端的结构
            products = getreturnprovalue(copy.deepcopy(productListDiscount), [])
            swap_products = getcpproducts(product_cp, buygifts)
            optimal_dis = getreturndisvalue(copy.deepcopy(productListDiscount), [], product_activity_list,
                                            discount_list)
    else:
        if buygifts != []:
            all_for_one(productListDiscount, buygifts, gifts_ecodes)
        # 将商品活动执行后传入的商品结果重组成返回给前端的结构
        products = getreturnprovalue(copy.deepcopy(productListDiscount), [])
        swap_products = getcpproducts(product_cp, buygifts)
        optimal_dis = getreturndisvalue(copy.deepcopy(productListDiscount), [], product_activity_list, discount_list)
        dis_proitems = getreturnprodisvalue(copy.deepcopy(productListDiscount), [], product_activity_list,
                                            discount_list)

    fullgit_dis = getreturnbgpro(copy.deepcopy(productListDiscount), [], product_activity_list, discount_list,
                                 optimal_dis, gabg, pabg)
    fullgit_disgroup = getreturnbgtwo(fullgit_disgroup)

    # setdisamt(optimal_dis,"optimal_dis")
    # setdisamt(dis_proitems, "dis_proitems")

    return {"products": products, "swap_products": swap_products, "optimal_dis": optimal_dis, "alldis": alldis,
            "dis_proitems": dis_proitems, "fullgit_dis": fullgit_dis, "fullgit_disgroup": fullgit_disgroup}

def setdisamt(disproitem,input_type):
    for row in disproitem:
        if input_type=="optimal_dis":
            row["disamt"]=CalculationPrice(row["disamt"])
        elif input_type=="dis_proitems":
            row["dis_amt"] = CalculationPrice(row["dis_amt"])

def set_updisproduct(after_alldis_pro,row_item,buygifts):
    updis_products=[]
    if after_alldis_pro != []:
        after_alldis_pro = sorted(after_alldis_pro, key=lambda x: x['total_amt_receivable'],
                                  reverse=False)
        if row_item.prom_type_two == 6:
            disrow = copy.deepcopy(copy.deepcopy(after_alldis_pro[0]))
        else:
            disrow = copy.deepcopy(util.calculation(copy.deepcopy(after_alldis_pro[0])))
        for r_row in disrow["productList"]:
            disrow["disproductList"].append(r_row)
        updis_products = disrow["disproductList"]
    if row_item.prom_type_two == 5 and buygifts:
        if len(buygifts) == 1 and "buygift" in buygifts[0].keys():
            disrow = copy.deepcopy(copy.deepcopy(buygifts[0]))
            for r_row in disrow["productList"]:
                disrow["disproductList"].append(r_row)
            updis_products = disrow["disproductList"]
        else:
            if "buygift" in buygifts[-1].keys():
                disrow = copy.deepcopy(copy.deepcopy(buygifts[-1]))
                for r_row in disrow["productList"]:
                    disrow["disproductList"].append(r_row)
                updis_products = disrow["disproductList"]
            else:
                for i in range(0, len(buygifts)):
                    if "purchase" in buygifts[-1].keys():
                        disrow = copy.deepcopy(copy.deepcopy(buygifts[i]))
                        for r_row in disrow["productList"]:
                            disrow["disproductList"].append(r_row)
                        updis_products = disrow["disproductList"]
                        break
    return updis_products


def getgadis(productListDiscount, alldis, product_activity_list, gabg=None):
    '''
    重组可返回的商品活动
    :param productListDiscount: 执行过商品活动的商品结构
    :param alldis:存放返回的所有可用策略
    :param product_activity_list:商品活动集合
    :return:
    '''
    for row in productListDiscount:
        if not row.discountId:
            continue
        for row1 in row.discountId:
            row_dis = linq(product_activity_list).where(lambda x: x["id"] == row1).tolist().copy()
            nrow_dis = row_dis[0]
            new_dis = {"id": nrow_dis.get("id", ""), "ename": nrow_dis.get("ename", ""),
                       "type_one": "GA", "type_two": nrow_dis.get("prom_type_two", ""),
                       "type_three": nrow_dis.get("prom_type_three", ""),
                       "publish_date": nrow_dis.get("publish_date", "")}
            if not row_dis:
                continue
            if alldis:
                newrowdis = linq(alldis).where(lambda x: x["id"] == row1).tolist()
                if not newrowdis:
                    alldis.append(new_dis)
            else:
                alldis.append(new_dis)
    if gabg:
        for buygift in gabg:
            for row2 in product_activity_list:
                if buygift['id'] == row2['id']:
                    new_dis = {"id": row2.get("id", ""), "ename": row2.get("ename", ""),
                               "type_one": "GA", "type_two": row2.get("prom_type_two", ""),
                               "type_three": row2.get("prom_type_three", ""),
                               "publish_date": row2.get("publish_date", "")}
                    if new_dis not in alldis:
                        alldis.append(new_dis)


def getpadis(originalproductlist, alldis, discount_list, userInfo, disitem={}):
    '''
    重组可返回的商品活动
    :param productListDiscount: 执行过商品活动的商品结构
    :param alldis:存放返回的所有可用策略
    :param product_activity_list:商品活动集合
    :return:
    '''
    for row_item in discount_list:
        if disitem and disitem.id != row_item.id:
            continue

        # 判断当前活动是否限制会员并且当前用户可否参与
        if row_item.members_only:
            if userInfo.id is not None and userInfo.discount is not None:
                # 当前用户会员级别不再此活动会员级别范围之内
                if userInfo.id not in row_item.members_group:
                    continue
            # 当前活动限制会员参加 且 当前用户不是会员
            else:
                continue
        r_disobj = {"id": row_item.id, "ename": row_item.ename, "type_one": "PA", "type_two": row_item.prom_type_two,
                    "type_three": row_item.prom_type_three, "publish_date": row_item.publish_date}
        new_dis_products = getproductliststwo(originalproductlist, row_item)
        new_dis_pro = new_dis_products.get("dis_products", [])
        if not new_dis_pro:
            continue
        # 判断执行条件是否符合
        if row_item.prom_type_two == 1:
            if getdisbyoriginalpro(row_item, copy.deepcopy(new_dis_pro)):
                alldis.append(r_disobj)
        if row_item.prom_type_two == 2:
            if getfsbyoriginalpro(row_item, copy.deepcopy(new_dis_pro)):
                alldis.append(r_disobj)
        if row_item.prom_type_two == 4:
            if getbgbyoriginalpro(row_item, copy.deepcopy(new_dis_pro)):
                alldis.append(r_disobj)
        if row_item.prom_type_two == 5:
            if getcpbyoriginalpro(row_item, copy.deepcopy(new_dis_pro)):
                alldis.append(r_disobj)
        if row_item.prom_type_two == 6:
            if getpebyoriginalpro(row_item, copy.deepcopy(new_dis_pro)):
                alldis.append(r_disobj)


def getproductlists(productListDiscount):
    '''
    第一步筛选：将传入的商品明细进行可参与全场策略和不可参与全场策略的分组
    :param productListDiscount:
    :return:
    '''
    new_products = {}
    dis_products = []  # 参与计算的商品明细
    nodis_products = []  # 不参与计算的商品明细
    for row in productListDiscount:
        productSeatList = row.productSeatList
        new_disrowpro = {}
        new_nodisrowpro = {}
        total_amt_list = 0
        total_amt_retail = 0
        total_amt_receivable = 0
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
            for row_i in productSeatList:
                row_i.amt_receivable = float("%.2f" % round(float(util.add(row_i.amt_receivable, 0.001)), 2))
                if row_i.is_run_store_act and row_i.is_buy_gifts != "y":
                    new_disrowpro.productSeatList.append(row_i)
                    new_disrowpro.qtty = new_disrowpro.qtty + 1
                    total_amt_list = total_amt_list + float(row_i.amt_list)
                    total_amt_retail = total_amt_retail + float(row_i.amt_retail)
                    total_amt_receivable = total_amt_receivable + float(row_i.amt_receivable)
                else:
                    new_nodisrowpro.productSeatList.append(row_i)
                    new_nodisrowpro.qtty = new_nodisrowpro.qtty + 1
                    total_amt_listnodis = total_amt_listnodis + float(row_i.amt_list)
                    total_amt_retailnodis = total_amt_retailnodis + float(row_i.amt_retail)
                    total_amt_receivablenodis = total_amt_receivablenodis + float(row_i.amt_receivable)
        if new_disrowpro.productSeatList:
            # 吊牌金额
            new_disrowpro.total_amt_list = total_amt_list
            # 零售金额
            new_disrowpro.total_amt_retail = total_amt_retail
            # 应收金额
            new_disrowpro.total_amt_receivable = total_amt_receivable
            dis_products.append(new_disrowpro)
        if new_nodisrowpro.productSeatList:
            # 吊牌金额
            new_nodisrowpro.total_amt_list = total_amt_listnodis
            # 零售金额
            new_nodisrowpro.total_amt_retail = total_amt_retailnodis
            # 应收金额
            new_nodisrowpro.total_amt_receivable = total_amt_receivablenodis
            nodis_products.append(new_nodisrowpro)
    new_products["dis_products"] = dis_products  # 可参与全场策略
    new_products["nodis_products"] = nodis_products  # 不可参与全场策略
    return new_products


def getproductliststwo(productList, dis):
    '''
    第二步筛选：从可参与全场促销的商品中筛选出可参与当前全场活动的商品
    :param productList:商品
    :param dis:全场活动
    :return:
    '''
    new_products = {}
    dis_products = []  # 可参与计算的商品明细
    nodis_products = []  # 不可参与计算的商品明细

    for row in productList:
        row_prodSeat = row.productSeatList
        if dis.target_item == "amt_receivable":
            row_prodSeat = sorted(row_prodSeat, key=lambda x: x.amt_receivable, reverse=True)  # 按照应收价格降序
        elif dis.target_item == "amt_list":
            row_prodSeat = sorted(row_prodSeat, key=lambda x: x.amt_list, reverse=True)  # 按照吊牌价格降序
        else:
            row_prodSeat = sorted(row_prodSeat, key=lambda x: x.amt_retail, reverse=True)  # 按照零售价格降序
        new_disrowpro = {}
        new_nodisrowpro = {}
        total_amt_list = 0
        total_amt_retail = 0
        total_amt_receivable = 0
        total_amt_listnodis = 0
        total_amt_retailnodis = 0
        total_amt_receivablenodis = 0
        give_max_pronum=0
        give_max_amtlist=0
        give_max_pronumnodis = 0
        give_max_amtlistnodis = 0
        if row_prodSeat:
            new_disrowpro = copy.deepcopy(row)
            new_nodisrowpro = copy.deepcopy(row)
            new_disrowpro.productSeatList = []
            new_disrowpro.qtty = 0
            new_nodisrowpro.productSeatList = []
            new_nodisrowpro.qtty = 0
            for row_i in row_prodSeat:
                v_comparison = 0
                if dis.specific_target_type == "amt_receivable":
                    # 按应收价比较
                    v_comparison = float(row_i.amt_receivable)
                elif dis.specific_target_type == "discount":
                    # 按折扣比较
                    v_comparison = round(float(util.add(util.div(row_i.amt_receivable, row_i.amt_list), 0.001)), 2)
                if dis.comp_symb_type == "ge":
                    # 大于等于
                    if v_comparison >= float(dis.value_num)  and row_i.is_run_store_act:
                        if dis.prom_type_two != 4:
                            if dis.target_item == "amt_retail":
                                row_i.amt_receivable = row_i.amt_retail
                            elif dis.target_item == "amt_list":
                                row_i.amt_receivable = row_i.amt_list
                        row_i.upamt_receivable = row_i.amt_receivable
                        new_disrowpro.productSeatList.append(row_i)
                        new_disrowpro.qtty = new_disrowpro.qtty + row_i.qtty
                        total_amt_list = total_amt_list + float(row_i.amt_list)
                        total_amt_retail = total_amt_retail + float(row_i.amt_retail)
                        total_amt_receivable = total_amt_receivable + float(row_i.amt_receivable)
                        if row_i.is_buy_gifts=='y':
                            give_max_pronum=give_max_pronum+1
                            give_max_amtlist=give_max_amtlist+float(row_i.amt_list)
                    else:
                        new_nodisrowpro.productSeatList.append(row_i)
                        new_nodisrowpro.qtty = new_nodisrowpro.qtty + row_i.qtty
                        total_amt_listnodis = total_amt_listnodis + float(row_i.amt_list)
                        total_amt_retailnodis = total_amt_retailnodis + float(row_i.amt_retail)
                        total_amt_receivablenodis = total_amt_receivablenodis + float(row_i.amt_receivable)
                        if row_i.is_buy_gifts=='y':
                            give_max_pronumnodis=give_max_pronumnodis+1
                            give_max_amtlistnodis=give_max_amtlistnodis+float(row_i.amt_list)
                elif dis.comp_symb_type == "g":
                    # 大于
                    if v_comparison > float(dis.value_num)  and row_i.is_run_store_act :
                        if dis.prom_type_two != 4:
                            if dis.target_item == "amt_retail":
                                row_i.amt_receivable = row_i.amt_retail
                            elif dis.target_item == "amt_list":
                                row_i.amt_receivable = row_i.amt_list
                        row_i.upamt_receivable = row_i.amt_receivable
                        new_disrowpro.productSeatList.append(row_i)
                        new_disrowpro.qtty = new_disrowpro.qtty + row_i.qtty
                        total_amt_list = total_amt_list + float(row_i.amt_list)
                        total_amt_retail = total_amt_retail + float(row_i.amt_retail)
                        total_amt_receivable = total_amt_receivable + float(row_i.amt_receivable)
                        if row_i.is_buy_gifts=='y':
                            give_max_pronum=give_max_pronum+1
                            give_max_amtlist=give_max_amtlist+float(row_i.amt_list)
                    else:
                        new_nodisrowpro.productSeatList.append(row_i)
                        new_nodisrowpro.qtty = new_nodisrowpro.qtty + row_i.qtty
                        total_amt_listnodis = total_amt_listnodis + float(row_i.amt_list)
                        total_amt_retailnodis = total_amt_retailnodis + float(row_i.amt_retail)
                        total_amt_receivablenodis = total_amt_receivablenodis + float(row_i.amt_receivable)
                        if row_i.is_buy_gifts=='y':
                            give_max_pronumnodis=give_max_pronumnodis+1
                            give_max_amtlistnodis=give_max_amtlistnodis+float(row_i.amt_list)
                elif dis.comp_symb_type == "e":
                    # 等于
                    if v_comparison >= float(dis.value_num)  and row_i.is_run_store_act:
                        if dis.prom_type_two != 4 :
                            if dis.target_item == "amt_retail":
                                row_i.amt_receivable = row_i.amt_retail
                            elif dis.target_item == "amt_list":
                                row_i.amt_receivable = row_i.amt_list
                        row_i.upamt_receivable = row_i.amt_receivable
                        new_disrowpro.productSeatList.append(row_i)
                        new_disrowpro.qtty = new_disrowpro.qtty + row_i.qtty
                        total_amt_list = total_amt_list + float(row_i.amt_list)
                        total_amt_retail = total_amt_retail + float(row_i.amt_retail)
                        total_amt_receivable = total_amt_receivable + float(row_i.amt_receivable)
                        if row_i.is_buy_gifts=='y':
                            give_max_pronum=give_max_pronum+1
                            give_max_amtlist=give_max_amtlist+float(row_i.amt_list)
                    else:
                        new_nodisrowpro.productSeatList.append(row_i)
                        new_nodisrowpro.qtty = new_nodisrowpro.qtty + row_i.qtty
                        total_amt_listnodis = total_amt_listnodis + float(row_i.amt_list)
                        total_amt_retailnodis = total_amt_retailnodis + float(row_i.amt_retail)
                        total_amt_receivablenodis = total_amt_receivablenodis + float(row_i.amt_receivable)
                        if row_i.is_buy_gifts=='y':
                            give_max_pronumnodis=give_max_pronumnodis+1
                            give_max_amtlistnodis=give_max_amtlistnodis+float(row_i.amt_list)
        if new_disrowpro.productSeatList:
            new_disrowpro.amt_list = new_disrowpro.productSeatList[0].amt_list  # 吊牌价格
            new_disrowpro.amt_retail = new_disrowpro.productSeatList[0].amt_retail  # 零售价格
            new_disrowpro.amt_receivable = new_disrowpro.productSeatList[0].amt_receivable  # 计算的价格（默认应收价格）
            new_disrowpro.total_amt_list = total_amt_list  # 吊牌金额
            new_disrowpro.total_amt_retail = total_amt_retail  # 零售金额
            new_disrowpro.total_amt_receivable = total_amt_receivable  # 应收金额
            new_disrowpro.give_max_pronum=give_max_pronum
            new_disrowpro.give_max_amtlist=give_max_amtlist
            dis_products.append(new_disrowpro)
        if new_nodisrowpro.productSeatList:
            new_nodisrowpro.amt_list = new_nodisrowpro.productSeatList[0].amt_list  # 吊牌价格
            new_nodisrowpro.amt_retail = new_nodisrowpro.productSeatList[0].amt_retail  # 零售价格
            new_nodisrowpro.amt_receivable = new_nodisrowpro.productSeatList[0].amt_receivable  # 应收价格
            new_nodisrowpro.total_amt_list = total_amt_listnodis  # 吊牌金额
            new_nodisrowpro.total_amt_retail = total_amt_retailnodis  # 零售金额
            new_nodisrowpro.total_amt_receivable = total_amt_receivablenodis  # 应收金额
            new_nodisrowpro.give_max_pronum=give_max_pronumnodis
            new_nodisrowpro.give_max_amtlist=give_max_amtlistnodis
            nodis_products.append(new_nodisrowpro)
    new_products["dis_products"] = dis_products  # 可参与该全场策略的
    new_products["nodis_products"] = nodis_products  # 不可参与该全场策略的
    return new_products


def mergepro(after_dis_pro, new_nodis_pro):
    '''
    将没有参与全场活动的商品合并到参与计算后的对象结构中
    :param after_dis_pro:
    :param new_nodis_pro:
    :param nodis_products:
    :return:
    '''
    total_amt_list = 0  # 所有商品的总吊牌金额
    total_amt_retail = 0  # 所有商品的总零售金额
    total_amt_receivable = 0  # 所有商品的总应收金额
    productList = []
    total_amt_list = after_dis_pro.get("total_amt_list", 0)  # 所有商品的总吊牌金额
    total_amt_retail = after_dis_pro.get("total_amt_retail", 0)  # 所有商品的总零售金额
    total_amt_receivable = after_dis_pro.get("total_amt_receivable", 0)  # 所有商品的总应收金额
    new_total_amt_receivable = after_dis_pro.get("new_total_amt_receivable", 0)  # 执行促销后总金额
    give_max_pronum=after_dis_pro.get("give_max_pronum",0)
    give_max_amtlist=after_dis_pro.get("give_max_amtlist",0)
    # if new_nodis_pro:
    for row in new_nodis_pro+after_dis_pro.get("nodisproductList",[]):
        productList.append(row)
        total_amt_list = float(total_amt_list) + float(row.total_amt_list)
        total_amt_retail = float(total_amt_retail) + float(row.total_amt_retail)
        total_amt_receivable = float(total_amt_receivable) + float(row.total_amt_receivable)
        give_max_pronum=give_max_pronum+row.give_max_pronum
        give_max_amtlist=give_max_amtlist+row.give_max_amtlist
    # if after_dis_pro.get("nodisproductList", []):
    #     for row4 in after_dis_pro.get("nodisproductList"):
    #         productList.append(row4)
    #         total_amt_list = float(total_amt_list) + float(row4.total_amt_list)
    #         total_amt_retail = float(total_amt_retail) + float(row4.total_amt_retail)
    #         total_amt_receivable = float(total_amt_receivable) + float(row4.total_amt_receivable)
    #         give_max_pronum=give_max_pronum+row4.give_max_pronum
    #         give_max_amtlist=give_max_amtlist+row4.give_max_amtlist

    after_dis_pro["productList"] = productList
    after_dis_pro["total_amt_list"] = total_amt_list  # 所有商品的总吊牌金额
    after_dis_pro["total_amt_retail"] = total_amt_retail  # 所有商品的总零售金额
    after_dis_pro["total_amt_receivable"] = total_amt_receivable  # 所有商品的总应收金额
    after_dis_pro["new_total_amt_receivable"] = new_total_amt_receivable
    after_dis_pro["give_max_pronum"] = give_max_pronum
    after_dis_pro["give_max_amtlist"] = give_max_amtlist

    return after_dis_pro


def getreturnprovalue(productList, targetproducts):
    '''
    将商品重组成返回值里的商品格式
    :param productList:
    :param targetproducts:
    :return:
    '''
    products = targetproducts
    for row in productList:
        productSeatList = row.productSeatList
        new_products = {}
        if productSeatList:
            try:
                productSeatList = sorted(productSeatList, key=lambda x: x.is_buy_gifts, reverse=False)
            except KeyError:
                pass
            for row_i in productSeatList:
                new_products = {}
                if products:

                    row_sku = linq(products).where(lambda x: (x["lineno"] == row.lineno or x["lineno"] == -1) and x[
                        "amt_receivable"] == row_i.amt_receivable and x["isfullgift"] == row_i.is_buy_gifts and x[
                                                                 "ecode"] == row.ecode and x["sku"] == row.sku and x[
                                                                 "ga_dis"] == row_i.discountId and x["pa_dis"] == row_i.fulldiscounts).tolist()
                    if row_sku:
                        if (row_sku[0]["lineno"] == -1 or row_sku[0]["lineno"] == row.lineno):
                            isnewrow = False
                            ishavegadis = True
                            ishavepadis = True
                            for row2 in row_i.discountId:
                                if row2 not in row_sku[0]["ga_dis"]:
                                    ishavegadis = False
                                    break
                                else:
                                    ishavegadis = True
                            for row3 in row_i.fulldiscounts:
                                if row3 not in row_sku[0]["pa_dis"]:
                                    ishavepadis = False
                                    break
                                else:
                                    ishavepadis = True

                            if not ishavegadis and not ishavepadis:
                                isnewrow = True
                            if isnewrow:
                                new_products=setnewitem_byreturnpro(row_i.amt_list,row_i.amt_retail,row_i.amt_receivable,row_i.discountId,row_i.fulldiscounts,row_i.is_buy_gifts,row_i.is_taken_off,row_i.ecode,row_i.sku,-1,row_i.pcond_id, row_i.pitem_id)

                            else:
                                new_products = {}
                                row_sku[0]['qtty'] = row_sku[0]['qtty'] + 1

                        else:
                            lineno=row.lineno
                            row_sku1 = linq(products).where(
                                lambda x: x["lineno"] == row.lineno and x["ecode"] == row.ecode and x[
                                    "sku"] == row.sku).tolist().copy()
                            if row_sku1 and row_sku1[0]["lineno"] == row.lineno:
                                lineno = -1
                            new_products = setnewitem_byreturnpro(row_i.amt_list, row_i.amt_retail,
                                                                  row_i.amt_receivable, row_i.discountId,
                                                                  row_i.fulldiscounts, row_i.is_buy_gifts,
                                                                  row_i.is_taken_off, row_i.ecode, row_i.sku, lineno,row_i.pcond_id, row_i.pitem_id)
                    else:
                        lineno = row.lineno
                        row_sku1 = linq(products).where(
                            lambda x: x["lineno"] == row.lineno and x["ecode"] == row.ecode and x[
                                "sku"] == row.sku).tolist().copy()
                        if row_sku1 and row_sku1[0]["lineno"] == row.lineno:
                            lineno = -1
                        else:
                            lineno = row.lineno
                        new_products = setnewitem_byreturnpro(row_i.amt_list, row_i.amt_retail,
                                                              row_i.amt_receivable, row_i.discountId,
                                                              row_i.fulldiscounts, row_i.is_buy_gifts,
                                                              row_i.is_taken_off, row_i.ecode, row_i.sku, lineno,row_i.pcond_id, row_i.pitem_id)
                else:
                    new_products = setnewitem_byreturnpro(row_i.amt_list, row_i.amt_retail,
                                                          row_i.amt_receivable, row_i.discountId,
                                                          row_i.fulldiscounts, row_i.is_buy_gifts,
                                                          row_i.is_taken_off, row_i.ecode, row_i.sku, row.lineno,row_i.pcond_id, row_i.pitem_id)
                if new_products:
                    new_products["discount"] = Keeptwodecplaces(div(new_products["amt_receivable"],new_products["amt_list"]))
                    products.append(new_products)
    return products


def getreturndisvalue(productList, targetalldis, product_activity_list, fullcourt_activity_list):
    '''
    最优促销结构重组
    :param productList:
    :param targetalldis:
    :return:
    '''
    alldis = targetalldis
    for row in productList:
        productSeatList = row.productSeatList
        new_products = {}
        if productSeatList:
            for row_i in productSeatList:
                if row_i.discountPrice == [] and row_i.fulldiscountPrice == []:
                    continue
                if row_i.discountId and row_i.discountPrice != []:
                    if alldis:
                        for index, row2 in enumerate(row_i.discountId):
                            if index == len(row_i.discountPrice):
                                continue
                            row_dis1 = linq(alldis).where(lambda x: x["id"] == row2 and x["type_one"] == "GA").tolist()
                            if row_dis1:
                                ecode = row.sku if row.sku else row.ecode
                                if ecode not in row_dis1[0]["products"]:
                                    row_dis1[0]["products"].append(ecode)
                                    row_dis1[0]["qtty"].append(1)
                                else:
                                    r_index = (row_dis1[0]["products"]).index(ecode)
                                    row_dis1[0]["qtty"][r_index] = row_dis1[0]["qtty"][r_index] + 1
                                row_dis1[0]["disamt"] = float(util.add(row_dis1[0]["disamt"],(row_i.discountPrice)[index]))
                            else:
                                # 从策略对象中查询策略详细信息
                                setnewitem_byreturndis(product_activity_list, row2, row, row_i, index, "GA", alldis,1)
                    else:
                        for index, row2 in enumerate(row_i.discountId):
                            if index == len(row_i.discountPrice):
                                continue
                            # 从策略对象中查询策略详细信息
                            setnewitem_byreturndis(product_activity_list, row2, row, row_i, index, "GA", alldis,1)

                if row_i.fulldiscounts and row_i.fulldiscountPrice != []:
                    if alldis:
                        for index, row2 in enumerate(row_i.fulldiscounts):
                            if index == len(row_i.fulldiscountPrice):
                                continue
                            row_dis = linq(alldis).where(lambda x: x["id"] == row2 and x["type_one"] == "PA").tolist()
                            if row_dis:
                                ecode = row.sku if row.sku else row.ecode
                                if ecode not in row_dis[0]["products"]:
                                    row_dis[0]["products"].append(ecode)
                                    row_dis[0]["qtty"].append(1)
                                else:
                                    r_index=(row_dis[0]["products"]).index(ecode)
                                    row_dis[0]["qtty"][r_index]=row_dis[0]["qtty"][r_index]+1
                                row_dis[0]["disamt"] = float(util.add(row_dis[0]["disamt"],(row_i.fulldiscountPrice)[index]))
                            else:
                                # 从策略对象中查询策略详细信息
                                setnewitem_byreturndis(fullcourt_activity_list, row2, row, row_i, index, "PA", alldis,1)
                    else:
                        for index, row2 in enumerate(row_i.fulldiscounts):
                            if index == len(row_i.fulldiscountPrice):
                                continue

                            setnewitem_byreturndis(fullcourt_activity_list, row2, row, row_i, index, "PA", alldis,1)
    return alldis


def getreturnprodisvalue(productList, targetproducts, product_activity_list, fullcourt_activity_list):
    '''
    将商品重组成返回值里的商品执行促销情况（pos使用）
    :param productList:
    :param targetproducts:
    :return:
    '''
    products = targetproducts
    for row in productList:
        productSeatList = row.productSeatList
        new_products = {}
        if productSeatList:
            for row_i in productSeatList:
                if row_i.discountPrice == [] and row_i.fulldiscountPrice == []:
                    continue
                new_products = {}
                if products:
                    if row_i.discountId and row_i.discountPrice != []:
                        for index1, r1 in enumerate(row_i.discountId):
                            if index1 == len(row_i.discountPrice):
                                continue
                            row_info = linq(products).where(
                                lambda x: x["ecode"] == row.ecode and x["sku"] == row.sku and x["dis_id"] == r1 and x[
                                    "dis_type_one"] == "GA").tolist()
                            if row_info:
                                row_info[0]["qtty"] = row_info[0]["qtty"] + 1
                                row_info[0]["dis_amt"] =float(util.add(row_info[0]["dis_amt"],(row_i.discountPrice)[index1]))
                            else:
                                setnewitem(product_activity_list, r1, row, row_i, index1, "GA", products)

                    if row_i.fulldiscounts and row_i.fulldiscountPrice != []:
                        for index2, r2 in enumerate(row_i.fulldiscounts):
                            if index2 == len(row_i.fulldiscountPrice):
                                continue
                            row_info = linq(products).where(
                                lambda x: x["ecode"] == row.ecode and x["sku"] == row.sku and x["dis_id"] == r2 and x[
                                    "dis_type_one"] == "PA").tolist()
                            if row_info:
                                row_info[0]["qtty"] = row_info[0]["qtty"] + 1
                                row_info[0]["dis_amt"] = float(util.add(row_info[0]["dis_amt"],(row_i.fulldiscountPrice)[index2]))
                            else:
                                setnewitem(fullcourt_activity_list, r2, row, row_i, index2, "PA", products)


                else:
                    if row_i.discountId and row_i.discountPrice != []:
                        for index1, r1 in enumerate(row_i.discountId):
                            if index1 == len(row_i.discountPrice):
                                continue
                            setnewitem(product_activity_list, r1, row, row_i, index1, "GA", products)
                    if row_i.fulldiscounts and row_i.fulldiscountPrice != []:
                        for index2, r2 in enumerate(row_i.fulldiscounts):
                            if index2 == len(row_i.fulldiscountPrice):
                                continue
                            setnewitem(fullcourt_activity_list, r2, row, row_i, index2, "PA", products)

    return products


def getreturnbgpro(productList, targetbgpro, product_activity_list, fullcourt_activity_list, optimal_dis, gabg=None,
                   pabg=None):
    '''
    满足执行的但目前单据商品无法执行的赠品活动列表
    :param targetproducts: 执行买赠活动列表
    :param product_activity_list: 可参加商品活动列表
    :param fullcourt_activity_list: 可参加全场活动列表
    :param gabg  参加过商品活动的促销活动明细
    :return:
    '''
    bgpro = targetbgpro
    if gabg:
        # 循环促销活动列表，每个促销活动包括其活动ID与赠送商品总数
        for row in gabg:
            if "qtty" not in row.keys():
                continue
            new_dis = {}  # 新建变量new_dis存储节点内容
            new_dis["compute_list"] = []
            operations = []
            totals = 0
            for dis_i in product_activity_list:  # 遍历可参加的商品活动列表
                if row['id'] == dis_i['id']:  # 匹配ID获取活动明细
                    new_dis["type_one"] = "GA"
                    new_dis["publish_date"] = dis_i['publish_date']
                    new_dis["type_three"] = dis_i['prom_type_three']
                    new_dis["type_two"] = dis_i['prom_type_two']
                    new_dis["ename"] = dis_i['ename']
                    new_dis["id"] = dis_i['id']
                    new_dis["is_run_other_pro"] = dis_i['is_run_other_pro'].lower()
                    new_dis["is_run_store_act"] = dis_i['is_run_store_act'].lower()
                    new_dis["is_run_other"] = "y"
                    if new_dis["type_two"] == 5:
                        new_dis["prom_type_two_c"] = dis_i["prom_type_two_c"]
                    for seat in productList:
                        for product in seat.productSeatList:
                            if dis_i["specific_activities"][0]["target_type"].lower() == "amt_receivable":
                                totals += product.amt_receivable
                                if new_dis["type_two"] == 4:
                                    if product.is_taken_off:
                                        continue
                                elif new_dis["type_two"] == 5:
                                    if product.is_taken_off or product.is_buy_gifts == "y":
                                        continue
                                totals += product.amt_receivable
                            if dis_i["specific_activities"][0]["target_type"].lower() == "amt_list":
                                totals += product.amt_list
                                if new_dis["type_two"] == 4:
                                    if product.is_taken_off:
                                        continue
                                elif new_dis["type_two"] == 5:
                                    if product.is_taken_off or product.is_buy_gifts == "y":
                                        continue
                                totals += product.amt_list
                            if dis_i["specific_activities"][0]["target_type"].lower() == "qtty":
                                if new_dis["type_two"] == 4:
                                    if product.is_taken_off:
                                        continue
                                elif new_dis["type_two"] == 5:
                                    if product.is_taken_off or product.is_buy_gifts == "y":
                                        continue
                                totals += product.qtty
                            if dis_i["specific_activities"][0]["target_type"].lower() == "amt_retail":
                                if new_dis["type_two"] == 4:
                                    if product.is_taken_off:
                                        continue
                                elif new_dis["type_two"] == 5:
                                    if product.is_taken_off or product.is_buy_gifts == "y":
                                        continue
                                totals += product.amt_retail
                    bg = dis_i["specific_activities"][0]["operation_set"]
                    for gift in bg:
                        compare = gift["comp_symb_type"]
                        if compare == "G":
                            value_num = gift["value_num"] + 1
                        else:
                            value_num = gift["value_num"]
                        if totals >= value_num:
                            operations.append(gift)
                    if new_dis["type_three"] == "GA1501" or new_dis["type_three"] == "GA1502":
                        purchase_way = "T"
                    elif new_dis["type_three"] == "GA1503" or new_dis["type_three"] == "GA1504":
                        purchase_way = "D"
                    else:
                        purchase_way = "J"
                    for operation in operations:
                        if new_dis["type_two"] != 5:
                            try:
                                if new_dis["type_three"]=='ga1402':
                                    if int(operation["promotion_lineno"])<=int(row['promotion_lineno']):
                                        new_dis["compute_list"].append(
                                            {"product_list": operation["buy_gifts"]["product_list"], "give_value": row['qtty'],
                                             "list_sort": operation["promotion_lineno"]})
                                else:
                                    new_dis["compute_list"].append(
                                        {"product_list": operation["buy_gifts"]["product_list"],
                                         "give_value": row['qtty'],
                                         "list_sort": 1})
                            except KeyError:
                                new_dis["compute_list"].append(
                                    {"product_list": operation["buy_gifts"]["product_list"], "give_value": row['qtty']})
                        else:

                            try:
                                new_dis["compute_list"].append(
                                    {"pcond_id": operation["pcond_id"], "target_item": dis_i["target_item"],
                                     "purchase_condition": operation["redemption"]["purchase_condition"],
                                     "purchase_way": purchase_way,
                                     "product_list": operation["redemption"]["product_list"], "times": row["times"],
                                     "single_value": row["bsc_qtty"], "give_value": row['qtty']})
                            except KeyError:
                                new_dis["compute_list"].append(
                                    {"product_list": operation["buy_gifts"]["product_list"], "give_value": row['qtty']})
                    bgpro.append(new_dis)

    if pabg:
        for row in pabg:
            new_dis = {}  # 新建变量new_dis存储节点内容
            new_dis["compute_list"] = []
            for dis_i1 in fullcourt_activity_list:
                if row['id'] == dis_i1['id']:  # 匹配ID获取活动明细
                    new_dis["type_one"] = "PA"
                    new_dis["publish_date"] = dis_i1['publish_date']
                    new_dis["type_three"] = dis_i1['prom_type_three']
                    new_dis["type_two"] = dis_i1['prom_type_two']
                    new_dis["ename"] = dis_i1['ename']
                    new_dis["id"] = dis_i1['id']
                    new_dis["is_run_other_pro"] = dis_i1['is_run_other_pro'].lower()
                    new_dis["is_run_store_act"] = dis_i1['is_run_store_act'].lower()
                    if new_dis["type_two"] == 5:
                        new_dis["prom_type_two_c"] = dis_i1["prom_type_two_c"]
                    dis_num = 0
                    if optimal_dis:
                        for dis in optimal_dis:
                            if dis["type_one"] == "GA":
                                dis_num += 1
                        if dis_num != len(optimal_dis):
                            for dis in optimal_dis:
                                if dis['type_one'] == "PA":
                                    for dis_i in fullcourt_activity_list:
                                        if dis['id'] == dis_i["id"]:
                                            if dis_i['is_run_store_act'] == "Y":
                                                new_dis["is_run_other"] = "y"
                                            else:
                                                new_dis["is_run_other"] = "n"
                                                break
                                    if new_dis["is_run_other"] == "n":
                                        break
                                else:
                                    for dis_i1 in product_activity_list:
                                        if dis['id'] == dis_i1["id"]:
                                            if dis_i1['is_run_store_act'] == "Y":
                                                new_dis["is_run_other"] = "y"
                                            else:
                                                new_dis["is_run_other"] = "n"
                                                break
                                    if new_dis["is_run_other"] == "n":
                                        break
                        else:
                            new_dis["is_run_other"] = "y"
                    else:
                        new_dis["is_run_other"] = "n"
                    if new_dis["type_three"] == "PA1401":
                        purchase_way = "T"
                    elif new_dis["type_three"] == "PA1402":
                        purchase_way = "D"
                    else:
                        purchase_way = "J"
                    for operation in reversed(row["operations"]):
                        if new_dis["type_two"] != 5:
                            try:
                                new_dis["compute_list"].append(
                                    {"product_list": operation["buy_gifts"]["product_list"],
                                     "give_value": row['give_value'],
                                     "list_sort": operation["promotion_lineno"]})
                            except KeyError:
                                new_dis["compute_list"].append(
                                    {"product_list": operation["buy_gifts"]["product_list"],
                                     "give_value": row['give_value']})
                        else:
                            try:
                                new_dis["compute_list"].append(
                                    {"pcond_id": operation["pcond_id"], "target_item": dis_i1["target_item"],
                                     "purchase_condition": operation["redemption"]["purchase_condition"],
                                     "purchase_way": purchase_way,
                                     "product_list": operation["redemption"]["product_list"], "times": row["times"],
                                     "single_value": row["bsc_qtty"], "give_value": row['qtty']})
                            except KeyError:
                                new_dis["compute_list"].append(
                                    {"product_list": operation["redemption"]["product_list"], "give_value": row['qtty']})
                    bgpro.append(new_dis)

    return bgpro


def getreturnbgtwo(fullgit_disgroup):
    if fullgit_disgroup:
        for index in range(0, len(fullgit_disgroup)):
            fullgit_disgroup[index] = list(fullgit_disgroup[index])
    else:
        return []
    return fullgit_disgroup


def getcpproducts(products_cp, buygifts):
    products = []
    if buygifts != []:
        for row in buygifts:
            if "purchase" not in row.keys():
                continue
            for row1 in row["disproductList"]+row["productList"]:
                for row2 in row1.productSeatList:
                    if row2.is_repurchase == "y":
                        if products != []:
                            product = products[-1]
                            if product["ecode"] == row2.ecode and product["sku"] == row2.sku and (
                                    product["lineno"] == row2.lineno or product["lineno"] == -1) and product[
                                "amt_receivableb"] == row2.upamt_receivable and product[
                                "amt_receivablea"] == row2.amt_receivable and product["pcond_id"] == row2.pcond_id and \
                                    product["groupnum"] == row2.groupnum and product["ga_dis"] == row2.discountId and \
                                    product["pa_dis"] == row2.fulldiscounts:
                                product["qtty"] += 1
                            else:
                                lineno=row2.lineno
                                if product["ecode"] == row2.ecode and product["sku"] == row2.sku:
                                    if buygifts.index(row)!=product["times"]:
                                        continue
                                    lineno=-1
                                else:
                                    for p in products:
                                        if p["ecode"] == row2.ecode and p["sku"] == row2.sku:
                                            if buygifts.index(row) != p["times"]:
                                                break
                                    if products.index(p)!=len(products)-1:
                                        continue
                                setnewitem_byreturnswappro(row2.ecode, row2.sku, lineno, row2.upamt_receivable,
                                                       row2.amt_receivable, row2.pcond_id, row2.groupnum,
                                                       row2.discountId,
                                                       row2.fulldiscounts, buygifts.index(row), products)
                        else:
                            setnewitem_byreturnswappro(row2.ecode, row2.sku, row2.lineno, row2.upamt_receivable,
                                                   row2.amt_receivable, row2.pcond_id, row2.groupnum,
                                                   row2.discountId,
                                                   row2.fulldiscounts,buygifts.index(row), products)
        for p1 in products:
            if "times" in p1.keys():
                p1.pop("times")


    if products_cp != []:
        for row2 in products_cp:
            if products != []:
                product = products[-1]
                if product["ecode"] == row2["ecode"] and product["sku"] == row2["sku"] and (
                        product["lineno"] == row2["lineno"] or product["lineno"] == -1) and product["amt_receivableb"] == row2["amt_receivableb"] and product["amt_receivablea"] == row2["amt_receivablea"] and product["pcond_id"] == row2["pcond_id"] and \
                        product["groupnum"] == row2["groupnum"] and product["ga_dis"] == row2["ga_dis"] and product["pa_dis"] == row2["pa_dis"]:
                    product["qtty"] += 1
                else:
                    lineno=row2['lineno']
                    if product["ecode"] == row2["ecode"] and product["sku"] == row2["sku"]:
                        lineno=-1

                    setnewitem_byreturnswappro(row2['ecode'], row2['sku'], lineno, row2['amt_receivableb'],
                                           row2['amt_receivablea'], row2['pcond_id'], row2['groupnum'],
                                           row2['ga_dis'],
                                           row2['pa_dis'],None, products)
            else:
                setnewitem_byreturnswappro(row2['ecode'], row2['sku'], row2['lineno'], row2['amt_receivableb'], row2['amt_receivablea'], row2['pcond_id'], row2['groupnum'], row2['ga_dis'],
                                       row2['pa_dis'],None, products)
    return products

def setnewitem_byreturnpro(amt_list,amt_retail,amt_receivable,discountId,fulldiscounts,is_buy_gifts,is_taken_off,ecode,sku,lineno,pcond_id, pitem_id):
    new_products={}
    new_products["amt_list"] = amt_list
    new_products["amt_retail"] = amt_retail
    new_products["amt_receivable"] = amt_receivable
    new_products["ga_dis"] = list(set(discountId))
    new_products["pa_dis"] = list(set(fulldiscounts))
    new_products["isfullgift"] = is_buy_gifts
    new_products["is_taken_off"] = is_taken_off
    # new_products["is_repurchase"] = row_i.is_repurchase
    new_products["ecode"] = ecode
    new_products["sku"] = sku
    new_products["lineno"] = lineno
    new_products["pcond_id"]=pcond_id
    new_products["pitem_id"] = pitem_id
    new_products["qtty"] = 1
    return new_products

def setnewitem_byreturnswappro(ecode,sku,lineno,amt_receivableb,amt_receivablea,pcond_id,groupnum,ga_dis,pa_dis,times,products):
    '''
    设置返回计算后的换购商品明细的一行信息
    :param ecode: 商品（款号）
    :param sku: 条码
    :param lineno: 行号
    :param amt_receivableb:应收价
    :param amt_receivablea:应收价
    :param pcond_id: 促销优惠明细ID
    :param groupnum:标记翻倍的倍数分组
    :param ga_dis:执行的商品促销ID集合
    :param pa_dis:执行的全场促销ID集合
    :param times:
    :param products:返回的列表
    :return:
    '''
    purproduct = {}
    purproduct["ecode"] = ecode
    purproduct["sku"] = sku
    purproduct["lineno"] = lineno
    purproduct["amt_receivableb"] = amt_receivableb
    purproduct["amt_receivablea"] = amt_receivablea
    purproduct["qtty"] = 1
    purproduct["pcond_id"] = pcond_id
    purproduct["groupnum"] = groupnum
    purproduct["ga_dis"] = ga_dis
    purproduct["pa_dis"] = pa_dis
    if times is not None:
        purproduct["times"] = times
    products.append(purproduct)

def setnewitem_byreturndis(activity_list,dis_id,row,row_i,listindex,distypeone,alldis,qtty):
    '''
    设置最优促销结构重组一行的信息
    :param activity_list: 促销活动
    :param dis_id: 当前处理的促销id
    :param row: 商品明细行
    :param row_i: 单个数量的商品明细行
    :param listindex:促销优惠金额的列表索引
    :param distypeone: 促销一类编码
    :param alldis: 返回的列表
    :param qtty: 优惠商品的数量
    :return:
    '''
    new_dis = {}
    row_dis = linq(activity_list).where(lambda x: x["id"] == dis_id).tolist().copy()
    if row_dis:
        nrow_dis = row_dis[0]
        new_dis = {"id": nrow_dis.get("id", ""), "ename": nrow_dis.get("ename", ""),
                   "type_one": distypeone, "type_two": nrow_dis.get("prom_type_two", ""),
                   "type_three": nrow_dis.get("prom_type_three", ""),
                   "publish_date": nrow_dis.get("publish_date", "")}
        new_dis["type_one_ename"] = util.get_distypeename(new_dis["type_one"], 1)
        new_dis["type_two_ename"] = util.get_distypeename(str(new_dis["type_two"]), 2)
        new_dis["type_three_ename"] = util.get_distypeename(str(new_dis["type_three"]).upper(), 3)

    new_dis["products"] = []
    new_dis["qtty"]=[]
    new_dis["products"].append(row.sku if row.sku else row.ecode)
    new_dis["qtty"].append(qtty)
    if distypeone == "GA":
        new_dis["disamt"] = float((row_i.discountPrice)[listindex])
    else:
        new_dis["disamt"] = float((row_i.fulldiscountPrice)[listindex])
    alldis.append(new_dis)

def setnewitem(activity_list,dis_id,row,row_i,listindex,distypeone,products):
    '''
    设置商品执行促销情况的一行明细信息
    :param activity_list: 促销活动
    :param dis_id: 当前处理的促销id
    :param row: 商品明细行
    :param row_i: 单个数量的商品明细行
    :param listindex:促销优惠金额的列表索引
    :param distypeone: 促销一类编码
    :param products: 返回的列表
    :return:
    '''
    row_dis = []
    row_dis = linq(activity_list).where(lambda x: x["id"] == dis_id).tolist().copy()
    if row_dis:
        nrow_dis = {}
        nrow_dis = row_dis[0]
        new_products = {}
        new_products["ecode"] = row.ecode
        new_products["sku"] = row.sku
        new_products["qtty"] = 1
        new_products["dis_id"] = dis_id
        new_products["dis_ename"] = nrow_dis.get("ename", "")
        new_products["dis_type_one"] = distypeone
        if distypeone=="GA":
            new_products["dis_amt"] = float((row_i.discountPrice)[listindex])
        else:
            new_products["dis_amt"] = float((row_i.fulldiscountPrice)[listindex])
        products.append(new_products)
