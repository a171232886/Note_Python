import os
from xml.dom import minidom
"""
参考：
1. https://blog.csdn.net/qq_36072270/article/details/105295539
2. https://docs.python.org/zh-cn/3/library/xml.dom.minidom.html
3. https://blog.csdn.net/m0_37102093/article/details/109622710
"""
def read_xml(path_or_str):
        if os.path.exists(path_or_str):
            #解析xml文件(句柄或文件路径)
            doc = minidom.parse(path_or_str)  
        else:
            #解析xml字符串
            doc = minidom.parseString(path_or_str)  
        root_node = doc.documentElement  #获得根节点

        print(f"root_node.nodeName = {root_node.nodeName}")  # 结点名称
        print(f"root_node.nodeType = {root_node.nodeType}")  # 结点类型  （元素结点，文本结点，属性结点）
        print(f"root_node.childNodes = {root_node.childNodes}")  # 所有子节点，为列表

        print(root_node.childNodes[1].attributes)

if __name__ == "__main__":
    read_xml("/home/wh/Desktop/code/python_note/xml/test.xml")