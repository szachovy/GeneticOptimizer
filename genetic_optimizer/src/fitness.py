
try:
    from preprocessing import Preprocess_Dataframe
except ModuleNotFoundError as m:
    from .preprocessing import Preprocess_Dataframe

from datetime import datetime

class Fitness(Preprocess_Dataframe):
    def __init__(self, file_name):
        super().__init__(file_name)
        
        print(self.population)
        self.sum_cols()
        self.log = str(datetime.now()) + '\n' + 'Fitness function established' + '\n'        
        print(self.log)

    def sum_cols(self):
        for i in self.population:
            print(column[i])