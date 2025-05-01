# FastAPI进阶用法与分析

# 1. 并发访问

分析并发访问时，3种实现的执行情况

## 1.1 基础

1. server

   ```python
   # server.py
   
   import uvicorn, time
   from fastapi import FastAPI
   from threading import current_thread
   
   
   app = FastAPI()
   
   @app.get("/test")
   def read_root(data: dict):
       print(f"[{current_thread().ident}] Begin")
       
       time.sleep(2)
       
       print(f"[{current_thread().ident}] Data: {data}")
       
       time.sleep(2)
       
       print(f"[{current_thread().ident}] End")
       
       return {"echo": f"receive data: {data}"}
       
   
   
   if __name__ == "__main__":
       uvicorn.run(app, host="0.0.0.0", port=8000)
   ```

   

2. client

   ```python
   import requests
   import argparse
   
   parse = argparse.ArgumentParser()
   parse.add_argument("-d", type=str)
   args = parse.parse_args()
   
   
   def test():
       print(f"Data: {args.d}")
       url = "http://127.0.0.1:8000/test"
       headers = {
           "Content-Type": "application/json"
       }
       payload = {"data": args.d}
       
       response = requests.get(url, headers=headers, json=payload)
       print(response.json())
       
       
       
   if __name__ == "__main__":
       test()
   ```

   ```
   python code/test/test_fastapi/client.py -d 1
   ```

   ```
   python code/test/test_fastapi/client.py -d 2
   ```

3. 输出

   面对多个请求，启动多个线程

   ```python
   INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
   [140545002104576] Begin
   [140544993711872] Begin
   [140545002104576] Data: {'data': '1'}
   [140544993711872] Data: {'data': '2'}
   [140545002104576] End
   INFO:     127.0.0.1:58124 - "GET /test HTTP/1.1" 200 OK
   [140544993711872] End
   INFO:     127.0.0.1:58134 - "GET /test HTTP/1.1" 200 OK
   ```

   



## 1.2 async

1. server

   ```python
   @app.get("/test")
   async def read_root(data: dict):
       print(f"[{current_thread().ident}] Begin")
       
       time.sleep(2)
       
       print(f"[{current_thread().ident}] Data: {data}")
       
       time.sleep(2)
       
       print(f"[{current_thread().ident}] End")
       
       return {"echo": f"receive data: {data}"}    
   ```

   

2. 输出

   面对多个请求，顺序执行

   ```python
   INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
   [140428800546624] Begin
   [140428800546624] Data: {'data': '1'}
   [140428800546624] End
   INFO:     127.0.0.1:50794 - "GET /test HTTP/1.1" 200 OK
   [140428800546624] Begin
   [140428800546624] Data: {'data': '2'}
   [140428800546624] End
   INFO:     127.0.0.1:50800 - "GET /test HTTP/1.1" 200 OK
   ```

   

## 1.3 async + await

1. server

   ```python
   @app.get("/test")
   async def read_root(data: dict):
       print(f"[{current_thread().ident}] Begin")
       
       await asyncio.sleep(2)
       
       print(f"[{current_thread().ident}] Data: {data}")
       
       await asyncio.sleep(2)
       
       print(f"[{current_thread().ident}] End")
       
       return {"echo": f"receive data: {data}"}
   ```

2. 输出

   面对多个请求，单线程内交错执行

   ```python
   INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
   [139845369354048] Begin
   [139845369354048] Begin
   [139845369354048] Data: {'data': '1'}
   [139845369354048] Data: {'data': '2'}
   [139845369354048] End
   INFO:     127.0.0.1:47884 - "GET /test HTTP/1.1" 200 OK
   [139845369354048] End
   INFO:     127.0.0.1:47894 - "GET /test HTTP/1.1" 200 OK
   ```




# 2. Background Tasks

https://fastapi.tiangolo.com/tutorial/background-tasks/



1. You can define background tasks to be run *after* returning a response.

2. 代码

   ```python
   # server.py
   
   import uvicorn, time
   from fastapi import BackgroundTasks, FastAPI
   
   app = FastAPI()
   
   
   def write_notification(email: str, message=""):
       time.sleep(6)
       if email == "raise":
           raise ValueError("test error")
       print(f"Notification sent to {email} with message: {message}")
   
   
   @app.post("/send-notification/{email}")
   async def send_notification(email: str, background_tasks: BackgroundTasks):
       background_tasks.add_task(write_notification, email, message="some notification")
       return {"message": "Notification sent in the background"}
   
   
   if __name__ == "__main__":
       uvicorn.run(app, host="0.0.0.0", port=8000)
   ```

   ```python
   # client.py
   
   import requests
   
   url = "http://127.0.0.1:8000/send-notification/123"
   headers = {
       "Accept": "application/json",
       "Content-Type": "application/json",
   }
   payload = {}
   
   response = requests.request("POST", url, headers=headers, json=payload)
   
   print(response.text)
   print(response.json())
   ```

   

