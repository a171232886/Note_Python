#
# @file __init__.py
#

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(sys.path)

# 导入模块的各种函数
import print_hello_down

# 重定义各种函数
print_hello_down = print_hello_down.print_hello_down