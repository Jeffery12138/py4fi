#
# Monte Carlo valuation of European call option
# in Black-Scholes-Merton model
# bsm_mcs_euro.py
#
# Python for Finance, 2nd ed.
# (c) Dr. Yves J. Hilpisch
#
import math
import numpy as np

# Parameter Values 设置参数
S0 = 100.  # initial index level 初始值
K = 105.  # strike price 股票价格
T = 1.0  # time-to-maturity 到期时间
r = 0.05  # riskless short rate 无风险的短期利率
sigma = 0.2  # volatility 年化报酬率？

I = 100000  # number of simulations 模拟次数

# Valuation Algorithm 评估算法
z = np.random.standard_normal(I)  # pseudo-random numbers 伪随机数，I个
# index values at maturity 到期时的指数值
ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T + sigma * math.sqrt(T) * z)  #向量化的计算方法
hT = np.maximum(ST - K, 0)  # payoff at maturity 到期收益
C0 = math.exp(-r * T) * np.mean(hT)  # Monte Carlo estimator 蒙特卡洛估计

# Result Output 结果输出
print('Value of the European call option %5.3f.' % C0)  ##格式化输出，小数点后3位的浮点数，共占5位。
