#!/usr/bin/env python3

import numpy as np
import pandas as pd
import random
import xlsxwriter # support saving xlsx file in unix-domain systems

class Configuration_Executer(object):
    '''
        This class provide functional operations on given configuration dataset
        whose will give reasonable output after transformations
    '''


    def __init__(self, population_size, chromosome_size, equal_chromosomes, initialization_method, representation, saving_method):
        self.population_size = int(population_size)
        self.chromosome_size = int(chromosome_size)
        self.equal_chromosomes = bool(equal_chromosomes)
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
                chromosomes = []

                for chromosome_layer in range(self.population_size):                
                    count = int(input('How many chromosomes in {0} layer, full chromosome length is {1} : '.format(chromosome_layer, self.chromosome_size)))
                    
                    if count > self.chromosome_size:
                        count = self.chromosome_size
                 
                    chromosomes.append([random.randint(0, 1) for gene in range(count)])
                
                population = pd.DataFrame(data=chromosomes)
                                                
            else:
                raise Exception('Could not specify chromosomes equality option')


        elif self.representation == 'Real_Valued':
            print("You have chosen Real Valued representation option")

            DEFAULT_PRECISION = 2

            min_gene = float(input('Select minimal possible value of gene : '))
            max_gene = float(input('Select maximal possible value of gene : '))

            if min_gene > max_gene:
                min_gene, max_gene = max_gene, min_gene
            
            if self.equal_chromosomes:
                chromosomes = []
                for chromosome_layer in range(self.population_size):
                    chromosomes.append([round(random.uniform(min_gene, max_gene), DEFAULT_PRECISION) for gene in range(self.chromosome_size)])            

                population = pd.DataFrame(data=chromosomes)

            elif not self.equal_chromosomes:
                print('You have chosen unequal chromosomess option')
                chromosomes = []

                for chromosome_layer in range(self.population_size):                
                    count = int(input('How many chromosomes in {0} layer, full chromosome length is {1} : '.format(chromosome_layer, self.chromosome_size)))
                    
                    if count > self.chromosome_size:
                        count = self.chromosome_size
                 
                    chromosomes.append([round(random.uniform(min_gene, max_gene), DEFAULT_PRECISION) for gene in range(count)])
                
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
                        count = int(input('How many chromosomes in {0} layer, full chromosome length is {1} : '.format(chromosome_layer, self.chromosome_size)))
                    
                        if count > self.chromosome_size:
                            count = self.chromosome_size
                 
                        chromosomes.append([random.randint(min_gene, max_gene) for gene in range(count)])

                    population = pd.DataFrame(data=chromosomes)

                else:
                    raise Exception('Could not specify chromosomes equality option')

            except ValueError as v:
                print('In integer representation, minimal and maximal possible selected gene must be also integer')


        elif self.representation == 'Permutation':
            print("You have chosen Permutation representation option")
            
            try:
                min_gene = int(input('Select minimal possible value of gene, must be an integer but remember, the difference between min and max must be equal chromosome size! : '))
                max_gene = int(input('Select maximal possible value of gene, must be an integer : '))

                try:
                    assert((max_gene - min_gene) == self.chromosome_size)
                except AssertionError as a:
                    print('Difference between max and min gene must be equal chromosome size')

                if min_gene > max_gene:
                    min_gene, max_gene = max_gene, min_gene
                        
                if self.equal_chromosomes:
                    chromosomes = []
                    for chromosome_layer in range(self.population_size):
                        chromosomes.append(np.random.permutation([min_gene + gene for gene in range(max_gene - min_gene)]))
                
                    population = pd.DataFrame(data=chromosomes)

                elif not self.equal_chromosomes:
                    print('You have chosen unequal chromosomes option')
                    chromosomes = []

                    for chromosome_layer in range(self.population_size):                
                        count = int(input('How many chromosomes in {0} layer, full chromosome length is {1} : '.format(chromosome_layer, self.chromosome_size)))
                    
                        if count > self.chromosome_size:
                            count = self.chromosome_size
                 
                        chromosomes.append(np.random.permutation([min_gene + gene for gene in range(count)]))
                    # tu sie trzeba zastanowic

                    population = pd.DataFrame(data=chromosomes)
               
                else:
                    raise Exception('Could not specify chromosomes equality option')

            except ValueError as v:
                print('In integer representation, minimal and maximal possible selected gene must be also integer')

        else:
            raise Exception('Wrong value in representation input, check DEFAULTS for more info')    

        return population

    # i`ll do it later
    def heuristic_initialization(self):
        return

    def save(self, population, file_name):
        if self.saving_method == 'csv':
            try:
                population.to_csv("../DataSets/{}.csv".format(file_name))
            except Exception as e:
                print('Unable to save a dataframe')

        elif self.saving_method == 'xlsx':
            try:
                population.to_excel("../DataSets/{}.xlsx".format(file_name))
            except Exception as e:
                print('Unable to save a dataframe')

        elif self.saving_method == 'json':
            try:
                population.to_json("../DataSets/{}.json".format(file_name))
            except Exception as e:
                print('Unable to save a dataframe')

        else:
            raise Exception('Wrong input in saving method, check DEFAULTS for more info')
