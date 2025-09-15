# Pydantic

Pydantic 是一个声明复杂数据结构的库，可用于数据格式验证和序列化/反序列化。广泛应用于Python各第三方库中，比如FastAPI。

- 本文档基于版本 2.11.7
- 官方文档：https://docs.pydantic.dev/2.11/concepts/serialization/



快速开始

```python
from pydantic import BaseModel, Field
from typing import Optional

# 定义一个用户模型
class User(BaseModel):
    id: int = Field(description="The unique identifier for the user", default=0)
    name: str = "John Doe"  # 提供默认值
    age: Optional[int] = None  # 可选字段，默认为 None
    hobbies: list[str] = []  # 一个字符串列表，默认为空列表

# 使用字典数据创建实例（反序列化）
user_data = {
    "id": 123,
    "name": "Alice",
    "age": 30,
    "hobbies": ["coding", "reading"]
}

# Pydantic 会自动验证数据
user = User(**user_data)
print(user) 
# > id=123 name='Alice' age=30 hobbies=['coding', 'reading']

# 访问属性
print(user.name) # > Alice

# 转换为字典
print(user.model_dump()) 
# > {'id': 123, 'name': 'Alice', 'age': 30, 'hobbies': ['coding', 'reading']}

# 转换为 JSON
print(user.model_dump_json()) 
# > {"id": 123, "name": "Alice", "age": 30, "hobbies": ["coding", "reading"]}
```





# 1. 数据验证

在根据输入数据创建`BaseModel`实例时，进行的数据校验。用户在这一阶段可自定义验证器（validator）

官方文档：https://docs.pydantic.dev/2.11/concepts/validators/



## 1.1 validator 

