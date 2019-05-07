#!/usr/bin/env python3 
from configparser import ConfigParser
from abc import ABCMeta, abstractmethod
import numpy as np


class Load_Configuration(object):
    '''
        This is auxiliary class for configuration purposes,
        used from DEFAULTS.ini file placed in this directory
    '''
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('DEFAULTS.ini')
            
    def read(self, argument):
        return self.config['GENERATOR'][argument]


class Representation_Types(metaclass=ABCMeta):
    '''
       ds 
    '''
    @abstractmethod
    def binary_representation(self):
        raise NotImplementedError("Generator do not contain Binary Representation population generator")

    @abstractmethod
    def integer_representation(self):
        raise NotImplementedError("Generator do not contain Integer Representation population generator")

    @abstractmethod
    def permutation_representation(self):
        raise NotImplementedError("Generator do not contain Permutation Representation population generator")


class Population_Generator(Representation_Types):
    '''
        dsa   
    '''       
    config = Load_Configuration()
    
    def __init__(self, population_size=config.read('POPULATION_SIZE'), chromosome_size=config.read('CHROMOSOME_SIZE'), equal_chromosomes=config.read('EQUAL_CHROMOSOMES'), initialization_method=config.read('INITIALIZATION_METHOD'), representation = config.read('REPRESENTATION'), saving_method = config.read('SAVING_METHOD')):

        self.population_size = population_size
        self.chromosome_size = chromosome_size
        self.equal_chromosomes = equal_chromosomes
        self.initialization_method = initialization_method
        self.representation = representation
        self.saving_method = saving_method
        

    def binary_representation(self):
        
        pass

    def integer_representation(self):
        pass

    def permutation_representation(self):
        pass

print(Population_Generator().population_size)