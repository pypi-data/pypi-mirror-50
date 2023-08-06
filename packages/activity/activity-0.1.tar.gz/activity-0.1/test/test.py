
import json
from pro.apis.main import acceptParams
json={
	"product_list": [
		{
			"ecode": "AS001",
			"sku":"AS00101",
			"lineno":"1",
			"amt_list": 18.8,
			"amt_retail": 18.8,
			"amt_receivable": 18.8,
			"qtty": 2
		}
	],
	"promotion_list": {
		"product_activity_list": [
			{
				"prom_type_two": 2,
				"prom_type_three": "ga1201",
				"id":"1",
				"ename": "统一减现1",
				"target_item":"amt_receivable",
				"prom_type_two_c":"2",
				"publish_date":"11112",
				"members_only": "n",
				"members_group": [
					1,
					2,
					3
				],
				"is_run_other_pro": "y",
				"is_run_store_act": "y",
				"is_run_vip_discount": "n",
				"max_times": -1,
				"exchange_condition": 1,
				"gift_condition": 1,
				"specific_activities": [
					{
						"product_list": [
							"as001",
							"as003"
						],
						"target_type": "qtty",
						"operation_set":
						[
							{
								"comp_symb_type": "ge",
								"value_num": 2,
								"money_off_value": 5,
								"pcond_id":1
							}
						]
					}
				]
			}
		],
		"fullcourt_activity_list": [
		]
	},
	"user":{
		"id":"1",
		"discount":"1"
	}
}

result = acceptParams(json['product_list'], json['promotion_list'], json['user'],2)
print (result)