1. validator 分为两种：

   - 针对特定字段的`field validator`
     - [field *after* validators](https://docs.pydantic.dev/2.11/concepts/validators/#field-after-validator)
     - [field *before* validators](https://docs.pydantic.dev/2.11/concepts/validators/#field-before-validator)
     - [field *plain* validators](https://docs.pydantic.dev/2.11/concepts/validators/#field-plain-validator)
     - [field *wrap* validators](https://docs.pydantic.dev/2.11/concepts/validators/#field-wrap-validator)

   - 针对整个数据结构的`model validator`
     - [model *before* validators](https://docs.pydantic.dev/2.11/concepts/validators/#model-before-validator)
     - [model *after* validators](https://docs.pydantic.dev/2.11/concepts/validators/#model-after-validator)
     - [model *wrap* validators](https://docs.pydantic.dev/2.11/concepts/validators/#model-wrap-validator)



2. 每类 validator 的”执行时间“

   -  before：在BaseModel的”内部类型验证逻辑“之前

   - after：在BaseModel的”内部类型验证逻辑“之后

   - warp：使用该validotar，完全控制验证过程

     

### 1.1.1 field validator

1. 四类validator

   - **After validators**: run after Pydantic's internal validation. 

   - **Before validators**: run before Pydantic's internal parsing and validation (e.g. coercion of a `str` to an `int`). 

   - **Plain validators**: 替代掉before和内部验证
     - **跳过内部类型验证**：Pydantic 不会对该字段执行其内部的类型验证

   - **Wrap Validators**：允许您完全控制验证过程，可以在 Pydantic 内部验证之前、之后或完全绕过它。



2. 最为常用，也是最推荐的`before`和`after`

   ```python
   from pydantic import BaseModel, field_validator
   from typing import Any
   
   class Model(BaseModel):
       numbers: list[int]
   
       @field_validator('numbers', mode='before')
       @classmethod
       def ensure_list(cls, value: Any) -> Any:
           # 注意：此处类型检查可以不写，
           # 如果一定要写建议写Any
           print(f"before validate: {value} ({type(value)})")
           if not isinstance(value, list):  
               return [value]
           else:
               return value
   
       @field_validator('numbers', mode='after')  
       @classmethod
       def is_even(cls, value: int) -> int:
           print(f"after validate: {value} ({type(value)})")
           for v in value:
               if v % 2 == 1:
                   raise ValueError(f'{v} is not an even number')
           return value  
       
   model = Model(numbers=10)
   ```

   输出

   ```
   before validate: 10 (<class 'int'>)
   after validate: [10] (<class 'list'>)
   ```

   

3. `plain`的执行逻辑

   ```python
   from pydantic import BaseModel, field_validator
   class ComparisonModel(BaseModel):
       value: int
       
       @field_validator('value', mode='before')
       def before_validator(cls, v):
           print("Before validator - internal validation will still happen")
           return v
       
       @field_validator('value', mode='plain')
       def plain_validator(cls, v):
           print("Plain validator - no internal validation")
           return v
       
       @field_validator('value', mode='after')
       def after_validator(cls, v):
           print("After validator - internal validation has already happened")
           return v
   
   model = ComparisonModel(value=10)
   ```

   输出

   ```
   Plain validator - no internal validation
   After validator - internal validation has already happened
   ```

   

4. warp

   ```python
   from typing import Any
   from pydantic import BaseModel, Field, ValidationError, ValidatorFunctionWrapHandler, field_validator
   
   
   class Model(BaseModel):
       my_string: str = Field(max_length=5)
   
       @field_validator('my_string', mode='wrap')
       @classmethod
       def truncate(cls, value: Any, handler: ValidatorFunctionWrapHandler) -> str:
           try:
               print('Before validation:', value)
               res = handler(value)
               print('After validation:', res)
               return res
           except ValidationError as err:
               if err.errors()[0]['type'] == 'string_too_long':
                   return handler(value[:5])
               else:
                   raise
   
   model = Model(my_string='abcde')
   print(model.my_string)
   ```

   

   - **必须的 `handler` 参数**：接收一个可调用对象，用于接收 Pydantic 的内部验证器

   - **完全控制**：您可以决定是否调用、何时调用、如何调用内部验证

   - **异常处理**：可以包装 `handler` 在 try-except 块中处理异常



5. warp 和before，after，plain在一起

   - 一般不会出现这种情况，因为一旦使用warp就没有必要再去定义before，after，plain

   ```python
   from pydantic import BaseModel, ValidationError, field_validator
   
   class ValidationOrderExample(BaseModel):
       value: int
       
       # 1. before 验证器
       @field_validator('value', mode='before')
       def before_validator(cls, v):
           print(f" Before validator: {v} (type: {type(v).__name__})")
           if isinstance(v, str) and v.isdigit():
               return int(v)  # 字符串转数字
           return v
       
       # 2. after 验证器
       @field_validator('value')
       def after_validator(cls, v):
           print(f" After validator: {v} (type: {type(v).__name__})")
           if v > 100:
               raise ValueError("Value too large")
           return v
       
       # 3. plain 验证器
       @field_validator('value', mode='plain')
       def plain_validator(cls, v):
           print(f"2. Plain validator: {v} (type: {type(v).__name__})")
           # 跳过所有后续验证，包括内部验证
           return v * 2
       
       # 4. wrap 验证器（最后执行）
       @field_validator('value', mode='wrap')
       def wrap_validator(cls, v, handler):
           print(f"1. Wrap validator - before handler: {v}")
           try:
               result = handler(v)  # 这里会触发 before + 内部 + after 验证器
               print(f"3. Wrap validator - after handler: {result}, type: {type(result)}")
               return result + 10
           except Exception as e:
               print(f"Wrap validator caught error: {e}")
               return 999
           
   v = ValidationOrderExample(value="50")
   ```

   

   输出

   ```
   1. Wrap validator - before handler: 50
   2. Plain validator: 50 (type: str)
   3. Wrap validator - after handler: 5050, type: <class 'str'>
   Wrap validator caught error: can only concatenate str (not "int") to str
   ```

   



### 1.1.2 model validator

1. 针对全部数据，有三种类型
   - after
   - before
   - wrap

2. 最为常用的after和before

   - 注意 model validator 的 after 不再是类方法，而是实例方法，并且需要返回self

   ```python
   from typing import Any
   from pydantic import BaseModel, model_validator
   
   
   class UserModel(BaseModel):
       username: str
       password: str
       password_repeat: str
   
       @model_validator(mode='before')
       @classmethod
       def check_card_number_not_present(cls, data: Any) -> Any:  
           print(f"Before validation data: {data}")
           if isinstance(data, dict):  
               if 'card_number' in data:
                   raise ValueError("'card_number' should not be included")
           return data
       
       @model_validator(mode='after')
       def check_passwords_match(self):
           print(f"After validation instance: {self}")
           if self.password != self.password_repeat:
               raise ValueError('Passwords do not match')
           return self
   
   user = UserModel(username='john_doe', password='secure123', password_repeat='secure123')
   ```

   输出

   ```
   Before validation data: {'username': 'john_doe', 'password': 'secure123', 'password_repeat': 'secure123'}
   After validation instance: username='john_doe' password='secure123' password_repeat='secure123'
   ```

   

3. wrap 用法

   ```python
   import logging
   from typing import Any
   from typing_extensions import Self
   from pydantic import BaseModel, ModelWrapValidatorHandler, ValidationError, model_validator
   
   
   class UserModel(BaseModel):
       username: str
   
       @model_validator(mode='wrap')
       @classmethod
       def log_failed_validation(cls, data: Any, handler: ModelWrapValidatorHandler[Self]) -> Self:
           try:
               print(f'Validating data: {data}')
               res = handler(data)
               print(f'Validation successful: {res}')
               return res 
           
           except ValidationError:
               logging.error('Model %s failed to validate with data %s', cls, data)
               raise
   
   user = UserModel(username='alice')
   ```

   



## 1.2 model_validate()

1. 官方文档：https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_validate

2. 注意：此处主要讨论`model_validate()`，与`model_validate_json()` 区别仅在于输出

   - `model_validate()` 接收的是字典

   - `model_validate_json()` 接收的是json字符串



### 1.2.1 与`__init__()`区别

1. `BaseModel.__init__()` 和 `BaseModel.model_validate()` 共享同一套验证、类型转换和错误收集引擎。

   它们的区别主要在于**调用方式**和**输入数据的来源**，而不是底层验证规则

   ```python
   data = {"name": "Li", "age": 32}
   model = BaseModel(**data)
   model = BaseModel.model_validate(data)
   ```



2. 两个方法的使用场景

   - `BaseModel.__init__()`：传入已知数据，快速创建实例
   - `BaseModel.model_validate()` ：传入外部数据，需要自定义数据验证/处理逻辑




### 1.2.2 处理步骤

1. 未发现Python源码，文档中也未说明

   此处直接使用 DeepSeek 生成的答案，并进行后续验证



2. 两种validator

   - model validator 针对全部数据项的
   - field validator 针对单个字段的

   

3. 需重点关注：

   - 调用 before 验证器（model validator）

   - 核心字段验证（field validator）和转换

   - 调用 after 验证器（model validator）

   **此三部分是可以使用用户自定义逻辑的**
   
   
   
4. `BaseModel.model_validate()`伪代码展示核心逻辑

   ```python
   # 伪代码展示 model_validate() 的核心逻辑
   def model_validate(cls, data: Any) -> 'Model':
       try:
           # 1. 输入数据预处理
           processed_data = cls._prepare_input_data(data)
           
           # 2. 调用 before 验证器
           processed_data = cls._run_model_validators('before', processed_data)
           
           # 3. 核心字段验证和转换
           validated_data = cls._validate_and_convert_fields(processed_data)
           
           # 4. 创建模型实例
           instance = cls.__new__(cls)
           
           # 5. 初始化实例属性
           cls._init_private_attributes(instance, validated_data)
           
           # 6. 调用 after 验证器
           instance = cls._run_model_validators('after', instance)
           
           # 7. 构建完成
           return instance
           
       except ValidationError as e:
           # 统一错误处理
           cls._handle_validation_error(e, data)
   ```

   

2. 核心逻辑

   ```
   model_validate() 开始
       │
       ├── 1. 输入预处理
       │     ├── 字符串 → JSON 解析
       │     ├── 模型实例 → 字典转换
       │     └── 其他类型 → 字典尝试转换
       │
       ├── 2. Before 验证器
       │     ├── 执行所有 @model_validator(mode='before')
       │     └── 可以修改输入数据
       │
       ├── 3. 字段级验证 (核心)
       │     ├── 遍历所有模型字段
       │     ├── 类型检查和解包 (Union, Optional等)
       │     ├── 自定义验证器 (@field_validator)
       │     ├── 默认值处理
       │     ├── 别名解析
       │     └── 错误收集和聚合
       │
       ├── 4. 实例创建
       │     ├── 使用 __new__() 创建实例
       │     └── 避免递归调用 __init__()
       │
       ├── 5. 属性设置
       │     ├── 设置所有验证后的字段值
       │     └── 初始化私有属性
       │
       ├── 6. After 验证器
       │     ├── 执行所有 @model_validator(mode='after')
       │     └── 可以修改实例属性
       │
       └── 7. 返回验证成功的实例
   ```



### 1.2.3 处理步骤验证

1. 基于BaseModel定义数据结构和validator

   ```python
   from pydantic import BaseModel, field_validator, model_validator, ValidationError, Field
   from datetime import datetime
   from typing import Optional
   
   class User(BaseModel):
       id: int
       name: str
       email: Optional[str] = None
       age: int = Field(gt=0, le=120)
       created_at: datetime = Field(default_factory=datetime.now)
       status: str = "active"
       
       # 步骤2: Before 验证器
       @model_validator(mode='before')
       @classmethod
       def step2_before_validation(cls, data):
           print("🔹 步骤2: Before 验证器执行")
           print(f"   输入数据: {data}")
           
           # 添加默认邮箱
           if isinstance(data, dict) and 'name' in data and 'email' not in data:
               email = f"{data['name'].lower().replace(' ', '.')}@example.com"
               data['email'] = email
               print(f"   添加默认邮箱: {email}")
           
           # 确保时间戳
           if 'created_at' not in data:
               data['created_at'] = datetime.now()
               print(f"   添加创建时间: {data['created_at']}")
               
           return data
   
       # 步骤3: 字段级验证 - 名称验证
       @field_validator('name')
       @classmethod
       def step3_name_validator(cls, v):
           print(f"🔹 步骤3: 字段验证 - name: '{v}'")
           if len(v) < 2:
               raise ValueError("名字太短")
           if len(v) > 50:
               raise ValueError("名字太长")
           return v.title()  # 首字母大写
    
   
       # 步骤6: After 验证器
       @model_validator(mode='after')
       def step6_after_validation(self):
           print("🔹 步骤6: After 验证器执行")
           print(f"   当前实例: {self}")
           
           # 基于年龄设置状态
           if self.age < 18:
               self.status = "minor"
               print(f"   设置状态为: {self.status} (未成年人)")
           elif self.age > 65:
               self.status = "senior" 
               print(f"   设置状态为: {self.status} (老年人)")
               
           return self
   ```
   
   
   
   

2. 测试`model_validate()`关键执行逻辑

   ```python
   def test_validation_steps():
       print("=" * 60)
       print("🚀 开始验证 model_validate() 的6个执行步骤")
       print("=" * 60)
       
       # 测试数据
       test_data = {
           "id": "123",  # 字符串，需要类型转换
           "name": "john doe",  # 小写，需要转换
           "age": 16  # 未成年人
       }
       
       print(f"📥 步骤1: 输入数据预处理")
       print(f"   原始数据: {test_data}")
       print(f"   id 类型: {type(test_data['id'])} -> 需要转换为 int")
       print(f"   name: '{test_data['name']}' -> 需要首字母大写")
       print(f"   email: 未提供 -> 需要生成默认值")
       
       try:
           print("\n" + "=" * 60)
           print("🔄 开始执行 User.model_validate(test_data)")
           print("=" * 60)
           
           # 步骤1+2+3+4+5+6: 完整验证流程
           user = User.model_validate(test_data)
           
           print("\n" + "=" * 60)
           print("✅ 验证成功！最终结果:")
           print("=" * 60)
           print(f"   用户ID: {user.id} (类型: {type(user.id)})")
           print(f"   姓名: {user.name}")
           print(f"   邮箱: {user.email}")
           print(f"   年龄: {user.age}")
           print(f"   状态: {user.status}")
           print(f"   创建时间: {user.created_at}")
           
       except ValidationError as e:
           print("\n❌ 验证失败！错误信息:")
           print(f"   错误数量: {len(e.errors())}")
           for error in e.errors():
               print(f"   - 字段: {error['loc']}, 错误: {error['msg']}")
   ```

   输出

   ```bash
   ============================================================
   🚀 开始验证 model_validate() 的执行步骤
   ============================================================
   📥 步骤1: 输入数据预处理
      原始数据: {'id': '123', 'name': 'john doe', 'age': 16}
      id 类型: <class 'str'> -> 需要转换为 int
      name: 'john doe' -> 需要首字母大写
      email: 未提供 -> 需要生成默认值
   
   ============================================================
   🔄 开始执行 User.model_validate(test_data)
   ============================================================
   🔹 步骤2: Before 验证器执行
      输入数据: {'id': '123', 'name': 'john doe', 'age': 16}
      添加默认邮箱: john.doe@example.com
      添加创建时间: 2025-09-15 09:54:03.407591
   🔹 步骤3: 字段验证 - name: 'john doe'
   🔹 步骤6: After 验证器执行
      当前实例: id=123 name='John Doe' email='john.doe@example.com' age=16 created_at=datetime.datetime(2025, 9, 15, 9, 54, 3, 407591) status='active'
      设置状态为: minor (未成年人)
   
   ============================================================
   ✅ 验证成功！最终结果:
   ============================================================
      用户ID: 123 (类型: <class 'int'>)
      姓名: John Doe
      邮箱: john.doe@example.com
      年龄: 16
      状态: minor
      创建时间: 2025-09-15 09:54:03.407591
   ```

   

3. 测试错误聚合

   ```python
   def test_error_aggregation():
       print("\n" + "=" * 60)
       print("🐛 测试错误聚合功能")
       print("=" * 60)
       
       invalid_data = {
           "id": "not_a_number",  # 无法转换为int
           "name": "a",  # 太短
           "age": -5,  # 负数，违反多个约束
           "email": "invalid-email"  # 无效邮箱格式
       }
       
       print(f"📥 包含多个错误的数据: {invalid_data}")
       
       try:
           user = User.model_validate(invalid_data)
       except ValidationError as e:
           print(f"❌ 捕获到 {len(e.errors())} 个错误:")
           for i, error in enumerate(e.errors(), 1):
               print(f"   {i}. 字段: {error['loc']}")
               print(f"      类型: {error['type']}")
               print(f"      信息: {error['msg']}")
               print(f"      输入值: {error['input']}")
               print()
   ```

   输出

   ```bash
   ============================================================
   🐛 测试错误聚合功能
   ============================================================
   📥 包含多个错误的数据: {'id': 'not_a_number', 'name': 'a', 'age': -5, 'email': 'invalid-email'}
   🔹 步骤2: Before 验证器执行
      输入数据: {'id': 'not_a_number', 'name': 'a', 'age': -5, 'email': 'invalid-email'}
      添加创建时间: 2025-09-15 10:00:27.804786
   🔹 步骤3: 字段验证 - name: 'a'
   ❌ 捕获到 3 个错误:
      1. 字段: ('id',)
         类型: int_parsing
         信息: Input should be a valid integer, unable to parse string as an integer
         输入值: not_a_number
   
      2. 字段: ('name',)
         类型: value_error
         信息: Value error, 名字太短
         输入值: a
   
      3. 字段: ('age',)
         类型: greater_than
         信息: Input should be greater than 0
         输入值: -5
   
   ```

   

## 1.3 自定义类的数据验证

1. 使用自定义类作为类变量的类型时

   - 通过在`@field_validator`调用自定义类的方法

   ```python
   from pydantic import BaseModel, Field, field_validator, ValidationError
   
   class Custom:
       def __init__(self, value: str):
           self.value = value
   
       @classmethod
       def validate(cls, v):
           print(f"Validating Custom with value: {v}")
           if not isinstance(v, str):
               raise ValueError("Invalid value for Custom")
           return cls(v)
       
   
   class Model(BaseModel):
   	
       # 必须添加的Config
       class Config:
           arbitrary_types_allowed = True
   
       name: str
       custom: Custom
   
       @field_validator('custom', mode='before')
       def validate_custom(cls, v):
           print(f"Running validator for custom with value: {v}")
           try:
               ins = Custom.validate(v)
               return ins
           except ValueError as e:
               raise ValueError(f"Custom validation error: {e}")
           
   
   model = Model(name="Test", custom="valid_string")
   print("="* 20)
   model = Model(name="Test", custom=123)  # This will raise a validation error
   ```

   输出

   ```bash
   Running validator for custom with value: valid_string
   Validating Custom with value: valid_string
   ====================
   Running validator for custom with value: 123
   Validating Custom with value: 123
   Traceback (most recent call last):
     File "/home/dell/wh/code/learn/ms_autogen/_pydantic/z1.py", line 36, in <module>
       model = Model(name="Test", custom=123)  # This will raise a validation error
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
     File "/home/dell/wh/code/learn/ms_autogen/.venv/lib/python3.11/site-packages/pydantic/main.py", line 253, in __init__
       validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   pydantic_core._pydantic_core.ValidationError: 1 validation error for Model
   custom
     Value error, Custom validation error: Invalid value for Custom [type=value_error, input_value=123, input_type=int]
       For further information visit https://errors.pydantic.dev/2.11/v/value_error
   ```

   





# 2. 序列化

(**Serialization**)

1. 序列化是将BaseModel实例保存成 dict / json （最终目的是保存成 json 或其他格式的文件），方便进行网络传输或者持久化

   上面的”数据验证“，实际上相当于反序列化（deserialization），根据 dict / json 创建BaseModel实例

2. 官方文档：https://docs.pydantic.dev/2.11/concepts/serialization/

3. 重点讨论均围绕`model_dump()`方法，也是`model_dump_json()`的前置步骤
   - https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_dump

     

4. Pydantic provides several [functional serializers](https://docs.pydantic.dev/2.11/api/functional_serializers/#pydantic.functional_serializers) to customise how a model is serialized to a dictionary or JSON.
   - [`@field_serializer`](https://docs.pydantic.dev/2.11/api/functional_serializers/#pydantic.functional_serializers.field_serializer)
   - [`@model_serializer`](https://docs.pydantic.dev/2.11/api/functional_serializers/#pydantic.functional_serializers.model_serializer)

   

5. 两种均可设置mode为`plain`或者`wrap`，默认均为plain

   - [`PlainSerializer`](https://docs.pydantic.dev/2.11/api/functional_serializers/#pydantic.functional_serializers.PlainSerializer) （默认）
   - [`WrapSerializer`](https://docs.pydantic.dev/2.11/api/functional_serializers/#pydantic.functional_serializers.WrapSerializer)

   如果需要使用默认的serializer，mode=wrap
   
   如果想完全使用自定义的serialzier逻辑，mode=plain



## 2.1 serializer

通常情况

- 针对某个字段的使用`@field_serializer`

- 针对全部数据的使用`@model_serializer(mode="wrap")`

### 2.1.1 field serializer

1. 用于定义针对指定字段进行的序列化逻辑

   推荐方式（默认），`model=plain`

   既可以返回序列化后的值，也可以返回一个字典

   ```python
   from pydantic import (
       BaseModel, Field, 
       field_validator, ValidationError, 
       field_serializer, SerializationInfo
   )
   
   class User(BaseModel):
       name: str
       email: str
       is_sensitive: bool = False
   
       @field_serializer('name')
       def serialize_name(self, name: str) -> str:
           if self.is_sensitive:
               return "****"
           return name
   
       @field_serializer('email')
       def serialize_email(self, email: str, info: SerializationInfo):
           """
           info 是一个可选的参数，可以不接收
               传进来的 info 是一个 FieldSerializationInfo 对象
               而 FieldSerializationInfo(SerializationInfo)
           """
           print(f"Serializing email for field: {info.field_name}")
           print(f"Serialization info: {info}")
           return email
   
   # 测试
   user = User(
       name="张三",
       email="zhangsan@example.com",
       is_sensitive=True
   )
   
   print("Python 字典序列化")
   print(user.model_dump())
   ```

   输出

   ```
   Python 字典序列化
   Serializing email for field: email
   Serialization info: SerializationInfo(include=None, exclude=None, context=None, mode='python', by_alias=False, exclude_unset=False, exclude_defaults=False, exclude_none=False, round_trip=False, serialize_as_any=False)
   {'name': '****', 'email': 'zhangsan@example.com', 'is_sensitive': True}
   ```

   

2. wrap模式下必须返回字典

   ```python
   from pydantic import BaseModel, field_serializer, SerializationInfo
   from datetime import datetime
   
   class Event(BaseModel):
       title: str
       start_time: datetime
   
       @field_serializer('start_time', mode='wrap')
       def serialize_start_time(self, info: SerializationInfo, handler):
           # 可以传入，也可以不传入 handler
           print("🔹 执行包装字段序列化器 (start_time)")
   
           # 1. 首先，获取该字段默认的序列化值
           #    调用 handler(self.start_time)
           default_value = handler(self.start_time)
   
           # 2. 然后，对默认值进行包装或修改
           return {
               'iso_format': default_value, # 默认序列化的结果
               'readable_format': self.start_time.strftime('%B %d, %Y at %I:%M %p'),
               'year': self.start_time.year
           }
   
   event = Event(title="Team Meeting", start_time=datetime(2023, 10, 27, 14, 30))
   print(event.model_dump())
   ```

   输出

   ```
   🔹 执行包装字段序列化器 (start_time)
   {'title': 'Team Meeting', 'start_time': {'iso_format': datetime.datetime(2023, 10, 27, 14, 30), 'readable_format': 'October 27, 2023 at 02:30 PM', 'year': 2023}}
   ```

   



### 2.1.2 model_serializer

1. 可用于针对整个Model中数据的序列化逻辑定义

   model 默认为 plain

   ```python
   from pydantic import (
       BaseModel, Field, 
       field_validator, ValidationError, 
       model_serializer, field_serializer, SerializationInfo
   )
   from typing import Any
   
   
   class Model(BaseModel):
       x: str
       y: int
   
       @model_serializer
       def ser_model(self) -> dict[str, Any]:
           print('Serializing model')
           return {'x': f'serialized {self.x}', 'y': self.y}
   
   
   print(Model(x='test value', y=1).model_dump())
   ```

   输出

   ```
   Serializing model
   {'x': 'serialized test value', 'y': 1}
   ```

   

2. wrap模式下必须返回字典

   在这种模式下，你的序列化器函数更像一个后处理钩子。

   如果需要用到model_serializer，mode=wrap会更常用一些
   
   ```python
   from pydantic import (
       BaseModel, Field, 
       field_validator, ValidationError, 
       model_serializer, field_serializer, SerializationInfo
   )
   from typing import Any, Callable
   
   class Product(BaseModel):
       id: int
       name: str
       cost_price: float  # 成本价，内部使用
       selling_price: float  # 售价，对客户可见
   
       @model_serializer(mode='wrap')
       def serialize_model(self, handler: Callable, info: SerializationInfo) -> dict:
           default_data = handler(self)
           
           # 检查序列化上下文（如果有的话）
           context = info.context
           if context and context.get('internal_use'):
               # 内部使用，显示所有字段
               return default_data
           else:
               # 对外API，隐藏成本价
               if 'cost_price' in default_data:
                   del default_data['cost_price']
               return default_data
   
   # 使用
   product = Product(id=1, name="Laptop", cost_price=800, selling_price=1200)
   
   # 外部API - 隐藏成本价
   print(product.model_dump())
   # 输出: {'id': 1, 'name': 'Laptop', 'selling_price': 1200.0}
   
   # 内部使用 - 显示所有字段
   print(product.model_dump(context={'internal_use': True}))
   # 输出: {'id': 1, 'name': 'Laptop', 'cost_price': 800.0, 'selling_price': 1200.0}
   
   ```
   
   



## 2.2 SerializationInfo

1. SerializationInfo 的定义

   ```python
   class SerializationInfo(Protocol):
       @property
       def include(self) -> IncExCall: ...
   
       @property
       def exclude(self) -> IncExCall: ...
   
       @property
       def context(self) -> Any | None:
           """Current serialization context."""
   
       @property
       def mode(self) -> str: ...
   
       @property
       def by_alias(self) -> bool: ...
   
       @property
       def exclude_unset(self) -> bool: ...
   
       @property
       def exclude_defaults(self) -> bool: ...
   
       @property
       def exclude_none(self) -> bool: ...
   
       @property
       def serialize_as_any(self) -> bool: ...
   
       @property
       def round_trip(self) -> bool: ...
   
       def mode_is_json(self) -> bool: ...
   
       def __str__(self) -> str: ...
   
       def __repr__(self) -> str: ...
   
           
   class FieldSerializationInfo(SerializationInfo, Protocol):
       @property
       def field_name(self) -> str: ...
   ```

   

2. `SerializationInfo`中定义的参数，可以在`BaseModel.model_dump()`中传入

   ```python
   model_dump(
       *,
       mode: Literal["json", "python"] | str = "python",
       include: IncEx | None = None,
       exclude: IncEx | None = None,
       context: Any | None = None,
       by_alias: bool | None = None,
       exclude_unset: bool = False,
       exclude_defaults: bool = False,
       exclude_none: bool = False,
       round_trip: bool = False,
       warnings: (
           bool | Literal["none", "warn", "error"]
       ) = True,
       fallback: Callable[[Any], Any] | None = None,
       serialize_as_any: bool = False
   ) -> dict[str, Any]
   ```
   
   在参数中重点关注 include， exclude，context



### 2.2.1 include 和 exclude

include 和 exclude 两个参数，可以控制哪些field应该被序列化，哪些应该被排除

```python
from pydantic import BaseModel, SecretStr

class User(BaseModel):
    id: int
    username: str
    password: SecretStr


class Transaction(BaseModel):
    id: str
    user: User
    value: int


t = Transaction(
    id='1234567890',
    user=User(id=42, username='JohnDoe', password='hashedpassword'),
    value=9876543210,
)

# using a set:
print(t.model_dump(exclude={'user', 'value'}))
#> {'id': '1234567890'}

# using a dict:
print(t.model_dump(exclude={'user': {'username', 'password'}, 'value': True}))
#> {'id': '1234567890', 'user': {'id': 42}}

print(t.model_dump(include={'id': True, 'user': {'id'}}))
#> {'id': '1234567890', 'user': {'id': 42}}
```



### 2.2.2 context

可以在`model_dump()`传入一些序列化时需要用到的参数，是一个字典结构

```python
from pydantic import BaseModel, SerializationInfo, field_serializer


class Model(BaseModel):
    text: str

    @field_serializer('text')
    def remove_stopwords(self, v: str, info: SerializationInfo):
        context = info.context
        if context:
            stopwords = context.get('stopwords', set())
            v = ' '.join(w for w in v.split() if w.lower() not in stopwords)
        return v


model = Model.model_construct(**{'text': 'This is an example document'})
print(model.model_dump())  # no context
#> {'text': 'This is an example document'}
print(model.model_dump(context={'stopwords': ['this', 'is', 'an']}))
#> {'text': 'example document'}
print(model.model_dump(context={'stopwords': ['document']}))
#> {'text': 'This is an example'}
```







## 2.3 serializer执行顺序

1. 执行顺序
   - 先进入`model validator`，
   - 然后针对每个字段进入对应的`field validator`, 
   - 最后返回`model validator`



2. 代码验证

   ```python
   from datetime import datetime
   from pydantic import BaseModel, field_serializer, model_serializer
   from typing import Any, Dict
   
   class NestedModel(BaseModel):
       """嵌套模型，用于验证递归序列化"""
       nested_field: str
       nested_timestamp: datetime
       
       @field_serializer('nested_timestamp')
       def serialize_nested_timestamp(self, dt: datetime, _info):
           print("🔹 执行嵌套模型的字段序列化器 (nested_timestamp)")
           return dt.strftime('嵌套时间: %Y-%m-%d')
   
   class User(BaseModel):
       """主模型，包含所有序列化器类型"""
       name: str
       age: int
       signup_date: datetime
       nested: NestedModel
       
       # 字段序列化器 - 最高优先级
       @field_serializer('signup_date')
       def serialize_signup_date(self, dt: datetime, _info):
           print("🔹 执行字段序列化器 (signup_date)")
           return dt.strftime('注册时间: %Y-%m-%d %H:%M:%S')
       
       @field_serializer('age')
       def serialize_age(self, age: int, _info):
           print("🔹 执行字段序列化器 (age)")
           return f"年龄: {age}岁"
       
       # 模型序列化器 - 次优先级
       @model_serializer(mode='wrap')
       def serialize_model(self, handler):
           print("🔸 开始执行模型序列化器")
           print("🔸 首先调用 handler（触发字段序列化器和默认逻辑）...")
           
           # 调用handler会触发字段序列化器和默认序列化逻辑
           result = handler(self)
           print(f"🔸 handler返回的中间结果: {result}")
           
           # 模型序列化器可以对结果进行全局修改
           print("🔸 模型序列化器进行后处理...")
           result['processed_by'] = 'model_serializer'
           result['welcome_message'] = f"欢迎, {result['name']}!"
           
           # 甚至可以修改已经被字段序列化器处理过的值
           result['age'] = result['age'] + " (已验证)"
           
           return result
   
   # 创建测试数据
   print("🚀 创建测试实例...")
   test_user = User(
       name="张三",
       age=25,
       signup_date=datetime(2023, 10, 27, 14, 30, 0),
       nested=NestedModel(
           nested_field="嵌套值",
           nested_timestamp=datetime(2023, 11, 1, 10, 0, 0)
       )
   )
   
   print("\n🎯 开始调用 model_dump()...")
   print("=" * 50)
   
   result = test_user.model_dump()
   
   print("=" * 50)
   print("\n📋 最终序列化结果:")
   print(result)
   ```

   输出

   ```
   ==================================================
   🔸 开始执行模型序列化器
   🔸 首先调用 handler（触发字段序列化器和默认逻辑）...
   🔹 执行字段序列化器 (age)
   🔹 执行字段序列化器 (signup_date)
   🔹 执行嵌套模型的字段序列化器 (nested_timestamp)
   🔸 handler返回的中间结果: {'name': '张三', 'age': '年龄: 25岁', 'signup_date': '注册时间: 2023-10-27 14:30:00', 'nested': {'nested_field': '嵌套值', 'nested_timestamp': '嵌套时间: 2023-11-01'}}
   🔸 模型序列化器进行后处理...
   ==================================================
   
   📋 最终序列化结果:
   {'name': '张三', 'age': '年龄: 25岁 (已验证)', 'signup_date': '注册时间: 2023-10-27 14:30:00', 'nested': {'nested_field': '嵌套值', 'nested_timestamp': '嵌套时间: 2023-11-01'}, 'processed_by': 'model_serializer', 'welcome_message': '欢迎, 张三!'}
   ```

   





## 2.4 Duck Typing 序列化

1. 此处的“鸭子类型”是指：

   - 在数据类型声明时，使用的是基类，而实际传入的是派生类实例（该情况在框架搭建时十分常见）
   
   ```python
   from pydantic import BaseModel
   
   class Base(BaseModel):
       id: int
       name: str
   
   
   class User(Base):
       password: str
   
   
   class Login(BaseModel):
       created_at: str
       account: Base
   
   data = {
       "account":{
           "id": 123,
           "name": "John Doe",
           "password": "securepassword"
       },
       "created_at": "2023-10-01T12:00:00Z"
   }
   login = Login(**data)
   print(login)            # created_at='2023-10-01T12:00:00Z' account=Base(id=123, name='John Doe')
   ```
   
   在account的类型声明时，使用的是`Base`，而实际传入的是`User`实例
   
   因此在打印时，只打印了Base属性的id和name，没有password
   
   
   
   

2. `SerializeAsAny[<SomeType>]` 类型注解

   - **验证时**：像普通的 `<SomeType>` 一样进行验证
   - **序列化时**：像 `Any` 类型一样进行序列化（保留实际对象的完整信息）

   ```python
   from pydantic import BaseModel, SerializeAsAny
   
   class Animal(BaseModel):
       name: str
   
   class Dog(Animal):
       breed: str
   
   class Zoo(BaseModel):
       # 使用 SerializeAsAny 来保留子类的所有字段
       animals: list[SerializeAsAny[Animal]]
   
   # 验证时当作 Animal，但序列化时保留 Dog 的所有字段
   zoo = Zoo(animals=[Dog(name="Buddy", breed="Golden Retriever")])
   
   print(zoo.model_dump_json())
   # 输出: {"animals": [{"name": "Buddy", "breed": "Golden Retriever"}]}
   # 如果不使用 SerializeAsAny，breed 字段会被丢弃
   ```



3. `BaseModel.model_dump(serialize_as_any=True)`实现全局的 `SerializeAsAny` 效果。

   - 该参数默认为False

   ```python
   class Animal(BaseModel):
       name: str
   
   class Dog(Animal):
       breed: str = "Unknown"
   
   class Zoo(BaseModel):
       animals: list[Animal]
           
   zoo = Zoo(animals=[Dog(name="Buddy")])
   print(zoo.model_dump_json(serialize_as_any=True))
   print(zoo.model_dump_json(serialize_as_any=False))
   
   #  输出: 
   # {"animals":[{"name":"Buddy","breed":"Unknown"}]}
   # {"animals":[{"name":"Buddy"}]}
   ```

   


## 2.5 自定义类的序列化

```python
from pydantic import BaseModel, field_serializer

class Custom:
    def __init__(self, value: str):
        self.value = value
    
    def serialize(self) -> str:
        return f"CustomSerialized {self.value}"
    

class Item(BaseModel):

    class Config:
        arbitrary_types_allowed = True

    id: int
    name: str
    custom_field: Custom

    @field_serializer('custom_field')
    def serialize_custom_field(self, value: Custom) -> str:
        return value.serialize()
    
data = {
    "id": 1,
    "name": "Sample Item",
    "custom_field": Custom("example")
}
item = Item(**data)
print(item.model_dump())        # {'id': 1, 'name': 'Sample Item', 'custom_field': 'CustomSerialized example'}
```





# 3. 其他

## 3.1 model_copy

可以选择是浅拷贝还是深拷贝

```python
from pydantic import BaseModel


class BarModel(BaseModel):
    whatever: int


class FooBarModel(BaseModel):
    banana: float
    foo: str
    bar: BarModel


m = FooBarModel(banana=3.14, foo='hello', bar={'whatever': 123})

print(m.model_copy(update={'banana': 0}))
#> banana=0 foo='hello' bar=BarModel(whatever=123)
print(id(m.bar) == id(m.model_copy().bar))					# 浅拷贝
#> True

# normal copy gives the same object reference for bar
print(id(m.bar) == id(m.model_copy(deep=True).bar))			# 深拷贝
#> False
# deep copy gives a new object reference for `bar`
```



## 3.2 model_json_schema

将model自动生成标准的`JSONSchema`描述文件

- [JSONSchema笔记](https://github.com/a171232886/Note_Python/blob/main/JSONSchema.md)

对于生成（网络后端）接口描述文件，十分有帮助

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from enum import Enum

# 定义一个枚举类，表示用户角色
class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

# 继承 BaseModel 来创建我们的模型
class User(BaseModel):
    name: str = Field(..., min_length=1, max_length=20, description="用户的真实姓名")
    email: EmailStr  # 专用邮箱字符串类型，会自动进行格式验证
    age: int = Field(ge=0, le=120, description="用户的年龄")  # ge:大于等于，le:小于等于
    role: Role = Role.USER  # 使用枚举类型，并设置默认值为 Role.USER
    nickname: Optional[str] = Field(
        None, min_length=3, max_length=15, description="用户的昵称，可选"
    )  # 可选字段，默认值为 None

    # 可选的模型配置
    class Config:
        title = "用户模型"  # 为生成的 Schema 设置标题
        schema_extra = {
            "example": {
                "name": "张三",
                "email": "zhangsan@example.com",
                "age": 25,
                "role": "user",
                "nickname": "小三"
            }
        }


import json
schema = User.model_json_schema()
print(json.dumps(schema, indent=2, ensure_ascii=False))
```

输出

```json
{
  "$defs": {
    "Role": {
      "enum": [
        "admin",
        "user",
        "guest"
      ],
      "title": "Role",
      "type": "string"
    }
  },
  "example": {
    "age": 25,
    "email": "zhangsan@example.com",
    "name": "张三",
    "nickname": "小三",
    "role": "user"
  },
  "properties": {
    "name": {
      "description": "用户的真实姓名",
      "maxLength": 20,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "email": {
      "format": "email",
      "title": "Email",
      "type": "string"
    },
    "age": {
      "description": "用户的年龄",
      "maximum": 120,
      "minimum": 0,
      "title": "Age",
      "type": "integer"
    },
    "role": {
      "$ref": "#/$defs/Role",
      "default": "user"
    },
    "nickname": {
      "anyOf": [
        {
          "maxLength": 15,
          "minLength": 3,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "用户的昵称，可选",
      "title": "Nickname"
    }
  },
  "required": [
    "name",
    "email",
    "age"
  ],
  "title": "用户模型",
  "type": "object"
}
```

