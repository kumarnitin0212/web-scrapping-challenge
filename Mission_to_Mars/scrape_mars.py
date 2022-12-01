# Automates browser actions
from splinter import Browser

# Parses the HTML
from bs4 import BeautifulSoup 

# For scraping with Chrome
from webdriver_manager.chrome import ChromeDriverManager
import time

import pandas as pd
#-----------------------------------------------------------------------------------------------------  
# ### NASA Mars News - scrape data
#
# Scrape the [Mars News Site](https://redplanetscience.com/) and collect the latest News Title and 
# Paragraph Text.
#-----------------------------------------------------------------------------------------------------
def scrape_news():
    
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()} 
    browser = Browser('chrome', **executable_path, headless=False)
    
    # Visit Mars News Site
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)

    # Let it sleep for 1 second
    time.sleep(1)
    
    # Convert the browser html to a soup object and then quit the browser
    news_html = browser.html
    news_soup = BeautifulSoup(news_html, 'html.parser')
    browser.quit()

    # Search for news titles and news text
    news_texts = news_soup.find_all('div', class_='list_text')

    # Save the latest news (first element in class_='list_text' bs4.element.ResultSet)
    latest_news = news_texts[0]

    # Search for the latest news_tile and news_p (from class 'bs4.element.Tag')
    news_title = latest_news.find('div', class_='content_title').text
    news_p     = latest_news.find('div', class_='article_teaser_body').text

    return (news_title, news_p)
#-----------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------
# ### JPL Mars Space Images—Featured Image  - scrape data
#  * Visit the URL for the Featured Space Image site. (https://spaceimages-mars.com)
#  * Find the image URL for the current Featured Mars Image
#-----------------------------------------------------------------------------------------------------
def scrape_featured_image():
    
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # Visit Featured Space Image Site
    image_url = 'https://spaceimages-mars.com'
    browser.visit(image_url)

    # Convert the browser html to a soup object and then quit the browser
    image_html = browser.html
    image_soup = BeautifulSoup(image_html, 'html.parser')
    browser.quit()

    # Search for the featured image and news text
    image_srcs = image_soup.find_all('div', class_='floating_text_area')

    # Loop through list of image_srcs
    for image_src in image_srcs:
        
        try:
            # Find the URL for the current Featured Mars Image
            image_filename = image_src.a['href']
            
            # Save the complete URL String
            featured_image_url = f"{image_url}/{image_filename}"
        except AttributeError as e:
            print(e)

    return featured_image_url
#-----------------------------------------------------------------------------------------------------

    
#-----------------------------------------------------------------------------------------------------
# ### Mars Facts - scrape data
# * Visit the Mars Facts webpage (https://galaxyfacts-mars.com) 
# * Use Pandas to scrape the table containing facts about the planet including diameter, mass, etc.
# * Use Pandas to convert the data to a HTML table string.
#-----------------------------------------------------------------------------------------------------
def scrape_facts():
    
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # Visit Mars Facts webpage
    facts_url = 'https://galaxyfacts-mars.com'
    browser.visit(facts_url)

    # Let it sleep for 1 second
    time.sleep(1)

    # Convert the browser html to a soup object and then quit the browser
    facts_html = browser.html
    facts_soup = BeautifulSoup(facts_html, 'html.parser')
    browser.quit()

    # Scrape the table containing facts about the planet including diameter, mass, etc.
    tables = pd.read_html(facts_url)

    # Save the table with Mars facts data
    facts_df         = tables[0]
    facts_df.columns = ['Description', 'Mars','Earth']
    facts_df         = facts_df.set_index('Description') 

    # Convert the mars fact df to a HTML table string
    facts_html = facts_df.to_html()

    return facts_html
