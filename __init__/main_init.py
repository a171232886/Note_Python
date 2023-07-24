import arithmetic as a4
import sys
print(sys.path)

""" 
arithmetic存在__init__.py时，
    1. 在import arithmetic时，首先执行arithmetic中的__init__.py
    2. __init__.py负责向用户提供接口，而屏蔽细节

__init__.py的内容：通常分为两部分
    1. 导入模块的各种函数
        相当于C++的头文件
    2. 重定义各种函数
        对于用户而言，相当于实现<包名.函数名>的简单调用，
        而不必<包名.文件夹名1.文件夹名2.....文件名.函数名>

注意：
    1. 使用__init__.py需要避免命名冲突
    2. 不要在__init__.py添加复杂函数
        因为每次import arithmetic都会执行__init__.py这会影响速度    

参考：
1. https://zhuanlan.zhihu.com/p/115350758
"""

def letscook(x, y, oper):
    r = 0
    if oper == "+":
        r = a4.add(x, y)
    elif oper == "-":
        r = a4.sub(x, y)
    elif oper == "*":
        r = a4.mul(x, y)
    else:
        r = a4.dev(x, y)

    print("{} {} {} = {}".format(x, oper, y, r))

if __name__ == "__main__":

    # x, y = 3, 8

    # letscook(x, y, "+")
    # letscook(x, y, "-")
    # letscook(x, y, "*")
    # letscook(x, y, "/")

    # a4.print_a4(3,8)
    a4.hello.print_hello()