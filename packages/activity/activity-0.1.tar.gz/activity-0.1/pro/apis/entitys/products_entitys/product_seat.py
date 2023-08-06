# -*- coding:utf-8 -*-
# author:尹晨
# datetime:2018/9/27 15:46

from pro.utils.util import Keeptwodecplaces
from pro.utils.util import div

class ProductSeat():
    def __init__(self, obj):
        # 商品编码
        self.ecode = obj['ecode']
        # 标记该商品是否可以参与促销计算（值y/n，y可以，n不可以）
        self.is_discount = str(obj.get("is_discount", "y")).lower() if obj.get("is_discount", "y") else "y"
        # 吊牌价
        self.amt_list = float(obj['amt_list'])
        # 零售价
        self.amt_retail = float(obj['amt_retail'])
        # 应收价
        self.amt_receivable = float(obj['amt_receivable'])
        #折扣
        self.discount=Keeptwodecplaces(div(obj["amt_receivable"],obj["amt_list"]))
        # 最原始的应收价，用于计算商品活动优惠金额使用
        self.upamt_receivable = float(obj['amt_receivable'])
        # # 执行了商品活动没有执行全场活动时的价格，用于计算商品活动优惠金额使用
        # self.beforpadisamt_receivable = obj['amt_receivable']
        # # 执行了商品活动没有执行全场活动时的价格，用于计算全场活动优惠金额使用（会根据计算使用金额不同来变化）
        # self.beforpadisamt_receivablebypa = obj['amt_receivable']
        # sku
        self.sku = obj['sku']
        #行号
        self.lineno = obj['lineno']
        # 数量
        self.qtty = 1
        # 是否占位
        self.seat = False
        # 是否可以进行下次商品活动
        self.is_run_other_pro = True
        # 是否可以进行全场活动
        self.is_run_store_act = True
        # 记录优惠过程
        self.str_discount = '商品' + self.ecode
        # 参加商品的活动id集合
        self.discountId = []
        #参加商品活动优惠的金额
        self.discountPrice = []
        #是否参加过VIP折上折  true为参加过
        self.is_run_vip_discount = False
        #记录参加的全场活动
        self.fulldiscounts=[]
        # 参加全场活动优惠的金额
        self.fulldiscountPrice = []
        # 因翻倍限制所不能参加的活动---活动ID
        self.notProId = []
        #是否是赠品
        self.is_buy_gifts = "n"
        #是否是换购品
        self.is_repurchase = "n"
        #换购的倍数组
        self.groupnum=None
        #换购的行数值
        self.pcond_id=-1
        #
        self.pitem_id = obj.get("pitem_id", -1)
        #换购执行类型--打折、优惠、特价
        self.purchase_way=None
        #差额
        self.diffPrice=0
        #每次执行活动后的金额
        self.after_dis_amt_receivable=[]
        #增加买免标记让全场识别
        self.is_taken_off = False
        #全场换购专用,标记是否满足换购活动条件
        self.no_pur_seat=False
        #换购出参专用，防止多个结果影响出参
        self.times=None
        #全场换购记录单价用，解决同一换购品在不同梯度
        self.pur_seat=False
        #全场换购记录换购品用，解决同一换购品在不同梯度
        self.pur=False
    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)
