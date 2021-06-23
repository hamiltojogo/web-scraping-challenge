#!/usr/bin/env python
# coding: utf-8

# NASA Mars News

# In[8]:


#import dependcies 
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import pymongo

def scrape ():


    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Latest news
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    artile_soup = BeautifulSoup(html, 'html.parser')
    article = artile_soup.find('div', class_ = 'list_text')
    news_title = article.find('div', class_='content_title').text
    news_paragraph = article.find('div', class_='article_teaser_body').text


    # Mars Featured Image

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser_pic = Browser('chrome', **executable_path, headless=False)
    url_pic = 'https://spaceimages-mars.com/'
    browser_pic.visit(url_pic)
    html_pic = browser_pic.html
    image_soup = BeautifulSoup(html_pic, 'html.parser')
    image_path = image_soup.find('img', class_='headerimage fade-in')['src']
    featured_image_url = url_pic + image_path
    


    # Mars Facts
    url_facts = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url_facts)
    mars_facts = tables[0]
    #rename the columns
    mars_facts.columns = ['Variable', 'Mars', 'Earth']
    #drop the unneeded column
    del mars_facts['Earth']
    #mars_facts.drop(index= mars_facts.index[0], axis = 0, inplace = True)
   


    # Mars Hemispheres

    hemi_url = 'https://marshemispheres.com/'
    browser.visit(hemi_url)
    hemi_html = browser.html
    hemi_soup = BeautifulSoup(hemi_html, 'html.parser')
    #list to store resultes 
    hemi_list = []
    all_mars = hemi_soup.find('div', class_='collapsible results')
    hemi = all_mars.find_all('div', class_='item')
    for name in hemi:
        # Title
        hemi_name = name.find('div', class_="description")
        title = hemi_name.h3.text.strip('Enhanced')     
        #links for high res image    
        hemi_link = name.find('a', class_='itemLink product-item')['href']
        #print(hemi_link)
        browser.visit(hemi_url + hemi_link)       
        img_html = browser.html
        img_soup = BeautifulSoup(img_html, 'html.parser')
       
        img_link = img_soup.find('div')
        url = img_link.find('img', class_= 'wide-image')['src']
        img_url = hemi_url + url       
        #add results to list         
        hemi_list.append({'Titel': title, 'image_url':img_url})   
        #return to main page
        browser.visit(hemi_url)



    
    mars_results = {
        'News Title':news_title,
        'News Text':news_paragraph,
        'Featured Image url':featured_image_url,
        'Mars Facts':mars_facts,
        'Links to hemiphere phtots':hemi_list,
    }
    return mars_results
    
        

