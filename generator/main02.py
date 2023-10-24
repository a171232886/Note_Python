
def gen(num):
    while num > 0:
        """
        tmp = yield num的两步行为
        1. 将 num 返回
        2. 等待用户传入的值，并将其赋值给tmp
        """
        tmp = yield num
        if tmp is not None:
            num = tmp
        num -= 1

g = gen(5)

first = next(g)
print(f"first: {first}")

# 生成器的sen用法
print(f"send: {g.send(10)}")

# for 会调用next(g)
# 对于生成器而言
# next(g) 和 g.send(None) 是相同的
for i in g:
    print(i)