from bs4 import BeautifulSoup
import requests
import xlsxwriter


site_url='https://www.allsales.in'
page_url='https://www.allsales.in/Bangalore/BrandList/10'

page_response = requests.get(page_url)
page_source = page_response.text.encode('utf8','replace')

soup = BeautifulSoup(page_source,"html.parser")

link_div = soup.find_all('div',{'class':'AreaName'})

workbook = xlsxwriter.Workbook('brands.xlsx')
worksheet = workbook.add_worksheet()

worksheet.set_column(0, 0, 30)
worksheet.set_column(1, 1, 80)

worksheet.write('A1','Brand')
worksheet.write('B1','Link')

row = 1
col = 0
brand_links=[]

for each_div in link_div:
	link_link=each_div.find('a')
	worksheet.write(row, col, link_link.text)
	worksheet.write(row,col+1,site_url+link_link["href"])
	brand_links.append((link_link.text,site_url+link_link["href"]))
	row+=1

workbook.close()


workbook2 = xlsxwriter.Workbook('address.xlsx')
worksheet2=workbook2.add_worksheet()
worksheet2.set_column(0, 0, 30)
worksheet2.set_column(1, 1, 80)
worksheet2.set_column(2, 2, 30)

worksheet2.write('A1','Store')
worksheet2.write('B1','Address')
worksheet2.write('C1','Phone')

row=1
col=0

for each_brand in brand_links:
        print each_brand[0]
        page_response = requests.get(each_brand[1])
        page_source = page_response.text.encode('utf8','replace')
        soup=BeautifulSoup(page_source)
        store_div=soup.find_all('div',{'class':'StoresArea'})

        for each_div in store_div:
                try:
                        add_div=each_div.find('div',{'class':'AddCont'})
                        phone_div=each_div.find('a')
                        worksheet2.write(row,col,each_brand[0])
                        worksheet2.write(row, col+1, add_div.text)
                        worksheet2.write(row,col+2,phone_div.text)
                        row+=1
                except:
                        row+=1
                

workbook2.close()



