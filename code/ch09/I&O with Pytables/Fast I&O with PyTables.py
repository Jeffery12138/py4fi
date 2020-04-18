# Pytables is a Python binding for the HDF5 database standard. The library's import name is tables.

# A PyTables database can have many tables, and it supports compression and
# indexing and also nontrivial queries on tables.

# In addition, it can store NumPy arrays efficiently.

import tables as tb  # The package name is Pytables, the import name is tables.
import datetime as dt
import os
import numpy as np
from pylab import plt, mpl
import numexpr as ne
import pandas as pd
import tstables as tstab
import random

plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'
fig_path = 'H:/py4fi/images/ch09/'

path = 'data/'
if not os.path.exists(path):
    os.makedirs(path)

# Working with Tables
# filename = path + 'pytab.h5'
# h5 = tb.open_file(filename, 'w')  # Open the database file in HDF5 binary storage format.
# row_des = {
#     'Date': tb.StringCol(26, pos=1),  # The Date column for date-time information (as a str object)
#     'No1': tb.IntCol(pos=2),  # The two column to store int objects
#     'No2': tb.IntCol(pos=3),
#     'No3': tb.Float64Col(pos=4),  # The two column to store float objects
#     'No4': tb.Float64Col(pos=5)
# }
#
# rows = 2000000
# filters = tb.Filters(complevel=0)  # Via Filters objects, compression levels can be specified, among other
# tab = h5.create_table('/', 'ints_floats',  # The name of this node in its parent group.
#                         row_des,  # The description of the row data structure.
#                         title='Integers and Floats',  # The name (title) of the table
#                         expectedrows=rows,  # The expected number of rows; allows for optimizations.
#                         filters=filters)
# # print(type(tab))
# print(tab)
# pointer = tab.row
# ran_int = np.random.randint(0, 10000, size=(rows, 2))
# ran_flo = np.random.standard_normal((rows, 2)).round(4)
#
# for i in range(rows):
#     pointer['Date'] = dt.datetime.now()
#     pointer['No1'] = ran_int[i, 0]
#     pointer['No2'] = ran_int[i, 1]
#     pointer['No3'] = ran_flo[i, 0]
#     pointer['No4'] = ran_flo[i, 1]
#     pointer.append()  # The new row is appended
#
# tab.flush()  # All writen rows are flushed; i.e., committed as permanent changes.
# # print(tab)

# The Python Loop is quite slow in this case. Using Numpy structured arrays instead.

# Note that the row description is not needed anymore;
# Pytables uses the dtype object of the structured array to infer the data types instead.
# dty = np.dtype([('Date', 'S26'), ('No1', '<i4'), ('No2', '<i4'), ('No3', '<f8'), ('No4', '<f8')])
#
# sarray = np.zeros(len(ran_int), dtype=dty)
# sarray['Date'] = dt.datetime.now()
# sarray['No1'] = ran_int[:, 0]
# sarray['No2'] = ran_int[:, 1]
# sarray['No3'] = ran_flo[:, 0]
# sarray['No4'] = ran_flo[:, 1]
# # print(sarray[:4])
# h5.create_table('/', 'ints_floats_from_array', sarray, title='Integer and Floats', expectedrows=rows, filters=filters)
# # print(type(h5))
# # print(h5)
# h5.remove_node('/', 'ints_floats_from_array')
# # This removes the second Table object with the redundant data.
# # print(h5)
# print(tab[:4])
# print(tab[:4]['No4'])
# print(np.sum(tab[:]['No3']))
# print(np.sum(np.sqrt(tab[:]['No1'])))

# plt.figure(figsize=(10, 6))
# plt.hist(tab[:]['No3'], bins=30)  # Plotting a column from the Table object.
# plt.savefig(fig_path+'io_05.png')
# plt.show()

