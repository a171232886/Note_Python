
"""
利用描述器的四种优先级，
可分析t.hello和A.hello到底输出什么

在研究情形2时，应注释掉__set__函数，否则不对
这可能是由于__set__的功能导致
"""

class Des:

    def __get__(self, obj, objtype):
        return "__get__"
    
    def __set__(self, obj, objtype):
        print("This is set")
        return "__set__"

    print("class Hello")
    
class Test:
    hello = Des()

    def __init__(self) -> None:
        self.hello = "hello"
        print("init", self.hello)


t = Test()
print(t.__dict__)
print(t.hello)

# 把Test.hello理解成一种无法初始化的临时对象
# 可能比较贴切
print(Test.hello)