# HTTP

结合deepseek和qwen的回答



# 1. 从字符串开始

## 1.1 基础概念

（宁愿直接用英文原词，不用易造成误解的中文翻译）

1. **Bit** （比特，Binary Digit 的缩写）

   - **定义**: 比特是计算机中最小的数据单位，表示二进制的一个位。

   - **取值**: 比特只能取两个值：`0` 或 `1`。

2. **Byte**（字节）

   - **定义**: 字节是计算机存储和传输数据的基本单位。
   - **大小**: 1 个字节通常由 8 个比特（bit） 组成。1 字节 = 8 比特
   - **范围**: 1 个字节可以表示 2^8 = 256 种不同的值，范围是 `0` 到 `255`。

3. **Word** (字)

   - **定义**: 字是计算机中一次处理的数据单位，其大小取决于计算机的架构。
   - **大小**: 字的大小通常与 CPU 的位数相关：
     - 在 32 位系统中，1 个字 = 4 字节 = 32 比特。
     - 在 64 位系统中，1 个字 = 8 字节 = 64 比特。
   - **用途**: **字是 CPU 处理数据的基本单位**，比如寄存器的大小通常是一个字。

4. **Character** （字符）

   - **定义**: 字符是文本的基本单位，表示一个符号或字母。例如：

     - 英文字符：`A`, `B`, `C`
     - 中文字符：`中`, `文`
     - 符号：`!`, `@`, `#`
     - 表情符号：`😊`, `🚀`

   - **编码**: 字符在计算机中通过编码方式（如 ASCII、Unicode）存储为二进制数据。

     - 例如，字符 `A` 的 ASCII 编码是 `65`（二进制 `01000001`）。
     - 字符 `中` 的 Unicode 编码是 `U+4E2D`，UTF-8 编码是 `E4 B8 AD`（3 个字节）。

   - **存储**:  **一个字符可能占用多个字节，具体取决于编码方式**

     

## 1.2 Unicode与编码

- **Unicode** 是一个字符集，定义了世界上几乎所有字符的唯一编号（称为“码点”）。
- **UTF-8** 是一种编码方式，用于将 Unicode 字符的码点转换为计算机可以存储和传输的字节序列。



### 1.2.1 Unicode**（统一码）**

1. **定义**: Unicode 是一个国际标准，旨在为世界上所有的字符（包括字母、符号、表情符号等）分配一个**唯一的编号**（称为“码点”）。
2. **码点**: 每个字符在 Unicode 中都有一个唯一的码点，通常用 `U+` 开头表示，**采用十六进制**。例如：

     - 字符 `A` 的码点是 `U+0041`。
     - 汉字 `中` 的码点是 `U+4E2D`。
     - 表情符号 `😊` 的码点是 `U+1F60A`。
3. **范围**: Unicode 的码点范围是 `U+0000` 到 `U+10FFFF`，可以表示超过 100 万个字符。



### 1.2.2 UTF-8

**Unicode Transformation Format - 8-bit**

1. **定义**: UTF-8 是 Unicode 的**一种实现方式**，是一种可变长度的编码方式。

   - **它将 Unicode 码点转换为字节序列**，以便计算机可以存储和传输。

2. **可变长度**: UTF-8 使用 1 到 4 个字节来表示一个 Unicode 字符。

     - 英文字符（ASCII 字符）用 1 个字节表示。

     - 大多数常用字符（如中文、日文、韩文等）用 2 到 3 个字节表示。

     - 特殊字符（如表情符号）用 4 个字节表示。


3. **兼容 ASCII**: UTF-8 完全兼容 ASCII 编码，ASCII 字符的 UTF-8 编码与 ASCII 编码相同。



### 1.2.3 例子: `A中😊`

1. 编码

   - 字符 `A` 的 Unicode 码点是 `U+0041`，UTF-8 编码是 `41`（1 个字节）。
   - 汉字 `中` 的 Unicode 码点是 `U+4E2D`，UTF-8 编码是 `E4 B8 AD`（3 个字节）。
   - 表情符号 `😊` 的 Unicode 码点是 `U+1F60A`，UTF-8 编码是 `F0 9F 98 8A`（4 个字节）。

2. Python中

   - `str` 类型使用 Unicode 编码存储字符。
   - `bytes` 类型用于存储 UTF-8 编码的字节序列。

   ```python
   # Unicode 字符串
   s = "A中😊"
   print(s)  # A中😊
   
   # 将 Unicode 字符串编码为 UTF-8 字节序列
   b = s.encode('utf-8')
   print(b)  # b'A\xe4\xb8\xad\xf0\x9f\x98\x8a'
   
   # 将 UTF-8 字节序列解码为 Unicode 字符串
   s2 = b.decode('utf-8')
   print(s2)  # A中😊
   ```



