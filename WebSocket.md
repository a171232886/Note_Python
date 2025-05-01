# WebSocket

# 1. 概念

（通义千问生成）

WebSocket 是一种在单个 TCP 连接上进行全双工通信的协议。WebSocket 使得客户端和服务器之间的数据交换变得更加简单，允许服务端主动向客户端推送数据。在 WebSocket API 中，浏览器和服务器只需要完成一次握手，两者之间就直接可以创建持久性的连接，并进行双向数据传输。



## 1.1 WebSocket 的特点

- **全双工通信**：WebSocket 允许服务器和客户端同时发送数据，这意味着在同一个连接中，双方都可以独立地发送数据，而不需要等待对方的数据发送完毕。

- **减少通信开销**：相比传统的 HTTP 请求，WebSocket 协议减少了不必要的头信息和状态信息，从而减少了数据传输的开销。

- **保持连接状态**：一旦建立连接，除非连接断开，否则这个连接会一直保持活动状态。

- **支持多种数据格式**：WebSocket 不仅可以发送文本数据，还可以发送二进制数据。

  

## 1.2 建立 WebSocket 连接

WebSocket 连接的建立是通过一个称为“升级”的过程实现的，这个过程是从 HTTP 协议开始的。以下是建立 WebSocket 连接的基本步骤：

1. **客户端发起请求**：客户端（通常是浏览器）发送一个特殊的 HTTP 请求给服务器，请求将连接升级到 WebSocket 协议。这个请求中包含了 `Upgrade: websocket` 和 `Connection: Upgrade` 头信息，以及一个用于安全验证的密钥。
2. **服务器响应**：如果服务器支持 WebSocket 并同意升级，它会返回一个 101 状态码（Switching Protocols），表示协议已经从 HTTP 切换到了 WebSocket。响应中也会包含一些必要的头信息来确认握手过程。
3. **连接建立**：一旦握手成功，客户端和服务器之间的 WebSocket 连接就建立了，双方可以通过这个连接自由地发送消息。



## 1.3 WebSocket API

在 JavaScript 中，可以使用 WebSocket 对象来操作 WebSocket 连接。以下是一些常用的 API 方法和事件：

- **方法**
  - `new WebSocket(url, [protocols])`：创建一个新的 WebSocket 实例。
  - `send(data)`：通过连接发送数据。
  - `close([code], [reason])`：关闭连接，可选参数 `code` 和 `reason` 用于指定关闭的原因。
- **事件**
  - `onopen`：当连接成功建立时触发。
  - `onmessage`：当从服务器接收消息时触发。
  - `onerror`：当发生错误时触发。
  - `onclose`：当连接关闭时触发。



## 1.4 应用场景

WebSocket 适合于需要频繁交互的应用，例如实时聊天应用、在线游戏、股票市场数据更新等。由于它可以实现实时的双向通信，因此在这些场景下，WebSocket 能够提供更好的用户体验和更低的延迟。





# 2. 简单使用

基于python-socketio实现，支持同步和异步两种方式

