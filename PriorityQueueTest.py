from queue import PriorityQueue

# PriorityQueue也是线程安全的，可用于多线程间的同步

class Job(object):
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
        print('New job:', description)
        return

    def __lt__(self, other):
        return self.priority < other.priority

q = PriorityQueue()

q.put(Job(5, 'Mid-level job'))
q.put(Job(10, 'Low-level job'))
q.put(Job(1, 'Important job'))
q.put(Job(3, 'little Important job'))

while not q.empty():
    next_job = q.get()
    print('Processing job', next_job.description)
