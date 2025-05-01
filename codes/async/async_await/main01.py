import asyncio
import time

"""
await：await <corountine object>

await say_after(1, "hello")程序执行动作：
1. 将corountine object变为task 
    (效果上可如此理解，但是实际不是这样)
2. event loop 被告知此处有一个task；
    event loop 被告知当前await所在的task
    需要等待<corountine object>的task完成之后再运行
3. yield
    event loop 被告知此处<corountine object>的task当前无法运行
4. event loop再次选择执行此任务时，
    await 获取<corountine object>的返回值（运行该函数）

event_loop无法直接从task的手中夺回（程序运行）控制权
task有两种方式交回控制权
1. await
2. 函数运行结束自动交回    

"""

"""
输出：等待3秒
started at 16:31:56
hello
world
finished at 16:31:59

不符合使用协程的初衷，await完成的事情过多
"""


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after(1, "hello")
    await say_after(2, "world")

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())