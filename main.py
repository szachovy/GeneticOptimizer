#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'WJ Maj'

import timeit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src import *

#pyspark
#cython
#datetime
# tempfile with latest configuration

class Genetic_Optimizer(Load_Population):
#    def __mro__()
    def __init__(self, mnt = 5):
        super().__init__(mnt)
#        print(mro())
#        print(self.a)


if __name__ == '__main__':
    gen = Genetic_Optimizer()
