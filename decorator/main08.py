"""
用于装饰类的装饰器（类的装饰器）: 带参数
"""

def outer(perfix):

    def add_str(cls):

        def __str__(self):
            self.__dict__["prefix"] = perfix
            return str(self.__dict__)
        
        cls.__str__ = __str__
        return cls
    
    return add_str

@outer("Hello")
class MyObject:
    def __init__(self, a, b):
        self.a = a
        self.b = b

# 等价于
# MyOject = outer("Hello")(MyOject)

o = MyObject(1, 2)
print(o)