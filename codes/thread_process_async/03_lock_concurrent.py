import threading
import time

class Account:
    def __init__(self, blance) -> None:
        self.blance = blance

def draw(account, amount):
    if account.blance >= amount:
        # 若添加time.sleep会阻塞，按照python的机制，会发生线程切换
        # 也就是t1在if分支sleep 0.1s，而t2也会进入if分支，发生了取两次钱的境况
        # 此时一定出现blance<0的情况
        # 若不添加time.sleep，取两次钱的情况会随机出现
        time.sleep(0.1)
        
        print(f"{threading.current_thread().name} Success")
        # 取钱
        account.blance -= amount
        print(f"{threading.current_thread().name} now blance =", account.blance)
    else:
        print(f"{threading.current_thread().name} Failure")

def main():
    account = Account(800)
    t1 = threading.Thread(name="t1", target=draw, args=(account, 600))
    t2 = threading.Thread(name="t2", target=draw, args=(account, 600))

    t1.start()
    t2.start()

if __name__ == "__main__":
    main()