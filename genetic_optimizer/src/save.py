
__author__ = 'WJ Maj'

from .optimizator import Optimizer
from .fitness import Fitness

import logging

class Save(object):

    def __init__(self, file_name, config, start, stop, generations, performance):
        self.file_name = file_name
        self.config = config
        self.duration = stop - start
        self.generations = generations
        self.start = start
        self.stop = stop
        self.performance = performance
        

    @property
    def save_population(self):
        if self.saved:
            return 'Check results directory to see optimizer results'
        else:
            raise 'None of saving options provided in STANDARDS.conf'

    @save_population.setter
    def save_population(self, population):        
        if self.config.output_loc():
            get_files = self.config.output_loc()
        
            if get_files['file_name']:
                extension = get_files['file_name'].split(".")

                if extension[-1] == 'csv':
                    population.to_csv(get_files['file_name'])
                elif extension[-1] == 'xlsx':
                    population.to_excel(get_files['file_name'])
                elif extension[-1] == 'json':
                    population.to_json(get_files['file_name'])  
                else:
                    print('Wrong extension of saving file provided, unable to save')
                    exit(0)

            if get_files['fig_name']:
                Optimizer(self.config.performance(), Fitness(population).fit_population()).group_population(save=True, file_name=get_files['fig_name'])

            if get_files['log_name']:
                logging.basicConfig(level = logging.INFO, filename = get_files['log_name'])
                logging.info('Population optimized : ' + self.file_name) 
                logging.info('Optimizer started up at : ' + str(self.start)) 
                logging.info('Optimizer ended up at : ' + str(self.stop)) 
                logging.info('Total time of optimizer activity : ' + str(self.stop - self.start))  
                logging.info('Number of generations produced : ' + str(self.generations))
                perform = ""
                for key, val in self.performance.items():
                    perform += "\n" + str(key) + " -> " + str(val) 

                logging.info('Performance settings during optimization : ' + perform) 

            self.saved = True

        else:
            self.saved = False
