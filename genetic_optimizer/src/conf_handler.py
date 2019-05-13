
__author__ = 'WJ Maj'

from configparser import ConfigParser
import os
import socket

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

class Load_Configuration(object):
    '''
        This is auxiliary class for generator configuration purposes,
        used from DEFAULTS.ini file placed in this Generator directory.
    '''
    PATH = './Generator/DEFAULTS.ini'

    def __init__(self):
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
    PATH = 'STANDARDS.conf'

    def __init__(self):
        if path_existence(self.PATH):
            self.config = ConfigParser()
            self.config.read(self.PATH)
            # REMEMBER TO CHANGE IT WHEN DEPLOY
            self.in_dir = str("../" + self.config.get('INPUTLOCATION', 'DIR'))
            self.out_dir =str("../" + self.config.get('OUTPUTLOCATION', 'DIR'))

    def performance(self):
        getperformance = {'min' : self.config.get('PERFORMANCE', 'MINITER'), 'max' : self.config.get('PERFORMANCE', 'MAXITER')}
        return getperformance

    def input_loc(self):
        if dir_existence(self.in_dir):        
            return self.in_dir

    def output_loc(self):
        if dir_existence(self.out_dir):
            getfiles = {'file_name' : None, 'fig_name' : None}

            if bool(self.config.get('OUTPUTLOCATION', 'DOOUT')):
                getfiles['file_name'] = str(self.out_dir + '/' + self.config.get('OUTPUTLOCATION', 'OUTNAME') + '.' + self.config.get('OUTPUTLOCATION', 'OUTFORMAT'))

            if bool(self.config.get('OUTPUTLOCATION', 'DOFIG')):
                getfiles['fig_name'] = str(self.out_dir + '/' + self.config.get('OUTPUTLOCATION', 'FIGNAME') + '.' + self.config.get('OUTPUTLOCATION', 'FIGFORMAT'))

            return getfiles

    def log_file(self):
        if dir_existence(self.out_dir):
            if bool(self.config.get('SYSTEM', 'LOGFILE')):
                return True
        return False

    def err_log_file(self):
        if dir_existence(self.out_dir):
            if bool(self.config.get('SYSTEM', 'ERRLOGFILE')):
                return True
        return False

    def timestamp(self):
        if bool(self.config.get('SYSTEM', 'SETTIMESTAMP')):
            return True
        else:
            return False

    def settimeit(self):
        if bool(self.config.get('SYSTEM', 'SETTIMEIT')):
            return True
        else:
            return False

    # i`ll do it later
    def server(self):
        if bool(self.config.get('SERVER', 'ACTIVE')):
            pass
        return
