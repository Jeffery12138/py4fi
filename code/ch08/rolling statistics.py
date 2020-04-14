import pandas as pd
import numpy as np
from pylab import plt, mpl
import os

plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'

fig_path = 'H:/py4fi/images/ch08/'
if not os.path.exists(fig_path):
    os.makedirs(fig_path)

filename = 'tr_eikon_eod_data.csv'
data = pd.read_csv(filename, index_col=0, parse_dates=True)
sym = 'AAPL.O'
data = pd.DataFrame(data[sym]).dropna()
print(data.tail())
window = 20
data['min'] = data[sym].rolling(window=window).min()
data['mean'] = data[sym].rolling(window=window).mean()
data['std'] = data[sym].rolling(window=window).std()
data['median'] = data[sym].rolling(window=window).median()
data['max'] = data[sym].rolling(window=window).max()
data['ewma'] = data[sym].ewm(halflife=0.5, min_periods=window).mean()  # 多种方法其实都是用来设置alpha
# print(data.dropna().head())
# ax = data[['min', 'mean', 'max']].iloc[-200:].plot(figsize=(10, 6), style=['g--', 'r--', 'g--'], lw=0.8)
# data[sym].iloc[-200:].plot(figsize=(10, 6), lw=2.0)  # .iloc 切片取行 .iloc[-200:]取最后200行
# plt.show()
# data[sym].iloc[-200:].plot(ax=ax, lw=2.0)
# plt.savefig(fig_path+'fts_05.png')
# # plt.show()

data['SMA1'] = data[sym].rolling(window=42).mean()
data['SMA2'] = data[sym].rolling(window=252).mean()
print(data[[sym, 'SMA1', 'SMA2']].tail())
# data[[sym, 'SMA1', 'SMA2']].plot(figsize=(10, 6))
# plt.savefig(fig_path+'fts_06.png')
# plt.show()
data.dropna(inplace=True)
print(data)
data['positions'] = np.where(data['SMA1']>data['SMA2'], 1, -1)
ax = data[[sym, 'SMA1', 'SMA2', 'positions']].plot(figsize=(10, 6), secondary_y='positions')  # 第二个y轴 数据为'positions'
ax.get_legend().set_bbox_to_anchor((0.25, 0.85))  # 设置图例位置
plt.savefig(fig_path+'fts_07.png')
plt.show()
