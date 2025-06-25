import os
import pytest


pytest.main(["-v"])
os.system("allure generate -o report -c cache")