# PyTables also provides flexible tools to query data via typical SQL-like statements.
# query = '((No3 < -0.5) | (No3 > 0.5)) & ((No4 < -1) | (No4 > 1))'
# iterator = tab.where(query)  # The iterator object based on the query.
# res = [(row['No3'], row['No4']) for row in iterator]
# res = np.array(res)
# print(res[:3])
# plt.figure(figsize=(10, 6))
# # 点图，x坐标， y坐标，res.T转置
# # plt.plot(res.T[0], res.T[1], 'ro')
# # plt.savefig(fig_path+'io_06.png')
# # plt.show()
# # 下面的写法更加符合直觉
# # plt.plot(res[:, 0], res[:, 1], 'ro')
# # plt.show()
#
# values = tab[:]['No3']
# print('Max %18.3f' % values.max())
# print('Ave %18.3f' % values.mean())
# print('Min %18.3f' % values.min())
# print('Std %18.3f' % values.std())

# res = [(row['No1'], row['No2']) for row in
#        tab.where('((No1 > 9800) | (No1 < 200)) & ((No2 > 4500) | (No2 < 5500))')]
# for r in res[:4]:
#     print(r)

# res = [(row['No1'], row['No2']) for row in
#        tab.where('(No1 == 1234) & (No2 > 9776)')]
# for r in res:
#     print(r)

# Working with Compressed Tables
# A major advantage of working with PyTables is the approach it takes to compression. It uses compression not only to
# save space on disk, but also to impored the performance of I/O operations in certain hardware scenarios.
# filename = path + 'pytabc.h5'
# h5c = tb.open_file(filename, 'w')
# filters = tb.Filters(complevel=5, complib='blosc')
# # The Blosc compression engine is used, which is optimized for performance.
# tabc = h5c.create_table('/', 'ints_floats', sarray, title='Integers and Floats',
#                         expectedrows=rows, filters=filters)
# query = '((No3 < -0.5) | (No3 > 0.5) & (No4 < -1) | (No4 > 1))'
# iteratorc = tabc.where(query)
# res = [(row['No3'], row['No4']) for row in iteratorc]
# res = np.array(res)
# print(res[:3])
# arr_non = tab.read()
# print(tab.size_on_disk)
# print(tab.size_in_memory)
# print(arr_non.nbytes)
#
# arr_nom = tabc.read()
# print(tabc.size_on_disk)
# print(tabc.size_in_memory)
# print(arr_nom.nbytes)
# h5c.close()
#
# # Working with Arrays
# # PyTables is also quite fast and efficient when it comes to storing and retrieving ndarray objects.
# # Writing these objects directly to an HDF5 database is faster
# than looping over the objects and writing the data row-by-row
# # to a Table object or using the approach via structured ndarray objects.
# arr_int = h5.create_array('/', 'integers', ran_int)
# arr_flo = h5.create_array('/', 'floats', ran_flo)
# print(h5)
# h5.close()

# Out-of-Memory Computations
# PyTables supports out-of-memory operations, which makes it possible
# to implement array-based computations that do not fit in memory.
# filename = path + 'earray.h5'
# h5 = tb.open_file(filename, 'w')
# n = 500  # The fixed number of column.
# ear = h5.create_earray('/', 'ear',  # The name of this node in its parent group.
#                       atom=tb.Float64Atom(),  # representing the type and shape of the atomic objects to be saved.
#                       shape=(0, n))  # The shape for instantiation (no rows, n columns).
# print(type(ear))
# rand = np.random.standard_normal((n, n))  # The ndarray object with the random numbers ...
# print(rand[:4, :4])
# for _ in range(750):
#     ear.append(rand)
# ear.flush()
# print(ear)
# print(ear.size_on_disk)
#
# # For out-of-memory computations that do not lead to aggregations,
# # another EArray object of the same shape (size) is need.
# out = h5.create_earray('/', 'out', atom=tb.Float64Atom(), shape=(0, n))
# print(out.size_on_disk)
# print(h5)
# The code that follows uses Expr to calculate the mathematical expression
# on the whole EArray object from before.
# Expr is based on the numerical expression Library numexpr.
# Transforms a str object-based expression to an Expr object.
# expr = tb.Expr('3 * sin(ear) + sqrt(abs(ear))')
# expr.set_output(out, append_mode=True)  # Defines the output to be the out EArray object.
# expr.eval()  # Initiates the evaluation of the expression.
# print(h5)
# print(out.size_on_disk)
# print(out[0, :10])
# out_ = out.read()
# print(out_[0, :10])

