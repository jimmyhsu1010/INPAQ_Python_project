
import random
x = []

while len(x) <= 10:
    x.append(random.randint(0, 30))

for i in range(len(x)-1, -1, -1):
    for j in range(len(x)-1, -1, -1):
        if x[j] < x[i]:
            x[j], x[i] = x[i], x[j]


print(x)


