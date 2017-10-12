from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import xlsxwriter


workbook = xlsxwriter.Workbook("people.xlsx")
worksheet = workbook.add_worksheet()


def initialize_workbook():
	

	worksheet.set_column(0, 0, 30)
	worksheet.set_column(1, 1, 80)
	worksheet.set_column(2, 2, 100)
	worksheet.set_column(3, 3, 80)
	worksheet.set_column(4, 4, 50)
	worksheet.set_column(5, 5, 50)
	worksheet.set_column(6, 6, 80)

	worksheet.write('A1', 'Brand')
	worksheet.write('B1', 'Store Name')
	worksheet.write('C1', 'Address')
	worksheet.write('D1', 'Phone Number')
	worksheet.write('E1', 'Open Days')
	worksheet.write('F1', 'Timings')
	worksheet.write('G1', 'LatLon')

def write_store(store_data,row):
	worksheet.write(row,0,store_data["brand"])
	worksheet.write(row,1,store_data["store_name"])
	worksheet.write(row,2,store_data["address"])
	worksheet.write(row,3,store_data["phone"])
	worksheet.write(row,4,store_data["open_days"])
	worksheet.write(row,5,store_data["timing"])
	worksheet.write(row,6,store_data["LatLon"])




def select_dropdown_option(driver, select_locator, option_text):
	dropdown = select_locator
	for option in dropdown.find_elements_by_tag_name('option'):
		if option.text == option_text:
			option.click()
			break

def select_dropdown(driver, dropdown_id):
	driver.implicitly_wait(10)
	dropdown = driver.find_element_by_css_selector(dropdown_id)
	return dropdown

def open_store_list_page(driver,site_url, state_dropdown_id, city_dropdown_id):
	driver.get(site_url)

	state_dropdown = select_dropdown(driver, state_dropdown_id)
	select_dropdown_option(driver, state_dropdown, "Karnataka")

	city_dropdown = select_dropdown(driver, city_dropdown_id)
	select_dropdown_option(driver, city_dropdown, "Bengaluru")

	driver.implicitly_wait(10)
	submit_button = driver.find_element_by_id("storeLocBtn")
	submit_button.click()

def extract_store_data(driver,row):
	initialize_workbook()
	driver.implicitly_wait(10)
	source = driver.page_source
	soup = BeautifulSoup(source,'html.parser')

	name = soup.findAll('h3',{'class':'lh-22'})

	store_detail = {}
	store_detail['brand'] = name[0].text
	store_detail['store_name'] = name[1].text

	address = soup.find('p',{'class':'gray-color font-15'})
	store_detail['address'] = address.text

	phone = soup.find('a',{'class':'gray-color font-18'})
	store_detail['phone'] = phone.text


	timings = soup.find(lambda tag: tag.name == 'span' and tag.get('class') == ['gray-color'])
	store_detail['open_days'] = timings.text
	time_limits = timings.findNextSiblings()
	store_detail['timing'] = time_limits[0].text

	map_span = soup.find('span',{'class':'gray-color font-16 mar-lt-5'})

	link = map_span.find_all('a')[0]

	s = link['onclick']

	store_detail['LatLon'] = s[s.find("(")+1:s.find(")")]

	write_store(store_detail,row)




def open_stores(driver):
	store_urls = []
	row = 1
	stores = driver.find_element_by_id("store-locator")
	for link in stores.find_elements_by_tag_name('a'):
		store_urls.append(link.get_attribute("href"))
	
	for url in store_urls:
		driver.get(url)
		row = row+1
		driver.implicitly_wait(15)
		extract_store_data(driver,row)



driver = webdriver.Chrome()

site_url = "https://www.peopleonline.co.in/content/store-locators-9"

state_dropdown_id = "select#state"

city_dropdown_id = "select#city"

open_store_list_page(driver, site_url, state_dropdown_id, city_dropdown_id)

driver.implicitly_wait(10)
open_stores(driver)

driver.quit()

workbook.close()













