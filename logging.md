# 1. 参考

1. python 3.12 官方：https://docs.python.org/zh-cn/3/library/logging.html

2. 主要基于通义千问

# 2. 快速开始

`logging`模块是Python标准库的一部分，它提供了一种灵活的方式来记录应用程序的运行时信息。

## 2.1 关键概念

1. 通过`logger = logging.getLogger(name)`进行使用
   - 为按模块精细化日志管理，项目中可以包含若干个logger，它们之间存在层级关系。（但通常全局只有一个就满足需求）
   - 多次使用相同的名字调用 [`getLogger()`](https://docs.python.org/zh-cn/3/library/logging.html#logging.getLogger) 会一直返回相同的 Logger 对象的引用。
   
2. 一个logger下可以设置多个handler，用于完成不同的任务处理
   - `FileHandler`用于将日志输出到文件中
   - `StreamHandler`用于将日志打印到终端
3. 每个hanlder可以设置独属于自己的format
   - 通过`Formatter`设置

4. logging是线程安全的

   https://docs.python.org/zh-cn/3/library/logging.html#thread-safety

   

## 2.2 创建步骤

下面是从零开始使用`logging`模块的步骤：

1. **创建一个Logger**

    首先，你需要创建一个`Logger`对象。`Logger`对象是`logging`模块的核心，它负责接收日志消息并决定如何处理这些消息。

    ```python
    import logging
    
    # 创建一个名为'my_logger'的logger对象
    logger = logging.getLogger('my_logger')
    
    # 设置logger的级别，这里设置为DEBUG，意味着所有级别的日志都将被处理
    logger.setLevel(logging.DEBUG)
    ```

2. **添加Handler**

    `Handler`决定了日志消息的去向，例如可以将日志消息输出到控制台、写入文件或者发送邮件等。

    最常用的两种`Handler`是`StreamHandler`（输出到控制台）和`FileHandler`（写入文件）。

    ```python
    # 创建一个StreamHandler，用于输出到控制台
    console_handler = logging.StreamHandler()
    
    # 创建一个FileHandler，用于写入文件
    file_handler = logging.FileHandler('app.log')
    ```

3. **设置日志格式**

    `Formatter`对象用于指定日志消息的格式，包括日期时间、日志级别、logger名字和实际的日志信息等。

    ```python
    # 创建一个Formatter，设置日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 将Formatter添加到Handler中
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    ```

4. **将Handler添加到Logger**

    将创建好的`Handler`添加到`Logger`对象中，这样logger就知道如何处理日志消息了。

    ```python
    # 将Handler添加到logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    ```

5. **记录日志**

    现在，你可以使用`logger`对象记录不同级别的日志消息了。`logging`模块提供了`debug()`, `info()`, `warning()`, `error()`, 和 `critical()`等方法，分别对应不同的日志级别。

    ```python
    # 记录日志
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')
    ```



## 2.3 简单框架

```python
import logging

def setup_logger():
    logger = logging.getLogger(__name__)  # 使用模块名作为logger的名字
    logger.setLevel(logging.DEBUG)  # 设置logger的级别

    # 创建handler和formatter，这里省略具体代码
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    # 将handler添加到logger
    logger.addHandler(handler)

    return logger

# 在模块的初始化部分调用setup_logger
logger = setup_logger()


logger.info("hello world")
```





# 3. 日志内容

## 3.1 基本格式

1. 默认使用`%()s`来表示一个占位符

   ```python
   formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(filename)s:%(funcName)s:%(lineno)d] %(message)s')
   ```

   

2. 可以使用python的str.format形式：`{}`，但需指定style

   ```python
   formatter = logging.Formatter(
       "[{asctime}][{levelname}][{filename}:{funcName}:{lineno}] {message}",
       style="{"
   )
   ```

   - **推荐方式**，可以轻松设置字符串格式

     

   比如，设置levelname占用字段宽度相同

   ```python
       formatter = logging.Formatter(
           "[{asctime}][{levelname:^8s}][{filename}:{funcName}:{lineno}] {message}",
           style="{"
       )
   ```

   其他格式化设置：https://docs.python.org/zh-cn/3/library/string.html?spm=5176.28103460.0.0.76713da2bnsFAC#formatstrings

   

3. 关于Formatter的style

   https://docs.python.org/zh-cn/3/library/logging.html#formatter-objects

   - **style** ([*str*](https://docs.python.org/zh-cn/3/library/stdtypes.html#str)) -- 可以是 `'%'`, `'{'` 或 `'$'` 之一并决定格式字符串将如何与数据合并: 使用 [printf 风格的字符串格式化](https://docs.python.org/zh-cn/3/library/stdtypes.html#old-string-formatting) (`%`), [`str.format()`](https://docs.python.org/zh-cn/3/library/stdtypes.html#str.format) (`{`) 或 [`string.Template`](https://docs.python.org/zh-cn/3/library/string.html#string.Template) (`$`) 之一。 这将只应用于 *fmt* 和 *datefmt* (例如 `'%(message)s'` 或 `'{message}'`)，而不会应用于传给日志记录方法的实际日志消息。 但是，也存在 [其他方式](https://docs.python.org/zh-cn/3/howto/logging-cookbook.html#formatting-styles) 可以为日志消息使用 `{` 和 `$` 格式化。

     

## 3.2 LogRecord 属性

https://docs.python.org/zh-cn/3/library/logging.html#logrecord-attributes

全部可选信息

| 属性名称    | 格式              | 描述                                                         |
| :---------- | :---------------- | :----------------------------------------------------------- |
| 时间        | `%(asctime)s`     | 表示人类易读的 [`LogRecord`](https://docs.python.org/zh-cn/3/library/logging.html#logging.LogRecord) 生成时间。 默认形式为 '2003-07-08 16:49:45,896' （逗号之后的数字为时间的毫秒部分）。 |
| logger名称  | `%(name)s`        | 用于记录调用的日志记录器名称。                               |
| 文件名      | `%(filename)s`    | `pathname` 的文件名部分，比如`main.py`                       |
| 模块名      | `%(module)s`      | 模块 (`filename` 的名称部分)，比如`main`                     |
| 函数名      | `%(funcName)s`    | 函数名包括调用日志记录.                                      |
| 代码行号    | `%(lineno)d`      | 发出日志记录调用所在的源行号（如果可用）。                   |
| level名     | `%(levelname)s`   | 消息文本记录级别（`'DEBUG'`，`'INFO'`，`'WARNING'`，`'ERROR'`，`'CRITICAL'`）。 |
| message     | `%(message)s`     | 记入日志的消息，即 `msg % args` 的结果。 这是在发起调用 [`Formatter.format()`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Formatter.format) 时设置的。 |
| process     | `%(process)d`     | 进程ID（如果可用）                                           |
| processName | `%(processName)s` | 进程名（如果可用）                                           |
| thread      | `%(thread)d`      | 线程ID（如果可用）                                           |
| threadName  | `%(threadName)s`  | 线程名（如果可用）                                           |
| taskName    | `%(taskName)s`    | [`asyncio.Task`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.Task) 名称（如果可用）。 |



# 4. 日志等级和颜色设置

## 4.1 等级和分工

1. **DEBUG**: 

   - 蓝色
   - 最详细的日志信息，通常用于开发阶段；在生产环境中，通常会关闭DEBUG级别的日志
   - **去打印那些在INFO级别不打印的信息**

2. **INFO**: 

   - 绿色
   - 用于记录一般运行时信息

3. **WARNING**: 

   - 黄色
   - 当检测到可能存在问题的情况，但**还不至于导致应用程序失败时**

4. **ERROR**: 

   - 红色
   - 当应用程序遇到错误，导致某个功能无法正常执行时

5. **CRITICAL**: 

   - 白底红字 或 紫色

   - 导致整个应用程序或系统崩溃时（raise Error）

     

## 4.2 颜色设置

1. 使用colorlog代替logging.Formatter

   ```
   pip install colorlog
   ```

   

2. 设置颜色

   在之前添加`log_color`字段

   ```python
   import logging
   from colorlog import ColoredFormatter
   
   def setup_logger():
       logger = logging.getLogger('my_logger')
       logger.setLevel(logging.DEBUG)
   
       # 创建一个彩色Formatter
       formatter = ColoredFormatter(
           "{log_color}[{asctime}][{levelname}][{filename}:{funcName}:{lineno}] {message}",
           style="{",
           log_colors={
               'DEBUG': 'blue',
               'INFO': 'green',
               'WARNING': 'yellow',
               'ERROR': 'red',
               'CRITICAL': 'red,bg_white',
           }
       )
   
       # 创建一个StreamHandler
       stream_handler = logging.StreamHandler()
       stream_handler.setFormatter(formatter)
   
       # 将handler添加到logger
       logger.addHandler(stream_handler)
   
       return logger
   
   # 在模块的初始化部分调用setup_logger
   logger = setup_logger()
   
   def main():
       logger.info("hello world")
       logger.debug("hello world")
       logger.warning("hello world")
       logger.error("hello world")
       logger.critical("hello world")
       
       
   if __name__ == "__main__":
       main()
   ```
   
   

# 5. 日志保存和文件轮换

## 5.1 日志保存

1. 设置`logging.FileHandler()`

2. 代码

   ```python
   import logging
   from colorlog import ColoredFormatter
   
   def setup_logger():
       logger = logging.getLogger('my_logger')
       logger.setLevel(logging.DEBUG)
   
       # 创建一个彩色Formatter
       formatter = logging.Formatter(
           "[{asctime}][{levelname:^8s}][{filename}:{funcName}:{lineno}] {message}",
           style="{"
       )
   
       # 创建一个FileHandler
       file_handler = logging.FileHandler('a.log')
       file_handler.setFormatter(formatter)
   
       # 将handler添加到logger
       logger.addHandler(file_handler)
   
       return logger
   
   # 在模块的初始化部分调用setup_logger
   logger = setup_logger()
   
   def main():
       logger.info("hello world")
       logger.debug("hello world")
       logger.warning("hello world")
       logger.error("hello world")
       logger.critical("hello world")
       
       
   if __name__ == "__main__":
       main()
   ```
   
   

## 5.2 日志文件轮换

### 5.2.1 用途

1. 在长时间运行的应用中，日志文件会很大，不利于后期维护（比如服务器需要连续运行一个月）
   - 此时可以使用日志文件轮换：按指定时间点创建新的日志文件，后续日志就会保存在新文件中。

2. 当新的日志文件被创建时，旧的文件会被重命名，通常在文件名后面加上时间戳。

   例如，如果基本文件名是`my_app.log`，则旧的文件可能会被重命名为`my_app.log.2023-07-13`

### 5.2.2 实现

1. 使用`TimedRotatingFileHandler`

   **注意**：该方案在极高并发情况下是否安全有待探究。（当文件切换瞬间来了条日志）

   https://docs.python.org/zh-cn/3/library/logging.handlers.html#timedrotatingfilehandler

2. 代码
    ```python
    import logging
    from logging.handlers import TimedRotatingFileHandler
    
    # 创建一个logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    # 创建一个TimedRotatingFileHandler实例
    handler = TimedRotatingFileHandler(
        filename='my_app.log',  # 日志文件名
        when='midnight',  # 以每天午夜作为日志滚动的时间点
        interval=1,  # 默认为1，每隔1个时间单位（这里是天）滚动一次
        backupCount=0  # 如果不为0，为n，则保留最近n天的日志文件
    )
    
    # 设置日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    # 将handler添加到logger
    logger.addHandler(handler)
    
    # 使用logger记录日志
    logger.debug('This is a debug message.')
    logger.info('This is an info message.')
    logger.warning('This is a warning message.')
    logger.error('This is an error message.')
    logger.critical('This is a critical message.')
    ```
    
    `when`的6种选项
    
    | 值           | 间隔类型                                                    |
    | :----------- | :---------------------------------------------------------- |
    | `'S'`        | 秒                                                          |
    | `'M'`        | 分钟                                                        |
    | `'H'`        | 小时                                                        |
    | `'D'`        | 天                                                          |
    | `'W0'-'W6'`  | 工作日(0=星期一)                                            |
    | `'midnight'` | 如果未指定 *atTime* 则在午夜执行轮换，否则将使用 *atTime*。 |
    
    当使用基于星期的轮换时，星期一为 'W0'，星期二为 'W1'，以此类推直至星期日为 'W6'。 

3. **仅当提交日志时才有可能触发轮换**
   - 如果在应用程序执行期间，日志记录输出的生成频率高于每分钟一次，*那么* 你可以预期看到间隔一分钟时间的日志文件。
   - 如果（假设）日志记录消息每五分钟才输出一次，那么文件时间将会存在对应于没有输出（因而没有轮换）的缺失。



# 6. 单Logger下的代码框架

足够支持小型项目的日常使用

**注意使用时将when改回“midnight”**

```python
import logging, time
from logging.handlers import TimedRotatingFileHandler
from colorlog import ColoredFormatter

class Logger:
    
    def __init__(self, level, file_path) -> None:
        self.file_path = file_path
        self.logger = logging.getLogger()
        
        self.logger.setLevel(level)
        
        self.init_stream_handler()
        self.init_file_handler()
        
        self.logger.addHandler(self.stream_handler)
        self.logger.addHandler(self.file_handler)        

    
    
    def init_stream_handler(self):
        
        self.stream_handler = logging.StreamHandler()
        
        formatter = ColoredFormatter(
            "{log_color}[{asctime}][{levelname:^8s}][{filename}:{funcName}:{lineno}] {message}",
            style="{",
            log_colors={
                'DEBUG': 'blue',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        
        self.stream_handler.setFormatter(formatter)
    
    def init_file_handler(self):
        
        self.file_handler = TimedRotatingFileHandler(
            filename=self.file_path,
            # when="midnight"
            when="S"
        )
        
        formatter = logging.Formatter(
            "[{asctime}][{levelname:^8s}][{filename}:{funcName}:{lineno}] {message}",
            style="{"
        )
        
        self.file_handler.setFormatter(formatter)
        
        
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)
        
    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)
        
    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)
        
    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)
        
    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)
    
    
        
logger = Logger(level=logging.DEBUG, file_path="a.log")

if __name__ == "__main__":
    
    for i in range(10):
        logger.debug('This is a debug message.')
        logger.info('This is an info message.')
        logger.warning('This is a warning message.')
        logger.error('This is an error message.')
        logger.critical('This is a critical message.')
        
        time.sleep(1)
```



# 7. Filter

## 7.1 概念

1. 当日志需要过滤或者修改内容时
2. 继承自logging.Filter，编写类（比如`SpecialFilter`），并添加到logger（或者handler）
   - 注意，`SpecialFilter`中的`filter`规则不能覆盖`logger.setLevel(logging.DEBUG)`
3. `SpecialFilter`中的`filter`中
   - 返回True，此条log会被传入handler
   - 返回False，此条log不会被传入handler
4. `filter`中可利用record（[LogRecord对象](https://docs.python.org/zh-cn/3/library/logging.html#logrecord-objects)）进行复杂逻辑编写

## 7.2 实现

```python
import logging

class SpecialFilter(logging.Filter):
    def __init__(self, key):
        super().__init__()
        self.key = key

    def filter(self, record):
        message = record.getMessage()
        if self.key in message:
            record.levelname = "正常"
            return True
        else:
            return False

# 创建根 Logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

# 创建处理器
root_handler = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
root_handler.setFormatter(formatter)
root_logger.addHandler(root_handler)

# 创建过滤器并添加到处理器
special_filter = SpecialFilter("key")
root_logger.addFilter(special_filter)

# 输出日志
root_logger.debug('key')
root_logger.debug('hello')
```







# 8. 多logger

多个logger是为了对各个模块精准调整日志的需要，但通常用不到

## 8.1 层级

详细信息可查看：https://docs.python.org/zh-cn/3/library/logging.html#logger-objects

1. 每个`Logger`实例都有一个名字，这个名字定义了它在层次结构中的位置

   ```python
   root = logging.getLogger()					# 最高层的logger
   parent = logging.getLogger('parent')		# 父logger
   child = logging.getLogger('parent.child')	# 子logger
   ```

   打印logger名字
   
   ```python
   print(root.name)
   print(parent.name)
   print(child.name)
   ```
   
   ```
   root
   parent
   parent.child
   ```
   
   打印logger的父logger
   
   ```python
   print(root.parent)
   print(parent.parent)
   print(child.parent)
   ```
   
   ```
   None
   <RootLogger root (WARNING)>
   <Logger parent (WARNING)>
   ```
   
   

2. logger日志级别

   - 如果子日志器没有设置自己的日志级别，它将继承父日志器的日志级别。

   - 如果子日志器设置了日志级别，那么它将优先使用自己设置的日志级别。

     

3. logger的`propagate`

   当子logger的`propagate`参数设为`True`（默认）

   - 它产生的日志记录将被传递给它的父日志器

   为False时则不上传日志



4. **子logger不会继承父logger的handler**

   当子logger没定义handler，而`propagate = True`时，日志会传到父logger中打印

   

## 8.2 代码

```python
import logging

# 创建根记录器并设置其日志级别和处理器
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

# 添加一个处理器到根记录器
handler = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root_logger.addHandler(handler)


# =============================================

# 创建一个名为 'myapp' 的子记录器
logger_myapp = logging.getLogger('myapp')
logger_myapp.setLevel(logging.DEBUG)

# 添加一个处理器到子记录器
# handler = logging.StreamHandler()
# formatter = logging.Formatter('%(message)s')
# handler.setFormatter(formatter)
# logger_myapp.addHandler(handler)

logger_myapp.propagate = False


# 发送日志消息
logger_myapp.debug('Debug message from submodule.')
```

可以尝试以下情况

- `logger_myapp.propagate = False` 且 未定义 handler
- `logger_myapp.propagate = True` 且 未定义 handler
- `logger_myapp.propagate = False` 且 定义 handler
- `logger_myapp.propagate = True` 且 定义 handler









