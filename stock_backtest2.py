import FinanceDataReader as fdr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

#plot 한글출력
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)


#krx에서 주가 가져오기
def krx_stock(name,start_time,end_time):
    df_krx = fdr.StockListing('KRX')
    #위에 입력한 기업명을 이용해서 종목코드 가져오기
    #name = 기업명 위에서 입력
    code = df_krx[df_krx['Name']==name]['Code'].iloc[0]
    #기간 잡고 주가 가져오기
    
    stock_data = fdr.DataReader(code,start_time,end_time)
    stock_data['5일 이동평균'] = stock_data['Close'].rolling(window=5).mean()
    stock_data['20일 이동평균'] = stock_data['Close'].rolling(window=20).mean()
    stock_data['60일 이동평균'] = stock_data['Close'].rolling(window=60).mean()
    stock_data['120일 이동평균'] = stock_data['Close'].rolling(window=120).mean()
    stock_data.to_csv('./stock_data.csv')
    return stock_data

#주가 정보 이용해서 plot
# https://digital-play.tistory.com/18
def stock_plot(stock_data,name):
    plt.plot(stock_data.index,stock_data['5일 이동평균'],label = '5days')
    plt.plot(stock_data.index,stock_data['20일 이동평균'],label = '20days')
    plt.plot(stock_data.index,stock_data['60일 이동평균'],label = '60days')
    plt.plot(stock_data.index,stock_data['120일 이동평균'],label = '120days')
    #for d,p in zip(date,close_price):
    # plt.plot(d,p,':')
    #plt.xlim([ratio_data.columns[0]-0.2,2022.2])
    plt.xlabel('date')
    plt.ylabel('Y-axis')
    plt.xticks(rotation = 45)
    plt.title(name + ' 주가 이동평균')
    plt.legend()
    plt.show()
    return None




# 초기 자본금 5천만원
initial_capital = 50000000

# 매수 금액
buy_amount = initial_capital * 0.5

# 거래 비용 0.1%
transaction_cost = 0.001

# 수익률 측정
def calculate_returns(data):
    returns = data.pct_change()
    return returns

# 매수/매도 신호 생성
def generate_signals(data, buy_amount):
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0
    
    # 초기 매수
    signals.iloc[0] = 1
    signals.iloc[0] = int(buy_amount / data.iloc[0] * (1 - transaction_cost))
    
    # 매수 신호 생성
    for i in range(1, len(data)):
        if signals['signal'][i-1] == 0 and calculate_returns(data[:i])[-1] >= 0.1:
            signals['signal'][i] = 1
            signals['signal'][i] = int(buy_amount / data.iloc[i] * (1 - transaction_cost))
    
    # 매도 신호 생성
    sell_signals = []
    returns = calculate_returns(data)
    for i in range(1, len(data)):
        if returns.iloc[i] >= 0.05 and (i == len(data)-1 or returns.iloc[i+1] < 0.05):
            sell_signals.append(i)
    
    for sell_signal in sell_signals:
        signals['signal'][sell_signal] = -1
        signals['signal'][sell_signal] = int(signals['signal'][sell_signal-1] * (1 - transaction_cost))
    
    return signals

# 수익 계산
def calculate_profit(data, signals):
    positions = pd.DataFrame(index=data.index).fillna(0.0)
    positions['positions'] = signals['signal'].cumsum()
    
    portfolio = pd

def stock_backtest(stock_data,name,start_time): # backtest??
    
    start = 50000000
    buy = start//stock_data.iloc[0]['Close']
    cash = start - buy * stock_data.iloc[0]['Close']

    now = buy * stock_data.iloc[-1]['Close']
    #print(stock_data.iloc[-1]['Close']) 맞는값 확인
    now_cash = cash + now
    result = ((now_cash - start)/start * 100).round(2)
    return result
'''
def stock_backtest_2(stock_data):
    stock_data_change_ACC = 1
    #누적수익률은 곱셈으로 계산되어져야 한다.
    stock_data_change_ACC = (1+stock_data['Change']).cumprod()-1
    print(stock_data_change_ACC)
    return stock_data_change_ACC
'''

def main():
    # https://finance.naver.com/sise/
    print('--- 주가 가져와서 이동평균 그래프 그리기, backtest ---')
    name = input('기업명 입력하기 : ')     #종목명 입력
    start_year = int(input('몇 년도 자료부터 가져올지, 너무 오래된것 x : '))
    start_month = int(input('시작 월 : '))
    start_day = int(input('시작일 : '))
    start_time = datetime.date(start_year,start_month,start_day)

    end_year = int(input('끝나는 년도 : '))
    end_month = int(input('월 : '))
    end_day = int(input('일 : '))
    end_time = datetime.date(end_year,end_month,end_day)
  
    stock_data = krx_stock(name,start_time,end_time)
    print(stock_data.head())
    stock_plot(stock_data,name) #주가 이동평균 그래프
    print('백테스트 결과 : ',stock_backtest(stock_data,name,start_time)) #backtest

    #stock_backtest_2(stock_data)


    return None

if __name__ =='__main__':
    main()