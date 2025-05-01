# 实现一个链表

# iterable
class Node:
    def __init__(self, name) -> None:
        self.name = name
        self.next = None

    def __iter__(self):
        node = self
        while node is not None:
            yield node
            node = node.next
    
node1 = Node("node1")
node2 = Node("node2")
node3 = Node("node3")
node1.next = node2
node2.next = node3


# 用法1
for node in node1:
    print(node.name)

# 用法2
it = iter(node1) # 获取iterator
first = next(it) # 跳过第一个元素

for node in it:
    print(node.name)    