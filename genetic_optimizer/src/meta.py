
__author__ = 'WJ Maj'

from abc import ABCMeta, abstractmethod

class Implement_Func(metaclass=ABCMeta):
    
    @abstractmethod
    def generate(self):
        raise

    @abstractmethod
    def optimize(self):
        raise

