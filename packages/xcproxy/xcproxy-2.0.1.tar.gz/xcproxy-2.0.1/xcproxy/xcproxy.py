import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


import HtmlDownload
import Htmlparse
import math
def progress_bar(portion,total):
    # portion，已经完成的数量 ； total 总任务数量
    # return ： 返回true
    part = total / 50
    count = math.ceil(portion / part)
    sys.stdout.write('\r')
    sys.stdout.write(('[%-50s]%.2f%%' % (('>' * count),portion/total*100)))
    sys.stdout.flush()

def run():
    ip_pool = []
    response = HtmlDownload.get_Highly_anonymous()  # 获取高匿IP页面信息
    ip_list,port_list,localtion_list,type_list,Effective_time_list,Last_verification_time_list=Htmlparse.html_parse(response)
    total = len(ip_list)
    portion = 0
    print("测试中..")
    for i in range(0,total):
        ip_dict = {ip_list[i]:port_list[i]} # 将每个IP与对应端口打包成一个字典
        # 这里调用IP测试函数，返回一个 boolean ，true就放入ip池
        is_work = HtmlDownload.ip_test(ip_dict)
        if is_work == True:
            ip_pool.append(ip_dict)
        portion += 1
        progress_bar(portion,total)
    print('\n')
    return ip_pool # 返回ip池




