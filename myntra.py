
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import xlsxwriter


driver = webdriver.Chrome()

site_url = "http://www.myntra.com/tshirts/roadster/roadster-men-black-printed-round-neck-t-shirt/1491461/buy?src=search&uq=false&q=men-tshirts&p=1"


driver.get(site_url)

driver.implicitly_wait(10)
source = driver.page_source
soup = BeautifulSoup(source,'html.parser')

divs  = soup.find_all('div',{'class':'pdp-description-container'})

print (divs)

driver.quit()

