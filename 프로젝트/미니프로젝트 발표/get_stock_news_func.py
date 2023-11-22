import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


def get_link_date():
    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    # LG 에너지 솔루션
    raw_list = []
    link_list = []    # LG 엔솔 뉴스 (한페이지 당) 10개 full link 리스트
    title_list = []   # LG 엔솔 뉴스 제목 10개 리스트
    date_list = []    # LG 엔솔 뉴스 10개 날짜 시간 리스트    
    
    for i in tqdm(range(1, 250)):

        base_url = f"https://finance.naver.com/item/news_news.naver?code=373220&page={i}&sm=title_entity_id.basic&clusterId="
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' 

    
    
        response = requests.get(base_url, headers={"User-Agent":user_agent})
        if response.status_code == 200:
#             print("잘연결")
            soup = BeautifulSoup(response.text)
            tag_list = soup.select("body>div>table>tbody>tr>td.title>a")
            date_raw_list = soup.select("body > div > table> tbody > tr > td.date")
            # print(tag_list)
            # print(date_raw_list)

            for tag in tag_list:
                raw_list.append(tag.get("href"))
                title_list.append(tag.get_text())   # title 이 길어질 경우 ...해결 
            for d in date_raw_list:
                date_list.append(d.get_text())

#             print(date_list)
            # print(raw_list)   # 1번 페이지 10개 제목 일부 링크 리스트
            # print(len(raw_list))
#             print(title_list)

        else:
            print("문제 발생")
            
    for link in raw_list:
        if "/item/news_read.naver?" in link:
            link_list.append('https://finance.naver.com'+link)
# #            print(link_list)   # page 1 full link 10개 리스트       


    

    
    contents_list = []
    for link in tqdm(link_list):
        url = link
        response = requests.get(url, headers = {"User-Agent":user_agent})
        try:
            txt = response.text
            soup = BeautifulSoup(txt, 'lxml')

            soup2 = soup.find('div', attrs={"class":"scr01"})
            soup3 = soup2.select('div')[0].text
            result = soup2.text.strip().replace(soup3, "")
            contents_list.append(result)
        except:
            if soup2:
                contents_list.append(soup2.text)
            else:
                contents_list.append("NaN")
            
    data = pd.DataFrame({"date":date_list,
              "links":link_list,
              "titles":title_list,
              "contents":contents_list})
    data = data.drop_duplicates(subset='contents')
    data.reset_index(drop=True)
    data.to_csv('stock_news.csv')
        
    return data
