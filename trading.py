#1_Import
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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

long = long_order(datalist, nc, delta = 0.2)
short = short_order(datalist, nc, delta = 0.2)
osci = oscillate(datalist, ncc, delta = 0.03)
long_final_indices = intersection_indices(long,osci)
short_final_indices = intersection_indices(short,osci)
print(len(long_final_indices))
print(len(short_final_indices))

#4


