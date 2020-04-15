import numpy as np
import pandas as pd
import os
from pylab import plt, mpl

plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'

fig_path = 'H:/py4fi/images/ch08/'
if not os.path.exists(fig_path):
    os.makedirs(fig_path)

raw = pd.read_csv('tr_eikon_eod_data.csv', index_col=0, parse_dates=True)
data = raw[['.SPX', '.VIX']].dropna()
print(data.tail())
# data.plot(subplots=True, figsize=(10, 6))
# plt.savefig(fig_path+'fts_08.png')
# data.loc[:'2012-12-31'].plot(secondary_y='.VIX', figsize=(10, 6))
# plt.savefig(fig_path+'fts_09.png')
# plt.show()
print(data.loc[:'2012-12-31'].tail())
rets = np.log(data/data.shift(1))
print(rets.head())
rets.dropna(inplace=True)
rets.plot(subplots=True, figsize=(10, 6))
# plt.savefig(fig_path+'fts_10.png')
# pd.plotting.scatter_matrix(rets, alpha=0.2, diagonal='hist', hist_kwds={'bins':35}, figsize=(10, 6))  # alpha=0.2透明度
# plt.savefig(fig_path+'fts_11.png')
# pd.plotting.scatter_matrix(rets, alpha=0.2, diagonal='kde', figsize=(10, 6))
# plt.show()
reg = np.polyfit(rets['.SPX'], rets['.VIX'], deg=1)  # b1 b0 x, y  y=b1x+b0       线性回归，最小平方法
ax = rets.plot(kind='scatter', x='.SPX', y='.VIX', figsize=(10, 6))
ax.plot(rets['.SPX'], np.polyval(reg, rets['.SPX']), 'r', lw=2)
plt.savefig(fig_path+'fts_12.png')
# plt.show()
print(rets.corr().iloc[0, 1])
# ax = rets['.SPX'].rolling(window=252).corr(rets['.VIX']).plot(figsize=(10, 6))
# ax.axhline(rets.corr().iloc[0, 1], c='r')
ax = pd.DataFrame(rets['.SPX'].rolling(window=252).corr(
                  rets['.VIX'])).plot(figsize=(10, 6))  # 要把Series Class转变为Data Frame Class，否则plot会报错
print(type(ax))
ax.axhline(rets.corr().iloc[0, 1], c='r')
plt.savefig(fig_path+'fts_13.png')
plt.show()
