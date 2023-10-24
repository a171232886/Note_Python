# 这6个变量或值全部被认为是 False
lst = [[], {}, set(), None, False, 0]
for a in lst:
    if not a:
        # bool(a) 被认为是 False
        print(a)

####################################
a = None

if a:
    """
    python中不止None一种情况被认为是False
    [], {}, set(), None, False, 0 都会被认为是False
    """
    print("Not None")

if a == None:
    """
    __eq__ 会重载==，因此此时的逻辑取决于重载的逻辑
    False == None 为假，即False和None不相等

    ==字节码中使用COMPARE_OP
    cpython中调用PyObject_RichCompareBool()，
    速度慢
    """
    print("a == None")

if a is None:
    """
    is的字节码中使用IS_OP，
    在cpython中的行为是比较两个变量的地址（两个指针的比较）
    速度快
    """
    print("a is None")

# 因此对于None，使用is或者is not来判断