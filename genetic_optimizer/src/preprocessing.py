
import pandas as pd
import numpy as np

class Preprocess_Dataframe(object):
    '''
        
    '''
    def __init__(self, file_name, config):
        self.file_name = file_name
        self.config = config
        self.population = None

    def get_file(self):
        extension = self.file_name.split(".")

        if extension[-1] == 'csv':
            self.population = pd.read_csv('{}{}'.format(self.config.input_loc(), self.file_name, header=None))
     
        elif extension[-1] == 'xlsx':
            self.population = pd.read_xlsx('{}{}'.format(self.config.input_loc(), self.file_name, header=None))
     
        elif extension[-1] == 'json':
            self.population = pd.read_json('{}{}'.format(self.config.input_loc(), self.file_name, header=None))
        else:
            raise Exception('Invalid file name extension')     

        self.drop_unnamed()
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
    