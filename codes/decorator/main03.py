import time

# 常见的不带参数装饰器

def timeit(f):

    # NOTE: wrapper 更普遍的的定义是
    # def wrapper(*args, **kwargs) 
    #    # something
    #    f(*args, **kwargs)
    #    # something 
    # 此时可接受任意参数
    def wrapper(x):
        start = time.time()
        result = f(x)
        end = time.time()
        print(end-start)
        return result
    
    return wrapper

@timeit
def func(x):
    time.sleep(x)

# 装饰器写法相当于 func = timeit(func)


func = timeit(func)
func(1)