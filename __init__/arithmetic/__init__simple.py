#
# @file __init__.py
#

# 导入模块的各种函数
import arithmetic.add
import arithmetic.sub
import arithmetic.mul
import arithmetic.dev
import arithmetic.print_a4

# 重定义各种函数
add = arithmetic.add.add
sub = arithmetic.sub.sub
mul = arithmetic.mul.mul
dev = arithmetic.dev.dev

print_a4 = arithmetic.print_a4.print_a4