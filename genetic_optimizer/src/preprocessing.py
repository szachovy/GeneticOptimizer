
__all__ = ['Preprocess_Dataframe']
try:
    from conf_handler import Main_Configuration
except ModuleNotFoundError as m:
    from .conf_handler import Main_Configuration

import pandas as pd


def check_input_file(initialize):
    def wrapper(*args):
        if args:
            return initialize(*args)
        else:
            raise Exception('Input file name with extension to optimize, ex. Genetic_Optimizer().optimize(myfile.csv)')
    return wrapper()


class Preprocess_Dataframe(object):

 
    def __init__(self, file_name):
        self.config = Main_Configuration()

        extension = file_name.split(".")

        if extension[-1] == 'csv':
            self.population = pd.read_csv('{}{}'.format(self.config.input_loc(), file_name))
        elif extension[-1] == 'xlsx':
            self.population = pd.read_xlsx('{}{}'.format(self.config.input_loc(), file_name))
        elif extension[-1] == 'json':
            self.population = pd.read_json('{}{}'.format(self.config.input_loc(), file_name))
        else:
            raise Exception('Invalid file name extension')

        print(self.population)    