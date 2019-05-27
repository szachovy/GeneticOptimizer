#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#TODO
# check optimizer on other files
# package path change
# check setup.py

__author__ = 'WJ Maj'

from .src.meta import Implement_Func
from .src.conf_handler import Load_Configuration
from .src.pipeline import Pipeline
from .Generator.generator import Generator

from configparser import ConfigParser
import inspect

def load_config(gen):
    '''
        Load default configuration parameters from DEFAULTS.ini file in Generator directory,
        if not provided by user.
    '''
    def wrapper(*args, **kwargs):
        config = Load_Configuration()
        for arg in inspect.getfullargspec(gen).args:
            try:
                kwargs[arg]
            except KeyError as k:
                kwargs[arg] = config.read(arg.upper())
        try:
            gen(*args, **kwargs)
        except TypeError as t:
            raise t('Insert full name arguments while changing configuration parameters')
    return wrapper
        
def check_file(opt):
    '''
        Raise exception if user do not provide input data set,
        which will be optimized.
    '''
    def wrapper(*args, **kwargs):
        try:
            if args[0]:                     
                opt(*args)
        except IndexError as i:
            print('Pandas DataFrame or file path are not passed into function parameter during optimization')
    return wrapper


class Optimizer(Implement_Func):
    '''
        Generate or Optimize your data set in efficient way.
        ...      
    '''
    @staticmethod
    @load_config
    def generate(population_size, chromosome_size, equal_chromosomes, initialization_method, representation, saving_method):
        '''
            ...
        '''
        Generator(population_size, chromosome_size, equal_chromosomes, initialization_method, representation, saving_method)
    
    @staticmethod
    @check_file
    def optimize(file_name, iterations=None, shuffle_scale=None, variety=None, chromosome_weight=None):
        '''
            ...
        '''
        Pipeline(file_name, iterations, shuffle_scale, variety, chromosome_weight)

if __name__ == '__main__':
    gen = Optimizer()
#    gen.generate()
    gen.optimize('./datasets/bineq.csv', 5)
    
