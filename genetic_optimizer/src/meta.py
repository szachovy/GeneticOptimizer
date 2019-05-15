
from abc import ABCMeta, abstractmethod

class Implement_Func(metaclass=ABCMeta):
    
    @abstractmethod
    def generate(self):
        raise NotImplementedError('Generator is temporarily unavailable')

    @abstractmethod
    def optimize(self):
        raise NotImplementedError('Optimizator is temporarily unavailable')

