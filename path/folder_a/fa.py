import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)

# 相当于添加主目录路径
add_path = os.path.join(current_dir,"../")
sys.path.append(add_path)
print(sys.path)

import folder_b.fb as fb

fb.print_fb()



def print_fa():
    print("This is fa!")