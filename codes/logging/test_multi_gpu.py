import torch
import pynvml
import logging


def write_gpu_utilization(logger):
    # 每个GPU对应一个rank（进程），只让一个进程处理logger信息
    # 通常让rank0处理
    if 0 == torch.distributed.get_rank():
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        memory_usage = f"GPU 0 memory occupied: {info.used//1024**2} MB.\n"
        logger.debug(memory_usage)


def create_logger():
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

    return logger

def main():
    # ... 其他程序
    logger = create_logger()
    write_gpu_utilization(logger)
    # ... 其他程序

if __name__ == "__main__":
    main()