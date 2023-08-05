import requests
       
header = {
    'Host':'www.xicidaili.com',
    'Referer':'https://www.xicidaili.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
}

def get_Highly_anonymous(): # 获取高匿IP页面响应
    link = r'https://www.xicidaili.com/nn'
    response = requests.get(link,headers=header)
    return response.text
    

def ip_test(proxy): # 传入一个IP
    header = {
        'Host':'www.ip138.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
    }
    link = 'http://www.ip138.com/'
    try:
        response = requests.get(link,headers=header,proxies=proxy,timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.Timeout:
        return False
        