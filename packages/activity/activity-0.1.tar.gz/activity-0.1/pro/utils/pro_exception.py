# encoding=utf-8

class ProException(RuntimeError):
    def __init__(self, args):
        self.arg = ""
        if len(args)>0:
            for i in args:
               self.arg+=i

