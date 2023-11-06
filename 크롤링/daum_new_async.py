# daum_news_async.py
# 뉴스 목록 csv파일에서 저장된 링크들의 뉴스들을 aiohttp를 이용해서 크롤링
import nest_asyncio
nest_asyncio.apply()
import pandas as pd
import aiohttp
from bs4 import BeautifulSoup
import time
import asyncio
async def get_news(url,session):
    async with session.get(url) as response:
        if response.status == 200:
            html = await response.text()
            soup= BeautifulSoup(html,'lxml')
            p_list= soup.select("div.article_view p")
            article = [] # 리스트에 문단(p)의 text들을 저장..
            for p in p_list:
                article.append(p.get_text())             
            # 리스트안의 문단들을 합쳐서 하나의 문자열로 만들기
            return " ".join(article) # 구분자문자열.join(리스트)      
        # url의 개별 뉴스를 크롤링 하는 코루틴 함수

async def main(links):
    #메인 루틴
    # 뉴스 링크 개수만큼 get_news() 코루틴을 생성해서 event Loop를 이용해 실행
3
    async with aiohttp.ClientSession() as sess:
        
        # 20개의 코루틴을 생성한 뒤에 event Loop에 넣어서 실행
        result = await asyncio.gather(*[get_news(link,sess)for link in links] )
        # result:리스트  -에는 20개의 뉴스기사
    return result

if __name__ == "__main__":
    # csv 파일을읽어서 DataFrame 을 생성
    df = pd.read_csv("daum_new_list_2023-04-19.csv")
    #print(df)
    links =df["link"]
    print(links)
    start = time.time()
    result = asyncio.run(main(links))
    end = time.time()
    print('걸린시간:', end-start, "초")