import os
import arff


class Data:
    def __init__(self, filename, read_mode, backend_mode):
        self.data = None

         

    def read_data_wrapper(self, filename, read_mode):

        if read_mode == "arff":

            self.read_data_arff(filename)

        if read_mode == "csv":

            self.read_data_csv(filename)
        

    def read_data_arff(self, filename):

        main_dir = os.path.dirname(os.path.abspath(__file__))
        resources_dir = os.path.join(main_dir, '../resources')
        filepath = os.path.join(resources_dir, 'data', filename)

        with open(filepath, "r") as f:
            
            self.data = arff.load(f)

    def read_data_csv(self, filename):
        
        pass


class PandasData(Data):
    def __init__(self, data):
        self.data = data

    def summary(self):
        return self.data.describe()


class PySparkData(Data):
    def __init__(self, data):
        self.data = data


    def summary(self):
        return self.data.describe().toPandas()

