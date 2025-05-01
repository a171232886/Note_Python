# Python魔术方法

参考：https://www.bilibili.com/video/BV1b84y1e7hG/



# 1. 构造与析构

## 1.1  `__new__` 与`__init__`

1. new 负责从类建立对象的过程

2. init 负责对对象的初始化

3. 两者都会被调用

   ```python
   class A:
       def __new__(cls, x):
           print("A.__new__")
           return super().__new__(cls)
       
       def __init__(self, x):
           print("A.__init__")
   
   o = A(1)
   # o = A(1) 过程类似于
   # obj = __new__(A, 1)
   # __init__(obj, 1)
   ```

4. 在单例模式时（全局仅有一个对象）时，会用到

   



## 1.2 `__del__`

1. 类似于析构函数，但考虑到python复杂的垃圾回收机制，不建议当做析构函数使用

2. 与`del`关键字并不是一回事

   ```python
   class A():
   	def __del__(self):
   		print("__del__")
   
   o = A()
   x = o
   
   del o	# 此时不会触发__del__， 还有一个x的引用
   
   print("finish")
   ```




# 2. 字符串

## 2.1 `__repr__`, `__str__`

```python
class A:
	def __repr__(self):
		return "<A repr>"
	def __str__(self):
		return "<A str>"		
```

1. print时优先级

   - `__str__` 高于 `__repr__`

     

2. 可以使用builtin函数

   ```python
   print( repr( A() ) )
   print( str( A() ) )
   ```



## 2.2  `__format__`

`__format__`部分

```python
class A:
	def __format__(slf, spec):
        # 当A被调用format或者f-string时使用
        if spec == 'x':
            return "0xA"
        return "<A>"
    
print(f"{A()}")
print(f"{A():b}")
print(f"{A():x}")
```



## 2.3 `__bytes__`

```python
class A:
    def __bytes__(self):
        print("__bytes__")
        return bytes([0, 1])
    
print(bytes(A()))
```

输出

```bash
__bytes__
b'\x00\x01'
```



# 2. 比较

## 2.1 普通比较

```python
class Date:
	def __init__(self, y, m, d):
        self.year = y
        self.month = m
        self.date = d
        
     def __eq__(self, other):
        return self.year == other.year
    
     def __ne__(self, other):
        return self.year != other.year
    
     def __gt__(self, other):
        print("greater than")
        return self.year > other.year
        
x = Date(2022, 2, 22)
y = Date(2022, 2, 22)

print( x == y )  # x.__eq__(y)
print( x != y )
```

1. 类中没有实现`__eq__`时，`==`默认调用`is`

2. 类中没有实现`__ne__`时， `!=`为`==`取反， 因此通常只实现`__eq__`即可

3. 以下部分建议若定义，就全定义，不依靠python的默认判别机制

   - `__gt__` greater than
   - `__lt__` less than
   - `__ge__` greater than or equal to
   - `__le__`  less than or equal to   
4. 当自定义了`__eq__`时， 默认的`__hash__`会被删除

## 2.2  `__hash__`

```python
class Date:
        def __init__(self, y, m, d):
			self.year = y
			self.month = m
            self.date = d
            
		def __eq__(self, other):
        	return self.year == other.year
        	
        def __hash__(self):
        	# 推荐做法：把核心参数做成一个元组，调用系统的hash() 
        	return hash((self.year, self.month, self.data))
```



1. 当自定义了`__eq__`时， 默认的`__hash__`会被删除
   - 建议两者同时定义

## 2.3  `__bool__`

1. 在调用`bool()`方法时使用

   

# 3. 属性

## 3.1 `__getattr__`

1. `__getattr__`：当调用==不存在的某个属性==的时候，定义需要完成的动作

   ```python
   class A:
       def __getattr__(self, name):
           print(f"Error getting {name}")
           raise AttributeError
   
   o = A()
   print(o.test) # A不存在test属性，此时调用会触发__getattr__
   ```

