import pytest
from datetime import datetime

@pytest.fixture(autouse=True, scope="session")
def f():
    # 前置操作
    print(datetime.now(), "开始执行")
    
    yield "fixture_result"  # 执行用例
    
    # 后置操作
    print("\n", datetime.now(), "执行结束")