
import json
from pro.apis.main import acceptParams
# json={
# 	"product_list": [
# 		{
# 			"ecode": "AS001",
# 			"sku":"AS00101",
# 			"lineno":"1",
# 			"amt_list": 18.8,
# 			"amt_retail": 18.8,
# 			"amt_receivable": 18.8,
# 			"qtty": 3
# 		},
# 		{
# 			"ecode": "AS002",
# 			"sku":"AS00201",
# 			"lineno":"2",
# 			"amt_list": 19.8,
# 			"amt_retail": 19.8,
# 			"amt_receivable": 19.8,
# 			"qtty": 5
# 		},
#         {
# 			"ecode": "AS003",
# 			"sku":"AS00301",
# 			"lineno":"3",
# 			"amt_list": 29.8,
# 			"amt_retail": 29.8,
# 			"amt_receivable": 29.8,
# 			"qtty": 3
# 		},
#         {
# 			"ecode": "AS004",
# 			"sku":"AS00401",
# 			"lineno":"4",
# 			"amt_list": 24.8,
# 			"amt_retail": 24.8,
# 			"amt_receivable": 24.8,
# 			"qtty": 2
# 		},
#         {
# 			"ecode": "AS005",
# 			"sku":"AS00501",
# 			"lineno":"5",
# 			"amt_list": 22.8,
# 			"amt_retail": 22.8,
# 			"amt_receivable": 22.8,
# 			"qtty": 3
# 		}
# 	],
# 	"promotion_list": {
# 		"product_activity_list": [
# 			{
# 				"prom_type_two": 4,
# 				"prom_type_three": "ga1401",
# 				"id":"1",
# 				"ename": "统一买赠1",
# 				"target_item":"amt_receivable",
# 				"prom_type_two_c":"1",
# 				"publish_date":"11111",
# 				"members_only": "n",
# 				"members_group": [
# 					1,
# 					2,
# 					3
# 				],
# 				"is_run_other_pro": "y",
# 				"is_run_store_act": "y",
# 				"is_run_vip_discount": "n",
# 				"max_times": -1,
# 				"exchange_condition": 1,
# 				"gift_condition": 1,
# 				"specific_activities": [
# 					{
# 						"product_list": [
# 							"AS004"
# 						],
# 						"target_type": "qtty",
# 						"operation_set":
# 						[
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 2,
# 								"promotion_lineno":1,
# 								"buy_gifts": {
# 									"product_list": [
# 										{
# 											"ECODE": "AS002"
# 										}
# 									],
# 									"give_value": 1
# 								}
#
# 							}
# 						]
# 					}
# 				]
# 			},
# 			{
# 				"prom_type_two": 4,
# 				"prom_type_three": "ga1402",
# 				"id":"2",
# 				"ename": "梯度买赠1",
# 				"target_item":"amt_receivable",
# 				"prom_type_two_c":"1",
# 				"publish_date":"11111",
# 				"members_only": "n",
# 				"members_group": [
# 					1,
# 					2,
# 					3
# 				],
# 				"is_run_other_pro": "y",
# 				"is_run_store_act": "y",
# 				"is_run_vip_discount": "n",
# 				"max_times": -1,
# 				"exchange_condition": 1,
# 				"gift_condition": 1,
# 				"specific_activities": [
# 					{
# 						"product_list": [
# 							"AS001"
# 						],
# 						"target_type": "qtty",
# 						"operation_set":
# 						[
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 1,
# 								"promotion_lineno":1,
# 								"buy_gifts": {
# 									"product_list": [
# 										{
# 											"ECODE": "AS002"
# 										}
# 									],
# 									"give_value": 1
# 								}
#
# 							},
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 2,
# 								"promotion_lineno":2,
# 								"buy_gifts": {
# 									"product_list": [
# 										{
# 											"ECODE": "AS003"
# 										}
# 									],
# 									"give_value": 2
# 								}
#
# 							}
# 						]
# 					}
# 				]
# 			},
# 			{
# 				"prom_type_two": 4,
# 				"prom_type_three": "ga1402",
# 				"id":"3",
# 				"ename": "梯度买赠2",
# 				"target_item":"amt_receivable",
# 				"prom_type_two_c":"1",
# 				"publish_date":"11111",
# 				"members_only": "n",
# 				"members_group": [
# 					1,
# 					2,
# 					3
# 				],
# 				"is_run_other_pro": "y",
# 				"is_run_store_act": "y",
# 				"is_run_vip_discount": "n",
# 				"max_times": -1,
# 				"exchange_condition": 1,
# 				"gift_condition": 1,
# 				"specific_activities": [
# 					{
# 						"product_list": [
# 							"AS001"
# 						],
# 						"target_type": "qtty",
# 						"operation_set":
# 						[
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 2,
# 								"promotion_lineno":1,
# 								"buy_gifts": {
# 									"product_list": [
# 										{
# 											"ECODE": "AS002"
# 										}
# 									],
# 									"give_value": 1
# 								}
#
# 							},
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 4,
# 								"promotion_lineno":2,
# 								"buy_gifts": {
# 									"product_list": [
# 										{
# 											"ECODE": "AS006"
# 										}
# 									],
# 									"give_value": 2
# 								}
#
# 							}
# 						]
# 					}
# 				]
# 			}
# 		],
# 		"fullcourt_activity_list": [
# 		]
# 	},
# 	"user":{
# 		"id":"1",
# 		"discount":"1"
# 	}
# }

