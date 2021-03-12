from currency import Currency

x1 = Currency("USD", 10)
x2 = Currency("NTD", 310)

print(x1.convert("NTD"))
print(x1 + x2)
x3 = Currency("NTD", 350)

print(x3 > x2)

print(x2 + x1)