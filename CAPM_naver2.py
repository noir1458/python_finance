#저번 글에서 파이썬을 활용해서  Capm 기대수익률을 계산 했었는데, 
#자료에 결측치가 있는 경우 베타를 계산할 때 공분산 계산이 안돼서 수정을 좀 해보았다.
#수정하다가 단일 연도 베타 말고 시계열로 연속되는 베타를 구하고 싶어져서 연도별로 반복해서 베타를 구하는 식을 추가했다.
import FinanceDataReader as fdr
import numpy as np
import datetime
import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
Years = [2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]
s_date = datetime.datetime(2008,1,1)
e_date = datetime.datetime(2008,12,31)
s_market = 'KS11'
C_list = ["005930","035420","005380","034220","017670",'000660','051910','008350','005610','009410','005180','001060','073240','004490']
def Beta(x):
    market = fdr.DataReader(s_market , s_date , e_date)["Close"]
    market_df = pd.DataFrame({'market':np.log(market / market.shift(1))})  
    ticker_close = fdr.DataReader(x,s_date,e_date)["Close"]
    ticker_df = pd.DataFrame({'ticker':np.log(ticker_close / ticker_close.shift(1)).dropna()})
    Df = pd.concat([market_df, ticker_df], axis=1) 
    # 결측치가 있는 경우 자료 크기가 서로 달라서 공분산 계산이 안된다. 그래서 일단 하나의 데이터 프레임으로 묶고,
    Df = Df.dropna(how = 'any')
    # 두 자료에서 하나라도 Nan 값이 있는 경우 행을 탈락시켜서 자료 크기를 맞춰줬다.
    beta = (np.cov(Df['ticker'],Df['market'])/np.var(Df['market']))[0,1]
    # 두 자료를 하나의 데이터 프레임으로 묶었으니까 데이터를 불러올 때는 칼럼으로 불러와 준다.
    return beta

def geomean(x):
    geomean = 1
    for i in x:
        geomean = geomean*i
    geomean = geomean ** (1/len(x))
    return geomean

def Er(x):
    beta = Beta(x)
    eri = Mrf + beta*Rp
    return eri
    
Rf = fdr.DataReader('FRED:DGS3',s_date,e_date)
Mr = fdr.DataReader('KS11',s_date,e_date)['Close'][1:]
Mrf = geomean(Rf['DGS3'])  #무위험 수익률 
Mmr = (Mr[-1]/Mr[0]-1)*100 # 시장 수익률
Rp = Mmr - Mrf             # 위험프리미엄 = 시장수익률 - 무위험 수익률
# 베타와 기대수익률을 연도별로 연속해서 구해보았다. (임시저장)

def BE_series(i) :
    BE_df = pd.DataFrame(columns = ['beta', 'Er'])
    for x in Years:
        s_date = datetime.datetime(x,1,1)
        e_date = datetime.datetime(x,12,31)
        BE_df.loc[x] = [Beta(i), [Er(i)]]  
    return BE_df
