
try:
    from fitness import Fitness

except ModuleNotFoundError as m:
    from .fitness import Fitness


from sklearn import svm


class Optimizer(Fitness):
    def __init__(self, file_name):
        super().__init__(file_name)
        print(self.log)
        print(self.config.performance())