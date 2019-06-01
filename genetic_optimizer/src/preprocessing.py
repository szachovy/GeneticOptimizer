
__author__ = 'WJ Maj'

import pandas as pd
import numpy as np

class Preprocess_Dataframe(object):
    """
        Check property of dataset,
        alarm irregularities in case of wrongs in data

        Arguments:
            data: population sent in file or dataframe
            config: self config or default

        Returns:
            population: exact dataset for futher processing -> pandas.DataFrame
    
    """
    def __init__(self, data, config):
        self.data = data
        self.config = config
        self.population = None

    def get_file(self):
        if type(self.data) is not str: 
            self.population = pd.DataFrame(data=self.data)     
            self.population.sort_index(inplace=True)

        else:
            extension = self.data.split(".")

            if extension[-1] == 'csv':
                self.population = pd.read_csv(self.data)     
                self.drop_unnamed()
            elif extension[-1] == 'xlsx':
                self.population = pd.read_excel(self.data)
                self.drop_unnamed()
            elif extension[-1] == 'json':
                self.population = pd.read_json(self.data)
            
            self.population.sort_index(inplace=True)
        
        print(self.population)
        self.check_types()
        self.all_nan_exception()

        return self.population

    def all_nan_exception(self):
        population_transposed = self.population.transpose()

        for column in population_transposed:
            if population_transposed[column].isnull().all():
                raise Exception('Each chromosome must have at least one gene')

    def check_types(self):
        accepted_types = [np.int64, np.float64]
        try:
            assert(all(list(map(lambda column: column in accepted_types, list(self.population.dtypes)))))
        except AssertionError as a:
            raise Exception('Chromosomes cannot contain string objects')

    def drop_unnamed(self):
        self.population.drop(self.population.columns[0], axis=1, inplace=True)
    