# json={
#   "product_list": [
#     {
#       "ecode": "AS001",
#       "sku": "AS00101",
#       "lineno": "1",
#       "amt_list": 15,
#       "amt_retail": 15,
#       "amt_receivable": 15,
#       "qtty": 4
#     },
#     {
#       "ecode": "AS002",
#       "sku": "AS00201",
#       "lineno": "2",
#       "amt_list": 19.8,
#       "amt_retail": 19.8,
#       "amt_receivable": 19.8,
#       "qtty": 5
#     },
#     {
#       "ecode": "AS003",
#       "sku": "AS00301",
#       "lineno": "3",
#       "amt_list": 29.8,
#       "amt_retail": 29.8,
#       "amt_receivable": 29.8,
#       "qtty": 3
#     },
#     {
#       "ecode": "AS004",
#       "sku": "AS00401",
#       "lineno": "4",
#       "amt_list": 24.8,
#       "amt_retail": 24.8,
#       "amt_receivable": 24.8,
#       "qtty": 2
#     },
#     {
#       "ecode": "AS005",
#       "sku": "AS00501",
#       "lineno": "5",
#       "amt_list": 22.8,
#       "amt_retail": 22.8,
#       "amt_receivable": 22.8,
#       "qtty": 3
#     },
#     {
#       "ecode": "AS006",
#       "sku": "AS00601",
#       "lineno": "6",
#       "amt_list": 22.8,
#       "amt_retail": 22.8,
#       "amt_receivable": 22.8,
#       "qtty": 5
#     },
#     {
#       "ecode": "AS007",
#       "sku": "AS00701",
#       "lineno": "7",
#       "amt_list": 22.8,
#       "amt_retail": 22.8,
#       "amt_receivable": 22.8,
#       "qtty": 3
#     },
#     {
#       "ecode": "AS008",
#       "sku": "AS00801",
#       "lineno": "8",
#       "amt_list": 22.8,
#       "amt_retail": 22.8,
#       "amt_receivable": 22.8,
#       "qtty": 3
#     }
#   ],
#   "promotion_list": {
#     "product_activity_list": [
#       {
#         "prom_type_two": 4,
#         "prom_type_two_code": "ga14-01",
#         "prom_type_three": "ga1401",
#         "id": "1",
#         "ename": "统一买赠1",
#         "target_item": "amt_receivable",
#         "prom_type_two_c": "1",
#         "publish_date": "11111",
#         "members_only": "n",
#         "members_group": [
#           1,
#           2,
#           3
#         ],
#         "is_run_other_pro": "y",
#         "is_run_store_act": "y",
#         "is_run_vip_discount": "n",
#         "max_times": -1,
#         "exchange_condition": 1,
#         "gift_condition": 1,
#         "specific_activities": [
#           {
#             "product_list": [
#               "AS001"
#             ],
#             "target_type": "amt_receivable",
#             "operation_set": [
#               {
#                 "comp_symb_type": "ge",
#                 "value_num": 20,
#                 "promotion_lineno": 1,
#                 "buy_gifts": {
#                   "product_list": [
#                     {
#                       "ecode": "AS005"
#                     }
#                   ],
#                   "give_value": 1
#                 }
#               }
#             ]
#           }
#         ]
#       },
#       {
#         "prom_type_two": 4,
#         "prom_type_two_code": "ga14-02",
#         "prom_type_three": "ga1401",
#         "id": "2",
#         "ename": "统一买赠2",
#         "target_item": "amt_receivable",
#         "prom_type_two_c": "1",
#         "publish_date": "11111",
#         "members_only": "n",
#         "members_group": [
#           1,
#           2,
#           3
#         ],
#         "is_run_other_pro": "y",
#         "is_run_store_act": "y",
#         "is_run_vip_discount": "n",
#         "max_times": -1,
#         "exchange_condition": 1,
#         "gift_condition": 1,
#         "specific_activities": [
#           {
#             "product_list": [
#               "AS001"
#             ],
#             "target_type": "amt_receivable",
#             "operation_set": [
#               {
#                 "comp_symb_type": "ge",
#                 "value_num": 20,
#                 "promotion_lineno": 1,
#                 "buy_gifts": {
#                   "product_list": [
#                     {
#                       "ecode": "AS006"
#                     }
#                   ],
#                   "give_value": 1
#                 }
#               }
#             ]
#           }
#         ]
#       },
#       {
#         "prom_type_two": 4,
#         "prom_type_two_code": "ga17-01",
#         "prom_type_three": "ga1701",
#         "id": "3",
#         "ename": "线上统一买赠1",
#         "target_item": "amt_receivable",
#         "prom_type_two_c": "1",
#         "publish_date": "11111",
#         "members_only": "n",
#         "members_group": [
#           1,
#           2,
#           3
#         ],
#         "is_run_other_pro": "y",
#         "is_run_store_act": "y",
#         "is_run_vip_discount": "n",
#         "max_times": -1,
#         "exchange_condition": 1,
#         "gift_condition": 1,
#         "specific_activities": [
#           {
#             "product_list": [
#               "AS001"
#             ],
#             "target_type": "amt_receivable",
#             "operation_set": [
#               {
#                 "comp_symb_type": "ge",
#                 "value_num": 20,
#                 "promotion_lineno": 1,
#                 "buy_gifts": {
#                   "product_list": [
#                     {
#                       "ecode": "AS009",
#                       "sku":"AS00901",
#                       "amt_list": 110
#                     }
#                   ],
#                   "give_value": 1
#                 },
#                 "pcond_id":1
#               },
#               {
#                 "comp_symb_type": "ge",
#                 "value_num": 20,
#                 "promotion_lineno": 1,
#                 "buy_gifts": {
#                   "product_list": [
#                     {
#                       "ecode": "AS010",
#                       "sku":"AS01001",
#                       "amt_list": 100
#                     }
#                   ],
#                   "give_value": 1
#                 },
#                 "pcond_id":2
#               }
#             ]
#           }
#         ]
#       }
#     ],
#     "fullcourt_activity_list": []
#   },
#   "user": {
#     "id": "1",
#     "discount": "1"
#   }
# }