### 1.2.4 UTF-8的字节前缀

对于UTF-8的可变长度编码，`b'\x41\xe4\xb8\xad\xf0\x9f\x98\x8a'`，怎么区分前几个字节表示一个字符？

1. UTF-8 使用 1 到 4 个字节表示一个字符，具体规则如下：

    | 字符范围（Unicode 码点） | UTF-8 编码格式                        | 字节数 |
    | :----------------------- | :------------------------------------ | :----- |
    | `U+0000` 到 `U+007F`     | `0xxxxxxx`                            | 1 字节 |
    | `U+0080` 到 `U+07FF`     | `110xxxxx 10xxxxxx`                   | 2 字节 |
    | `U+0800` 到 `U+FFFF`     | `1110xxxx 10xxxxxx 10xxxxxx`          | 3 字节 |
    | `U+10000` 到 `U+10FFFF`  | `11110xxx 10xxxxxx 10xxxxxx 10xxxxxx` | 4 字节 |

    **前缀规则**:

    - 单字节字符以 `0` 开头。

    - 多字节字符的第一个字节以 `110`、`1110` 或 `11110` 开头，表示字符占用的字节数。

    - 后续字节以 `10` 开头，表示它们是当前字符的一部分。

      

2. 通过检查每个字节的前缀，可以确定它属于哪个字符：

    - 如果字节以 `0` 开头，它是一个单字节字符。

    - 如果字节以 `110` 开头，它是一个双字节字符的第一个字节。

    - 如果字节以 `1110` 开头，它是一个三字节字符的第一个字节。

    - 如果字节以 `11110` 开头，它是一个四字节字符的第一个字节。

    - 如果字节以 `10` 开头，它是当前字符的后续字节。

      


### 1.2.5 其他编码方式

Unicode 有多种编码方式，常见的有：

1. **UTF-8**:

     - 可变长度编码，使用 1 到 4 个字节表示一个字符。

     - 兼容 ASCII，英文字符用 1 个字节，中文字符用 2~3 个字节。


2. **UTF-16**:

     - 可变长度编码，使用 2 或 4 个字节表示一个字符。

     - 大多数常用字符用 2 个字节，特殊字符用 4 个字节。


3. **UTF-32**:

     - 固定长度编码，使用 4 个字节表示一个字符。

       

**示例**

1. 字符 `A`

   - Unicode 码点：`U+0041`（十六进制）

   - UTF-8 编码：`41`（1 字节）

   - UTF-16 编码：`0041`（2 字节）

   - UTF-32 编码：`00000041`（4 字节）


2. 汉字 `中`

   - Unicode 码点：`U+4E2D`（十六进制）

   - UTF-8 编码：`E4 B8 AD`（3 字节）

   - UTF-16 编码：`4E2D`（2 字节）

   - UTF-32 编码：`00004E2D`（4 字节）


3. 表情符号 `😊`

   - Unicode 码点：`U+1F60A`（十六进制）

   - UTF-8 编码：`F0 9F 98 8A`（4 字节）

   - UTF-16 编码：`D83D DE0A`（4 字节，使用代理对）

   - UTF-32 编码：`0001F60A`（4 字节）



## 1.3 HTTP中的编码

HTTP报文在传输时的编码方式

1. 在Header中，通常使用ASCII编码

   - ASCII编码可看做UTF-8的子集

   若包含非ASCII字符，使用 **MIME 编码**（如 `RFC 2047`）将其转换为 ASCII 格式，而转换的基础通常是 **UTF-8 编码**。

   

2. MIME编码

   - 非ASCII字符 --> UTF-8编码 --> 将UTF-8编码进行二次编码，转换成使用多个ASCII字符表示的字符串（Base64 或 Quoted-Printable 编码）

   - 将二次编码后的字符串封装在 `=?charset?编码方式?编码后的字符串?=` 格式中

   例如：

   - 原始字符串：`你好`

   - UTF-8 编码：`E4 BD A0 E5 A5 BD`

   - Base64 编码：`5Lit5paH`

   - 最终结果：`Subject: =?UTF-8?B?5Lit5paH?=`

     

3. 在Body中，编码方式有Header中的`Content-Type`指定
   - `Content-Type: text/html; charset=utf-8` 表示报文体是 UTF-8 编码的 HTML 文本。
   - `Content-Type: application/json; charset=utf-8` 表示报文体是 UTF-8 编码的 JSON 数据。
   - `Content-Type: image/png` 表示是二进制数据（如图片），不需要字符编码。



# 2. HTTP报文组成

## 2.1 请求报文

HTTP 请求报文由以下三部分组成：

