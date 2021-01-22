from threading import Thread


class mul_thread(object):
    def __init__(self, num, target, args):
        self.num = num
        self.thread = []
        for i in range(num):
            self.thread.append(Thread(target=target, args=args))
            self.thread[i].setDaemon(True)

    def start(self):
        for i in range(self.num):
            self.thread[i].start()

    def join(self):
        for i in range(self.num):
            self.thread[i].join()