# json={
# 	"product_list": [
# 		{
# 			"ecode": "AS001",
# 			"sku":"AS00101",
# 			"lineno":"1",
# 			"amt_list": 18.8,
# 			"amt_retail": 18.8,
# 			"amt_receivable": 18.8,
# 			"qtty": 3
# 		},
# 		{
# 			"ecode": "AS002",
# 			"sku":"AS00201",
# 			"lineno":"2",
# 			"amt_list": 19.8,
# 			"amt_retail": 19.8,
# 			"amt_receivable": 19.8,
# 			"qtty": 5
# 		},
#         {
# 			"ecode": "AS003",
# 			"sku":"AS00301",
# 			"lineno":"3",
# 			"amt_list": 29.8,
# 			"amt_retail": 29.8,
# 			"amt_receivable": 29.8,
# 			"qtty": 3
# 		},
#         {
# 			"ecode": "AS004",
# 			"sku":"AS00401",
# 			"lineno":"4",
# 			"amt_list": 24.8,
# 			"amt_retail": 24.8,
# 			"amt_receivable": 24.8,
# 			"qtty": 2
# 		},
#         {
# 			"ecode": "AS005",
# 			"sku":"AS00501",
# 			"lineno":"5",
# 			"amt_list": 22.8,
# 			"amt_retail": 22.8,
# 			"amt_receivable": 22.8,
# 			"qtty": 3
# 		},
#         {
# 			"ecode": "AS006",
# 			"sku":"AS00601",
# 			"lineno":"6",
# 			"amt_list": 22.8,
# 			"amt_retail": 22.8,
# 			"amt_receivable": 22.8,
# 			"qtty": 5
# 		},
#         {
# 			"ecode": "AS007",
# 			"sku":"AS00701",
# 			"lineno":"7",
# 			"amt_list": 22.8,
# 			"amt_retail": 22.8,
# 			"amt_receivable": 22.8,
# 			"qtty": 3
# 		},
#         {
# 			"ecode": "AS008",
# 			"sku":"AS00801",
# 			"lineno":"8",
# 			"amt_list": 22.8,
# 			"amt_retail": 22.8,
# 			"amt_receivable": 22.8,
# 			"qtty": 3
# 		}
# 	],
# 	"promotion_list": {
# 		"product_activity_list": [
# 			{
# 				"prom_type_two": 4,
# 				"prom_type_three": "ga1401",
# 				"id":"1",
# 				"ename": "统一买赠1",
# 				"target_item":"amt_receivable",
# 				"prom_type_two_c":"1",
# 				"publish_date":"11111",
# 				"members_only": "n",
# 				"members_group": [
# 					1,
# 					2,
# 					3
# 				],
# 				"is_run_other_pro": "y",
# 				"is_run_store_act": "y",
# 				"is_run_vip_discount": "n",
# 				"max_times": -1,
# 				"exchange_condition": 1,
# 				"gift_condition": 1,
# 				"specific_activities": [
# 					{
# 						"product_list": [
# 							"AS001",
#                             "AS005"
# 						],
# 						"target_type": "amt_receivable",
# 						"operation_set":
# 						[
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 9,
# 								"promotion_lineno":1,
# 								"buy_gifts": {
# 									"product_list": [
# 										{
# 											"ECODE": "AS005"
# 										}
# 									],
# 									"give_value": 1
# 								}
#
# 							}
# 						]
# 					}
# 				]
# 			},
# 			{
# 				"prom_type_two": 4,
# 				"prom_type_three": "ga1402",
# 				"id":"3",
# 				"ename": "梯度买赠1",
# 				"target_item":"amt_receivable",
# 				"prom_type_two_c":"1",
# 				"publish_date":"11111",
# 				"members_only": "n",
# 				"members_group": [
# 					1,
# 					2,
# 					3
# 				],
# 				"is_run_other_pro": "y",
# 				"is_run_store_act": "y",
# 				"is_run_vip_discount": "n",
# 				"max_times": -1,
# 				"exchange_condition": 1,
# 				"gift_condition": 1,
# 				"specific_activities": [
# 					{
# 						"product_list": [
# 							"AS006"
# 						],
# 						"target_type": "qtty",
# 						"operation_set":
# 						[
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 2,
# 								"promotion_lineno":1,
# 								"buy_gifts": {
# 									"product_list": [
# 										{
# 											"ECODE": "AS007"
# 										}
# 									],
# 									"give_value": 1
# 								}
#
# 							},
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 3,
# 								"promotion_lineno":2,
# 								"buy_gifts": {
# 									"product_list": [
# 										{
# 											"ECODE": "AS008"
# 										}
# 									],
# 									"give_value": 2
# 								}
#
# 							}
# 						]
# 					}
# 				]
# 			},
# 			{
# 				"prom_type_two": 4,
# 				"prom_type_three": "ga1403",
# 				"id":"2",
# 				"ename": "组合买赠1",
# 				"target_item":"amt_receivable",
# 				"prom_type_two_c":"1",
# 				"publish_date":"11111",
# 				"members_only": "n",
# 				"members_group": [
# 					1,
# 					2,
# 					3
# 				],
# 				"is_run_other_pro": "y",
# 				"is_run_store_act": "y",
# 				"is_run_vip_discount": "n",
# 				"max_times": -1,
# 				"exchange_condition": 1,
# 				"gift_condition": 1,
# 				"rela_symb_type":"and",
# 				"specific_activities": [
# 					{
# 						"product_list": [
# 							"AS004"
# 						],
# 						"target_type": "qtty",
# 						"operation_set":
# 						[
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 1,
# 								"promotion_lineno":1,
# 								"buy_gifts": {
# 									"product_list": [
# 										{
# 											"ECODE": "AS002"
# 										}
# 									],
# 									"give_value": 1
# 								}
#
# 							}
# 						]
# 					},
# 					{
# 						"product_list": [
# 							"AS001"
# 						],
# 						"target_type": "qtty",
# 						"operation_set":
# 						[
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 1,
# 								"promotion_lineno":1,
# 								"buy_gifts": {
# 									"product_list": [
# 										{
# 											"ECODE": "AS002"
# 										}
# 									],
# 									"give_value": 1
# 								}
#
# 							}
# 						]
# 					}
# 				]
# 			},
# 			{
# 				"prom_type_two": 4,
# 				"prom_type_three": "ga1403",
# 				"id":"4",
# 				"ename": "组合买赠2",
# 				"target_item":"amt_receivable",
# 				"prom_type_two_c":"1",
# 				"publish_date":"11111",
# 				"members_only": "n",
# 				"members_group": [
# 					1,
# 					2,
# 					3
# 				],
# 				"is_run_other_pro": "y",
# 				"is_run_store_act": "y",
# 				"is_run_vip_discount": "n",
# 				"max_times": -1,
# 				"exchange_condition": 1,
# 				"gift_condition": 1,
# 				"rela_symb_type":"and",
# 				"specific_activities": [
# 					{
# 						"product_list": [
# 							"AS006"
# 						],
# 						"target_type": "qtty",
# 						"operation_set":
# 						[
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 1,
# 								"promotion_lineno":1,
# 								"buy_gifts": {
# 									"product_list": [
# 										{
# 											"ECODE": "AS007"
# 										}
# 									],
# 									"give_value": 1
# 								}
#
# 							}
# 						]
# 					},
# 					{
# 						"product_list": [
# 							"AS008"
# 						],
# 						"target_type": "qtty",
# 						"operation_set":
# 						[
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 1,
# 								"promotion_lineno":1,
# 								"buy_gifts": {
# 									"product_list": [
# 										{
# 											"ECODE": "AS007"
# 										}
# 									],
# 									"give_value": 1
# 								}
#
# 							}
# 						]
# 					}
# 				]
# 			}
# 		],
# 		"fullcourt_activity_list": [
# 		]
# 	},
# 	"user":{
# 		"id":"1",
# 		"discount":"1"
# 	}
# }

# json={
# 	"product_list": [
# 		{
# 			"ecode": "AS001",
# 			"sku":"AS00101",
# 			"lineno":"1",
# 			"amt_list": 15,
# 			"amt_retail": 15,
# 			"amt_receivable": 15,
# 			"qtty": 4
# 		},
# 		{
# 			"ecode": "AS002",
# 			"sku":"AS00201",
# 			"lineno":"2",
# 			"amt_list": 19.8,
# 			"amt_retail": 19.8,
# 			"amt_receivable": 19.8,
# 			"qtty": 4
# 		},
#         {
# 			"ecode": "AS003",
# 			"sku":"AS00301",
# 			"lineno":"3",
# 			"amt_list": 29.8,
# 			"amt_retail": 29.8,
# 			"amt_receivable": 29.8,
# 			"qtty": 3
# 		},
#         {
# 			"ecode": "AS004",
# 			"sku":"AS00401",
# 			"lineno":"4",
# 			"amt_list": 29.8,
# 			"amt_retail": 29.8,
# 			"amt_receivable": 29.8,
# 			"qtty": 3
# 		}
# 	],
# 	"promotion_list": {
# 		"product_activity_list": [
# 			{
# 				"prom_type_two": 4,
# 				"prom_type_three": "ga1405",
# 				"id":"4",
# 				"ename": "组合买赠2",
# 				"target_item":"amt_receivable",
# 				"prom_type_two_c":"1",
# 				"publish_date":"11111",
# 				"members_only": "n",
# 				"members_group": [
# 					1,
# 					2,
# 					3
# 				],
# 				"is_run_other_pro": "y",
# 				"is_run_store_act": "y",
# 				"is_run_vip_discount": "n",
# 				"max_times": -1,
# 				"exchange_condition": 1,
# 				"gift_condition": 1,
# 				"rela_symb_type":"and",
# 				"specific_activities": [
# 					{
# 						"product_list": [
# 							"AS002"
# 						],
# 						"target_type": "qtty",
# 						"operation_set":
# 						[
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 1,
# 								"promotion_lineno":1,
# 								"buy_gifts": {
# 									"product_list": [
# 										{
# 											"ECODE": "AS003"
# 										}
# 									],
# 									"give_value": 1
# 								}
#
# 							}
# 						]
# 					},
# 					{
# 						"product_list": [
# 							"AS001"
# 						],
# 						"target_type": "amt_receivable",
# 						"operation_set":
# 						[
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 20,
# 								"promotion_lineno":1,
# 								"buy_gifts": {
# 									"product_list": [
# 										{
# 											"ECODE": "AS003"
# 										}
# 									],
# 									"give_value": 1
# 								}
#
# 							}
# 						]
# 					}
# 				]
# 			}
# 		],
# 		"fullcourt_activity_list": [
# 		]
# 	},
# 	"user":{
# 		"id":"1",
# 		"discount":"1"
# 	}
# }

