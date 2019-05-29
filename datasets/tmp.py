import pandas


population = pandas.read_csv('szri.csv')
population.drop(population.columns[0], axis=1, inplace=True)
population = population[population.loc[1]]
print(population)


#for gene in range(population.shape[1]):
#    population[gene] = 5
print(population)