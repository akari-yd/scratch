import random


class pool(object):
    def __init__(self):
        self.ip_list = [{"https": "171.12.115.4"},
                        {"https": "58.220.95.8"},
                        {"https": "47.91.137.211"}]
        self.user_agent_list = ["Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
                                "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
                                "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
                                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
                                "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
                                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/41.0.2228.0 Safari/537.36",
                                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, "
                                "like Gecko) Chrome/41.0.2227.1 Safari/537.36",
                                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/41.0.2227.0 Safari/537.36",
                                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/41.0.2227.0 Safari/537.36",
                                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/41.0.2226.0 Safari/537.36",
                                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
                                "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
                                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
                                "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
                                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
                                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/42.0.2311.135 Safari/537.36 Edge/12.246 "
                                ]

    def ip(self):
        ip = random.choice(self.ip_list)
        return ip

    def user_agent(self):
        user_agent_get = random.choice(self.user_agent_list)
        return user_agent_get

    def ip_update(self, ip_list):
        self.ip.append(ip_list)


def ip_get():
    ip_list = []
    return ip_list
