# 1. 测试框架

测试框架：抽象出来的工具集合，提供大量组件、工具、功能

- 用例发现
- 用例管理
- 环境管理
- 用例执行
- 测试报告



`pytest` 完全兼容 `unittest`

`pytest`对 assert 进行高级封装 （AST），这对python数据结构很友好 



# 2. 快速上手

1. 安装

   ```
   pip install pytest
   ```

   

2. 执行

   - 终端执行

     ```
     pytest
     ```

   - 代码执行

     ```python
     # main.py
     import pytest
     
     pytest.main()
     ```

     

# 3. 看懂结果

## 3.1 样例

```python
# main.py
import pytest

def test_number():
    assert 1 == 2

def test_str():
    assert "aaa" == "aaac"
    
def test_list():
    a = [1, 2, 3]
    b = [1, 2, 4]
    assert a == b    
    
def test_dict():
    a = {"a": 1, "b": 2}
    b = {"a": 1, "b": 3}
    assert a == b
    
pytest.main()
```



输出

```bash
============================================ test session starts ===========================================
platform linux -- Python 3.12.10, pytest-8.3.5, pluggy-1.6.0
rootdir: /home/dell/wh/code/test/lr_pytest
configfile: pytest.ini
collected 4 items                                                                                              

test_demo.py FFFF                                                                                        [100%]

=============================================== FAILURES ==================================================
_____________________________________________ test_number __________________________________________________

    def test_number():
>       assert 1 == 2
E       assert 1 == 2

test_demo.py:4: AssertionError
_______________________________________________ test_str __________________________________________________

    def test_str():
>       assert "aaa" == "aaac"
E       AssertionError: assert 'aaa' == 'aaac'
E         
E         - aaac
E         ?    -
E         + aaa

test_demo.py:7: AssertionError
_______________________________________________ test_list _______________________________________________

    def test_list():
        a = [1, 2, 3]
        b = [1, 2, 4]
>       assert a == b
E       assert [1, 2, 3] == [1, 2, 4]
E         
E         At index 2 diff: 3 != 4
E         Use -v to get more diff

test_demo.py:12: AssertionError
__________________________________________________ test_dict _______________________________________________

    def test_dict():
        a = {"a": 1, "b": 2}
        b = {"a": 1, "b": 3}
>       assert a == b
E       AssertionError: assert {'a': 1, 'b': 2} == {'a': 1, 'b': 3}
E         
E         Omitting 1 identical items, use -vv to show
E         Differing items:
E         {'b': 2} != {'b': 3}
E         Use -v to get more diff

test_demo.py:17: AssertionError
=========================================== warnings summary ===============================================
../../../../miniconda3/envs/wh_test/lib/python3.12/site-packages/_pytest/config/__init__.py:1500
  /home/dell/miniconda3/envs/wh_test/lib/python3.12/site-packages/_pytest/config/__init__.py:1500: PytestConfigWarning: No files were found in testpaths; consider removing or adjusting your testpaths configuration. Searching recursively from the current directory instead.
    self.args, self.args_source = self._decide_args(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================================= short test summary info ============================================
FAILED test_demo.py::test_number - assert 1 == 2
FAILED test_demo.py::test_str - AssertionError: assert 'aaa' == 'aaac'
FAILED test_demo.py::test_list - assert [1, 2, 3] == [1, 2, 4]
FAILED test_demo.py::test_dict - AssertionError: assert {'a': 1, 'b': 2} == {'a': 1, 'b': 3}
====================================== 4 failed, 1 warning in 0.05s ========================================
```



## 3.2 构成

1. 执行环境：版本、根目录、用例数量

   ```
   ========================================== test session starts =========================================
   platform linux -- Python 3.12.10, pytest-8.3.5, pluggy-1.6.0
   rootdir: /home/dell/wh/code/test/lr_pytest
   configfile: pytest.ini
   collected 4 items  
   ```

   

2. 执行过程：文件名称、用力结果、执行进度

   ```
   test_demo.py FFFF                                                                              [100%]
   ```



