import tushare as ts
df = ts.get_k_data('600150', start='2018-01-01', end='2021-10-31')
df.set_index('date',inplace=True)
df = df.reset_index('date')
df1 = ts.get_realtime_quotes('600150')  #即时接口
df2 = ts.get_tick_data('600150',date='2018-10-25',src='tt')
df3 = ts.get_today_ticks('600150')

#visual

df = df[['date','close']]
import matplotlib.pyplot as plt
plt.plot(df['date'],df['close'])
plt.show()