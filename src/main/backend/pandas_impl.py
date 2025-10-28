from .base import Data
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


class PandasData(Data):
    def __init__(self, filename=None, read_mode=None, sep=None):
        super().__init__(filename, read_mode)
        self.read_data_wrapper(filename, read_mode, sep)

    def read_data_wrapper(self, filename, read_mode, sep=None):
        raw_data = super().read_data_wrapper(filename, read_mode)
        
        if read_mode == "arff":
            columns = [attr[0] for attr in raw_data["attributes"]]
            self.df = pd.DataFrame(raw_data["data"], columns=columns)
        elif read_mode == "csv":
            if sep == None:
                self.df = pd.read_csv(raw_data)
            else:
                self.df = pd.read_csv(raw_data, sep=sep)

    def summary(self):
        return self.df.describe()


    def zeroR_pandas(self, class_col):
        most_common = self.df[class_col].mode()[0]
        return most_common


    def oneR_pandas(self, class_col):
        attributes = self.df.columns.drop(class_col)
        best_feature = None
        min_error = float('inf')
        rules = {}

        for  attribute in attributes:
            # Agrupa por feature e calcula a classe mais frequente
            grouped = self.df.groupby(attribute)[class_col].agg(lambda x: x.value_counts().idxmax())
            # Calcula erro
            predictions = self.df[attribute].map(grouped)
            error = (predictions != self.df[class_col]).sum()

            if error < min_error:
                min_error = error
                best_feature = attribute
                rules = grouped.to_dict()

        return best_feature, rules, min_error
    

    def apply_c45(self):
        pass