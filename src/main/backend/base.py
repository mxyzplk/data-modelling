import os
import arff


class Data:
    def __init__(self, filename=None, read_mode=None):
        self.df = None


    def read_data_wrapper(self, filename, read_mode):

        if read_mode == "arff":

            self.read_data_arff(filename)

        if read_mode == "csv":

            self.read_data_csv(filename)
        

    def read_data_arff(self, filename):

        backend_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(backend_dir, '..', '..')  
        resources_dir = os.path.join(project_root, 'resources', 'data')
        filepath = os.path.abspath(os.path.join(resources_dir, filename))

        with open(filepath, "r") as f:
            
            raw_data = arff.load(f)

        return raw_data

    def read_data_csv(self, filename):

        backend_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(backend_dir, '..', '..')  
        resources_dir = os.path.join(project_root, 'resources', 'data')
        raw_data = os.path.abspath(os.path.join(resources_dir, filename))
        
        return raw_data





