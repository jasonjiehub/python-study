import threading
import time

lock = threading.Lock()

def print_time(threadName, delay, counter):
    lock.acquire()
    while counter:
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1
    lock.release()

class myThread(threading.Thread):
    def __init__(self, threadId, name, counter):
        # 覆写构造函数时需要调用父类的构造函数
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.counter = counter

    def run(self):
        print('开始线程：' + self.name)
        print_time(self.name, 5, self.counter)
        print('退出线程: ' + self.name)

# 创建线程
thread1 = myThread(1, 'Thread-1', 5)
thread2 = myThread(2, 'Thread-2', 5)

# 开启线程
thread1.start()
thread2.start()

print('main over')

