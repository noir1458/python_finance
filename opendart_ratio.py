
# https://dart.fss.or.kr/ 가입하고 키 발급받아서 넣기
api_key = 'xxxxxxxxxxxxxxx'

#!pip install OpenDartReader
#!pip install --upgrade opendartreader
# https://github.com/FinanceData/OpenDartReader
import numpy as np
import pandas as pd
import OpenDartReader
import matplotlib.pyplot as plt
import FinanceDataReader as fdr

#plot 한글출력
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# dart에서 정보 가져오기
dart = OpenDartReader(api_key)
  
#df_2020 = dart.finstate(name, 2020,'11011')
#df_2021 = dart.finstate(name, 2021,'11011')
#df_2022 = dart.finstate(name, 2022,'11011')
#df_2020.to_csv(str(name) +'_finstate_2020.csv')
#df_2021.to_csv(str(name) +'_finstate_2021.csv')
#df_2022.to_csv(str(name) +'_finstate_2022.csv')
# <- 폴더모양 클릭하면 csv 파일 확인 가능하다

# 기업명에서 종목코드 가져오기
def name_to_code(name):
  df_krx = fdr.StockListing('KRX')
  code = df_krx[df_krx['Name']==name]['Code'].iloc[0]
  return code

# 표에서 CFS, 연결재무재표(CFS) 라고 되어있는걸로 하기, 연결재무재표를 써야 종속기업 실적이 포함된다고 한다.
# 자본금 indexerror 생길때 자본금 = 0 으로 처리함
# 이름과 년도가 주어졌을때 재무재표 정보 가져오기
def data_from_finstate(name,year):
  use = dart.finstate(name, year,'11011')
  use.to_csv(str(name) +'_finstate_' +str(year)+'.csv')
  세전이익 = float(use.loc[(use['account_nm']== '법인세차감전 순이익') & (use['fs_div']=='CFS')]['thstrm_amount'].values[0].replace(',',''))
  매출액 = float(use.loc[(use['account_nm']== '매출액') & (use['fs_div']=='CFS')]['thstrm_amount'].values[0].replace(',',''))
  #총자산의평균값 = 0
  자산총계 = float(use.loc[(use['account_nm']== '자산총계') & (use['fs_div']=='CFS')]['thstrm_amount'].values[0].replace(',',''))
  당기순이익 = float(use.loc[(use['account_nm']== '당기순이익') & (use['fs_div']=='CFS')]['thstrm_amount'].values[0].replace(',',''))
  이익잉여금 = float(use.loc[(use['account_nm']== '이익잉여금') & (use['fs_div']=='CFS')]['thstrm_amount'].values[0].replace(',',''))
  #매출채권평균값 = 0
  #재고자산평균값 = 0
  #총자산평균값 = 0
  try:
    자본금 = float(use.loc[(use['account_nm']== '자본금') & (use['fs_div']=='CFS')]['thstrm_amount'].values[0].replace(',',''))
  except IndexError:
    자본금 = 0
  자본총계 = float(use.loc[(use['account_nm']== '자본총계') & (use['fs_div']=='CFS')]['thstrm_amount'].values[0].replace(',',''))
  부채총계 = float(use.loc[(use['account_nm']== '부채총계') & (use['fs_div']=='CFS')]['thstrm_amount'].values[0].replace(',',''))

  유동자산 = float(use.loc[(use['account_nm']== '유동자산') & (use['fs_div']=='CFS')]['thstrm_amount'].values[0].replace(',',''))
  비유동자산 = float(use.loc[(use['account_nm']== '비유동자산') & (use['fs_div']=='CFS')]['thstrm_amount'].values[0].replace(',',''))
  유동부채 = float(use.loc[(use['account_nm']== '유동부채') & (use['fs_div']=='CFS')]['thstrm_amount'].values[0].replace(',',''))
  비유동부채 = float(use.loc[(use['account_nm']== '비유동부채') & (use['fs_div']=='CFS')]['thstrm_amount'].values[0].replace(',',''))
  result = [세전이익,매출액,자산총계,당기순이익,이익잉여금,자본금,자본총계,부채총계,유동자산,비유동자산,유동부채,비유동부채]
  return result

#정보 이용해서 재무비율분석
def ratio_from_data(name,year):
  #0 세전이익,1 매출액,2 자산총계,3 당기순이익,4 이익잉여금,5 자본금,6 자본총계,7 부채총계,8 유동자산,9 비유동자산,10 유동부채,11 비유동부채 = data_from_finstate_2022
  r0 = data_from_finstate(name,year)
  r1 = data_from_finstate(name,year-1)
  #부채비율 = 자본총계/자산총계
  #유동비율 = 유동자산/유동부채
  #ROA = 당기순이익/자산총계
  #ROE = 당기순이익/ ((전기자본총계 + 당기자본총계)/2)
  #ROS = 세전이익/매출액

  부채비율 = r1[6]/(r1[8]+r1[9])
  유동비율 = r1[8]/r1[10]
  ROA = r1[3]/r1[2] * 100
  ROE = r1[3]/((r1[6]+r0[6])/2) * 100
  ROS = r1[0]/r1[1] * 100
  result = [부채비율,유동비율,ROA,ROE,ROS]
  return result

#시작년도를 입력받아서 최근까지 비율분석하기, DataFrame으로 내보냄
def start_ratio(name,start_year):
  ratio_data = pd.DataFrame([],index = ['부채비율','유동비율','ROA','ROE','ROS'])
  for k in range(start_year,2023):
    add_sr = pd.Series(ratio_from_data(name,k),index = ['부채비율','유동비율','ROA','ROE','ROS'],name = k)
    ratio_data = pd.concat([ratio_data,add_sr],axis=1)
  ratio_data = ratio_data.round(2) #반올림
  return ratio_data


#비율분석 이용하여 그래프 그리기
def ratio_plot(name,ratio_data):
  for tmp in ratio_data.index:
    #print(ratio_data.loc[tmp])
    plt.scatter(ratio_data.columns,ratio_data.loc[tmp],marker='x',label=tmp)
    for y,tmp2 in zip(ratio_data.columns,ratio_data.loc[tmp]):
      plt.text(y,tmp2,tmp2,
              fontsize = 12,
              color = 'black',
              horizontalalignment = 'center',
              verticalalignment = 'top'
              )
    plt.plot(ratio_data.columns,ratio_data.loc[tmp],':')
    plt.legend()
  plt.xlim([ratio_data.columns[0]-0.2,2022.2])
  plt.xticks([i for i in range(ratio_data.columns[0],2023)])
  plt.xlabel('년')
  plt.ylabel('Y-axis')
  plt.title(name + ' 재무비율분석')
  plt.show()
  return None 


def main():
  print(' --- 재무재표 정보 가져와서 비율분석, 그래프 --- ')
  name = input('기업명 입력하기 (이름 중복되는경우 dart에서 종목코드 찾아서 입력) : ')     #종목명 입력
  if name.isdigit() == False: # 이름을 종목코드로 바꾸기
    name = name_to_code(name)
  start_year = int(input('몇 년도 자료부터 가져올지, 너무 오래된것 x : '))
  
  ratio_data = start_ratio(name,start_year)  #비율분석
  print(ratio_data) #비율분석 결과 표 출력
  ratio_plot(name,ratio_data)          #비율분석 그래프 그리기
  ratio_data.to_csv(name +'_비율분석_' + str(start_year) +'.csv')
  return None

if __name__ =='__main__':
  main()