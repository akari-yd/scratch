import requests
import re
import json
import file
from queue import Queue
# import random
from mult_thread import mul_thread
import ip


# url:the url of the web,return response for ok  or empty for error


def gethtml(url):
    ip_pool = ip.pool()
    user_agent = ip_pool.user_agent()
    headers = {'Host': 'movie.douban.com',
               'User-Agent': user_agent}
    try:
        r = requests.get(url, timeout=30, headers=headers)#, proxy=ip_pool.ip)  # ,proxies={'https':ran})
        r.encoding = 'utf-8'
        r.raise_for_status()
        return r
    except:
        return ''


# url :the url of the web  return the aim message of the url
def get_movie(url):
    response = gethtml(url)
    if response:
        name = re.findall(r'name=\"title\" value=\".+?\"', response.text)
        if name:
            name = name[0][20:-1]
        else:
            name = ' '

        rating_value = re.findall(r'"ratingValue": "\d\.\d"', response.text)
        if rating_value:
            rating_value = rating_value[0][-4:-1]
        else:
            rating_value = ' '

        votes = re.findall(r'v:votes">\d+?</span>', response.text)
        if votes:
            votes = votes[0][9:-7]
        else:
            votes = ' '

        data_get = re.findall(r'\d+-\d+-\d+', response.text)
        if data_get:
            data = re.sub('-', '', data_get[0])
        else:
            data = ' '

        percent = re.findall(r'\d{1,2}\.\d%', response.text)[:5]

        language = re.findall(r'语言:</span> .+?<br/>', response.text)
        if language:
            language = language[0][11:-5]
        else:
            language = ' '

        length = re.findall(r'\d+分钟</span>', response.text)
        if length:
            length = length[0][:-7]
        else:
            length = ' '

        msg = [name, language, length, rating_value, votes, data] + percent
        return msg
    else:
        return []


# the total function of the mode
def movie_get_msg(type_='movie'):
    tag_url = 'https://movie.douban.com/j/search_tags?type=' + type_ + '&source='
    response_tag = gethtml(tag_url)
    if response_tag:
        data_tag = json.loads(response_tag.text)
        # tags=data_tag['tags']
        # sorts=['recommend','time','rank']
        depth = 20
        count = 0
        head_url = 'https://movie.douban.com/j/search_subjects?type=' + type_ + '&tag='
        tag = '热门'
        sort_url = '&sort='
        sort = 'recommend'
        page_url = '&page_limit=20&page_start='
        # page_start='0'
        queue_m = Queue()
        queue_out = Queue()
        msg = [['序号', '名称', '语言', '时长', '评分', '评价人数', '上映时间',
                '五星占比', '四星占比', '三星占比', '二星占比', '一星占比']]
        for i in range(depth):
            page_start = str(20 * i)
            start_url = head_url + tag + sort_url + sort + page_url + page_start
            response = gethtml(start_url)
            if response:
                data = json.loads(response.text)
                movies = data['subjects']
                for movie in movies:
                    count = count + 1
                    queue_m.put([count, movie['url']])
            else:
                print('number:', count, ' ERROR!')
        thread_num = 20
        thread = mul_thread(thread_num, per_thread, (queue_m, queue_out))
        thread.start()
        thread.join()
        while queue_out.empty() is not True:
            movie = queue_out.get()
            if int(movie[0]) > count:
                msg.append(movie)
            else:
                msg.insert(int(movie[0]), movie)
        file_name = tag + '-' + type_ + '.xlsx'
        file.filesave(file_name, msg)
        for tag in msg[0]:
            file.sortxlsx(file_name, tag, 0)
    else:
        print('GETTING TAG ERROR!')


def per_thread(queue_m, queue_out):
    while queue_m.empty() is not True:
        movie = queue_m.get()
        msg_movie = get_movie(movie[1])
        if msg_movie:
            queue_out.put([str(movie[0])] + msg_movie)


def main():
    movie_get_msg()
