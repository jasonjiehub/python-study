from string import Template
import string

# 格式化
form = "123%s56%s89"
lst = (4, 7)
print(form % lst)

s = Template('${data}111')
s.substitute(data='22')
print(s)

print(string.digits)
print(string.ascii_letters)
print(string.ascii_lowercase.find("cd"))

seq = ['1', '2', '3']
sep = '+'
print(sep.join(seq))
print("aDSFSDFSD".lower())
print("how are you".title())
print("1+2+3".split("+"))



