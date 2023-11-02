import time
"""
1. 装饰器可以是类，也可以是函数
2. 被装饰的可以是类，也可是函数
"""

"""
类作为装饰器

此时 Timer 等价于
def timeit(f):

    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(end-start)
        return result
    
    return wrapper
"""

class Timer:
    def __init__(self, func) -> None:
        self.func = func

    def __call__(self, *args, **kwargs):
        start = time.time()
        ret = self.func(*args, **kwargs)
        end = time.time()
        print(end-start)
        return ret 

@Timer
def add(a, b):
    return a + b

# 等价于
# add = Timer(add)

# NOTE: 
# 1. 此时add从函数变成了Timer类的对象
# 2. Timer(add) 调用Timer.__init__()
# 3. add(2, 3) 调用Timer.__call__()

print(add(2, 3))

print(type(add)) # <class '__main__.Timer'>

