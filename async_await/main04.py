import asyncio

"""
1. event_loop 最小调度单位为task，不能直接调度coroutine object
2. await 可以用于coroutine object，也可以用于task，还可以是future
3. coroutine object在Cpython中的逻辑相当于一个简单的生成器
4. task在Cpython中继承了future


3. await的字节码包含GET_AWAITABLE和YIELD_FROM

GET_AWAITABLE
1. 传入一个coroutine object，返回一个coroutine object
2. 传入一个task/future，返回一个生成器
    yield self

    

"""

async def main():
    """
    await coroutine object时，当前task不会交出控制权，等待coroutine object执行完毕

    在await asyncio.sleep(1)中，经过一系列变化，最终 await 的是一个future
    """
    await asyncio.sleep(1)

    """
    await task时，通知event loop后，会交出控制权，
    event loop再次选择该task时，才执行task
    """
    await asyncio.create_task(
        asyncio.sleep(1)
    )

asyncio.run(main())