3. 失败原因：用例内容、断言提示

   ```
   ___________________________________________ test_number ________________________________________________
   
       def test_number():
   >       assert 1 == 2
   E       assert 1 == 2
   
   test_demo.py:4: AssertionError
   ```

   

4. 整体摘要：结果情况、结果数量、花费时间

   ```
   ======================================= short test summary info =========================================
   FAILED test_demo.py::test_number - assert 1 == 2
   FAILED test_demo.py::test_str - AssertionError: assert 'aaa' == 'aaac'
   FAILED test_demo.py::test_list - assert [1, 2, 3] == [1, 2, 4]
   FAILED test_demo.py::test_dict - AssertionError: assert {'a': 1, 'b': 2} == {'a': 1, 'b': 3}
   ====================================== 4 failed, 1 warning in 0.05s =====================================
   ```

   

## 3.3 结果类型

用例结果缩写

| 缩写 |  单词   | 含义                       |
| :--: | :-----: | -------------------------- |
|  .   | passed  | 通过                       |
|  F   | failed  | 失败（用例执行报错）       |
|  E   |  error  | 出错（fixture执行报错）    |
|  s   | skipped | 跳过                       |
|  X   | xpassed | 预期外的通过（不符合预期） |
|  x   | xfailed | 预期内的失败（符合预期）   |



# 4. 用例规则

## 4.1 用例发现规则

1. 用例发现：测试框架在识别、加载用例的过程

2. pytest的用例发现

   - 遍历所有的目录，对目录名没有要求

     （跳过`venv`和隐藏目录）

   - 打开以`test_`开头或以`_test`结尾的python文件
   - 遍历所有的以`Test`开头的类
     - 搜集所有的以`test_`开头的函数或方法

3. 按目前发现规则：

   ```python
   def test_func():
       pass
   
   a = test_func
   ```

   pytest 会将 `a` 也看做测试用例

   

## 4.2 用例内容规则

> pytest 8.4 增加了一个强制要求

pytest对用例的要求：

1. 可调用的（函数、方法、类、对象）
2. 以`test_`开头
3. 没有参数（参数有另外含义）
4. 没有返回值（默认为None）



```python
def add(a, b):
    return a+b

class TestAdd:
    def test_int(self):
        res = add(1,3)
        assert res == 4
        
    def test_str(self):
        res = add("1", "3")
        assert res == "13"
```



#  5. 配置框架

配置可以改变pytest默认的规则：

## 5.1 命令参数

1. 比如`pytest -v`

2. 常用参数

   - `-v`：显示更多信息

   - `-s`：停止IO捕获，在用例中正常使用输入输出。

     比如，当测试用例中出现`a = input()`时，需要使用。

     但在自动化测试中，不应该出现输入输出

   - `-x`：快速退出。出现一个失败用例，立刻停止全部测试

   - `-m`：用例筛选

## 5.2 配置文件





# 6. 标记mark

对用例进行标记，进而进行不同处理

一个用例可以添加多个标记

## 6.1 用户自定义标记

**只能实现用例筛选**

步骤

- 注册
- 标记
- 筛选



1. 注册

   编写配置文件

   ```ini
   # pytest.ini
   
   [pytest]
   
   markers = 
       api: 接口测试
       web: UI测试
       ut: 单元测试
       login: 登录测试
       ddt: 数据驱动测试
   ```
   
   验证
   
   ```bash
   pytest --markers
   ```
   
   输出
   
   ```
   @pytest.mark.api: 接口测试
   
   @pytest.mark.web: UI测试
   
   @pytest.mark.ut: 单元测试
   
   @pytest.mark.login: 登录测试
   
   ...
   ```



2. 标记

   ```python
   @pytest.mark.api
   def test_api():
   	pass
   ```




3. 筛选

   只执行标记为`api`的测试用例

   ```
   pytest -m api
   ```

   

## 6.2 框架内置标记

用例增加特殊执行效果



常用的的内置标记

- `skip`：无条件跳过
- `skipif`：有条件跳过
- `xfail`：预期失败
- `parametrize`：参数化
- `usefixtures`：使用fixtures



