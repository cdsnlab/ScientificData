import json

a = ("abc", "def")
b = ("qwe", "asd")
c = ("iop", "iop")

l = []
for i in range(10):
    l.append(a)

for i in range(10):
    l.append(b)
    for j in range(10):
        l.append(c)

pairs = list(set(l))
result = list(map(lambda x: (x[0], x[1], l.count(x)), pairs))
print(result)