
from sklearn.cluster import KMeans
import scipy.stats as stats

from collections import OrderedDict
import matplotlib.pyplot as plt
import math
import pandas as pd
import numpy as np
import operator

class Optimizer(object):

    def __init__(self, performance, fitted_population):

        self.performance = performance
        self.fitted_population = fitted_population

    def elbow(self):
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
        
        slope = (sum_of_squared_distances[int(self.fitted_population.shape[0])-1] - sum_of_squared_distances[0]) / (int(self.fitted_population.shape[0]) - 1)
        intercept = sum_of_squared_distances[0] - slope
        
        distance = []

        for label in range(len(sum_of_squared_distances)):
            distance.append(abs((slope * label) - (sum_of_squared_distances[label]) + intercept)/(math.sqrt(slope**2 + intercept**2)))
        
        return distance.index(max(distance))
                    
    def group_population(self):
        self.fitted_population['Chromosome'] = self.fitted_population['Chromosome'] * self.performance['chromosome_weight']

        population_groups = KMeans(n_clusters=self.elbow())
        population_groups.fit(self.fitted_population[['Chromosome', 'Total']])

        self.fitted_population = pd.concat([self.fitted_population, pd.Series(self.change_order(population_groups), name='Labels')], axis=1)
        
        # plt.title('Fitted chromosomes groups')
        # plt.xlabel('Number of chromosome')
        # plt.ylabel('Total value')
        # plt.scatter(self.fitted_population['Chromosome'], self.fitted_population['Total'], c=population_groups.labels_)
        # plt.scatter(population_groups.cluster_centers_[:,0], population_groups.cluster_centers_[:,1], marker='x')
        # plt.show()
        return population_groups

    @staticmethod
    def change_order(population_groups):
        order = {}
        pivot_order = {}
        new_order = []

        for k,v in enumerate(population_groups.cluster_centers_):
            order[int(k)] = v[1]

        pivot_order = list(OrderedDict(sorted(order.items(), key=operator.itemgetter(1))).keys())

        for label in list(population_groups.labels_):
            new_order.append(pivot_order.index(int(label)))
            
        return new_order

    @staticmethod
    def cluster_distances(population_groups):
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


    def roulette_wheel_selection(self, population_groups):
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

    def parent_selection(self, population_groups, population):
        probability = self.roulette_wheel_selection(population_groups)
        print(probability)
        
        self.fitted_population['Chromosome'] = self.fitted_population['Chromosome'] / self.performance['chromosome_weight']

        self.fitted_population['Selected'] = pd.Series(data=[False for row in range(self.fitted_population.shape[0])])
        print(self.fitted_population)
        
        first_parent = self.fitted_population[self.fitted_population['Selected'] == False].sample(n = 1)
        print(first_parent)
 
        label = np.random.choice([cluster for cluster in probability.keys()], p=probability[int(first_parent['Labels'])])
        second_parent = self.fitted_population[(self.fitted_population['Selected'] == False) & (self.fitted_population['Labels'] == label)].sample(n = 1)
        print(second_parent)

        print(self.fitted_population['Total'].loc[self.fitted_population['Labels'].isin(first_parent['Labels'])])
        print(self.fitted_population['Total'].loc[self.fitted_population['Labels'].isin(second_parent['Labels'])])
        F_test = stats.f_oneway(first_parent.iloc[:, 0: self.fitted_population.columns.get_loc('Total')].values[0], second_parent.iloc[:, 0: self.fitted_population.columns.get_loc('Total')].values[0]) 
        #F_test = stats.f_oneway(self.fitted_population['Total'].loc[self.fitted_population['Labels'].isin(first_parent['Labels'])], self.fitted_population['Total'].loc[self.fitted_population['Labels'].isin(second_parent['Labels'])])

 
        
        child = {}
        for column in range(self.fitted_population.columns.get_loc('Total')):
            child[column] = [(max(float(first_parent[column]), float(second_parent[column])))]
        
        child['Total'] = sum([sum(value) for value in child.values()])

        worse_parent_total = min(float(first_parent['Total']), float(second_parent['Total']))
        better_parent_total = max(float(first_parent['Total']), float(second_parent['Total']))

        parent_survived = first_parent if int(first_parent['Labels']) > int(second_parent['Labels']) else second_parent

        child = pd.DataFrame.from_dict(child)
        print(child)
        child_F_test = stats.f_oneway(child.iloc[:, 0: self.fitted_population.columns.get_loc('Total')].values[0], parent_survived.iloc[:, 0: self.fitted_population.columns.get_loc('Total')].values[0])
        print(F_test[0])
        print(child_F_test[0])

        print(better_parent_total + worse_parent_total)
        print(better_parent_total + float(child['Total']) * self.performance['variety'])

        child = pd.concat([child, pd.Series(int(second_parent['Chromosome']) if int(first_parent['Labels']) > int(second_parent['Labels']) else int(first_parent['Chromosome']), name='Chromosome'), pd.Series(min(int(first_parent['Labels']), int(second_parent['Labels'])), name='Labels'), pd.Series(True, name='Selected')], axis=1)        
        get_worse_parent_index = int(self.fitted_population['Chromosome'].loc[int(first_parent['Chromosome']) if float(first_parent['Total']) == worse_parent_total else int(second_parent['Chromosome'])])
        print(child)
