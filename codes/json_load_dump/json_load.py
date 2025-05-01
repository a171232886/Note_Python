import os
os.chdir("/home/dell/wh/code/test/NEW")
import json

""" 未完成！
json中load和loads区别
1. json.loads处理字符串
2. json.load处理文件流

参考：
    1. https://docs.python.org/3/library/json.html
    2. https://blog.csdn.net/daerzei/article/details/100598901
"""


def main():
    with open("test_dict.json",'r') as file:
        file_dict = json.load(file)
    # with open("test_num.json",'r') as file:
    #     file_num = json.load(file)    
    with open("test_list.json",'r') as file:
        file_list = json.load(file)    

    pass

if __name__ == "__main__":
    main()