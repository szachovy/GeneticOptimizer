
__author__ = 'WJ Maj'

import numpy as np
import pandas as pd
import random
import platform
import os

if platform.system() == 'Linux':
    import xlsxwriter # support saving xlsx file in unix-domain systems


def makedir(save):
    """
        Create required directory if not exists
        
        Args:
            population: population which will be saved in save function
            file_name: file created inside directory
    """
    def wrapper(*args):
        directory = os.path.join(os.getcwd(), 'datasets')
        if not os.path.exists(directory):
            os.makedirs(directory)
        save(*args)
    return wrapper

class Configuration_Executer(object):
    '''
        This class provide functional operations on given configuration dataset
        whose will give reasonable output after transformations
    '''

    def __init__(self, population_size, chromosome_size, equal_chromosomes, initialization_method, representation, saving_method):
        try:
            self.population_size = int(population_size)
        except ValueError as v:
            print("Wrong type of population_size input, check the DEFAULTS for more info")
            raise
            
        try:
            self.chromosome_size = int(chromosome_size)
        except ValueError as v:
            
            raise v("Wrong type of chromosome_size input, check the DEFAULTS for more info")
                          
        try:
            self.equal_chromosomes = bool(equal_chromosomes)
        except ValueError as v:
            print("Wrong type of equal_chromosomes input, check the DEFAULTS for more info")   
            raise
       
        self.initialization_method = initialization_method
        self.representation = representation
        self.saving_method = saving_method       

    def count_chromosomes(self, chromosome_layer : str) -> int:
        try:
            count = int(input('How many chromosomes in {0} layer, full chromosome length is {1} : '.format(chromosome_layer, self.chromosome_size)))

            if count > self.chromosome_size:
                count = self.chromosome_size
            
            if count < 0:
                raise Exception('Numer of chromosomes cannot be negative value')

            return count

        except ValueError as v:
            raise Exception('Number of chromosomes in each layer must be an integer value!')
        

    def random_initialization(self):
        population = pd.DataFrame()
        
        if self.representation == 'Binary':
            print("You have chosen Binary representation option")

            if self.equal_chromosomes:
                population = pd.DataFrame(data=np.random.randint(2, size=(self.population_size, self.chromosome_size)))

            elif not self.equal_chromosomes:
                print('You have chosen unequal chromosomes option')
                chromosomes = []

                for chromosome_layer in range(self.population_size):                
                    chromosomes.append([random.randint(0, 1) for gene in range(self.count_chromosomes(chromosome_layer))])
                
                population = pd.DataFrame(data=chromosomes)
                                                
            else:
                raise Exception('Could not specify chromosomes equality option')


        elif self.representation == 'Real_Valued':
            print("You have chosen Real Valued representation option")

            DEFAULT_PRECISION = 2

            chromosomes = []

            min_gene = float(input('Select minimal possible value of gene : '))
            max_gene = float(input('Select maximal possible value of gene : '))

            if min_gene > max_gene:
                min_gene, max_gene = max_gene, min_gene
            
            if self.equal_chromosomes:
                for chromosome_layer in range(self.population_size):
                    chromosomes.append([round(random.uniform(min_gene, max_gene), DEFAULT_PRECISION) for gene in range(self.chromosome_size)])            

            elif not self.equal_chromosomes:
                print('You have chosen unequal chromosomess option')

                for chromosome_layer in range(self.population_size):                
                    chromosomes.append([round(random.uniform(min_gene, max_gene), DEFAULT_PRECISION) for gene in range(self.count_chromosomes(chromosome_layer))])
                
            population = pd.DataFrame(data=chromosomes)
       
        
        elif self.representation == 'Integer':
            print("You have chosen Integer representation option")
            try:
                min_gene = int(input('Select minimal possible value of gene, must be an integer : '))
                max_gene = int(input('Select maximal possible value of gene, must be an integer : '))
                
                if min_gene > max_gene:
                    min_gene, max_gene = max_gene, min_gene

                if self.equal_chromosomes:
                    population = pd.DataFrame(data=np.random.randint(min_gene, max_gene, size=(self.population_size, self.chromosome_size)))

                elif not self.equal_chromosomes:
                    print('You have chosen unequal chromosomes option')
                    chromosomes = []

                    for chromosome_layer in range(self.population_size):                
                        chromosomes.append([random.randint(min_gene, max_gene) for gene in range(self.count_chromosomes(chromosome_layer))])

                    population = pd.DataFrame(data=chromosomes)

                else:
                    raise Exception('Could not specify chromosomes equality option')

            except ValueError as v:
                print('In integer representation, minimal and maximal possible selected gene must be also integer')


        elif self.representation == 'Permutation':
            print("You have chosen Permutation representation option")

            chromosomes = []            

            try:
                min_gene = int(input('Select minimal possible value of gene, must be an integer but remember, the difference between min and max must be equal chromosome size! : '))
                max_gene = int(input('Select maximal possible value of gene, must be an integer : '))

                if min_gene > max_gene:
                    min_gene, max_gene = max_gene, min_gene

                try:
                    assert((max_gene - min_gene) == self.chromosome_size)
                except AssertionError as a:
                    print('Difference between max and min gene must be equal chromosome size')

                        
                if self.equal_chromosomes:
                    for chromosome_layer in range(self.population_size):
                        chromosomes.append(np.random.permutation([min_gene + gene for gene in range(max_gene - min_gene)]))

                elif not self.equal_chromosomes:
                    print('You have chosen unequal chromosomes option')

                    for chromosome_layer in range(self.population_size):                
                        chromosomes.append(np.random.permutation([min_gene + gene for gene in range(self.count_chromosomes(chromosome_layer))]))
                else:
                    raise Exception('Could not specify chromosomes equality option')
                
                population = pd.DataFrame(data=chromosomes)

            except ValueError as v:
                print('In integer representation, minimal and maximal possible selected gene must be also integer')

        else:
            raise Exception('Wrong value in representation input, check DEFAULTS for more info')    

        return population

    # i`ll do it later
    def heuristic_initialization(self):
        return            

    @makedir
    def save(self, population, file_name : str): # save population with given extension
        getos_slashes = self.os_slashes_for_saving()

        if self.saving_method == 'csv':
            try:    
                population.to_csv("datasets{}{}.csv".format(getos_slashes, file_name))
            except Exception as e:
                print('Unable to save a dataframe in csv format')

        elif self.saving_method == 'xlsx':
            try:
                population.to_excel("datasets{}{}.xlsx".format(getos_slashes, file_name))
            except Exception as e:
                print('Unable to save a dataframe in xlsx format')

        elif self.saving_method == 'json':
            try:
                population.to_json("datasets{}{}.json".format(getos_slashes, file_name))
            except Exception as e:
                print('Unable to save a dataframe in json format')

        else:
            raise Exception('Wrong input in saving method, check DEFAULTS for more info')

    @staticmethod
    def os_slashes_for_saving() -> str: # Perform appropiate slashes
        if platform.system() == 'Windows':
            return '\\'
        else:
            return '/'
