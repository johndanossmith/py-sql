from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

driver = webdriver.Chrome()
driver.get('https://www.autoscout24.com/lst/porsche/911?atype=C&cy=NL&desc=0&page=1&search_id=k2li2zd3xg&sort=standard&source=listpage_pagination&ustate=N%2CU')

accept_button = driver.find_element("xpath", "//button[@class='_consent-accept_1i5cd_111']")
accept_button.click()

with open("detail.sql", "a") as f:
    f.write("CREATE TABLE Details (id INT, URL varchar(255), ImgURL varchar(255), Title varchar(255), Brand varchar(255), Model varchar(255), Price varchar(255), Mileage varchar(255), Year varchar(255), Horsepower varchar(255), Fuel varchar(255), Color varchar(255), Origincolor varchar(255), Paint varchar(255), SellerName varchar(255), SellerPhone varchar(255));\n")

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

    with open("detail.sql", "a") as f:
        for article in articles:
            j += 1
            detail_URL = 'https://www.autoscout24.com/'+article["href"] 
            print(detail_URL)
            detailpage = requests.get(detail_URL)
            soupdetail = BeautifulSoup( detailpage.content , 'html.parser')
            picture = soupdetail.find("picture", class_="ImageWithBadge_picture__n6hct")
            if picture == None:
                carimg = soupdetail.find("img", class_="image-gallery-thumbnail-image")
                carimgurl = carimg['src']
            else: 
                carimg = picture.find('img')
                carimgurl = carimg['src']
            print(carimgurl)
            title = soupdetail.find('title')
            if title == None:
                titletext = carimg['alt']
            else:
                titletext = title.text
                titletext = titletext.replace("'", "")
            print(titletext)
            brand = soupdetail.find('div', class_ = "CommonComponents_nameContainer__3Z_zp")
            if brand == None:
                brandtext = str(None)
            else: brandtext = brand.text
            brandtext = brandtext.replace("'", "")
            print(brandtext)
            model = soupdetail.find('span', class_ = "StageTitle_model__pG_6i StageTitle_boldClassifiedInfo__L7JmO")
            modeltext = model.text
            print(modeltext)
            price = soupdetail.find("span", class_ = "PriceInfo_price__JPzpT")
            pricetext = price.text
            print(pricetext)
            mileage = soupdetail.find("div", class_ = "Carpass_carpassLink__j821i")
            if mileage == None:
                mileagetext = str(None)
                yeartext = str(None)
                horsepowertext = str(None)
                fueltext = str(None)
                colortext = str(None)
                origincolor = str(None)
                painttext = str(None)
            else: 
                mileagetext = mileage.text
                print(mileagetext)
                year = mileage.find_next("dd", class_="DataGrid_defaultDdStyle__29SKf DataGrid_fontBold__r__dO")
                yeartext = year.text
                print(yeartext)
                power = year.find_next("section", class_="DetailsSection_container__kJAVE DetailsSection_breakElement__ODImO")
                horsepower = power.find_next("dd", class_="DataGrid_defaultDdStyle__29SKf DataGrid_fontBold__r__dO")
                horsepowertext = horsepower.text
                print(horsepowertext)
                fu = horsepower.find_next("section", class_ = "DetailsSection_container__kJAVE DetailsSection_breakElement__ODImO")
                fuel = fu.find_next("dd", class_="DataGrid_defaultDdStyle__29SKf DataGrid_fontBold__r__dO")
                fueltext = fuel.text
                print(fueltext)
                col = fuel.find_next("section", class_ = "DetailsSection_container__kJAVE DetailsSection_breakElement__ODImO")
                color = col.find_next("dd", class_="DataGrid_defaultDdStyle__29SKf DataGrid_fontBold__r__dO")
                colortext = color.text
                print(colortext)
                origin = color.find_next("dd", class_="DataGrid_defaultDdStyle__29SKf DataGrid_fontBold__r__dO")
                if origin == None:
                    origincolor = str(None)
                else: origincolor = origin.text
                origincolor = origin.text
                print(origincolor)
                paint = origin.find_next("dd", class_="DataGrid_defaultDdStyle__29SKf DataGrid_fontBold__r__dO")
                if paint == None:
                    painttext = str(None)
                else: painttext = paint.text
                print(painttext)
            seller = soupdetail.find("span", class_="Contact_contactName__MFXhS")
            if seller == None:
                sellername = str(None)
            else: sellername = seller.text
            print(sellername)
            phone = soupdetail.find("a", class_="scr-link Contact_link__hRROM")
            if phone == None:
                sellerphone = str(None)
            else: sellerphone = phone.text
            print(sellerphone)
            f.write("INSERT INTO Details (id, URL, ImgURL, Title, Brand, Model, Price, Mileage, Year, Horsepower, Fuel, Color, Origincolor, Paint, SellerName, SellerPhone) VALUES ("+str(j)+", '"+detail_URL+"', '"+carimgurl+"', '"+titletext+"', '"+brandtext+"', '"+modeltext+"', '"+pricetext+"', '"+mileagetext+"', '"+yeartext+"', '"+horsepowertext+"', '"+fueltext+"', '"+colortext+"', '"+origincolor+"', '"+painttext+"', '"+sellername+"', '"+sellerphone+"');\n")