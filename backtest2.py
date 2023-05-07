import FinanceDataReader as fdr
kospi = fdr.DataReader('KS11','2000')
print(kospi.head())
kospi['change'] = (kospi['Close'] - kospi['Open'])/kospi['Open'] * 100
print(kospi.head())

for year in range(2000, 2020):
    buy_month = str(year) + '-11'
    sell_month = str(year+1) + '-04'
    print(buy_month, sell_month)

누적수익률 = 1.0

for year in range(2000, 2021):
    buy_month = str(year) + '-11'
    sell_month = str(year+1) + '-04'

    매수가 = kospi[buy_month].iloc[0]['Open']      # 11월 첫 거래일 시가
    매도가 = kospi[sell_month].iloc[-1]['Close']   # 4월 마지막 거래일 종가
    수익률 = 매도가/매수가

    누적수익률 = 누적수익률 * 수익률

print(누적수익률)