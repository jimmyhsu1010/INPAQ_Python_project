
import random
# x = random.sample(range(10000), k=30)

x = [1, 2, 4, 5, 6, 8, 7, 9, 3]

# for i in range(len(x)-1, -1, -1): # 升冪
#     for j in range(len(x)-1, -1, -1):
#         if x[j] < x[i]:
#             x[j], x[i] = x[i], x[j]

for i in range(len(x)): # 降冪
    for j in range(len(x)):
        if x[i] > x[j]:
            x[i], x[j] = x[j], x[i]


print(x)


