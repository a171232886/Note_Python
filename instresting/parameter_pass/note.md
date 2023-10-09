# 问题

为什么func2的修改没有传递出来

```python
def fun1(x):
    x[0] = 1
    x[1] = 2
def fun2(x):
    x = [1, 2]


def main():
    d1 = [3, 3]
    d2 = [3, 3]

    fun1(d1)
    fun2(d2)
    
    print(d1)
    print(d2)
    
if __name__ == "__main__":
    main()
```
输出
```
[1, 2]
[3, 3]
```

解释：
1. fun1 的修改了变量x的内容，相当于C++中修改的指针指向的内容
2. fun2 修改了x的指向，相当于C++修改的指针指向。 python传参的方式接近于C++的指针按值传递（详见test03.cpp），因此无法将修改传出。

# 深入分析

Arguments are (passed by assignment)[https://docs.python.org/3/faq/programming.html#how-do-i-write-a-function-with-output-parameters-call-by-reference]. The rationale behind this is twofold:

1. the parameter passed in is actually a reference to an object (but the reference is passed by value)
2. some data types are mutable, but others aren't

So:

- If you pass a mutable object into a method, the method gets a reference to that same object and you can mutate it to your heart's delight, but if you rebind the reference in the method, the outer scope will know nothing about it, and after you're done, the outer reference will still point at the original object.

- If you pass an immutable object to a method, you still can't rebind the outer reference, and you can't even mutate the object.

也就是

1. 当函数参数为可变对象（mutable object）时（比如list和dict）
    - 可以在函数内修改对象内容，函数外也会收到修改的影响
    - 但不能让函数内的形参重新指向一个其他的对象（rebind），这种修改不会被传递回来

2. 当函数参数为不可变对象（ immutable object）时（比如int和str）
    - 既不能修改
    - 也不能重新绑定

# 参考
1. https://stackoverflow.com/questions/77252528/why-the-dict-of-python-is-not-affected-as-a-parameter-passed-into-the-function
2. https://stackoverflow.com/questions/986006/how-do-i-pass-a-variable-by-reference
3. https://docs.python.org/3/faq/programming.html#how-do-i-write-a-function-with-output-parameters-call-by-reference
