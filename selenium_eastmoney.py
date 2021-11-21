import re
import time
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)
browser.get("https://so.eastmoney.com/")#访问东方财富网
browser.find_element_by_xpath('//*[@id="searchSuggest"]').send_keys('中国恒大')
browser.find_element_by_xpath('//*[@id="searchbox"]/div[2]/form/input[2]').click()
browser.find_element_by_xpath('//*[@id="app"]/div[2]/ul/li[6]/a/span').click()
time.sleep(2)
page = browser.page_source

# 正则提取
p_title = '<div class="cfh_item_t">.*? target="_blank">(.*?)</a>'
p_href = '<div class="cfh_item_t"><a href="(.*?)" target="_blank>"'
p_date = '<span class="cfh_item_time">(.*?)</span>'
p_source = '<span class="cfh_zz">.*?target="_blank">(.*?)</a></span>'

source = re.findall(p_source, page, re.S)
date = re.findall(p_date, page, re.S)
href = re.findall(p_href, page, re.S)
title = re.findall(p_title, page, re.S)
# 测试是否提取成功
print('*'*20)
print(len(title))
print('*'*20)

for i in range(len(title)):
    title[i] = title[i].strip()
    title[i] = re.sub('<.*?>', '', title[i])
    source[i] = source[i].strip()
    date[i] = date[i].strip()
    date[i] = date[i].split(' ')[0]
    date[i] = re.sub('年', '-', date[i])
    date[i] = re.sub('月', '-', date[i])
    date[i] = re.sub('日', '-', date[i])
    if ('小时' in date[i]) or ('分钟' in date[i]):
        date[i] = time.strftime("%Y-%m-%d")
    else:
        date[i] = date[i]
# 结果展示
print(title)
print(date)
print(source)
