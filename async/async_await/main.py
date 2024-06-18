import asyncio
import time

"""
corountine
corountine function: async def func()
    func()返回一个corountine object，而不会运行这个函数

进入async模式：asyncio.run(<corountine object>)。程序会执行以下动作：
    1. 创建一个event loop
    2. 将传入的corountine object变为event loop中的task
    3. 运行可执行的task
"""

# Python 3.7+
async def main():
    print('Hello ...')
    await asyncio.sleep(1)
    print('... World!')

asyncio.run(main())

# coro = main() 返回一个corountine object
