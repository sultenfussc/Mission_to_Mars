# Dependencies
from operator import index
from bs4 import BeautifulSoup
import requests
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import pandas as pd
 

def scrape_info():
    ### Setup Splinter ###
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
   
    ### NASA Mars News ###
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

    ### JPL Mars Space Images: Featured Image ###
    url2 = 'https://spaceimages-mars.com'
    browser.visit(url2)
    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')

    featured_image = soup2.find('img', class_='headerimage').get('src')
    featured_image_url = (f'{url2}/{featured_image}')
    #featured_image_url

    ### Mars Facts ###
    url3 = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url3)
    #tables

    df = tables[0]
    df_copy = df.copy()
    df_copy.columns = ['Mars - Earth Comparison','Mars','Earth']
    df_copy.set_index('Mars - Earth Comparison')
    new_df = df_copy.drop([0])
    comparison_profile = new_df.to_html()

    df2 = tables [1]
    df2_copy = df2.copy()
    df2_copy.columns = ['Mars','Planet Data']
    df2_copy.set_index('Mars')
    new_df2 = df2_copy.drop([1])
    mars_profile = new_df2.to_html()

    ### Mars Hemispheres ###
    # Go to page
    url4 = 'https://marshemispheres.com/'
    browser.visit(url4)

    # Find link to each hemisphere
    hemisphere_links = browser.links.find_by_partial_text('Hemisphere')
    hemisphere_urls = []
    for i in range(len(hemisphere_links)):
        hemisphere_urls.append(hemisphere_links[i]['href'])
    #hemisphere_urls

    img_urls = []
    for i in range(len(hemisphere_urls)):
        url5 = hemisphere_urls[i]
        browser.visit(url5)
        img_links = browser.links.find_by_partial_text('Sample')[0]['href']
        
        # locate title on the page
        html4 = browser.html
        soup = BeautifulSoup(html4, 'html.parser')
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
        'news_p':news_p,
        'featured_image_url':featured_image_url,
        'facts_table': {
            'comparison_profile':comparison_profile,
            'mars_profile':mars_profile,
        },
        'img_urls': img_urls
    }

    print(all_scraped_info)

    browser.quit()
    return all_scraped_info