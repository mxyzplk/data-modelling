import os
import yaml

class Config:
    def __init__(self):
        self.config = None
        self.read_config()


    def read_config(self):

        backend_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(backend_dir, '..', '..') 
        resources_dir = os.path.join(project_root, 'resources')
        filepath = os.path.join(resources_dir,  'config.yaml')        

        with open(filepath, "r") as f:
            
            self.config = yaml.safe_load(f)
