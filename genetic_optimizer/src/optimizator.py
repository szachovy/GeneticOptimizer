
__author__ = 'WJ Maj'

from sklearn.cluster import KMeans
import scipy.stats as stats

from collections import OrderedDict
import matplotlib.pyplot as plt
import math
import pandas as pd
import numpy as np
import operator

class Optimizer(object):
    """
        Head of opmizer operations.
        Provide statistic and ML algorithms in code execution.
        
        Argumens:
            performance: configuration performance data in execution
            fitted_population: population after fittness function run  
    """

    def __init__(self, performance, fitted_population):

        self.performance = performance
        self.fitted_population = fitted_population

    def elbow(self):
        """
            Find elbow point inside KMeans clustering.
            To get the most effective number of clusters according to the dataset

            Returns:
                number of cluster in the (elbow)
        """
        sum_of_squared_distances = []
 
        for cluster in range(1, int(self.fitted_population.shape[0]) + 1):
            clusters_no = KMeans(n_clusters=cluster)
            clusters_no = clusters_no.fit(self.fitted_population[['Chromosome', 'Total']])
            sum_of_squared_distances.append(clusters_no.inertia_)
        
        return self.linear_group_size(sum_of_squared_distances)
        
        # plt.plot(range(1, int(self.population.shape[0])), Sum_of_squared_distances, 'bx-')
        # plt.xlabel('cluster number')
        # plt.ylabel('Sum_of_squared_distances')
        # plt.title('Elbow method for optimal number of clusters')
        # plt.show()

    def linear_group_size(self, sum_of_squared_distances):
        """
            Algorithms for elbow method.
            It is a normal fuction which connects vertex of integrals and 
            calculates height of points:
            
            Returns:
                The highest point distance
        """
        slope = (sum_of_squared_distances[int(self.fitted_population.shape[0])-1] - sum_of_squared_distances[0]) / (int(self.fitted_population.shape[0]) - 1)
        intercept = sum_of_squared_distances[0] - slope
        
        distance = []

        for label in range(len(sum_of_squared_distances)):
            distance.append(abs((slope * label) - (sum_of_squared_distances[label]) + intercept)/(math.sqrt(slope**2 + intercept**2)))
        
        return distance.index(max(distance))
                    
    def group_population(self, save=False, data=False):
        """
            Use KMeans clustering alogrithms form scikit-learn framework to cluster groups of parents
            in order to perform parent selection later.

            Returns:
                population_groups: get labels and cluster centers in posterior parent selection algorithm
        """
        self.fitted_population['Chromosome'] = self.fitted_population['Chromosome'] * self.performance['chromosome_weight']

        population_groups = KMeans(n_clusters=self.elbow())
        population_groups.fit(self.fitted_population[['Chromosome', 'Total']])

        self.fitted_population = pd.concat([self.fitted_population, pd.Series(self.change_order(population_groups), name='Labels')], axis=1)

#        plt.title('Fitted chromosomes groups')
#        plt.xlabel('Number of chromosome')
#        plt.ylabel('Total fitted value')
#        plt.scatter(self.fitted_population['Chromosome'], self.fitted_population['Total'], c=population_groups.labels_)
#        plt.scatter(population_groups.cluster_centers_[:,0], population_groups.cluster_centers_[:,1], marker='x')
#        plt.show()

        
        if (save and data):
            plt.title('Fitted chromosomes groups')
            plt.xlabel('Number of chromosome')
            plt.ylabel('Total fitted value')
            plt.scatter(self.fitted_population['Chromosome'], self.fitted_population['Total'], c=population_groups.labels_)
            plt.scatter(population_groups.cluster_centers_[:,0], population_groups.cluster_centers_[:,1], marker='x')
#            plt.show()
            plt.savefig(data)

        else:
            return population_groups

    @staticmethod
    def change_order(population_groups) -> list:
        """
            By default number sign of clusters are selected randomly which affects wrongly estimation of distances between
            cluster centers later.

            To avoid this problem this function change every data set order from the smallest to the biggest.
            
            Args:
                population_groups: unordered population groups

            Returns:
                new_order: population groups with ascending order of notation 
        """
        order = {}
        pivot_order = {}
        new_order = []

        for k,v in enumerate(population_groups.cluster_centers_):
            order[int(k)] = v[1]

        pivot_order = list(OrderedDict(sorted(order.items(), key=operator.itemgetter(1))).keys())

        for label in list(population_groups.labels_):
            new_order.append(pivot_order.index(int(label)))
            
        return new_order

