import queue
q = queue.Queue(maxsize=0)
# for i in range(100):
#     q.put(i)
#
# for i in range(100):
#     print(q.get())
q.put(0)
print(q.get())
print(q.empty())
