"""
Created on Mon Sep 12 23:45:28 2016

@author: deepesh singh
"""
import pandas as pd
import numpy as np
import math
from math import isnan
from pulp import *
from collections import Counter
from more_itertools import unique_everseen

# sales=pd.read_csv("sales_lift.csv",header=None)
sales=pd.read_csv("sales_lift_input.csv",header=None)

lift=sales.iloc[2:,1:]
lift=np.array(lift)
lift = lift.astype(np.int) # read the lifts from csv
brands=sales.iloc[0:1,:]
brands=np.array(brands)
brands=np.delete(brands,0)
brands=brands.tolist()  # read the brands from csv
ff=Counter(brands)
all_brands=ff.items()
# the racks and the shelfs available
rack_shelf=[[1,1,2,3],[2,4,5,6],[3,7,8,9,10]]

col_con=[1,0,0,2,2,3,1,1]

order=list(unique_everseen(brands))
order_map = {}
for pos, item in enumerate(order):
    order_map[item] = pos
    
brands_lift=sorted(all_brands, key=lambda x: order_map[x[0]])
#*************GREEDY ALGORITHM******************************

x1=len(lift[0]) # get the input matrix size
x2=len(lift)
var=np.zeros(shape=(x2,x1)) # decision variable matrix
#recursive function
def fun1(lift):
    max_index=np.where(lift==lift.max())
    max_index=list(max_index)
    ss=np.array(max_index).reshape(-1).tolist()
    length=len(ss)
    x=length/2
    row=int(ss[0])
    col=int(ss[x])
    lift=np.squeeze(np.asarray(lift))
    if lift[row][col]!=0:
        if (sum(var[row])==0 and np.sum(var,axis=0)[col]<col_con[col]):
            var[row][col]=1
            lift=np.squeeze(np.asarray(lift))
            lift[row]=0
            fun1(lift)
        else:
            lift[row][col]=0
            fun1(lift)
           
fun1(lift)       
#retreive the original lift matrix       
lift2=sales.iloc[2:,1:]
lift2=np.array(lift2)
lift2 = lift2.astype(np.int) # read the lifts from csv
print("the max lift obtained is:",np.sum((var*lift2)))

print ("The decision variable matrix is:")
var=var.astype(int)
print((var))
