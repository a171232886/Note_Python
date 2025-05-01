"""
最简单的装饰器，但最能说明其本质

参考：https://www.bilibili.com/video/BV1Gu411Q7JV/
"""

def dec(f):
    return 1
@dec
def fun(x):
    return x + 1

# NOTE: 装饰器的写法完全等价于
# fun = dec(fun)
# 即：将函数fun传入装饰器函数dec，装饰器函数的返回值命名为fun

print(fun)  # 输出1