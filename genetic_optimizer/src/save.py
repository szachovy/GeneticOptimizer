
import logging

class Save(object):
    #@property
    #@setter
    #output loc conf getfiles['filename'] getfiles['figname']
    #return population if provided
    #return logfile if provided
    #return fig if provided
    def __init__(self, config, duration, generations):
        self.config = config
        self.duration = duration
        self.generations = generations

    @property
    def save_population(self):
        if self.saved == True:
            return 'Population saved'
        else:
            raise Exception('Errors occured during saving population, check your output options in STANDARDS.conf')

    @save_population.setter
    def save_population(self, population):        
        getfiles = self.config.output_loc()
#        if getfiles['file_name'] 
#        population

        self.saved = True
