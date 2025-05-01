import requests
import random
from bs4 import BeautifulSoup

urls = [
    f"https://www.cnblogs.com/#p{page}"
    for page in range(1, 50 + 1)
]

# 一个简单的爬虫
# 用于下载指定的url内容
# 生产者的执行动作
def craw(url):
    r = requests.get(url)
    # print(url, len(r.text))
    return r.text


# 提取网页标题
# 消费者的执行动作
def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_="post-item-title")
    return [(link["href"], link.get_text()) for link in links]

if __name__ == "__main__":
    for result in parse(craw(urls[2])):
        print(result)