```
请求行（Request Line）
请求头（Request Headers）

请求体（Request Body）
```

注意：

- 请求头和请求体中有一行空行

- HTTP中的使用`\r\n`来区分三块内容

  因此，上述报文实际上是

  ```
  请求行\r\n请求头\r\n\r\n请求体
  ```

  （若请求头中需换行，也是用`\r\n`）

  

### 2.1.1 请求行

请求行包含三个部分：

- **请求方法（Method）**: 表示客户端希望服务器执行的操作。
  - 常见方法：`GET`、`POST`、`PUT`、`DELETE`等。
- **请求目标（Request Target）**: 表示请求的资源路径。
  - 例如：`/index.html`。
- **HTTP 版本（HTTP Version）**: 表示使用的 HTTP 协议版本。
  - 例如：`HTTP/1.1`。

格式：

```
<Method> <Request Target> <HTTP Version>
```

示例：

```
GET /index.html HTTP/1.1
```



### 2.1.2 请求头

请求头包含客户端发送给服务器的附加信息，每个头字段由 `字段名: 字段值` 组成。

常见请求头字段：

- `Host`: 请求的目标主机名和端口号。
  - 示例：`Host: www.example.com` （通常使用域名）
- `User-Agent`: 客户端的浏览器或应用程序信息。
  - 示例：`User-Agent: Mozilla/5.0`
- `Accept`: 客户端能够接收的响应内容类型。
  - 示例：`Accept: text/html,application/xhtml+xml`
- `Content-Type`: 请求体的媒体类型（仅适用于 POST 或 PUT 请求）。
  - 示例：`Content-Type: application/json`
- `Content-Length`: 请求体的长度（字节数）。
  - 示例：`Content-Length: 123`

**示例**：

```
Host: www.example.com
User-Agent: Mozilla/5.0
Accept: text/html,application/xhtml+xml
```



### 2.1.3 请求体

请求体包含客户端发送给服务器的数据，通常用于 `POST` 或 `PUT` 请求。

**常见格式**：

- 表单数据：`application/x-www-form-urlencoded`
- JSON 数据：`application/json`
- 文件上传：`multipart/form-data`

**示例**：

```
username=admin&password=123456
```



### 2.1.4 示例

```
POST /api/data HTTP/1.1
Host: example.com
Content-Type: application/json
Content-Length: 32

{"key": "value", "name": "test"}
```

换行替换成`\r\n`

```
POST /api/data HTTP/1.1\r\nHost: example.com\r\nContent-Type: application/json\r\nContent-Length: 32\r\n\r\n{"key": "value", "name": "test"}
```





## 2.2 响应报文

HTTP 响应报文由以下三部分组成：

1. **状态行（Status Line）**

2. **响应头（Response Headers）**

3. **响应体（Response Body）**

   

### 2.2.1 状态行

状态行包含三个部分：

- **HTTP 版本（HTTP Version）**: 表示使用的 HTTP 协议版本。
  - 例如：`HTTP/1.1`。
- **状态码（Status Code）**: 表示服务器对请求的处理结果。
  - 常见状态码：`200`（成功）、`404`（未找到）、`500`（服务器内部错误）。
- **状态文本（Status Text）**: 对状态码的简短描述。
  - 例如：`OK`、`Not Found`。

**格式**：

```
<HTTP Version> <Status Code> <Status Text>
```

**示例**：

```
HTTP/1.1 200 OK
```



### 2.2.2 响应头

响应头包含服务器返回给客户端的附加信息，每个头字段由 `字段名: 字段值` 组成。

**常见响应头字段**：

- `Content-Type`: 响应体的媒体类型。
  - 示例：`Content-Type: text/html; charset=utf-8`
- `Content-Length`: 响应体的长度（字节数）。
  - 示例：`Content-Length: 123`
- `Server`: 服务器的软件信息。
  - 示例：`Server: Apache/2.4.1`
- `Set-Cookie`: 设置客户端的 Cookie。
  - 示例：`Set-Cookie: sessionid=12345; Path=/`

**示例**：

```
Content-Type: text/html; charset=utf-8
Content-Length: 123
Server: Apache/2.4.1
```



### 2.2.3 响应体

响应体包含服务器返回给客户端的数据，通常是 HTML 页面、JSON 数据、图片等。

**示例**：

```
<!DOCTYPE html>
<html>
<head>
    <title>示例页面</title>
</head>
<body>
    <p>你好，世界！</p>
</body>
</html>
```



### 2.2.4 示例

```
HTTP/1.1 200 OK
date: Thu, 06 Mar 2025 09:26:47 GMT
server: uvicorn
content-length: 25
content-type: application/json

{"message":"Hello World"}
```

