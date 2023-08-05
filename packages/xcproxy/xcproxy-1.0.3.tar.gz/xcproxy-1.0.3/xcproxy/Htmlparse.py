#from lxml import etree
from bs4 import BeautifulSoup

class Htmlparse(object):
    def html_parse(self,response):
        
        #这里是BeautifulSoup的网页分析代码
        r = BeautifulSoup(response,'html5lib')
        div = r.find_all('div',class_='clearfix proxies')[0]
        tbody = div.find('tbody')
        tr = tbody.find_all('tr')
        ip_list = []
        port_list = []
        localtion_list = []
        type_list = []
        Effective_time_list = []
        Last_verification_time_list = []
        for each in range(1,len(tr)):
            ip = tr[each].find_all('td')[1].text  # IP
            port = tr[each].find_all('td')[2].text  # 端口
            localtion = tr[each].find_all('td')[3].text.strip()  # 地区
            type_ = tr[each].find_all('td')[5].text.strip() #   协议类型
            Effective_time = tr[each].find_all('td')[8].text.strip() # 有效时间
            Last_verification_time = tr[each].find_all('td')[9].text.strip() # 最后验证时间
            ip_list.append(ip)
            port_list.append(port)
            localtion_list.append(localtion)
            type_list.append(type_)
            Effective_time_list.append(Effective_time)
            Last_verification_time_list.append(Last_verification_time)
            #print(ip,port,localtion,type_,Effective_time,Last_verification_time)

        '''
        # 这里用 xpath来进行元素定位
        res = etree.HTML(response)
        tr = res.xpath("//div[@class='clearfix proxies']/table/tr[1]")[0]
        ip_list = tr.xpath('//td[2]/text()')[0]
        port_list = tr.xpath('//td[3]/text()')[0]
        print(ip_list,port_list)'''

        return ip_list,port_list,localtion_list,type_list,Effective_time_list,Last_verification_time_list