# As a benchmark, the in-memory performance of the numexpr module can be considered.
# expr = '3 * sin(out_) + sqrt(abs(out_))'
# t1 = dt.datetime.now()
# ne.set_num_threads(1)  # 设置1线程
#
# # Return the previous setting for the number of threads.
# # Sets a number of threads to be used in operations.
# print(ne.evaluate(expr)[0, :10])
# t2 = dt.datetime.now()
#
# ne.set_num_threads(4)  # 设置4线程
# print(ne.evaluate(expr)[:, :10])
# t3 = dt.datetime.now()
# print(t1, t2, t3)
# h5.close()

# TsTables
# The package TsTables uses PyTables to build a high-performance storage for time series data.
# It stores time series data into daily partitions and provides functions to query for subsets of data across partitions.
# Its goals are to support a workflow where tons (gigabytes) of time series data are appended periodically to a HDF5 file,
# and need to be read many times (quickly) for analytical models and research.
# pip install tstables

# Sample Data
no = 5000000  # The number of time steps.
co = 3  # The number of time series.
interval = 1. / (12 * 30 * 24 * 60)  # 1分钟有多少年
vol = 0.2
rn = np.random.standard_normal((no, co))
rn[0] = 0.0
paths = 100 * np.exp(np.cumsum(-0.5 * vol ** 2 * interval + vol * np.sqrt(interval) * rn, axis=0))  # 几何的布朗运动预测股价
paths[0] = 100
dr = pd.date_range('2019-01-01', periods=no, freq='1s')
print(dr[-6:])
df = pd.DataFrame(paths, index=dr, columns=['ts1', 'ts2', 'ts3'])
# print(df.info())
# print(df.head())
# print(df.shape)
# df[::100000].plot(figsize=(10, 6))
# plt.savefig(fig_path+'io_07.png')
# plt.show()

# Data Storage
# TsTables stores financial time series data based on a specific chunk-based structure that allows for fast retrieval of arbitrary data
# subsets defined by some time interval.
# To this end, the package adds the function create_ts() to PyTables.
# To provide the data types for the table columns, the following uses a method based on the tb.IsDescription class from PyTables.


class ts_desc(tb.IsDescription):
    timestamp = tb.Int64Col(pos=0)  # The column for the timestamps.
    ts1 = tb.Float64Col(pos=1)  # The column to store the numerical data
    ts2 = tb.Float64Col(pos=2)
    ts3 = tb.Float64Col(pos=3)


h5 = tb.open_file(path + 'tstab.h5', 'w')
ts = h5.create_ts('/', 'ts', ts_desc)  # Creates the TsTable object based on the ts_desc object.
ts.append(df)  # Appends the data from the DataFrame object to the TsTable object.
print(ts)
print(type(ts))
read_start_dt = dt.datetime(2019, 2, 1, 0, 0)
read_end_dt = dt.datetime(2019, 2, 5, 23, 59)
rows = ts.read_range(read_start_dt, read_end_dt)
print(rows.info())
print(rows.head())
h5.close()

# (rows[::500] / rows.iloc[0]).plot(figsize=(10, 6))
# plt.savefig(fig_path + 'io_08.png')
# plt.show()

# Consider the following benchmark, which retrieves 100 chunks of data
# consisting of 4 days' worth of 1-second bars.
h5 = tb.open_file(path + 'tstab.h5', 'r')
ts = h5.root.ts._f_get_timeseries()  # This connects to the TsTable object.
for _ in range(100):
    d = random.randint(1, 24)
    read_start_dt = dt.datetime(2019, 2, d, 0, 0, 0)
    read_end_dt = dt.datetime(2019, 2, d+3, 23, 59, 59)
    rows = ts.read_range(read_start_dt, read_end_dt)
    print(rows.info())
h5.close()