import pandas as pd
import numpy as np
from pylab import plt, mpl
import os

fig_paht = 'H:/py4fi/images/ch08/'
if not os.path.exists(fig_paht):
    os.makedirs(fig_paht)

plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'

tick = pd.read_csv('fxcm_eur_usd_tick_data.csv', index_col=0, parse_dates=True)
print(tick.info())
print(tick.head())
print(tick.tail())
tick['Mid'] = tick.mean(axis=1)  #中价
# tick['Mid'].plot(figsize=(10, 6))
# plt.savefig(fig_paht+'fts_14.png')
# plt.show()
tick_resam = tick.resample(rule='5min', label='right').last()
print(tick_resam.head())
print(tick_resam.shape)
tick_resam['Mid'].plot(figsize=(10, 6))
plt.savefig(fig_paht+'fts_15.png')
plt.show()
