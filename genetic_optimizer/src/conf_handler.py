
__author__ = 'WJ Maj'

from configparser import ConfigParser
#check the path existence


class Load_Population(object):
    def __init__(self, a = 10):
        self.a = a
        print(self.a)

class Load_Configuration(object):
    '''
        This is auxiliary class for generator configuration purposes,
        used from DEFAULTS.ini file placed in this Generator directory.
    '''
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('./Generator/DEFAULTS.ini')
            
    def read(self, argument):
        return self.config.get('DEFAULT', argument)