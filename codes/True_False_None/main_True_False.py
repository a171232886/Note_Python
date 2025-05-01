# 这6个变量或值全部被认为是 False
lst = [[], {}, set(), None, False, 0]
for a in lst:
    if not a:
        # bool(a) 被认为是 False
        print(a)


##############################################
# 以下为判断方式
a = 1

if a is True:
    """
    仅当 a 为 True 时为真，a 为 True 之外的任何东西为假，包括 a=1
    a is True 的对立面是 a is not True，而不是 a is False！
    适用于把True当成一种特定标志，而独立于1,[1]等其他值的情况
    """

    print("a is True")

    """
    因此此情况完整的写法为
    if a is True:
        print("a is True")
    elif a is False:
        print("a is False")
    else:
        # a为True或False之外的任何值
        print("a is not True or False")
    """

if a == True:
    """
    不推荐的写法，因为==可以被重载，通过__eq__重载
    此时的逻辑取决于重载的逻辑
    在 a = True，a = 1 的情况下，a == True 为真
    在 a = False，a = 0，a = -1, a = [1] 的情况下，a == True 为假
    """
    print("a == True")

if a:
    """
    从字节码和Cpython中的实现来看，
    条件不为Py_True或Py_False的情况下，调用PyObject_IsTrue()

    PyObject_IsTrue()有三个返回值：
    1 代表Py_True
    0 代表Py_False 或者 Py_None
    -1 代表出错

    针对内置number：integer, float, complex, decimal 
        为0的时候返回false，非0返回true

    针对内置数据结构：dict, set, list, tuple, str等mapping或sequence
        len()为0的时候返回false，非0返回true, 即判断变量是否为空

    针对自定义数据结构：Cpython调用slot_nb_bool()，依序执行
        1. 判断是否定义__bool__，若有则调用__bool__
        2. 判断是否定义__len__，若有则调用__len__
        3. 返回true

    建议明确代码逻辑，比if a更明确的逻辑写法
    """
     
    print("a")

if bool(a):
    """
    bool()在Cpython中实际上是一个类，但表现上是一个只返回True或False的函数
    bool()在Cpython中调用PyObject_IsTrue()实现相关功能

    因此，完全没有必要使用该方法，直接使用if a即可
    """
    print("bool(a) is True")