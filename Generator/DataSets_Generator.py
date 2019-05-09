#!/usr/bin/env python3 

from configparser import ConfigParser
from abc import ABCMeta, abstractmethod
import numpy as np
import pandas as pd
import random

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
        This class provide functional operations on given configuration dataset
        whose will give reasonable output after transformations
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
        
        if self.representation == 'Binary':
            print("You have chosen Binary representation option")
            if self.equal_chromosomes:
                population = pd.DataFrame(data=np.random.randint(2, size=(self.population_size, self.chromosome_size)))

            elif not self.equal_chromosomes:
                print('You have chosen unequal chromosomes option')
                population = pd.DataFrame(data=self.fill_unequal_chromosomes(0,1))
                                                
            else:
                raise Exception('Could not specify chromosomes equality option')


        elif self.representation == 'Real_Valued':
            print("You have chosen Real Valued representation option")
            min_gene = input('Select minimal possible value of gene')
            max_gene = input('Select maximal possible value of gene')

            
       
        
        elif self.representation == 'Integer':
            print("You have chosen Integer representation option")
            try:
                min_gene = int(input('Select minimal possible value of gene, must be an integer'))
                max_gene = int(input('Select maximal possible value of gene, must be an integer'))
                
                if self.equal_chromosomes:
                    population = pd.DataFrame(data=np.random.randint(min_gene, max_gene, size=(self.population_size, self.chromosome_size)))

                elif not self.equal_chromosomes:
                    

                else:
                    raise Exception('Could not specify chromosomes equality option')

            except ValueError as v:
                print('In integer representation, minimal and maximal possible selected gene must be also integer')


        elif self.representation == 'Permutation':
            print("You have chosen Permutation representation option")
            min_gene = input('Select minimal possible value of gene')
            max_gene = input('Select maximal possible value of gene')
                        
            #linspace

        else:
            raise Exception('Wrong value in representation input, check DEFAULTS for more info')    

        return population

    def heuristic_initialization(self):
        if not self.equal_chromosomes:
            self.generator.fill_unequal_chromosomes()        
        return

    def fill_unequal_chromosomes(self, *args):
        chromosomes_count = []

        for layer in range(self.population_size):                
            chromosomes_count[layer] = input('How many chromosomes in {0} layer, full chromosome length is {1}:'.format(layer, self.chromosome_size))
                    
            if chromosomes_count[layer] > self.chromosome_size:
                chromosomes_count[layer] = self.chromosome_size
                    
            chromosomes_count[layer] = [random.randint(0, 1) for gene in range(chromosome_count[layer])]

    @staticmethod
    def save(population, file_name):

        if self.saving_method == 'csv':
            try:
                population.to_csv("../DataSets/{}".format(file_name))
            except Exception as e:
                print('Unable to save a dataframe')

        elif self.saving_method == 'xlsx':
            try:
                population.to_excel("../DataSets/{}".format(file_name))
            except Exception as e:
                print('Unable to save a dataframe')

        elif self.saving_method == 'json':
            try:
                population.to_json("../DataSets/{}".format(file_name))
            except Exception as e:
                print('Unable to save a dataframe')

        else:
            raise Exception('Wrong input in saving method, check DEFAULTS for more info')

        finally:
            print('Finish!\nPopulation Generated in DataSets directory')                                

                
class Population_Generator(Representation_Types, Configuration_Executer):
    '''
        This is main Generator class obliged for propietary
        executing Configuration_Executer functions  
        and produce output file
    '''       
    generator = Configuration_Executer()
    
    def __init__(self):
        super().__init__()
        self.generate()        
    

    def initialize_population(self):
        if self.initialization_method == 'Random':
            return self.generator.random_initialization()
        
        elif self.initialization_method == 'Heuristic':
            self.generator.heuristic_initialization()
                
        else:
            raise Exception('Wrong input in initialization_method, check DEFAULTS for more info')

    def save_population(self, population):
        file_name = input('How to name file : ')
        self.generator.save(population, filename)

    
    def generate(self):
        binary_population = self.initialize_population()
        self.save_population(binary_population)


gen = Population_Generator()
