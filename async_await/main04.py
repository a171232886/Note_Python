import asyncio

"""
1. event_loop 最小调度单位为task，不能直接调度coroutine object
2. await 可以用于coroutine object，也可以用于task，还可以是future
3. coroutine object相当于一个简单的生成器
4. task在Cpython中继承了future


3. await的字节码包含GET_AWAITABLE和YIELD_FROM

"""

async def main():
    await asyncio.create_task(
        asyncio.sleep(1)
    )

asyncio.run(main())