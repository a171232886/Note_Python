import threading
import blog_spider

def single_thread():
    print("single thread")
    for url in blog_spider.urls:
        blog_spider.crawl(url)

def multi_thread():
    print("multi thread")

    # 经典的多线程写法
    threads = []
    for url in blog_spider.urls:
        threads.append(
            # 注意这里的参数传递方式
            # args=(url,) 传递的是一个元组
            # args=(url) 传递的是一个字符串
            #   假设传入url=“hello”，python认为传入5个参数分别为'h', 'e', 'l', 'l', 'o'
            threading.Thread(target=blog_spider.crawl, args=(url))
        )
    
    # 启动所有线程
    for thread in threads:
        thread.start()
    
    # 等待所有线程结束
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    # single_thread()
    multi_thread()
    print("main end")