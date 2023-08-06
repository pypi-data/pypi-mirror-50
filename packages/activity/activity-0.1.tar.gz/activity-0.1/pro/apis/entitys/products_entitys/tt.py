class Person():
    def __init__(self) -> None:
        super().__init__()
        self.a = 1
        self.b = 2
        self.c = 3


p = Person()

r = "a"
print(getattr(p,r))