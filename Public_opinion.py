import re
import time
import requests
import pymysql

def baidu(company):
    # 获取网页源代码
    #url = "https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&word="
    url = "https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=" + company
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31'}
    res = requests.get(url, headers=headers, timeout=10).text

    p_href = '<h3 class="news-title_1YtI1"><a href="(.*?)"'
    p_title = '<h3 class="news-title_1YtI1">.*?>(.*?)</a>'
    p_date = '<span class="c-color-gray2 c-font-normal" aria-label="(.*?)">'
    p_source = '<span class="c-color-gray c-font-normal c-gap-right" aria-label="(.*?)">'
    source = re.findall(p_source, res, re.S)
    date = re.findall(p_date, res, re.S)
    href = re.findall(p_href, res, re.S)
    title = re.findall(p_title, res, re.S)

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

    score = []
    keywords = ['违约', '诉讼', '违法', '震惊', '离职', '控诉', '亏损', '跌',
                '失败', '制裁', '打压', '抗议', '愤怒', '负面', '涉事', '危机',
                '举报', '减持', '威胁', '争议', '波动', '恶意', '美国', '管制',
                '短缺', '紧张', '收缩', '偿还']
    for i in range(len(title)):
        num = 0
        try:
            article = requests.get(href[i], headers=headers, timeout=10).text
        except:
            article = '爬取失败'
        try:
            article = article.encode('ISO-8859-1').decode('utf-8')
        except:
            try:
                article.encode('ISO-8859-1').decode('gbk')
            except:
                article = article
        p_article = '<p>(.*?)</p>'
        article_main = re.findall(p_article, article)
        article = ''.join(article_main)
        for k in keywords:
            if (k in article) or (k in title[i]):
                num -= 5
        score.append(num)

        company_re = company[0] + '.{0,5}' + company[-1]
        if len(re.findall(company_re, article)) < 1:
            title[i] = ''
            href[i] = ''
            date[i] = ''
            source[i] = ''
            score[i] = ''
    while '' in title:
        title.remove('')
    while '' in href:
        href.remove('')
    while '' in date:
        date.remove('')
    while '' in source:
        source.remove('')
    while '' in score:
        score.remove('')

    for i in range(len(title)):
        print(str(i + 1) + '.' + title[i] + '(' + date[i] + ' ' + source[i] + ') ')
        print(href[i])
        print(company + '该新闻舆情评分为' + str(score[i]))

    for i in range(len(title)):
        db = pymysql.connect(host='localhost', port=3306, user='root', password='', database='pachong', charset='utf8')
        cur = db.cursor()
        # %%
        sql_1 = 'SELECT * FROM article WHERE company = %s'
        cur.execute(sql_1, company)
        data_all = cur.fetchall()
        title_all = []
        for j in range(len(data_all)):
            title_all.append(data_all[j][1])

        if title[i] not in title_all:
            sql_2 = 'INSERT INTO article(company, title, href, source, date, score) VALUES (%s,%s,%s,%s,%s,%s)'
            cur.execute(sql_2, (company, title[i], href[i], source[i], date[i], score[i]))
            db.commit()
        # %%
        # cur.execute(sql, (company, title[i], href[i], source[i], data[i]))
        # db.commit()
        cur.close()
        db.close()

    print('^_^_' * 10 + '^')
    print(title)


companys = ['恒大', '万科', '中兴通讯', '中国船舶']
for i in companys:
    try:
        baidu(i)
        print(i + '爬取成功')
    except:
        print(i + '导入数据失败')
