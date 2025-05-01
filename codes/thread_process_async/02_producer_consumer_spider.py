import queue
import threading
import blog_spider
import time
import random
# 生产者
def do_craw(url_queue, html_queue):
    # 不可以写while not url.queue.empty()
    # 因为一旦url_queue为空，线程就会结束
    # 我们需要生产者一直生产，因此使用while True
    while True:
        url = url_queue.get()
        # 模拟负载
        time.sleep(random.randint(1, 2))
        html = blog_spider.crawl(url)
        html_queue.put(html)
        print(threading.current_thread().name, "url_queue.size=", url_queue.qsize())
    return

# 消费者
def do_parse(html_queue, fout):
    while True:
        html = html_queue.get()
        # 模拟负载
        time.sleep(random.randint(1, 2))
        results = blog_spider.parse(html)
        for result in results:
            fout.write(str(result) + "\n")
        print(threading.current_thread().name, "html_queue.size=", html_queue.qsize())
    return

def main():

    url_queue = queue.Queue()
    html_queue = queue.Queue()
    for url in blog_spider.urls:
        url_queue.put(url)
    
    fout = open("02_producer_consumer_spider.txt", "w")

    threads_craw = []
    # 创建3个生产者线程
    for i in range(3):
        t = threading.Thread(target=do_craw, args=(url_queue,html_queue), name=f"craw_{i}")
        threads_craw.append(t)

    threads_parse = []
    # 创建2个消费者线程
    for i in range(2):
        t = threading.Thread(target=do_parse, args=(html_queue, fout), name=f"parse_{i}")
        threads_parse.append(t)

    # 启动所有线程
    for t in threads_craw:
        t.start()
    for t in threads_parse:
        t.start()

    return

if __name__ == "__main__":
    main()