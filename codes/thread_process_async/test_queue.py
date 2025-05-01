import queue

"""
注意: 
当队列已满时，queue.put会阻塞
当队列为空时，queue.get会阻塞
"""

def test_queue():
    # 创建一个队列
    q = queue.Queue()

    # 添加元素
    q.put("hello")

    # 获取元素
    res = q.get()
    print(res)

    # 查看元素个数
    num = q.qsize()

    # 判断队列是否为空
    flag1 = q.empty()

    # 判断队列是否已满
    flag2 = q.full()
    
    return

def test2():
    q = queue.Queue()
    # 空队列使用get，此时会阻塞
    print("Hello")
    res = q.get()
    print(res)
    print("Hello")

def test3():
    q = queue.Queue(maxsize=2)
    q.put("Hello")
    q.put("World")
    print("Hello")
    # 满队列使用put，此时会阻塞
    q.put("!")
    print("Hello")

if __name__ == "__main__":
    test_queue()
    test2()
    test3()