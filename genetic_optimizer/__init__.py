#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'WJ Maj'

from src.conf_handler import Load_Configuration
from Generator.generator import Generator

import timeit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from configparser import ConfigParser

#pyspark
#cython
#datetime
# tempfile with latest configuration




class Genetic_Optimizer(object):
    config = Load_Configuration()

    def __init__(self, mnt = 5):        
#        super().__init__(mnt)
#        print(self.a)
        pass
    def generate(self, population_size=config.read('POPULATION_SIZE'), chromosome_size=config.read('CHROMOSOME_SIZE'), equal_chromosomes=config.read('EQUAL_CHROMOSOMES'),initialization_method=config.read('INITIALIZATION_METHOD'), representation=config.read('REPRESENTATION'), saving_method=config.read('SAVING_METHOD')):
        Generator(population_size, chromosome_size, equal_chromosomes, initialization_method, representation, saving_method)

    def optimize(self, file_name):
        return

if __name__ == '__main__':
    gen = Genetic_Optimizer()
    gen.generate()
    
