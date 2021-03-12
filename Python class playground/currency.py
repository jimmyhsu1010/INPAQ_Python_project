
class Currency:
    rates = {
        "USD": 1,
        "NTD": 30
    }

    def __init__(self, symbol, amount):
        self.symbol = symbol
        self.amount = amount

    '''
    顯示的是 Python 中表示物件的標準輸出，並不夠直覺，
    我們希望 print(c1) 時，能夠看到 USD $10 之類的資訊，
    該怎麼做呢？可以使用 __repr__() 方法
    '''

    def __repr__(self):
        return "{} ${:.2f}".format(self.symbol, self.amount)

    '''
    接著定義類別內提供匯率資訊與轉換方法，就能讓貨幣自行換成他國貨幣
    '''

    def convert(self, symbol):
        new_amount = (self.amount * self.rates[symbol]) / self.rates[self.symbol]
        return Currency(symbol, new_amount) # 要繼續使用__repr__就要丟回去Currency。

    '''
    不同會比加總和比較大小，需要定義__add__()和__ge__()
    '''

    def __add__(self, other):
        new_amount = self.amount + other.convert(self.symbol).amount
        return Currency(self.symbol, new_amount)

    def __gt__(self, other): # "gt" 代表 "greater than"
        return self.amount > other.convert(self.symbol).amount