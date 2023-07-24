#
# @file __init__.py
#

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(sys.path)

# 导入模块的各种函数
import add
import sub
import mul
import dev
import print_a4
import hello

# 重定义各种函数
add = add.add
sub = sub.sub
mul = mul.mul
dev = dev.dev

print_a4 = print_a4.print_a4
# print_hello = hello.print_hello