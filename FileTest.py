import fileinput
import queue

lst = []
q = queue.Queue(maxsize=0)

for line in fileinput.input("id.txt"):
    line = line.strip('\n')
    lst.append(line)
    q.put(line)

print(lst)
print('我是分割线------------------')
while not q.empty():
    a = q.get()
    print(a)
    print(a in lst)
    print(type(a))


