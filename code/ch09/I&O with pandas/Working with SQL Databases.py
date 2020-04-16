import pandas as pd
import numpy as np
import os
import sqlite3 as sq3
from pylab import plt, mpl

plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'

path = 'data/'
fig_path = 'H:/py4fi/images/ch09/'
if not os.path.exists(path):
    os.makedirs(path)
if not os.path.exists(fig_path):
    os.makedirs(fig_path)

data = np.random.standard_normal((1000000, 5)).round(4)
print(data[:3])
filename = path + 'numbers'
con = sq3.Connection(filename + '.db')
query = 'CREATE TABLE numbers (No1 real, No2 real, No3 real, No4 real, No5 real)'
q = con.execute
qm = con.executemany
q(query)
qm('INSERT INTO numbers VALUES (?, ?, ?, ?, ?)', data)
con.commit()
# temp = q('SELECT * FROM numbers').fetchall()
# print(temp[:3])
# print(np.array(temp).shape)
# query = 'SELECT * FROM numbers WHERE No1 > 0 AND No2 < 0'
# res = np.array(q(query).fetchall()).round(3)
# print(res[:5])
# print(res.shape)
# res = res[::100]  # 全部抓取，步长100
# plt.figure(figsize=(10, 6))
# plt.plot(res[:, 0], res[:, 1], 'ro')
# plt.savefig(fig_path+'io_01.png')
# plt.show()
# print(res.shape)

# From SQL to Pandas
data = pd.read_sql('SELECT * FROM numbers', con)
# Reading the whole table with pandas takes roughly the same amount of time as reading it into a Numpy
print(data.head())

# The data is now in-memory, which allows for much faster analytics
# print(data[(data['No1'] > 0) & (data['No2'] < 0)].head())
#
# q = '(No1 < -0.5 | No1 > 0.5) & (No2 < -1 | No2 > 1)'
# res = data[['No1', 'No2']].query(q)
# print(res[:5])
# plt.figure(figsize=(10, 6))
# plt.plot(res['No1'], res['No2'], 'ro')
# plt.savefig(fig_path+'io_02.png')
# plt.show()

# Data as h5s File
h5s = pd.HDFStore(filename + '.h5s', 'w')  # pandas an HDFStore object is created.
h5s['data'] = data
# The complete DataFrame object is stored in the database file via binary storage.
h5s.close()
h5s = pd.HDFStore(filename+'.h5s', 'r')
data_ = h5s['data']  # The DataFrame is read and stored in-memory as data_.
h5s.close()
print(data_.head())
print(data_ is data)  # To check if two reference refer to the same object. The two DataFrame objects are not same.
print((data_ == data).all())  # ...but they now contain the same data
print(np.allclose(data_, data))

# Data as CSV File
data.to_csv(filename+'.csv')
df = pd.read_csv(filename+'.csv')
df[['No1', 'No2', 'No3', 'No4']].hist(bins=20, figsize=(10, 6))
plt.savefig(fig_path+'io_03.png')
plt.show()

# Data as Excel File
data[:100000].to_excel(filename+'.xlsx')  # The data set is restricted to 100,000 rows
df = pd.read_excel(filename+'.xlsx', sheet_name='Sheet1')
print(df.head())
df[['No1', 'No2', 'No3', 'No4', 'No5']].cumsum().plot(figsize=(10, 6))
plt.savefig(fig_path+'io_04.png')
plt.show()




