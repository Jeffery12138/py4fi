# Pytables is a Python binding for the HDF5 database standard. The library's import name is tables.

# A PyTables database can have many tables, and it supports compression and
# indexing and also nontrivial queries on tables.

# In addition, it can store NumPy arrays efficiently.

import tables as tb  # The package name is Pytables, the import name is tables.
import datetime as dt
import os
import numpy as np
from pylab import plt, mpl

plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'
fig_path = 'H:/py4fi/images/ch09/'

path = 'data/'
if not os.path.exists(path):
    os.makedirs(path)

# Working with Tables
filename = path + 'pytab.h5'
h5 = tb.open_file(filename, 'w')  # Open the database file in HDF5 binary storage format.
row_des = {
    'Date': tb.StringCol(26, pos=1),  # The Date column for date-time information (as a str object)
    'No1': tb.IntCol(pos=2),  # The two column to store int objects
    'No2': tb.IntCol(pos=3),
    'No3': tb.Float64Col(pos=4),  # The two column to store float objects
    'No4': tb.Float64Col(pos=5)
}

rows = 2000000
filters = tb.Filters(complevel=0)  # Via Filters objects, compression levels can be specified, among other
tab = h5.create_table('/', 'ints_floats',  # The name of this node in its parent group.
                        row_des,  # The description of the row data structure.
                        title='Integers and Floats',  # The name (title) of the table
                        expectedrows=rows,  # The expected number of rows; allows for optimizations.
                        filters=filters)
# print(type(tab))
# print(tab)
pointer = tab.row
ran_int = np.random.randint(0, 10000, size=(rows, 2))
ran_flo = np.random.standard_normal((rows, 2)).round(4)

for i in range(rows):
    pointer['Date'] = dt.datetime.now()
    pointer['No1'] = ran_int[i, 0]
    pointer['No2'] = ran_int[i, 1]
    pointer['No3'] = ran_flo[i, 0]
    pointer['No4'] = ran_flo[i, 1]
    pointer.append()  # The new row is appended

tab.flush()  # All writen rows are flushed; i.e., committed as permanent changes.
# print(tab)

# The Python Loop is quite slow in this case. Using Numpy structured arrays instead.

# Note that the row description is not needed anymore;
# Pytables uses the dtype object of the structured array to infer the data types instead.
dty = np.dtype([('Date', 'S26'), ('No1', '<i4'), ('No2', '<i4'), ('No3', '<f8'), ('No4', '<f8')])

sarray = np.zeros(len(ran_int), dtype=dty)
sarray['Date'] = dt.datetime.now()
sarray['No1'] = ran_int[:, 0]
sarray['No2'] = ran_int[:, 1]
sarray['No3'] = ran_flo[:, 0]
sarray['No4'] = ran_flo[:, 1]
# print(sarray[:4])
h5.create_table('/', 'ints_floats_from_array', sarray, title='Integer and Floats', expectedrows=rows, filters=filters)
# print(type(h5))
# print(h5)
h5.remove_node('/', 'ints_floats_from_array')
# This removes the second Table object with the redundant data.
# print(h5)
# print(tab[:4])
# print(tab[:4]['No4'])
# print(np.sum(tab[:]['No3']))
# print(np.sum(np.sqrt(tab[:]['No1'])))

# plt.figure(figsize=(10, 6))
# plt.hist(tab[:]['No3'], bins=30)  # Plotting a column from the Table object.
# plt.savefig(fig_path+'io_05.png')
# plt.show()

# PyTables also provides flexible tools to query data via typical SQL-like statements.
query = '((No3 < -0.5) | (No3 > 0.5)) & ((No4 < -1) | (No4 > 1))'
iterator = tab.where(query)  # The iterator object based on the query.
res = [(row['No3'], row['No4']) for row in iterator]
res = np.array(res)
print(res[:3])
plt.figure(figsize=(10, 6))
# 点图，x坐标， y坐标，res.T转置
# plt.plot(res.T[0], res.T[1], 'ro')
# plt.savefig(fig_path+'io_06.png')
# plt.show()
# 下面的写法更加符合直觉
# plt.plot(res[:, 0], res[:, 1], 'ro')
# plt.show()

values = tab[:]['No3']
print('Max %18.3f' % values.max())
print('Ave %18.3f' % values.mean())
print('Min %18.3f' % values.min())
print('Std %18.3f' % values.std())

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
filename = path + 'pytabc.h5'
h5c = tb.open_file(filename, 'w')
filters = tb.Filters(complevel=5, complib='blosc')
# The Blosc compression engine is used, which is optimized for performance.
tabc = h5c.create_table('/', 'ints_floats', sarray, title='Integers and Floats',
                        expectedrows=rows, filters=filters)
query = '((No3 < -0.5) | (No3 > 0.5) & (No4 < -1) | (No4 > 1))'
iteratorc = tabc.where(query)
res = [(row['No3'], row['No4']) for row in iteratorc]
res = np.array(res)
print(res[:3])
arr_non = tab.read()
print(tab.size_on_disk)
print(tab.size_in_memory)
print(arr_non.nbytes)

arr_nom = tabc.read()
print(tabc.size_on_disk)
print(tabc.size_in_memory)
print(arr_nom.nbytes)
h5c.close()