1. 样例一

   ```python
   import pytest
   
   def add(a, b):
       return a+b
   
   class TestAdd:
       
       @pytest.mark.api
       @pytest.mark.skipif(True, reason="Skipping this test")
       def test_int(self):
           res = add(1,3)
           assert res == 4
       
       @pytest.mark.xfail
       def test_str(self):
           res = add("1", "3")
           assert res == "14"
   ```

   

2. 参数化与数据驱动测试

   - 数据驱动测试 = 参数化测试 + 数据文件

   - 根据数据文件的内容，动态决定用例的数量和内容



# 7. 数据驱动测试参数

1. 数据文件，驱动用例执行数量和内容

2. 样例代码

   ```python
       @pytest.mark.parametrize("a, b, expected", [
           (1, 2, 3),
           (4, 5, 9),
           (10, 20, 30)
       ])
       def test_ddt(self, a, b, expected):
           assert add(a, b) == expected
           
   ```

   **通常从数据文件中读取数据，而不是直接将数据写好**

   

   比如，使用手动编写的`read_csv()`函数产生全部数据

   ```
   @pytest.mark.parametrize("a, b, expected", read_csv())
   ```

   

# 8. 夹具fixture

夹具：在用例**执行之前、执行之后**，自动运行代码

场景：

- 之前：加密参数，之后：解密结果
- 之前：启动浏览器，之后：关闭浏览器
- 之前：注册、登录账号，之后：删除账号  



## 8.1 创建fixture

```python
@pytest.fixture
def f():
    # 前置操作
    print(time.time(), "开始执行")
    
    yield # 执行用例
    
    # 后置操作
    print(time.time(), "执行结束")
    
```



## 8.2 使用fixture

1. 第一种方式：推荐方式

   ```python
   def test_1(f):
       pass
   ```

   

2. 第二种方式：给用例加上标记

   ```python
   @pytest.mark.usefixtures("f")
   def test_2():
       pass
   ```

   



## 8.3 高级方法

1. 自动使用：所有用例自动使用

   ```python
   @pytest.fixture(autouse=True)
   def f():
       pass
   ```

   

2. 依赖使用

   `f`在执行前先执行`ff`

   ```python
   @pytest.fixture()
   def ff():
       pass
   
   @pytest.fixture()
   def f(ff):
       pass
   ```

   

3. 返回内容

   ```python
   @pytest.fixture
   def f():
       # 前置操作
       print(time.time(), "开始执行")
       
       yield "fixture_result"  # 执行用例
       
       # 后置操作
       print(time.time(), "执行结束")
       
   
   def test(f):
       print("收到fixture的结果", f)
   ```

   

4. 范围共享

   适用于昂贵的初始化（如数据库连接、浏览器启动）

   - 默认范围：`function`，本函数内

   - 全局范围：`session`

     - 在根目录下，创建`conftest.py`，需要共享的`fixture`放此处。
     
     - `pytest`会自动发现`conftest.py`，保证全局用例都能获取到。
     
       
   
   ```python
   # conftest.py
   @pytest.fixture(autouse=True, scope="session")
   def f():
       # 前置操作
       print(time.time(), "开始执行")
       
       yield "fixture_result"  # 执行用例
       
       # 后置操作
       print(time.time(), "执行结束")
       
   ```
   
   ```python
   # test_1.py
   def test_1(f):
       print("收到fixture的结果", f)
   ```
   
   ```python
   # test_2.py 
   def test_2(f):
       print("收到fixture的结果", f)
   ```
   
   
   
   输出
   
   ```bash
   test_fixture.py::test_1 1749631063.1157985 开始执行
   收到fixture的结果 fixture_result
   PASSED
   test_fixture.py::test_2 收到fixture的结果 fixture_result
   PASSED1749631063.1164677 执行结束
   ```
   
   可以看到，`开始执行`只输出了一次



# 9. 插件管理

1. 插件类型：
   - 内置插件：不需要安装
   - 第三方插件

2. 插件启用管理
   - 启用：`-p <插件名>`
   - 禁用：`-p no:<插件名>`

3. 插件使用方式
   - 参数方式
   - 配置文件
   - `fixture`
   - 标记mark



# 10. 常用第三方插件

