#!/usr/bin/env python3 

from configparser import ConfigParser
from abc import ABCMeta, abstractmethod
import numpy as np
import pandas as pd

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

class Configuration_Executer(object):
    '''
        This class provide functional operations on given dataset
        whose will give reasonable output
    '''
    config = Load_Configuration()

    def __init__(self, population_size=config.read('POPULATION_SIZE'), chromosome_size=config.read('CHROMOSOME_SIZE'), equal_chromosomes=config.read('EQUAL_CHROMOSOMES'), initialization_method=config.read('INITIALIZATION_METHOD'), representation = config.read('REPRESENTATION'), saving_method = config.read('SAVING_METHOD')):
        
        try:
            self.population_size = int(population_size)
        except ValueError as v:
            print("Wrong type of population_size input, check DEFAULTS for more info")
            
        try:
            self.chromosome_size = int(chromosome_size)
        except ValueError as v:
            print("Wrong type of chromosome_size input, check DEFAULTS for more info")    
            
        try:
            self.equal_chromosomes = bool(equal_chromosomes)
        except ValueError as v:
            print("Wrong type of equal_chromosomes input, check DEFAULTS for more info")
                
        self.initialization_method = initialization_method
        self.representation = representation
        self.saving_method = saving_method

    def random_initialization(self):
        population = pd.DataFrame()
        print('tera tu')
        if self.representation == 'Binary':
            population = pd.DataFrame(data=np.random.randint(2, size=(self.population_size, self.chromosome_size)))

        elif self.representation == 'Real_Valued':
            self.real_valued_representation()
        elif self.representation == 'Integer':
            self.integer_representation()
        elif self.representation == 'Permutation':
            self.permutation_representation()
        else:
            raise Exception('Wrong value in representation input, check DEFAULTS for more info')

        if not self.equal_chromosomes:
            self.generator.fill_unequal_chromosomes()        

        return population

    def heuristic_initialization(self):
        if not self.equal_chromosomes:
            self.generator.fill_unequal_chromosomes()        
        return

    def fill_unequal_chromosomes(self):
        pass

    @staticmethod
    def save_csv(population):
        population.to_csv("../DataSets/tmp.csv")
    
    @staticmethod
    def save_xlsx(population):
        pass
    
    @staticmethod
    def save_json(population):
        pass
                

                
class Population_Generator(Representation_Types, Configuration_Executer):
    '''
        This is main Generator class obliged for propietary
        executing Configuration_Executer functions  
    '''       
    generator = Configuration_Executer()
    
    def __init__(self):
        super().__init__()
        self.generate()        
    

    def initialize_population(self):
        if self.initialization_method == 'Random':
            print('i jest random')
            return self.generator.random_initialization()
        
        elif self.initialization_method == 'Heuristic':
            print('i jest heuristic')
            self.generator.heuristic_initialization()
                
        else:
            raise Exception('Wrong input in initialization_method, check DEFAULTS for more info')

    def save_population(self, population):
        if self.saving_method == 'csv':
            print('zapis csv')
            self.generator.save_csv(population)

        elif self.saving_method == 'xlsx':
            print('zapis xlsx')
            self.generator.save_xlsx(population)

        elif self.saving_method == 'json':
            print('zapis json')
            self.generator.save_json(population)

        else:
            raise Exception('Wrong input in saving method, check DEFAULTS for more info')


    def generate(self):

        binary_population = self.initialize_population()
        self.save_population(binary_population)


        #print(self.population_size)
        #print(type(self.population_size))

        
#print(Population_Generator().population_size)
#print(Configuration_Executer().a())

gen = Population_Generator()
