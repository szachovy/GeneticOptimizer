
try:
    from fitness import Fitness

except ModuleNotFoundError as m:
    from .fitness import Fitness

from sklearn.cluster import KMeans


#from sklearn.cluster import KMeans
#naive bayes

class Optimizer(Fitness):
    def __init__(self, file_name):
        super().__init__(file_name)
        self.performance = self.config.performance()
        self.fitted_population = self.fit_population()
        print(self.fitted_population)
#        self.elbow()
        self.group_population()

    def elbow(self):
        print(self.fitted_population.shape[0])
        for cluster in range(1, 101):
            kmeanModel = KMeans(n_clusters=cluster).fit(self.fitted_population)
            kmeanModel.fit(self.fitted_population)
            distortions.append(sum(np.min(cdist(self.fitted_population, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / self.fitted_population.shape[0])

    def group_population(self):
        self.fitted_population['Chromosome'] = self.fitted_population['Chromosome'] * self.performance['chromosome_weight']
        population_groups = KMeans(n_clusters=4)
        population_groups.fit(self.fitted_population[['Chromosome', 'Total']])
        print(population_groups.labels_)