3. background task直接使用了starlette.background

   > The class `BackgroundTasks` comes directly from [`starlette.background`](https://www.starlette.io/background/)

4. background task 的执行顺序

   https://www.starlette.io/background/

   > The tasks are executed in order. In case one of the tasks raises an exception, the following tasks will not get the opportunity to be executed.



# 3. Callback

OpenAPI：https://spec.openapis.org/oas/latest.html#callback-object

FastAPI：https://fastapi.tiangolo.com/advanced/openapi-callbacks/

1. 客服端向服务端发送的请求中，包含了第三方url

   在服务端处理相关请求时，会向第三方url发送请求。

2. **建议在FastAPI中，基于POST方式直接手动实现Callback**。

   **其提供的Callback功能，完全是出于OpenAPI描述文档的需要**

   ```python
   @invoices_callback_router.post(
       "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived
   )
   def invoice_notification(body: InvoiceEvent):
       pass
   ```

   > It doesn't need to have any actual code, because your app will never call this code. It's only used to document the *external API*. So, the function could just have `pass`.



# 4. Webhook

 资料：

- OpenAPI中：https://spec.openapis.org/oas/latest.html#oas-webhooks
- FastAPI中：https://fastapi.tiangolo.com/advanced/openapi-webhooks
- Github Webhook的应用：https://docs.github.com/en/webhooks

FastAPI关于支持Webhook的issue

- https://github.com/fastapi/fastapi/issues/4709



## 4.1 概念

1. 假设有两个机器A和B，A需要实时的了解B的更新，使用网络通信，有两种可能

   - polling：A每隔几秒向B发送请求，询问是否有更新
   - 长连接：A和B之间一直保持连接，B一有更新就发送

2. Webhook提供了第三种方式，事件驱动

   很接近“订阅-发布”模式

   - 注册：A 向 B注册，告知B以下两部分信息
     - 什么事件可以触发
     - B向A的哪个url发送消息
   - 通知：当B中发生了A注册的事件时，向A指定的URL发送消息

   ```mermaid
    graph LR
        A(server A) --"注册"--> B(server B)
        B --通知--> A
   ```

   相比于前两种方式，可以显著节约网络通信资源


3. Github Webhooks就是这种应用

   > Webhooks let you subscribe to events happening in a software system and automatically receive a delivery of data to your server whenever those events occur.

   > When you create a webhook, you specify a URL and subscribe to events that occur on GitHub. When an event that your webhook is subscribed to occurs, GitHub will send an HTTP request with data about the event to the URL that you specified. 



4. 各方面支持

   - OpenAPI在3.1.0中，才引入webhook
   - FastAPI 0.99.0开始支持webhook

   事实上，使用简单的POST类型接口即可实现webhook，其核心技术就是在服务端的接口函数中发送一个http请求



## 4.2 实现

基于通义千问生成代码修改

签名是为了验证身份，初次学习可以跳过

1. 用于注册 webhook 和触发事件的服务端，模拟GitHub的 webhook 机制

   ```python
   # server_b.py
   
   from fastapi import FastAPI, HTTPException
   from pydantic import BaseModel
   import requests, hmac, hashlib, json
   import uvicorn
   
   """
   用于注册 webhook 和触发事件的服务端，模拟GitHub的 webhook 机制
   """
   
   app = FastAPI()
   
   # 存储已注册的 webhook
   webhooks = []
   
   class WebhookRequest(BaseModel):
       url: str
       event: str
   
   class OrderStatusChanged(BaseModel):
       order_id: str
       new_status: str
   
   # 共享密钥，用于生成签名
   SECRET_KEY = "your-secret-key"
   
   @app.post("/webhooks")
   async def register_webhook(webhook: WebhookRequest):
       webhooks.append(webhook)
       return {"message": "Webhook registered successfully"}
   
   @app.post("/trigger-event")
   async def trigger_event(order_status: OrderStatusChanged):
       # 注意：不一定是因为请求直接触发，也可能是由于后端运行某个程序达到某种状态触发
       for webhook in webhooks:
           if webhook.event == "order_updated":
               send_webhook_notification(webhook.url, order_status)
       return {"message": "Event triggered and notifications sent"}
   
   def send_webhook_notification(url: str, order_status: OrderStatusChanged):
       payload = {
           "orderId": order_status.order_id,
           "newStatus": order_status.new_status
       }
       payload_json = json.dumps(payload)
       
       # 生成签名
       signature = hmac.new(SECRET_KEY.encode(), payload_json.encode(), hashlib.sha256).hexdigest()
       
       headers = {
           "Content-Type": "application/json",
           "X-Signature": f"sha256={signature}"
       }
       
       try:
           response = requests.post(url, data=payload_json, headers=headers)
           response.raise_for_status()
       except requests.exceptions.RequestException as e:
           print(f"Failed to send webhook notification to {url}: {e}")
           
   
   if __name__ == "__main__":
       uvicorn.run(app, host="0.0.0.0", port=8001)
   ```

   

2. 用于接收消息的服务端，模拟用户的服务端

   ```python
   # server_a.py
   
   from fastapi import FastAPI, Request
   import hmac, json, hashlib, uvicorn
   
   """
   用于接收消息的服务端，模拟用户的服务端
   
   """
   
   app = FastAPI()
   
   @app.post('/receive_webhook')
   def receive_webhook(request: Request, payload: dict):
       signature = request.headers.get('X-Signature')
       
       # 验证签名
       expected_signature = hmac.new(b'your-secret-key', json.dumps(payload).encode(), hashlib.sha256).hexdigest()
       if not hmac.compare_digest(signature.split('=')[1], expected_signature):
           return {"error": "Invalid signature"}
       
       print(f"Received webhook: {payload}")
       return {"message": "Webhook received successfully"}
   
   if __name__ == '__main__':
       uvicorn.run(app, host='0.0.0.0', port=8000)
   ```

   

3. 模拟事件触发

   ```python
   # simulate.py
   import requests
   
   def simluated_register_webhook():
       """
       模拟注册 webhook
       """
       url = "http://127.0.0.1:8001/webhooks"
       headers = {
           "Content-Type": "application/json"
       }
       data = {
           "url": "http://127.0.0.1:8000/receive_webhook",
           "event": "order_updated"
       }
       
       response = requests.post(url, headers=headers, json=data)
       print(response.json())
       
       
   def simluated_trigger_event():
       """
       模拟触发事件
       """
       url = "http://127.0.0.1:8001/trigger-event"
       headers = {
           "Content-Type": "application/json"
       }
       data = {
           "order_id": "12345",
           "new_status": "shipped"
       }
   
       response = requests.post(url, headers=headers, json=data)
       print(response.json())
       
       
   
   if __name__ == "__main__":
       simluated_register_webhook()
       simluated_trigger_event()
   ```

   

## 4.3 FastAPI中的webhook

https://fastapi.tiangolo.com/advanced/openapi-webhooks

https://fastapi.tiangolo.com/reference/fastapi/?h=webhook#fastapi.FastAPI.openapi_version

1. FastAPI中所谓的webhook令人费解：**webhook相当于APIRouter，仅为生成OpenAPI文档使用**

   > The `app.webhooks` attribute is an `APIRouter` with the *path operations* that will be used just for documentation of webhooks.

   > The `app.webhooks` object is actually just an `APIRouter`
   >
   > Notice that with webhooks you are actually not declaring a *path* (like `/items/`), the text you pass there is just an **identifier** of the webhook (the name of the event), for example in `@app.webhooks.post("new-subscription")`, the webhook name is `new-subscription`.



2. 可观察此两种情况的docs，发现对app.webhook的支持实属鸡肋

   ```python
   import uvicorn
   from fastapi import FastAPI, APIRouter
   
   new_webhook = APIRouter(prefix="/new_webhook")
   
   @new_webhook.post("/hello")
   def hello(data: dict):
       """hello world"""
       return {"message": "Hello World"}
   
   app = FastAPI(
       webhooks=new_webhook,
   )
   
   
   if __name__ == "__main__":
       uvicorn.run(app, host="0.0.0.0", port=8000)
   ```

   ```python
   import uvicorn
   from fastapi import FastAPI
   
   app = FastAPI()
   
   @app.webhooks("/new_webhooks")
   def hello(data: dict):
       """hello world"""
       return {"message": "Hello World"}
   
   if __name__ == "__main__":
       uvicorn.run(app, host="0.0.0.0", port=8000)
   ```

   

3. **建议在FastAPI中使用Webhook，就直接根据原理实现即可，不要使用其app.webhook**

