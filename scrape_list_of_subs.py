import pandas as pd
from bs4 import *
import requests
import re


# scrape reddit list
data = []
def next_page(soup):
    x = soup.find('ul',{'class':'pager'})
    s = str(x.select('a')[1])
    for i in re.findall(r'"([^"]*)"', s):
        return(i)
link= "/top-sfw-subreddits"
i =1
while i <= 1000:
    
    url = "https://frontpagemetrics.com" + link
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('table', {'class':"table table-bordered"})
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    
    link = next_page(soup)
    i+=1

    
    
    
subreddits = pd.DataFrame(data)
subreddits.columns=['rank','Subreddits', 'Subscribers']
subreddits.to_csv("list_of_subreddits.csv")