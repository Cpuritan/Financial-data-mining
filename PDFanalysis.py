import re
import time
from selenium import webdriver
import pdfplumber
import os

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)
browser.get("http://www.cninfo.com.cn/new/index")#访问巨潮资讯网
browser.find_element_by_xpath('/html/body/header/div/div[5]/div/div[1]/input').send_keys('强制退市')
browser.find_element_by_xpath('/html/body/header/div/div[5]/div/div/span/span/button/span/i').click()
time.sleep(4)
page = browser.page_source

p_count = '<span class="total-box" style="">共(.*?)条'
count = re.findall(p_count, page)[0]
pages = int(int(count)/10)
page_ = []
page_.append(page)
for i in range(4):
    browser.find_element_by_xpath('//*[@id="fulltext-search"]/div/div/div[2]/div[4]/div[2]/div/button[2]/i').click()
    time.sleep(3)
    page = browser.page_source
    page_.append(page)
    time.sleep(1)
allpage = "".join(page_)
browser.quit()

# 正则提取
p_code = '<div class="cell">.*?<span class="code">(.*?)</span>'
#p_href = '<a target="_blank" href="(.*?)" data-id'
p_href = '<div class="cell"><a target="_blank" href="(.*?)" data-id'
p_date = '<div class="cell"><span class="time">(.*?)</span>'
p_title = '<span title="" class="r-title">(.*?)</span>'
code = re.findall(p_code, allpage, re.S)
href = re.findall(p_href, allpage, re.S)
date = re.findall(p_date, allpage, re.S)
title = re.findall(p_title, allpage, re.S)
# 测试是否提取成功
print('*'*20)
print(len(code))
print('*'*20)

# 数据清洗
for i in range(len(code)):
    title[i] = title[i].strip()
    title[i] = re.sub('<.*?>', '', title[i])
    href[i] = 'http://www.cninfo.com.cn' + href[i]
    href[i] = re.sub('amp;', '', href[i])
    date[i] = date[i].strip()
    date[i] = date[i].split(' ')[0]
    date[i] = re.sub('年', '-', date[i])
    date[i] = re.sub('月', '-', date[i])
    date[i] = re.sub('日', '-', date[i])
    if ('小时' in date[i]) or ('分钟' in date[i]):
        date[i] = time.strftime("%Y-%m-%d")
    else:
        date[i] = date[i]
    print(str(i+1) + '.' + title[i] + ' - ' + date[i])

# PDF*筛选*
for i in range(len(title)):
    if '2021' in date[i]:# or '2020' in date[i]:
        pass
    else:
        title[i] = ''
        href[i] = ''
        date[i] = ''

while '' in title:
    title.remove('')
while '' in href:
    href.remove('')
while '' in date:
    date.remove('')

for i in range(len(href)):
    chrome_options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'C:\\Users\\鲍鱼展翅\\Desktop\\language bank\\金融数据挖掘\\Financial-data-mining\\公告'} #这边你可以修改文件储存的位置
    chrome_options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(href[i])
    try:
        browser.find_element_by_xpath('//*[@id="noticeDetail"]/div/div[1]/div[3]/div[1]/button/span').click()
        time.sleep(3)
        browser.quit()
        print(str(i+1) + '.' + title[i] + "下载完毕捏^u^")
    except:
        print(title[i] + "不是PDF文件！！！！！^!^")

# 1.遍历文件夹中的所有PDF文件
file_dir = 'C:\\Users\\鲍鱼展翅\\Desktop\\language bank\\金融数据挖掘\\Financial-data-mining\\公告'  # 也可以改成你自己需要遍历的文件夹，这里用的相对路径
file_list = []
for files in os.walk(file_dir):  # 遍历该文件夹及其里面的所有子文件夹
    for file in files[2]:
        if os.path.splitext(file)[1] == '.pdf' or os.path.splitext(file)[1] == '.PDF':
            file_list.append(file_dir + '\\' + file)
print(file_list)

# 2.PDF文本解析和内容筛选
pdf_all = []
for i in range(len(file_list)):
    pdf = pdfplumber.open(file_list[i])
    pages = pdf.pages
    text_all = []
    for page in pages:  # 遍历pages中每一页的信息
        text = page.extract_text()  # 提取当页的文本内容
        text_all.append(text)  # 通过列表.append()方法汇总每一页内容
    text_all = ''.join(text_all)  # 把列表转换成字符串
    print(text_all)  # 打印全部文本内容
    pdf.close()

    # 通过正文进行筛选
    if ('自有' in text_all) or ('议案' in text_all) or ('理财' in text_all) or ('现金管理' in text_all):
        pdf_all.append(file_list[i])
print(pdf_all)  # 打印筛选后的PDF列表

# # 3.筛选后文件的移动
# for pdf_i in pdf_all:
#     newpath = 'E:\\筛选后的文件夹\\' + pdf_i.split('\\')[-1]  # 这边这个移动到的文件夹一定要提前就创建好！
#     os.rename(pdf_i, newpath)  # 执行移动操作

print('PDF文本解析及筛选完毕！')
