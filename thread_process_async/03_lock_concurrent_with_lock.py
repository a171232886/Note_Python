import threading
import time

class Account:
    def __init__(self, blance) -> None:
        self.blance = blance

lock = threading.Lock()

def draw(account, amount):
    with lock:
        if account.blance >= amount:
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