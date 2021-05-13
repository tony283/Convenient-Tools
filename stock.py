import math
import datetime
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt


class StockDetect:
    def __init__(self, data=None):
        if data and isinstance(data, (list, tuple)) and isinstance(data[0], (int, float)):
            self.it = data
            self.com_list = []
            self.ab_list = []
            self.ang_list = []
            self.num = 0
            self.stock_name = None
            self.start = None
            self.fit = []
            print("Data loaded...")
        elif not data:
            print("Empty StockDetector added.\nUsing 'add_stock' command to add stock list.")

        else:
            print("Data Error. Initialization failed.")

    def dft(self):
        self.num = len(self.fit)  # num of days
        summary = []
        for i in range(self.num):
            total_sin = 0
            total_cos = 0
            for j in range(self.num):
                total_sin += self.fit[j] * math.sin(2 * math.pi * (i / self.num) * j)
                total_cos += self.fit[j] * math.cos(2 * math.pi * (i / self.num) * j)
            z = complex((total_cos * 2) / self.num, (total_sin * 2) / self.num)
            summary.append(z)
        self.com_list = summary.copy()
        self.ab_list = [abs(z) for z in self.com_list]
        self.ang_list = [math.atan(z.imag / z.real) * (180 / math.pi) for z in self.com_list]
        print("Successful DFT Try.")

    def reach_mod(self):
        if self.ab_list:
            return self.ab_list
        else:
            print("Missing ab_list...")

    def reach_angle(self):
        if self.ang_list:
            return self.ang_list
        else:
            print("Missing ang_list...")

    def add_stock(self, stock_id, start, end=datetime.date.today(), search_engine='yahoo'):
        self.stock_name = stock_id
        self.it = []
        self.start = start
        temp1 = []
        temp2 = []
        stock_info = web.DataReader(self.stock_name, search_engine, start, end)  # 'econdb', 'yahoo'
        close = stock_info['Close']
        for i in close:
            temp1.append(i)
        leng1 = len(close)
        for j in range(leng1):
            day_index = stock_info.index[j].__sub__(stock_info.index[0])
            temp2.append(int(day_index.days))
        for k in range(leng1-1):
            minus = temp2[k + 1] - temp2[k]
            self.it.append(temp1[k])
            if 1 == minus:
                continue
            else:
                delta = temp1[k+1] - temp1[k]
                for h in range(minus - 1):
                    self.it.append(temp1[k] + delta * (h+1) / minus)
        self.it.append(temp1[-1])
        print('Price List of Stock ID %s from ' % self.stock_name + \
              str(start.strftime('%y-%m-%d')) + ' to ' + str(end.strftime('%y-%m-%d')) + ' is loaded!')

    def plot_stock(self, ab=True, ag=False):
        size = self.num - 1
        t_list = [self.num / (i+1) for i in range(size)]
        t = np.array(t_list, dtype=float)  # t is term
        if ab:
            yab = self.ab_list[:]
            del yab[0]
            ab_st = np.array(yab)
            plt.plot(t, ab_st)
            plt.xlabel('Period (Days)')
            plt.ylabel('Correlation')
            plt.title('Correlation Plot for Stock %s' % self.stock_name)
            plt.show()
        if ag:
            yag = self.ang_list[:]
            del yag[0]
            ab_st = np.array(yag)
            plt.plot(t, ab_st)
            plt.xlabel('Period (Days)')
            plt.ylabel('Phase')
            plt.title('Phase Plot for Stock %s' % self.stock_name)
            plt.show()
        print('Successful Plotted')

    def fit(self):
        print('fitting starts.')
        l = len(self.it)
        temp_list = []
        for i in range(365):
            temp = sum(self.it[0:i+1]) / (i + 1)
            temp_list.append(temp)
        for j in range(l - 366):
            temp =sum(self.it[j+1:j+366]) / 365
            temp_list.append(temp)
        temp = sum(self.it[l-365:]) / 365
        temp_list.append(temp)
        self.fit = [self.it[i] - temp_list[i] for i in range(l)]
        print('fitting succeeded')

    def empty(self):
        if self.it:
            return False
        else:
            return True


def acquire(id, start):
    temp = StockDetect()
    temp.add_stock(id, start)
    temp.fit()
    temp.dft()
    temp.plot_stock()

if __name__ == '__main__':
    acquire('002382.SZ', datetime.datetime(2016, 1, 1))