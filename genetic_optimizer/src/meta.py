
__author__ = 'WJ Maj'

from abc import ABCMeta, abstractmethod

class Implement_Func(metaclass=ABCMeta):
    """
        Check main class.
        
        Returns:
            raise: if reference problem occurred in first stadium of connections with src
    """    
    @abstractmethod
    def generate(self):
        raise

    @abstractmethod
    def optimize(self):
        raise

