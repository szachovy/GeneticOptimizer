

try:
    from conf_handler import Main_Configuration
except ModuleNotFoundError as m:
    from .conf_handler import Main_Configuration

import pandas as pd
import numpy as np
from datetime import datetime

class Preprocess_Dataframe(object):
    '''
        
    '''
    def __init__(self, file_name):
        self.config = Main_Configuration() 
        extension = file_name.split(".")

        if extension[-1] == 'csv':
            self.population = pd.read_csv('{}{}'.format(self.config.input_loc(), file_name, header=None))

        elif extension[-1] == 'xlsx':
            self.population = pd.read_xlsx('{}{}'.format(self.config.input_loc(), file_name, header=None))

        elif extension[-1] == 'json':
            self.population = pd.read_json('{}{}'.format(self.config.input_loc(), file_name, header=None))
        else:
            raise Exception('Invalid file name extension')

        self.drop_unnamed()
        self.check_types()

        self.log = str(datetime.now()) + "\n" + "File found and cleaned properly\n"
        print(self.log)

    def check_types(self):
        accepted_types = [np.int64, np.float64]
        try:
            assert(all(list(map(lambda column: column in accepted_types, list(self.population.dtypes)))))
        except AssertionError as a:
            raise Exception('Chromosomes cannot contain string objects')

    def drop_unnamed(self):
        self.population.drop(self.population.columns[0], axis=1, inplace=True)
    