# json={
# 	"product_list": [
# 		{
# 			"ecode": "AS001",
# 			"sku":"AS00101",
# 			"lineno":"1",
# 			"amt_list": 18.8,
# 			"amt_retail": 18.8,
# 			"amt_receivable": 18.8,
# 			"qtty": 6
# 		},
# 		{
# 			"ecode": "AS002",
# 			"sku":"AS00201",
# 			"lineno":"2",
# 			"amt_list": 19.8,
# 			"amt_retail": 19.8,
# 			"amt_receivable": 19.8,
# 			"qtty": 5
# 		},
#         {
# 			"ecode": "AS003",
# 			"sku":"AS00301",
# 			"lineno":"3",
# 			"amt_list": 29.8,
# 			"amt_retail": 29.8,
# 			"amt_receivable": 29.8,
# 			"qtty": 3
# 		},
#         {
# 			"ecode": "AS004",
# 			"sku":"AS00401",
# 			"lineno":"4",
# 			"amt_list": 29.8,
# 			"amt_retail": 29.8,
# 			"amt_receivable": 29.8,
# 			"qtty": 3
# 		}
# 	],
# 	"promotion_list": {
# 		"product_activity_list": [
# 		],
# 		"fullcourt_activity_list": [
# 			{
# 				"prom_type_two": 6,
# 				"prom_type_three": "pa1501",
# 				"id": "1",
# 				"ename": "全场买免",
# 				"target_item": "amt_receivable",
# 				"prom_type_two_c": "1",
# 				"publish_date": "111111",
# 				"members_only": "n",
# 				"members_group": [],
# 				"is_run_other_pro": "y",
# 				"is_run_store_act": "y",
# 				"is_run_vip_discount": "n",
# 				"max_times": -1,
# 				"exchange_condition": 1,
# 				"gift_condition": 1,
# 				"specific_activities": [
# 					{
# 						"specific_target_type":"amt_receivable",
# 						"comp_symb_type":"ge",
# 						"value_num":10,
# 						"target_type": "qtty",
# 						"operation_set":
# 						[
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 2,
# 								"promotion_lineno":1,
#                                 "buy_from": 1
#
# 							}
# 						]
# 					}
# 				]
# 			}
# 		]
# 	},
# 	"user":{
# 		"id":"1",
# 		"discount":"1"
# 	}
# }

# json={
# 	"product_list": [
# 		{
# 			"ecode": "AS001",
# 			"sku":"AS00101",
# 			"lineno":"1",
# 			"amt_list": 18.8,
# 			"amt_retail": 18.8,
# 			"amt_receivable": 18.8,
# 			"qtty": 6
# 		},
# 		{
# 			"ecode": "AS002",
# 			"sku":"AS00201",
# 			"lineno":"2",
# 			"amt_list": 19.8,
# 			"amt_retail": 19.8,
# 			"amt_receivable": 19.8,
# 			"qtty": 5
# 		},
#         {
# 			"ecode": "AS003",
# 			"sku":"AS00301",
# 			"lineno":"3",
# 			"amt_list": 29.8,
# 			"amt_retail": 29.8,
# 			"amt_receivable": 29.8,
# 			"qtty": 3
# 		},
#         {
# 			"ecode": "AS004",
# 			"sku":"AS00401",
# 			"lineno":"4",
# 			"amt_list": 29.8,
# 			"amt_retail": 29.8,
# 			"amt_receivable": 29.8,
# 			"qtty": 3
# 		}
# 	],
# 	"promotion_list": {
# 		"product_activity_list": [
# 		],
# 		"fullcourt_activity_list": [
# 			{
# 				"prom_type_two": 4,
# 				"prom_type_three": "pa1301",
# 				"id": "1",
# 				"ename": "全场买赠",
# 				"target_item": "amt_receivable",
# 				"prom_type_two_c": "1",
# 				"publish_date": "111111",
# 				"members_only": "n",
# 				"members_group": [],
# 				"is_run_other_pro": "y",
# 				"is_run_store_act": "y",
# 				"is_run_vip_discount": "n",
# 				"max_times": -1,
# 				"exchange_condition": 1,
# 				"gift_condition": 1,
# 				"specific_activities": [
# 					{
# 						"specific_target_type":"amt_receivable",
# 						"comp_symb_type":"ge",
# 						"value_num":10,
# 						"target_type": "qtty",
# 						"operation_set":
# 						[
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 2,
# 								"promotion_lineno":1,
#                                 "buy_gifts": {
#                                     "product_list": [{
#                                         "ecode": "AS005",
#                                         "amt_list": "29.8"
#                                     }],
#                                     "give_value": 2
#                                 },
#                                 "pcond_id": 1
#
# 							}
# 						]
# 					}
# 				]
# 			},
#             {
# 				"prom_type_two": 4,
# 				"prom_type_three": "pa1601",
# 				"id": "2",
# 				"ename": "全场线上买赠",
# 				"target_item": "amt_receivable",
# 				"prom_type_two_c": "1",
# 				"publish_date": "111111",
# 				"members_only": "n",
# 				"members_group": [],
# 				"is_run_other_pro": "y",
# 				"is_run_store_act": "y",
# 				"is_run_vip_discount": "n",
# 				"max_times": -1,
# 				"exchange_condition": 1,
# 				"gift_condition": 1,
# 				"specific_activities": [
# 					{
# 						"specific_target_type":"amt_receivable",
# 						"comp_symb_type":"ge",
# 						"value_num":20,
# 						"target_type": "qtty",
# 						"operation_set":
# 						[
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 2,
# 								"promotion_lineno":1,
#                                 "buy_gifts": {
#                                     "product_list": [{
#                                         "ecode": "AS005",
#                                         "amt_list": "29.8"
#                                     }],
#                                     "give_value": 2
#                                 },
#                                 "pcond_id": 1
#
# 							}
# 						]
# 					}
# 				]
# 			}
# 		]
# 	},
# 	"user":{
# 		"id":"1",
# 		"discount":"1"
# 	}
# }

