
__author__ = 'WJ Maj'

import numpy as np
import pandas as pd

class Fitness(object):

    def __init__(self, population):
        self.denominators = []            
        self.population = population

    def sum_cols(self):
        for column in self.population:
            self.denominators.append(self.population[column].count())
    
    def fit_population(self):
        fit_population = {}
        get_denominator = 0

        self.sum_cols()

        for column in self.population:
            occurrences = dict(self.population[column].value_counts())
            fit_population[get_denominator] = []

            for value in range(self.population.shape[0]):
                try:
                    if self.denominators[get_denominator] == 1:
                        fit_population[get_denominator].append(float((self.denominators[get_denominator]) * self.population[column][value])/self.denominators[get_denominator])    
            
                    else:
                        fit_population[get_denominator].append(float((self.denominators[get_denominator] - occurrences[self.population[column][value]]) * self.population[column][value])/self.denominators[get_denominator])

                except KeyError as k:
                    fit_population[get_denominator].append(np.NaN)

            get_denominator += 1

        fit_population = pd.DataFrame(fit_population)

        fit_population['Total'] = fit_population.sum(axis=1)
        fit_population['Chromosome'] = [index for index in range(fit_population.shape[0])]

        return fit_population
