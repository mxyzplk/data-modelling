from .base import Data


class PandasData(Data):
    def __init__(self, data):
        self.data = data

    def summary(self):
        return self.data.describe()
