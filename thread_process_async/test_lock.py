import threading

lock = threading.Lock()

# 写法一
lock.acquire()
try:
    print("lock1")
finally:
    lock.release()


# 写法二
with lock:
    print("lock2")