# ---------------------------------------------------------------------------------

    @staticmethod
    def cluster_distances(population_groups) -> list:
        """
            Measure distance between each cluster recursively in order to set list of data
            converted later for probability in roulette wheel

            Args:
                population_groups: ouput generated from KMeans

            Returns:
                centroid_dists: list of distances between centroids measurement
        """
        centroid_dists = []
        centroids = list(population_groups.cluster_centers_)

        centroids.sort(key=lambda x: x[1])

        for destination_cluster, value in enumerate(centroids):
            dists = []
            for source_cluster, value in enumerate(centroids):
                if (centroids[source_cluster][0] == centroids[destination_cluster][0]) and (centroids[source_cluster][1] == centroids[destination_cluster][1]):
                    pass
                else:
                    dist = math.sqrt((centroids[source_cluster][0] - centroids[destination_cluster][0])**2 + (centroids[source_cluster][1] - centroids[destination_cluster][1])**2)
                    dists.append(dist)
            
            centroid_dists.append(dists)

        return centroid_dists


    def roulette_wheel_selection(self, population_groups) -> dict:
        """
            Exchange cluster distances into probability of cluster selection in second parent selection/

            Args:
                population_groups: ouput generated from KMeans

            Returns:
                probability: dict of each cluster probabilities to draw second parent in child creation
        """
        centroid_dists = self.cluster_distances(population_groups)

        max_prob = [sum(dist) for dist in centroid_dists]
        cluster = 0
        probability = {}

        for centroid in centroid_dists:
            dist = []
            for target in centroid:
                dist.append(target / max_prob[cluster])

            dist.insert(cluster, 0)
            probability[cluster] = dist
            cluster += 1

        return probability

    def next_generation(self, population_groups, population):
        """
            Develop next generation of population according to fitted population ingredients

            Args:
                population_groups: ouput generated from KMeans
                population: clean population dataset without add ons

            Returns:
                population: new population with inserted childrens and worse parent removed 
        """
        probability = self.roulette_wheel_selection(population_groups)
        
        self.fitted_population['Chromosome'] = self.fitted_population['Chromosome'] / self.performance['chromosome_weight']
        self.fitted_population['Selected'] = pd.Series(data=[False for row in range(self.fitted_population.shape[0])])

#        print(self.fitted_population)
        try:
            similarity = 0

            while ((self.fitted_population['Selected'] == True).sum() / self.fitted_population.shape[0]) < self.performance['shuffle_scale']:
                first_parent = None
                second_parent = None

                while True:
                    first_parent = self.choose_first_parent()
                    second_parent = self.choose_second_parent(probability, first_parent)
            
                    if int(first_parent.isnull().sum(axis = 1)) == int(second_parent.isnull().sum(axis=1)):
                        break
    
                F_test = stats.f_oneway(first_parent.iloc[:, 0: self.fitted_population.columns.get_loc('Total')].values[0], second_parent.iloc[:, 0: self.fitted_population.columns.get_loc('Total')].values[0])
    
                worse_parent_total = min(float(first_parent['Total']), float(second_parent['Total']))
                better_parent_total = max(float(first_parent['Total']), float(second_parent['Total']))
    
                parent_survived = first_parent if int(first_parent['Labels']) > int(second_parent['Labels']) else second_parent
    
                child = self.child(first_parent, second_parent)
                child_F_test = stats.f_oneway(child.iloc[:, 0: self.fitted_population.columns.get_loc('Total')].values[0], parent_survived.iloc[:, 0: self.fitted_population.columns.get_loc('Total')].values[0])
    
#                print(self.fitted_population)
                if (child_F_test[0] != 0) and (F_test[0] > child_F_test[0]) and ((better_parent_total + worse_parent_total) < (better_parent_total + float(child['Total'])) * self.performance['variety']):
    
                    child = pd.concat([child, pd.Series(int(second_parent['Chromosome']) if int(first_parent['Labels']) > int(second_parent['Labels']) else int(first_parent['Chromosome']), name='Chromosome'), pd.Series(min(int(first_parent['Labels']), int(second_parent['Labels'])), name='Labels'), pd.Series(True, name='Selected')], axis=1)

                    self.update_fitted_population(child)
                    population = self.update_population(population, child, first_parent, second_parent)

#                    print(self.fitted_population)

                else:
                    if similarity > self.fitted_population.shape[0] * (1 - self.performance['variety']):
                        return population
                    else:
                        similarity += 1

            return population
        
        except ValueError as v:
            print('Your population is not adapted for your config parameters. Changing SHUFFLE_SCALE or VARIETY may avoid this kind of problems')


    def choose_first_parent(self): # Choose first parent to injection
        return self.fitted_population[self.fitted_population['Selected'] == False].sample(n = 1)

    def choose_second_parent(self, probability, first_parent): # Choose second parent to injection
        label = np.random.choice([cluster for cluster in probability.keys()], p=probability[int(first_parent['Labels'])])
        return self.fitted_population[(self.fitted_population['Selected'] == False) & (self.fitted_population['Labels'] == label)].sample(n = 1)        

    def child(self, first_parent, second_parent): # Match child with parents genes
        child = {}
    
        for column in range(self.fitted_population.columns.get_loc('Total')):
            child[column] = [(max(float(first_parent[column]), float(second_parent[column])))]
            
        child['Total'] = sum([sum(value) for value in child.values()])

        return pd.DataFrame.from_dict(child)


    def update_fitted_population(self, child): # Update fitted population with child
        self.fitted_population.set_index('Chromosome')
        self.fitted_population.update(child.set_index('Chromosome'))
        self.fitted_population.reset_index()

    def update_population(self, population, child, first_parent, second_parent): # update real population with child
        for gene in range(population.shape[1]):
            population.iat[int(child['Chromosome']), gene] = max(population.loc[int(first_parent['Chromosome'])][gene], population.loc[int(second_parent['Chromosome'])][gene])
        return population

