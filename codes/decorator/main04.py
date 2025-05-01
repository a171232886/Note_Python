import time

# 带参数装饰器

def timeit(iteration):

    def inner(f):

        def wrapper(*args, **kwargs):
            for i in range(iteration):
                start = time.time()
                result = f(*args, **kwargs)
                end = time.time()
                print(end-start)
            return result
        
        return wrapper
    
    return inner


# @timeit(10)
def func(x):
    time.sleep(x)

# NOTE: 此时带参数装饰器写法相当于
# func = timeit(10)(func)
# 即: 先执行timeit(10)获取inner，后执行inner(func)获取wrapper

func(1)
