def DataFactory(backend: str, data):
    """
    Cria um wrapper de dados baseado no backend escolhido.

    Args:
        backend (str): 'pandas' ou 'pyspark'
        data: objeto de dados correspondente ao backend
              - PandasData: pd.DataFrame
              - PySparkData: pyspark.sql.DataFrame

    Returns:
        Data: instância de PandasData ou PySparkData
    """
    if backend.lower() == "pandas":
        from .pandas_impl import PandasData
        return PandasData(data)
    elif backend.lower() == "pyspark":
        from .pyspark_impl import PySparkData
        return PySparkData(data)
    else:
        raise ValueError(f"Backend '{backend}' não suportado. Use 'pandas' ou 'pyspark'.")