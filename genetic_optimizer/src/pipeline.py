# All sumarized here

try:
    from conf_handler import Main_Configuration
    from preprocessing import Preprocess_Dataframe
    from fitness import Fitness
    from optimizator import Optimizer
    from save import Save
except ModuleNotFoundError as m:
    from .conf_handler import Main_Configuration
    from .preprocessing import Preprocess_Dataframe
    from .fitness import Fitness
    from .optimizator import Optimizer
    from .save import Save

from datetime import datetime


class Pipeline(object):
    def __init__(self, file_name):
        self.config = Main_Configuration()

        #preprocessing
        self.population = Preprocess_Dataframe(file_name, self.config).get_file()
 #       print(self.population)
        print(str(datetime.now()) + "\n" + "File found and cleaned properly")

        #fitness
        self.fitted_population = Fitness(self.population).fit_population()
#        print(self.fitted_population)
        print(str(datetime.now()) + "\n" + "Population fitted correctly")

        #optimizer
        self.new_population = Optimizer(self.config.performance(), self.fitted_population)

        # group population
        groups = self.new_population.group_population()
        print(str(datetime.now()) + "\n" + "Population grouped into clusters")
#        print(groups)
#        print(groups.labels_)
#        print(groups.cluster_centers_)

        # select parent
        self.population = self.new_population.next_generation(groups, self.population)
        print(str(datetime.now()) + "\n" + "Generated {} generation of population".format(1))
        # test accurracy
        #------------

        #save
        #-------------
        

        