#1_Import
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import time
from functools import reduce
import operator

#2_Read data [Day,Time,Open,High,Low,Close]
txtname = input('Enter name of the data file: ') #USERINPUT
data =pd.read_excel(txtname)   
datalist = data.values.tolist()

#3 By data find order condition
nc = int(input('Bars for checking: ')) #USERINPUT_exp(x,xs)
ncc = int(input('Bars for oscillate: ')) #USERINPUT_exp(xo)

def long_order(data, x, delta = 0.2):
    datalist2 = data        
    k = x
    ordercheck_long = []
    for i in range(len(datalist2)):
        if i - k + 1 >= 0:
            prev = datalist2[i - k + 1][2]
            curr = datalist2[i][2]
            ampl = round(100*((curr - prev)/prev) , 3)
            if ampl >= delta:
                ordercheck_long.append(i)
    return ordercheck_long

def short_order(data, xs, delta = 0.2):
    datalist3 = data        
    k = xs
    ordercheck_short = []
    for i in range(len(datalist3)):
        if i - k + 1 >= 0:
            prev = datalist3[i - k + 1][2]
            curr = datalist3[i][-1]
            ampl = round(100*((curr - prev)/prev) , 3)
            if ampl <= -delta:
                ordercheck_short.append(i)
    return ordercheck_short

def oscillate(data, xo, delta = 0.01):
    o_o = data[:]
    index = []
    k = xo
    for i in range(len(o_o)):
        ok = True
        if i + k -1 < len(o_o):
            for j in range(1, k):
                prev = o_o[i + j - 1][-1]
                curr = o_o[i + j][-1]
                ampl = abs(100 * (curr - prev) / prev)
                if ampl > delta:
                    ok = False
                    break
        else:
            ok = False
        if ok:
            index.append(i)
    return index

def intersection_indices(list1, list2):
    set2 = set(list2)
    return [i for i in list1 if i in set2]

def remove_indices_in_time_range(indices, datalist, start_hour=2, start_minute=0, end_hour=9, end_minute=0):
    start_time = time(start_hour, start_minute)
    end_time   = time(end_hour, end_minute)
    filtered = []
    for i in indices:
        t = datalist[i][1] 
        if hasattr(t, 'time'):
            t = t.time()
        if not (start_time <= t <= end_time):
            filtered.append(i)
    return filtered

long = long_order(datalist, nc, delta = 0.2)
short = short_order(datalist, nc, delta = 0.2)
osci = oscillate(datalist, ncc, delta = 0.03)
long_indices = intersection_indices(long,osci)
short_indices = intersection_indices(short,osci)
long_final_indices = remove_indices_in_time_range(long_indices, datalist, start_hour=2, start_minute=0, end_hour=9, end_minute=0)
short_final_indices = remove_indices_in_time_range(short_indices, datalist, start_hour=2, start_minute=0, end_hour=9, end_minute=0)

#4 Order to TP/SL, no more margin, certain period
def tpl(tm, pm): #tp's list
    tp = np.linspace(tm, pm, 100)
    tpl = tp.tolist()
    return tpl

def sll(tpl, a, b): #sl's list
    sll =[]
    rt = np.linspace(a,b, 100)
    k = np.array(tpl)
    for i in range(100):
        x = k * rt[i]
        sll.append(x.tolist())
    return sll

def final_long(e, d, data, indices, lev, timeframe, tpl, sll):    #same order, sl = (e(ratio),d(tp value))
    index = indices[:]
    pct = []
    while index != []:
        c = index[0]
        f = 1
        start = data[c][2]
        tpp = start * (1 + tpl[d]/100)
        slp = start * (1 - sll[e][d]/100)
        bep = start * (1 - 0.5 / lev)
        while True:            
            if len(index) > 1 and c+f == index[1]:
                index.remove(index[1])
            high = data[c+f][3]
            low = data[c+f][4]
            if low <= bep:
                pct.clear()
                pct.append(-1)
                return pct
            if high >= tpp:
                pct.append(1+tpl[d]/100)
                f = 0
                index.remove(c)
                break
            elif low <= slp:
                pct.append(1-sll[e][d]/100)
                f = 0
                index.remove(c)
                break
            else:
                f += 1
                if f == timeframe:
                    close = data[c+f-1][-1]
                    pct.append((close-start)/start*100)
                    index.remove(c)
                    break
    return pct

def final_short(e, d, data, indices, lev, timeframe, tpl, sll):    #same order, sl = (e(ratio),d(tp value))
    index = indices[:]
    pct = []
    while index != []:
        c = index[0]
        f = 1
        start = data[c][2]
        tpp = start * (1 - tpl[d]/100)
        slp = start * (1 + sll[e][d]/100)
        bep = start * (1 + 0.5 / lev)
        while True:            
            if len(index) > 1 and c+f == index[1]:
                index.remove(index[1])
            high = data[c+f][3]
            low = data[c+f][4]
            if high >= bep:
                pct.clear()
                pct.append(-1)
                return pct
            if low <= tpp:
                pct.append(1+tpl[d]/100)
                f = 0
                index.remove(c)
                break
            elif high >= slp:
                pct.append(1-sll[e][d]/100)
                f = 0
                index.remove(c)
                break
            else:
                f += 1
                if f == timeframe:
                    close = data[c+f-1][-1]
                    pct.append((start-close)/start*100)
                    index.remove(c)
                    break
    return pct

margin = float(input('Enter your margin at start: '))
leverage = int(input('Enter leverage: '))
ratio_max = int(input('Enter maximum ratio: ')) #b
ratio_min = int(input('Enter minimum ratio: ')) #a
tp_max = float(input('Enter maximum TP%: ')) #pm
tp_min = float(input('Enter minimum TP%: ')) #tm
tim = int(input('How long you want to wait? '))

tplf = tpl(tp_min, tp_max)
sllf = sll(tplf, ratio_min, ratio_max)

longl = []
shortl = []
m = 0
while m < len(sllf) :
    n = 0
    while n < len(tplf):
        m1 = m
        m2 = m 
        n1 = n
        n2 = n
        longl.append(final_long(m1, n1, datalist, long_final_indices, leverage, tim, tplf, sllf))
        shortl.append(final_short(m2, n2, datalist, short_final_indices, leverage, tim, tplf, sllf))
        n += 1
    m += 1

print(longl)
print(shortl)





