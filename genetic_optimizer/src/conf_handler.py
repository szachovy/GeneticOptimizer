
__author__ = 'WJ Maj'

from configparser import ConfigParser
import os
import socket
import platform
import numpy as np

def path_existence(PATH : str) -> bool:
    """
        Check the path existence of configuration files.
    """
    try:
        assert(os.path.exists(PATH))
        return True
    except AssertionError as a:
        raise IOError("selected configuration file doesn`t exist in that place")    


def dir_existence(path : str) -> bool:
    """
        Check the directory existence of configuration files
    """
    try:
        assert(os.path.isdir(path))
        return True
    except AssertionError as a:
        raise IOError("input or output dir moved or doesn`t exists")  


def os_slashes(init): # perform system slashes
    def wrapper(*args, **kwargs):
        if platform.system() == 'Windows':
            kwargs['slashes'] = '\\'
        else:
            kwargs['slashes'] = '/'

        init(*args, **kwargs)
    return wrapper


class Load_Configuration(object):
    '''
        This is auxiliary class for generator configuration purposes,
        used from DEFAULTS.ini file placed in this Generator directory.
    '''

    @os_slashes
    def __init__(self, slashes):
        os.path.dirname(os.path.realpath(__file__))
#        self.PATH = '.{}Generator{}DEFAULTS.ini'.format(slashes, slashes)
        self.PATH = '{}{}DEFAULTS.ini'.format(os.path.dirname(os.path.realpath(__file__)), slashes)
        if path_existence(self.PATH):
            self.config = ConfigParser()
            self.config.read(self.PATH)
            
    def read(self, argument):
        return self.config.get('DEFAULT', argument)


class Main_Configuration(object):
    """
        Configuration class used by STANDARDS.conf to manipulate
        some behaviour used for genetic_optimizer algorythms
    """

    @os_slashes
    def __init__(self, iterations, shuffle_scale, variety, chromosome_weight, slashes):
        self.user_provided_input = {'iterations' : iterations, 'shuffle_scale': shuffle_scale, 'variety': variety, 'chromosome_weight': chromosome_weight}
        self.PATH = '{}{}STANDARDS.conf'.format(os.path.dirname(os.path.realpath(__file__)), slashes)
        if path_existence(self.PATH):
            self.config = ConfigParser()
            self.config.read(self.PATH)
            
            directory = os.path.join(os.getcwd(), self.config.get('OUTPUTLOCATION', 'DIR'))
            if not os.path.exists(directory):
               os.makedirs(directory)            

            self.out_dir = str(directory) + '{}'.format(slashes)

    def performance(self) -> dict:
        """ 
            Performance section in STANDARDS.conf
            Accumulate user provided input with default options
        """
        getperformance = {'iterations' : float(self.config.get('PERFORMANCE', 'ITERATIONS')), 'shuffle_scale' : float(self.config.get('PERFORMANCE', 'SHUFFLE_SCALE')) , 'chromosome_weight' : float(self.config.get('PERFORMANCE', 'CHROMOSOMELAYERWEIGHT')), 'variety': float(self.config.get('PERFORMANCE', 'VARIETY'))}
        for key, value in self.user_provided_input.items():
            if value is not None:
                getperformance[key] = value

        if (round(getperformance['shuffle_scale'], 2) or round(getperformance['variety'], 2)) not in np.arange(0, 2, 0.01):
            raise Exception('shuffle_scale or variety must be in range from 0 to 1 (0% - 100%)')

        elif (getperformance['iterations'] or getperformance['chromosome_weight']) < 0:
            raise Exception('All features must be positive')

        else:
            return getperformance

    def output_loc(self):
        """
            Route to output directory if some saving options were provided
        """
        if any([self.config.getboolean('OUTPUTLOCATION', 'DOOUT'), self.config.getboolean('OUTPUTLOCATION', 'DOFIG'), self.config.getboolean('OUTPUTLOCATION', 'DOLOG')]):
            if dir_existence(self.out_dir):
                getfiles = {'file_name' : False, 'fig_name' : False, 'log_name' : False}

                if self.config.getboolean('OUTPUTLOCATION', 'DOOUT'):
                    getfiles['file_name'] = str(self.out_dir + self.config.get('OUTPUTLOCATION', 'OUTNAME') + '.' + self.config.get('OUTPUTLOCATION', 'OUTFORMAT'))

                if self.config.getboolean('OUTPUTLOCATION', 'DOFIG'):
                    getfiles['fig_name'] = str(self.out_dir + self.config.get('OUTPUTLOCATION', 'FIGNAME') + '.' + self.config.get('OUTPUTLOCATION', 'FIGFORMAT'))

                if self.config.getboolean('OUTPUTLOCATION', 'DOLOG'):
                    getfiles['log_name'] = str(self.out_dir + self.config.get('OUTPUTLOCATION', 'LOGNAME') + '.' + self.config.get('OUTPUTLOCATION', 'LOGFORMAT'))

                return getfiles
        else:
            return False

    # i`ll do it later
    def server(self):
        if self.config.getboolean('SERVER', 'ACTIVE'):
            pass
        return

