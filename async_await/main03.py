import asyncio
import time

"""
将corountine object变为task的方法：
使用asyncio.gather

"""


async def say_after(delay, what):
    await asyncio.sleep(delay)
    return f"{what} - {delay}"

async def main():

    print(f"started at {time.strftime('%X')}")

    """
    asyncio.gather
    传入corountine object，task，future
    返回future

    相当于告诉event loop：
    要等所有的传入的所有task运行结束之后，才可以继续
    """
    ret = await asyncio.gather(
        say_after(1, "hello"),
        say_after(2, "world")
        )
    
    print(ret)
    
    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())