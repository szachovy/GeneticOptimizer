#!/usr/bin/env python3
# *-* conding utf-8 *-*

__author__ = 'WJ Maj'

from configparser import ConfigParser
from abc import ABCMeta, abstractmethod
import re

try:
    from conf_exec import Configuration_Executer # This module is placed in Generator directory (to prevent navigation problems)
except ImportError:
    from .conf_exec import Configuration_Executer

class Representation_Types(metaclass=ABCMeta):
    '''
       This class is concerned for implementation issues comes from
        Population_Generator class.
    '''
    @abstractmethod
    def generate(self):
        raise 

                
class Generator(Representation_Types):
    '''
        This is main Generator class obliged for propietary
        executing Configuration_Executer functions  
        and produce output file
    '''       
    def __init__(self, population_size, chromosome_size, equal_chromosomes, initialization_method, representation, saving_method): # send parameters to conf_exec file

        self.initialization_method = initialization_method
        self.generator = Configuration_Executer(population_size, chromosome_size, equal_chromosomes, initialization_method, representation, saving_method)
        self.generate()
		    

    def initialize_population(self):
        try:
            if self.initialization_method == 'Random':
                return self.generator.random_initialization()
        
            elif self.initialization_method == 'Heuristic':
                raise Exception("Heuristic mode is not implemented yet, please be patient")
#                return self.generator.heuristic_initialization()
                
        except Exception as e:
            raise Exception('Wrong input in initialization_method, check DEFAULTS for more info')

    def save_population(self, population):

        file_name = input('How to name file : ')
        try:
            assert(bool(re.match('^[a-zA-Z0-9]+$', file_name)))
            self.generator.save(population, file_name)

        except AssertionError as a:
            print('Incorrect file name')

    
    def generate(self):
        try:
            binary_population = self.initialize_population()
            self.save_population(binary_population)
            print('Finish!\nPopulation Generated in datasets directory')                         

        except Exception as e:
            print('Configurator executer failed')

        finally:
            pass
