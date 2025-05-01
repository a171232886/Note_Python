"""
问题：python的函数参数传递作用方式需要探究，并非简单的C++中的引用传递

以下脚本执行结果为

{'a': 'a', 'b': 'b', 'c': 'c'}
{'a': 'a', 'b': 'b', 'c': {}}
{'a': 'a', 'b': 'b', 'c': {'ds': 'ds'}}

fun2的函数内的修改并未传递出来
"""

def fun1(x):
    x["c"] = "c"

def fun2(x):
    x = {"ds": "ds"}

def fun3(x):
    c = {"ds": "ds"}
    x["c"] = c

def main():
    d1 = {"a": "a", "b": "b", "c": {}}
    d2 = {"a": "a", "b": "b", "c": {}}
    d3 = {"a": "a", "b": "b", "c": {}}

    fun1(d1)
    fun2(d2["c"])
    fun3(d3)

    print(d1)
    print(d2)
    print(d3)

if __name__ == "__main__":
    main()