#        self.fitted_population = pd.concat([self.fitted_population, child]).drop_duplicates(keep='last').sort_values('Chromosome')
        self.fitted_population.set_index('Chromosome')
        self.fitted_population.update(child.set_index('Chromosome'))
        self.fitted_population.reset_index()
#        self.fitted_population.loc[[get_worse_parent_index]] = child
        
#        self.fitted_population.drop(labels=[get_worse_parent_index], inplace=True)
        #place = self.fitted_population['Chromosome'].loc[int(first_parent['Chromosome']) if float(first_parent['Total']) == worse_parent_total else int(second_parent['Chromosome'])]
        #self.fitted_population[place] = child
        print(self.fitted_population)
        print(population)

        for gene in range(population.shape[1]):
            population.loc[int(child['Chromosome'])][gene] = max(population.loc[int(first_parent['Chromosome'])][gene], population.loc[int(second_parent['Chromosome'])][gene])

        print(population.loc[int(child['Chromosome'])])
        print(population)
#        if (child_F_test[0] != 0) and (F_test[0] > child_F_test[0]) and ((better_parent_total + worse_parent_total) < (better_parent_total + float(child['Total'])) * self.performance['variety']):
#            print('weszlo')
            # child = pd.concat([child, pd.Series(int(second_parent['Chromosome']) if int(first_parent['Labels']) > int(second_parent['Labels']) else int(first_parent['Chromosome']), name='Chromosome'), pd.Series(min(int(first_parent['Labels']), int(second_parent['Labels'])), name='Labels'), pd.Series(True, name='Selected')], axis=1)
            # place = self.fitted_population['Chromosome'].loc[int(first_parent['Chromosome']) if float(first_parent['Total']) == worse_parent_total else int(second_parent['Chromosome'])]
# 
        # 
            # self.fitted_population[place] = child
            # print(self.fitted_population)
#            place += 1
#            self.fitted_population.drop(self.fitted_population.loc[place])
#            print(self.fitted_population)
            
#            -----------------
#            child_F_test = stats.f_oneway(self.fitted_population['Total'].loc[self.fitted_population['Labels'] == child['Labels']], self.fitted_population['Total'].loc[self.fitted_population['Labels'] == max(int(first_parent['Labels']), int(second_parent['Labels']))])        
                

        # while (sum(self.fitted_population.iloc(self.fitted_population['Selected'] == True)) / self.fitted_population.shape[0]) > self.performance['shuffle_scale']:
            # first_parent = self.fitted_population[self.fitted_population['Selected'] == False].sample(n = 1)
            # print(first_parent)
# 
            # label = np.random.choice([cluster for cluster in probability.keys()], p=probability[int(first_parent['Labels'])])
            # second_parent = self.fitted_population[(self.fitted_population['Selected'] == False) & (self.fitted_population['Labels'] == label)].sample(n = 1)
            # print(second_parent)
        # 
            # print(self.fitted_population['Total'].loc[self.fitted_population['Labels'].isin(first_parent['Labels'])])
            # print(self.fitted_population['Total'].loc[self.fitted_population['Labels'].isin(second_parent['Labels'])])
# 
            # F_test = stats.f_oneway(self.fitted_population['Total'].loc[self.fitted_population['Labels'].isin(first_parent['Labels'])], self.fitted_population['Total'].loc[self.fitted_population['Labels'].isin(second_parent['Labels'])])
            # print(F_test)
            # print(F_test[0])
        # 
            # child = {}
            # for column in range(self.fitted_population.columns.get_loc('Total')):
                # child[column] = [(max(first_parent[column], second_parent[column]))]
# 
            # child['Total'] = sum([column for column in child.values()])
            # 
            # worse_parent_total = min(first_parent['Total'], second_parent['Total'])
            # better_parent_total = max(first_parent['Total'], second_parent['Total'])
            # 
            # if (better_parent_total + worse_parent_total) < (better_parent_total + child['Total']) * self.performance['variety']:
                # if first_parent['Labels'] > second_parent['Labels']:
                    # child['Chromosome'] = second_parent['Chromosome']
                # else:
                    # child['Chromosome'] = first_parent['Chromosome']
# 
                # child['Labels'] = min(first_parent['Labels'], second_parent['Labels'])
                # child['Selected'] = True
# 
                # child_F_test = stats.f_oneway(self.fitted_population['Total'].loc[self.fitted_population['Labels'].isin(max(first_parent['Labels'], second_parent['Labels']))], self.fitted_population['Total'].loc[self.fitted_population['Labels'].isin(child['Labels'])])
            # 
                # if F_test[0] > child_F_test[0]:
                    # for column in range(self.fitted_population.columns.get_loc('Total')):
                        # if child[column] == first_parent[column]:
                            # population.get_value(self.fitted_population['Chromosome'].loc[self.fitted_population['Total'] == worse_parent_total], column) = population.get_value(self.fitted_population['Chromosome'].loc[...], column)
                        # else:
                            # population.get_value(self.fitted_population['Chromosome'].loc[self.fitted_population['Total'] == worse_parent_total], column) = population.get_value(self.fitted_population['Chromosome'].loc[...], column)
# 
                    # place = self.fitted_population['Chromosome'].loc[self.fitted_population['Total'] == (min(first_parent['Total'], second_parent['Total']))]
                    # self.fitted_population.loc[place] = child
                    # place += 1
                    # self.fitted_population.drop(self.fitted_population.loc[place])
# 
        # return population

        
