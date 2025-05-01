"""
with 需要额外调用类的__enter__和__exit__函数

当__init__和__enter__遇到错误时，则中断，不执行__exit__
"""

class Test:
    def __init__(self, num):
        print("__init__")
        self.num = num

    def __enter__(self):
        # 进入with语句时执行
        # 比如文件读取中的打开文件操作
        print("__enter__")
        self.num = 100

        # 返回值赋予with ... as <var>中as后的变量
        # 通常返回self
        return self

    def __exit__(self, excepetion, value, traceback):
        # 退出with语句时执行
        # 比如关闭文件操作
        print("__exit__")
        
    def get(self):
        # 一些其他功能函数
        return self.num

with Test(10) as t:
    a = t.get()
    print(a)


"""
执行结果为
__init__
__enter__
100
__exit__
"""