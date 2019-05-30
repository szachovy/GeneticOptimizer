# Genetic Optimizer
_Genetic algorithm optimizer using K-Means clustering with one way ANOVA algorithms_

[![Build Status](https://travis-ci.org/szachovy/GeneticOptimizer.svg?branch=master)](https://travis-ci.org/szachovy/GeneticOptimizer)

## Before:
![github-small](https://github.com/szachovy/GeneticOptimizer/blob/master/Images/first.png)

## After:
![github-small](https://github.com/szachovy/GeneticOptimizer/blob/master/Images/last.svg)

## Installation:

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install genetic_optimizer.

```bash
pip3 install genetic-optimizer
```

### Note:

Package require =>Python 3.6.5, using genetic_optimizer in Python 2.x.x projects may not work correctly.
If you are not sure about your python version, try:

```bash
python3 --version
```

## Usage

```python
import genetic_optimizer

some_object = genetic_optimizer.Optimizer()
some_object = generate(population_size=46, chromosome_size=8, equal_chromosomes=True, initialization_method='Random', representation='Binary', saving_method='csv')
```

_These are default options for generator, you can change them in DEFAULTS.ini file in package directory_

```python
some_object = optimize(data=None, iterations=12, shuffle_scale=0.6, variety=0.8, chromosome_weight=0.0000001)
```

_These are default options for optimizer, you can change them in STANDARDS.conf file in package directory_

### Note

- If optimizer got stuck at the beginning, that usually means that your dataframe with population to small to find appropiate parents in order to create next generations.

- For more description, please check out project wiki.

## Pros
- There is no mutation and crossover probability. Program matches parents according to group differences and create new child, built from the _most successful_ pairs of genes from them.
  That means new generations are closer to each one and every child is _not worse_ that _genetic worse_ parent.

- You can play off with options to achive more precised results.

## Cons

- Fitness and parent selection process takes place recursively. If you are not using some RDD computing, program execution may be longer.

## Contributing

Pull requests are welcome. 
For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Tools

- [micro editor](https://micro-editor.github.io/)
- Unix console

_Code is mostly written in accordance with [Google PEP style guide](https://google.github.io/styleguide/pyguide.html)_


