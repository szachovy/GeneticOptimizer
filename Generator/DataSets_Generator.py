#!/usr/bin/env python3 

from configparser import ConfigParser
from abc import ABCMeta, abstractmethod
import numpy as np


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
    def binary_representation(self):
        raise NotImplementedError("Generator do not handle Binary Representation population generator")

    @abstractmethod
    def integer_representation(self):
        raise NotImplementedError("Generator do not handle Integer Representation population generator")

    @abstractmethod
    def real_valued_representation(self):
        raise NotImplementedError("Generator do not handle Real Valued Representation population generator")    

    @abstractmethod
    def permutation_representation(self):
        raise NotImplementedError("Generator do not handle Permutation Representation population generator")

class Configuration_Executer(object):
    '''
        This class provide functional operations on given dataset
        whose will give reasonable output
    '''
    config = Load_Configuration()

    def __init__(self, population_size=config.read('POPULATION_SIZE'), chromosome_size=config.read('CHROMOSOME_SIZE'), equal_chromosomes=config.read('EQUAL_CHROMOSOMES'), initialization_method=config.read('INITIALIZATION_METHOD'), representation = config.read('REPRESENTATION'), saving_method = config.read('SAVING_METHOD')):
    
        self.population_size = population_size
        self.chromosome_size = chromosome_size
        self.equal_chromosomes = equal_chromosomes
        self.initialization_method = initialization_method
        self.representation = representation
        self.saving_method = saving_method
            
    def type_converter(self):
        try:
            map(int, self.population_size)
        except ValueError as v:
            print("Wrong type of population_size input, make sure that you placed integer value")
    
        try:
            map(int, self.chromosome_size)
        except ValueError as v:
            print("Wrong type of chromosome_size input, make sure that you placed integer value")    
    
        try:
            map(bool, self.equal_chromosomes)
        except ValueError as v:
            print("Wrong type of equal_chromosomes input, make sure that you placed 0 or 1")
            
    def a(self):
        return self.population_size


                
class Population_Generator(Representation_Types, Configuration_Executer):
    '''
        This is main Generator class obliged for propietary
        executing Configuration_Executer functions  
    '''       
    generator = Configuration_Executer()
    
    def __init__(self):
        super().__init__()

        if self.representation == 'Binary':
            self.binary_representation()
        elif self.representation == 'Real_Valued':
            self.real_valued_representation()
        elif self.representation == 'Integer':
            self.integer_representation()
        elif self.representation == 'Permutation':
            self.permutation_representation()
        else:
            raise Exception('Wrong value in representation input, make sure that you placed one of the following strings: Binary, Real_Valued, Integer, Permutation')
            

    def binary_representation(self):
        print('tu cie mam')        
#        np.random.randint(2, size=())

    def integer_representation(self):
        pass

    def real_valued_representation(self):
        pass

    def permutation_representation(self):
        pass

        
#print(Population_Generator().population_size)
#print(Configuration_Executer().a())

gen = Population_Generator()
print(gen.population_size)
print(gen.initialization_method)

print(type(gen.population_size))
print(type(gen.initialization_method))
