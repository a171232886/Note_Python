import logging

"""
1. 日志级别: NOTSET、DEBUG、INFO、WARNING、ERROR、CRITICAL
    - 若设置为INFO, 则会打印WARNING、ERROR、CRITICAL
    - 默认为WARNING
2. 基础设置basicConfig
    level：主要调整logging的级别
    filename：输出日志的路径
    filemode：直接写入w,还是追加写入a
    format：输出的格式, 
            常用 “%(asctime)s %(name)s:%(levelname)s:%(message)s”
            即，时间，名称，输出级别，信息
    datefmt：对时间格式的设置，与time.strftime()相同，
            常用"%Y-%m-%d %H:%M:%S"
            https://docs.python.org/zh-cn/3/library/time.html#time.strftime
    

3. format的可选信息
    %(levelno)s：打印日志级别的数值。
    %(levelname)s：打印日志级别的名称。
    %(pathname)s：打印当前执行程序的路径，其实就是sys.argv[0]。
    %(filename)s：打印当前执行程序名。
    %(funcName)s：打印日志的当前函数。
    %(lineno)d：打印日志的当前行号。
    %(asctime)s：打印日志的时间。
    %(thread)d：打印线程ID。
    %(threadName)s：打印线程名称。
    %(process)d：打印进程ID。
    %(processName)s：打印线程名称。
    %(module)s：打印模块名称。
    %(message)s：打印日志信息。


参考:
1. https://docs.python.org/zh-cn/3/howto/logging.html
2. https://zhuanlan.zhihu.com/p/445411809
3. https://zhuanlan.zhihu.com/p/166236399
"""

def main():
    # 最简使用
    logging.basicConfig(filename="test.log", 
                        filemode="w", 
                        format="[%(asctime)s][%(levelname)s] %(message)s", 
                        datefmt="%Y-%m-%d %H:%M:%S", 
                        level=logging.DEBUG)
    logging.debug('This is a debug message')
    logging.info('This is an info message')
    logging.warning('This is a warning message')
    logging.error('This is an error message')
    logging.critical('This is a critical message')

    # 异常处理
    a = 5
    b = 0
    try:
        c = a / b
    except Exception as e:
        logging.exception("Exception occurred")

if __name__ == "__main__":
    main()