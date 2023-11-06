
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
url = "https://news.daum.net"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'

def get_news_list():
    """
    daum 뉴스 목록 조회
    조회결과는 pandas의 DataFrame(표) 로 만들어서 반환.
    """
    # 요청
    response = requests.get(url, headers={'User-Agent':user_agent})
    # 상태코드가 200 인지 확인.
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        tag_list = soup.select("ul.list_newsissue > li strong > a")
        print(len(tag_list))
        link_list = []
        title_list = []
        for tag in tag_list:
            link_list.append(tag.get("href"))
            title_list.append(tag.get_text().strip())
            
        return pd.DataFrame({
            "title":title_list,
            "link":link_list
        })
    else:
        print("문제발생:", response.status_code)
def get_news(url):
    # news 상세 기사 url을 받아서 뉴스 내용을 반환
    # 연결
    response = requests.get(url,headers={"user_agent":user_agent})      
    if response.status_code == 200:
        soup = BeautifulSoup(response.text,"lxml")
        p_list= soup.select("div.article_view p")

        article = [] # 리스트에 문단(p)의 text들을 저장..
        for p in p_list:
            article.append(p.get_text())             
        # 리스트안의 문단들을 합쳐서 하나의 문자열로 만들기
        return " ".join(article) # 구분자문자열.join(리스트) 
["123", "456"]  123  456 
if __name__ =="__main__":
        # 뉴스 목록을 저장
        from datetime import datetime
        import os
        import time
        ###############################################################################################
        # 뉴스 목록 가져 오기 
        ###############################################################################################

        d=datetime.now().strftime("%Y-%m-%d") # strftime(): 날짜 시간을 원하는형태의 문자열로 변환
        file_path = f"daum_new_list_{d}.csv"
        print(file_path)
        result=get_news_list()
        # # csv 파일로 저장
        result.to_csv(file_path, index = False)  # utf-8형태로 저장    
        ###############################################################################################
        # 개별 뉴스들의 기사를 저장.
        ###############################################################################################
        # result: DataFrame(표)에서 링크 조회
        links =result["link"]  # 표["컬럼이름"] => 컬럼의 값들(행)을 반환
        start = time.time()
        result_news= [get_news(link) for link in links]
        end = time.time()
        print("개별 뉴스 기사 가져오는데 걸린시간",end-start,"초")
        
        # print(len(result_news))
        # print(result_news)
        # 날짜이름으로 news/디렉토리를 생성
        save_path = f"news/{d}"
        os.makedirs(save_path, exist_ok = True) # 상위 디렉토리까지 생성
        titles = result["title"] # 뉴스 제목
        import re
        for title, news in zip(titles, result_news):
            title = re.sub('[^\w]','',title)
            with open(f"{save_path}/{title}.txt","wt", encoding=
            'utf-8') as fw:
                fw.write(news)

        print("완료")
