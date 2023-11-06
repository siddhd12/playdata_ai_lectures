import nest_asyncio
nest_asyncio.apply()
import pandas as pd
import aiohttp
from bs4 import BeautifulSoup
import time
import asyncio  



async def get_word(url,sess):
    # url 리스트 받고 비동기 
    async with sess.get(url) as response:
        # if response.status == 200:
        #     return await response.text()
        html = await response.text()
        soup = BeautifulSoup(html,'lxml')
        content_list = soup.select("div.SENSE-BODY > div.dflex.no-grow > div.SENSE-CONTENT > span")
        print("정의는",content_list)
        # article = []
        # for art in content_list:
        #     article.append(art.get_text())
            # return "".join(article)
    return content_list




async def main(url_list):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    headers = {
        "User_Agent":user_agent
    }
    # 13개 받은거 갖고와서 쓰고 
    async with aiohttp.ClientSession(headers=headers, connector=aiohttp.TCPConnector(ssl=False)) as sess:
        # 13개의 코루틴을 생성한 뒤에 event Loop에 넣어서 실행
        result = await asyncio.gather(*[get_word( url, sess)for url in url_list] )
        # result:리스트  -에는 13 개의 사전
        return result






if __name__ =="__main__":
    base_url = 'https://www.macmillandictionary.com/us/dictionary/american/{}'
    keywords = ['hi', 'apple', 'banana', 'call', 'feel',
                'hello', 'bye', 'like', 'love', 'environmental',
                'buzz', 'ambition', 'determine'] 

    url_list= [base_url.format(word) for word in keywords]
    print(url_list)
    start = time.time()
    result=asyncio.run(main(url_list))
    print(result[0])
    end = time.time()
    print('걸린시간:', end-start, "초")