"""
装饰器：用于修改函数行为，而不对函数本身修改
1. 广泛应用于日志，flask，输入变量检测等
2. 作用原理
    - 将函数名（句柄）传入装饰器函数
    - 在装饰器函数中设定一些额外功能
"""

def dec(fun):
    def warpper():
        print("dec1")
        fun()
        print("dec2")
        return fun()
    return warpper()

@dec
def fun():
    print("fun")


if __name__ == "__main__":
    fun