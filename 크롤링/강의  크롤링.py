# daum_news_async.py
# 뉴스목록 csv 파일에 저장된 링크들의 뉴스들을 aiohttp를 이용해서 크롤링.

import pandas as pd
import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def get_news(url, session):
    # url의 개별 뉴스를 크롤링 하는 코루틴 함수.
    # 연결 요청
    async with session.get(url) as response:
        if response.status == 200:
            html = await response.text()
            soup = BeautifulSoup(html, "lxml")
            p_list = soup.select("div.article_view p")

            article = [] # 리스트에 문단(p)의 text들을 저장.
            for p in p_list:
                article.append(p.get_text())
            # 리스트안의 문단들을 합쳐서 하나의 문자열로 만들기.
            return "\n\n".join(article)  # 구분자문자열.join(리스트
   

async def main(links):
    # 메인루틴
    # 뉴스 링크 개수만큼 get_news() 코루틴을 생성해서 event loop 를 이용해 실행.
    
    async with aiohttp.ClientSession() as sess:
        # 20개의 코루틴을 생성한 뒤에 event loop에 넣어서 실행.
        result = await asyncio.gather(*[get_news(link, sess) for link in links])
        #result:리스트 - 에는 20개의 뉴스기사.
        print(type(result))
    return result


if __name__ == "__main__":
    import time
    # csv 파일을 읽어서 DataFrame을 생성
    df = pd.read_csv("daum_new_list_2023-04-19.csv")
    # print(df)
    links = df["link"] # link 컬럼의 값들을 조회
    # print(links)
    
    start = time.time()
    result = asyncio.run(main(links))
    end = time.time()
    print('걸린시간:', end-start, "초")

=====================
    
    
base_url = 'https://www.macmillandictionary.com/us/dictionary/american/{keyword}'
keywords = ['hi', 'apple', 'banana', 'call', 'feel',
            'hello', 'bye', 'like', 'love', 'environmental',
            'buzz', 'ambition', 'determine'] 

==========================================

# english_word_search_async.py
########################
#import 
##########################


async def get_word(url, session):
    pass


async def main(url_list):
    pass

if __name__ == '__main__':
        

    base_url = 'https://www.macmillandictionary.com/us/dictionary/american/{keyword}'
    keywords = ['hi', 'apple', 'banana', 'call', 'feel',
                'hello', 'bye', 'like', 'love', 'environmental',
                'buzz', 'ambition', 'determine'] 
    url_list = [base_url.format(word) for word in keywords]

    main(url_list)








