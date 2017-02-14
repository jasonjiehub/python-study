a = 2
b = 3
if a == 1:
    print('1')
elif a == 2 and b == 3:
    print(2)
else:
    print('3')

assert a > 1
c = 10
while c > 0:
    print(c)
    c -= 1

for number in range(1, 5):
    print(number)

print([x*x for x in range(10) if x % 2 == 0])


