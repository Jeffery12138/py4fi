import pandas as pd
import numpy as np
from pylab import mpl, plt
# import cufflinks as cf
import os

plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'
# %matplotlib inline

# python内建的文件读入方式
filename = 'tr_eikon_eod_data.csv'
f = open(filename, 'r')
print(f.readlines()[:5])

# pandas读入DataFrame
data = pd.read_csv(filename, index_col=0, parse_dates=True)
print(data.info())  # data信息
print(data.describe().round(2))  # 基本序数统计量
print(data.mean())
print(data.aggregate([min,
                      np.mean,
                      np.std,
                      np.median,
                      max]).round(2))
print(data.diff().head())  # diff() provides the changes between two index values.
print(data.diff().mean())
print(data.pct_change().round(3).head())  # pct_change() 间断时间报酬率
print(data.pct_change().round(3).mean())  # 日报酬率期望
# print(data.head())
# print(data.shape)
fig_path = 'H:/py4fi/images/ch08/'
if not os.path.exists(fig_path):
    os.makedirs(fig_path)
# data.plot(figsize=(10, 12), subplots=True)
# plt.savefig(fig_path+'fts_01.png')
instruments = ['Apple Stock', 'Microsoft Stock', 'Intel Stock', 'Amazon Stock', 'Goldman Sachs Stock',
               'SPDR S&P 500 ETF Trust', 'S&P 500 Index', 'VIX Volatility Index', 'EUR/USD Exchange Rate',
               'Gold Price', 'VanEck Vectors Gold Miners EFE', 'SPDR Gold Trust']
# print(data.columns)
# print(instruments)
# # print(zip(data.columns, instruments))
# for ric, name in zip(data.columns, instruments):
#     print('{:8s} | {}'.format(ric, name))
# data.pct_change().mean().plot(kind='bar', figsize=(10, 6))
# plt.savefig(fig_path+'fts_02.png')
# plt.show()
rets = np.log(data / data.shift(1))  # 连续时间报酬率
print(rets.head().round(3))
rets.cumsum().apply(np.exp).plot(figsize=(10, 6))  # P1 = P0 * exp(R)，当P0=1时，P1=exp(R)
print(rets.cumsum().apply(np.exp))
# plt.savefig(fig_path+'fts_03.png')
plt.show()