1. pytest收录的插件

   https://docs.pytest.org/en/stable/reference/plugin_list.html



## 10.1 pytest-html

1. 用途：生成HTML报告

2. 安装

   ```
   pip install pytest-html
   ```

3. 使用

   ```
   pytest --html=report.html --self-contained-html
   ```

   也可以在`pytest.ini`中添加

   ```
   addopts = -s --html=report.html --self-contained-html
   ```



## 10.2 pytest-xdist

1. 用途：分布式执行。**默认使用多进程实现**

   **注意**：

   - 启动多进程，本身就有时间消耗
   - 分布式执行，有并发、资源竞争等问题

2. 安装

   ```
   pip install pytest-xdist
   ```

3. 使用

   ```
   -n 12
   ```

   创建12个进程
   
   



## 10.3 pytest-rerunfailures

1. 用途：用例失败后，重新执行

   针对网络波动、UI渲染等问题

2. 安装

   ```
   pip install pytest-rerunfailures
   ```

3. 使用

   ```
   --reruns 5 --reruns-delay 1
   ```

   - 失败后重新执行5次，若有一次成功，则用例通过
   - 在重试前先等待1秒

   

## 10.4 pytest-result-log

1. 用途：把用例的执行结果记录到日志文件中

2. 安装：

   ```
   pip install pytest-result-log
   ```

3. 使用

   ```ini
   # pytest.ini
   
   log_file = logs/test.log
   log_file_level = INFO
   log_file_format = %(asctime)s - %(name)s - %(levelname)s - %(message)s
   log_file_date_format = %Y-%m-%d %H:%M:%S
   
   ; 是否启用结果日志
   result_log_enable = 1
   ; 结果日志分隔线                
   result_log_separator = 1
   ; 分割线等级
   result_log_level_separator = warning
   ; 结果日志详细等级
   result_log_level_verbose = info
   ```

   注意：`ini`文件中的注释是以`;`开头



# 11. 企业级测试报告

## 11.1 基础使用

1. `allure`是一个测试报告框架，支持多种语言。

   **allure网页效果很友好**

   - https://allurereport.org/docs/install-for-linux/#install-from-a-deb-package
   - https://github.com/allure-framework/allure2/releases/tag/2.34.0

   下载对应`deb`包，然后`sudo dpkg -i <allure包>.deb`

2. 安装对应pytest插件

   ```
   pip install allure-pytest
   ```

3. 配置

   ```
   --alluredir=temps --clean-alluredir
   ```

   - 执行pytest时，只是将数据保存到`temps`，并没有生成报告
   - 新生成的数据覆盖已有的报告

4. 生成报告

   ```
   allure generate -o report -c temps
   ```

   生成报告到`report`文件夹，数据来源是`temps`文件夹



## 11.2 分组和关联

1. allure 支持对用例进行分组和关联（敏捷开发术语）

   四个级别

   ```python
   @allure.epic		# 史诗，表示里程碑
   @allure.feature		# 主题，表示模块
   @allure.story		# 故事，表示功能
   @allure.title		# 标题，表示用例
   ```

   - 使用相同装饰器，自动分为一组
   - 一个用例可以在很多组

2. 脚本

   ```python
   import allure
   
   @allure.epic("e1")		
   @allure.feature("f1")	
   @allure.story("s1")		
   @allure.title("t1")		
   def test_1():
       """
       测试用例1
       """
       assert True
   
   
   @allure.epic("e1")		
   @allure.feature("f1")	
   @allure.story("s2")		
   @allure.title("t2")
   def test_2():
       """
       测试用例2
       """
       assert True
   
   
   @allure.title("t3")
   def test_3():
       """
       测试用例3
       """
       assert True
       
       
   @allure.feature("f2")
   def test_4():
       """
       测试用例4
       """
       assert True    
   
   ```

   

3. 执行效果

   <img src="images/pytest/image-20250612170243655.png" alt="image-20250612170243655" style="zoom:80%;" />

   - 建议四个级别写完整



# 12. Web自动化测试实战

1. 安装 `selenium` 插件

   ```
   pip install pytest-selenium
   ```

