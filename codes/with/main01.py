"""
with 上下文管理器：常用于读写文件、加锁和socket
可以使代码变简洁且安全
"""

# 常用方法
with open("1.txt", 'r') as file:
    string = file.readline()
    print(string)

# 等效于
file = open("1.txt", 'r')
try:
    string = file.readline()
    print(string)
finally:
    # 主动处理file.close() 
    file.close()       