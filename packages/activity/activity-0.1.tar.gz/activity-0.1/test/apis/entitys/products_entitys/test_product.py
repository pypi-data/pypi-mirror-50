import unittest
from pro.apis.entitys.products_entitys.product import Product
from pro.apis.entitys.products_entitys.product_seat import ProductSeat
import json

class ProductTest(unittest.TestCase):

    def test_getMaxAmtReceivable_when_hasone_then_returnone(self):
        class ProductMock(Product):
            def __init__(self, obj):
                self.productSeatList = obj["productSeatList"]

        class ProductSeatMock(ProductSeat):
            def __init__(self, obj):
                self.amt_receivable = obj["amt_receivable"]
                self.seat = obj["seat"]
                self.is_run_other_pro = obj["is_run_other_pro"]


        p1 = ProductSeatMock({"amt_receivable": 5, "seat": False, "is_run_other_pro": True})
        p2 = ProductSeatMock({"amt_receivable": 6, "seat": True, "is_run_other_pro": False})
        p3 = ProductSeatMock({"amt_receivable": 7, "seat": False, "is_run_other_pro": True})
        p4 = ProductSeatMock({"amt_receivable": 8, "seat": False, "is_run_other_pro": False})

        productSeatList = [p1, p2, p3, p4]
        productMock = ProductMock({"productSeatList": productSeatList})
        self.assertEqual(p3, productMock.getMaxAmtReceivable())
        


    def test_getMaxAmtReceivable_when_hasnull_then_returnnull(self):
        class ProductMock(Product):
            def __init__(self, obj):
                self.productSeatList = obj["productSeatList"]

        class ProductSeatMock(ProductSeat):
            def __init__(self, obj):
                self.amt_receivable = obj["amt_receivable"]
                self.seat = obj["seat"]
                self.is_run_other_pro = obj["is_run_other_pro"]


        p1 = ProductSeatMock({"amt_receivable": 5, "seat": True, "is_run_other_pro": True})
        p2 = ProductSeatMock({"amt_receivable": 6, "seat": True, "is_run_other_pro": True})
        p3 = ProductSeatMock({"amt_receivable": 7, "seat": False, "is_run_other_pro": False})
        p4 = ProductSeatMock({"amt_receivable": 8, "seat": False, "is_run_other_pro": False})

        productSeatList = [p1, p2, p3, p4]
        productMock = ProductMock({"productSeatList": productSeatList})
        self.assertEqual(None, productMock.getMaxAmtReceivable())

if __name__=="__main__":
    ProductTest()


