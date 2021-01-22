import douban_book
import douban_movie
import time


if __name__ == '__main__':
    time_begin = time.time()
    #douban_movie.movie_get_msg()
    time_movie = time.time()
    print('movie_get finished,using time ', int(time_movie - time_begin), ' s')
    douban_book.book()
    time_book = time.time()
    print('book_get finished,using time ', int(time_book - time_movie), ' s')
