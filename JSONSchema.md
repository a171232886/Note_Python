# JSON Schema

1. JSON Schema的官网：

   - https://json-schema.org/
   - https://json-schema.org/specification

   当前都是基于2020-12版本（最新）

2. OpenAPI 规范中遵循的接口描述方式就是 JSON Schema

3. 安装

   ```
   pip install jsonschema
   ```

   




# 1. 快速使用

```python
from jsonschema import validate

# 定义schema
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"}
    },
    "required": ["name"]
}

# 有效数据
valid_data = {"name": "John", "age": 30}
validate(instance=valid_data, schema=schema)  # 不会抛出异常

# 无效数据
invalid_data = {"age": 30}
try:
    validate(instance=invalid_data, schema=schema)
except Exception as e:
    print(f"验证失败: {e}")
```



# 2. Schema 书写规则

1. 基本结构

   JSON Schema 本身也是一个 JSON 文档，通常要包含 `$schema` 关键字，用于说明 JSON Schema 版本

   - 使用jsonschema库时不需要
   - 通常均为2020-12版本（最新）

   ```json
   {
     "$schema": "https://json-schema.org/draft/2020-12/schema",
     // 其他规则...
   }
   ```

   

2. 类型验证

   使用 `type` 关键字定义数据类型：

   ```json
   {
     "type": "string"  // 可以是 string, number, integer, boolean, array, object, null
   }
   ```

   

## 2.1 通用关键字

主要用于提供元数据、文档说明和默认值等，

它们不会直接影响数据的验证结果（`enum`和`const`除外），但能增强 Schema 的可读性、可维护性和用户体验。



### 2.1.1 `title`

- 作用：为 Schema 或属性提供一个人类可读的标题。

- 用途：在文档或表单生成工具中显示为标签。

- 示例：

  ```json
  {
    "title": "用户信息",
    "type": "object",
    "properties": {
      "name": { "title": "姓名", "type": "string" }
    }
  }
  ```



### 2.1.2 `description`

- 作用：提供详细的描述信息，解释字段的用途或约束。

- 用途：生成文档或表单中的帮助文本。

- 示例：

  ```json
  {
    "description": "用户注册信息",
    "type": "object",
    "properties": {
      "email": {
        "description": "必须是有效的邮箱地址",
        "type": "string",
        "format": "email"
      }
    }
  }
  ```



### 2.1.3 `default`

- 作用：指定字段的默认值（如果字段未提供或为 `null`）。

- 用途：填充表单默认值或初始化数据。

- 注意：`default` 不会自动填充数据，需由解析器实现。

- 示例：

  ```json
  {
    "type": "object",
    "properties": {
      "role": {
        "type": "string",
        "default": "guest"
      }
    }
  }
  ```



### 2.1.4 `examples`

- 作用：提供字段的示例值（可以是数组，允许多个示例）。

- 用途：帮助理解字段的预期格式或内容。

- 示例：

  ```json
  {
    "type": "string",
    "examples": ["foo", "bar"]
  }
  ```



### 2.1.5 `enum`

- 作用：限制字段只能取枚举列表中的值。

- 用途：实现下拉选择或固定选项。

- 示例：

  ```json
  {
    "type": "string",
    "enum": ["admin", "user", "guest"]
  }
  ```



### 2.1.6 `const`

- 作用：字段必须严格等于指定的固定值（**类似单值的 `enum`**）。

- 用途：验证字段是否为特定值。

- 示例：

  ```json
  {
    "type": "string",
    "const": "active"
  }
  ```



### 2.1.7 `$comment`

- 作用：添加开发者注释（不会被验证器处理）。

- 用途：内部开发说明，类似于代码注释。

- 示例：

  ```json
  {
    "$comment": "此字段未来可能弃用，改用 user_id",
    "type": "integer"
  }
  ```



## 2.2 常用类型验证

### 2.2.1 数值验证

- `minimum`, `maximum`: 最小/最大值

- `exclusiveMinimum`, `exclusiveMaximum`: 排除边界值的最小/最大值

- `multipleOf`: 必须是指定值的倍数

```json
{
  "type": "number",
  "minimum": 0,
  "exclusiveMaximum": 100,
  "multipleOf": 5
}
```



### 2.2.2 字符串验证

- `minLength`, `maxLength`: 最小/最大长度

- `pattern`: 正则表达式模式

- `format`: 预定义格式(email, uri, date-time等)

```json
{
  "type": "string",
  "minLength": 3,
  "maxLength": 20,
  "pattern": "^[A-Za-z]+$",
  "format": "email"
}
```



### 2.2.3 数组验证

- `items`: 定义数组元素的模式

- `minItems`, `maxItems`: 最小/最大元素数量

- `uniqueItems`: 元素是否必须唯一

- `contains`: 数组必须包含至少一个匹配项

```json
{
  "type": "array",
  "items": { "type": "string" },
  "minItems": 1,
  "uniqueItems": true
}
```



### 2.2.4 对象验证

- `properties`: 定义属性及其模式

- `required`: 必需属性列表

- `additionalProperties`: 是否允许额外属性

- `propertyNames`: 属性名的模式