实际上也是使用`\r\n`表示换行





## 2.3 MIME类型

报文header中，`Content-Type`（或`Accept`）的取值，指定了body的数据类型

包含多种类型

- `application/json`：JSON数据
- `application/octet-stream`：二进制数据
- `text/plain`：纯文本
- `image/jpeg`：JPEG图片
- `audio/mpeg`：MP3音频
- `video/mp4`：MP4视频
- `multipart/form-data`：表单数据分成多个部分
- ......

其中重点关注`application/json`和`application/octet-stream`

- POST请求通常使用`application/json`，即body是一个json
- 在上传文件时，可使用`application/octet-stream`。因为是表示二进制数据，可接受任意文件类型数据。在不考虑网络安全的情况下，具体文件类型可根据上传的文件后缀名来确定。











# 3. Socket搭建

(针对POST请求, DeepSeek生成)

Socket 提供了对 TCP 和 UDP 的直接操作，但需要开发者手动实现网络通信的各个步骤。以此可以来学习HTTP的请求和响应报文组成。

## 3.1 HTTP服务器

```python
import socket
import json

def handle_request(request):
    """
    处理HTTP请求，解析请求行、请求头和请求体，并生成相应的HTTP响应。
    
    :param request: 接收到的HTTP请求字符串
    :return: 生成的HTTP响应字符串
    """
    # 将请求按行分割
    request_lines = request.split('\r\n')
    # 第一行是请求行，包含方法、路径和协议版本
    request_line = request_lines[0]
    # 解析请求行，提取方法、路径和协议版本
    method, path, _ = request_line.split(' ')

    # 如果是POST请求，解析请求体
    if method == 'POST':
        # 请求体的内容是请求的最后一行
        body = request_lines[-1]
        try:
            # 尝试将请求体解析为JSON
            data = json.loads(body)
            # 构建成功的响应数据
            response_data = {"status": "success", "received": data}
        except json.JSONDecodeError:
            # 如果JSON解析失败，返回错误信息
            response_data = {"status": "error", "message": "Invalid JSON"}
    else:
        # 如果不是POST请求，返回错误信息
        response_data = {"status": "error", "message": "Only POST requests are supported"}

    # 将响应数据转换为JSON格式的字符串
    response_body = json.dumps(response_data)
    # 构建HTTP响应头
    response_headers = [
        "HTTP/1.1 200 OK",  # 状态行
        "Content-Type: application/json",  # 响应内容类型
        f"Content-Length: {len(response_body)}",  # 响应体长度
        "Connection: close",  # 关闭连接
    ]
    # 将响应头和响应体组合成完整的HTTP响应
    response = "\r\n".join(response_headers) + "\r\n\r\n" + response_body
    return response

def start_server(host='127.0.0.1', port=8080):
    """
    启动一个简单的HTTP服务器，监听指定主机和端口，处理客户端请求。
    
    :param host: 服务器绑定的主机地址，默认为127.0.0.1
    :param port: 服务器绑定的端口号，默认为8080
    """
    # 创建一个TCP/IP Socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定Socket到指定主机和端口
    server_socket.bind((host, port))
    # 开始监听，允许最多5个客户端连接
    server_socket.listen(5)
    print(f"Listening on {host}:{port}...")

    while True:
        # 等待客户端连接
        # client_socket是新的Socket对象，用于与客户端通信
        # client_address是客户端的地址，是一个(host, port)的元组。例如('127.0.0.1', 39874)
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        # 接收客户端发送的请求数据，最大1024字节
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Received request:\n{request}")

        # 处理请求并生成响应
        response = handle_request(request)
        # 将响应发送回客户端
        client_socket.sendall(response.encode('utf-8'))
        # 关闭客户端连接
        client_socket.close()

if __name__ == "__main__":
    # 启动服务器
    start_server(port=8081)
```



## 3.2 HTTP客户端

