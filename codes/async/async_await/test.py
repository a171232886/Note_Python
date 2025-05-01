import asyncio

# 定义一个协程函数
async def my_coroutine(id):
    print(f"Begin from coroutine {id}")
    await asyncio.sleep(1)
    print(f"End from coroutine {id}")

async def task_a(num1,num2):
   tasks = [asyncio.create_task(my_coroutine(i)) for i in range(num1,num2)]
   await asyncio.wait(tasks)
   return


async def task_b(num):
   await my_coroutine(num)
   return

async def main():
    # 创建多个任务
    tasks = [
        asyncio.create_task( task_a(num1=10, num2=15) ),
        asyncio.create_task( task_b(100) ),
        asyncio.create_task( task_b(200) ),
    ]

    # 使用asyncio.wait()等待所有任务完成
    done, _ = await asyncio.wait(tasks)

    pass


# 调用asyncio.run()来运行main()协程
asyncio.run(main())