- `minProperties`, `maxProperties`: 最小/最大属性数量

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "age": { "type": "integer" }
  },
  "required": ["name"],
  "additionalProperties": false
}
```



## 2.3 组合模式

- `allOf`: 必须满足所有子模式

- `anyOf`: 满足任意一个子模式

- `oneOf`: 必须满足且仅满足一个子模式

- `not`: 不能匹配指定模式

```json
{
  "oneOf": [
    { "type": "string", "maxLength": 5 },
    { "type": "number", "minimum": 0 }
  ]
}
```



## 2.4 条件验证



## 2.5 引用和复用

- `$defs` (或 `definitions`): 定义可复用的子模式
- `$ref`: 引用定义的模式

```python
{
  "$defs": {
    "address": {
      "type": "object",
      "properties": {
        "street": { "type": "string" },
        "city": { "type": "string" }
      }
    }
  },
  "properties": {
    "shippingAddress": { "$ref": "#/$defs/address" },
    "billingAddress": { "$ref": "#/$defs/address" }
  }
}
```





## 2.6 样例

```python
{
  "type": "object",
  "properties": {
    "username": {
      "type": "string",
      "minLength": 4,
      "maxLength": 20,
      "pattern": "^[a-z0-9_]+$"  #正则：只允许小写字母、数字和下划线
    },
    "role": {
      "type": "string",
      "enum": ["admin", "user", "guest"]  # 枚举值
    },
    "age": {
      "type": "integer",
      "minimum": 18,
      "maximum": 99
    },
    "email": {
      "type": "string",
      "format": "email",
      "pattern": ".+@.+\\..+"  # 简单邮箱正则
    },
    "contact": {				# 结构嵌套
      "type": "object",
      "properties": {
        "email": {
          "type": "string",
          "format": "email"
        },
        "phone": {
          "type": "string",
          "pattern": "^\\+?[0-9]{10,15}$"
        }
      },
      "required": ["email"]
    }
  },
  "required": ["username", "email"]
}
```



2. 引用和复用

   ```python
   schema = {
       "definitions": {
           "address": {
               "type": "object",
               "properties": {
                   "street": {"type": "string"},
                   "city": {"type": "string"}
               },
               "required": ["street", "city"]
           }
       },
       "type": "object",
       "properties": {
           "home_address": {"$ref": "#/definitions/address"},
           "work_address": {"$ref": "#/definitions/address"}
       }
   }
   ```




# 3. 错误分析

## 3.1 基本错误捕获

1. 最简单的错误处理方式是捕获 `ValidationError` 异常：

   ```python
   from jsonschema import validate, ValidationError
   
   schema = {
       "type": "object",
       "properties": {
           "name": {"type": "string"},
           "age": {"type": "integer"}
       },
       "required": ["name"]
   }
   
   data = {"age": "30"}  # 错误：age应该是整数，且缺少name
   
   try:
       validate(instance=data, schema=schema)
   except ValidationError as e:
       print(f"验证失败: {e.message}")
       print(f"错误路径: {e.json_path}")  # 错误在数据中的位置
       print(f"错误值: {e.instance}")    # 引发错误的值
       print(f"期望的规则: {e.schema}")  # schema中的验证规则
   ```

   



2. 错误对象属性

   `ValidationError` 对象包含以下有用属性：
   
   | 属性          | 描述                               |
   | :------------ | :--------------------------------- |
   | `message`     | 人类可读的错误信息                 |
   | `path`        | 错误在数据结构中的路径（列表形式） |
   | `json_path`   | 错误路径的JSON Path表示            |
   | `schema_path` | 错误在schema中的路径               |
   | `instance`    | 引发错误的实际值                   |
   | `schema`      | 相关的schema规则                   |
   | `context`     | 对于复合验证器，包含子错误         |
   | `cause`       | 底层异常（如果有）                 |



## 3.2 获取多个错误

默认情况下，`validate()` 在遇到第一个错误时就停止。要收集所有错误，使用验证器实例：

```python
from jsonschema import Draft7Validator

validator = Draft7Validator(schema)
errors = sorted(validator.iter_errors(data), key=lambda e: e.path)

for error in errors:
    print(f"错误路径: {error.path}")
    print(f"错误信息: {error.message}")
    print("----")
```





## 3.3 样例

```python
from jsonschema import Draft7Validator, ValidationError

def validate_json(data, schema):
    validator = Draft7Validator(schema)
    errors = list(validator.iter_errors(data))
    
    if not errors:
        return True, None
    
    error_details = []
    for error in errors:
        error_details.append({
            "field": ".".join(map(str, error.path)) or "root",
            "message": error.message,
            "value": error.instance,
            "expected": error.schema.get("type") if "type" in error.schema else None
        })
    
    return False, error_details

# 使用示例
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 3},
        "age": {"type": "integer", "minimum": 18},
        "email": {"type": "string", "format": "email"}
    },
    "required": ["name", "email"]
}

data = {
    "name": "Al",
    "age": 17,
    "email": "invalid-email"
}

is_valid, errors = validate_json(data, schema)
if not is_valid:
    print("验证失败:")
    for error in errors:
        print(f"{error['field']}: {error['message']}")
```



