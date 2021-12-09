import os
import pandas as pd
from selenium import webdriver
import time
import re
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)

# 获取并下载浙江省金融机构本外币存贷款数据表
url1 = 'http://hangzhou.pbc.gov.cn/hangzhou/125249/4341047/index.html'
browser.get(url1)
time.sleep(2)
browser.find_element_by_xpath('//*[@id="zoom"]/p/a').click()
time.sleep(3)
print("下载完成，进行下一步任务")
#下载东方财富网券商业绩月报网页表格，写入csv文件
data_all = pd.DataFrame()
url2 = 'https://data.eastmoney.com/other/qsjy.html'
browser.get(url2)
time.sleep(2)
data = browser.page_source
table = pd.read_html(data)[1]
print(table)
table.to_csv(r'./table_eastmoney.csv')
print("FINISH！！！")





