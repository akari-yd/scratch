# -*- coding: UTF-8 -*-

import urllib3
from urllib import error
from urllib.request import urlopen, Request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import file
import time
from mult_thread import mul_thread
from queue import Queue
import ip

urllib3.disable_warnings()


def book():
    # tag = input('输入要查询的作家：\n')
    tag = '刘慈欣'
    num = search_num(tag)
    queue_num = Queue()
    for i in range(int(num)):
        queue_num.put(i)
    queue_book_url = Queue()
    thread_num = int(num)
    thread = mul_thread(thread_num, search_url, (tag, queue_num, queue_book_url))
    thread.start()
    thread.join()

    queue_book = Queue()
    thread_num = queue_book_url.qsize()
    thread = mul_thread(thread_num, book_spider, (queue_book_url, queue_book))
    thread.start()
    thread.join()
    book_list = book_store(queue_book)
    file_name = tag + '.xlsx'
    file.filesave(file_name, book_list)
    for tag in ['序号', '书名', '作家', '出版社', '出版时间', '页数', '价格', 'ISBN']:
        file.sortxlsx(file_name, tag, 0)


def search_num(tag):
    url_origin = 'https://search.douban.com/book/subject_search?search_text=' + tag + '&cat=1001&start=0'
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument('blink-settings=imagesEnabled=false')
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url_origin)
    html_origin = browser.page_source
    # print(html_origin)

    if re.findall(r'检测到有异常请求从你的 IP 发出', html_origin):
        print('ip被禁止')
        exit(1)

    soup = BeautifulSoup(html_origin, 'lxml')
    num = soup.find_all('a', class_='num')[-1].get_text()

    return num


def search_url(tag, queue_num, queue_book_url):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument('blink-settings=imagesEnabled=false')
    browser = webdriver.Chrome(options=chrome_options)
    page_num = queue_num.get()

    url = 'https://search.douban.com/book/subject_search?search_text=' + tag + '&cat=1001&start=' + str(page_num * 15)
    browser.get(url)
    html = browser.page_source
    book_url = re.findall(r'https://book.douban.com/subject.+?/', html)

    time.sleep(1)

    browser.close()
    browser.quit()

    book_url = list(dict.fromkeys(book_url))
    queue_book_url.put(book_url)


def get_html(url):
    ip_pool = ip.pool()
    user_agent = ip_pool.user_agent()
    headers = {'User-Agent': user_agent,
               'Referer': 'https://book.douban.com/'}
    try:
        req = Request(url, headers=headers)#, proxy=ip_pool.ip)
        html = urlopen(req).read().decode('utf-8')
        return html
    except (error.HTTPError, error.URLError) as e:
        print(e)
        return ''


def book_store(queue_book):
    book_list = [['序号', '书名', '作家', '出版社', '出版时间', '页数', '价格', 'ISBN']]
    count = 0

    while queue_book.empty() is not True:
        count = count + 1
        book_list.append([count] + queue_book.get())

    return book_list


def book_spider(queue_book_url, queue_book):
    book_url_list = queue_book_url.get()
    for url in book_url_list:
        html = get_html(url)
        if html is None:
            print('豆瓣拒绝访问')
            exit(1)

        book_name = re.findall(r'<span property="v:itemreviewed">.*?</span>', html)
        if book_name:
            book_name = book_name[0][32:-7]
        else:
            book_name = ''
        # print(book_name)

        author_str = re.findall(r'\"author\":[\s\S]+?\"name\": \".+?\"', html)
        if author_str:
            author_str = author_str[0]
            author = re.split(r'["]', author_str)[-2]
        else:
            author = ''

        pub_firm = re.findall(r'<span class="pl">出版社:</span>.+?<br/>', html)
        if pub_firm:
            pub_firm = pub_firm[0][28:-5]
        else:
            pub_firm = ''

        pub_time = re.findall(r'<span class="pl">出版年:</span>.*?<br/>', html)
        if pub_time:
            pub_time = pub_time[0][28:-5]
        else:
            pub_time = ''

        page_num = re.findall(r'<span class="pl">页数:</span>.*?<br/>', html)
        if page_num:
            page_num = page_num[0][27:-5]
        else:
            page_num = ''

        price = re.findall(r'<span class="pl">定价:</span>.*?<br/>', html)
        if price:
            price = price[0][27:-5]
        else:
            price = ''

        isbn = re.findall(r'<span class="pl">ISBN:</span>.*?<br/>', html)
        if isbn:
            isbn = isbn[0][29:-5]
        else:
            isbn = ''

        queue_book.put([book_name, author, pub_firm, pub_time, page_num, price, isbn])