```python
import socket
import json

def send_post_request(host='127.0.0.1', port=8081, path='/', data=None):
    """
    向指定的HTTP服务器发送POST请求，并接收响应。

    :param host: 服务器的主机地址，默认为127.0.0.1
    :param port: 服务器的端口号，默认为8081
    :param path: 请求的路径，默认为'/'
    :param data: 要发送的JSON数据，默认为None
    :return: 服务器的响应内容
    """
    # 创建一个TCP/IP Socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # 连接到服务器
        client_socket.connect((host, port))
        
        # 构建HTTP请求
        if data is not None:
            # 将数据转换为JSON格式
            json_data = json.dumps(data)
            # 构建请求头和请求体
            request = f"POST {path} HTTP/1.1\r\n"
            request += f"Host: {host}:{port}\r\n"
            request += "Content-Type: application/json\r\n"
            request += f"Content-Length: {len(json_data)}\r\n"
            request += "Connection: close\r\n"
            request += "\r\n"
            request += json_data
        else:
            # 如果没有数据，发送一个空的POST请求
            request = f"POST {path} HTTP/1.1\r\n"
            request += f"Host: {host}:{port}\r\n"
            request += "Content-Length: 0\r\n"
            request += "Connection: close\r\n"
            request += "\r\n"
        
        # 发送请求
        client_socket.sendall(request.encode('utf-8'))
        
        # 接收响应
        response = client_socket.recv(4096).decode('utf-8')
        
        # 返回响应内容
        return response
    
    finally:
        # 关闭Socket连接
        client_socket.close()

if __name__ == "__main__":
    # 要发送的JSON数据
    data = {"key": "value", "another_key": "another_value"}
    
    # 发送POST请求并打印响应
    response = send_post_request(port=8081, data=data)
    print("Response from server:")
    print(response)
```





## 3.3 运行效果

1. 请求报文

   ```
   POST / HTTP/1.1
   Host: 127.0.0.1:8081
   Content-Type: application/json
   Content-Length: 48
   Connection: close
   
   {"key": "value", "another_key": "another_value"}
   ```

   

2. 响应报文

   ```
   HTTP/1.1 200 OK
   Content-Type: application/json
   Content-Length: 83
   Connection: close
   
   {"status": "success", "received": {"key": "value", "another_key": "another_value"}}
   ```



3. 也可以使用curl发送请求报文

   ```bash
   curl -v -X POST http://127.0.0.1:8081/ \
        -H "Content-Type: application/json" \
        -H "Connection: close" \
        -d '{"key": "value", "another_key": "another_value"}'
   ```

   `-v` 表示打印请求报文和响应报文

   `-i` 表示打印响应报文



# 4. FastAPI和Requests

## 4.1 基于FastAPI的服务端

```python
import uvicorn
from fastapi import FastAPI, requests

app = FastAPI()

@app.post("/hello")
def hello(request: requests.Request, data: dict):
    headers = request.headers
    return {"message": "Hello World"}
    
uvicorn.run(app, host="127.0.0.1", port=8081)
```

通常`data`使用`pydantic.BaseModel`详细定义数据结构



## 4.2 基于Requests的客户端

```python
import requests

url = "http://127.0.0.1:8081/hello"
data = {"key": "value", "name": "test"}
response = requests.post(url, json=data)

# 检查状态码
if response.status_code == 200:
    print('请求成功')
else:
    print(f'请求失败，状态码: {response.status_code}')

# 输出响应内容
print(response.text)

# 输出响应头
print(response.headers)

# 输出 cookies
print(response.cookies)

# 输出最终的 URL
print(response.url)

# 输出重定向历史
print(response.history)

# 解析 JSON 数据（如果响应是 JSON 格式）
try:
    data = response.json()
    print(data)
except ValueError:
    print('响应内容不是 JSON 格式')

```



# 5. 文件上传下载

假设操作的文件对象为

```
# text.txt
Hello, World!
```



## 5.1 服务端

```python
import uvicorn
import shutil
from fastapi import FastAPI, requests, UploadFile
from fastapi.responses import FileResponse

app = FastAPI()

@app.post("/hello")
def hello(request: requests.Request, data: dict):
    headers = request.headers
    return {"message": "Hello World"}


@app.post("/upload")
def upload(file: UploadFile):
    file_name = "receive_" + file.filename
    
    # 'wb'针对二进制文件，application/octet-stream
    with open(file_name, "wb") as buffer:
        # 采用内存更高效的写法
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}


@app.get("/download")
def download():
    print( "download" )
    return FileResponse(path="receive_text.txt", 
                        filename="receive_text.txt", 
                        media_type="application/octet-stream")
    
uvicorn.run(app, host="127.0.0.1", port=8081)
```



## 5.2 上传

