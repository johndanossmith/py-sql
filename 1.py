from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

# driver = webdriver.Chrome()
# driver.get('https://www.autoscout24.com/lst/porsche/911?atype=C&cy=NL&desc=0&page=1&search_id=k2li2zd3xg&sort=standard&source=listpage_pagination&ustate=N%2CU')

# accept_button = driver.find_element("xpath", "//button[@class='_consent-accept_1i5cd_111']")
# accept_button.click()

with open("url.sql", "a") as f:
    f.write("CREATE TABLE URLs (id INT, Urlname varchar(255));\n")
    
URL = 'https://www.autoscout24.com/lst/porsche/911?atype=C&cy=NL&desc=0&page=1&search_id=k2li2zd3xg&sort=standard&source=listpage_pagination&ustate=N%2CU'
page = requests.get(URL)
soup = BeautifulSoup( page.content , 'html.parser')

paginations = soup.find_all("li", class_ = "pagination-item")
for pagination in paginations:
    num = pagination.text
    
j = 0
for i in range(int(num)):
    URL = 'https://www.autoscout24.com/lst/porsche/911?atype=C&cy=NL&desc=0&page='+str(i+1)+'&search_id=k2li2zd3xg&sort=standard&source=listpage_pagination&ustate=N%2CU'
    page = requests.get(URL)
    soup = BeautifulSoup( page.content , 'html.parser')
    articles = soup.find_all("a", class_ = "ListItem_title__znV2I ListItem_title_new_design__lYiAv Link_link__pjU1l")

    with open("url.sql", "a") as f:
        for article in articles:
            j += 1
            detail_URL = 'https://www.autoscout24.com/'+article["href"]
            f.write("INSERT INTO URLs (id, Urlname) VALUES ("+str(j)+", '"+detail_URL+"');\n")

time.sleep(100)