2. 使用

   ```
   --driver chrome
   ```

   ```python
   import pytest
   
   @pytest.mark.web
   def test_web_1(selenium):
       selenium.get("https://www.baidu.com")
       print("Web test 1 executed")
       print(selenium.title)
   ```

   



# 13. 测试框架封装

封装：

- 隐藏细节
- 增加功能
- 优化功能



接口自动化封装：

- 使用yaml作为用例，降低自动化门槛
- 自动请求接口、断言接口
- 自动在日志记录HTTP报文
- 自动生成`allure`测试报告





# 15. 接口测试用例

## 15.1 设计用例内容

1. 名字
2. 标记（可选）
3. 步骤
   - 请求接口：GET https://www.baidu.com
   - 响应断言：status_code == 200
   - 提取变量：json()['code']



## 15.2 YAML的样例

```yaml
name: 登录成功用例
steps:
  - request: # 发送请求
      method: POST
      url: http://example.com/api/login
      headers:
        Content-Type: application/json
      body:
        username: testuser
        password: testpassword
  
  - response: # 响应验证
      status_code: 200
      body:
        message: 登录成功
        token: 
          type: string
          description: 用户登录后返回的令牌
      headers:
        Content-Type: application/json
    
  - extract: # 提取令牌
      token: $.body.token
```





# 16. 封装接口自动化框架

## 16.1 请求接口

1. 使用`requests`库发送网络连接

   ```python
   import requests
   
   response = requests.request(
       method='GET', 
       url='https://example.com', 
       params={'key': 'value'}, 
       headers={'User-Agent': 'my-app'}
   )
   ```

   



## 16.2 断言响应

1. 使用python的 assert

   ```python
   assert response.status_code == 200
   assert response.json()["data"] == "hello world"
   ```



2. 使用`jsonschema`

   ```
   pip install jsonschema
   ```



## 16.3 jsonschema

### 16.3.1 基础

openapi规范中遵循的接口描述方式就是jsonschema

- 当前都是基于2020-12版本（最新）

JSON Schema的官网：

- https://json-schema.org/
- https://json-schema.org/specification



1. 基础用法

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

   



2. 升级

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

   

3. 引用和复用

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




### 16.3.2 错误分析

1. 基本错误捕获

最简单的错误处理方式是捕获 `ValidationError` 异常：

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



2. 获取多个错误

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



3. 错误对象属性

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







## 16.4 变量提取

基本原则：

- JSON: JSONPATH

  ```
  pip install jsonpath-ng
  ```

  

- HTML: XPATH

- 字符串：re
  - 可用来兜底

### 16.4.1 jsonpath的使用

1. 基础

   ```python
   import json
   from jsonpath_ng import parse
   
   # 示例 JSON 数据
   data = {
       "store": {
           "book": [
               {
                   "category": "reference",
                   "author": "Nigel Rees",
                   "title": "Sayings of the Century",
                   "price": 8.95
               },
               {
                   "category": "fiction",
                   "author": "Evelyn Waugh",
                   "title": "Sword of Honour",
                   "price": 12.99
               }
           ],
           "bicycle": {
               "color": "red",
               "price": 19.95
           }
       }
   }
   
   # 解析 JSONPath 表达式
   jsonpath_expr = parse("$.store.book[*].author")
   
   # 查找匹配项
   matches = [match.value for match in jsonpath_expr.find(data)]
   print(matches)  # 输出: ['Nigel Rees', 'Evelyn Waugh']
   ```
   
   获取全部的价格
   
   ```
   jsonpath_expr = parse("$..price")
   prices = [match.value for match in jsonpath_expr.find(data)]
   print(prices)  # [8.95, 12.99, 19.95]
   ```
   
   





## 16.5 封装

```yaml
name: 登录成功用例
steps:
  - request: # 发送请求
      method: POST
      url: http://example.com/api/login
      headers:
        Content-Type: application/json
      body:
        username: testuser
        password: testpassword
  
  - response: # 响应验证
      status_code: 200
      body:
        message: 登录成功
        token: 
          type: string
          description: 用户登录后返回的令牌
      headers:
        Content-Type: application/json
    
  - extract: # 提取令牌
      token: $.body.token
```







