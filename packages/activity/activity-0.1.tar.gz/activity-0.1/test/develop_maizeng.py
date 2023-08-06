import json
import operator

from collections import Counter
from pro.apis.main import acceptParams

with open("./tmp/productest.json", encoding="utf8") as f:
    json_python = json.load(f)
    json_product = json_python["product_list"]
    json_promotion = json_python["promotion_list"]
    json_user = json_python["user"]
    retail_carryway=json_python["retail_carryway"]

print(acceptParams(json_product, json_promotion, json_user, retail_carryway))
