import asyncio
import aiohttp
import blog_spider

# 创建信号量
sem = asyncio.Semaphore(10)

async def async_craw(url):
    # 使用信号量控制并发度
    async with sem:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                # await 表示该操作无需阻塞等待，协程跳转至其他任务
                result = await resp.text()
                print(f"请求{url}成功")

# 创建一个asyncio的事件循环
loop = asyncio.get_event_loop()

# 创建一个任务列表
tasks = [loop.create_task(async_craw(url)) for url in blog_spider.urls]

# 运行
loop.run_until_complete(asyncio.wait(tasks))