1. 使用`requests`库

   ```python
   file_name = "text.txt"
   with open(file_name, "rb") as file:
       # file是一个元组，(文件名，文件对象，文件类型)
       files = {'file': (file_name, file, "application/octet-stream")}
       response = requests.post(url + "upload", files=files)
       print(response.json())
   ```

   可以使用curl查看相对完整的报文

   ```bash
   curl --trace-ascii - -F "file=@text.txt;type=application/octet-stream" 127.0.0.1:8081/upload

2. 完整报文

   ```
   POST /upload HTTP/1.1
   Host: 127.0.0.1:8081
   Content-Length: 214
   Content-Type: multipart/form-data; boundary=------------------------OudarFyTcP4CeZ32tPyHAf
   
   --------------------------OudarFyTcP4CeZ32tPyHAf
   Content-Disposition: form-data; name="file"; filename="example.txt"
   Content-Type: text/plain
   
   Hello, World!
   --------------------------OudarFyTcP4CeZ32tPyHAf--
   
   ```

   实际发送为（可使用 `3.2 HTTP客户端`验证）

   ```
   POST /upload HTTP/1.1\r\nHost: 127.0.0.1:8081\r\nContent-Length: 214\r\nContent-Type: multipart/form-data; boundary=------------------------OudarFyTcP4CeZ32tPyHAf\r\n\r\n--------------------------OudarFyTcP4CeZ32tPyHAf\r\nContent-Disposition: form-data; name="file"; filename="example.txt"\r\nContent-Type: text/plain\r\n\r\nHello, World!\r\n--------------------------OudarFyTcP4CeZ32tPyHAf--\r\n
   ```

   请求体长度214为

   ```python
   len("""--------------------------OudarFyTcP4CeZ32tPyHAf\r\nContent-Disposition: form-data; name="file"; filename="example.txt"\r\nContent-Type: text/plain\r\n\r\nHello, World!\r\n--------------------------OudarFyTcP4CeZ32tPyHAf--\r\n""")
   ```



## 5.3 下载

1. 使用requests库

   ```python
   response = requests.get(url + "download")
   with open("downloaded_text.txt", "wb") as file:
       file.write(response.content)
   ```

   也可以使用

   ```
   curl -o downloaded_text.txt "127.0.0.1:8081"
   ```

2. 完整响应报文

   ```
   HTTP/1.1 200 OK
   content-type: application/octet-stream
   content-disposition: attachment; filename="receive_text.txt"
   content-length: 11
   
   Hello World
   ```

   实际使用`\r\n`代替换行

   ```
   HTTP/1.1 200 OK\r\ncontent-type: application/octet-stream\r\ncontent-disposition: attachment; filename="receive_text.txt"\r\ncontent-length: 11\r\n\r\nHello World
   ```

   



# 6. multipart多部分

```
POST /upload HTTP/1.1
Host: 127.0.0.1:8081
Content-Length: 348
Content-Type: multipart/form-data; boundary=THIS_IS_BOUNDARy

--THIS_IS_BOUNDARy
Content-Disposition: form-data; name="file"; filename="example.txt"
Content-Type: text/plain

Hello, World!
--THIS_IS_BOUNDARy
Content-Disposition: form-data; name="data"

{"username": "john_doe", "age": 30}
--THIS_IS_BOUNDARy--

