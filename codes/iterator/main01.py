# 实现一个链表

# iterator
class NodeIter:
    def __init__(self, node) -> None:
        self.curr_node = node # 状态

    def __next__(self):
        if self.curr_node is None:
            raise StopIteration

        node = self.curr_node
        self.curr_node = self.curr_node.next

        return node
    
    def __iter__(self):
        # 为满足用法2，
        # Python文档官方规定iterator应该也是iterable
        return self

# iterable
class Node:
    def __init__(self, name) -> None:
        self.name = name
        self.next = None

    def __iter__(self):
        return NodeIter(self)
    
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