import re
import time
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)
browser.get("http://www.cninfo.com.cn/new/index")#访问巨潮资讯网
browser.find_element_by_xpath('/html/body/header/div/div[5]/div/div[1]/input').send_keys('股权质押')
browser.find_element_by_xpath('/html/body/header/div/div[5]/div/div/span/span/button/span/i').click()
time.sleep(5)
page = browser.page_source

# 正则提取
p_code = '<div class="cell">.*?<span class="code">(.*?)</span>'
p_date = '<div class="cell"><span class="time">(.*?)</span>'
p_title = '<span title="" class="r-title">(.*?)</span>'
code = re.findall(p_code, page, re.S)
date = re.findall(p_date, page, re.S)
title = re.findall(p_title, page, re.S)
# 测试是否提取成功
print('*'*20)
print(len(code))
print('*'*20)
# 数据清洗
for i in range(len(code)):
    title[i] = title[i].strip()
    title[i] = re.sub('<.*?>', '', title[i])
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
print(code)
print(date)
print(title)
