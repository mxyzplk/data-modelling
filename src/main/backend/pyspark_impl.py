from .base import Data
from pyspark.sql import SparkSession
import pandas as pd


class PySparkData(Data):
    def __init__(self, filename=None, read_mode=None):
        super().__init__(filename, read_mode)


    def read_data_wrapper(self, filename, read_mode):
        raw_data = super().read_data_wrapper(filename, read_mode)
        spark = SparkSession.builder.getOrCreate()

        if read_mode == "arff":

            columns = [attr[0] for attr in raw_data["attributes"]]
            pdf = pd.DataFrame(raw_data["data"], columns=columns)
            self.df = spark.createDataFrame(pdf)

        elif read_mode == "csv":
            self.d = spark.read.csv(raw_data, header=True, inferSchema=True)


    def summary(self):
        return self.df.describe().toPandas()