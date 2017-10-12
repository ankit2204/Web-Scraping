from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import xlsxwriter


site_url='https://www.myntra.com'
page_url='http://www.myntra.com/men-tshirts?src=tNav'

driver = webdriver.Chrome()

driver.get(page_url)

driver.implicitly_wait(20)

sort_list = driver.find_element_by_class_name('sort')

popular_sort = sort_list.find_elements_by_xpath(".//*")


for sort_element in popular_sort:
    print (sort_element.text)
    if sort_element.text == 'Popular':
        print ('sorted')
        sort_element.click()

driver.implicitly_wait(10)

select_more = driver.find_elements_by_class_name('show-more')

for select_tag in select_more:
    try:
        if 'SHOW MORE PRODUCTS' in select_tag.text:
            for i in range(5):
                select_tag .click()
    except Exception as e:
        print 'exception in show more products'

driver.implicitly_wait(10)

page_source = driver.page_source

soup = BeautifulSoup(page_source,"html.parser")

def has_data_order_and_style(tag):
    return tag.has_attr('data-styleid') and tag.has_attr('data-order')

all_li = soup.find_all(has_data_order_and_style)

workbook = xlsxwriter.Workbook('myntra_products_delete.xlsx')
worksheet = workbook.add_worksheet()

worksheet.set_column(0, 0, 30)
worksheet.set_column(1, 1, 80)
worksheet.set_column(2, 2, 10)
worksheet.set_column(3, 3, 10)
worksheet.set_column(4, 4, 10)

worksheet.write('A1','Rank')
worksheet.write('B1','Data-StyleID')
worksheet.write('C1','Brand')
worksheet.write('D1','Product')
worksheet.write('E1','Discounted Price')
worksheet.write('F1','MRP')
worksheet.write('G1','Discount')
worksheet.write('H1','Product Description')
worksheet.write('I1','Material and Care')
worksheet.write('J1','Photo Link')
worksheet.write('K1','Product Link')

row = 1
col = 0


for each_li in all_li:

    try:
        link_link_1=each_li['data-styleid']
        link_link_2=each_li['data-order']
        link_link_3=each_li.find('div',{'class':'brand'})
        link_link_4=each_li.find('div',{'class':'product'})
        link_link_5=each_li.find('div',{'class':'price'})
        link_link_6=link_link_5.find('span',{'class':'strike'})
        link_link_7=link_link_5.find('span',{'class':'discount'})
        link_link_8=each_li.find('img')
        
        worksheet.write(row, col, link_link_2)
        worksheet.write(row, col+1, link_link_1)
        worksheet.write(row, col+2, link_link_3.text)
        worksheet.write(row, col+3, link_link_4.text)
        worksheet.write(row, col+4, link_link_5.text)
        worksheet.write(row, col+5, link_link_6.text)
        worksheet.write(row, col+6, link_link_7.text)
        
        
        product_url=site_url +'/'+each_li.find('a').get('href')
        
        driver.get(product_url)
        driver.implicitly_wait(10)
        source = driver.page_source
        product_soup = BeautifulSoup(source,"html.parser")
        
        
        prod_li = product_soup.find_all('p',{'class':'pdp-product-description-content'})
        worksheet.write(row, col+7, prod_li[0].text)
        worksheet.write(row, col+8, prod_li[2].text)
        
        worksheet.write(row, col+9, link_link_8["_src"])
        worksheet.write(row, col+10,product_url)
        
        row+=1

        print row
    except Exception as e:
        print link_link_1


workbook.close()
