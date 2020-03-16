# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import time


# Connect to chromedriver
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

# Scrape function
def scrape():
   
    # Create empty dictionary to store data
    mars_data = {}
    browser = init_browser()

# Mars News
    marsNews_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(marsNews_url)
    time.sleep(1)

    # Scrape page 
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    slide = soup.find_all('li', class_='slide')[1]
    title = slide.find('h3').text
    news_p = slide.find('div', class_='article_teaser_body').text
    
    # Store data in dictionary
    mars_data["title"] = title
    mars_data["news_p"] = news_p

# Featured Image
    featuredImg_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featuredImg_url)
    time.sleep(1)

    # Scrape page
    # Use fancybox http://fancybox.net/
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    fancybox = soup.find_all('a', class_='fancybox')[0]
    img = fancybox.get('data-fancybox-href')
    featured_image_url = f'https://www.jpl.nasa.gov/{img}'

    # Store data in dictionary
    mars_data["featured_image_url"] = featured_image_url

# Current weather 
    marsWeather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(marsWeather_url)
    time.sleep(1)

    # Scrape page
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_weather = soup.find('p', class_='TweetTextSize')

    # Store in dictionary
    mars_data["mars_weather"] = mars_weather

# Mars Facts
    marsFacts_url = "https://space-facts.com/mars/"

    # Use pandas to scrape
    tables = pd.read_html(marsFacts_url)

    # Grab Mars Facts
    mars_df = tables[1]

    # Name columns
    mars_df.columns = ['Description', 'Value']

    # Set index
    mars_df.set_index('Description', inplace=True)

    # Convert Data Frame to HTML
    html_table = mars_df.to_html()

    # Remove any new lines and white spaces
    html_table = html_table.replace('\n', ' ')

    # Store data in a dictionary
    mars_data["mars_facts"] = html_table

    # close the browser
    browser.quit()

    return mars_data
