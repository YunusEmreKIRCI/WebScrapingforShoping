from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import csv
#istediğiniz filtrelemeleri yaptıktan sonra gelene birinci sayfanın linki url kısmına kopylayın
url = "https://www.lcwaikiki.com/tr-TR/TR/arama?q=sweat&LastFilter=m_1007&m_1007=39597,31870,37339,30816,37812,32027,37342,30817,31696,30611,32220,37291,37473,30989&PageIndex="
uruncount = 0
all_links = []
driver = webdriver.Firefox()
bedenurunlist=[]
urunlist = {}
fotolist = [] 
l = 0  
#range sayfa sayısının 1 fazlası olmalı
for i in range (1,51):
  
    driver.get(url+str(i))
    wait = WebDriverWait(driver, 30) 
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    page = driver.page_source

    
    soup = BeautifulSoup(page, "html.parser")
    links = soup.find_all("div", attrs={"class": "product-card product-card--one-of-4"})

    for link in links: 
        l+=1
        print(l)
        print(link.find("a").get("href"))
        all_links.append({"link":"https://www.lcwaikiki.com" + link.find("a").get("href")})                    

for link in all_links:
   
    print(uruncount)
    
    driver.get(link.get("link"))
    sleep(3)
    wait = WebDriverWait(driver, 50) 
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
   
    
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    try:
        price = soup.find("span", {"class": "advanced-price"}).text
        urunkodtext = soup.find("div", {"class": "product-code"}).text
        urunkodtext1 = urunkodtext.split()[2] + urunkodtext.split()[3] + urunkodtext.split()[4] +"-01" 
        renk = urunkodtext.split()[6]
        try:
            renk = renk + " " + urunkodtext.split()[7] 
        except:
            pass
        urunad = soup.find("div", {"class": "product-title"}).text
        flink = soup.find_all("div", attrs={"class": "col-xs-6"})
        urunaciklama = soup.find("div", {"class": "panel-body"}).find("li").text
        yascins = soup.find("div", {"class": "col-md-6 option-info nopadding"}).find_all("p")
        yasgrubu = ""
        cinsiyet = ""
        for i in yascins:
            if "Cinsiyet:" in i.text:
                cinsiyet = i.text.split()[1]
                try:
                    yasgrubu = i.text.split()[2]
                except:
                    yasgrubu = "Yetişkin"
                
       
        bedenlist = soup.find("div", attrs={"class": "option-size"}).find_all("a")
        
       
        c = 0
        urunlist = {"urunkod": urunkodtext1, "urunad": urunad.strip(), "urunaciklama": urunaciklama.strip(), "beden": "" , "cinsiyet" : cinsiyet ,"yasgrubu": yasgrubu, "renk": renk, "price": price}
        for i in flink:
            try:
                s = i.find("img").get("src")
                #fotolist.append({"foto" + str(c) : s})
                urunlist["foto" + str(c)] = s
                c+=1
            except:
                c+=1
                pass
        for i in bedenlist:
            c = i.get("class")

            if c != None:
                continue
            uruncount+=1
            urunlist["beden"] = i.text
            urunekle = urunlist.copy()
            bedenurunlist.append(urunekle)
    except:
        pass

df = pd.DataFrame(bedenurunlist)
df.to_csv("links.csv", encoding='utf-8')
