# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 12:32:25 2022
WEB SCRAPING
@author: Soura
"""
import pandas as pd
import numpy as np
import requests 
from bs4 import BeautifulSoup

## To scrape a website:
    # Use the API
    # HTML web scraping using tool like bs4
    
url= "https://insights.blackcoffer.com/future-of-work-how-ai-has-entered-the-workplace/"


## STEP 1:
    # Get the HTML

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}

r= requests.get(url,headers= headers)   # GET request for getting the website data
html_content= r.content  # HTML code of the website
#print(html_content)

## STEP 2:
    # Parse the HTML
soup= BeautifulSoup(html_content, 'html.parser')
#print(soup)

## STEP 3:
    # HTML tree traversal


## Commonly used types of ojects
# Tag  >> type(title)
# Navigable string   >> type(title.string)
# BeautifulSoup  >> type(soup)
# Comment

#title= soup.title ## Get the title of soup

#paras= soup.find_all('p') ## Get all the paras from page
#print(paras)

#print(soup.find('p')) # First para

#print(soup.find('p')['class']) # classes of page
#print(soup.find_all("p", class_= 'lead')) # Find all elements with class lead

## Get text from tags/soup
#print(soup.find('p').get_text())
#print(soup.get_text())
#textfile= soup.get_text()

txt= soup.find(attrs= {"class":"td-post-content"}).text
print(txt)

with open("title.txt", 'w',encoding="utf-8") as file:     
    file.write(txt)


'''
## Get all anchors tags from page
anchors= soup.find_all('a')
#print(anchor)

all_links= set()
for link in anchors:
    if link.get('href')!="#":
        linktext= url+ link.get('href')
        all_links.add(linktext)
        print(linktext)
print(all_links)
'''


# Import required libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Set options to display the window of chrome
options = Options()
options.headless = True
options.add_argument('window-size=1920x1080')

# Multiple urls
file= pd.read_csv("C:\\Users\\Soura\\Downloads\\Input.csv")
urls= list(file["URL"])
urls


time.sleep(2)
# Pass multiple urls using 'for' loop to 'chrome' driver
for i in range(len(urls)):
    path =r"C:\\Users\\Soura\\Downloads\\chromedriver_win32"
    driver = webdriver.Chrome(path,options=options)
    driver.get(urls[i])
    #driver.maximize_window()
    # Get 'article_title' and 'article_paragraph' using xpath
    article_title = driver.find_element_by_xpath('//h1').text
    article_paragraph = driver.find_element_by_xpath("//div[contains(@class,'td-post-content')]").text
    
    with open(f'data/{i}.txt','w') as file:
        file.write(article_title+"\n" )
        file.writelines("% s" %data for data in article_paragraph)


# Quit driver
    driver.quit()
    

import nltk
nltk.download()

f= open("text1.txt")
f1=f.read()

#text=txt.replace('\n','')


