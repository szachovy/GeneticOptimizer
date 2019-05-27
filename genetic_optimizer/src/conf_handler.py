
__author__ = 'WJ Maj'

from configparser import ConfigParser
import os
import socket
import platform
import numpy as np

def path_existence(PATH):
    '''
        Check the path existence of two main configuration files.
        ...
    '''
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


def os_slashes(init):
    def wrapper(*args, **kwargs):
        if platform.system() == 'Linux':
            kwargs['slashes'] = '/'
        else:
            kwargs['slashes'] = '\\'

        init(*args, **kwargs)
    return wrapper


class Load_Configuration(object):
    '''
        This is auxiliary class for generator configuration purposes,
        used from DEFAULTS.ini file placed in this Generator directory.
    '''

    @os_slashes
    def __init__(self, slashes):
        self.PATH = '.{}Generator{}DEFAULTS.ini'.format(slashes, slashes)
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

    @os_slashes
    def __init__(self, iterations, shuffle_scale, variety, chromosome_weight, slashes):
        self.user_provided_input = {'iterations': iterations, 'shuffle_scale': shuffle_scale, 'variety': variety, 'chromosome_weight': chromosome_weight}
        self.PATH = '.{}src{}STANDARDS.conf'.format(slashes, slashes)
        if path_existence(self.PATH):
            self.config = ConfigParser()
            self.config.read(self.PATH)
            # REMEMBER TO CHANGE IT WHEN DEPLOY IF ERR
            self.in_dir = str(".{}" + self.config.get('INPUTLOCATION', 'DIR') + "{}").format(slashes, slashes)
            self.out_dir =str(".{}" + self.config.get('OUTPUTLOCATION', 'DIR') + "{}").format(slashes, slashes)

    def performance(self):
        getperformance = {'iterations' : float(self.config.get('PERFORMANCE', 'ITER')), 'shuffle_scale' : float(self.config.get('PERFORMANCE', 'SHUFFLE_SCALE')) , 'chromosome_weight' : float(self.config.get('PERFORMANCE', 'CHROMOSOMELAYERWEIGHT')), 'variety': float(self.config.get('PERFORMANCE', 'VARIETY'))}
        
        for key, value in self.user_provided_input.items():
            if value is not None:
                getperformance[key] = value
        
        if (getperformance['shuffle_scale'] or getperformance['variety']) not in np.arange(0, 2, 0.01):
            raise Exception('Sum of crossover probability and mutation probability must be in range from 0 to 1 (0% - 100%)')
                
        elif (getperformance['iterations'] or getperformance['chromosome_weight']) < 0:
            raise Exception('All features in PERFORMANCE section must be positive')

        else:
            return getperformance

    def input_loc(self):
        if dir_existence(self.in_dir):        
            return self.in_dir

    def output_loc(self):
        if any([bool(self.config.get('OUTPUTLOCATION', 'DOOUT')), bool(self.config.get('OUTPUTLOCATION', 'DOFIG')), bool(self.config.get('OUTPUTLOCATION', 'DOLOG'))]):
            if dir_existence(self.out_dir):
                getfiles = {'file_name' : False, 'fig_name' : False, 'log_name' : False}

                if bool(self.config.get('OUTPUTLOCATION', 'DOOUT')):
                    getfiles['file_name'] = str(self.out_dir + self.config.get('OUTPUTLOCATION', 'OUTNAME') + '.' + self.config.get('OUTPUTLOCATION', 'OUTFORMAT'))

                if bool(self.config.get('OUTPUTLOCATION', 'DOFIG')):
                    getfiles['fig_name'] = str(self.out_dir + self.config.get('OUTPUTLOCATION', 'FIGNAME') + '.' + self.config.get('OUTPUTLOCATION', 'FIGFORMAT'))

                if bool(self.config.get('OUTPUTLOCATION', 'DOLOG')):
                    getfiles['log_name'] = str(self.out_dir + self.config.get('OUTPUTLOCATION', 'LOGNAME') + '.' + self.config.get('OUTPUTLOCATION', 'LOGFORMAT'))

                return getfiles
        else:
            return False

    # i`ll do it later
    def server(self):
        if bool(self.config.get('SERVER', 'ACTIVE')):
            pass
        return

