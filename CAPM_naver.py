# https://blog.naver.com/hmoolung/222939547945
import FinanceDataReader as fdr
import numpy as np
import datetime
import pandas as pd
import math
# 필요한 라이브러리 도구들 소환
s_date = datetime.datetime(2023,1,1)
e_date = datetime.datetime(2023,4,30)
# 기대수익률을 구하고 싶은 기간 설정
s_market = 'KS11'
# 마켓 포트폴리오는 코스피 지수로 설정했다.
def Beta(x):
    market = fdr.DataReader(s_market , s_date , e_date)["Close"]
    market_lograte = np.log(market / market.shift(1)).dropna()
    ticker_close = fdr.DataReader(x,s_date,e_date)["Close"]
    ticker_lograte = np.log(ticker_close / ticker_close.shift(1)).dropna()
    beta = (np.cov(market_lograte,ticker_lograte)/np.var(market_lograte))[0,1]
    return beta
# 베타 = 공분산(마켓포트폴리오, 개별자산)/분산(마켓포트폴리오) 로 구했다. 간단해 보이지만 간단하게 만드는게 엄청 힘들었다..
def geomean(x):
    geomean = 1
    for i in x:
        geomean = geomean*i
    geomean = geomean ** (1/len(x))
    return geomean
# 무위험수익률 구하는데 필요한 기하평균 함수도 스윽 만들고
def Er(x):
    beta = Beta(x)
    eri = Mrf + beta*Rp
    return eri
# 마지막으로 최종 기대수익률 구하는 Capm 공식
Rf = fdr.DataReader('FRED:DGS3',s_date,e_date)
Mr = fdr.DataReader('KS11',s_date,e_date)['Close'][1:]
# 무위험수익률은 미국 3년 국채사용, 시장수익률은 역시 코스피를 사용
#Mrf = 무위험 수익률, Mmr = 시장수익률. 그냥 M붙혀서 썼다.
Mrf = geomean(Rf['DGS3'])  
# 무위험수익률 기하평균 해주고
Mmr = (Mr[-1]/Mr[0]-1)*100
 # 시장수익률은 (마지막날 코스피지수/첫날 코스피지수) 로 썼다.
Rp = Mmr - Mrf             
# 위험프리미엄 = 시장수익률 - 무위험 수익률
