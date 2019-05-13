
from conf_handler import Main_Configuration

class Preprocess_Dataframe(object):
    def __init__(self):
        a = Main_Configuration()
        print(a.performance())
        print(a.input_loc())
        print(a.output_loc())
        print(a.log_file())
        print(a.err_log_file())
        print(a.timestamp())
        print(a.settimeit())
            

Preprocess_Dataframe()