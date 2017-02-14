import threading
import time


def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1


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
thread1 = myThread(1, 'Thread-1', 1)
thread2 = myThread(2, 'Thread-2', 2)

# 开启线程
thread1.start()
thread2.start()

# 在线程thread1上调用无参join方法，则当前线程(main)会等待thread1执行完之后才继续执行
# 在线程thread2上调用有参join方法，传入一个整数3，则说明当前线程会等待thread2三秒，三秒后，当前线程会继续执行(也是和其他线程交替执行)
thread1.join()
thread2.join(3)

print('main over')