```



1. `multipart/form-data` 将表单数据分成多个部分（parts），

   - 每个部分之间使用一个唯一的边界字符串（boundary）进行分隔。

   - 每个部分都有自己的头部信息，用于描述该部分的内容类型、编码方式等。

   - 每个部分可以包含文本字段或文件数据。

     

2. Boundary的规则：

   - 在实际使用时必须以`--`开头
   - 最后一个以`--`结尾

   比如：`THIS_IS_BOUNDARy`，

   实际使用中，通常是一个随机字符串`------------------------OudarFyTcP4CeZ32tPyHAf`

   

3. 特点

   - 支持混合传输数据：每个部分的数据类型不一样

   - 支持多文件上传：每个部分都是一个文件

     

4. 在上传文件时，通常headers中的`Content-Type: multipart/form-data` 

   - 其中的每个部分的`Content-Type: application/octet-stream` 

   

5. 在每个部分中

   ```
   --THIS_IS_BOUNDARy
   Content-Disposition: form-data; name="file"; filename="example.txt"
   Content-Type: text/plain
   
   Hello, World!
   ```

   - `Content-Disposition: form-data`是固定写法

   - `name`表示当前部分的名字，必须

     - 对FastAPI而言，**定义的接口中变量名要和每个部分的`name`保持一致**

       ```python
       def upload(file: UploadFile=File(...), data: str=Form(...))
       ```

   - `filename` 等附加字段是对这部分的描述
     - 不是全部的附加信息，FastAPI都能识别到

   

## 6.1 混合数据上传

1. server

   ```python
   @app.post("/upload")
   def upload(file: UploadFile=File(...), data: str=Form(...)):
       
       file_name = "receive_" + file.filename
       print(data)
       with open(file_name, "wb") as buffer:
           shutil.copyfileobj(file.file, buffer)      
       
       return {"filename": file.filename}
   ```
   
   `File(...)`和`str=Form(...)`表示从body中提取对应格式的信息
   
   
   
2. 完整HTTP报文

   ```
   POST /upload HTTP/1.1
   Host: 127.0.0.1:8081
   Content-Length: 348
   Content-Type: multipart/form-data; boundary=THIS_IS_BOUNDARy
   
   --THIS_IS_BOUNDARy
   Content-Disposition: form-data; name="file"; filename="example.txt"
   Content-Type: text/plain
   
   Hello, World!
   --THIS_IS_BOUNDARy
   Content-Disposition: form-data; name="data"
   
   {"username": "john_doe", "age": 30}
   --THIS_IS_BOUNDARy--
   
   ```

   实际上

   ```
   POST /upload HTTP/1.1\r\nHost: 127.0.0.1:8081\r\nContent-Length: 258\r\nContent-Type: multipart/form-data; boundary=THIS_IS_BOUNDARy\r\n\r\n--THIS_IS_BOUNDARy\r\nContent-Disposition: form-data; name="file"; filename="example.txt"\r\nContent-Type: text/plain\r\n\r\nHello, World!\r\n--THIS_IS_BOUNDARy\r\nContent-Disposition: form-data; name="data"\r\n\r\n{"username": "john_doe", "age": 30}\r\n--THIS_IS_BOUNDARy--\r\n
   ```

   

3. 当使用curl同时上传文件和表单数据时

   ```bash
   curl -X POST "http://localhost:8000/upload" \
   > -H "Content-Type: multipart/form-data; boundary=--------------------------OudarFyTcP4CeZ32tPyHAf" \
   > -F "file=@example.txt" \
   > -F "data={\"username\": \"john_doe\", \"age\": 30}"
   ```

   或者使用requests库

   ```python
   files = {
   	"file": ("example.txt", open(file_path, "rb"), "text/plain")
   }
   data = {
   	"data": json.dumps({"username": "JohnDoe","age": 30})  # 将 JSON 数据转换为字符串
   }
   
   response = requests.post("http://127.0.0.1:8000/upload", files=files, data=data)
   
   print(response.json())
   ```

   生成的HTTP请求报文中，**数据对应的部分类型，都是表单数据而不是json**

   ```
   Content-Disposition: form-data; name="data"
   ```



4. FastAPI 提供了多种依赖注入函数，用于从请求的不同部分提取数据：

   | 依赖注入函数 |                    作用                     |              示例               |
   | :----------: | :-----------------------------------------: | :-----------------------------: |
   |    `Path`    |            从路径参数中提取数据             |   `item_id: int = Path(...)`    |
   |   `Query`    |            从查询参数中提取数据             |      `q: str = Query(...)`      |
   |    `Body`    |          从请求体中提取 JSON 数据           |    `item: Item = Body(...)`     |
   |    `File`    |   从 `multipart/form-data` 请求中提取文件   | `file: UploadFile = File(...)`  |
   |    `Form`    | 从 `multipart/form-data` 请求中提取表单数据 |     `name: str = Form(...)`     |
   |   `Header`   |             从请求头中提取数据              | `user_agent: str = Header(...)` |
   |   `Cookie`   |            从 Cookie 中提取数据             | `session_id: str = Cookie(...)` |



## 6.2 多文件上传

1. 服务端

   ```python
   @app.post("/uploads")
   async def upload_files(files: List[UploadFile] = File(...)):
       
       for file in files:
           print(f"文件名: {file.filename}, 类型: {file.content_type}")
           with open(file.filename, "wb") as buffer:
               shutil.copyfileobj(file.file, buffer)
               
       return {"message": "文件上传成功"}
   ```



2. 客户端

   ```python
   import requests
   from contextlib import ExitStack
   
   def upload_files(url, file_paths):
       """
       动态上传多个文件，并确保文件安全打开和关闭。
   
       :param url: 上传的目标URL
       :param file_paths: 文件路径列表，例如 ['file1.txt', 'file2.txt']
       :return: 服务器的响应
       """
       with ExitStack() as stack:
           files = []
           for file_path in file_paths:
               file = stack.enter_context(open(file_path, 'rb'))  # 安全打开文件
               files.append(('files', (file_path, file, 'application/octet-stream')))
   
           response = requests.post(url, files=files)
           return response.json()
   ```

   - `ExitStack` 是 Python 的上下文管理器工具，用于动态管理多个上下文（如文件打开）。

     - 使用 `stack.enter_context()` 将文件对象添加到 `ExitStack` 中，确保所有文件在退出 `with` 块时自动关闭。

   - `files`在不考虑文件退出的情况下，可写为

     ```python
     files = [
         ('files', ('file1.txt', open('file1.txt', 'rb'), 'text/plain')),
         ('files', ('file2.txt', open('file2.txt', 'rb'), 'text/plain'))
     ]
     ```

     



# 7. 流式传输

1. 流式传输有很多应用场景

   - 大文件上传：分为多个文件块流式上传，避免对内存占用过大。

   - （实时类需求）边下边播：电影边下载边播放

2. 无论请求还是相应，在实际传输中，都是先发送header，然后再发送每部分内容（chunk）



以下案例将“流式请求”和“流式相应”结合一起

## 7.1 服务端

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import time
import json

app = FastAPI()

@app.post("/stream")
async def stream_data(request: Request):
    
    # 接收客户端流式上传的 JSON 数据
    async for chunk in request.stream():
        
        # 收到的第一个chunk是b''
        if len(chunk) == 0:
            continue
        
        data = json.loads(chunk)
        print(f"Received: {data}")  # 打印接收到的数据
        
        
    def process_data():

        # 模拟处理逻辑
        for i in range(5):
            data = {"processed": i}
            yield json.dumps(data) + "\n"  # 返回处理后的数据
            time.sleep(0.1)

    return StreamingResponse(process_data(), media_type="application/json")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```



