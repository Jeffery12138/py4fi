import numpy as np
import pandas as pd
from matplotlib.pylab import plt, mpl
import os
data_path = 'H:/py4fi/py4fi2nd-master/py4fi2nd-master/images/ch01/'

#设置绘图格式，字体格式
plt.style.use('seaborn')  ##绘图格式seaborn
mpl.rcParams['font.family'] = 'serif'  ##字体格式serif
# %matplotlib inline

#读入本地CSV文档
data = pd.read_csv('tr_eikon_eod_data.csv', index_col=0, parse_dates=True)
#index_col=0 把colume=0的那一列作为标签
#parse_dates=True 格式化日期，去除空格之后的内容？or保留年月日，去除时分秒?
# print(data.head(15))  ##打印前15行
# print(data.tail(15))  ##打印后15行

#取出某一列
# data = data['.SPX']  ##一维结果，pandas里面的series
# data = data[['.SPX']]  ##二维结果
data = pd.DataFrame(data['.SPX'])  ##二维结果, DataFrame格式，与上行等价
# print(data.head(15))

#去除missing data
data.dropna(inplace=True)  ##原位直接更改，不留副本
# print(data.head(15))

##获取data信息
# print(data.info())

#计算报酬率

#间断时间报酬率 R=(P1-P0)/P0 不具可加性 pandas内置方法计算
# print(data.pct_change().head(15))
#连续时间报酬率 R=Ln(P1/P0) 具有可加性 手动自己算
# print(data.shift(1).head(15))  ##将每一个数字向前一天移1位
data['rets'] = np.log(data/data.shift(1))  ##新建一列保存连续报酬率
# print(data.head(15))

#计算日波动度
# data['rets'].rolling(252).std() ##前252个交易日（包括今天）的日报酬率的标准差即为今天的日波动度
#计算年波动度
data['vola'] = data['rets'].rolling(252).std()*np.sqrt(252)  ##日波动度乘以根号T
# data['vola'] = data['rets'].rolling(252, min_periods=30).std()*np.sqrt(252)
# ##rolling中的min_periods方法，等于30意味30个数据即开始计算，31,32,33.....后面的数据直接加入进行计算，直到252个数据，
# 然后加入最后一个数据，去除最前一个数据，保持252的window开始rolling，数据耗损量不会太大
# print(data.head(15))

#开始画图
data[['.SPX', 'vola']].plot(subplots=True, figsize=(10, 6))
if not os.path.exists(data_path):
    os.mkdir(data_path)
plt.savefig(data_path+'spx_volatility.png')