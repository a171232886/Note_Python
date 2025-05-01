"""
用于装饰类的装饰器（类的装饰器）
"""

def add_str(cls):
    
    def __str__(self):
        return str(self.__dict__)
    
    # 替换原来class中的__str__
    cls.__str__ = __str__
    return cls

@add_str
class MyObject:
    def __init__(self, a, b):
        self.a = a
        self.b = b


# 等价于
# MyOject = add_str(MyOject)
# 给add_str传入一个类，传出也是一个类

o = MyObject(1, 2)
print(o)