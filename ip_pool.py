from urllib.request import Request, urlopen
import re
import requests

class ip_pool():
    def __init__(self):
        pass
    
    def get_ip(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/85.0.4183.121 Safari/537.36'}
        url_origin = 'https://ip.ihuan.me/address/5Lit5Zu9.html'
        url = url_origin
        ip_pool_origin = []
        for i in range(15):
            req = Request(url, headers = headers)
            html = urlopen(req).read().decode('utf-8')
            print(html)
            ip_https = re.findall(r'<.*?>.+?</a></td><td>\d*?</td><td><.*?>中国</a>&nbsp;<.*?>.*?</a>&nbsp;<.*?>.*?</a>&nbsp;</td><td><.*?>.*?</a></td><td>支持', html)
            
            for ip in ip_https:
                temp = ip_pool_origin.append(re.split(r'[<>]', ip)[2])
                print(temp)
            next_page = re.findall(r'".*?"aria-label="Next">', html)[0][1:-18]
            if next_page:
                url = 'https://ip.ihuan.me/address/5Lit5Zu9.html' + next_page
            else:
                break
        ip_pool = check_ip(ip_pool_origin)
        return ip_pool
        

    def check_ip(self, ip_pool_origin):
        ip_pool = []
        for ip in ip_pool_origin:
            try:
                requests.get('http://www.douban.com', proxies={"http":"http://" + ip})
            except:
                pass
            else:
                ip_pool.append(ip)
        return ip_pool
ip = ip_pool()
print(ip.get_ip())
