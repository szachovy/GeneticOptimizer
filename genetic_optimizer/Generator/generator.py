#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

__author__ = 'WJ Maj'

from configparser import ConfigParser
from abc import ABCMeta, abstractmethod
import re

try:
    from conf_exec import Configuration_Executer # This module is placed in Generator directory (to prevent navigation problems)
except ImportError:
    from .conf_exec import Configuration_Executer

class Load_Configuration(object):
    '''
        This is auxiliary class for configuration purposes,
        used from DEFAULTS.ini file placed in this directory.
    '''
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('DEFAULTS.ini')
            
    def read(self, argument):
        return self.config['GENERATOR'][argument]


class Representation_Types(metaclass=ABCMeta):
    '''
       This class is concerned for implementation issues comes from
        Population_Generator class.
    '''
    @abstractmethod
    def generate(self):
        raise NotImplementedError("Generator temporarily do not handle population generate requests")

                
class Generator(Representation_Types):
    '''
        This is main Generator class obliged for propietary
        executing Configuration_Executer functions  
        and produce output file
    '''       
    config = Load_Configuration()

    def __init__(self, population_size=config.read('POPULATION_SIZE'), chromosome_size=config.read('CHROMOSOME_SIZE'), equal_chromosomes=config.read('EQUAL_CHROMOSOMES'), initialization_method=config.read('INITIALIZATION_METHOD'), representation = config.read('REPRESENTATION'), saving_method = config.read('SAVING_METHOD')):

        self.initialization_method = initialization_method
        self.generator = Configuration_Executer(population_size, chromosome_size, equal_chromosomes, initialization_method, representation, saving_method)
        self.generate()
		    

    def initialize_population(self):
        try:
            if self.initialization_method == 'Random':
                return self.generator.random_initialization()
        
            elif self.initialization_method == 'Heuristic':
                print("Heuristic mode is not implemented yet, please be patient")
                exit(0)
                return self.generator.heuristic_initialization()
                
        except Exception as e:
            raise Exception('Wrong input in initialization_method, check DEFAULTS for more info')
            exit(0)

    def save_population(self, population):

        file_name = input('How to name file : ')
        try:
            assert(bool(re.match('^[a-zA-Z0-9]+$', file_name)))
            self.generator.save(population, file_name)

        except AssertionError as a:
            print('Incorrect file name')
            exit(0)

    
    def generate(self):
        try:
            binary_population = self.initialize_population()
            self.save_population(binary_population)
            print('Finish!\nPopulation Generated in datasets directory')                         

        except Exception as e:
            print('Configurator executer failed')

        finally:
            exit(0)

gen = Generator()