- https://python-socketio.readthedocs.io/en/stable/
- [Introduction | Socket.IO](https://socket.io/docs/v4/)

安装

```bash
pip install python-socketio
```

若要使用异步方式

```bash
pip install "python-socketio[asyncio_client]"
```



## 2.1 概念

Socket.IO 中的概念

### 2.1.1 Event

https://python-socketio.readthedocs.io/en/stable/client.html#using-the-event-driven-client

1. Event：相当于REST通信中的API

   有两种定义方式：

   ```python
   @sio.event
   def message(data):
       # event名为函数名
       print('I received a message!')
   
   @sio.on('my message')
   def on_message(data):
       #  event名为'my message'
       print('I received a message!')
   ```

2. namespace：不同namespace下可以有相同的event 

   - 默认namespace为“/”

   ```python
   @sio.on('my message', namespace="1")
   def on_message_1(data):
       #  event名为'my message'
       print('I received a message!')
   
   @sio.on('my message', namespace="2")
   def on_message_2(data):
       #  event名为'my message'
       print('I received a message!')
   ```

3. 三个关键event必须清晰定义
   - The `connect`, `connect_error` and `disconnect` events are special

### 2.1.2 emit

https://python-socketio.readthedocs.io/en/stable/client.html#id4

1. `sio.emit('my message', {'foo': 'bar'})`

   相当于向`my message`这个event发送数据`{'foo': 'bar'}`

   可以设置namespace等参数

2. `sio.send({'foo': 'bar'})`

   相当于`sio.emit('my message', {'foo': 'bar'})`



### 2.1.3 room

https://python-socketio.readthedocs.io/en/stable/server.html#rooms

1. 聊天室

   一个人发信息，聊天室内其余人员都收到该信息

2. 提供方法有

   [`socketio.Server.enter_room()`](https://python-socketio.readthedocs.io/en/stable/api.html#socketio.Server.enter_room) and [`socketio.Server.leave_room()`](https://python-socketio.readthedocs.io/en/stable/api.html#socketio.Server.leave_room)

   ```python
   @sio.event
   def begin_chat(sid):
       sio.enter_room(sid, 'chat_users')
   
   @sio.event
   def exit_chat(sid):
       sio.leave_room(sid, 'chat_users')
   ```

3. 发送

   ```python
   sio.emit('my reply', data, room='chat_users') # 服务端
   ```

   

## 2.2 代码案例

1. 服务端

   ```python
   # server.py
   import socketio
   import eventlet
   import eventlet.wsgi
   
   # 创建 SocketIO 服务器，并指定 namespace
   sio = socketio.Server()
   
   # 定义连接事件
   @sio.on('connect', namespace='/chat')
   def connect(sid, environ):
       print('Client connected to /chat:', sid)
   
   # 定义加入房间事件
   @sio.on('join_room', namespace='/chat')
   def join_room(sid, data):
       room = data['room']
       sio.enter_room(sid, room, namespace='/chat')
       print(f'Client {sid} joined room {room}')
       sio.emit('room_message', {'data': f'{sid} has joined the room {room}'}, room=room, namespace='/chat')
   
   # 定义消息事件
   @sio.on('message', namespace='/chat')
   def message(sid, data):
       room = data['room']
       print(f'Message from {sid} in room {room}: {data["data"]}')
       sio.emit('response', {'data': f'Server received: {data["data"]}'}, room=room, namespace='/chat')
   
   @sio.on("message", namespace="/test")
   def test(sid, data):
       print(f"Test message received: {data}")
   
   # 定义断开连接事件
   @sio.on('disconnect', namespace='/chat')
   def disconnect(sid):
       print('Client disconnected from /chat:', sid)
   
   # 创建 WSGI 应用
   app = socketio.WSGIApp(sio)
   
   # 启动服务器
   if __name__ == '__main__':
       eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)
   ```

   注：sid为程序为客户端自动分配，无需手动传入

2. 客户端1

   ```python
   # client1.py
   import socketio
   
   # 创建 SocketIO 客户端，并指定 namespace
   sio = socketio.Client()
   
   # 定义连接事件
   @sio.on('connect', namespace='/chat')
   def on_connect():
       print('Connected to server')
       sio.emit('join_room', {'room': 'room1'}, namespace='/chat')
   
   # 定义消息事件
   @sio.on('response', namespace='/chat')
   def on_response(data):
       print('Response from server:', data)
   
   # 定义房间消息事件
   @sio.on('room_message', namespace='/chat')
   def on_room_message(data):
       print('Room message:', data)
   
   # 定义断开连接事件
   @sio.on('disconnect', namespace='/chat')
   def on_disconnect():
       print('Disconnected from server')
   
   if __name__ == '__main__':
       # 连接到服务器
       sio.connect('http://localhost:5000', namespaces=['/chat', '/test'])
   
       # 发送消息
       sio.emit('message', {'room': 'room1', 'data': 'Hello, server!'}, namespace='/chat')
       sio.emit('message', {'data': 'Hello, server!'}, namespace='/test')
   
   
       # 加入房间
       sio.emit('join_room', {'room': 'room1'}, namespace='/chat')
   
       # 一直等待
       sio.wait()   
   
       # 关闭连接可用 sio.disconnect() 方法
   ```

   

3. 客户端2

   ```python
   # client2.py
   import socketio
   
   # 创建 SocketIO 客户端，并指定 namespace
   sio = socketio.Client()
   
   # 定义连接事件
   @sio.on('connect', namespace='/chat')
   def on_connect():
       print('Connected to server')
       sio.emit('join_room', {'room': 'room1'}, namespace='/chat')
   
   # 定义消息事件
   @sio.on('response', namespace='/chat')
   def on_response(data):
       print('Response from server:', data)
   
   # 定义房间消息事件
   @sio.on('room_message', namespace='/chat')
   def on_room_message(data):
       print('Room message:', data)
   
   # 定义断开连接事件
   @sio.on('disconnect', namespace='/chat')
   def on_disconnect():
       print('Disconnected from server')
   
   if __name__ == '__main__':
       # 连接到服务器
       sio.connect('http://localhost:5000', namespaces=['/chat', '/test'])
   
       # 加入房间
       sio.emit('join_room', {'room': 'room1'}, namespace='/chat')
   
       # 发送消息
       sio.emit('message', {'room': 'room1', 'data': 'This is client 2.'}, namespace='/chat')
   
       # 一直等待
       sio.wait()   
   
       # 关闭连接可用 sio.disconnect() 方法
   ```

# 2. FastAPI中使用

## 2.1 原生

[WebSockets - FastAPI](https://fastapi.tiangolo.com/advanced/websockets/#websockets)

1. **FastAPI** provides the same `WebSocket` directly just as a convenience for you, the developer. But it comes directly from Starlette.
   
   - https://www.starlette.io/websockets/
   
   注意，FastAPI中的websocket：
   
   - 没有namespace和room，仅为websocket的基础功能
   - 需要使用async

2. 过于简陋，过于难用

## 2.2 集成python-socketio

```python
import uvicorn
import socketio
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 配置 CORS（跨域资源共享）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/send")
def send():
    return {"message": "OK"}

# 创建 Socket.IO 服务器实例
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")
app_asgi = socketio.ASGIApp(sio, other_asgi_app=app)

@sio.event
async def connect(sid, environ):
    print(f"Client {sid} connected")

@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")

@sio.event
async def message(sid, data):
    print(f"Message from {sid}: {data}")
    await sio.emit('response', {'data': f"Server received: {data}"}, room=sid)

if __name__ == "__main__":
    uvicorn.run(app_asgi, host="0.0.0.0", port=8000)
```

docs中仅包含非websocket应用
