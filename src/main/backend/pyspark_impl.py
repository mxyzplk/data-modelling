from .base import Data


class PySparkData(Data):
    def __init__(self, data):
        self.data = data


    def summary(self):
        return self.data.describe().toPandas()