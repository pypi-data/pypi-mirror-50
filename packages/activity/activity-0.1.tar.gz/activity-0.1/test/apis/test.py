
from pro.utils.linq import linq
import pro.utils.util as util
from pro.apis.entitys.GA_entitys.cp.unify_discount_cp import Unify_Cp
from pro.apis.entitys.products_entitys.product import Product
from pro.apis.GA_api.CP_api.cp_utils import calculate_fun
import copy

product_activity_list=[{
      "gift_condition": 1,
      "prom_type_three": "GA1501",
      "rela_symb_type": "and",
      "prom_type_two_c": 60,
      "specific_activities": [{
        "target_type": "QTTY",
        "operation_set": [{
            "redemption": {
              "give_value": 2,
              "purchase_condition": 30,
              "product_list": [{
                  "AMT_LIST": 49,
                  "ECODE": "18D0001"
                },
                {
                  "AMT_LIST": 49,
                  "ECODE": "18D0002"
                }
              ]
            },
            "comp_symb_type": "GE",
            "value_num": 2,
            "pcond_id": 1
          },
          {
            "redemption": {
              "give_value": 2,
              "purchase_condition": 20,
              "product_list": [{
                  "AMT_LIST": 269,
                  "ECODE": "18F1001"
                },
                {
                  "AMT_LIST": 269,
                  "ECODE": "18F1002"
                }
              ]
            },
            "comp_symb_type": "GE",
            "value_num": 2,
            "pcond_id": 2
          }
        ],
        "product_list": [
          "18T5300",
          "18T5301"
        ]
      }],
      "is_run_store_act": "N",
      "members_only": "N",
      "prom_type_two": 5,
      "prom_scope": "GA",
      "exchange_condition": 1,
      "ename": "统一特价换购（商品-POS）",
      "is_run_vip_discount": "N",
      "max_times": -1,
      "target_item": "AMT_LIST",
      "id": 1475,
      "publish_date": 1547520693000,
      "is_run_other_pro": "N"
    }]
productJsonList=[{
      "lineno": 1,
      "amt_receivable": 50,
      "ProductName": "男休闲T恤",
      "is_buy_gifts": "N",
      "amt_retail": 10,
      "sku": "18T53016666",
      "RetailType": "1",
      "qtty": 2,
      "amt_list": 199,
      "ecode": "18T5301",
      "is_repurchase": "N"
    },
    {
      "lineno": 2,
      "amt_receivable": 55,
      "ProductName": "女休闲T恤",
      "is_buy_gifts": "N",
      "amt_retail": 10,
      "sku": "18T53000105",
      "RetailType": "1",
      "qtty": 2,
      "amt_list": 59,
      "ecode": "18T5300",
      "is_repurchase": "N"
    },
    {
      "lineno": 3,
      "amt_receivable": 55,
      "ProductName": "女休闲T恤",
      "is_buy_gifts": "N",
      "amt_retail": 10,
      "sku": "18T53000105",
      "RetailType": "1",
      "qtty": 1,
      "amt_list": 59,
      "ecode": "18D0001",
      "is_repurchase": "N"
    },
    {
      "lineno": 4,
      "amt_receivable": 55,
      "ProductName": "女休闲T恤",
      "is_buy_gifts": "N",
      "amt_retail": 10,
      "sku": "18T53000105",
      "RetailType": "1",
      "qtty": 2,
      "amt_list": 59,
      "ecode": "18F1001",
      "is_repurchase": "N"
    }
  ]
cp=[]
# 所有商品对象集合
productList = []
i = 1
for productJson in productJsonList:
    productList.append(Product(productJson, i))
    i = i + 1
for bean in product_activity_list:
    two_id = bean['prom_type_two']
    three_id = str(bean['prom_type_three']).lower()
    if "ga1501" == three_id:
        cp.append(Unify_Cp(bean))

for bean in cp:
    newrow=calculate_fun(bean,productList)


    print(newrow)

for bean1 in cp:
    newrow1 = calculate_fun(bean, productList,1,newrow[0]["pro_list"])
    print(newrow1)


from pro.apis.GA_api.CP_api.cp_utils import getNewPrice
nrr=getNewPrice(bean,newrow1[0]["pro_list"])

print(nrr)

r=10
new_price=-1
r =new_price if new_price>=0 else r

print(r)

aa=[]
print(list(set(aa.append(id))) if len(aa)>0 else ["33"])
