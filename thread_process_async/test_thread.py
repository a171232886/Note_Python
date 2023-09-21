import threading
import time

# Step1：某个函数
def func(a,b):
    # 模拟负载
    time.sleep(20)
    print(a+b)
    return

def main():
    # Step2：创建线程
    t1 = threading.Thread(target=func,args=(1,2))
    t2 = threading.Thread(target=func,args=(3,4))

    # Step3：创建线程
    t1.start()
    t2.start()

    print("main thread")

    # Step4：等待线程结束
    # 若不添加join，则主线程结束后，子线程仍然会继续执行，但整个进程会等待子线程。
    # 此时可观察到输出顺序为"main thread"，"main end"和func

    # 添加join，主线程等待，直到子线程结束，才会继续执行
    # 此时可观察到输出顺序为"main thread"，func和"main end"
    t1.join()
    t2.join()
    return

if __name__ == "__main__":
    main()
    print("main end")
