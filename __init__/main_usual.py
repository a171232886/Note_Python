#
# @file main.py
#

import arithmetic.add
import arithmetic.sub as sub

from arithmetic.mul import mul
from arithmetic import dev


""" 
arithmetic不存在__init__.py时，正常的函数调用
(注意把arithmetic/__init__.py重命名)

参考：
1. https://zhuanlan.zhihu.com/p/115350758
"""

def letscook(x, y, oper):
    r = 0
    if oper == "+":
        r = arithmetic.add.add(x, y)
    elif oper == "-":
        r = sub.sub(x, y)
    elif oper == "*":
        r = mul(x, y)
    else:
        r = dev.dev(x, y)

    print("{} {} {} = {}".format(x, oper, y, r))

if __name__ == "__main__":

    x, y = 3, 8

    letscook(x, y, "+")
    letscook(x, y, "-")
    letscook(x, y, "*")
    letscook(x, y, "/")