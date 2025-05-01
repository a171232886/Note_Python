import logging
import logging.handlers

def main():
    """
    1. 获取 Logger 对象的方法为 getLogger(), 单例模式, 整个系统只有一个 root Logger 对象
    2. Logger 对象可以设置多个 Handler 对象, Handler 对象又可以设置 Formatter 对象
        针对有时候我们既想在控制台中输出DEBUG 级别的日志，又想在文件中输出WARNING级别的日志。
        可以只设置一个最低级别的 Logger 对象，两个不同级别的 Handler 对象。
    3. 临时禁止输出日志，logger.disabled = True

    """
    # 1. 创建logger
    logger = logging.getLogger("logger")

    # 2. 创建handler
    handler1 = logging.StreamHandler()
    handler2 = logging.FileHandler(filename="test.log", mode="w")

    # 3. 设置输出等级
    logger.setLevel(logging.DEBUG) # 通常设置为两个handler输出中的最低等级
    handler1.setLevel(logging.WARNING)
    handler2.setLevel(logging.DEBUG)

    # 4. 设置输出格式
    formatter = logging.Formatter(fmt="[%(asctime)s][%(levelname)s] %(message)s",
                                  datefmt="%Y-%m-%d %H:%M:%S")
    handler1.setFormatter(formatter)
    handler2.setFormatter(formatter)

    # 5. 添加到logger
    logger.addHandler(handler1)
    logger.addHandler(handler2)

    # 分别为 10、30、30
    # print(handler1.level)
    # print(handler2.level)
    # print(logger.level)

    # 临时禁止输出日志
    # logger.disabled = True

    logger.debug('This is a customer debug message')
    logger.info('This is an customer info message')
    logger.warning('This is a customer warning message')
    logger.error('This is an customer error message')
    logger.critical('This is a customer critical message')


if __name__ == "__main__":
    main()