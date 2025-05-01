"""
了解装饰器的前置知识：
1. python中的函数只是一个对象：
    函数名相当于变量名
    函数内容相当于变量内容
2. 函数可以作为一个参数传入另一个函数
3. 函数也可以作为另一个函数的返回值

参考：https://www.bilibili.com/video/BV1Gu411Q7JV/
"""

# 函数作为参数传入
def fun(f, x):
    return f(x)

def fun1(x):
    return x * 2

def fun2(x):
    return x * 3

print(fun(fun1, 2))
print(fun(fun2, 2))

# 函数作为返回值传出
def outer(n):

    # 将传入的n用于定义新函数 
    def inner(x):
        return x * n
    
    return inner

f1 = outer(2)
f2 = outer(3)

print(f1(2))
print(f2(2))

"""
注意：
1. “函数作为返回值传出”的例子，存在闭包的概念
2. n对于inner而言是自由变量，因为它并未在inner中绑定任何值（没有被赋初值）
   而n是outer的局部变量
3. 按《流畅的python》第9.6小节定义：闭包就是延伸了作用域的函数。
    此时inner是闭包，因为它使用了来自外部函数outer的局部变量。
    注意：闭包使用的外部函数的局部变量，而不是全局变量
"""