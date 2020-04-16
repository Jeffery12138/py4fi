import numpy as np

path = 'data/'

dtimes = np.arange('2019-01-01 10:00:00', '2025-12-31 22:00:00', dtype='datetime64[m]')
print(len(dtimes))
dty = np.dtype([('Date', 'datetime64[m]'), ('No1', 'f'), ('No2', 'f')])
# Defines the special dtype object for the structured array
data = np.zeros(len(dtimes), dtype=dty)
# Instantiates an ndarray object with the special dtype.
print(data.dtype)
data['Date'] = dtimes
print(data)
a = np.random.standard_normal((len(dtimes), 2)).round(4)
data['No1'] = a[:, 0]
data['No2'] = a[:, 1]
print(data.nbytes)
np.save(path+'array', data)  # 存取
np.load(path+'array.npy')  # 读入
data = np.random.standard_normal((10000, 6000)).round(4)
print(data.nbytes)
np.save(path+'array', data)
print(np.load(path+'array.npy'))