import pandas as pd
import numpy as np
import os
import csv

path = 'data/'
if not os.path.exists(path):
    os.makedirs(path)

rows = 5000
a = np.random.standard_normal((rows, 5)).round(4)
print(a)
t = pd.date_range(start='2019/1/1', periods=rows, freq='H')  # 生成时间，起始时间，时间个数，时间间隔，H：小时
print(t)

csv_file = open(path+'data.csv', 'w')
headers = 'date, no1, no2, no3, no4, no5\n'
csv_file.write(headers)
for t_, (no1, no2, no3, no4, no5) in zip(t, a):
    s = '{}, {}, {}, {}, {}, {}\n'.format(t_, no1, no2, no3, no4, no5)
    csv_file.write(s)
csv_file.close()
csv_file = open(path+'data.csv', 'r')
print(csv_file.readline())
print(csv_file.readline())
for i in range(5):
    print(csv_file.readline(), end='')
csv_file.close()
csv_file = open(path+'data.csv', 'r')
content = csv_file.readlines()
print(content[:5])
csv_file.close()

with open(path+'data.csv', 'r') as f:
    csv_reader = csv.reader(f)  # csv.reader(f)
    lines = [line for line in csv_reader]  # Return a list of List objects
print(lines[:5])

with open(path+'data.csv', 'r') as f:
    csv_reader = csv.DictReader(f)  # csv.DictReader(f)
    lines = [line for line in csv_reader]  # Returns a List of dict objects.

print(lines[:3])