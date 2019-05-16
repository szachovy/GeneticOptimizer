#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'WJ Maj'

from src.conf_handler import Load_Configuration
from Generator.generator import Generator
from src.preprocessing import Preprocess_Dataframe
from src.fitness import Fitness
from src.meta import Implement_Func

import timeit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from configparser import ConfigParser

#pyspark
# tempfile with latest configuration

def check_file(opt):
    def wrapper(*args):
        try:
            if args[1]:
                opt(*args)
        except IndexError as i:
            print('type file name placed in datasets directory which will be optimized, ex. Genetic_Optimizer().optimize(myfile.csv)')
    return wrapper


class Genetic_Optimizer(Implement_Func):
    config = Load_Configuration()

    def generate(self, population_size=config.read('POPULATION_SIZE'), chromosome_size=config.read('CHROMOSOME_SIZE'), equal_chromosomes=config.read('EQUAL_CHROMOSOMES'),initialization_method=config.read('INITIALIZATION_METHOD'), representation=config.read('REPRESENTATION'), saving_method=config.read('SAVING_METHOD')):
        Generator(population_size, chromosome_size, equal_chromosomes, initialization_method, representation, saving_method)
    
    @check_file
    def optimize(self, file_name : str):
#        Preprocess_Dataframe(file_name)        
        Fitness(file_name)

if __name__ == '__main__':
    gen = Genetic_Optimizer()
#    gen.generate()
    gen.optimize('permneq.csv')
    
