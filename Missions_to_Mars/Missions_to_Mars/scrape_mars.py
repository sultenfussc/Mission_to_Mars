# Dependencies
from base64 import urlsafe_b64encode
from bs4 import BeautifulSoup
import requests
import os
import pymongo
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import pandas as pd

# Setup splinter
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # NASA Mars News
    
    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    titles = soup.find_all('div', class_='content_title')
    news_title = titles[0].text
    #news_title
    paragraphs = soup.find_all('div', class_='article_teaser_body')
    news_p = paragraphs[0].text
    #news_p

    # JPL Mars Space Images: Featured Image
    url2 = 'https://spaceimages-mars.com'
    browser.visit(url2)
    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')

    featured_image = soup2.find('img', class_='headerimage').get('src')
    featured_image_url = (f'{url}/{featured_image}')
    #featured_image_url

    # Mars Facts
    url3 = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url3)
    #tables

    df = tables[0]
    df_copy = df.copy()
    df_copy.columns = ['Mars - Earth Comparison','Mars','Earth']
    df_copy.set_index('Mars - Earth Comparison')
    new_df = df_copy.drop([0])
    # new_df
    comparison_profile = new_df.to_html('Mars_Earth_Comparison_table.html')

    df2 = tables [1]
    df2_copy = df2.copy()
    df2_copy.columns = ['Mars','Planet Data']
    df2_copy.set_index('Mars')
    new_df2 = df2_copy.drop([1])
    # new_df2
    mars_profile = new_df2.to_html('Mars_Planet_Profile.html')

    # Mars Hemispheres
    # Go to page
    url3 = 'https://marshemispheres.com/'
    browser.visit(url3)

    # HTML object
    html3 = browser.html

    # Find link to each hemisphere
    hemisphere_links = browser.links.find_by_partial_text('Hemisphere')
    hemisphere_urls = []
    for i in range(len(hemisphere_links)):
        hemisphere_urls.append(hemisphere_links[i]['href'])
    #hemisphere_urls

    img_urls = []
    for i in range(len(hemisphere_urls)):
        url4 = hemisphere_urls[i]
        browser.visit(url4)
        img_links = browser.links.find_by_partial_text('Original')[0]['href']
        
        # locate title on the page
        html = browser.html
        soup = BeautifulSoup(html3, 'html.parser')
        titles = soup.find('h2', class_='title').text
        
        # append titles and img_links into list
        img_urls.append({
            'title': titles,
            'img_url': img_links
        })
    # img_urls

    # load all variables into dictionary
    all_scraped_info = {
        'news_title':news_title,
        'news_text':news_p,
        'featured_image':featured_image_url,
        'facts_table': {
            'comparison_profile': comparison_profile,
            'mars_profile': mars_profile,
        },
        'img_urls': img_urls
    }

    browser.quit()
    return all_scraped_info