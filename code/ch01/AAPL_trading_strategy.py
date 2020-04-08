import numpy as np
import pandas as pd
from sklearn.svm import SVC
from matplotlib.pylab import plt, mpl
import os

data_path = 'H:/py4fi/py4fi2nd-master/py4fi2nd-master/images/ch01/'
data = pd.read_csv('tr_eikon_eod_data.csv', index_col=0, parse_dates=True)

data = pd.DataFrame(data['AAPL.O'])
data.dropna(inplace=True)
data['Returns'] = np.log(data/data.shift(1))

lags = 6
cols = []
for lag in range(1, lags+1):
    col = 'lag_{}'.format(lag)
    data[col] = np.sign(data['Returns'].shift(lag))  ##np.sign(>0)=1, np.sign(<0)=-1, 取data['Return']值得正负，往下移动lag位
    cols.append(col)

data.dropna(inplace=True)

model = SVC(gamma='scale')
model.fit(data[cols], np.sign(data['Returns']))
data['Prediction'] = model.predict(data[cols])

data['Strategy'] = data['Prediction']*data['Returns']  ##预测收益

plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'

data[['Returns', 'Strategy']].cumsum().apply(np.exp).plot(figsize=(10, 6))
plt.savefig(data_path+'AAPL_trading_strategy.png')

data['Prediction'].plot(figsize=(10, 3))
plt.savefig(data_path+'sign_prediction.png')

data['Number'] = np.where(data.Prediction != data.Prediction.shift(), 1, 0)
print(data['Number'].cumsum()) ##总共买进卖出交易902次，扣除风险和手续费，实际并没有预测的那么高的收益

# print(data[['Returns', 'Strategy']].cumsum().apply(np.exp))  ##累计收益之和，前1天，前2天，。。。前n天

print(data.head(15))


