
"""
生成器 generator：
1. 生成器是一种特殊的迭代器
2. 迭代器在运行时，会将迭代状态保存在一个对象里
    而生成器会将迭代状态保存在函数栈帧（frame）里
"""

# gen是生成器函数
def gen(num):
    while num > 0:
        # 生成器函数中的关键字yield
        # yield 对应的字节码是YIELD_VALUE，操作是
        # 1. 函数return当前值，保存函数栈帧的状态，相当于函数暂停
        # 2. next(<函数>)时，会直接从下一行开始运行
        yield num
        num -= 1
    
    # 在生成器函数中的return <value>，
    # 等价于 raise StopIteration
    # 获取 <value> 需要 catch StopIteration
    return

# g是生成器对象
g = gen(5)

# 迭代器的用法
for i in g:
    print(i)