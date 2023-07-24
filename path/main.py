"""
针对模块导入路径设置：
目标：
    1. 在任何目录下，执行python脚本，均能正确导入本项目内的模块或函数
    2. 设置方法通用，尽在py脚本开头添加内容
    3. 项目内所有模块的导入，均基于主目录进行

关键函数、变量：
    1. __file__ python内置变量, 当前文件的绝对路径
    2. sys.path 系统环境变量

python模块导入路径构成（依次搜索）：
    1. 当前主目录（自动添加）
    2. PATHONPATH    
        可手动添加
    3. 标准链接库目录（系统内置）
    4. 路径文件（.pth文件）
        通常不用
    通常是基于PATHONPATH进行添加路径
    
参考：
1. https://blog.csdn.net/cckavin/article/details/85392392
2. https://www.cnblogs.com/ljhdo/p/10674242.html
"""

"""
通用的程序
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__))) # 主目录下文件使用
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")) # 主目录下的一级目录中文件使用
"""

import os
import sys
print(__file__)
current_dir = os.path.dirname(os.path.abspath(__file__)) # 获取当前文件所在文件夹的绝对路径
print(current_dir)
print(sys.path) # 会默认添加当前文件所在的绝对路径

from folder_a import fa
from folder_b import fb


def main():
    fa.print_fa()
    fb.print_fb()

if __name__ == "__main__":
    main
