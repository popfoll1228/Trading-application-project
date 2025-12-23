#1_Import
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#2_Read data [Day,Time,Open,High,Low,Close]
txtname = input('Enter name of the data file: ')
data =pd.read_excel(txtname)   #USERINPUT
datalist = data.values.tolist()