2. `__getattr__`的官方解释

   Called when the default attribute access fails with an [`AttributeError`](https://docs.python.org/3/library/exceptions.html#AttributeError) (either [`__getattribute__()`](https://docs.python.org/3/reference/datamodel.html?highlight=setattr#object.__getattribute__) raises an [`AttributeError`](https://docs.python.org/3/library/exceptions.html#AttributeError) because *name* is not an instance attribute or an attribute in the class tree for `self`; or [`__get__()`](https://docs.python.org/3/reference/datamodel.html?highlight=setattr#object.__get__) of a *name* property raises [`AttributeError`](https://docs.python.org/3/library/exceptions.html#AttributeError)). This method should either return the (computed) attribute value or raise an [`AttributeError`](https://docs.python.org/3/library/exceptions.html#AttributeError) exception.

   

   Note that if the attribute is found through the normal mechanism, [`__getattr__()`](https://docs.python.org/3/reference/datamodel.html?highlight=setattr#object.__getattr__) is not called. (This is an intentional asymmetry between [`__getattr__()`](https://docs.python.org/3/reference/datamodel.html?highlight=setattr#object.__getattr__) and [`__setattr__()`](https://docs.python.org/3/reference/datamodel.html?highlight=setattr#object.__setattr__).) 

   

## 3.2 `__getattribute__`

1. 只要调属性（无论是否存在），就会使用到`__getattribute__`

   ```python
   class A:
   	def __init__(self):
           self.data = "abc"
           self.counter = 0
   	def __getattribute__(self, name):
           print("[__getattribute__]")
           return super().__getattribute__(name)
   
   o = A()
   print(o.data)
   ```

   

2. 一个简单的调用次数统计

   ```python
   class A:
   	def __init__(self):
           self.data = "abc"
           self.counter = 0
   	def __getattribute__(self, name):
           if name == "data":
           	self.counter += 1
           return super().__getattribute__(name)
   
   o = A()
   print(o.data)
   print(o.data)
   print(o.counter)
   ```
   
   
   注意：

   1. `o.counter`会将`counter`以字符串的方式传入` __getattribute__`的`name`

   2. `__getattribute__`默认动作是`super().__getattribute__(name)`（写成`object.__getattribute__(name)`也可以）

      - 而不是`getattr()`，`return getattr()`会制造一个无限递归错误

   3. 因为只要调用属性，就会用到`__getattribute__`。在其内部编写代码时需要谨慎，易产生无限递归错误

      ```python
           def __getattribute__(self, name):
              self.counter += 1  # self.counter也会调用__getattribute__，进而产生无限递归错误
              return super().__getattribute__(name)
      ```

      

## 3.3 `__setattr__`

   给类内属性/方法赋值时用到

1. 基础

   - 类内外赋值（比如`self.idx = 1`）会调用`__setattr__`
   - `setattr()`会调用`__setattr__`
   - `setattr()`可以增加新属性/方法，也可以更新原有属性/方法

   ```python
   from typing import Any
   
   def func(x):
       print(f"func: {x}")
   
   class A:
       def __init__(self) -> None:
           self.idx = 1	# 会触发__setattr__
   
       def __setattr__(self, __name: str, __value: Any) -> None:
           print(f"__setattr__ {__name} {__value}")
           super().__setattr__(__name, __value)
   
       def func1(self, x):
           print(f"A.func1: {x}")
   
   
   a = A()
   
   a.idx = 0				# 直接修改会触发__setattr__
   
   print("==============================")
   setattr(a, "idx", 2)        # 更新已有属性值
   setattr(a, "num", 2)        # 设置新属性值
   setattr(a, "func", func)    # 设置新方法
   setattr(a, "func1", func)    # 更新方法
   
   print("==============================")
   print(a.idx)
   print(a.num)
   
   print("==============================")
   a.func(1)
   a.func1(2)
   
   print("==============================")
   print(dir(a))
   ```

   输出

   ```
   __setattr__ idx 1
   __setattr__ idx 0
   ==============================
   __setattr__ idx 2
   __setattr__ num 2
   __setattr__ func <function func at 0x7efd4df65800>
   __setattr__ func1 <function func at 0x7efd4df65800>
   ==============================
   2
   2
   ==============================
   func: 1
   func: 2
   ==============================
   ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'func', 'func1', 'idx', 'num']
   ```

   



## 3.4 `__delattr__` 

尝试删除一个属性的时候调用

```python
class A:
   def __init__(self):
      self.data = "abc"
   def __delattr__(self, name):
      print(f"del {name}")
      super().__delattr__(name)

o = A()
del o.data
print(o.data)
```



## 3.5 `__dir__`

1. dir()内置函数

   获取对象的全部属性（变量和方法）

   ```python
   o = A()
   print(dir(o))
   ```


2. `__dir__`

   程序执行`dir()`时会调用，必须返回一个Sequence ，比如List

   ```python
   class A:
      def __init__(self):
         self.data = "abc"
      def __dir__(self):
         li = super().__dir__()
         # 删除以下划线开头的属性
         return [el for el in li if not el.startswitch("_")]
   
   o = A()
   print(dir(o))
   ```
   
   

## 3.6 `__get__`, `__set__`, `__delete__`

均与descriptor相关

1. 描述器基础代码

   ```python
   class D:
       def __get__(self, obj, owner=None):
           print(self, obj, owner)
           return 0
       
   class A:
       x = D()  # x是一个descriptor
       
   o = A()
   print(o.x)
   ```
   
   打印结果为
   
   ```python
   <__main__.D object at 0x7f2a5ea66dd0>
   <__main__.A object at 0x7f2a5ea66e90>
   <class '__main__.A'>
   ```
   
   也就是` def __get__(self, obj, owner=None)`的三个参数为实际上为`x`, `o`, `A`

2. 描述器的使用方法

   ```python
   class D:
       def __init__(self):
           self.val = 0
           
       def __get__(self, obj, owner=None):
           # 描述器获取值时调用
           return self.val
       
       def __set__(self, obj, value):
           # 描述器设置值时调用
           self.val = value
       
       def __delete__(self, obj):
           # 删除描述器时调用
           print("delete")
       
   class A:
       x = D()  # x是一个descriptor
       
   o = A()
   print(o.x)
   o.x = 1
   print(o.x)
   del o.x
   ```

   

## 3.7 `__slots__`

```python
class A:
    # 规定类A下可以有哪些自定义的attribute
    __slots__ = [ 'a', 'b' ]
    
o = A()
o.a = 1
o.x = 1 # 报错
```



# 4. 类构建进阶

## 4.1 `__init_subclass__`

建立子类时，基类调用

```python
class Base:
    def __init_subclass__(cls):
        print(cls)

class A(Base):
    pass

print(A.name)
```

可以带一些参数

```python
class Base:
    def __init_subclass__(cls, name):
        print(cls)
        cls.name = name


class A(Base, name="Jack"):
    pass

print(A.name)
```



## 4.2 `__set_name__`

   在类中定义另外一个类的对象时会被调用

1. 代码

   ```python
   class D:
       def __set_name__(self, owner, name):
           print(owner, name)
   
   class A:
       x = D()
   ```

   打印

   ```
   <class '__main__.A'>
   x
   ```

   可见name为x，在一些log时可能会用到



## 4.3 `__class_getitem__`

1. 对类使用方括号索引时调用

    ```python
    class A:
        def __class_getitem__(cls, item):
            print(item)
            return "abs"

    print(A[0])

    ```

    ```
    0
    abs
    ```

2. type hint的实现方式

    ```python
    int_arr_type = list[int]
    li: int_arr_type = []
    ```



## 4.4 `__prepare__`

与metaclass相关

```python
class M(type):
    def __new__(cls, name, bases, dict):
        print('M.__new__',name, bases, dict)
        return type.__new__(cls, name, bases, dict)
    
    def __init__(self, name, bases, dict):
        print('M.__init__',name, bases, dict)
        self.test = 'test'
        return type.__init__(self, name, bases, dict)
        
    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        print('M.__prepare__',name, bases, kwds)
        return {"x": 10}


class A(metaclass=M):
    pass

print(A.x)
```

输出

```
M.__prepare__ A () {}
M.__new__ A () {'x': 10, '__module__': '__main__', '__qualname__': 'A'}
M.__init__ A () {'x': 10, '__module__': '__main__', '__qualname__': 'A'}
10
```



可见，调用顺序为`__prepare__`，`__new__`, `__init__`



## 4.5 `__instancecheck__`、`__subclasscheck__`

不建议编写该部分，python对这两个功能的实现，存在bug

但直接使用`isinstance()`和`issubclass()`是没问题的

```python
class M(type):
    def __instancecheck__(self, instance):
        print('M.__instancecheck__')
        return type.__instancecheck__(self, instance)
    
    def __subclasscheck__(self, subclass):
        print('M.__subclasscheck__')
        return type.__subclasscheck__(self, subclass)
    

class A(metaclass=M):
    pass

o = A()
print(isinstance(123, A))
print(issubclass(int, A))
print(isinstance(o, A))   # 此时并没有调用我们定义的__instancecheck__
```

打印

```
M.__instancecheck__
False
M.__subclasscheck__
False
True
```



关于`print(isinstance(o, A))`的问题

1. 看上去是一个Python的bug
   https://github.com/python/cpython/issues/79264



# 5. 运算

## 5.1 常见方法

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        print(f"Vector({self.x}, {self.y})")

    def __add__(self, other):
        # v1 + v2
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        # v1 - v2
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        # v1 * v2
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)
        return Vector(self.x * other.x, self.y * other.y)

    def __rmul__(self, other):
        # 2 * v1
        return Vector(self.x * other, self.y * other)
    
    def __imul__(self, other):
        # v1 *= v2
        return Vector(self.x * other.x, self.y * other.y)
    
    def __matmul__(self, other):
        # v1 @ v2
        return Vector(self.x * other.x, self.y * other.y)

    def __truediv__(self, other):
        # v1 / v2
        return Vector(self.x / other.x, self.y / other.y)
    
    def __floordiv__(self, other):
        # v1 // v2
        return Vector(self.x // other.x, self.y // other.y)
    
    def __mod__(self, other):
        # v1 % v2
        return Vector(self.x % other.x, self.y % other.y)
    
    def __divmod__(self, other):
        # divmod(v1, v2)
        # 返回一个元组，包含商和余数
        return Vector(divmod(self.x, other.x), divmod(self.y, other.y))

    def __pow__(self, other):
        # v1 ** v2
        return Vector(self.x ** other.x, self.y ** other.y)
    
    def __lshift__(self, other):
        # v1 << v2
        return Vector(self.x << other.x, self.y << other.y)
    
    def __rshift__(self, other):
        # v1 >> v2
        return Vector(self.x >> other.x, self.y >> other.y)
    
    def __and__(self, other):
        # v1 & v2
        return Vector(self.x & other.x, self.y & other.y)
    
v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 * v2)      # 调用 __mul__
print(v1 * 2)       # 调用 __mul__
print(2 * v1)       # 调用 __rmul__
v1 *= v2            # 调用 __imul__
```

1. 函数中other不一定和self是相同类型，比如v1 * 2
2. 当运算符左侧对象未定义当前操作时（比如 2 * v1）, python会调用运算符右侧对象的0该操作符的r版本（`__rmul__`）
3. 对自身修改的函数，调用操作符的i版本（`__imul__`）
   - 所有靠符号触发操作的运算，均有i版本（比如+），而mod(x,y)则没有



## 5.2 不传参

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __neg__(self):
        return Vector(-self.x, -self.y)
    
    def __pos__(self):
        return Vector(self.x, self.y)

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def __invert__(self):
        return Vector(self.y, self.x)
    
    def __complex__(self):
        return complex(self.x, self.y)
    
    def __int__(self):
        return int(abs(self))
    
    def __float__(self):
        return float(abs(self))
    
    def __index__(self):
        return int(self)
    
    def __round__(self, n=None):
        # 四舍五入
        return round(abs(self), n)
    
    def __trunc__(self):
        # 截断, 取整数部分
        # math库中的trunc函数
        return int(self)
    
    def __floor__(self):
        # 向下取整
        # math库中的floor函数
        import math
        return math.floor(abs(self))
    
    def __ceil__(self):
        # 向上取整
        # math库中的ceil函数
        import math
        return math.ceil(abs(self))
    
v1 = Vector(1, 2)
lst = [0, 1, 2]
print(lst[v1])          # 调用 __index__
```



# 6. 模拟

## 6.1 `__call__`

使对象像函数一样使用

```python
class Multiplier:
    def __init__(self, x):
        self.x = x

    def __call__(self, other):
        return self.x * other.x
    
o = Multiplier(2)
print(o(3)) # 6
```



## 6.2 常用

```python
class MyList:
    def __init__(self, data):
        self.data = data
        
    def __len__(self):
    	return len(self.data)
    
    def __getitem__(self, index):
        # 使用方括号索引时用到
        return self.data[index]
    
    def __setitem__(self, index, value):
        # 使用方括号赋值时用到
        self.data[index] = value

    def __delitem__(self, index):
        # 使用方括号删除值时用到
        self.data = self.data[:index] + self.data[index+1:]

    def __reversed__(self):
        # 使用reversed()函数时用到
        return self.data[::-1]
    
    def __contains__(self, value):
        # 使用in运算符时用到
        return value in self.data
    
    def __iter__(self):
        # 迭代器，iter()函数时用到
        return iter(self.data)
    
    
x = MyList([1, 2, 3, 4, 5])

print(x[2])

x[2] = 100

del x[2]

print(reversed(x).data)

print(5 in x)

for i in x:
    print(i)
```



## 6.3 `__missing__`

```python
# 使用__missing__，必须继承dict
class MyDict(dict):
    def __missing__(self, key):
        # 定义key不存在时的动作
        return key
    
d = MyDict()
print(d['a'])
```



## 6.4 `__enter__`、`__exit__`

```python
import time

class Timer:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        # 定义进入with语句时的操作
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # 定义离开with语句时的操作

        # 如果with语句内部发生了异常，
        # 那么exc_type、exc_value和exc_traceback会返回异常的类型、值和追踪信息
        # 如未发生异常，则三个参数都为None
        print(exc_type, exc_value, exc_traceback)

        # 即便程序执行出错，也会执行__exit__方法
        print(f'{self.name} took {time.time() - self.start:.3f} seconds')

with Timer('test') as t:
    _ = 1000 * 100

with Timer('test') as t:
    _ = 1000 / 0
```











