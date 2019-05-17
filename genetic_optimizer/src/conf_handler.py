
__author__ = 'WJ Maj'

from configparser import ConfigParser
import os
import socket
import platform
import numpy as np

def path_existence(PATH):
    try:
        assert(os.path.exists(PATH))
        return True
    except AssertionError as a:
        raise IOError("selected configuration file doesn`t exist in that place")    

def dir_existence(path):
    try:
        assert(os.path.isdir(path))
        return True
    except AssertionError as a:
        raise IOError("input or output dir moved or doesn`t exists")  

def os_slashes():
    if platform.system() == 'Linux':
        return '/'
    else:
        return '\\'

class Load_Configuration(object):
    '''
        This is auxiliary class for generator configuration purposes,
        used from DEFAULTS.ini file placed in this Generator directory.
    '''

    def __init__(self):
        self.slashes = os_slashes()
        self.PATH = '.{}Generator{}DEFAULTS.ini'.format(self.slashes, self.slashes)
        if path_existence(self.PATH):
            self.config = ConfigParser()
            self.config.read(self.PATH)
            
    def read(self, argument):
        return self.config.get('DEFAULT', argument)


class Main_Configuration(object):
    '''
        Configuration class used by STANDARDS.conf to manipulate
        some behaviour used for genetic_optimizer algorythms
    '''

    def __init__(self):
        self.slashes = os_slashes()
        self.PATH = '.{}src{}STANDARDS.conf'.format(self.slashes, self.slashes)
        if path_existence(self.PATH):
            self.config = ConfigParser()
            self.config.read(self.PATH)
            # REMEMBER TO CHANGE IT WHEN DEPLOY IF ERR
            self.in_dir = str(".{}" + self.config.get('INPUTLOCATION', 'DIR') + "{}").format(self.slashes, self.slashes)
            self.out_dir =str(".{}" + self.config.get('OUTPUTLOCATION', 'DIR') + "{}").format(self.slashes, self.slashes)

    def performance(self):
        cross = float(self.config.get('PERFORMANCE', 'CROSSPROB'))
        mut = float(self.config.get('PERFORMANCE', 'MUTATIONPROB'))
        miniter = float(self.config.get('PERFORMANCE', 'MINITER'))
        maxiter = float(self.config.get('PERFORMANCE', 'MAXITER'))
        chromosome_weight = float(self.config.get('PERFORMANCE', 'CHROMOSOMELAYERWEIGHT'))


        if (cross or mut) not in np.arange(0, 2, 0.01):
            raise Exception('Sum of crossover probability and mutation probability must be in range from 0 to 1 (0% - 100%)')
        
        elif (miniter or maxiter or chromosome_weight) < 0:
            raise Exception('All features in PERFORMANCE section must be positive')

        elif miniter > maxiter:
            raise Exception('Minimum number of iterations cannot be greater number than maximun number of iterations')

        else:
            getperformance = {'min' : miniter, 'max' : maxiter,
                            'cross' : cross, 'mut' : mut, 'chromosome_weight' : chromosome_weight}
            return getperformance

    def input_loc(self):
        if dir_existence(self.in_dir):        
            return self.in_dir

    def output_loc(self):
        if dir_existence(self.out_dir):
            getfiles = {'file_name' : None, 'fig_name' : None}

            if bool(self.config.get('OUTPUTLOCATION', 'DOOUT')):
                getfiles['file_name'] = str(self.out_dir + self.config.get('OUTPUTLOCATION', 'OUTNAME') + '.' + self.config.get('OUTPUTLOCATION', 'OUTFORMAT'))

            if bool(self.config.get('OUTPUTLOCATION', 'DOFIG')):
                getfiles['fig_name'] = str(self.out_dir + self.config.get('OUTPUTLOCATION', 'FIGNAME') + '.' + self.config.get('OUTPUTLOCATION', 'FIGFORMAT'))

            return getfiles

    def log_file(self):
        if dir_existence(self.out_dir):
            if bool(self.config.get('SYSTEM', 'LOGFILE')):
                return True
        return False

    def timestamp(self):
        if bool(self.config.get('SYSTEM', 'SETTIMESTAMP')):
            return True
        else:
            return False

    # i`ll do it later
    def server(self):
        if bool(self.config.get('SERVER', 'ACTIVE')):
            pass
        return

