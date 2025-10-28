import pandas as pd
import numpy as np
from scipy.stats import spearmanr, pearsonr


def eta_squared(x, y):
    """
    Calcula o coeficiente Eta (η) entre variável categórica x e contínua y.
    """
    grupos = [y[x == categoria] for categoria in np.unique(x)]
    ss_between = sum(len(g) * (g.mean() - y.mean())**2 for g in grupos)
    ss_total = sum((y - y.mean())**2)
    eta = np.sqrt(ss_between / ss_total)
    return eta


def get_correlation(df: pd.DataFrame, atributo: str, classe: str, tipo_atributo: str, tipo_classe: str):

    if df.empty:
        raise ValueError("O DataFrame está vazio.")
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Esperado um pandas.DataFrame, mas recebi {type(df)}")
    # 🔍 2️⃣ Verifica se as colunas existem
    if atributo not in df.columns:
        raise ValueError(f"A coluna '{atributo}' não existe no DataFrame.")
    if classe not in df.columns:
        raise ValueError(f"A coluna '{classe}' não existe no DataFrame.")

    x = df[atributo].dropna()
    y = df.loc[x.index, classe].dropna()
    
    resultado = {"atributo": atributo, "tipo": tipo_atributo, "classe": classe, "tipo": tipo_classe}

    if tipo_atributo == "nominal" and tipo_classe == "continuous":
        resultado["method"] = "Eta (nominal x continuous)"
        resultado["value"] = eta_squared(x, y)
    elif tipo_atributo == "ordinal" and tipo_classe == "continuous":
        # Codifica ordinal como números se necessário
        x_num = pd.Categorical(x).codes
        corr, pval = spearmanr(x_num, y)
        resultado["method"] = "Spearman"
        resultado["value"] = corr
        resultado["p-value"] = pval
    elif tipo_atributo == "continuous" and tipo_classe == "continuous":
        corr, pval = pearsonr(x, y)
        resultado["method"] = "Pearson"
        resultado["value"] = corr
        resultado["p-value"] = pval
    else:
        resultado["method"] = None
        resultado["value"] = None

    return resultado


# Exemplo de uso:
# df = pd.DataFrame({
#     "satisfacao": [1, 2, 3, 4, 5],
#     "renda": [2000, 2200, 2500, 3000, 3200]
#})

#resultado = spearman_corr(df, "satisfacao", "renda")
#print(f"Spearman rho = {resultado['rho']}, p-valor = {resultado['p-valor']}")

