from pylab import plt, mpl
import pickle
import numpy as np
from random import gauss
import os

plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'

path = 'data/'
if not os.path.exists(path):
    os.makedirs(path)

a = [gauss(1.5, 2) for i in range(1000000)]  # 平均数1.5，标准差2

pkl_file = open(path+'data.pkl',  'wb')  # 二进制写入
pickle.dump(a, pkl_file)
pkl_file.close()
pkl_file = open(path+'data.pkl', 'rb')  # 二进制读入
b = pickle.load(pkl_file)
print(a[:3])
print(b[:3])
print(np.allclose(np.array(a), np.array(b)))  # 比较两个阵列是否完全一样
pkl_file.close()
pkl_file = open(path+'data.pkl', 'wb')
pickle.dump(np.array(a), pkl_file)
pickle.dump(np.array(a)**2, pkl_file)
pkl_file.close()

# Reading the two ndarray objects back into memory.
# Pickle stores objects according to the first in, first out(FIFO) principle
pkl_file = open(path+'data.pkl', 'rb')
x = pickle.load(pkl_file)
print(x[:4])
y = pickle.load(pkl_file)
print(y[:4])
pkl_file.close()

# Store a dict object containing all the other objects

pkl_file = open(path+'data.pkl', 'wb')
pickle.dump({'x': x, 'y': y}, pkl_file)
pkl_file.close()

pkl_file = open(path+'data.pkl', 'rb')
data = pickle.load(pkl_file)
pkl_file.close()

for key in data.keys():
    print(key, data[key][:4])