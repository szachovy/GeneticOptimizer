
__author__ = 'WJ Maj'
__all__ = ['Load_Population']

from configparser import ConfigParser
#check the path existence

class Load_Population(object):
    def __init__(self, a = 10):
        self.a = a
        print(self.a)