## 7.2 客户端

```python
import requests
import json
import time

def stream_client():
    url = "http://127.0.0.1:8000/stream"

    # 模拟流式上传的 JSON 数据
    def generate_data():
        for i in range(5):
            data = {"value": i}
            print(f"Sending to server: {data}")
            yield json.dumps(data)
            time.sleep(0.1)  # 模拟上传间隔

    # 发送流式请求并接收流式响应
    with requests.post(url, data=generate_data(), stream=True) as response:
        for chunk in response.iter_lines():
            # 收到的第一个chunk是b``
            if chunk:
                print(f"Received from server: {json.loads(chunk)}")

if __name__ == "__main__":
    stream_client()
```



得到结果

```
Sending to server: {'value': 0}
Sending to server: {'value': 1}
Sending to server: {'value': 2}
Sending to server: {'value': 3}
Sending to server: {'value': 4}
Received from server: {'processed': 0}
Received from server: {'processed': 1}
Received from server: {'processed': 2}
Received from server: {'processed': 3}
Received from server: {'processed': 4}
```





## 7.3 Socket客户端

```python
import socket
import json
import time

def send_http_request(host, port, path, data):
    # 创建 socket 连接
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    # 构造 HTTP 请求头
    headers = (
        f"POST {path} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        "Content-Type: application/json\r\n"
        "Transfer-Encoding: chunked\r\n"  # 使用分块传输编码
        "\r\n"
    )
    sock.send(headers.encode("utf-8"))

    # 发送流式数据
    for chunk in data:
        chunk_size = len(chunk)
        sock.send(f"{chunk_size:x}\r\n".encode("utf-8"))  # 发送块大小
        sock.send(chunk + b"\r\n")  # 发送块数据        
    sock.send(b"0\r\n\r\n")  # 发送结束标志

    # 接收流式响应
    response = b""
    while True:
        part = sock.recv(4096)
        if not part:
            break
        response += part

    sock.close()
    return response

def stream_client():
    host = "127.0.0.1"
    port = 8000
    path = "/stream"

    # 模拟流式上传的 JSON 数据
    def generate_data():
        for i in range(3):
            data = json.dumps({"value": i}).encode("utf-8")
            yield data
            time.sleep(1)  # 模拟上传间隔

    # 发送流式请求并接收流式响应
    response = send_http_request(host, port, path, generate_data())
    print("Raw response:")
    print(response.decode("utf-8"))

if __name__ == "__main__":
    stream_client()
```



发送的HTTP报文

```
POST /stream HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json
Transfer-Encoding: chunked

c
{"value": 0}
c
{"value": 1}
c
{"value": 2}
0


```

实际上

```
POST /stream HTTP/1.1\r\nHost: 127.0.0.1:8000\r\nContent-Type: application/json\r\nTransfer-Encoding: chunked\r\n\r\nc\r\n{"value": 0}\r\nc\r\n{"value": 1}\r\nc\r\n{"value": 2}\r\n0\r\n\r\n
```



接受到的报文

```
HTTP/1.1 200 OK
date: Mon, 10 Mar 2025 10:37:59 GMT
server: uvicorn
content-type: application/json
transfer-encoding: chunked

11
{"processed": 0}

11
{"processed": 1}

11
{"processed": 2}


0


```

实际上

```
HTTP/1.1 200 OK\r\ndate: Mon, 10 Mar 2025 10:37:59 GMT\r\nserver: uvicorn\r\ncontent-type: application/json\r\ntransfer-encoding: chunked\r\n\r\n11\r\n{"processed": 0}\n\r\n11\r\n{"processed": 1}\n\r\n11\r\n{"processed": 2}\n\r\n11\r\n{"processed": 3}\n\r\n11\r\n{"processed": 4}\n\r\n0\r\n\r\n
```

