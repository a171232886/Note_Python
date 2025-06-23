# 14. YAML文件格式

1. YAML: YAML Ain't Markup Language 

   - **YAML完全兼容JSON格式，并且支持Python相似写法**
   - 广泛应用于 Kubernetes、Ansible、Docker Compose 等工具的配置文件中
   - YAML文件在python中被读取为dict

   

2. 安装

   ```
   pip install pyyaml
   ```



3. 简单样例

   ```yaml
   # config.yaml
   name: "test"
   age: 27
   ```

   ```python
   import yaml
   
   with open("config.yaml", "r") as file:
       config = yaml.safe_load(file)
       
   print(config)
   ```

   

## 14.1 格式

1. 要点

   - `#` ：注释
   - `null` ：表示空值
   - 成员：通过缩进表示

   ```yaml
   # config.yaml
   name: 登录成功用例
   steps:
     request: # 发送请求
       method: POST
       url: http://example.com/api/login
       headers:
       Content-Type: application/json
       body:
       username: testuser
       password: testpassword
     
     response: 
       status_code: 200
   
     extract: null
   ```

   python读入后

   ```python
   {
     "name": "登录成功用例",
     "steps": {
       "request": {
         "method": "POST",
         "url": "http://example.com/api/login",
         "headers": {
           "Content-Type": "application/json"
         },
         "body": {
           "username": "testuser",
           "password": "testpassword"
         }
       },
       "response": {
         "status_code": 200
       },
       "extract": None
     }
   }
   ```

   

2. 数组或列表的两种表示方法：

   - 元素前添加`-` （不推荐）
   - 直接使用列表表示

   

   ```yaml
   name: 登录成功用例
   method:
     - post
     - get
   
   text: ["hello", "world"]
   
   input: [
     "how",
     "are",
     "you"
   ]
   ```

   python读取后

   ```python
   {
     "name": "登录成功用例",
     "method": [
       "post",
       "get"
     ],
     "text": [
       "hello",
       "world"
     ],
     "input": [
       "how",
       "are",
       "you"
     ]
   }
   ```

   


3. **注意**：

   - 成员中只要有一项添加了`-`，其上级均被视为数组

     ```yaml
     name: 登录成功用例
     method:
       - get: "ddd"
         post: "hello"
     ```

     python 中读取

     ```python
     {
       "name": "登录成功用例",
       "method": [
         {
           "get": "ddd",
           "post": "hello"
         }
       ]
     }
     ```

   - 同一缩进下，要么全加`-`，要么都不加

     ```yaml
     # 错误写法
     name: 登录成功用例
     method:
       - get: "ddd"
       post: "hello"
     ```

   **因此，不推荐使用`-`**

   

4. **完全按照json写**

   ```yaml
   # config.yaml
   {
     "name": "登录成功用例",
     "method": {
         "get": "ddd",
         "post": "hello"
     }
   }
     
   ```

   可正常载入



## 14.2 pyyaml基础用法

### 14.2.1 读取

1. 从文件中加载

   ```python
   with open('config.yaml', 'r') as file:
       data = yaml.safe_load(file)
   ```

2. 从字符串加载

   ```yaml
   yaml_str = """
   name: John Doe
   age: 30
   skills:
     - Python
     - JavaScript
   """
   data = yaml.safe_load(yaml_str)
   ```



3. yaml的`safe_load`和`load`的区别

   |         特性         | `safe_load`              | `load`                        |
   | :------------------: | :----------------------- | :---------------------------- |
   |      **安全性**      | 高 - 只解析基本数据类型  | 低 - 可以实例化任意Python对象 |
   |    **允许的标签**    | 仅限标准YAML标签         | 所有标签，包括自定义Python类  |
   | **执行任意代码风险** | 无                       | 有潜在风险                    |
   |       **性能**       | 稍快                     | 稍慢                          |
   |   **推荐使用场景**   | 处理不受信任的YAML输入时 | 处理完全可信的YAML输入时      |



### 14.2.2 写入

1. 转换成yaml字符串

   ```python
   data = {
       'name': 'Jane Smith',
       'age': 28,
       'skills': ['Python', 'SQL', 'Docker'],
       'employed': True
   }
   
   # 转换为 YAML 字符串
   yaml_str = yaml.dump(data)
   print(yaml_str)
   ```



2. 写入文件

   ```python
   with open('output.yaml', 'w') as file:
       yaml.dump(data, file)
   ```

   

3. `yaml.dump(data, file, indent=2, allow_unicode=True)` 

   起到的效果类似于 `json.dump(data, file, indent=2, ensure_ascii=False)`

   注意：`allow_unicode=True` 相当于json的`ensure_ascii=False`

