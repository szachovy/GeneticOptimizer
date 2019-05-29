#!/usr/bin/env python3
# *-* coding utf-8 *-*

__author__ = 'WJ Maj'


from .conf_handler import Main_Configuration
from .preprocessing import Preprocess_Dataframe
from .fitness import Fitness
from .optimizator import Optimizer
from .save import Save

from datetime import datetime

class Pipeline(object):
    """
        Main Executor
        Pipeline for sequenced apropiate proccessing of file inside referenced files
        Marks logs after each one stadium of executing code.

        Arguments:
            *args: arguments provided in main __init__.py file (unconverded by defaults which will be done in self.config)

        Returns:
            None 
    """
    def __init__(self, data, iterations, shuffle_scale, variety, chromosome_weight):
        self.config = Main_Configuration(iterations, shuffle_scale, variety, chromosome_weight)
        self.performance = self.config.performance()
        
        start = datetime.now()
        
        #preprocessing
        self.population = Preprocess_Dataframe(data, self.config).get_file()
        print(str(datetime.now()) + "\n" + "File found and cleaned properly")

        self.generation = 0
        while self.generation != self.performance['iterations']:  
               
            #fitness
            self.fitted_population = Fitness(self.population).fit_population()
            print(str(datetime.now()) + "\n" + "Population {} fitted correctly".format(self.generation))
#            print(self.fitted_population)

            #optimizer
            self.new_population = Optimizer(self.performance, self.fitted_population)
    
            # group population
            groups = self.new_population.group_population()
            print(str(datetime.now()) + "\n" + "Population {} grouped into clusters".format(self.generation))
            
            # make next generation
            self.population = self.new_population.next_generation(groups, self.population)
            print(str(datetime.now()) + "\n" + "Generated {} generation of population".format(self.generation))
            self.generation += 1

        stop = datetime.now()
        print(str(datetime.now()) + "\n" + "Population optimized without any errors")
        print("Total time of optimizer activity : " + str(stop - start))   

        #save
        save = Save(data, self.config, start, stop, self.generation, self.performance)
        save.save_population = self.population
        print(save.save_population)
        

        