# json={
#   "promotion_list": {
#     "fullcourt_activity_list": [],
#     "product_activity_list": [
#       {
#         "gift_condition": 1,
#         "prom_type_three": "GA1702",
#         "rela_symb_type": "and",
#         "prom_type_two_c": 50,
#         "specific_activities": [
#           {
#             "pitem_id": 448,
#             "target_type": "QTTY",
#             "operation_set": [
#               {
#                 "promotion_lineno": 1,
#                 "comp_symb_type": "G",
#                 "value_num": 4,
#                 "pcond_id": 684,
#                 "buy_gifts": {
#                   "give_value": 1.00,
#                   "product_list": [
#                     {
#                       "sku": "100001002902AI390",
#                       "amt_list": 1.00,
#                       "ecode": "PM4580253"
#                     }
#                   ]
#                 }
#               },
#               {
#                 "promotion_lineno": 2,
#                 "comp_symb_type": "G",
#                 "value_num": 4,
#                 "pcond_id": 685,
#                 "buy_gifts": {
#                   "give_value": 1.00,
#                   "product_list": [
#                     {
#                       "sku": "100001002902AI400",
#                       "amt_list": 1.00,
#                       "ecode": "PM4580253"
#                     }
#                   ]
#                 }
#               }
#             ],
#             "product_list": [
#               "1000001"
#             ]
#           },
#           {
#             "pitem_id": 449,
#             "target_type": "QTTY",
#             "operation_set": [
#               {
#                 "promotion_lineno": 1,
#                 "comp_symb_type": "G",
#                 "value_num": 9,
#                 "pcond_id": 686,
#                 "buy_gifts": {
#                   "give_value": 1.00,
#                   "product_list": [
#                     {
#                       "sku": "100001002902AI405",
#                       "amt_list": 1.00,
#                       "ecode": "PM4580253"
#                     }
#                   ]
#                 }
#               },
#               {
#                 "promotion_lineno": 2,
#                 "comp_symb_type": "G",
#                 "value_num": 9,
#                 "pcond_id": 687,
#                 "buy_gifts": {
#                   "give_value": 1.00,
#                   "product_list": [
#                     {
#                       "sku": "100001002902AI410",
#                       "amt_list": 1.00,
#                       "ecode": "PM4580253"
#                     }
#                   ]
#                 }
#               }
#             ],
#             "product_list": [
#               "1000001"
#             ]
#           },
#           {
#             "pitem_id": 447,
#             "target_type": "QTTY",
#             "operation_set": [
#               {
#                 "promotion_lineno": 1,
#                 "comp_symb_type": "GE",
#                 "value_num": 1,
#                 "pcond_id": 683,
#                 "buy_gifts": {
#                   "give_value": 1.00,
#                   "product_list": [
#                     {
#                       "sku": "100001002902AI390",
#                       "amt_list": 1.00,
#                       "ecode": "PM4580253"
#                     }
#                   ]
#                 }
#               }
#             ],
#             "product_list": [
#               "1000001"
#             ]
#           }
#         ],
#         "is_run_store_act": "N",
#         "members_only": "N",
#         "prom_type_two": 4,
#         "prom_scope": "GA",
#         "exchange_condition": 1,
#         "ename": "梯度送赠品1",
#         "prom_type_two_code": "GA17_01",
#         "is_run_vip_discount": "N",
#         "max_times": -1,
#         "target_item": "AMT_LIST",
#         "id": 163,
#         "publish_date": 1564023107105,
#         "is_run_other_pro": "N"
#       }
#     ]
#   },
#   "product_list": [
#     {
#       "lineno": "",
#       "amt_receivable": "100.00",
#       "is_buy_gifts": "N",
#       "amt_retail": "100.00",
#       "sku": "100000100001",
#       "amt_list": "100.00",
#       "qtty": 5,
#       "ecode": "1000001",
#       "is_repurchase": "N"
#     }
#   ],
#   "retail_carryway": 1,
#   "user": {
#     "discount": 1,
#     "id": -1
#   }
# }

# json={
#   "promotion_list": {
#     "fullcourt_activity_list": [],
#     "product_activity_list": [{
#       "gift_condition": 1,
#       "prom_type_three": "GA1701",
#       "rela_symb_type": "and",
#       "prom_type_two_c": 50,
#       "specific_activities": [{
#         "target_type": "QTTY",
#         "operation_set": [{
#           "promotion_lineno": 1,
#           "comp_symb_type": "GE",
#           "value_num": 1,
#           "pcond_id": 325,
#           "buy_gifts": {
#             "give_value": 1.00,
#             "product_list": [{
#               "AMT_LIST": 24.50,
#               "ECODE": "0000",
#               "sku": "0000020B390"
#             }, {
#               "AMT_LIST": 24.50,
#               "ECODE": "0000",
#               "sku": "0000020B405"
#             }]
#           }
#         }],
#         "product_list": ["172270251"]
#       }],
#       "is_run_store_act": "N",
#       "members_only": "N",
#       "prom_type_two": 4,
#       "prom_scope": "GA",
#       "exchange_condition": 1,
#       "ename": "46",
#       "prom_type_two_code": "GA17_01",
#       "is_run_vip_discount": "N",
#       "max_times": -1,
#       "target_item": "AMT_LIST",
#       "id": 46,
#       "publish_date": 1563326901000,
#       "is_run_other_pro": "N"
#     }]
#   },
#   "product_list": [{
#     "lineno": "",
#     "amt_receivable": "439.00",
#     "is_buy_gifts": "N",
#     "amt_retail": "439.00",
#     "sku": "1722702510100360",
#     "amt_list": "439.00",
#     "qtty": 2,
#     "ecode": "172270251",
#     "is_repurchase": "N"
#   }],
#   "retail_carryway": 1,
#   "user": {
#     "discount": 1,
#     "id": -1
#   }
# }


