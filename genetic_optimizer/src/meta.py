
from abc import ABCMeta, abstractmethod

class Implement_Func(metaclass=ABCMeta):
    
    @abstractmethod
    def generate(self):
        pass

    @abstractmethod
    def optimize(self):
        pass

