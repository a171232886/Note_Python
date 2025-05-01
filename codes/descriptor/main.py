"""
描述器：descriptor

1. 描述器是指定义了__get__或__set__或__delete__的类 
2. 描述器机制用到了LOAD_ATTR
3. 描述器机制是python众多机制的基础机制，
   但对用户而言意义不大，最大的作用似乎在main01.py

字节码 LOAD_ATTR, STORE_ATTR
1. 在使用类似`a.b`的代码就会使用LOAD_ATTR。
   LOAD_ATTR 在Cpython中调用PyObject_GetAttr,
   最终调用_PyObject_GenericGetAttrWithDict

2. 类似`a.b = c` 会调用STORE_ATTR

"""

"""
理解描述器行为的要点
1. descriptor object 需要在 class 的 type 中定义才有效
    （直接在class下定义，而不是在class的函数下）

2. 类似`a.b`的代码执行时的优先级

   （1）只有当descriptor中的__get__和__set__同时存在，优先执行descriptor
   （2）如果没有同时存在，先在class的__dict__中寻找b，
   （3）如果__dict__没有，执行descriptor的__get__
   （4）如果descriptor没有__get__，直接返回定义的descriptor对象
   
"""

# Name 作为描述器
class Name:
    def __get__(self, obj, objtype):
        return "Peter"
    
    def __set__(self, obj, objtype):
        return "__SET__"

# 情形0：没有descriptor
print("====================情形0========================")
class A0:
    def __init__(self) -> None:
        self.name = Name()

o = A0()
print(o.name)  # 打印 <__main__.Name object at 0x7f13478cb4f0>



# 情形1: 对应优先级（1）
print("====================情形1========================")
class A1:
    name = Name()
o = A1()
print(o.name) # 打印 "Peter"
print(A1.name) # 打印 "Peter"



# 情形2: 对应优先级（2）
print("====================情形2========================")
class Name2:
    def __get__(self, obj, objtype):
        return "Peter"

class A2:
    name = Name2()

o = A2()
o.name = "Bob"
print(o.__dict__)
print(o.name)           # 打印 "Bob", 优先级（2）

# 把Test.hello理解成一种无法初始化的临时对象
# 可能比较贴切
print(A2.__dict__)
print(A2.name)          # 打印 "Peter", 优先级（3）



# 情形3：对应优先级（3）
print("====================情形3========================")
class A3:
    name = Name()

o = A3()
print(o.name)  # 打印 "Peter"
print(A3.name) # 打印 "Peter"


# 情形4：对应优先级（4）
print("====================情形4========================")
class Name4:
    def get_name(self, obj, objtype):
        return "Peter"
    
class A4:
    name = Name4()  # 并不是描述器
    name2 = 'Hello'

o = A4()
print(o.__dict__)
print(o.name)       # 打印 <__main__.Name4 object at 0x7f1221cf3b50>
print(o.name2)      # 打印 Hello
print(A4.name)      # 打印 <__main__.Name4 object at 0x7f1221cf3b50>
print(A4.name2)     # 打印 Hello