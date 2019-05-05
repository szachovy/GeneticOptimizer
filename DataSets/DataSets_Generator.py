#!/usr/bin/env python3 
from configparser import ConfigParser
from abc import ABCMeta, abstractmethod

#config = ConfigParser()
#config.read('DEFAULTS.ini')

class Load_Configuration(type):
    
    def __new__(cls, *args, **kwargs):
        config = ConfigParser()
        config.read("DEFAULTS.ini")
        return super(Load_Configuration, cls).__new__(cls, config)


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


class Population_Generator(object):
    '''
        dsa   
    '''        
    def __init__(self, population_size=config['GENERATOR']['POPULATION_SIZE'], chromosome_size=config['GENERATOR']['CHROMOSOME_SIZE'], equal_chromosomes=config['GENERATOR']['EQUAL_CHROMOSOMES'], initialization_method=config['GENERATOR']['INITIALIZATION_METHOD'], representation=config['GENERATOR']['REPRESENTATION'], saving_method=config['GENERATOR']['SAVING_METHOD']):
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