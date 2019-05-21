# All sumarized here

try:
    from conf_handler import Main_Configuration
    from preprocessing import Preprocess_Dataframe
    from fitness import Fitness
    from optimizator import Optimizer
except ModuleNotFoundError as m:
    from .conf_handler import Main_Configuration
    from .preprocessing import Preprocess_Dataframe
    from .fitness import Fitness
    from .optimizator import Optimizer

from datetime import datetime


class Pipeline(object):
    def __init__(self, file_name):
        self.config = Main_Configuration()

        #preprocessing
        self.population = Preprocess_Dataframe(file_name, self.config).get_file()
 #       print(self.population)
        print(str(datetime.now()) + "\n" + "File found and cleaned properly\n")

        #fitness
        self.fitted_population = Fitness(self.population).fit_population()
#        print(self.fitted_population)
        print(str(datetime.now()) + "\n" + "Population fitted correctly\n")

        #optimizer
        Optimizer(self.config.performance(), self.fitted_population)          