# json={
# 	"product_list": [
# 		{
# 			"ecode": "AS001",
# 			"sku":"AS00101",
# 			"lineno":"1",
# 			"amt_list": 15,
# 			"amt_retail": 15,
# 			"amt_receivable": 15,
# 			"qtty": 4
# 		},
# 		{
# 			"ecode": "AS002",
# 			"sku":"AS00201",
# 			"lineno":"2",
# 			"amt_list": 19.8,
# 			"amt_retail": 19.8,
# 			"amt_receivable": 19.8,
# 			"qtty": 4
# 		},
#         {
# 			"ecode": "AS003",
# 			"sku":"AS00301",
# 			"lineno":"3",
# 			"amt_list": 29.8,
# 			"amt_retail": 29.8,
# 			"amt_receivable": 29.8,
# 			"qtty": 3
# 		},
#         {
# 			"ecode": "AS004",
# 			"sku":"AS00401",
# 			"lineno":"4",
# 			"amt_list": 29.8,
# 			"amt_retail": 29.8,
# 			"amt_receivable": 29.8,
# 			"qtty": 3
# 		},
#         {
# 			"ecode": "AS005",
# 			"sku":"AS00501",
# 			"lineno":"4",
# 			"amt_list": 29.8,
# 			"amt_retail": 29.8,
# 			"amt_receivable": 29.8,
# 			"qtty": 3
# 		}
# 	],
# 	"promotion_list": {
# 		"product_activity_list": [
# 			{
# 				"prom_type_two": 4,
# 				"prom_type_three": "ga1401",
# 				"id":"1",
# 				"ename": "统一买赠1",
# 				"target_item":"amt_receivable",
# 				"prom_type_two_c":"2",
# 				"publish_date":"11111",
# 				"members_only": "n",
# 				"members_group": [
# 					1,
# 					2,
# 					3
# 				],
# 				"is_run_other_pro": "y",
# 				"is_run_store_act": "y",
# 				"is_run_vip_discount": "n",
# 				"max_times": -1,
# 				"exchange_condition": 1,
# 				"gift_condition": 1,
# 				"specific_activities": [
# 					{
# 						"product_list": [
# 							"AS004"
# 						],
# 						"target_type": "qtty",
# 						"operation_set":
# 						[
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 2,
# 								"promotion_lineno":1,
# 								"buy_gifts": {
# 									"product_list": [
# 										{
# 											"ECODE": "AS005"
# 										}
# 									],
# 									"give_value": 1
# 								}
#
# 							}
# 						]
# 					}
# 				]
# 			},
# 			{
# 				"prom_type_two": 5,
# 				"prom_type_three": "ga1501",
# 				"id":"4",
# 				"ename": "统一特价换购",
# 				"target_item":"amt_receivable",
# 				"prom_type_two_c":"1",
# 				"publish_date":"11111",
# 				"members_only": "n",
# 				"members_group": [
# 					1,
# 					2,
# 					3
# 				],
# 				"is_run_other_pro": "y",
# 				"is_run_store_act": "y",
# 				"is_run_vip_discount": "n",
# 				"max_times": 2,
# 				"exchange_condition": 1,
# 				"gift_condition": 1,
# 				"rela_symb_type":"and",
# 				"specific_activities": [
# 					{
# 						"product_list": [
# 							"AS001"
# 						],
# 						"target_type": "qtty",
# 						"operation_set":
# 						[
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 1,
# 								"promotion_lineno":1,
# 								"redemption": {
# 									"purchase_condition": 10,
# 									"product_list": [
# 										{
# 											"ecode": "AS002",
# 											"amt_list": "19.8"
# 										}
# 									],
# 									"give_value": 2
# 								},
# 								"pcond_id":1
#
# 							},
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 1,
# 								"promotion_lineno":1,
# 								"redemption": {
# 									"purchase_condition": 20,
# 									"product_list": [
# 										{
# 											"ecode": "AS003",
# 											"amt_list": "29.8"
# 										}
# 									],
# 									"give_value": 2
# 								},
# 								"pcond_id":2
#
# 							}
# 						]
# 					}
# 				]
# 			},
# 			{
# 				"prom_type_two": 5,
# 				"prom_type_three": "ga1506",
# 				"id":"5",
# 				"ename": "统一优惠换购",
# 				"target_item":"amt_receivable",
# 				"prom_type_two_c":"1",
# 				"publish_date":"11111",
# 				"members_only": "n",
# 				"members_group": [
# 					1,
# 					2,
# 					3
# 				],
# 				"is_run_other_pro": "y",
# 				"is_run_store_act": "y",
# 				"is_run_vip_discount": "n",
# 				"max_times": -1,
# 				"exchange_condition": 1,
# 				"gift_condition": 1,
# 				"rela_symb_type":"and",
# 				"specific_activities": [
# 					{
# 						"product_list": [
# 							"AS001"
# 						],
# 						"target_type": "qtty",
# 						"operation_set":
# 						[
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 1,
# 								"promotion_lineno":1,
# 								"redemption": {
# 									"purchase_condition": 5,
# 									"product_list": [
# 										{
# 											"ecode": "AS002",
# 											"amt_list": "19.8"
# 										}
# 									],
# 									"give_value": 2
# 								},
# 								"pcond_id":1
#
# 							},
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 1,
# 								"promotion_lineno":1,
# 								"redemption": {
# 									"purchase_condition": 6,
# 									"product_list": [
# 										{
# 											"ecode": "AS003",
# 											"amt_list": "29.8"
# 										}
# 									],
# 									"give_value": 2
# 								},
# 								"pcond_id":2
#
# 							}
# 						]
# 					},
# 					{
# 						"product_list": [
# 							"AS004"
# 						],
# 						"target_type": "qtty",
# 						"operation_set":
# 						[
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 1,
# 								"promotion_lineno":1,
# 								"redemption": {
# 									"purchase_condition": 5,
# 									"product_list": [
# 										{
# 											"ecode": "AS002",
# 											"amt_list": "19.8"
# 										}
# 									],
# 									"give_value": 2
# 								},
# 								"pcond_id":1
#
# 							},
# 							{
# 								"comp_symb_type": "ge",
# 								"value_num": 1,
# 								"promotion_lineno":1,
# 								"redemption": {
# 									"purchase_condition": 6,
# 									"product_list": [
# 										{
# 											"ecode": "AS003",
# 											"amt_list": "29.8"
# 										}
# 									],
# 									"give_value": 2
# 								},
# 								"pcond_id":2
#
# 							}
# 						]
# 					}
# 				]
# 			}
# 		],
# 		"fullcourt_activity_list": [
# 		]
# 	},
# 	"user":{
# 		"id":"1",
# 		"discount":"1"
# 	}
# }

# json={
# 	"product_list": [
# 		{
# 			"ecode": "AS001",
# 			"sku":"AS00101",
# 			"lineno":"1",
# 			"amt_list": 18.8,
# 			"amt_retail": 18.8,
# 			"amt_receivable": 18.8,
# 			"qtty": 3
# 		},
# 		{
# 			"ecode": "AS002",
# 			"sku":"AS00201",
# 			"lineno":"2",
# 			"amt_list": 19.8,
# 			"amt_retail": 19.8,
# 			"amt_receivable": 19.8,
# 			"qtty": 5
# 		},
#         {
# 			"ecode": "AS003",
# 			"sku":"AS00301",
# 			"lineno":"3",
# 			"amt_list": 29.8,
# 			"amt_retail": 29.8,
# 			"amt_receivable": 29.8,
# 			"qtty": 3
# 		},
#         {
# 			"ecode": "AS004",
# 			"sku":"AS00401",
# 			"lineno":"4",
# 			"amt_list": 24.8,
# 			"amt_retail": 24.8,
# 			"amt_receivable": 24.8,
# 			"qtty": 2
# 		},
#         {
# 			"ecode": "AS005",
# 			"sku":"AS00501",
# 			"lineno":"5",
# 			"amt_list": 22.8,
# 			"amt_retail": 22.8,
# 			"amt_receivable": 22.8,
# 			"qtty": 3
# 		},
#         {
# 			"ecode": "AS006",
# 			"sku":"AS00601",
# 			"lineno":"6",
# 			"amt_list": 22.8,
# 			"amt_retail": 22.8,
# 			"amt_receivable": 22.8,
# 			"qtty": 5
# 		},
#         {
# 			"ecode": "AS007",
# 			"sku":"AS00701",
# 			"lineno":"7",
# 			"amt_list": 22.8,
# 			"amt_retail": 22.8,
# 			"amt_receivable": 22.8,
# 			"qtty": 3
# 		},
#         {
# 			"ecode": "AS008",
# 			"sku":"AS00801",
# 			"lineno":"8",
# 			"amt_list": 22.8,
# 			"amt_retail": 22.8,
# 			"amt_receivable": 22.8,
# 			"qtty": 3
# 		}
# 	],
# 	"promotion_list": {
# 		"product_activity_list": [
# 		],
# 		"fullcourt_activity_list": [
# 			{
# 			  "prom_type_two": 5,
# 			  "prom_type_three": "pa1401",
# 			  "ename": "统一特价换购",
# 			  "id": "1",
# 			  "prom_type_two_c": "3",
# 			  "publish_date": "1212111",
# 			  "members_only": "y",
# 			  "members_group": [
# 				1,
# 				2,
# 				3
# 			  ],
# 			  "is_run_other_pro": "y",
# 			  "is_run_store_act": "y",
# 			  "is_run_vip_discount": "y",
# 			  "max_times": -1,
# 			  "exchange_condition": 1,
# 			  "gift_condition": 1,
# 			  "specific_activities": [
# 				{
# 				  "specific_target_type": "amt_receivable",
# 				  "comp_symb_type": "ge",
# 				  "value_num": 20,
# 				  "target_type": "qtty",
# 				  "operation_set": [
# 					{
# 					  "comp_symb_type": "ge",
# 					  "value_num": 1,
# 					  "target_item": "amt_receivable",
# 					  "redemption": {
# 						"purchase_condition": 10,
# 						"product_list": [
# 						  {
# 							"ecode": "AS002",
# 							"amt_list": "19.8"
# 						  }
# 						],
# 						"give_value": 1
# 					  },
# 					  "pcond_id":1
# 					},
# 					{
# 					  "comp_symb_type": "ge",
# 					  "value_num": 1,
# 					  "target_item": "amt_receivable",
# 					  "redemption": {
# 						"purchase_condition": 12,
# 						"product_list": [
# 						  {
# 							"ecode": "AS001",
# 							"amt_list": "18.8"
# 						  }
# 						],
# 						"give_value": 1
# 					  },
# 					  "pcond_id":2
# 					}
# 				  ]
# 				}
# 			  ]
# 			}
# 		]
# 	},
# 	"user":{
# 		"id":"1",
# 		"discount":"1"
# 	}
# }

