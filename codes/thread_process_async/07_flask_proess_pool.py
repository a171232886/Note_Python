import flask
import math
import json
from concurrent.futures import ProcessPoolExecutor

app = flask.Flask(__name__)

def is_prime(n):
    # 判断n是不是素数
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0: # 偶数
        return False
    sqrt_n = int(math.floor(math.sqrt(n))) # 取整

    for i in range(3, sqrt_n + 1, 2): # 从3开始，步长为2
        if n % i == 0:
            return False
    return True

@app.route("/is_prime/<numbers>")
def api_is_prime(numbers):
    number_list = [int(number) for number in numbers.split(",")]
    results = process_pool.map(is_prime, number_list)
    return json.dumps(dict(zip(number_list, results)))

if __name__ == "__main__":
    # 创建进程池 必需main函数处创建
    process_pool = ProcessPoolExecutor()
    app.run(debug=True)