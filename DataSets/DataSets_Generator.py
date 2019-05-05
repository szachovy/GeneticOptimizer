#!/usr/bin/env python3 
from configparser import ConfigParser

config = ConfigParser()
config.read('DEFAULTS.ini')
#class Load_Configuration(type):
    
#    def __new__(cls, *args, **kwargs):
#        config = ConfigParser()
#        config.read("DEFAULTS.ini")
#        return super(Load_Configuration, cls).__new__(cls, config)

# ABSTRACT CLASS    
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