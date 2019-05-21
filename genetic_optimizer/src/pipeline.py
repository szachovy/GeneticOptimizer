# All sumarized here

try:
    from conf_handler import Main_Configuration
except ModuleNotFoundError as m
    from .conf_handler import Main_Configuration


from datetime import datetime


class Pipeline():
    def __init__(self):
        self.config = Main_Configuration()                
        pass