"""
可迭代对象 iterable：
    1. list, str, set, dict，file
    2. 数据保存者，可以没有状态，但需要有能力产生iterator
    3. 必需有__iter__()或者__getitem__()来保证在调用iter()时返回iterator

迭代器 iterator：
    1. 一个表示数据流的对象，通过调用__next__()获取下一个对象
    2. 有状态的，不必实现一个interface修改iterable中的数据
"""

# lst 是一个iteratable
lst = [0, 1, 3]

# for-loop 首先会执行iter(lst)，提取一个迭代器
# 再执行next(lst)
for i in lst:
    print(i)