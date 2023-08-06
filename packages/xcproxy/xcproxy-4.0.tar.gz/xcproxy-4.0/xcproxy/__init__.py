import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curPath)

from Proxy import proxy

start = proxy()  # 定义主类

def get_proxy():
    result = start.run() # 调用主类的函数
    return result