from concurrent.futures import ThreadPoolExecutor, as_completed
import blog_spider

# craw
with ThreadPoolExecutor() as pool:
    htmls = pool.map(blog_spider.craw, blog_spider.urls)
    htmls = list(zip(blog_spider.urls, htmls))
    for url, html in htmls:
        print(url, len(html))

# parse
with ThreadPoolExecutor() as pool:
    futures = []
    urls = []
    for url, html in htmls:
        future = pool.submit(blog_spider.parse, htmls)
        futures.append(future)
        urls.append(url)
    
    # for idx, future in enumerate(futures):
    #     print(urls[idx], future.result())

    for future in as_completed(futures):
        print(future.result())