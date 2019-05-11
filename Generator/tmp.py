#!/usr/bin/env python3
import numpy as np
import pandas as pd
import random
import csv

population_size = 46
chromosome_size = 8

#min_gene = float(input('min : '))
#max_gene = float(input('max : '))

DEFAULT_PRECISION = 2
chromosomes = []

args = random.randint(0,1)
def func(args):
    for chromosome_layer in range(population_size):
        chromosomes.append([fun(args) for gene in range(chromosome_size)])

    population = pd.DataFrame(data=chromosomes)
    return population

def fun()


print(func(args))