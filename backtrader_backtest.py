import backtrader as bt
import yfinance as yf

class RsiStrategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close)

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.order = self.buy()

        elif self.rsi > 70:
            self.order = self.sell()


cerebro = bt.Cerebro()  # create a "Cerebro" engine instance
cerebro.addstrategy(RsiStrategy)  # Add the trading strategy
# data = bt.feeds.YahooFinanceData(dataname="036570.KS", fromdate=datetime(2017, 1, 1), todate=datetime(2019, 12, 1))
data = bt.feeds.PandasData(dataname=yf.download('138040.KS', '2021-01-01', '2022-04-01'))

cerebro.adddata(data)
cerebro.broker.setcash(1000*10000) # 초기투자 금액
cerebro.addsizer(bt.sizers.SizerFix, stake=30) # 매매단위

print(f'Initial Portfolio Value : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.run()  # run it all
print(f'Final Portfolio Value : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.plot()  # and plot it with a sing