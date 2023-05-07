
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import FinanceDataReader as fdr
import requests

#plot 한글출력
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# 기업명에서 종목코드 가져오기
def name_to_code(name):
  df_krx = fdr.StockListing('KRX')
  code = df_krx[df_krx['Name']==name]['Code'].iloc[0]
  return code

# https://seong6496.tistory.com/156
def data_from_requests(name):
    URL = f"https://finance.naver.com/item/main.naver?code={name}"
    r = requests.get(URL)
    df = pd.read_html(r.text)[3]

    df.set_index(df.columns[0],inplace=True)
    df.index.rename('주요재무정보',inplace=True)
    df.columns = df.columns.droplevel(2)
    #df = df.fillna(0)

    annual_date = pd.DataFrame(df).xs('최근 연간 실적',axis=1)
    #quater_date = pd.DataFrame(df).xs('최근 분기 실적',axis=1)

    annual_date.to_csv('a.csv')
    return annual_date


#비율분석 이용하여 그래프 그리기
def ratio_plot_requests(name,ratio_data):
    ratio_data = ratio_data.drop(['매출액','영업이익','당기순이익','유보율','주당배당금(원)','시가배당률(%)','배당성향(%)'])
    ratio_data = ratio_data.drop(['EPS(원)','BPS(원)']) #그래프 그리기 힘들어서
    ratio_data = ratio_data.drop(['당좌비율']) # 키움증권 당좌비율 정보 x
    ratio_data = ratio_data.astype(np.float64)
    for tmp in ratio_data.index:
        #print(ratio_data.loc[tmp])
        plt.scatter(ratio_data.columns,ratio_data.loc[tmp],marker='o',label=tmp)
        for y,tmp2 in zip(ratio_data.columns,ratio_data.loc[tmp]):
            plt.text(y,tmp2,tmp2,
                    fontsize = 12,
                    color = 'black',
                    horizontalalignment = 'center',
                    verticalalignment = 'top'
                    )
        plt.plot(ratio_data.columns,ratio_data.loc[tmp],':')
    plt.legend(loc = 'best', frameon=False, fontsize = 8)
    #plt.xlim([ratio_data.columns[0]-0.2,2022.2])
    #plt.xticks([i for i in range(ratio_data.columns[0],2023)])
    #plt.figure(figsize=(6,8))
    plt.xlabel('년')
    plt.ylabel('Y-axis')
    plt.yscale('symlog')
    plt.title(name + ' 재무비율분석')
    plt.show()
    return None 

def H_test():
    for year in range(2000, 2020):
    buy_month = str(year) + '-11'
    sell_month = str(year+1) + '-04'
    print(buy_month, sell_month)


def main():
    print(' --- 재무재표 정보 가져와서 비율분석, 그래프 --- ')
    name = input('기업명 입력하기 (이름 중복되는경우 dart에서 종목코드 찾아서 입력) : ')     #종목명 입력
    code = name_to_code(name)
    #start_year = int(input('몇 년도 자료부터 가져올지, 너무 오래된것 x : '))

    ratio_data = data_from_requests(code)  #비율분석
    print(ratio_data) #비율분석 결과 표 출력
    ratio_plot_requests(name,ratio_data)          #비율분석 그래프 그리기
    ratio_data.to_csv(name +'_비율분석_fromNaver.csv')
    return None

if __name__ =='__main__':
    main()