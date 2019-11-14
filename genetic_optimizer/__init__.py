#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'WJ Maj'

# Files responsible for generator handling 
from .src.conf_handler import Load_Configuration
from .Generator.generator import Generator

# Files responsible for optimizer handling
from .src.pipeline import Pipeline

# All class exceptions if build fails
from .src.meta import Implement_Func

from configparser import ConfigParser
import inspect

def load_config(func):
    """
        Provide default configuration if user did not provide arguments for his population set up.
        Generator uses default values in DEFAULTS.ini file in src of project
        Optimizer uses defauld values in STANDARTS.conf file in src of project

        Args:
            *args: user provided arguments by sequence
            **kwargs: user provided arguments by keyword

        Returns:
            func: chosen function filled with default or provided args 
    """
    def wrapper(*args, **kwargs):
        config = Load_Configuration()
        arg_num = 0

        for arg in inspect.getfullargspec(func).args:
            try:
                if args[arg_num]:
                    pass
            except IndexError as i:
                try:
                    if kwargs[arg]:
                        pass
                except KeyError as k:
                    if func.__name__ == 'generate':
                        kwargs[arg] = config.read(arg.upper())
                    else:
                        if arg_num == 0:
                            raise Exception('Pandas DataFrame or file path are not passed into function parameter during optimization')
                        kwargs[arg] = None
                except ValueError as v:
                    pass

            finally:
                arg_num += 1

        func(*args, **kwargs)
    return wrapper

class Optimizer(Implement_Func):
    """
        Generate or Optimize your data set.

        Attributes:
            Properly handled by @load_config at all.

        Raises:
            Exception: attributes are not properly handled
            Exception: references failed
    
    """
    @staticmethod
    @load_config
    def generate(population_size, chromosome_size, equal_chromosomes, initialization_method, representation, saving_method):
        Generator(population_size, chromosome_size, equal_chromosomes, initialization_method, representation, saving_method)
    
    @staticmethod
    @load_config
    def optimize(data, iterations, shuffle_scale, variety, chromosome_weight):
        Pipeline(data, iterations, shuffle_scale, variety, chromosome_weight)    
