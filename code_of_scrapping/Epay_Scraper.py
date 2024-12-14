from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import numpy as np
import csv
import time as t
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
url ="https://www.ebay.com/b/Cell-Phones-Smartphones/9355/bn_320094?rt=nc&LH_ItemCondition=1000&mag=1"
driver.get(url)
data = []
page =1
running = True
while running:
    try:
        driver.get(url+f"&rt=nc&_pgn={page}")
        products_ul = driver.find_element(By.CLASS_NAME,"b-list__items_nofooter")
    except:
        running =False

    products_li =products_ul.find_elements(By.TAG_NAME,"li")



    links = []
    for li in products_li:
        span_tag = li.find_element(By.CLASS_NAME,'s-item__info')
        a_tag = span_tag.find_element(By.TAG_NAME,"a")
        href =a_tag.get_attribute('href')
        links.append(href)
    div_rating = driver.find_elements(By.CLASS_NAME,"s-item__reviews")
    for i,x in zip(links,products_li):
        try:
            img_class = products_ul.find_element(By.CLASS_NAME,"s-item__image-helper")
            span_tag = img_class.find_element(By.TAG_NAME,'img')
            product_imag_link =span_tag.get_attribute('src')
        except:
            img_class=np.nan
        try:
            div_rating = driver.find_element(By.CLASS_NAME,"s-item__reviews")
            number_of_rating = div_rating.find_element(By.TAG_NAME,"div").get_attribute("aria-label").split()[0]
            overall_rating =div_rating.find_elements(By.TAG_NAME,"span")[1].text[1:-1]
        except:
            number_of_rating = np.nan
            overall_rating = np.nan
        driver.get(i)
        try:
            h1 = driver.find_element(By.CLASS_NAME,"x-item-title__mainTitle")
            name_of_product = h1.find_element(By.TAG_NAME,"span").text
        except:
            name_of_product=np.nan
        
        try:
            div = driver.find_element(By.CLASS_NAME,"x-sellercard-atf_info_about-seller")
            seller_name = div.find_element(By.TAG_NAME,"span").text
        except:
            seller_name=np.nan
        
        try:
            div2 = driver.find_element(By.CLASS_NAME,"x-price-primary")
            price_after_promotion = div2.find_element(By.TAG_NAME,"span").text
        except:
            price_after_promotion=np.nan
        
        try:
            div3 =driver.find_element(By.CLASS_NAME,"ux-layout-section__textual-display--itemId")
            eBay_Product_ID_ePID=div3.find_elements(By.TAG_NAME,"span")[1].text
        except:
            h ="j"
        try:
            d = driver.find_elements(By.CLASS_NAME,"ux-layout-section-evo__row")
            x = driver.find_elements(By.CLASS_NAME,"ux-labels-values__labels")
            y = driver.find_elements(By.CLASS_NAME,"ux-labels-values__values")
            items = {}
            for i, f in zip(x, y):
                items[i.text] = f.text
            if "Screen Size" in items:
                Screen_Size = items["Screen Size"]
            else:
                Screen_Size=np.nan
            if "Color" in items:
                Color_name = items["Color"]
            elif "Colour" in items:
                Color_name =items["Colour"]
            else:
                Color_name=np.nan
            if "Brand" in items:
                Brand = items["Brand"]
            else:
                Brand=np.nan
            if "Model" in items:
                Model =items["Model"]
            else:
                Model=np.nan
            if "Storage Capacity" in items:
                internal_memory =items["Storage Capacity"]
            elif "Hard Drive Capacity" in items:
                internal_memory =items["Hard Drive Capacity"]
            elif "SSD Capacity" in items:
                internal_memory =items["SSD Capacity"]
            else:
                internal_memory=np.nan
            if "RAM" in items:
                RAM_Size =items["RAM"]
            elif "RAM Size" in items:
                RAM_Size=items["RAM Size"]
            else:
                RAM_Size=np.nan
            if "Model Number" in items:
                Model_Number = items["Model Number"]
            else:
                Model_Number=np.nan
            if "Processor" in items:
                Processor_version=items["Processor"]
            else:
                Processor_version=np.nan   
            if "eBay Product ID (ePID)" in items:
                eBay_Product_ID_ePID =items["eBay Product ID (ePID)"]
            else:
                eBay_Product_ID_ePID=np.nan
            if "Graphics Processing Type" in items:
                Graphics_Processor_version =items["Graphics Processing Type"]
            else:
                Graphics_Processor_version=np.nan
        except:
            Screen_Size=np.nan
            Color_name=np.nan
            Brand=np.nan
            Model=np.nan
            internal_memory=np.nan
            RAM_Size=np.nan
            Model_Number=np.nan
            Graphics_Processor_version=np.nan
            eBay_Product_ID_ePID=np.nan
            Graphics_Processor_version=np.nan
            
        try:    
            div = driver.find_element(By.CLASS_NAME,"x-bin-price")
            span = div.find_element(By.CLASS_NAME,"x-price-transparency--discount")
            spans = span.find_elements(By.TAG_NAME,"span")
            price_before_promotion = spans[1].text
            promotion_percent = spans[3].text.split()
        except:
            price_before_promotion=np.nan
            promotion_percent=np.nan


        product_type ="Smartphone"
        company_name ="EBAY"
        battery_size =np.nan
        amount_promotion = np.nan #price_before_promotion-price_after_promotion
        Highlights_or_Description_of_product = np.nan

        
        data.append([product_imag_link,Brand,Model,eBay_Product_ID_ePID,product_type,name_of_product,company_name,seller_name,price_before_promotion,price_after_promotion,amount_promotion,promotion_percent,Highlights_or_Description_of_product,overall_rating,number_of_rating,Color_name,Screen_Size,Model_Number,battery_size,Processor_version,Graphics_Processor_version,internal_memory,RAM_Size])
        print([product_imag_link,Brand,Model,eBay_Product_ID_ePID,product_type,name_of_product,company_name,seller_name,price_before_promotion,price_after_promotion,amount_promotion,promotion_percent,Highlights_or_Description_of_product,overall_rating,number_of_rating,Color_name,Screen_Size,Model_Number,battery_size,Processor_version,Graphics_Processor_version,internal_memory,RAM_Size])
    page+=1

import pandas as pd

columns =["product_imag_link","Brand","Model","eBay_Product_ID_ePID","product_type","name_of_product","company_name","seller_name","price_before_promotion","price_after_promotion","amount_promotion","promotion_percent","Highlights_or_Description_of_product","overall_rating","number_of_rating","Color_name","Screen_Size","Model_Number","battery_size","Processor_version","Graphics_Processor_version","internal_memory","RAM_Size"]

# Creating DataFrame
df = pd.DataFrame(data, columns=columns)

df.to_csv("ebay1.csv")