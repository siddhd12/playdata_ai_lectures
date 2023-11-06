

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
url ="https://finance.naver.com/sise/sise_market_sum.naver"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36' 

def get_stock_list():
    # 요청 
    response = requests.get(url, headers = {"User-Agent":user_agent})
    # 상태 코드 200 확인
    if response.status.code == 200: # 정상 응답 확인하기
        print("정상 상태 코드 확인", response.status_code)
        # 요청 받아온거 뷰티풀 소프에 저장 -> 파싱하기 위해
        soup = BeautifulSoup(response.text, 'lxml')
        tag_list = soup.select("#contentarea > div.box_type_l > table.type_2")
        print(len(tag_list))
    return print(len(tag_list))