#-----------------------------------------------------------------------------------------------------

   
#-----------------------------------------------------------------------------------------------------
# ### Mars Hemispheres - scrape data
# 
# * Visit the [astrogeology site](https://marshemispheres.com/) to obtain high-resolution images for 
#   each hemisphere of Mars.
# * Find the image URL to the full-resolution image.
# * Save the image URL string for the full resolution hemisphere image and the hemisphere title 
#   containing the hemisphere name. Use a Python dictionary to store the data using the keys 
#   `img_url` and `title`.
# * Append the dictionary with the image URL string and the hemisphere title to a list. This list will 
#   contain one dictionary for each hemisphere.
#-----------------------------------------------------------------------------------------------------
def scrape_hemispheres_images():  
    
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # Visit astrogeology site
    hemisphere_url = 'https://marshemispheres.com/'
    browser.visit(hemisphere_url)

     # Let it sleep for 1 second
    time.sleep(1)
    
    # Convert the browser html to a soup object and then quit the browser
    hemisphere_html = browser.html
    hemisphere_soup = BeautifulSoup(hemisphere_html, 'html.parser')
    browser.quit()
    
    # Search the item by class name
    item_hemisphere_images = hemisphere_soup.find_all('div', class_="item")
    
    # Loop through item_hemisphere_images and save the title and URL in a dictionary
    mars_hemispheres_images_urls = []

    for item in item_hemisphere_images:
    
        try: 
            mars_hemispheres_images = {}
            # ------------------------------------------------------------------
            # Search for image title
            img_title_h3 = item.find_all('h3')
            img_title    = img_title_h3[0].text
            # ------------------------------------------------------------------
            # Search for the image url
            a     = item.find_all('a')
            a_url = a[0]['href']
            
            # Save the complete image url
            img_url = f"{hemisphere_url}{ a_url}"
            # ------------------------------------------------------------------
            # Search for the img src url
            img_src = item.img['src']
            
            # Save the complete URL String
            img_src_url = f"{hemisphere_url}{img_src}"
            # ------------------------------------------------------------------
            # Save the dictionary of image title and url into a list
            mars_hemispheres_images['title']       =  img_title 
            mars_hemispheres_images['img_url']     =  img_url  
            mars_hemispheres_images['img_src_url'] =  img_src_url  
            mars_hemispheres_images_urls.append(mars_hemispheres_images)
            
        except AttributeError as e:
            print(e)
            
    return mars_hemispheres_images_urls
#-----------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------
# ### Main scrape function
# * Execute scrape_news() to scrape latest Mars News
# * Execute scrape_featured_image() to scrape the Mars Featured Image 
# * Execute scrape_facts() to scrape the Mars Facts data
# * Execute scrape_hemispheres_images() to scrape the Mars hemispheres images
#-----------------------------------------------------------------------------------------------------
def scrape():  
    #-----------------------------------------------------------------------------------------------------  
    # ### NASA Mars News - scrape data
    #-----------------------------------------------------------------------------------------------------  
    news_title, news_p = scrape_news()
    
    #-----------------------------------------------------------------------------------------------------
    # ### JPL Mars Space Images—Featured Image  - scrape data
    #-----------------------------------------------------------------------------------------------------
    featured_image_url = scrape_featured_image()
    
    #-----------------------------------------------------------------------------------------------------
    # ### Mars Facts - scrape data
    #-----------------------------------------------------------------------------------------------------
    facts_html = scrape_facts()
    
    #-----------------------------------------------------------------------------------------------------
    # ### Mars Hemispheres - scrape data
    mars_hemispheres_images_urls = scrape_hemispheres_images()
    
    #-----------------------------------------------------------------------------------------------------
    # Save the scraped data into a dictionary                                
    mars_scrape_data = { "news_title"         : news_title
                       , "news_p"             : news_p
                       , "featured_image_url" : featured_image_url
                       , "facts_html"         : facts_html 
                       , "hemispheres_images" : mars_hemispheres_images_urls 
                       }
    
    # Return the dictionary with all scraped data
    return  mars_scrape_data
#=====================================================================================================   