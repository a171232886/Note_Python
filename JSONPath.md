# JSONPath

用于从json文件中自动化提取数据

- 可在接口测试中用于提取参数



# 1. 快速开始

1. 安装

   JSONPath 有多种实现，此处使用`jsonpath-ng`

   ```
   pip install jsonpath-ng
   ```

   

2. 基础使用

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
   expr = parse("$.store.book[*].price")
   
   # 查找匹配项
   for match in expr.find(data):
       print(match.value)
   ```



3. JSONPath 表达式总是以 `$` 开头，表示 JSON 文档的根对象。

   路径使用点表示法 `.` 或方括号表示法 `[]` 来导航层次结构。

   

   ```
   $.store.book[0].title
   ```

   与

   ```
   $['store']['book'][0]['title']
   ```

   效果相同。

   但推荐使用`.`来表示成员

   

3. JSONPath表达式编写基础规则

   - `$`表示整个JSON数据

   - `.`表示下一层级（可按照对象的属性使用）

   - `*`/ `:`表示遍历所有元素

     - `book[*]` 与`book[:]`效果相同

       

4. 检索结果在`match.value`中

   ```python
   for match in expr.find(data):
       print(match.value)
   ```





# 2. 选择器

JSONPath 中的选择器(selector)是指用于从 JSON 结构中定位和提取特定数据的表达式组件。

1. 名称选择器

   选择特定名称的属性：

   ```
   $.store.book
   ```

   

2. 通配符选择器 `*`

   匹配任何属性名或数组元素：

   ```
   $.store.book[*].author  # 所有书的作者
   ```

   

3. 数组索引选择器

   选择数组中的特定元素：

   ```
   $.store.book[0]   # 第一本书
   $.store.book[-1]  # 最后一本书
   ```

   

4. 数组切片选择器 `[start:end:step]`

   类似于 Python 的切片：

   ```
   $.store.book[0:2]  # 前两本书
   $.store.book[::2]  # 每隔一本书
   ```

   

5. 递归下降选择器 `..`

   递归搜索所有层次：

   ```
   $..author	# 查找所有 author 字段
   $..book[0]  # 查找任何层次的第一个 book 元素
   ```

   

6. 过滤器表达式 `?()`

   基于逻辑表达式筛选：

   ```
   $.store.book[?(@.price < 10)]  				# 价格小于10的书
   $.store.book[?(@.category == 'fiction')]	# 小说类书籍
   ```

   注：

   - `@`表示当前层级
   - 符合条件的结果会放入一个列表中



# 3. 运算符和表达式

1. 比较运算符

   - `==` 等于

   - `!=` 不等于

   - `<` 小于

   - `<=` 小于等于

   - `>` 大于

   - `>=` 大于等于

   - `=~` 正则匹配 (某些实现支持)

     


2. 逻辑运算符

   - `&&` 与

   - `||` 或

   - `!` 非

     


3. 过滤器函数 (某些实现支持)

   ```
   $.store.book[?(@.price > avg(@[*].price))]  # 价格高于平均值的书
   ```

   



# 4. 特殊符号和用法

1. 当前节点 `@`

   在过滤器表达式中表示当前节点

   ```
   $.store.book[?(@.price < $.maxPrice)]  # 价格小于maxPrice的书
   ```

   

2. 联合路径 `,`

   选择多个路径：

   ```
   $['store']['book'][0]['title','author']  # 第一本书的标题和作者
   ```

   





# 5. 示例

**示例 JSON 数据**

```json
{
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
        "price": 12.99,
        "isbn": "0-553-21311-3"
      }
    ],
    "bicycle": {
      "color": "red",
      "price": 19.95
    }
  },
  "expensive": 10
}
```



**实用查询示例**

1. 获取所有书籍的作者：

   ```
   $.store.book[*].author
   ```



2. 获取所有作者 (递归搜索)：

   ```
   $..author
   ```



3. 获取 store 下的所有元素：

   ```
   $.store.*
   ```



4. 获取所有价格：

   ```
   $..price
   ```



5. 获取第三本书：

   ```
   $.store.book[2]
   ```



6. 获取最后一本书：

   ```
   $.store.book[-1]
   ```



7. 获取前两本书：

   ```
   $.store.book[0:2]
   ```



8. 获取有 ISBN 号的书：

   ```
   $.store.book[?(@.isbn)]
   ```



9. 获取价格低于 10 的书：

   ```
   $.store.book[?(@.price < 10)]
   ```

   

10. 获取所有书名和价格：

    ```
    $.store.book[*]['title','price']
    ```

