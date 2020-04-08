import math
import timeit

loops = 2500000
a = range(1, loops)


def f():
    for x in range(1, 2500000):
        return 3*math.log(x)+math.cos(x)**2


if __name__ == '__main__':
    print(timeit.timeit("f()", setup="from __main__ import f"))


## 总用时 1.3574408s