# staticmethod 
# 在类中使用此装饰器的函数，相当于一个普通函数
# 只是放在这个class的命名空间下。
# 类似于C++中的类的静态函数
#
# 提供了一种封装函数的办法
#
# staticmethod的Cpython的底层实现使用到了描述器

class A:
    @staticmethod
    def f(x):
        print(x)

A.f(1)
A().f(1)

# classmethod
# classmethod 与 staticmethod 的区别在于， 
# classmethod的第一个参数必需是class，但实际调用时不需要传入class
class A:
    @classmethod
    def f(cls, x):
        print(cls, x)

A.f(1)
A().f(1)