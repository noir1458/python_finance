import FinanceDataReader as fdr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.formula.api import ols

#plot 한글출력
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# krx에서 주가 가져오기, KOSPI 지수 정보 가져와서 같이 저장
# https://ktcf.tistory.com/m/47
def krx_stock_CAPM(name,start_year):
    df_krx = fdr.StockListing('KRX')
    # 위에 입력한 기업명을 이용해서 종목코드 가져오기
    # name = 기업명 위에서 입력
    code = df_krx[df_krx['Name']==name]['Code'].iloc[0]
    # 기간 잡고 주가 가져오기
    start_krx = str(start_year) +'-01-01'
    end_krx = '2023-04-29'
    stock_data = fdr.DataReader(code,start_krx,end_krx)
    # 코스피 정보 가져오기  
    ks_df = fdr.DataReader('KS11','2000')
    #ks_df.to_csv('./ks11_data.csv')

    #코스피수익률중 현재 날짜와 겹치는부분 찾아서 주가수익률과 합쳐서 내보내기

    #stock_data.to_csv('./stock_data.csv')
    return stock_data


# 그래프 그리고 회귀분석해서 베타 찾기
def stock_plot(stock_data,name,start_year):
    with plt.style.context('seaborn'):
        sns.jointplot('SSE','KOSPI',data=ret, kind='reg')
    daily_ols = ols('SSE~1+KOSPI',data=ret).fit()
    daily_ols.summary()
    #intercept 값이 알파, 그 밑의 값이 베타가 된다
    #미완성
    return None


def main():
    # https://finance.naver.com/sise/
    print('--- 주가 가져와서 이동평균 그래프 그리기, backtest ---')
    name = input('기업명 입력하기 : ')     #종목명 입력
    start_year = int(input('몇 년도 자료부터 가져올지, 너무 오래된것 x : '))
  
    stock_data = krx_stock_CAPM(name,start_year)


    return None

if __name__ =='__main__':
    main()