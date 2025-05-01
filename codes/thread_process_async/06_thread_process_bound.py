from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import math
import time

numbers = [11227343467] * 100

def is_prime(n):
    # 判断n是不是素数
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0: # 偶数
        return False
    sqrt_n = int(math.floor(math.sqrt(n))) # 取整

    for i in range(3, sqrt_n + 1, 2): # 从3开始，步长为2
        if n % i == 0:
            return False
    return True

def single_thread():
    for number in numbers:
        is_prime(number)

def multi_thread():
    with ThreadPoolExecutor() as pool:
        pool.map(is_prime, numbers)

def multi_process():
    with ProcessPoolExecutor() as pool:
        pool.map(is_prime, numbers)

if __name__ == "__main__":
    start = time.time()
    single_thread()
    end = time.time()
    print("单线程耗时: ", end - start)

    start = time.time()
    multi_thread()
    end = time.time()
    print("多线程耗时: ", end - start)

    start = time.time()
    multi_process()
    end = time.time()
    print("多进程耗时: ", end - start)


# 以下为Copilot自动生成

# 1. 什么是线程
# 线程是操作系统能够进行运算调度的最小单位。它被包含在进程之中，是进程中的实际运作单位。
# 一个进程中可以有多个线程，它们共享进程资源，但每个线程拥有自己的栈和局部变量。
# 线程由CPU独立调度执行，在多CPU环境下就允许多个线程同时运行。
# 同样多线程也可以实现并发操作，每个请求分配一个线程来处理。
#
# 2. 什么是进程

# 进程是指在系统中正在运行的一个应用程序，每个进程之间是独立的、不共享内存空间，但是它们可以通过进程间通信来通信。
# 一个进程可以包含一个或多个线程。
# 进程是资源分配的最小单位，线程是CPU调度的最小单位。
# 进程拥有自己的独立地址空间，每启动一个进程，系统就会为它分配地址空间，建立数据表来维护代码段、堆栈段和数据段。
# 进程间的切换会有较大的开销，资源开销较大。
# 进程间不会相互影响，一个进程挂掉不会影响其他进程。
# 进程可以拥有多个线程，同一个进程中的多个线程共享该进程中的全部系统资源。
# 线程间的切换开销小，资源开销较小。
# 线程间共享进程资源，一个线程挂掉会导致整个进程挂掉。
#
# 3. 什么是协程
# 协程是一种用户态的轻量级线程，协程的调度完全由用户控制。
# 协程拥有自己的寄存器上下文和栈。
# 协程调度切换时，将寄存器上下文和栈保存到其他地方，切换回来的时候，恢复先前保存的寄存器上下文和栈。
# 因此：
# 协程能保留上一次调用时的状态（即所有局部状态的一个特定组合），每次过程重入时，就相当于进入上一次调用的状态，换种说法：进入上一次离开时所处逻辑流的位置。
# 协程本质上是个单线程，协程相对于多线程的优势在于：无需线程上下文切换的开销、无需原子操作锁定及同步的开销，编程模型也非常简单。
# 协程不需要多线程的锁机制，因为只有一个线程，也不存在同时写变量冲突，在协程中控制共享资源不加锁，只需要判断状态就好了，所以执行效率比多线程高很多。
# 协程适用于IO密集型任务，如果是CPU密集型，则需要多线程配合。
# 协程的本质是控制流的一个特殊点，或者说是特殊的间断点，因此协程也被称为用户态线程。

