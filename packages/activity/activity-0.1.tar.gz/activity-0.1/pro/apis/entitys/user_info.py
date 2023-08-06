# encoding=utf-8

from pro.utils.pro_exception import ProException

# 会员模板类
class UserInfo(object):
    def __init__(self, obj):

        self.id = None
        self.discount = None
        if obj is None or 'id' not in obj:
            return
        if obj['id'] is not None and obj['id']:
            self.id = int(obj['id'])
            self.discount = 1
        if self.id is not None and  obj.get('discount'):
            self.discount = float(obj['discount'])

    # def __str__(self):
    #     return str(self.__dict__)
