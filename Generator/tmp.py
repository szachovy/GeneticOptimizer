#!/usr/bin/env python3
import numpy as np
import pandas as pd
import random
import csv
# a = "a"
# 
# def check(a):
    # try:
        # a = int(a)
    # except ValueError as e:
        # print("ValueError raised")
# 
    # return type(a)
# 
# print(check(a))

#print(pd.DataFrame(data=np.random.randint(2, size=(46, 8))))



#population = pd.DataFrame(data=np.random.randint(2, size=(46, 8)))
#population = pd.DataFrame(data=np.random.randint(1,5, size=(46,8)))

a = 5
b = 13
step = 0.05
#print(random.random())

#print([round(random.uniform(2.5,22.5), 2) for i in range(5)])
# must be an int
pop_size = 46
chr_size = 8

#print(np.random.permutation([a+i for i in range(b-a)]))

#population = pd.DataFrame(data=)
#print(population)

#a = (1,2,3)
a = random.randint(0, 1)

perm = True

def func(*args):
    e = iter(args)
    yield e
#    e = *args
#    print([e for i in range(5)])

func(a)

a = input('co zapisac : ')
print("../DataSets/{}.csv".format(a))


class A(object):
    def __init__(self):
        print("jest a")
    
    def f(self):
        print('czy siadzie?')


class B(A):
    
    def __init__(self):
        print('jest b')        
        new = A()

    def s(self):
        new.f()

n = B().s()





