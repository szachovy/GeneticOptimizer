
try:
    from preprocessing import Preprocess_Dataframe
except ModuleNotFoundError as m:
    from .preprocessing import Preprocess_Dataframe

from datetime import datetime
import numpy as np
import pandas as pd

#pyspark here

class Fitness(Preprocess_Dataframe):
    def __init__(self, file_name):
        super().__init__(file_name)
        
        self.denominators = []            
        self.sum_cols()
        self.fit_population()

        self.log = str(datetime.now()) + '\n' + 'Fitness function established' + '\n'        
        print(self.log)


    def sum_cols(self):
        for column in self.population:
            self.denominators.append(self.population[column].count())
    
    def fit_population(self):
        fit_population = {}
        get_denominator = 0

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

        fit_population = pd.DataFrame(fit_population).sum(axis = 1)
        return fit_population
