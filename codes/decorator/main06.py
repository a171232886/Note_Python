import time

"""
类作为装饰器：带参数
"""

class Timer:
    def __init__(self, prefix) -> None:
        self.prefix = prefix

    def __call__(self, func):
            
        def warpper(*args, **kwargs):
            start = time.time()
            ret = func(*args, **kwargs)
            end = time.time()
            print(end-start)
            return ret 
        
        return warpper
    
@Timer(prefix="current time: ")
def add(a, b):
    return a+b

# 等价于
# add = Timer(prefix="current time: ")(add)

print(add(2,3))