# json={"promotion_list":{"fullcourt_activity_list":[{"gift_condition":1,"prom_type_three":"PA1302","rela_symb_type":"and","prom_type_two_c":40,"specific_activities":[{"specific_target_type":"AMT_RECEIVABLE","target_type":"AMT_RECEIVABLE","comp_symb_type":"G","value_num":"0","operation_set":[{"promotion_lineno":1,"comp_symb_type":"GE","value_num":1,"buy_gifts":{"give_value":1,"product_list":[{"amt_list":113,"ecode":"AACN029-2"}]}},{"promotion_lineno":2,"comp_symb_type":"GE","value_num":2,"buy_gifts":{"give_value":1,"product_list":[{"amt_list":219.99,"ecode":"12345600"}]}},{"promotion_lineno":3,"comp_symb_type":"E","value_num":3,"buy_gifts":{"give_value":1,"product_list":[{"amt_list":99,"ecode":"2019070202"}]}},{"promotion_lineno":4,"comp_symb_type":"G","value_num":4,"buy_gifts":{"give_value":1,"product_list":[{"amt_list":219.99,"ecode":"12345600"}]}},{"promotion_lineno":5,"comp_symb_type":"G","value_num":5,"buy_gifts":{"give_value":1,"product_list":[{"amt_list":123,"ecode":"AAEN004-1"}]}}]}],"is_run_store_act":"N","members_only":"N","prom_type_two":4,"prom_scope":"PA","exchange_condition":1,"ename":"测试全场买赠0002","is_run_vip_discount":"N","max_times":0,"target_item":"AMT_LIST","id":83,"publish_date":1562132574000,"is_run_other_pro":"Y"}],"product_activity_list":[{"gift_condition":1,"prom_type_three":"GA1101","rela_symb_type":"and","prom_type_two_c":10,"specific_activities":[{"target_type":"QTTY","execute_product_list":["AAEN004-1","AKLM295-3","12345600","111","ABAP071-5H","TEST","ARHP147-2B","AACN003-4","2019070202","2019070204","2019070201","T1","2019070203"],"operation_set":[{"comp_symb_type":"GE","value_num":1,"discount_value":0.8}],"product_list":["TEST"]}],"is_run_store_act":"N","members_only":"N","prom_type_two":1,"prom_scope":"GA","exchange_condition":1,"ename":"全场统一8折","is_run_vip_discount":"N","max_times":0,"target_item":"AMT_RECEIVABLE","id":77,"publish_date":1562125154000,"is_run_other_pro":"N"}]},"product_list":[{"retailType":"","lineno":1,"amt_receivable":"200.8","is_buy_gifts":"N","amt_retail":"200.8","sku":"TEST102","amt_list":"200.8","qtty":"1","productName":"测试款号","ecode":"TEST","is_repurchase":"N"}],"retail_carryway":"1","user":{"discount":1,"id":-1}}
# json={
#   "promotion_list": {
#     "fullcourt_activity_list": [{
# 			"prom_type_two":2,
# 			"prom_type_two_code ": "PA12-11",
# 			"prom_type_three": "pa1201",
# 			"id": "1",
# 			"ename": "活动名称",
# 			"prom_type_two_c": "2",
# 			"publish_date": "111111",
# 			"members_only": "n",
# 			"members_group": [
# 				1,
# 				2,
# 				3
# 			],
# 			"is_run_other_pro": "y",
# 			"is_run_store_act": "y",
# 			"is_run_vip_discount": "n",
# 			"max_times": -1,
# 			"exchange_condition": 1,
# 			"gift_condition": 1,
# 			"specific_activities": [{
# 				"specific_target_type": "amt_receivable",
# 				"comp_symb_type": "ge",
# 				"value_num": 10,
# 				"target_type": "qtty",
# 				"operation_set": [{
# 					"comp_symb_type": "ge",
# 					"value_num": 2,
# 					"target_item": "amt_receivable",
# 					"money_off_value": 10,
# 				}]
#             }]
#       }],
#     "product_activity_list": [
#
#
#     ]
#   },
#   "product_list": [
#     {
#       "lineno": "",
#       "amt_receivable": "100.00",
#       "is_buy_gifts": "N",
#       "amt_retail": "100.00",
#       "sku": "100000100001",
#       "amt_list": "100.00",
#       "qtty": 7,
#       "ecode": "1000001",
#       "is_repurchase": "N"
#     }
#   ],
#   "retail_carryway": 1,
#   "user": {
#     "discount": 1,
#     "id": -1
#   }
# }
json={
	"promotion_list": {
		"fullcourt_activity_list": [
		{
			"gift_condition": 1,
			"prom_type_three": "PA1702",
			"rela_symb_type": "and",
			"prom_type_two_c": 80,
			"specific_activities": [{
				"pitem_id": 1808,
				"specific_target_type": "DISCOUNT",
				"target_type": "QTTY",
				"comp_symb_type": "GE",
				"value_num": "0.50",
				"operation_set": [{
					"promotion_lineno": 1,
					"comp_symb_type": "GE",
					"value_num": 1,
					"pcond_id": 2999,
					"buy_gifts": {
						"give_value": 2.00,
						"product_list": [{
							"sku": "1017000122211",
							"amt_list": 99.00,
							"ecode": "10170001"
						}]
					}
				}]
			}, {
				"pitem_id": 1809,
				"specific_target_type": "DISCOUNT",
				"target_type": "QTTY",
				"comp_symb_type": "GE",
				"value_num": "0.50",
				"operation_set": [{
					"promotion_lineno": 1,
					"comp_symb_type": "G",
					"value_num": 0,
					"pcond_id": 3000,
					"buy_gifts": {
						"give_value": 2.00,
						"product_list": [{
							"sku": "100000100001",
							"amt_list": 100.00,
							"ecode": "1000001"
						}]
					}
				}]
			}],
			"is_run_store_act": "Y",
			"members_only": "N",
			"prom_type_two": 4,
			"prom_scope": "PA",
			"exchange_condition": 1,
			"ename": "F7303",
			"prom_type_two_code": "PA17_01",
			"is_run_vip_discount": "N",
			"max_times": -1,
			"target_item": "AMT_LIST",
			"id": 339,
			"publish_date": 1564550802000,
			"is_run_other_pro": "Y"
		},
		{
			"gift_condition": 1,
			"prom_type_three": "PA1602",
			"rela_symb_type": "and",
			"prom_type_two_c": 70,
			"specific_activities": [{
				"pitem_id": 1820,
				"specific_target_type": "DISCOUNT",
				"target_type": "QTTY",
				"comp_symb_type": "GE",
				"value_num": "0.50",
				"operation_set": [{
					"promotion_lineno": 1,
					"comp_symb_type": "GE",
					"value_num": 1,
					"pcond_id": 3012,
					"buy_gifts": {
						"give_value": 1.00,
						"product_list": [{
							"sku": "1017000122211",
							"amt_list": 99.00,
							"ecode": "10170001"
						}]
					}
				}]
			}, {
				"pitem_id": 1821,
				"specific_target_type": "DISCOUNT",
				"target_type": "QTTY",
				"comp_symb_type": "GE",
				"value_num": "0.50",
				"operation_set": [{
					"promotion_lineno": 1,
					"comp_symb_type": "G",
					"value_num": 0,
					"pcond_id": 3013,
					"buy_gifts": {
						"give_value": 1.00,
						"product_list": [{
							"sku": "100000100001",
							"amt_list": 100.00,
							"ecode": "1000001"
						}]
					}
				}]
			}],
			"is_run_store_act": "Y",
			"members_only": "N",
			"prom_type_two": 4,
			"prom_scope": "PA",
			"exchange_condition": 1,
			"ename": "F7301",
			"prom_type_two_code": "PA16_01",
			"is_run_vip_discount": "N",
			"max_times": -1,
			"target_item": "AMT_LIST",
			"id": 345,
			"publish_date": 1564553646000,
			"is_run_other_pro": "Y"
		},
		{
			"gift_condition": 1,
			"prom_type_three": "PA1601",
			"rela_symb_type": "and",
			"prom_type_two_c": 70,
			"specific_activities": [{
				"pitem_id": 1745,
				"specific_target_type": "DISCOUNT",
				"target_type": "QTTY",
				"comp_symb_type": "GE",
				"value_num": "0.50",
				"operation_set": [{
					"promotion_lineno": 1,
					"comp_symb_type": "GE",
					"value_num": 1,
					"pcond_id": 2930,
					"buy_gifts": {
						"give_value": 1.00,
						"product_list": [{
							"sku": "100000100001",
							"amt_list": 100.00,
							"ecode": "1000001"
						}]
					}
				}]
			}],
			"is_run_store_act": "Y",
			"members_only": "N",
			"prom_type_two": 4,
			"prom_scope": "PA",
			"exchange_condition": 1,
			"ename": "F730",
			"prom_type_two_code": "PA16_01",
			"is_run_vip_discount": "N",
			"max_times": -1,
			"target_item": "AMT_LIST",
			"id": 319,
			"publish_date": 1564457360000,
			"is_run_other_pro": "Y"
		}],
		"product_activity_list": [
		{
			"gift_condition": 1,
			"prom_type_three": "GA1701",
			"rela_symb_type": "and",
			"prom_type_two_c": 50,
			"specific_activities": [{
				"pitem_id": 1844,
				"target_type": "QTTY",
				"operation_set": [{
					"promotion_lineno": 1,
					"comp_symb_type": "GE",
					"value_num": 1,
					"pcond_id": 3039,
					"buy_gifts": {
						"give_value": 1.00,
						"product_list": [{
							"sku": "100000100001",
							"amt_list": 100.00,
							"ecode": "1000001"
						}]
					}
				}],
				"product_list": ["1000001"]
			}],
			"is_run_store_act": "N",
			"members_only": "N",
			"prom_type_two": 4,
			"prom_scope": "GA",
			"exchange_condition": 1,
			"ename": "7/29",
			"prom_type_two_code": "GA17_01",
			"is_run_vip_discount": "Y",
			"max_times": -1,
			"target_item": "AMT_LIST",
			"id": 355,
			"publish_date": 1564561063000,
			"is_run_other_pro": "Y"
		},
		{
			"gift_condition": 1,
			"prom_type_three": "GA1803",
			"rela_symb_type": "and",
			"prom_type_two_c": 60,
			"specific_activities": [{
				"pitem_id": 1776,
				"target_type": "QTTY",
				"operation_set": [{
					"promotion_lineno": 1,
					"comp_symb_type": "GE",
					"value_num": 1,
					"pcond_id": 2960,
					"buy_gifts": {
						"give_value": 1.00,
						"product_list": [{
							"sku": "1017000122211",
							"amt_list": 99.00,
							"ecode": "10170001"
						}]
					}
				}, {
					"promotion_lineno": 2,
					"comp_symb_type": "GE",
					"value_num": 1,
					"pcond_id": 2961,
					"buy_gifts": {
						"give_value": 1.00,
						"product_list": [{
							"sku": "100000100001",
							"amt_list": 100.00,
							"ecode": "1000001"
						}]
					}
				}],
				"product_list": []
			}, {
				"pitem_id": 1777,
				"target_type": "QTTY",
				"operation_set": [{
					"promotion_lineno": 1,
					"comp_symb_type": "G",
					"value_num": 1,
					"pcond_id": 2960,
					"buy_gifts": {
						"give_value": 1.00,
						"product_list": [{
							"sku": "1017000122211",
							"amt_list": 99.00,
							"ecode": "10170001"
						}]
					}
				}, {
					"promotion_lineno": 2,
					"comp_symb_type": "G",
					"value_num": 1,
					"pcond_id": 2961,
					"buy_gifts": {
						"give_value": 1.00,
						"product_list": [{
							"sku": "100000100001",
							"amt_list": 100.00,
							"ecode": "1000001"
						}]
					}
				}],
				"product_list": ["1000001"]
			}],
			"is_run_store_act": "Y",
			"members_only": "N",
			"prom_type_two": 4,
			"prom_scope": "GA",
			"exchange_condition": 1,
			"ename": "B7293",
			"prom_type_two_code": "GA18_01",
			"is_run_vip_discount": "Y",
			"max_times": -1,
			"target_item": "AMT_RECEIVABLE",
			"id": 301,
			"publish_date": 1564469494000,
			"is_run_other_pro": "Y"
		},
		{
			"gift_condition": 1,
			"prom_type_three": "GA1701",
			"rela_symb_type": "and",
			"prom_type_two_c": 50,
			"specific_activities": [{
				"pitem_id": 1845,
				"target_type": "QTTY",
				"operation_set": [{
					"promotion_lineno": 1,
					"comp_symb_type": "GE",
					"value_num": 2,
					"pcond_id": 3040,
					"buy_gifts": {
						"give_value": 100.00,
						"product_list": [{
							"sku": "1017000122211",
							"amt_list": 99.00,
							"ecode": "10170001"
						}]
					}
				}],
				"product_list": ["1000001"]
			}],
			"is_run_store_act": "Y",
			"members_only": "N",
			"prom_type_two": 4,
			"prom_scope": "GA",
			"exchange_condition": 1,
			"ename": "A",
			"prom_type_two_code": "GA17_01",
			"is_run_vip_discount": "N",
			"max_times": -1,
			"target_item": "AMT_LIST",
			"id": 351,
			"publish_date": 1564561927325,
			"is_run_other_pro": "N"
		}]
	},
	"product_list": [{
		"lineno": "",
		"amt_receivable": "100.00",
		"is_buy_gifts": "N",
		"amt_retail": "100.00",
		"sku": "100000100001",
		"amt_list": "100.00",
		"qtty": 2,
		"ecode": "1000001",
		"is_repurchase": "N"
	}],
	"retail_carryway": 1,
	"user": {
		"discount": 1,
		"id": -1
	}
}
result = acceptParams(json['product_list'], json['promotion_list'], json['user'],1)
print (result)

rr=[]
for i in range(6):
	if i==0:
		rr.append(0)
	elif i==1:
		rr.append(1)
	elif i==2:
		rr.append(0)
	else:
		rr.append(1)

print(rr)

rrr="shanghaishipudongxinqu"
tttt="shanghaishi"
if tttt in rrr:
	print(444444)

# a=4.5
# b=a
# c=a-1
# print(c)
# print(b)
#
# r=1
# for i in range(0,3):
# 	print(i)

# import sys
#
# print(sys.modules)

