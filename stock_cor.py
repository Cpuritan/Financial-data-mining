import pandas as pd
import pymysql
import datetime
import tushare as ts
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

# 导出舆情数据评分
db = pymysql.connect(host='localhost', port=3306, user='root',
                     password='', database='pachong', charset='utf8')
company = '恒大'
date_list = list(pd.date_range('2021-07-01', '2021-11-13'))
for i in range(len(date_list)):
    date_list[i] = datetime.datetime.strftime(date_list[i], '%Y-%m-%d')
# SQL
cur = db.cursor()
sql = 'SELECT * FROM article WHERE company = %s AND date = %s'
score_list = {}
for d in date_list:
    cur.execute(sql, (company, d))
    data = cur.fetchall()
    score = 100
    for i in range(len(data)):
        score += data[i][5]
    score_list[d] = score

db.commit()
cur.close()
db.close()

data = pd.DataFrame.from_dict(score_list,orient='index',columns=['score'])

# 股票数据
df = ts.get_k_data('600150', start='2021-09-01', end='2021-11-13')
df.set_index('date', inplace=True)
df = df.reset_index('date')
df = df[['date', 'close']]# 收盘价

data1 = pd.merge(data, df, on='date', how='inner')
data1 = data1.rename(columns={'close':'price'})
# visual
plt.plot(data1['date'], data1['score'], linestyle='--', label='分数')
plt.xticks(rotation=45)
plt.twinx()
plt.plot(data1['date'], data1['price'], label='价格')
plt.xticks(rotation=45)
plt.show()

####temp
df = ts.get_k_data('600150', start='2021-06-01', end='2021-11-13')
df.set_index('date', inplace=True)
df = df.reset_index('date')
df = df[['date', 'open', 'close', 'high', 'low']]# 收盘价
plt.plot(df['date'], df['close'], linestyle='--', label='分数')
plt.xticks(rotation=45)
plt.twinx()
plt.plot(df['date'], df['low'], label='价格')
plt.xticks(rotation=45)
plt.show()
# Pearsonr
corr1 = pearsonr(df['close'], df['open'])
corr2 = pearsonr(df['close'], df['high'])
print('相关系数r值' + str(corr1[0]) + '，显著性水平P值' + str(corr1[1]))
print('相关系数r值' + str(corr2[0]) + '，显著性水平P值' + str(corr2[1]))
